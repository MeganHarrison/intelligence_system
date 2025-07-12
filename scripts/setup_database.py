#!/usr/bin/env python3
"""
Database Setup Script
Initialize the database schema using the restructured system
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import get_settings
from core.database import EnhancedDatabaseSetup


async def main():
    """Run database setup"""
    try:
        settings = get_settings()
        print("🚀 INTELLIGENCE AGENT - DATABASE SETUP")
        print("=" * 50)
        
        setup = EnhancedDatabaseSetup()
        await setup.setup_complete_schema()
        await setup.verify_setup()
        
        print("\n✅ Database setup complete!")
        print("Next steps:")
        print("1. Run: python scripts/run_ingestion.py")
        print("2. Test with: python scripts/query_system.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)