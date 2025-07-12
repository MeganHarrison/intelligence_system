"""
Document Ingestion System
Handles processing and ingestion of various document types
"""

from .universal import UniversalDocumentProcessor, UniversalDocumentIngestion
from .deduplication import SmartDocumentManager
from .pipelines import DocumentIngestionPipeline

__all__ = [
    'UniversalDocumentProcessor',
    'UniversalDocumentIngestion',
    'SmartDocumentManager',
    'DocumentIngestionPipeline'
]