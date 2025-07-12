# smart_dedup_ingest.py - Intelligent Document Management System
import asyncio
import hashlib
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from ..core.extractors import SupabaseDocumentExtractor
from .universal import UniversalDocumentProcessor
from dotenv import load_dotenv

class SmartDocumentManager:
    """
    Intelligent document management with deduplication
    Think of this as your strategic librarian who never files the same document twice
    """
    
    def __init__(self, supabase_url: str, supabase_key: str):
        self.extractor = SupabaseDocumentExtractor(supabase_url, supabase_key)
        self.processor = UniversalDocumentProcessor()
    
    def _generate_content_hash(self, content: str) -> str:
        """Generate unique hash for content deduplication"""
        # Normalize content (remove extra whitespace, normalize line endings)
        normalized = ' '.join(content.split()).strip()
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()
    
    def _generate_file_hash(self, file_path: Path) -> str:
        """Generate hash based on file metadata for file-level deduplication"""
        file_info = f"{file_path.name}_{file_path.stat().st_size}_{file_path.stat().st_mtime}"
        return hashlib.md5(file_info.encode('utf-8')).hexdigest()
    
    async def check_document_exists(self, content_hash: str, file_hash: str, file_path: str) -> Optional[Dict]:
        """Check if document already exists using multiple strategies"""
        
        # Strategy 1: Check by content hash
        try:
            result = self.extractor.supabase.table('strategic_documents').select('*').execute()
            
            for doc in result.data:
                existing_metadata = doc.get('metadata', {})
                
                # Check content hash
                if existing_metadata.get('content_hash') == content_hash:
                    return {'type': 'content_duplicate', 'existing_doc': doc}
                
                # Check file hash
                if existing_metadata.get('file_hash') == file_hash:
                    return {'type': 'file_duplicate', 'existing_doc': doc}
                
                # Check source file path
                if doc.get('source_file') == file_path:
                    return {'type': 'path_duplicate', 'existing_doc': doc}
            
            return None
            
        except Exception as e:
            print(f"⚠️ Error checking duplicates: {e}")
            return None
    
    async def smart_ingest_document(self, file_path: Path, document_type: str = "strategic", 
                                  update_policy: str = "skip") -> Tuple[str, str]:
        """
        Smart document ingestion with deduplication
        
        update_policy options:
        - 'skip': Skip if duplicate exists
        - 'update': Update existing document if file is newer
        - 'version': Create new version with timestamp
        - 'force': Always create new document
        """
        
        print(f"🔍 Processing: {file_path.name}")
        
        # Extract content
        extracted = await self.processor.extract_text_from_file(file_path)
        if not extracted:
            return "failed", f"Could not extract content from {file_path.name}"
        
        # Generate hashes
        content_hash = self._generate_content_hash(extracted['content'])
        file_hash = self._generate_file_hash(file_path)
        
        # Check for duplicates
        duplicate_check = await self.check_document_exists(content_hash, file_hash, str(file_path))
        
        if duplicate_check and update_policy != 'force':
            existing_doc = duplicate_check['existing_doc']
            duplicate_type = duplicate_check['type']
            
            print(f"   📋 Found {duplicate_type}: {existing_doc['title']}")
            
            if update_policy == 'skip':
                return "skipped", f"Document already exists (policy: skip)"
            
            elif update_policy == 'update':
                # Check if file is newer
                file_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
                existing_created = datetime.fromisoformat(existing_doc['created_at'].replace('Z', '+00:00'))
                
                if file_modified <= existing_created:
                    return "skipped", f"Existing document is newer (policy: update)"
                
                # Update existing document
                return await self._update_existing_document(existing_doc, extracted, file_path, content_hash, file_hash)
            
            elif update_policy == 'version':
                # Create versioned document
                extracted['title'] = f"{extracted['title']} (v{datetime.now().strftime('%Y%m%d_%H%M%S')})"
                # Continue to create new document
        
        # Create new document
        return await self._create_new_document(extracted, file_path, document_type, content_hash, file_hash)
    
    async def _update_existing_document(self, existing_doc: Dict, extracted: Dict, 
                                      file_path: Path, content_hash: str, file_hash: str) -> Tuple[str, str]:
        """Update an existing document"""
        
        try:
            # Update metadata with new hashes and modification info
            updated_metadata = existing_doc.get('metadata', {})
            updated_metadata.update({
                'content_hash': content_hash,
                'file_hash': file_hash,
                'last_updated': datetime.now().isoformat(),
                'update_reason': 'file_modification',
                'previous_content_hash': updated_metadata.get('content_hash'),
                **extracted['metadata']
            })
            
            # Generate new embedding for updated content
            embedding = self.extractor.embedding_model.encode(extracted['content']).tolist()
            
            # Update the document
            update_data = {
                'title': extracted['title'],
                'content': extracted['content'],
                'metadata': updated_metadata,
                'embedding': embedding,
                'updated_at': datetime.now().isoformat()
            }
            
            result = self.extractor.supabase.table('strategic_documents').update(update_data).eq('id', existing_doc['id']).execute()
            
            print(f"   ✅ Updated existing document: {extracted['title']}")
            return "updated", f"Successfully updated document {existing_doc['id']}"
            
        except Exception as e:
            print(f"   ❌ Error updating document: {e}")
            return "failed", f"Update failed: {e}"
    
    async def _create_new_document(self, extracted: Dict, file_path: Path, document_type: str,
                                 content_hash: str, file_hash: str) -> Tuple[str, str]:
        """Create a new document"""
        
        try:
            # Add deduplication metadata
            extracted['metadata'].update({
                'content_hash': content_hash,
                'file_hash': file_hash,
                'file_size': file_path.stat().st_size,
                'file_modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                'file_extension': file_path.suffix,
                'ingestion_timestamp': datetime.now().isoformat()
            })
            
            # Create document
            document = {
                'title': extracted['title'],
                'content': extracted['content'],
                'document_type': document_type,
                'source_file': str(file_path),
                'metadata': extracted['metadata']
            }
            
            doc_ids = await self.extractor.ingest_documents([document])
            
            if doc_ids:
                print(f"   ✅ Created new document: {extracted['title']}")
                return "created", f"Successfully created document {doc_ids[0]}"
            else:
                return "failed", "Document creation failed"
                
        except Exception as e:
            print(f"   ❌ Error creating document: {e}")
            return "failed", f"Creation failed: {e}"
    
    async def smart_folder_ingest(self, folder_path: str, document_type: str = "strategic",
                                update_policy: str = "skip") -> Dict[str, Any]:
        """
        Smart folder ingestion with comprehensive duplicate handling
        """
        
        folder = Path(folder_path)
        
        print("🚀 SMART DOCUMENT INGESTION")
        print("=" * 50)
        print(f"📁 Folder: {folder_path}")
        print(f"📋 Policy: {update_policy}")
        print(f"🎯 Type: {document_type}")
        print()
        
        # Get all supported files
        all_files = list(folder.rglob('*'))
        supported_files = [f for f in all_files if f.suffix.lower() in self.processor.supported_extensions]
        
        print(f"📊 Found {len(supported_files)} supported files")
        print(f"🔧 File types: {set(f.suffix.lower() for f in supported_files)}")
        print()
        
        # Process results tracking
        results = {
            'created': [],
            'updated': [],
            'skipped': [],
            'failed': [],
            'summary': {}
        }
        
        # Process each file
        for file_path in supported_files:
            status, message = await self.smart_ingest_document(file_path, document_type, update_policy)
            
            results[status].append({
                'file': file_path.name,
                'path': str(file_path),
                'message': message
            })
        
        # Generate summary
        results['summary'] = {
            'total_files': len(supported_files),
            'created_count': len(results['created']),
            'updated_count': len(results['updated']),
            'skipped_count': len(results['skipped']),
            'failed_count': len(results['failed']),
            'success_rate': (len(results['created']) + len(results['updated'])) / len(supported_files) * 100 if supported_files else 0
        }
        
        # Print summary
        print("\n📊 INGESTION SUMMARY")
        print("=" * 30)
        print(f"✅ Created: {results['summary']['created_count']}")
        print(f"🔄 Updated: {results['summary']['updated_count']}")
        print(f"⏭️  Skipped: {results['summary']['skipped_count']}")
        print(f"❌ Failed: {results['summary']['failed_count']}")
        print(f"📈 Success Rate: {results['summary']['success_rate']:.1f}%")
        
        return results
    
    async def cleanup_duplicates(self, dry_run: bool = True) -> Dict[str, Any]:
        """
        Find and optionally remove duplicate documents
        """
        print("🔍 DUPLICATE DETECTION ANALYSIS")
        print("=" * 40)
        
        try:
            # Get all documents
            result = self.extractor.supabase.table('strategic_documents').select('*').execute()
            documents = result.data
            
            # Group by content hash
            content_groups = {}
            file_groups = {}
            path_groups = {}
            
            for doc in documents:
                metadata = doc.get('metadata', {})
                
                # Group by content hash
                content_hash = metadata.get('content_hash')
                if content_hash:
                    if content_hash not in content_groups:
                        content_groups[content_hash] = []
                    content_groups[content_hash].append(doc)
                
                # Group by file hash
                file_hash = metadata.get('file_hash')
                if file_hash:
                    if file_hash not in file_groups:
                        file_groups[file_hash] = []
                    file_groups[file_hash].append(doc)
                
                # Group by source path
                source_file = doc.get('source_file')
                if source_file:
                    if source_file not in path_groups:
                        path_groups[source_file] = []
                    path_groups[source_file].append(doc)
            
            # Find duplicates
            content_duplicates = {k: v for k, v in content_groups.items() if len(v) > 1}
            file_duplicates = {k: v for k, v in file_groups.items() if len(v) > 1}
            path_duplicates = {k: v for k, v in path_groups.items() if len(v) > 1}
            
            duplicate_analysis = {
                'total_documents': len(documents),
                'content_duplicates': len(content_duplicates),
                'file_duplicates': len(file_duplicates),
                'path_duplicates': len(path_duplicates),
                'duplicate_groups': {
                    'content': content_duplicates,
                    'file': file_duplicates,
                    'path': path_duplicates
                }
            }
            
            print(f"📊 Total documents: {len(documents)}")
            print(f"🔄 Content duplicates: {len(content_duplicates)} groups")
            print(f"📁 File duplicates: {len(file_duplicates)} groups")
            print(f"📍 Path duplicates: {len(path_duplicates)} groups")
            
            if not dry_run:
                print("\n⚠️ CLEANUP NOT IMPLEMENTED - Use dry_run=True first")
                print("Manual cleanup recommended for safety")
            
            return duplicate_analysis
            
        except Exception as e:
            print(f"❌ Error analyzing duplicates: {e}")
            return {}

