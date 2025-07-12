# Intelligence Agent - Strategic AI System

A comprehensive intelligence agent system for document processing, strategic analysis, and business intelligence.

## 🏗️ Project Structure

```
intelligence_agent/
├── core/                    # Core system components
│   ├── __init__.py
│   ├── extractors.py        # Document extraction & vector search
│   ├── agents.py           # Strategic agent workflows
│   └── database.py         # Database setup & management
├── ingestion/              # Document processing & ingestion
│   ├── __init__.py
│   ├── universal.py        # Multi-format document processor
│   ├── deduplication.py    # Smart deduplication system
│   └── pipelines.py        # Ingestion pipelines
├── analysis/               # Intelligence analysis
│   ├── __init__.py
│   ├── business.py         # Business intelligence
│   ├── projects.py         # Project analytics
│   └── strategic.py        # Strategic analysis & briefings
├── scripts/                # Utility scripts
│   ├── __init__.py
│   ├── config_manager.py   # Configuration CLI tool
│   ├── setup_database.py   # Database initialization
│   ├── run_ingestion.py    # Document ingestion
│   ├── query_system.py     # Query interface
│   └── setup.py           # Installation script
├── config/                 # Configuration management
│   ├── __init__.py
│   ├── settings.py         # Main settings with profile support
│   ├── validators.py       # Configuration validation
│   └── profiles.py         # Environment-specific profiles
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_structure.py   # Structure tests
├── documents/              # Document storage
├── main.py                 # Main entry point
├── requirements.txt        # Full dependencies
├── requirements-minimal.txt # Core dependencies only
├── requirements-dev.txt    # Development dependencies
├── .env.example           # Base environment template
├── .env.development       # Development profile template
├── .env.production        # Production profile template
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Installation

Choose your installation method:

```bash
# Option 1: Automated setup
python scripts/setup.py

# Option 2: Manual installation
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Option 1: Use configuration manager (recommended)
python scripts/config_manager.py template development

# Option 2: Manual setup
cp .env.example .env

# Edit .env with your Supabase credentials
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_service_key

# Validate configuration
python scripts/config_manager.py validate
```

### 3. Database Setup

```bash
python scripts/setup_database.py
```

### 4. Document Ingestion

```bash
# Add documents to ./documents/ folder, then:
python scripts/run_ingestion.py
```

### 5. Run the System

```bash
# Main system interface
python main.py

# Or run specific queries
python scripts/query_system.py
```

## 📦 Installation Options

### Minimal Installation (Core Features)
```bash
pip install -r requirements-minimal.txt
```
Includes: Supabase, embeddings, basic document processing

### Full Installation (All Features)  
```bash
pip install -r requirements.txt
```
Includes: Word, PDF, Excel, PowerPoint, EPUB processing

### Development Installation
```bash
pip install -r requirements-dev.txt
```
Includes: Testing, linting, documentation tools

## 🔧 Features

### Document Processing
- **Universal Format Support**: PDF, Word, Excel, PowerPoint, HTML, Markdown, EPUB
- **Smart Deduplication**: Intelligent duplicate detection and management
- **Vector Embeddings**: Semantic search with sentence transformers
- **Metadata Intelligence**: Comprehensive document analysis

### Strategic Analysis
- **Multi-Agent Workflows**: Intelligence officer, strategic advisor, execution coordinator
- **Business Intelligence**: Comprehensive business analysis and insights
- **Project Analytics**: Project management and risk analysis
- **AI Briefings**: Automated CEO/executive briefings

### Configuration Management
- **Profile-Based Configuration**: Development, production, testing, staging profiles
- **Comprehensive Validation**: Automatic validation of all settings
- **CLI Management Tool**: Full-featured configuration manager
- **Environment Templates**: Profile-specific .env templates
- **Feature Flags**: Enable/disable specific functionality

## 🎯 Usage Examples

### Basic Document Search
```python
from core.extractors import SupabaseDocumentExtractor
from config.settings import get_settings

settings = get_settings()
extractor = SupabaseDocumentExtractor(
    settings.database.url,
    settings.database.key
)

# Search documents
results = await extractor.advanced_search("strategic planning")
```

### Strategic Analysis
```python
from core.agents import StrategicAgentWorkflow

workflow = StrategicAgentWorkflow(extractor)
results = await workflow.execute_strategic_workflow(
    query="What are our key execution gaps?",
    user_intent="strategic_analysis",
    priority="high"
)
```

### Business Intelligence
```python
from analysis.business import BusinessStrategicIntelligenceSystem

system = BusinessStrategicIntelligenceSystem()
insights = await system.comprehensive_business_analysis()
```

## 🧪 Testing

```bash
# Test project structure
python tests/test_structure.py

# Run with pytest (dev installation)
pytest tests/
```

## 📝 Configuration

The system uses profile-based configuration management with environment variables.

### Configuration Profiles
- **development**: Debug enabled, smaller batch sizes, relaxed security
- **production**: Optimized performance, larger batches, enhanced security
- **testing**: Fast execution, minimal features, test-specific settings
- **staging**: Production-like settings for pre-deployment testing

### Configuration Management CLI
```bash
# List available profiles
python scripts/config_manager.py list

# Show profile details
python scripts/config_manager.py show development

# Create environment template
python scripts/config_manager.py template production

# Validate configuration
python scripts/config_manager.py validate --profile production

# Export configuration
python scripts/config_manager.py export --output config.json

# Test configuration
python scripts/config_manager.py test
```

### Required Settings
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase service key

### Profile Selection
Set the `CONFIG_PROFILE` environment variable or use profile-specific .env files:
```bash
# Option 1: Set profile in environment
export CONFIG_PROFILE=production

# Option 2: Use profile-specific .env file
cp .env.production .env
```

### Key Configuration Options
- `DEBUG`: Enable debug mode
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `ENVIRONMENT`: Runtime environment
- `DB_TIMEOUT`: Database connection timeout
- `DB_BATCH_SIZE`: Database batch processing size
- `MAX_FILE_SIZE`: Maximum file size for processing
- `ENABLE_*`: Feature flags for various capabilities

See profile templates (`.env.development`, `.env.production`) for complete options.

## 🔍 Troubleshooting

### Import Errors
```bash
# Test the project structure
python tests/test_structure.py
```

### Database Issues
```bash
# Reinitialize database
python scripts/setup_database.py
```

### Missing Dependencies
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 🚀 Advanced Usage

### Custom Document Processing
```python
from ingestion.universal import UniversalDocumentProcessor

processor = UniversalDocumentProcessor()
extracted = await processor.extract_text_from_file(file_path)
```

### Smart Deduplication
```python
from ingestion.deduplication import SmartDocumentManager

manager = SmartDocumentManager(url, key)
results = await manager.smart_folder_ingest("./documents", policy="update")
```

### Project Intelligence
```python
from analysis.projects import ContextualProjectIntelligence

intelligence = ContextualProjectIntelligence(db_connection)
briefing = await intelligence.generate_executive_briefing()
```

## 📊 Performance

- **Vector Search**: Sub-second response times
- **Document Processing**: 10-50 files per minute (depending on size/type)
- **Scalability**: Handles 10K+ documents efficiently
- **Memory Usage**: Optimized batch processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Run linting: `black . && flake8`
5. Submit a pull request

## 📄 License

[Your License Here]

## 🔗 Links

- [Supabase Documentation](https://supabase.com/docs)
- [Sentence Transformers](https://www.sbert.net/)
- [Vector Database Guide](https://supabase.com/docs/guides/ai/vector-embeddings)

---

*Generated by Intelligence Agent System v1.0.0*