# Agentic Configuration Research System

🤖 **AI-Powered Configuration Research & Troubleshooting Platform**

Leverage agentic AI (MCP & Cursor AI) to streamline configuration research, automate troubleshooting, and optimize configuration validation. This system integrates Excel files, PDF error documents, and link validation to provide comprehensive configuration analysis and automated assistance.

## 🌟 Features

### 🔧 **Core Capabilities**
- **Excel Configuration Analysis**: Extract and validate configuration data from Excel files
- **PDF Error Document Processing**: Automated analysis of error documents for troubleshooting
- **Link Validation**: Comprehensive validation of configuration URLs and resources  
- **Configuration Validation**: Automated validation against best practices and security standards
- **AI-Powered Troubleshooting**: Intelligent troubleshooting recommendations using configuration agents

### 🚀 **AI Integration**
- **MCP (Model Context Protocol)** server for seamless AI tool integration
- **Cursor AI** integration for enhanced development workflow
- **WebSocket** real-time updates and notifications
- **RESTful API** for programmatic access and automation

### 🛡️ **Security & Validation**
- Security vulnerability detection in configurations
- Hardcoded credential detection
- SSL/TLS configuration validation
- Performance optimization recommendations
- Best practice compliance checking

## 🏗️ Architecture

```
├── src/
│   ├── mcp_server/          # MCP server implementation
│   ├── agents/              # AI agents for troubleshooting
│   ├── processors/          # Data processors (Excel, PDF)
│   ├── validators/          # Validation engines
│   └── integration/         # Cursor AI integration layer
├── config/                  # Configuration files
├── data/                    # Sample data and uploads
└── tests/                   # Test suites
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip or pipenv
- Virtual environment (recommended)

### Installation

1. **Clone and Setup**
```bash
git clone <repository-url>
cd agentic-config-research
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Start the System**
```bash
# Start web server (recommended)
python main.py server

# Or start on custom port
python main.py server --port 9000

# Start MCP server only
python main.py mcp
```

3. **Access the API**
- Web API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- WebSocket: ws://localhost:8000/ws

## 📖 Usage Examples

### Command Line Interface

```bash
# Analyze Excel configuration file
python main.py analyze --excel data/sample_config.xlsx --sheet "Config"

# Analyze PDF error document
python main.py analyze --pdf data/error_report.pdf

# Validate configuration files
python main.py validate --config config/app.json

# Validate multiple links
python main.py validate --links https://api.example.com https://db.example.com

# Automated troubleshooting
python main.py troubleshoot --issue "Database connection timeout" --system-type database
```

### REST API

```bash
# Upload and analyze Excel file
curl -X POST "http://localhost:8000/upload/excel" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@config_data.xlsx"

# Perform comprehensive analysis
curl -X POST "http://localhost:8000/research" \
     -H "Content-Type: application/json" \
     -d '{
       "task_type": "comprehensive_analysis",
       "parameters": {
         "excel_files": ["data/config.xlsx"],
         "config_files": ["config/app.json"],
         "links": ["https://api.example.com"],
         "issue_description": "Performance issues with database connections"
       }
     }'

# Execute specific MCP tool
curl -X POST "http://localhost:8000/tools/process_excel_config" \
     -H "Content-Type: application/json" \
     -d '{
       "file_path": "/workspace/data/config.xlsx",
       "config_type": "database"
     }'
```

### Python API

```python
from src.integration.cursor_integration import CursorIntegration

# Initialize integration layer
integration = CursorIntegration("/workspace")

# Analyze Excel file
result = await integration._handle_excel_analysis({
    "file_path": "data/config.xlsx",
    "config_type": "network"
})

# Perform troubleshooting
result = await integration._handle_troubleshooting({
    "issue_description": "SSL certificate validation failing",
    "system_type": "security"
})
```

## 🔧 Configuration

### MCP Server Configuration
Edit `config/mcp_config.json`:

