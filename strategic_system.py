# strategic_system.py
import asyncio
from strategic_code import SupabaseDocumentExtractor
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

class StrategicIntelligenceSystem:
    """Your complete strategic intelligence system"""
    
    def __init__(self):
        load_dotenv()
        self.extractor = SupabaseDocumentExtractor(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
    
    async def strategic_analysis(self, query: str, context: str = None):
        """Run comprehensive strategic analysis"""
        
        print(f"🎯 Analyzing: {query}")
        
        # Semantic search for relevant documents
        results = await self.extractor.advanced_search(query)
        
        # Temporal analysis
        temporal = await self.extractor.temporal_analysis(days=30)
        
        # Metadata intelligence
        metadata = await self.extractor.metadata_intelligence()
        
        return {
            'query': query,
            'relevant_documents': len(results),
            'key_insights': [doc['title'] for doc in results[:5]],
            'temporal_trend': temporal['trend_analysis']['direction'],
            'document_coverage': metadata['coverage_analysis']['metadata_coverage'],
            'recommendation': self._generate_recommendation(results, temporal)
        }
    
    def _generate_recommendation(self, results, temporal):
        """Generate strategic recommendation"""
        
        if not results:
            return "Insufficient data - increase document ingestion"
        
        trend = temporal['trend_analysis']['direction']
        doc_count = len(results)
        
        if trend == 'up' and doc_count > 10:
            return "High confidence - execute strategy with monitoring"
        elif trend == 'stable' and doc_count > 5:
            return "Moderate confidence - proceed with validation"
        else:
            return "Low confidence - gather more intelligence"

async def main():
    """Run your strategic intelligence system"""
    
    system = StrategicIntelligenceSystem()
    
    # Run analysis
    analysis = await system.strategic_analysis(
        "market expansion opportunities competitive analysis",
        context="Q4 strategic planning"
    )
    
    print("\n🚀 STRATEGIC INTELLIGENCE REPORT")
    print("=" * 50)
    print(f"📊 Relevant Documents: {analysis['relevant_documents']}")
    print(f"📈 Trend Direction: {analysis['temporal_trend']}")
    print(f"🎯 Recommendation: {analysis['recommendation']}")
    
    print("\n🔥 Key Insights:")
    for insight in analysis['key_insights']:
        print(f"   • {insight}")

if __name__ == "__main__":
    asyncio.run(main())