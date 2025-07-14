#!/usr/bin/env python3
"""
Direct Database Connection Fix - scripts/database_direct_connection.py
Bypass MCP server issues and connect directly to your database
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

class DirectDatabaseConnection:
    """Direct database connection bypassing MCP server"""
    
    def __init__(self):
        load_dotenv()
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        self.supabase = None
        
    async def initialize(self):
        """Initialize direct Supabase connection"""
        try:
            from supabase import create_client
            
            if not self.supabase_url or not self.supabase_key:
                raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")
            
            self.supabase = create_client(self.supabase_url, self.supabase_key)
            print("✅ Direct database connection established")
            return True
            
        except ImportError:
            print("❌ Supabase package not installed. Run: pip install supabase")
            return False
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    async def list_tables(self):
        """List available tables in your database"""
        if not self.supabase:
            print("❌ Database not connected")
            return []
        
        # Common tables from your schema
        tables_to_check = [
            'strategic_documents', 'clients', 'project', 'tasks', 'meetings',
            'project_reports', 'employees', 'credit_card_transactions'
        ]
        
        existing_tables = []
        
        for table in tables_to_check:
            try:
                result = self.supabase.table(table).select('*').limit(1).execute()
                existing_tables.append({
                    'table_name': table,
                    'status': 'accessible',
                    'record_count': len(result.data)
                })
            except Exception as e:
                existing_tables.append({
                    'table_name': table,
                    'status': f'error: {str(e)[:50]}',
                    'record_count': 0
                })
        
        return existing_tables
    
    async def execute_query(self, table_name: str, select_fields: str = "*", limit: int = 10, filters: Dict = None):
        """Execute a query safely using Supabase table interface"""
        if not self.supabase:
            print("❌ Database not connected")
            return None
            
        try:
            query = self.supabase.table(table_name).select(select_fields)
            
            # Apply filters if provided
            if filters:
                for field, value in filters.items():
                    query = query.eq(field, value)
            
            # Apply limit
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            return result.data
                
        except Exception as e:
            print(f"❌ Query execution failed: {e}")
            return None

    async def get_business_intelligence(self):
        """Get your actual business intelligence data"""
        print("📊 EXTRACTING BUSINESS INTELLIGENCE")
        print("=" * 45)
        
        intelligence = {}
        
        # Project Portfolio Analysis
        projects = await self.execute_query('project', 
            'project_number, name, est_revenue, est_profits, status, phase, client_id', 
            limit=50)
        
        if projects:
            total_revenue = sum(float(p.get('est_revenue', 0) or 0) for p in projects)
            active_projects = [p for p in projects if p.get('status') == 'active']
            
            intelligence['portfolio'] = {
                'total_projects': len(projects),
                'active_projects': len(active_projects),
                'total_revenue_pipeline': total_revenue,
                'top_projects': sorted(projects, 
                    key=lambda x: float(x.get('est_revenue', 0) or 0), 
                    reverse=True)[:5]
            }
            
            print(f"✅ Portfolio: {len(projects)} projects, ${total_revenue:,.0f} pipeline")
        
        # Client Analysis
        clients = await self.execute_query('clients', 
            'id, name, company, tier, status', 
            limit=50)
        
        if clients:
            intelligence['clients'] = {
                'total_clients': len(clients),
                'active_clients': len([c for c in clients if c.get('status') == 'active']),
                'tier_distribution': {}
            }
            
            # Count tier distribution
            for client in clients:
                tier = client.get('tier', 'unknown')
                intelligence['clients']['tier_distribution'][tier] = \
                    intelligence['clients']['tier_distribution'].get(tier, 0) + 1
            
            print(f"✅ Clients: {len(clients)} total clients")
        
        # Task Management
        tasks = await self.execute_query('tasks', 
            'id, title, status, priority, due_date', 
            limit=100)
        
        if tasks:
            intelligence['tasks'] = {
                'total_tasks': len(tasks),
                'pending_tasks': len([t for t in tasks if t.get('status') == 'PENDING']),
                'high_priority': len([t for t in tasks if t.get('priority') == 'HIGH']),
                'completed_tasks': len([t for t in tasks if t.get('status') == 'COMPLETED'])
            }
            
            print(f"✅ Tasks: {len(tasks)} total tasks")
        
        # Strategic Documents
        documents = await self.execute_query('strategic_documents', 
            'id, title, document_type, created_at', 
            limit=50)
        
        if documents:
            intelligence['documents'] = {
                'total_documents': len(documents),
                'recent_documents': len([d for d in documents 
                    if d.get('created_at') and 
                    datetime.fromisoformat(d['created_at'].replace('Z', '+00:00')) > 
                    datetime.now().replace(tzinfo=None) - timedelta(days=30)])
            }
            
            print(f"✅ Documents: {len(documents)} strategic documents")
        
        return intelligence

    async def get_strategic_insights(self):
        """Generate strategic insights from your data"""
        intelligence = await self.get_business_intelligence()
        
        print("\n🎯 STRATEGIC INSIGHTS")
        print("=" * 25)
        
        insights = []
        
        # Portfolio insights
        if 'portfolio' in intelligence:
            portfolio = intelligence['portfolio']
            revenue = portfolio['total_revenue_pipeline']
            
            if revenue > 50000000:  # $50M+
                insights.append(f"🚀 MASSIVE PIPELINE: ${revenue:,.0f} revenue opportunity")
            elif revenue > 10000000:  # $10M+
                insights.append(f"📈 STRONG PIPELINE: ${revenue:,.0f} revenue potential")
            
            if portfolio['active_projects'] > 20:
                insights.append(f"⚡ HIGH VELOCITY: {portfolio['active_projects']} active projects")
        
        # Client insights
        if 'clients' in intelligence:
            clients = intelligence['clients']
            tier_dist = clients['tier_distribution']
            
            if 'standard' in tier_dist and tier_dist['standard'] > 0:
                premium_opportunity = tier_dist['standard'] * 0.25  # 25% pricing uplift
                insights.append(f"💎 PRICING OPPORTUNITY: {tier_dist['standard']} clients ready for tier upgrade")
        
        # Task execution insights
        if 'tasks' in intelligence:
            tasks = intelligence['tasks']
            completion_rate = tasks['completed_tasks'] / tasks['total_tasks'] if tasks['total_tasks'] > 0 else 0
            
            if completion_rate > 0.8:
                insights.append("🎖️ EXECUTION EXCELLENCE: High task completion rate")
            elif tasks['pending_tasks'] > 20:
                insights.append("⚠️ EXECUTION BOTTLENECK: High pending task volume")
        
        # Print insights
        for insight in insights:
            print(f"   {insight}")
        
        return insights

async def main():
    """Test the direct database connection"""
    print("🚀 DIRECT DATABASE CONNECTION TEST")
    print("=" * 50)
    
    # Initialize connection
    db = DirectDatabaseConnection()
    
    if not await db.initialize():
        print("❌ Failed to initialize database connection")
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Check your .env file has SUPABASE_URL and SUPABASE_KEY")
        print("2. Verify credentials are correct")
        print("3. Ensure Supabase project is accessible")
        return
    
    # List available tables
    print("\n📋 CHECKING AVAILABLE TABLES:")
    tables = await db.list_tables()
    
    accessible_count = 0
    for table in tables:
        status = table.get('status', 'unknown')
        name = table.get('table_name', 'unknown')
        
        if status == 'accessible':
            print(f"✅ {name}")
            accessible_count += 1
        else:
            print(f"❌ {name} - {status}")
    
    print(f"\n📊 Accessibility: {accessible_count}/{len(tables)} tables accessible")
    
    if accessible_count == 0:
        print("❌ No tables accessible - check database permissions")
        return
    
    # Test business intelligence extraction
    print("\n🧠 TESTING BUSINESS INTELLIGENCE EXTRACTION:")
    intelligence = await db.get_business_intelligence()
    
    # Generate strategic insights
    insights = await db.get_strategic_insights()
    
    print("\n🎯 CONNECTION TEST RESULTS:")
    print("=" * 35)
    
    if accessible_count > 5 and intelligence:
        print("✅ SUCCESS: Direct database connection working perfectly!")
        print("💡 You can now bypass MCP server issues")
        print("🚀 Your intelligence system can use this direct connection")
        
        print("\n📈 BUSINESS DATA SUMMARY:")
        if 'portfolio' in intelligence:
            portfolio = intelligence['portfolio']
            print(f"   Projects: {portfolio['total_projects']} (${portfolio['total_revenue_pipeline']:,.0f} pipeline)")
        
        if 'clients' in intelligence:
            print(f"   Clients: {intelligence['clients']['total_clients']} active relationships")
        
        if 'tasks' in intelligence:
            print(f"   Tasks: {intelligence['tasks']['total_tasks']} in management system")
        
        print("\n🔧 NEXT STEPS:")
        print("1. Update your core components to use direct connection as fallback")
        print("2. Add error handling to existing MCP calls")
        print("3. Test your main intelligence system: python main.py")
        
    else:
        print("⚠️ PARTIAL SUCCESS: Some connectivity issues remain")
        print("🔧 Continue troubleshooting database permissions and configuration")

if __name__ == "__main__":
    from datetime import timedelta
    asyncio.run(main())