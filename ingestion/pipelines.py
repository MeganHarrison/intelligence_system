# ingest_markdown.py - Enhanced ingestion for markdown files
import asyncio
from ..core.extractors import SupabaseDocumentExtractor, DocumentIngestionPipeline
import os
from dotenv import load_dotenv
from pathlib import Path
import re

class EnhancedDocumentIngestionPipeline(DocumentIngestionPipeline):
    """Enhanced pipeline that handles multiple file types"""
    
    async def ingest_from_folder_enhanced(self, folder_path: str, document_type: str = "general") -> list[str]:
        """Ingest documents from folder - supports .txt, .md, .markdown files"""
        
        folder = Path(folder_path)
        documents = []
        
        # Support multiple file extensions
        file_patterns = ["*.txt", "*.md", "*.markdown"]
        
        for pattern in file_patterns:
            for file_path in folder.glob(pattern):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Extract title from markdown if available
                        title = self._extract_title_from_markdown(content, file_path.stem)
                        
                        # Extract metadata from markdown frontmatter if present
                        metadata = self._extract_markdown_metadata(content)
                        metadata.update({
                            'file_size': file_path.stat().st_size,
                            'file_extension': file_path.suffix,
                            'file_modified': file_path.stat().st_mtime
                        })
                        
                        documents.append({
                            'title': title,
                            'content': content,
                            'document_type': document_type,
                            'source_file': str(file_path),
                            'metadata': metadata
                        })
                        
                        print(f"📄 Found: {title} ({file_path.suffix})")
                        
                except Exception as e:
                    print(f"❌ Error reading {file_path}: {e}")
        
        print(f"🎯 Total files found: {len(documents)}")
        return await self.extractor.ingest_documents(documents)
    
    def _extract_title_from_markdown(self, content: str, fallback: str) -> str:
        """Extract title from markdown - looks for # Title or uses filename"""
        
        # Look for first H1 header
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
        
        # Look for any header
        header_match = re.search(r'^#+\s+(.+)$', content, re.MULTILINE)
        if header_match:
            return header_match.group(1).strip()
        
        # Use filename as fallback
        return fallback.replace('_', ' ').replace('-', ' ').title()
    
    def _extract_markdown_metadata(self, content: str) -> dict:
        """Extract YAML frontmatter from markdown if present"""
        
        metadata = {}
        
        # Check for YAML frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if frontmatter_match:
            try:
                import yaml
                metadata = yaml.safe_load(frontmatter_match.group(1)) or {}
            except ImportError:
                # If yaml not available, extract key-value pairs manually
                lines = frontmatter_match.group(1).split('\n')
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()
            except Exception:
                pass
        
        # Extract section count and structure info
        sections = len(re.findall(r'^#+', content, re.MULTILINE))
        metadata['section_count'] = sections
        metadata['word_count'] = len(content.split())
        metadata['character_count'] = len(content)
        
        return metadata

async def ingest_markdown_documents():
    """Enhanced document ingestion that handles markdown files"""
    
    load_dotenv()
    
    extractor = SupabaseDocumentExtractor(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    # Use enhanced pipeline
    pipeline = EnhancedDocumentIngestionPipeline(extractor)
    
    print("🚀 ENHANCED DOCUMENT INGESTION")
    print("=" * 40)
    print("📁 Scanning for documents...")
    
    # Ingest from documents folder with enhanced support
    doc_ids = await pipeline.ingest_from_folder_enhanced(
        "./documents",
        document_type="strategic"
    )
    
    print(f"\n✅ Successfully ingested {len(doc_ids)} documents!")
    print(f"📊 Document IDs: {doc_ids[:3]}..." if len(doc_ids) > 3 else f"📊 Document IDs: {doc_ids}")
    
    # Get analytics
    analytics = await extractor.get_document_analytics()
    print(f"\n📈 UPDATED ANALYTICS:")
    print(f"   • Total Documents: {analytics['total_documents']}")
    print(f"   • Document Types: {list(analytics['document_types'].keys())}")
    print(f"   • Database Health: {analytics['database_health']}")
    
    return doc_ids

async def test_markdown_search():
    """Test searching the newly ingested markdown documents"""
    
    load_dotenv()
    
    extractor = SupabaseDocumentExtractor(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    print("\n🔍 TESTING MARKDOWN SEARCH")
    print("=" * 30)
    
    # Test search queries
    test_queries = [
        "strategic planning",
        "implementation guide", 
        "documentation",
        "setup instructions"
    ]
    
    for query in test_queries:
        results = await extractor.advanced_search(query, filters={'document_type': 'strategic'})
        print(f"🎯 Query: '{query}' → {len(results)} results")
        
        if results:
            print(f"   Top result: {results[0]['title']}")
            print(f"   Preview: {results[0]['content'][:100]}...")
        print()

if __name__ == "__main__":
    asyncio.run(ingest_markdown_documents())
    asyncio.run(test_markdown_search())