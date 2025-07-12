#!/usr/bin/env python3
"""
Enhanced AI Chief of Staff - Replaces your current ai_chief_of_staff.py
Now with contextual project intelligence instead of generic alerts
"""

import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client
import logging

# Import your existing components
from ..core.extractors import SupabaseDocumentExtractor
from .projects import ContextualProjectIntelligence, EnhancedCEOBriefing

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIChiefOfStaffEnhanced:
    """
    Enhanced AI Chief of Staff with contextual project intelligence
    Replaces generic alerts with specific, actionable project insights
    """
    
    def __init__(self):
        """Initialize with environment configuration"""
        load_dotenv()
        
        # Supabase configuration
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")
        
        # Initialize components
        self.supabase = create_client(self.supabase_url, self.supabase_key)
        self.doc_extractor = SupabaseDocumentExtractor(self.supabase_url, self.supabase_key)
        self.enhanced_briefing = EnhancedCEOBriefing(self.supabase, self.doc_extractor)
        
        logger.info("🚀 Enhanced AI Chief of Staff initialized")
    
    async def generate_daily_briefing(self) -> str:
        """
        Generate the enhanced daily briefing with specific project context
        This replaces your current generic briefing output
        """
        
        logger.info("📊 Generating enhanced CEO briefing...")
        
        try:
            # Generate the contextual briefing
            briefing = await self.enhanced_briefing.generate_enhanced_briefing()
            
            # Save to file (optional)
            await self._save_briefing_to_file(briefing)
            
            # Create tasks in your project management system
            await self._create_action_items()
            
            logger.info("✅ Enhanced briefing generated successfully")
            return briefing
            
        except Exception as e:
            logger.error(f"❌ Error generating briefing: {e}")
            return self._generate_fallback_briefing(str(e))
    
    async def _save_briefing_to_file(self, briefing: str):
        """Save briefing to file for record keeping"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ceo_briefing_{timestamp}.md"
        
        try:
            with open(f"briefings/{filename}", 'w', encoding='utf-8') as f:
                f.write(briefing)
            logger.info(f"📁 Briefing saved to briefings/{filename}")
        except Exception as e:
            logger.warning(f"⚠️ Could not save briefing to file: {e}")
    
    async def _create_action_items(self):
        """Create action items in the tasks table based on briefing insights"""
        
        try:
            # Get project intelligence to create specific tasks
            project_intelligence = ContextualProjectIntelligence(self.supabase)
            briefing_data = await project_intelligence.generate_executive_briefing()
            
            task_count = 0
            
            # Create tasks for critical action items
            for action in briefing_data['action_items']:
                if action['priority'] in ['critical', 'high']:
                    
                    # Find the project ID if this action relates to a specific project
                    project_id = await self._find_project_id_by_name(action.get('client', ''))
                    
                    task_data = {
                        'project_id': project_id,
                        'title': action['title'],
                        'description': action['description'],
                        'status': 'pending',
                        'priority': action['priority'],
                        'assigned_to': 'CEO',  # or specific team member
                        'due_date': self._calculate_due_date(action.get('recommended_timeline', '1 week')),
                        'metadata': {
                            'source': 'ai_chief_of_staff',
                            'category': action.get('category', 'general'),
                            'auto_generated': True,
                            'briefing_date': datetime.now().isoformat()
                        }
                    }
                    
                    # Insert task into database
                    result = self.supabase.table('tasks').insert(task_data).execute()
                    if result.data:
                        task_count += 1
                        logger.info(f"✅ Created task: {action['title']}")
            
            logger.info(f"📋 Created {task_count} action items in project management system")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not create action items: {e}")
    
    async def _find_project_id_by_name(self, client_name: str) -> str:
        """Find project ID by client name"""
        
        if not client_name:
            return None
        
        try:
            # Search for active projects for this client
            result = self.supabase.table('projects').select('id').join(
                'clients', 'client_id', 'id'
            ).filter('clients.name', 'ilike', f'%{client_name}%').filter(
                'status', 'in', ['active', 'planning']
            ).limit(1).execute()
            
            if result.data:
                return result.data[0]['id']
            
        except Exception as e:
            logger.warning(f"⚠️ Could not find project for client {client_name}: {e}")
        
        return None
    
    def _calculate_due_date(self, timeline: str) -> str:
        """Calculate due date from timeline string"""
        
        from datetime import timedelta
        
        now = datetime.now()
        
        if '24 hours' in timeline or 'immediate' in timeline.lower():
            due_date = now + timedelta(days=1)
        elif '48 hours' in timeline:
            due_date = now + timedelta(days=2)
        elif '1 week' in timeline:
            due_date = now + timedelta(weeks=1)
        elif '2 weeks' in timeline:
            due_date = now + timedelta(weeks=2)
        else:
            due_date = now + timedelta(weeks=1)  # Default to 1 week
        
        return due_date.isoformat()
    
    def _generate_fallback_briefing(self, error_msg: str) -> str:
        """Generate a fallback briefing if the main system fails"""
        
        return f"""
