# query_intelligence.py
import asyncio
from strategic_code import SupabaseDocumentExtractor
import os
from dotenv import load_dotenv

load_dotenv()

async def get_strategic_intelligence():
    """Query your strategic intelligence"""
    
    extractor = SupabaseDocumentExtractor(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    # Advanced search with filters
    results = await extractor.advanced_search(
        query="competitive advantage strategy execution",
        filters={
            'document_type': 'strategic',
            'metadata_filters': {'priority': 'high'}
        }
    )
    
    print(f"🎯 Found {len(results)} strategic documents")
    
    for doc in results[:3]:  # Top 3 results
        print(f"\n📊 {doc['title']}")
        print(f"   Type: {doc['document_type']}")
        print(f"   Content: {doc['content'][:200]}...")
    
    # Get analytics
    analytics = await extractor.get_document_analytics()
    print(f"\n📈 Intelligence Overview:")
    print(f"   • Total Documents: {analytics['total_documents']}")
    print(f"   • Document Types: {list(analytics['document_types'].keys())}")
    print(f"   • Recent Activity: {analytics['recent_activity']} docs")
    
    return results

if __name__ == "__main__":
    asyncio.run(get_strategic_intelligence())