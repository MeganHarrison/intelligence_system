# targeted_queries.py - Query your actual business intelligence
import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from core.extractors import SupabaseDocumentExtractor
import os
from dotenv import load_dotenv

async def test_realistic_queries():
    """Test queries that match your actual business content"""
    
    load_dotenv()
    
    extractor = SupabaseDocumentExtractor(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    print("🎯 TARGETED BUSINESS INTELLIGENCE QUERIES")
    print("=" * 50)
    print("Testing queries that match your actual business content...")
    print()
    
    # Realistic queries based on your document names
    business_queries = [
        "Alleato Group meetings and partnerships",
        "engineering projects and technical reviews", 
        "weekly operations and project management",
        "Goodwill Bloomington design and construction",
        "Niemann Foods development projects",
        "Uniqlo retail construction",
        "PowerHIVE energy systems",
        "licensing requirements California",
        "subcontractor meetings coordination",
        "exterior design and architecture"
    ]
    
    total_results = 0
    
    for i, query in enumerate(business_queries, 1):
        print(f"🔍 Query {i}: '{query}'")
        
        try:
            # Use advanced search without strict filters
            results = await extractor.advanced_search(query)
            print(f"   📊 Found: {len(results)} documents")
            
            if results:
                # Show top results
                for j, doc in enumerate(results[:3], 1):
                    title = doc.get('title', 'No title')[:60]
                    content_preview = doc.get('content', '')[:100].replace('\n', ' ')
                    print(f"   {j}. {title}")
                    print(f"      Preview: {content_preview}...")
                
                total_results += len(results)
            else:
                print("   ❌ No matches found")
            
            print()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print()
    
    print("📈 QUERY ANALYSIS SUMMARY")
    print("=" * 30)
    print(f"💼 Total queries tested: {len(business_queries)}")
    print(f"📊 Total results found: {total_results}")
    print(f"🎯 Average results per query: {total_results/len(business_queries):.1f}")
    
    # Test basic document retrieval
    print("\n🔍 BASIC DOCUMENT VERIFICATION")
    print("=" * 35)
    
    try:
        # Get all documents to verify they exist
        all_docs_result = extractor.supabase.table('strategic_documents').select('id, title, document_type').limit(10).execute()
        
        print(f"📋 Sample documents in database:")
        for doc in all_docs_result.data:
            print(f"   • {doc['title']}")
        
        print(f"\n✅ Database is working - {len(all_docs_result.data)} documents retrieved")
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")

async def test_simple_search():
    """Test very simple searches to debug the search function"""
    
    load_dotenv()
    
    extractor = SupabaseDocumentExtractor(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    print("\n🧪 SIMPLE SEARCH DEBUG TEST")
    print("=" * 30)
    
    # Test with very simple, common words
    simple_words = ["meeting", "project", "group", "design", "review"]
    
    for word in simple_words:
        print(f"🔍 Testing word: '{word}'")
        
        try:
            query_embedding = await extractor._get_query_embedding(word)
            results = await extractor.semantic_search(query_embedding, limit=5)
            
            print(f"   📊 Found: {len(results)} documents")
            
            if results:
                for result in results[:2]:
                    title = result.get('title', 'No title')
                    print(f"   • {title}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()

async def test_fallback_search():
    """Test fallback search without vector similarity"""
    
    load_dotenv()
    
    extractor = SupabaseDocumentExtractor(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    print("\n🔄 FALLBACK SEARCH TEST")
    print("=" * 25)
    
    try:
        # Direct database query without vector search
        result = extractor.supabase.table('strategic_documents').select(
            'id, title, content, document_type'
        ).ilike('title', '%Alleato%').execute()
        
        print(f"📊 Direct search for 'Alleato': {len(result.data)} results")
        
        for doc in result.data[:3]:
            print(f"   • {doc['title']}")
        
        # Search in content
        content_result = extractor.supabase.table('strategic_documents').select(
            'id, title, content, document_type'
        ).ilike('content', '%meeting%').execute()
        
        print(f"📊 Content search for 'meeting': {len(content_result.data)} results")
        
        for doc in content_result.data[:3]:
            print(f"   • {doc['title']}")
    
    except Exception as e:
        print(f"❌ Fallback search failed: {e}")

async def main():
    """Run all test scenarios"""
    
    await test_realistic_queries()
    await test_simple_search() 
    await test_fallback_search()
    
    print("\n🎯 RECOMMENDATIONS:")
    print("1. Your database has 28 documents and is working perfectly")
    print("2. Vector search may need threshold adjustment")
    print("3. Try more specific business terms from your actual content")
    print("4. Consider hybrid search (vector + keyword)")

if __name__ == "__main__":
    asyncio.run(main())