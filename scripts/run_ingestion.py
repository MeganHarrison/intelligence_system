#!/usr/bin/env python3
"""
Document Ingestion Script
Run document ingestion with the restructured system
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.settings import get_settings
from ingestion.universal import UniversalDocumentIngestion
from ingestion.deduplication import SmartDocumentManager


async def main():
    """Run document ingestion"""
    try:
        settings = get_settings()
        print("🚀 INTELLIGENCE AGENT - DOCUMENT INGESTION")
        print("=" * 50)
        
        # Choose ingestion method
        print("Select ingestion method:")
        print("1. Universal ingestion (all file types)")
        print("2. Smart deduplication ingestion")
        
        choice = input("Enter choice (1-2) or press Enter for universal: ").strip()
        
        if choice == "2":
            manager = SmartDocumentManager(
                settings.database.url,
                settings.database.key
            )
            
            print("Select update policy:")
            print("1. Skip duplicates")
            print("2. Update if newer")
            print("3. Create versions")
            
            policy_choice = input("Enter choice (1-3) or press Enter for skip: ").strip()
            policies = {"1": "skip", "2": "update", "3": "version"}
            policy = policies.get(policy_choice, "skip")
            
            results = await manager.smart_folder_ingest("./documents", "strategic", policy)
            
        else:
            ingestion = UniversalDocumentIngestion(
                settings.database.url,
                settings.database.key
            )
            
            doc_ids = await ingestion.ingest_everything("./documents", "strategic")
            print(f"✅ Successfully ingested {len(doc_ids)} documents")
        
        print("\n🎯 Ingestion complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)