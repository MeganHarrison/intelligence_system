# business_strategic_system.py - Your Real Business Intelligence Command Center
import asyncio
from ..core.extractors import SupabaseDocumentExtractor
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

class BusinessStrategicIntelligenceSystem:
    """Strategic intelligence system tailored to your actual business operations"""
    
    def __init__(self):
        load_dotenv()
        self.extractor = SupabaseDocumentExtractor(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
    
    async def comprehensive_business_analysis(self):
        """Run comprehensive analysis across all your business areas"""
        
        print("🎯 COMPREHENSIVE BUSINESS INTELLIGENCE ANALYSIS")
        print("=" * 60)
        print("Analyzing your actual business operations and partnerships...")
        print()
        
        # Your actual business intelligence queries
        business_scenarios = [
            {
                'area': 'Partnership Management',
                'query': 'Alleato Group partnerships collaboration meetings decisions',
                'context': 'Strategic partnership coordination and outcomes'
            },
            {
                'area': 'Project Coordination', 
                'query': 'weekly operations subcontractor meetings project management',
                'context': 'Operational efficiency and project delivery'
            },
            {
                'area': 'Construction Projects',
                'query': 'Goodwill Bloomington exterior design construction development',
                'context': 'Active construction project management'
            },
            {
                'area': 'Client Development',
                'query': 'Niemann Foods development projects retail construction',
                'context': 'Client relationship and project development'
            },
            {
                'area': 'Engineering Coordination',
                'query': 'Applied Engineering technical reviews subcontractor coordination',
                'context': 'Technical project execution and quality'
            },
            {
                'area': 'Energy Systems',
                'query': 'PowerHIVE energy systems technical implementation',
                'context': 'Specialized technology and energy projects'
            }
        ]
        
        total_intelligence = 0
        business_insights = {}
        
        for scenario in business_scenarios:
            print(f"🔍 ANALYZING: {scenario['area']}")
            print(f"📋 Context: {scenario['context']}")
            
            analysis = await self.strategic_analysis(scenario['query'], scenario['context'])
            business_insights[scenario['area']] = analysis
            
            print(f"   📊 Documents Found: {analysis['relevant_documents']}")
            print(f"   📈 Trend: {analysis['temporal_trend']}")
            print(f"   🎯 Confidence: {analysis['recommendation']}")
            
            if analysis['key_insights']:
                print(f"   🔥 Top Insights:")
                for insight in analysis['key_insights'][:3]:
                    print(f"      • {insight}")
            
            total_intelligence += analysis['relevant_documents']
            print()
        
        # Generate executive summary
        await self._generate_executive_summary(business_insights, total_intelligence)
        
        return business_insights
    
    async def strategic_analysis(self, query: str, context: str = None):
        """Run strategic analysis with business context"""
        
        # Semantic search for relevant documents
        results = await self.extractor.advanced_search(query)
        
        # Temporal analysis
        temporal = await self.extractor.temporal_analysis(days=30)
        
        # Metadata intelligence
        metadata = await self.extractor.metadata_intelligence()
        
        return {
            'query': query,
            'context': context,
            'relevant_documents': len(results),
            'key_insights': [doc['title'] for doc in results[:5]],
            'temporal_trend': temporal['trend_analysis']['direction'],
            'document_coverage': metadata['coverage_analysis']['metadata_coverage'],
            'recommendation': self._generate_business_recommendation(results, temporal, context)
        }
    
    def _generate_business_recommendation(self, results, temporal, context):
        """Generate business-specific recommendations"""
        
        if not results:
            return "🔍 DISCOVERY NEEDED: Limited intelligence - expand documentation in this area"
        
        trend = temporal['trend_analysis']['direction']
        doc_count = len(results)
        
        if doc_count >= 15:
            if trend == 'up':
                return "🚀 HIGH ACTIVITY: Strong momentum - optimize and scale current operations"
            else:
                return "📊 MATURE AREA: Well-documented - focus on efficiency and optimization"
        elif doc_count >= 8:
            if trend == 'up':
                return "📈 GROWING FOCUS: Increasing activity - monitor and support expansion"
            else:
                return "⚖️ BALANCED OPERATIONS: Steady activity - maintain current approach"
        elif doc_count >= 3:
            return "🎯 TARGETED OPPORTUNITY: Moderate activity - consider strategic investment"
        else:
            return "🔍 INVESTIGATION REQUIRED: Limited data - needs strategic attention"
    
    async def _generate_executive_summary(self, business_insights, total_intelligence):
        """Generate executive-level summary of business intelligence"""
        
        print("📈 EXECUTIVE BUSINESS INTELLIGENCE SUMMARY")
        print("=" * 50)
        
        # Identify top performing areas
        sorted_areas = sorted(
            business_insights.items(), 
            key=lambda x: x[1]['relevant_documents'], 
            reverse=True
        )
        
        print(f"🎯 TOTAL BUSINESS INTELLIGENCE: {total_intelligence} strategic documents")
        print()
        
        print("🏆 TOP BUSINESS AREAS (by documentation depth):")
        for i, (area, data) in enumerate(sorted_areas[:3], 1):
            print(f"   {i}. {area}: {data['relevant_documents']} documents")
            print(f"      Status: {data['recommendation']}")
        
        print()
        print("🎯 STRATEGIC PRIORITIES:")
        
        # High-activity areas needing attention
        high_activity = [area for area, data in business_insights.items() if data['relevant_documents'] >= 10]
        if high_activity:
            print(f"   🚀 SCALE & OPTIMIZE: {', '.join(high_activity)}")
        
        # Medium-activity areas with potential
        medium_activity = [area for area, data in business_insights.items() if 5 <= data['relevant_documents'] < 10]
        if medium_activity:
            print(f"   📈 STRATEGIC INVESTMENT: {', '.join(medium_activity)}")
        
        # Low-activity areas needing development
        low_activity = [area for area, data in business_insights.items() if data['relevant_documents'] < 5]
        if low_activity:
            print(f"   🔍 DEVELOP & EXPAND: {', '.join(low_activity)}")
        
        print()
        print("💡 EXECUTIVE RECOMMENDATIONS:")
        print("   1. Leverage high-documentation areas for competitive advantage")
        print("   2. Systematize knowledge capture in growing areas") 
        print("   3. Identify expansion opportunities in under-documented areas")
        print("   4. Create cross-functional intelligence sharing protocols")
    
    async def deep_dive_analysis(self, business_area: str):
        """Deep dive into a specific business area"""
        
        area_queries = {
            'partnerships': 'Alleato Group partnerships meetings collaboration decisions outcomes',
            'operations': 'weekly operations meetings project management coordination',
            'construction': 'construction projects design exterior architecture development',
            'engineering': 'Applied Engineering technical reviews coordination subcontractor',
            'clients': 'client meetings project development business relationships',
            'energy': 'PowerHIVE energy systems technical implementation'
        }
        
        if business_area.lower() not in area_queries:
            print(f"❌ Unknown business area. Available: {list(area_queries.keys())}")
            return
        
        query = area_queries[business_area.lower()]
        
        print(f"🔬 DEEP DIVE: {business_area.upper()} INTELLIGENCE")
        print("=" * 50)
        
        # Get detailed results
        results = await self.extractor.advanced_search(query, filters={'document_type': 'strategic'})
        
        if not results:
            print("❌ No detailed intelligence found for this area")
            return
        
        print(f"📊 Found {len(results)} strategic documents")
        print()
        
        # Analyze document patterns
        print("📋 DOCUMENT ANALYSIS:")
        for i, doc in enumerate(results[:10], 1):
            title = doc['title']
            content_preview = doc.get('content', '')[:150].replace('\n', ' ')
            
            print(f"{i}. {title}")
            print(f"   Preview: {content_preview}...")
            print()
        
        # Temporal pattern analysis
        temporal = await self.extractor.temporal_analysis(days=30)
        print(f"📈 TEMPORAL INTELLIGENCE:")
        print(f"   • Activity Trend: {temporal['trend_analysis']['direction']}")
        print(f"   • Documents Last 30 Days: {temporal['total_documents']}")
        
        return results

async def main():
    """Run your business strategic intelligence system"""
    
    print("🎯 BUSINESS STRATEGIC INTELLIGENCE COMMAND CENTER")
    print("=" * 60)
    print("Welcome to your personalized business intelligence system!")
    print()
    
    system = BusinessStrategicIntelligenceSystem()
    
    print("Select analysis type:")
    print("1. Comprehensive Business Analysis (all areas)")
    print("2. Deep Dive Analysis (specific area)")
    print("3. Custom Query Analysis")
    print()
    
    choice = input("Enter choice (1-3) or press Enter for comprehensive analysis: ").strip()
    
    if choice == '2':
        print("\nAvailable areas: partnerships, operations, construction, engineering, clients, energy")
        area = input("Enter business area: ").strip()
        await system.deep_dive_analysis(area)
    
    elif choice == '3':
        query = input("Enter your custom business query: ").strip()
        if query:
            analysis = await system.strategic_analysis(query, "Custom business intelligence query")
            print(f"\n🎯 CUSTOM ANALYSIS RESULTS:")
            print(f"📊 Documents: {analysis['relevant_documents']}")
            print(f"📈 Trend: {analysis['temporal_trend']}")
            print(f"💡 Recommendation: {analysis['recommendation']}")
            print(f"🔍 Key Insights: {analysis['key_insights']}")
    
    else:
        # Default: comprehensive analysis
        await system.comprehensive_business_analysis()
    
    print("\n🎯 Business Intelligence Analysis Complete!")
    print("Your strategic intelligence system is fully operational! 🚀")

if __name__ == "__main__":
    asyncio.run(main())