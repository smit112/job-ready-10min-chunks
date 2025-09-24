# Agentic AI Configuration Research System

A comprehensive agentic AI system that leverages MCP (Model Context Protocol) and Cursor AI to streamline configuration research, automate troubleshooting, and optimize configuration validation. This system integrates Excel, PDF, and Link resources to provide intelligent configuration management capabilities.

## 🚀 Features

### Core Components

1. **Configuration Research Agent** - Main orchestrator for research tasks
2. **Excel Processor** - Handles configuration templates and validation rules
3. **PDF Parser** - Extracts error documentation and troubleshooting guides
4. **Link Analyzer** - Validates external resources and documentation
5. **Validation Engine** - Automated configuration testing and validation
6. **Troubleshooting AI** - AI-powered troubleshooting assistant
7. **Web Dashboard** - Modern web interface for system management

### Key Capabilities

- **Automated Configuration Analysis** - Process Excel files for configuration templates
- **Error Pattern Recognition** - Extract and analyze error patterns from PDFs
- **Link Validation** - Validate and analyze external documentation links
- **AI-Powered Troubleshooting** - Generate intelligent troubleshooting recommendations
- **Real-time Validation** - Comprehensive configuration validation with custom rules
- **Knowledge Base Integration** - Build and maintain troubleshooting knowledge base
- **Web Dashboard** - User-friendly interface for system management

## 📋 Prerequisites

- Python 3.8+
- pip or conda package manager
- Git (for cloning the repository)

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd agentic-ai-config-research
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

4. **Create necessary directories:**
```bash
mkdir -p data/{excel_templates,excel_output,pdf_docs,pdf_errors,link_cache,uploads}
mkdir -p logs
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Database
DATABASE_URL=sqlite:///./config_research.db
REDIS_URL=redis://localhost:6379

# AI Model Settings
DEFAULT_MODEL=gpt-4
MAX_TOKENS=4000
TEMPERATURE=0.1

# Dashboard Settings
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=8000
DEBUG=false

# Logging
LOG_LEVEL=INFO
LOG_FILE=/workspace/logs/app.log
```

### Settings Configuration

The system uses a centralized settings configuration in `configs/settings.py`. You can customize:

- File paths and directories
- AI model parameters
- Validation settings
- Dashboard configuration
- Logging settings

## 🚀 Quick Start

### 1. Start the Dashboard

```bash
cd dashboard
python app.py
```

The dashboard will be available at `http://localhost:8000`

### 2. Create a Research Task

```python
from agents.config_research_agent import ConfigResearchAgent

# Initialize the agent
agent = ConfigResearchAgent()

# Create a research task
task_id = agent.create_research_task(
    name="Database Configuration Analysis",
    description="Analyze database configuration files and validate settings",
    excel_files=["/path/to/database_config.xlsx"],
    pdf_files=["/path/to/database_errors.pdf"],
    links=["https://docs.postgresql.org/", "https://dev.mysql.com/doc/"],
    validation_rules={
        "required_fields": ["host", "port", "username", "password"],
        "port_range": {"min": 1, "max": 65535}
    }
)

# Execute the task
result = await agent.execute_research_task(task_id)
```

### 3. Create a Troubleshooting Case

```python
from agents.troubleshooting_ai import TroubleshootingAI

# Initialize the troubleshooting AI
troubleshooting_ai = TroubleshootingAI()

# Create a troubleshooting case
case_id = troubleshooting_ai.create_troubleshooting_case(
    title="Database Connection Timeout",
    description="Application cannot connect to database, getting timeout errors",
    error_messages=[
        "Connection timeout after 30 seconds",
        "Unable to establish connection to database server"
    ],
    configuration_context={
        "host": "localhost",
        "port": 5432,
        "database": "myapp",
        "timeout": 30
    },
    environment_info={
        "os": "Linux",
        "python_version": "3.9",
        "database_version": "PostgreSQL 13"
    },
    severity="high"
)

# Generate recommendations
recommendations = await troubleshooting_ai.generate_recommendations(case_id)
```

### 4. Validate Configuration

```python
from utils.validation_engine import ValidationEngine

# Initialize validation engine
validation_engine = ValidationEngine()

# Validate configuration
config_data = {
    "host": "localhost",
    "port": 5432,
    "username": "admin",
    "password": "secret123",
    "database": "myapp"
}

report = await validation_engine.validate_configuration(
    config_data=config_data,
    config_type="database",
    target_path="/path/to/config.json"
)

print(f"Validation Status: {report.overall_status}")
print(f"Passed Rules: {report.passed_rules}/{report.total_rules}")
```

## 📊 Usage Examples

### Excel Configuration Processing