async def main():
    """Demonstrate smart document management"""
    
    load_dotenv()
    
    print("🧠 SMART DOCUMENT MANAGEMENT SYSTEM")
    print("=" * 50)
    
    manager = SmartDocumentManager(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    # Demo different policies
    policies = ['skip', 'update', 'version']
    
    print("Available update policies:")
    for i, policy in enumerate(policies, 1):
        print(f"{i}. {policy}")
    
    print("\nSelect policy (1-3) or press Enter for 'skip':")
    choice = input().strip()
    
    if choice == '1':
        policy = 'skip'
    elif choice == '2':
        policy = 'update'
    elif choice == '3':
        policy = 'version'
    else:
        policy = 'skip'
    
    print(f"\n🎯 Using policy: {policy}")
    
    # Run smart ingestion
    results = await manager.smart_folder_ingest("./documents", "strategic", policy)
    
    # Show duplicate analysis
    print("\n🔍 Running duplicate analysis...")
    duplicate_analysis = await manager.cleanup_duplicates(dry_run=True)
    
    # Final analytics
    analytics = await manager.extractor.get_document_analytics()
    print(f"\n📈 FINAL DATABASE STATE:")
    print(f"   • Total Documents: {analytics['total_documents']}")
    print(f"   • Document Types: {list(analytics['document_types'].keys())}")
    print(f"   • Database Health: {analytics['database_health']}")

if __name__ == "__main__":
    asyncio.run(main())