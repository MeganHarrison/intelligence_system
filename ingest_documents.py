# ingest_documents.py
import asyncio
from strategic_code import SupabaseDocumentExtractor, DocumentIngestionPipeline
import os
from dotenv import load_dotenv

load_dotenv()

async def ingest_your_data():
    """Load your strategic documents"""
    
    extractor = SupabaseDocumentExtractor(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    pipeline = DocumentIngestionPipeline(extractor)
    
    # Ingest from folder of text files
    doc_ids = await pipeline.ingest_from_folder(
        "./documents",  # Your document folder
        document_type="strategic"
    )
    
    print(f"✅ Ingested {len(doc_ids)} documents")
    return doc_ids

if __name__ == "__main__":
    asyncio.run(ingest_your_data())