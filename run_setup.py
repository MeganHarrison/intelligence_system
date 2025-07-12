import asyncio
from strategic_code import SupabaseDocumentExtractor, SupabaseSetup
import os
from dotenv import load_dotenv

load_dotenv()

async def setup_database():
    """Initialize your strategic intelligence database"""
    
    # Initialize extractor
    extractor = SupabaseDocumentExtractor(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    # Setup database functions
    setup = SupabaseSetup(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    # Create vector search function
    setup.create_match_documents_function()
    setup.setup_row_level_security()
    
    print("✅ Database setup complete!")
    return extractor

if __name__ == "__main__":
    asyncio.run(setup_database())