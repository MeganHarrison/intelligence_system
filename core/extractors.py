# STRATEGIC AGENTS WITH SUPABASE VECTOR DATABASE
# Complete production-ready implementation

import asyncio
import json
import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer
import pandas as pd
from pathlib import Path
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseDocumentExtractor:
    """
    Production-ready document extractor using Supabase + pgvector
    Your strategic intelligence backbone
    """
    
    def __init__(self, supabase_url: str, supabase_key: str, embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize Supabase connection and embedding model
        
        Args:
            supabase_url: Your Supabase project URL
            supabase_key: Your Supabase service key
            embedding_model: HuggingFace model for embeddings
        """
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.embedding_model = SentenceTransformer(embedding_model)
        self.embedding_dimension = 384  # Dimension for all-MiniLM-L6-v2
        
        # Initialize database schema
        asyncio.create_task(self._ensure_tables_exist())
    
    async def _ensure_tables_exist(self):
        """Create necessary tables if they don't exist"""
        
        # Documents table with vector embeddings
        documents_table = """
        CREATE TABLE IF NOT EXISTS strategic_documents (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            document_type VARCHAR(50) DEFAULT 'general',
            source_file VARCHAR(255),
            metadata JSONB DEFAULT '{}',
            embedding VECTOR(384),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Enable pgvector extension
        enable_vector = "CREATE EXTENSION IF NOT EXISTS vector;"
        
        # Create indexes for performance
        indexes = [
            "CREATE INDEX IF NOT EXISTS strategic_documents_embedding_idx ON strategic_documents USING ivfflat (embedding vector_cosine_ops);",
            "CREATE INDEX IF NOT EXISTS strategic_documents_created_at_idx ON strategic_documents (created_at);",
            "CREATE INDEX IF NOT EXISTS strategic_documents_type_idx ON strategic_documents (document_type);",
            "CREATE INDEX IF NOT EXISTS strategic_documents_metadata_idx ON strategic_documents USING gin (metadata);"
        ]
        
        try:
            # Execute schema creation
            self.supabase.rpc('exec_sql', {'sql': enable_vector}).execute()
            self.supabase.rpc('exec_sql', {'sql': documents_table}).execute()
            
            for index in indexes:
                self.supabase.rpc('exec_sql', {'sql': index}).execute()
                
            logger.info("✅ Supabase schema initialized successfully")
            
        except Exception as e:
            logger.warning(f"Schema setup may need manual intervention: {e}")
    
    async def ingest_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Ingest documents into Supabase with vector embeddings
        
        Args:
            documents: List of docs with 'title', 'content', 'document_type', etc.
            
        Returns:
            List of document IDs
        """
        logger.info(f"🔄 Ingesting {len(documents)} documents...")
        
        doc_ids = []
        batch_size = 10  # Process in batches to avoid memory issues
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            batch_data = []
            
            for doc in batch:
                # Generate embedding
                embedding = self.embedding_model.encode(doc['content']).tolist()
                
                # Prepare document data
                doc_data = {
                    'title': doc.get('title', f"Document_{i}"),
                    'content': doc['content'],
                    'document_type': doc.get('document_type', 'general'),
                    'source_file': doc.get('source_file', ''),
                    'metadata': doc.get('metadata', {}),
                    'embedding': embedding
                }
                
                batch_data.append(doc_data)
            
            # Insert batch
            try:
                result = self.supabase.table('strategic_documents').insert(batch_data).execute()
                
                for record in result.data:
                    doc_ids.append(record['id'])
                    
                logger.info(f"✅ Batch {i//batch_size + 1} ingested successfully")
                
            except Exception as e:
                logger.error(f"❌ Error ingesting batch {i//batch_size + 1}: {e}")
                continue
        
        logger.info(f"🎯 Successfully ingested {len(doc_ids)} documents")
        return doc_ids
    
    async def _get_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for query"""
        return self.embedding_model.encode(query).tolist()
    
    async def semantic_search(self, query_embedding: List[float], limit: int = 20, 
                            document_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Perform semantic search using vector similarity
        
        Args:
            query_embedding: Query vector embedding
            limit: Maximum number of results
            document_type: Filter by document type
            
        Returns:
            List of similar documents with scores
        """
        
        # Build query with optional filtering
        query_builder = self.supabase.table('strategic_documents').select(
            'id, title, content, document_type, metadata, created_at'
        )
        
        if document_type:
            query_builder = query_builder.eq('document_type', document_type)
        
        # Use RPC for vector similarity search
        try:
            result = self.supabase.rpc('match_documents', {
                'query_embedding': query_embedding,
                'match_threshold': 0.1,  # Minimum similarity threshold
                'match_count': limit
            }).execute()
            
            return result.data
            
        except Exception as e:
            logger.error(f"❌ Semantic search error: {e}")
            
            # Fallback to regular search if RPC fails
            result = query_builder.limit(limit).execute()
            return result.data
    
    async def temporal_analysis(self, days: int = 30) -> Dict[str, Any]:
        """
        Analyze document patterns over time
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Temporal analysis insights
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Get documents from the specified period
        result = self.supabase.table('strategic_documents').select(
            'id, title, document_type, created_at, metadata'
        ).gte('created_at', cutoff_date.isoformat()).execute()
        
        documents = result.data
        
        # Analyze patterns
        analysis = {
            'total_documents': len(documents),
            'daily_breakdown': {},
            'type_distribution': {},
            'trend_analysis': {'direction': 'stable', 'velocity': 0}
        }
        
        # Group by day
        for doc in documents:
            created_date = datetime.fromisoformat(doc['created_at'].replace('Z', '+00:00')).date()
            day_key = created_date.isoformat()
            
            analysis['daily_breakdown'][day_key] = analysis['daily_breakdown'].get(day_key, 0) + 1
            analysis['type_distribution'][doc['document_type']] = analysis['type_distribution'].get(doc['document_type'], 0) + 1
        
        # Calculate trend
        if len(analysis['daily_breakdown']) > 1:
            dates = sorted(analysis['daily_breakdown'].keys())
            early_count = sum(analysis['daily_breakdown'][date] for date in dates[:len(dates)//2])
            late_count = sum(analysis['daily_breakdown'][date] for date in dates[len(dates)//2:])
            
            if late_count > early_count * 1.2:
                analysis['trend_analysis']['direction'] = 'up'
                analysis['trend_analysis']['velocity'] = (late_count - early_count) / early_count
            elif late_count < early_count * 0.8:
                analysis['trend_analysis']['direction'] = 'down'
                analysis['trend_analysis']['velocity'] = (early_count - late_count) / early_count
        
        return analysis
    
    async def metadata_intelligence(self) -> Dict[str, Any]:
        """
        Analyze document metadata patterns
        
        Returns:
            Metadata intelligence insights
        """
        
        # Get all documents with metadata
        result = self.supabase.table('strategic_documents').select(
            'id, document_type, metadata, created_at'
        ).execute()
        
        documents = result.data
        
        # Analyze metadata patterns
        metadata_keys = set()
        type_distribution = {}
        metadata_coverage = 0
        
        for doc in documents:
            doc_type = doc['document_type']
            metadata = doc.get('metadata', {})
            
            type_distribution[doc_type] = type_distribution.get(doc_type, 0) + 1
            
            if metadata:
                metadata_coverage += 1
                metadata_keys.update(metadata.keys())
        
        coverage_percentage = (metadata_coverage / len(documents)) * 100 if documents else 0
        
        return {
            'total_documents': len(documents),
            'document_types': list(type_distribution.keys()),
            'type_distribution': type_distribution,
            'metadata_structure': list(metadata_keys),
            'coverage_analysis': {
                'metadata_coverage': coverage_percentage,
                'documents_with_metadata': metadata_coverage
            }
        }
    
    async def advanced_search(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Advanced search combining semantic and metadata filtering
        
        Args:
            query: Search query
            filters: Additional filters (document_type, date_range, metadata)
            
        Returns:
            Combined search results
        """
        filters = filters or {}
        
        # Generate query embedding
        query_embedding = await self._get_query_embedding(query)
        
        # Start with semantic search
        results = await self.semantic_search(
            query_embedding,
            limit=50,  # Get more results for filtering
            document_type=filters.get('document_type')
        )
        
        # Apply additional filters
        if filters.get('date_range'):
            start_date, end_date = filters['date_range']
            results = [
                doc for doc in results
                if start_date <= datetime.fromisoformat(doc['created_at'].replace('Z', '+00:00')).date() <= end_date
            ]
        
        if filters.get('metadata_filters'):
            metadata_filters = filters['metadata_filters']
            filtered_results = []
            
            for doc in results:
                doc_metadata = doc.get('metadata', {})
                match = True
                
                for key, value in metadata_filters.items():
                    if key not in doc_metadata or doc_metadata[key] != value:
                        match = False
                        break
                
                if match:
                    filtered_results.append(doc)
            
            results = filtered_results
        
        return results[:20]  # Return top 20 results
    
    async def get_document_analytics(self) -> Dict[str, Any]:
        """Get comprehensive document analytics"""
        
        # Get basic stats
        total_result = self.supabase.table('strategic_documents').select('id', count='exact').execute()
        total_docs = total_result.count
        
        # Get type distribution
        type_result = self.supabase.table('strategic_documents').select(
            'document_type'
        ).execute()
        
        type_counts = {}
        for doc in type_result.data:
            doc_type = doc['document_type']
            type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
        
        # Get recent activity
        recent_result = self.supabase.table('strategic_documents').select(
            'created_at'
        ).gte('created_at', (datetime.now() - timedelta(days=7)).isoformat()).execute()
        
        return {
            'total_documents': total_docs,
            'document_types': type_counts,
            'recent_activity': len(recent_result.data),
            'avg_docs_per_day': len(recent_result.data) / 7,
            'database_health': 'healthy' if total_docs > 0 else 'needs_data'
        }

# ==============================================================================
# SUPABASE SETUP FUNCTIONS
# ==============================================================================

class SupabaseSetup:
    """Helper class for Supabase setup and configuration"""
    
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase = create_client(supabase_url, supabase_key)
    
    def create_match_documents_function(self):
        """Create the RPC function for vector similarity search"""
        
        function_sql = """
        CREATE OR REPLACE FUNCTION match_documents(
            query_embedding VECTOR(384),
            match_threshold FLOAT DEFAULT 0.1,
            match_count INT DEFAULT 10
        )
        RETURNS TABLE(
            id UUID,
            title TEXT,
            content TEXT,
            document_type VARCHAR(50),
            metadata JSONB,
            created_at TIMESTAMP WITH TIME ZONE,
            similarity FLOAT
        )
        LANGUAGE SQL
        AS $$
        SELECT
            strategic_documents.id,
            strategic_documents.title,
            strategic_documents.content,
            strategic_documents.document_type,
            strategic_documents.metadata,
            strategic_documents.created_at,
            1 - (strategic_documents.embedding <=> query_embedding) AS similarity
        FROM strategic_documents
        WHERE 1 - (strategic_documents.embedding <=> query_embedding) > match_threshold
        ORDER BY strategic_documents.embedding <=> query_embedding
        LIMIT match_count;
        $$;
        """
        
        try:
            self.supabase.rpc('exec_sql', {'sql': function_sql}).execute()
            logger.info("✅ Vector search function created successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error creating vector search function: {e}")
            return False
    
    def setup_row_level_security(self):
        """Setup Row Level Security policies"""
        
        policies = [
            "ALTER TABLE strategic_documents ENABLE ROW LEVEL SECURITY;",
            """
            CREATE POLICY "Enable read access for authenticated users" ON strategic_documents
            FOR SELECT USING (auth.role() = 'authenticated');
            """,
            """
            CREATE POLICY "Enable insert access for authenticated users" ON strategic_documents
            FOR INSERT WITH CHECK (auth.role() = 'authenticated');
            """,
            """
            CREATE POLICY "Enable update access for authenticated users" ON strategic_documents
            FOR UPDATE USING (auth.role() = 'authenticated');
            """
        ]
        
        for policy in policies:
            try:
                self.supabase.rpc('exec_sql', {'sql': policy}).execute()
                logger.info("✅ RLS policy applied successfully")
            except Exception as e:
                logger.warning(f"⚠️ RLS policy warning: {e}")

# ==============================================================================
# DOCUMENT INGESTION UTILITIES
# ==============================================================================

class DocumentIngestionPipeline:
    """Pipeline for ingesting various document types"""
    
    def __init__(self, extractor: SupabaseDocumentExtractor):
        self.extractor = extractor
    
    async def ingest_from_folder(self, folder_path: str, document_type: str = "general") -> List[str]:
        """Ingest all documents from a folder"""
        
        folder = Path(folder_path)
        documents = []
        
        for file_path in folder.glob("*.txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    documents.append({
                        'title': file_path.stem,
                        'content': content,
                        'document_type': document_type,
                        'source_file': str(file_path),
                        'metadata': {
                            'file_size': file_path.stat().st_size,
                            'file_modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                        }
                    })
                    
            except Exception as e:
                logger.error(f"❌ Error reading {file_path}: {e}")
        
        return await self.extractor.ingest_documents(documents)
    
    async def ingest_from_csv(self, csv_path: str, content_column: str, 
                            title_column: str = None, type_column: str = None) -> List[str]:
        """Ingest documents from CSV file"""
        
        df = pd.read_csv(csv_path)
        documents = []
        
        for _, row in df.iterrows():
            doc = {
                'title': row[title_column] if title_column else f"Document_{len(documents)}",
                'content': row[content_column],
                'document_type': row[type_column] if type_column else 'csv_import',
                'source_file': csv_path,
                'metadata': {k: v for k, v in row.items() if k not in [content_column, title_column, type_column]}
            }
            documents.append(doc)
        
        return await self.extractor.ingest_documents(documents)

# ==============================================================================
# COMPLETE USAGE EXAMPLE
# ==============================================================================

async def main():
    """Complete example of using Strategic Agents with Supabase"""
    
    print("🚀 STRATEGIC AGENTS + SUPABASE INTEGRATION")
    print("=" * 60)
    
    # Configuration
    SUPABASE_URL = "YOUR_SUPABASE_URL"  # Replace with your actual URL
    SUPABASE_KEY = "YOUR_SUPABASE_KEY"  # Replace with your actual key
    
    # Initialize components
    print("🔧 Initializing Supabase connection...")
    doc_extractor = SupabaseDocumentExtractor(SUPABASE_URL, SUPABASE_KEY)
    
    # Setup database functions
    print("🛠️ Setting up database functions...")
    setup = SupabaseSetup(SUPABASE_URL, SUPABASE_KEY)
    setup.create_match_documents_function()
    setup.setup_row_level_security()
    
    # Ingest sample documents
    print("📊 Ingesting sample documents...")
    sample_docs = [
        {
            'title': 'AI Strategy Document',
            'content': 'Our AI implementation strategy focuses on three key areas: automation, decision support, and customer experience enhancement.',
            'document_type': 'strategy',
            'metadata': {'department': 'Technology', 'priority': 'high'}
        },
        {
            'title': 'Project Management Best Practices',
            'content': 'Effective project management requires clear communication, defined milestones, and regular stakeholder updates.',
            'document_type': 'best_practices',
            'metadata': {'department': 'Operations', 'priority': 'medium'}
        }
    ]
    
    await doc_extractor.ingest_documents(sample_docs)
    
    # Initialize strategic workflow
    print("🎯 Initializing Strategic Workflow...")
    from intelligence_agent import StrategicAgentWorkflow  # Your original agent code
    
    workflow = StrategicAgentWorkflow(doc_extractor)
    
    # Run strategic analysis
    print("📈 Running Strategic Analysis...")
    results = await workflow.execute_strategic_workflow(
        query="What are our key strategic priorities and execution gaps?",
        user_intent="strategic_analysis",
        priority="high"
    )
    
    # Display results
    print("\n🎯 STRATEGIC INTELLIGENCE REPORT")
    print("=" * 40)
    
    synthesis = results['final_synthesis']
    print(f"📊 Success Probability: {synthesis['success_probability']:.1%}")
    print(f"🚀 Next Decision Point: {synthesis['next_decision_point']}")
    
    for finding in synthesis['key_findings']:
        print(f"   • {finding}")
    
    # Get analytics
    analytics = await doc_extractor.get_document_analytics()
    print(f"\n📈 DATABASE ANALYTICS")
    print(f"   • Total Documents: {analytics['total_documents']}")
    print(f"   • Document Types: {list(analytics['document_types'].keys())}")
    print(f"   • Recent Activity: {analytics['recent_activity']} docs in last 7 days")

if __name__ == "__main__":
    asyncio.run(main())