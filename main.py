#!/usr/bin/env python3
"""
Intelligence Agent - Main Entry Point
Restructured intelligence agent system
"""

import asyncio
import os
import sys
from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import get_settings, setup_logging, print_configuration_summary
from config.validators import ConfigValidationError
from core.extractors import SupabaseDocumentExtractor
from core.agents import StrategicAgentWorkflow
from analysis.business import BusinessStrategicIntelligenceSystem
from analysis.strategic import AIChiefOfStaffEnhanced


async def run_strategic_analysis():
    """Run strategic analysis workflow"""
    settings = get_settings()
    
    # Initialize components
    doc_extractor = SupabaseDocumentExtractor(
        settings.database.url,
        settings.database.key,
        settings.embedding.model_name
    )
    
    workflow = StrategicAgentWorkflow(doc_extractor)
    
    print("🎯 Running Strategic Analysis...")
    
    # Example analysis
    results = await workflow.execute_strategic_workflow(
        query="What are our key strategic priorities and execution gaps?",
        user_intent="strategic_analysis",
        priority="high"
    )
    
    # Display results
    synthesis = results['final_synthesis']
    print(f"\n📊 Success Probability: {synthesis['success_probability']:.1%}")
    print(f"🚀 Next Decision Point: {synthesis['next_decision_point']}")
    
    for finding in synthesis['key_findings']:
        print(f"   • {finding}")


async def run_business_intelligence():
    """Run business intelligence analysis"""
    print("📈 Running Business Intelligence Analysis...")
    
    system = BusinessStrategicIntelligenceSystem()
    insights = await system.comprehensive_business_analysis()
    
    return insights


async def run_ai_briefing():
    """Run AI Chief of Staff briefing"""
    settings = get_settings()
    
    print("📋 Generating AI Chief of Staff Briefing...")
    
    ai_chief = AIChiefOfStaffEnhanced()
    briefing = await ai_chief.generate_daily_briefing()
    
    print(briefing)


async def main():
    """Main application entry point"""
    print("🚀 INTELLIGENCE AGENT SYSTEM")
    print("=" * 50)
    
    try:
        # Check configuration
        profile = os.getenv('CONFIG_PROFILE', 'development')
        print(f"🔧 Loading configuration profile: {profile}")
        
        settings = get_settings(profile)
        setup_logging(settings)
        
        print(f"✅ Configuration loaded (Environment: {settings.environment})")
        
        # Show configuration summary if in debug mode
        if settings.debug:
            print()
            print_configuration_summary(settings)
        
        # Show menu
        print("\nSelect operation:")
        print("1. Strategic Analysis Workflow")
        print("2. Business Intelligence Analysis") 
        print("3. AI Chief of Staff Briefing")
        print("4. Run All Systems")
        
        choice = input("\nEnter choice (1-4) or press Enter for strategic analysis: ").strip()
        
        if choice == "2":
            await run_business_intelligence()
        elif choice == "3":
            await run_ai_briefing()
        elif choice == "4":
            print("🔄 Running all systems...")
            await run_strategic_analysis()
            await run_business_intelligence()
            await run_ai_briefing()
        else:
            await run_strategic_analysis()
        
        print("\n🎯 Analysis complete!")
        
    except (ValueError, ConfigValidationError) as e:
        print(f"❌ Configuration Error: {e}")
        print("\n🔧 Setup required:")
        print("1. Copy .env.example to .env")
        print("2. Configure SUPABASE_URL and SUPABASE_KEY")
        print("3. Run: python scripts/config_manager.py validate")
        print("4. Run: python scripts/setup_database.py")
        return 1
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)