```json
{
  "mcp_server": {
    "name": "agentic-config-research",
    "tools": [
      {
        "name": "process_excel_config",
        "enabled": true,
        "timeout": 300
      }
    ]
  },
  "ai_integration": {
    "cursor_ai": {
      "enabled": true,
      "api_port": 8000
    }
  }
}
```

### Validation Rules
Customize validation rules in `config/validation_rules.yaml`:

```yaml
validation_rules:
  database:
    required_fields:
      - host
      - port
      - database
    security_requirements:
      ssl_enabled: true
```

## 🛠️ Available Tools

### MCP Tools
1. **process_excel_config** - Process Excel configuration files
2. **analyze_error_pdf** - Analyze PDF error documents  
3. **validate_configuration_links** - Validate configuration URLs
4. **automated_troubleshooting** - AI-powered troubleshooting
5. **configuration_validation** - Validate configuration files

### API Endpoints
- `POST /research` - Perform configuration research
- `POST /upload/excel` - Upload Excel files
- `POST /upload/pdf` - Upload PDF files
- `GET /tools` - List available tools
- `POST /tools/{tool_name}` - Execute specific tool
- `GET /workspace/scan` - Scan workspace for files

## 🎯 Use Cases

### 1. **Configuration Audit**
- Scan workspace for configuration files
- Validate against security best practices
- Generate compliance reports

### 2. **Troubleshooting Automation**
- Upload error PDFs for automated analysis
- Get AI-powered troubleshooting recommendations
- Track resolution progress

### 3. **Excel Configuration Management**
- Extract configuration data from Excel files
- Validate network, database, and system settings
- Identify security vulnerabilities

### 4. **Link Health Monitoring**
- Validate all URLs in configuration files
- Monitor API endpoint availability
- Track response times and failures

## 🧪 Testing

```bash
# Run basic functionality test
python main.py validate --config data/sample_config.json

# Test link validation
python main.py validate --links https://www.google.com https://github.com

# Test troubleshooting
python main.py troubleshoot --issue "Connection timeout" --system-type network
```

## 📊 Sample Data

The system includes sample data for testing:
- `data/sample_config.json` - Sample configuration file
- `data/sample_links.txt` - Sample URLs for validation
- `config/validation_rules.yaml` - Validation rule examples

## 🔒 Security Features

- **Credential Detection**: Identifies hardcoded passwords and API keys
- **SSL/TLS Validation**: Ensures secure communication settings
- **Permission Analysis**: Checks file and service permissions
- **Security Scoring**: Provides security health scores
- **Compliance Checking**: Validates against security standards

## 🚀 Performance Optimization

- **Async Processing**: Non-blocking operations for better performance
- **Concurrent Validation**: Parallel processing of multiple resources
- **Caching**: Intelligent caching of analysis results
- **Resource Monitoring**: Track system resource usage

## 🤝 Integration with Cursor AI

This system is designed to work seamlessly with Cursor AI:
- **MCP Protocol**: Standard interface for AI tool integration
- **Real-time Updates**: WebSocket notifications for live feedback
- **Context Awareness**: Maintains context across operations
- **Intelligent Recommendations**: AI-powered suggestions and solutions

## 📝 Logging

Logs are stored in the `logs/` directory:
- `agentic_config_research.log` - Main application log
- `mcp_server.log` - MCP server specific logs

Configure logging levels in the main configuration file.

## 🛟 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   python main.py server --port 9000
   ```

2. **File not found errors**
   - Ensure file paths are absolute or relative to workspace
   - Check file permissions

3. **Memory issues with large files**
   - Increase system memory limits
   - Process files in smaller chunks

### Debug Mode
```bash
python main.py server --debug
```

## 🔄 Updates and Maintenance

- Regular updates to validation rules
- Security pattern updates
- Performance optimizations
- New AI model integrations

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with FastAPI, asyncio, and modern Python practices
- Integrates with Cursor AI for enhanced development experience
- Uses industry-standard validation and security practices
