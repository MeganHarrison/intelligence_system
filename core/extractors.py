# UPDATED core/extractors.py - Enhanced with error handling and direct connection fallback

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
    Enhanced with MCP fallback and error handling
    """
    
    def __init__(self, supabase_url: str, supabase_key: str, embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize Supabase connection and embedding model
        
        Args:
            supabase_url: Your Supabase project URL
            supabase_key: Your Supabase service key
            embedding_model: HuggingFace model for embeddings
        """
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.embedding_model = SentenceTransformer(embedding_model)
        self.embedding_dimension = 384  # Dimension for all-MiniLM-L6-v2
        self.connection_healthy = True
        
        # Initialize database schema with error handling
        asyncio.create_task(self._ensure_tables_exist_safe())
    
    async def _ensure_tables_exist_safe(self):
        """Create necessary tables if they don't exist - with error handling"""
        try:
            await self._ensure_tables_exist()
        except Exception as e:
            logger.warning(f"Table initialization via RPC failed: {e}")
            logger.info("Attempting direct table access verification...")
            await self._verify_tables_direct()
    
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
            self.connection_healthy = True
            
        except Exception as e:
            logger.warning(f"Schema setup may need manual intervention: {e}")
            self.connection_healthy = False
            # Don't raise - let the system continue with direct table access
    
    async def _verify_tables_direct(self):
        """Verify tables exist using direct table access"""
        try:
            # Test direct table access
            result = self.supabase.table('strategic_documents').select('id').limit(1).execute()
            logger.info("✅ Direct table access working - strategic_documents accessible")
            self.connection_healthy = True
        except Exception as e:
            logger.warning(f"Direct table access also failed: {e}")
            self.connection_healthy = False
    
    async def ingest_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Ingest documents into Supabase with vector embeddings
        Enhanced with error handling and retry logic
        """
        logger.info(f"🔄 Ingesting {len(documents)} documents...")
        
        doc_ids = []
        batch_size = 10  # Process in batches to avoid memory issues
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            batch_data = []
            
            for doc in batch:
                try:
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
                    
                except Exception as e:
                    logger.error(f"❌ Error processing document {i}: {e}")
                    continue
            
            # Insert batch with error handling
            if batch_data:
                try:
                    result = self.supabase.table('strategic_documents').insert(batch_data).execute()
                    
                    for record in result.data:
                        doc_ids.append(record['id'])
                        
                    logger.info(f"✅ Batch {i//batch_size + 1} ingested successfully")
                    
                except Exception as e:
                    logger.error(f"❌ Error ingesting batch {i//batch_size + 1}: {e}")
                    # Try individual inserts as fallback
                    for doc_data in batch_data:
                        try:
                            result = self.supabase.table('strategic_documents').insert(doc_data).execute()
                            if result.data:
                                doc_ids.append(result.data[0]['id'])
                        except Exception as individual_error:
                            logger.error(f"❌ Individual document insert failed: {individual_error}")
                            continue
        
        logger.info(f"🎯 Successfully ingested {len(doc_ids)} documents")
        return doc_ids
    
    async def _get_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for query with error handling"""
        try:
            return self.embedding_model.encode(query).tolist()
        except Exception as e:
            logger.error(f"❌ Error generating query embedding: {e}")
            # Return a zero vector as fallback
            return [0.0] * self.embedding_dimension
    
    async def semantic_search(self, query_embedding: List[float], limit: int = 20, 
                            document_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Perform semantic search using vector similarity
        Enhanced with multiple fallback strategies
        """
        
        # First try: Use RPC for vector similarity search
        try:
            result = self.supabase.rpc('match_documents', {
                'query_embedding': query_embedding,
                'match_threshold': 0.1,
                'match_count': limit
            }).execute()
            
            if result.data:
                return result.data
                
        except Exception as e:
            logger.warning(f"❌ Vector similarity search failed: {e}")
        
        # Second try: Direct table query with filters
        try:
            query_builder = self.supabase.table('strategic_documents').select(
                'id, title, content, document_type, metadata, created_at'
            )
            
            if document_type:
                query_builder = query_builder.eq('document_type', document_type)
            
            result = query_builder.limit(limit).execute()
            
            if result.data:
                logger.info(f"✅ Fallback search returned {len(result.data)} results")
                return result.data
                
        except Exception as e:
            logger.warning(f"❌ Fallback search also failed: {e}")
        
        # Third try: Return empty results but don't crash
        logger.warning("⚠️ All search methods failed - returning empty results")
        return []
    
    async def temporal_analysis(self, days: int = 30) -> Dict[str, Any]:
        """
        Analyze document patterns over time
        Enhanced with error handling
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Get documents from the specified period
            result = self.supabase.table('strategic_documents').select(
                'id, title, document_type, created_at, metadata'
            ).gte('created_at', cutoff_date.isoformat()).execute()
            
            documents = result.data
            
        except Exception as e:
            logger.error(f"❌ Temporal analysis query failed: {e}")
            # Return mock data structure
            return {
                'total_documents': 0,
                'daily_breakdown': {},
                'type_distribution': {},
                'trend_analysis': {'direction': 'unknown', 'velocity': 0},
                'error': str(e)
            }
        
        # Analyze patterns
        analysis = {
            'total_documents': len(documents),
            'daily_breakdown': {},
            'type_distribution': {},
            'trend_analysis': {'direction': 'stable', 'velocity': 0}
        }
        
        try:
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
        
        except Exception as e:
            logger.error(f"❌ Temporal analysis processing failed: {e}")
            analysis['error'] = str(e)
        
        return analysis
    
    async def metadata_intelligence(self) -> Dict[str, Any]:
        """
        Analyze document metadata patterns
        Enhanced with error handling
        """
        
        try:
            # Get all documents with metadata
            result = self.supabase.table('strategic_documents').select(
                'id, document_type, metadata, created_at'
            ).execute()
            
            documents = result.data
            
        except Exception as e:
            logger.error(f"❌ Metadata intelligence query failed: {e}")
            return {
                'total_documents': 0,
                'document_types': [],
                'type_distribution': {},
                'metadata_structure': [],
                'coverage_analysis': {
                    'metadata_coverage': 0,
                    'documents_with_metadata': 0
                },
                'error': str(e)
            }
        
        # Analyze metadata patterns
        metadata_keys = set()
        type_distribution = {}
        metadata_coverage = 0
        
        try:
            for doc in documents:
                doc_type = doc['document_type']
                metadata = doc.get('metadata', {})
                
                type_distribution[doc_type] = type_distribution.get(doc_type, 0) + 1
                
                if metadata:
                    metadata_coverage += 1
                    metadata_keys.update(metadata.keys())
        
        except Exception as e:
            logger.error(f"❌ Metadata analysis processing failed: {e}")
        
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
        Enhanced with multiple fallback strategies
        """
        filters = filters or {}
        
        try:
            # Generate query embedding
            query_embedding = await self._get_query_embedding(query)
            
            # Start with semantic search
            results = await self.semantic_search(
                query_embedding,
                limit=50,  # Get more results for filtering
                document_type=filters.get('document_type')
            )
            
        except Exception as e:
            logger.error(f"❌ Advanced search failed: {e}")
            # Fallback to basic text search
            try:
                query_builder = self.supabase.table('strategic_documents').select('*')
                
                # Simple text search in title and content
                query_builder = query_builder.or_(f'title.ilike.%{query}%,content.ilike.%{query}%')
                
                if filters.get('document_type'):
                    query_builder = query_builder.eq('document_type', filters['document_type'])
                
                result = query_builder.limit(20).execute()
                results = result.data
                
            except Exception as fallback_error:
                logger.error(f"❌ Fallback search also failed: {fallback_error}")
                return []
        
        # Apply additional filters
        try:
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
        
        except Exception as e:
            logger.error(f"❌ Filter application failed: {e}")
        
        return results[:20]  # Return top 20 results
    
    async def get_document_analytics(self) -> Dict[str, Any]:
        """Get comprehensive document analytics with error handling"""
        
        try:
            # Get basic stats
            total_result = self.supabase.table('strategic_documents').select('id', count='exact').execute()
            total_docs = total_result.count if total_result.count else 0
            
            # Get type distribution
            type_result = self.supabase.table('strategic_documents').select('document_type').execute()
            
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
                'database_health': 'healthy' if total_docs > 0 else 'needs_data',
                'connection_status': 'healthy' if self.connection_healthy else 'degraded'
            }
            
        except Exception as e:
            logger.error(f"❌ Document analytics failed: {e}")
            return {
                'total_documents': 0,
                'document_types': {},
                'recent_activity': 0,
                'avg_docs_per_day': 0,
                'database_health': 'error',
                'connection_status': 'failed',
                'error': str(e)
            }

# Rest of the file remains the same (SupabaseSetup, DocumentIngestionPipeline, etc.)
# ... (keeping the rest of the original code)