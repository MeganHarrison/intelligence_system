# For CSV data
async def ingest_from_csv():
    pipeline = DocumentIngestionPipeline(extractor)
    
    doc_ids = await pipeline.ingest_from_csv(
        "your_data.csv",
        content_column="content",
        title_column="title",
        type_column="category"
    )
    
    print(f"✅ Ingested {len(doc_ids)} documents from CSV")