```python
from utils.excel_processor import ExcelProcessor

# Initialize processor
processor = ExcelProcessor(
    templates_dir="/workspace/data/excel_templates",
    output_dir="/workspace/data/excel_output"
)

# Read Excel file
configs = processor.read_excel_file("/path/to/config.xlsx")

# Create configuration template
template_path = processor.create_configuration_template(
    template_name="database_config",
    config_schema={
        "host": {"type": "string", "required": True, "description": "Database host"},
        "port": {"type": "integer", "required": True, "description": "Database port"},
        "username": {"type": "string", "required": True, "description": "Username"},
        "password": {"type": "string", "required": True, "description": "Password"}
    }
)

# Validate configuration
validation_rules = {
    "host": {"required": True, "type": "string"},
    "port": {"required": True, "type": "integer", "min": 1, "max": 65535}
}

errors = processor.validate_configuration(config_data, validation_rules)
```

### PDF Error Analysis

```python
from utils.pdf_parser import PDFParser

# Initialize parser
parser = PDFParser(
    docs_dir="/workspace/data/pdf_docs",
    errors_dir="/workspace/data/pdf_errors"
)

# Parse PDF file
pdf_doc = parser.parse_pdf("/path/to/error_documentation.pdf")

# Extract error patterns
for error in pdf_doc.error_patterns:
    print(f"Error: {error['pattern']}")
    print(f"Severity: {error['severity']}")
    print(f"Solution: {error['solution']}")

# Extract troubleshooting steps
for step in pdf_doc.troubleshooting_steps:
    print(f"Step {step['step_number']}: {step['description']}")
    print(f"Commands: {step['commands']}")

# Search for specific errors
results = parser.search_documents(
    query="connection timeout",
    parsed_docs=[pdf_doc],
    search_type="errors"
)
```

### Link Analysis

```python
from utils.link_analyzer import LinkAnalyzer

# Initialize analyzer
analyzer = LinkAnalyzer(
    cache_dir="/workspace/data/link_cache",
    max_depth=3,
    timeout=30
)

# Analyze links
urls = [
    "https://docs.postgresql.org/",
    "https://dev.mysql.com/doc/",
    "https://docs.mongodb.com/"
]

link_infos = analyzer.analyze_links(urls, extract_content=True)

# Get domain statistics
stats = analyzer.get_domain_statistics(link_infos)
print(f"Total links analyzed: {len(link_infos)}")
print(f"Valid links: {sum(1 for link in link_infos if link.is_valid)}")

# Search links
search_results = analyzer.search_links(
    query="configuration",
    link_infos=link_infos,
    search_fields=["title", "description", "domain"]
)
```

## 🔧 API Reference

### Research Agent API

- `create_research_task()` - Create a new research task
- `execute_research_task()` - Execute a research task
- `get_task_status()` - Get task status
- `get_task_result()` - Get task results
- `list_tasks()` - List all tasks

### Troubleshooting AI API

- `create_troubleshooting_case()` - Create a troubleshooting case
- `generate_recommendations()` - Generate AI recommendations
- `search_knowledge_base()` - Search knowledge base
- `add_knowledge_base_entry()` - Add knowledge base entry

### Validation Engine API

- `validate_configuration()` - Validate configuration
- `add_validation_rule()` - Add custom validation rule
- `register_custom_validator()` - Register custom validator
- `get_validation_history()` - Get validation history

## 🌐 Web Dashboard

The web dashboard provides a modern interface for:

- **Task Management** - Create and monitor research tasks
- **Troubleshooting** - Manage troubleshooting cases and view recommendations
- **Validation** - Validate configurations and view validation history
- **Knowledge Base** - Search and manage troubleshooting knowledge
- **File Upload** - Upload Excel and PDF files for processing
- **Statistics** - View system statistics and performance metrics

### Dashboard Features

- Real-time task monitoring
- Interactive configuration validation
- AI-powered troubleshooting recommendations
- Knowledge base search and management
- File upload and processing
- Comprehensive reporting and analytics

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+)

2. **API Key Issues**
   - Verify API keys are set in `.env` file
   - Check API key permissions and quotas

3. **File Permission Errors**
   - Ensure proper permissions on data directories
   - Check file ownership and access rights

4. **Memory Issues**
   - Large PDF files may require more memory
   - Consider processing files in smaller batches

### Debug Mode

Enable debug mode for detailed logging:

```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
python dashboard/app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the GitHub repository
- Check the documentation and examples
- Review the troubleshooting section

## 🔮 Roadmap

- [ ] Enhanced AI model integration
- [ ] Real-time collaboration features
- [ ] Advanced analytics and reporting
- [ ] Integration with popular CI/CD tools
- [ ] Mobile application
- [ ] Plugin system for custom validators
- [ ] Multi-language support
- [ ] Advanced security features

## 📚 Additional Resources

- [API Documentation](http://localhost:8000/api/docs)
- [Configuration Examples](examples/)
- [Troubleshooting Guide](docs/troubleshooting.md)
- [Development Guide](docs/development.md)