# 📊 CEO DAILY BRIEFING (FALLBACK MODE)

📅 **DATE:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## ⚠️ SYSTEM NOTICE

The enhanced briefing system encountered an issue and is running in fallback mode.

**Error:** {error_msg}

## 🔧 RECOMMENDED ACTIONS

1. Check database connectivity
2. Verify Supabase configuration
3. Review system logs for details
4. Contact technical team if issues persist

## 📋 MANUAL REVIEW REQUIRED

Please manually review:
- Active project statuses
- Recent meeting outcomes  
- Overdue tasks and blockers
- Budget utilization across projects

---

**Next Steps:** Resolve technical issues and re-run enhanced briefing system.
"""

    async def run_daily_automation(self):
        """Run the complete daily automation sequence"""
        
        logger.info("🎯 Starting daily AI Chief of Staff automation...")
        
        # Generate the briefing
        briefing = await self.generate_daily_briefing()
        
        # Print the briefing (same as your current script output)
        print(briefing)
        
        # Optional: Send via email, Slack, etc.
        await self._send_notifications(briefing)
        
        logger.info("🎯 Daily automation complete!")
    
    async def _send_notifications(self, briefing: str):
        """Send briefing via various channels (email, Slack, etc.)"""
        
        # Add your notification logic here
        # Example: Send to Slack, email to executives, etc.
        
        logger.info("📬 Notifications sent (implement as needed)")


class DatabaseInitializer:
    """Helper class to ensure your database schema is properly set up"""
    
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase = create_client(supabase_url, supabase_key)
    
    async def setup_enhanced_schema(self):
        """Set up the enhanced database schema if needed"""
        
        logger.info("🔧 Checking database schema...")
        
        # Check if enhanced tables exist
        try:
            # Test if our enhanced tables exist
            result = self.supabase.table('projects').select('id').limit(1).execute()
            logger.info("✅ Enhanced schema detected")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Enhanced schema not found: {e}")
            logger.info("📋 Please run the database schema setup first")
            return False
    
    async def migrate_existing_data(self):
        """Migrate data from your existing tables to enhanced schema"""
        
        logger.info("🔄 Checking for data migration opportunities...")
        
        # Add migration logic here if you have existing data
        # This would move data from strategic_documents to the new schema
        
        logger.info("✅ Data migration check complete")


# ============================================================================
# MAIN EXECUTION - Replaces your current ai_chief_of_staff.py
# ============================================================================

async def main():
    """
    Main execution function - replaces your current ai_chief_of_staff.py
    """
    
    try:
        # Initialize the enhanced system
        ai_chief = AIChiefOfStaffEnhanced()
        
        # Optional: Check database schema
        db_init = DatabaseInitializer(ai_chief.supabase_url, ai_chief.supabase_key)
        schema_ready = await db_init.setup_enhanced_schema()
        
        if not schema_ready:
            print("⚠️ Enhanced database schema not detected.")
            print("📋 Please run the database setup script first:")
            print("   python setup_enhanced_database.py")
            return
        
        # Run the daily automation
        await ai_chief.run_daily_automation()
        
    except Exception as e:
        logger.error(f"❌ Fatal error in AI Chief of Staff: {e}")
        print(f"""
❌ AI Chief of Staff encountered a fatal error:

{str(e)}

🔧 Troubleshooting Steps:
1. Check your .env file has SUPABASE_URL and SUPABASE_KEY
2. Verify database connectivity
3. Ensure enhanced schema is set up
4. Check system logs for details

📞 Contact technical support if issues persist.
""")


if __name__ == "__main__":
    # Create briefings directory if it doesn't exist
    os.makedirs("briefings", exist_ok=True)
    
    # Run the enhanced AI Chief of Staff
    asyncio.run(main())