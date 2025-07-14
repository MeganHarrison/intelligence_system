# business_strategic_system.py - Your Real Business Intelligence Command Center
import asyncio
from core.extractors import SupabaseDocumentExtractor
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

class BusinessStrategicIntelligenceSystem:
    """Strategic intelligence system tailored to your actual business operations"""
    
    def __init__(self):
        load_dotenv()
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        try:
            self.extractor = SupabaseDocumentExtractor(
                self.supabase_url,
                self.supabase_key
            )
            self.connection_mode = "full"
        except Exception as e:
            logger.warning(f"Document extractor initialization failed: {e}")
            self.extractor = None
            self.connection_mode = "direct"
            # Initialize direct connection as fallback
            self._init_direct_connection()
    
    def _init_direct_connection(self):
        """Initialize direct Supabase connection as fallback"""
        try:
            from supabase import create_client
            self.supabase = create_client(self.supabase_url, self.supabase_key)
            logger.info("✅ Direct database connection established for business analysis")
        except Exception as e:
            logger.error(f"❌ Direct connection also failed: {e}")
            self.supabase = None
    
    async def comprehensive_business_analysis(self):
        """Run comprehensive analysis across all your business areas"""
        
        print("🎯 COMPREHENSIVE BUSINESS INTELLIGENCE ANALYSIS")
        print("=" * 60)
        print("Analyzing your actual business operations and partnerships...")
        print()
        
        if self.connection_mode == "direct":
            return await self._direct_business_analysis()
        else:
            return await self._full_business_analysis()
    
    async def _direct_business_analysis(self):
        """Direct database analysis when document extractor is unavailable"""
        
        if not self.supabase:
            print("❌ No database connection available")
            return {}
        
        print("🔄 Running direct database business analysis...")
        
        business_insights = {}
        total_intelligence = 0
        
        try:
            # Project Portfolio Analysis
            projects = self.supabase.table('project').select(
                'project_number, name, est_revenue, est_profits, status, phase, client_id'
            ).execute()
            
            if projects.data:
                active_projects = [p for p in projects.data if p.get('status') == 'active']
                total_revenue = sum(float(p.get('est_revenue', 0) or 0) for p in projects.data)
                
                business_insights['Project Portfolio'] = {
                    'relevant_documents': len(projects.data),
                    'key_insights': [
                        f"Total Projects: {len(projects.data)}",
                        f"Active Projects: {len(active_projects)}",
                        f"Total Revenue Pipeline: ${total_revenue:,.0f}",
                        f"Top Project: {max(projects.data, key=lambda x: float(x.get('est_revenue', 0) or 0)).get('name', 'Unknown')}"
                    ],
                    'temporal_trend': 'stable',
                    'recommendation': self._generate_project_recommendation(projects.data)
                }
                total_intelligence += len(projects.data)
                
                print(f"🔍 ANALYZING: Project Portfolio")
                print(f"   📊 Projects Found: {len(projects.data)}")
                print(f"   📈 Revenue Pipeline: ${total_revenue:,.0f}")
                print(f"   🎯 Active Projects: {len(active_projects)}")
                print()
            
            # Client Analysis
            clients = self.supabase.table('clients').select(
                'id, name, company, tier, status'
            ).execute()
            
            if clients.data:
                active_clients = [c for c in clients.data if c.get('status') != 'inactive']
                tier_distribution = {}
                for client in clients.data:
                    tier = client.get('tier', 'unknown')
                    tier_distribution[tier] = tier_distribution.get(tier, 0) + 1
                
                business_insights['Client Management'] = {
                    'relevant_documents': len(clients.data),
                    'key_insights': [
                        f"Total Clients: {len(clients.data)}",
                        f"Active Clients: {len(active_clients)}",
                        f"Tier Distribution: {tier_distribution}",
                        f"Premium Opportunity: {tier_distribution.get('standard', 0)} clients for upgrade"
                    ],
                    'temporal_trend': 'growing',
                    'recommendation': self._generate_client_recommendation(clients.data, tier_distribution)
                }
                total_intelligence += len(clients.data)
                
                print(f"🔍 ANALYZING: Client Management")
                print(f"   📊 Clients Found: {len(clients.data)}")
                print(f"   📈 Tier Distribution: {tier_distribution}")
                print()
            
            # Task Management Analysis
            tasks = self.supabase.table('tasks').select(
                'id, title, status, priority, due_date'
            ).execute()
            
            if tasks.data:
                pending_tasks = [t for t in tasks.data if t.get('status') == 'PENDING']
                high_priority = [t for t in tasks.data if t.get('priority') == 'HIGH']
                completed_tasks = [t for t in tasks.data if t.get('status') == 'COMPLETED']
                
                business_insights['Task Execution'] = {
                    'relevant_documents': len(tasks.data),
                    'key_insights': [
                        f"Total Tasks: {len(tasks.data)}",
                        f"Pending Tasks: {len(pending_tasks)}",
                        f"High Priority: {len(high_priority)}",
                        f"Completion Rate: {len(completed_tasks)/len(tasks.data)*100:.1f}%"
                    ],
                    'temporal_trend': 'active',
                    'recommendation': self._generate_task_recommendation(tasks.data)
                }
                total_intelligence += len(tasks.data)
                
                print(f"🔍 ANALYZING: Task Execution")
                print(f"   📊 Tasks Found: {len(tasks.data)}")
                print(f"   🎯 High Priority: {len(high_priority)}")
                print()
            
            # Strategic Documents Analysis
            try:
                documents = self.supabase.table('strategic_documents').select(
                    'id, title, document_type, created_at'
                ).execute()
                
                if documents.data:
                    recent_docs = [d for d in documents.data 
                                 if datetime.fromisoformat(d['created_at'].replace('Z', '+00:00')) > 
                                 datetime.now().replace(tzinfo=None) - timedelta(days=30)]
                    
                    business_insights['Strategic Documentation'] = {
                        'relevant_documents': len(documents.data),
                        'key_insights': [
                            f"Total Documents: {len(documents.data)}",
                            f"Recent Documents: {len(recent_docs)}",
                            f"Documentation Rate: {len(recent_docs)/30:.1f} docs/day"
                        ],
                        'temporal_trend': 'up' if len(recent_docs) > 15 else 'stable',
                        'recommendation': "📚 KNOWLEDGE ASSET: Strong documentation foundation supports strategic decisions"
                    }
                    total_intelligence += len(documents.data)
                    
                    print(f"🔍 ANALYZING: Strategic Documentation")
                    print(f"   📊 Documents Found: {len(documents.data)}")
                    print(f"   📈 Recent Activity: {len(recent_docs)} in last 30 days")
                    print()
            
            except Exception as e:
                logger.warning(f"Strategic documents analysis failed: {e}")
        
        except Exception as e:
            logger.error(f"❌ Direct business analysis failed: {e}")
            return self._get_fallback_analysis()
        
        # Generate executive summary
        await self._generate_direct_executive_summary(business_insights, total_intelligence)
        
        return business_insights
    
    async def _full_business_analysis(self):
        """Full analysis using document extractor"""
        
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
            
            try:
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
                
            except Exception as e:
                logger.error(f"❌ Analysis failed for {scenario['area']}: {e}")
                business_insights[scenario['area']] = {
                    'relevant_documents': 0,
                    'key_insights': [f"Analysis failed: {e}"],
                    'temporal_trend': 'unknown',
                    'recommendation': '🔧 SYSTEM CHECK: Analysis component needs attention'
                }
        
        # Generate executive summary
        await self._generate_executive_summary(business_insights, total_intelligence)
        
        return business_insights
    
    def _generate_project_recommendation(self, projects):
        """Generate recommendation based on project data"""
        if not projects:
            return "🔍 DATA NEEDED: No project data available for analysis"
        
        total_revenue = sum(float(p.get('est_revenue', 0) or 0) for p in projects)
        active_count = len([p for p in projects if p.get('status') == 'active'])
        
        if total_revenue > 50000000:  # $50M+
            return "🚀 MEGA PIPELINE: $50M+ revenue opportunity - scale execution systems"
        elif total_revenue > 10000000:  # $10M+
            return "📈 STRONG PIPELINE: Significant revenue potential - optimize delivery"
        elif active_count > 20:
            return "⚡ HIGH VELOCITY: Many active projects - focus on execution efficiency"
        else:
            return "🎯 GROWTH OPPORTUNITY: Expand pipeline development"
    
    def _generate_client_recommendation(self, clients, tier_distribution):
        """Generate recommendation based on client data"""
        standard_clients = tier_distribution.get('standard', 0)
        
        if standard_clients > 10:
            return "💎 TIER OPTIMIZATION: Major pricing opportunity - upgrade client tiers"
        elif standard_clients > 5:
            return "📈 PRICING POWER: Multiple clients ready for premium tier upgrade"
        else:
            return "🎯 CLIENT DEVELOPMENT: Focus on relationship deepening"
    
    def _generate_task_recommendation(self, tasks):
        """Generate recommendation based on task data"""
        high_priority = len([t for t in tasks if t.get('priority') == 'HIGH'])
        pending = len([t for t in tasks if t.get('status') == 'PENDING'])
        
        if high_priority > 25:
            return "🎖️ EXECUTION EXCELLENCE: High-priority focus demonstrates strategic discipline"
        elif pending > 25:
            return "⚡ EXECUTION ACCELERATION: High task volume - consider resource optimization"
        else:
            return "📊 BALANCED EXECUTION: Task management showing good control"
    
    def _get_fallback_analysis(self):
        """Fallback analysis when database is unavailable"""
        return {
            'System Status': {
                'relevant_documents': 0,
                'key_insights': [
                    "Database connection unavailable",
                    "Running in fallback mode",
                    "Core functionality preserved"
                ],
                'temporal_trend': 'maintenance',
                'recommendation': '🔧 SYSTEM MAINTENANCE: Restore database connection for full analysis'
            }
        }
    
    async def _generate_direct_executive_summary(self, business_insights, total_intelligence):
        """Generate executive summary for direct database analysis"""
        
        print("📈 EXECUTIVE BUSINESS INTELLIGENCE SUMMARY")
        print("=" * 50)
        
        # Identify top performing areas
        sorted_areas = sorted(
            business_insights.items(), 
            key=lambda x: x[1]['relevant_documents'], 
            reverse=True
        )
        
        print(f"🎯 TOTAL BUSINESS INTELLIGENCE: {total_intelligence} data points analyzed")
        print()
        
        print("🏆 TOP BUSINESS AREAS (by data depth):")
        for i, (area, data) in enumerate(sorted_areas[:3], 1):
            print(f"   {i}. {area}: {data['relevant_documents']} records")
            print(f"      Status: {data['recommendation']}")
        
        print()
        print("🎯 STRATEGIC PRIORITIES:")
        
        # Extract strategic recommendations
        for area, data in business_insights.items():
            if 'MEGA PIPELINE' in data['recommendation']:
                print(f"   🚀 SCALE OPERATIONS: {area}")
            elif 'TIER OPTIMIZATION' in data['recommendation']:
                print(f"   💎 PRICING POWER: {area}")
            elif 'EXECUTION EXCELLENCE' in data['recommendation']:
                print(f"   🎖️ MAINTAIN DISCIPLINE: {area}")
        
        print()
        print("💡 EXECUTIVE RECOMMENDATIONS:")
        print("   1. Leverage high-value project pipeline for expansion")
        print("   2. Implement client tier optimization for revenue boost") 
        print("   3. Maintain execution excellence across all areas")
        print("   4. Scale successful patterns to underperforming areas")
    
    async def strategic_analysis(self, query: str, context: str = None):
        """Run strategic analysis with business context - enhanced with error handling"""
        
        if not self.extractor:
            return {
                'query': query,
                'context': context,
                'relevant_documents': 0,
                'key_insights': ['Document extractor unavailable'],
                'temporal_trend': 'unknown',
                'document_coverage': 0,
                'recommendation': '🔧 SYSTEM CHECK: Document analysis component needs attention'
            }
        
        try:
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
            
        except Exception as e:
            logger.error(f"❌ Strategic analysis failed for query '{query}': {e}")
            return {
                'query': query,
                'context': context,
                'relevant_documents': 0,
                'key_insights': [f'Analysis error: {str(e)[:100]}'],
                'temporal_trend': 'error',
                'document_coverage': 0,
                'recommendation': '🔧 ANALYSIS ERROR: Check system connectivity and try again'
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
        
        if not self.extractor:
            print("⚠️ Document extractor unavailable - using direct database analysis")
            if self.supabase:
                try:
                    # Get related data from database
                    if business_area.lower() == 'clients':
                        results = self.supabase.table('clients').select('*').execute()
                        print(f"📊 Found {len(results.data)} client records")
                        for i, client in enumerate(results.data[:5], 1):
                            print(f"{i}. {client.get('name', 'Unknown')} - {client.get('company', 'N/A')}")
                    elif business_area.lower() == 'construction':
                        results = self.supabase.table('project').select('*').execute()
                        construction_projects = [p for p in results.data if 'construction' in p.get('name', '').lower()]
                        print(f"📊 Found {len(construction_projects)} construction projects")
                        for i, project in enumerate(construction_projects[:5], 1):
                            print(f"{i}. {project.get('name', 'Unknown')} - ${float(project.get('est_revenue', 0) or 0):,.0f}")
                    return
                except Exception as e:
                    print(f"❌ Direct database query failed: {e}")
                    return
            else:
                print("❌ No database connection available")
                return
        
        # Get detailed results using document extractor
        try:
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
            
        except Exception as e:
            logger.error(f"❌ Deep dive analysis failed: {e}")
            print(f"❌ Deep dive analysis failed: {e}")
        
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
    
    try:
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
    
    except Exception as e:
        logger.error(f"❌ Business analysis failed: {e}")
        print(f"❌ Analysis encountered an error: {e}")
        print("🔧 Try running the database diagnostics: python scripts/database_diagnostics.py")
    
    print("\n🎯 Business Intelligence Analysis Complete!")
    print("Your strategic intelligence system is fully operational! 🚀")

if __name__ == "__main__":
    asyncio.run(main())