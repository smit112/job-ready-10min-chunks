# Agentic Configuration Research System - Usage Guide

## 🎯 Overview

This guide provides detailed usage instructions for the Agentic Configuration Research System, covering all major features and integration scenarios.

## 🚀 Getting Started

### 1. Initial Setup

```bash
# Run the setup script
python setup.py

# Test the installation
python test_system.py

# Start the system
python main.py server
```

### 2. Verify Installation

Visit `http://localhost:8000` to see the API status and available tools.

## 📊 Core Features

### Excel Configuration Analysis

#### Command Line
```bash
# Basic Excel analysis
python main.py analyze --excel data/network_config.xlsx

# Specify sheet and configuration type
python main.py analyze --excel data/db_config.xlsx --sheet "Production" --config-type database
```

#### REST API
```bash
# Upload and analyze Excel file
curl -X POST "http://localhost:8000/upload/excel" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@network_config.xlsx"

# Process existing Excel file
curl -X POST "http://localhost:8000/tools/process_excel_config" \
     -H "Content-Type: application/json" \
     -d '{
       "file_path": "/workspace/data/config.xlsx",
       "sheet_name": "Config",
       "config_type": "network"
     }'
```

#### Python API
```python
from src.processors.excel_processor import ExcelProcessor

processor = ExcelProcessor()
result = await processor.process_file(
    "data/config.xlsx", 
    sheet_name="Config", 
    config_type="database"
)

print(f"Found {len(result['configuration_items'])} configuration items")
```

### PDF Error Document Analysis

#### Command Line
```bash
# Analyze PDF error document
python main.py analyze --pdf data/error_report.pdf

# Focus on specific error type
python main.py analyze --pdf data/network_errors.pdf --error-type network
```

#### REST API
```bash
# Upload and analyze PDF
curl -X POST "http://localhost:8000/upload/pdf" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@error_report.pdf"

# Analyze existing PDF
curl -X POST "http://localhost:8000/tools/analyze_error_pdf" \
     -H "Content-Type: application/json" \
     -d '{
       "file_path": "/workspace/data/errors.pdf",
       "error_type": "database",
       "extract_solutions": true
     }'
```

### Configuration Validation

#### Command Line
```bash
# Validate single configuration file
python main.py validate --config config/app.json

# Validate directory of configs
python main.py validate --config config/

# Specify format explicitly
python main.py validate --config app.yaml --format yaml
```

#### REST API
```bash
# Validate configuration
curl -X POST "http://localhost:8000/tools/configuration_validation" \
     -H "Content-Type: application/json" \
     -d '{
       "config_path": "/workspace/config/app.json",
       "validation_rules": ["security", "performance"],
       "config_format": "json"
     }'
```

### Link Validation

#### Command Line
```bash
# Validate multiple links
python main.py validate --links \
  https://api.example.com \
  https://db.example.com \
  https://monitoring.example.com

# Read links from file
python main.py validate --links $(cat data/sample_links.txt | grep -v "^#" | xargs)
```

#### REST API
```bash
# Validate links
curl -X POST "http://localhost:8000/tools/validate_configuration_links" \
     -H "Content-Type: application/json" \
     -d '{
       "links": [
         "https://api.example.com",
         "https://database.example.com"
       ],
       "check_content": true,
       "timeout": 10
     }'
```

### Automated Troubleshooting

#### Command Line
```bash
# Basic troubleshooting
python main.py troubleshoot --issue "Database connection timeout"

# Advanced troubleshooting with context
python main.py troubleshoot \
  --issue "SSL certificate validation failing" \
  --system-type security \
  --config-files config/ssl.json config/nginx.conf \
  --error-logs "SSL handshake failed" "Certificate expired"
```

#### REST API
```bash
# Automated troubleshooting
curl -X POST "http://localhost:8000/tools/automated_troubleshooting" \
     -H "Content-Type: application/json" \
     -d '{
       "issue_description": "Database connection timeout errors",
       "config_files": ["/workspace/config/database.json"],
       "error_logs": ["Connection timed out", "Max connections reached"],
       "system_type": "database"
     }'
```

## 🔧 Advanced Usage

### Comprehensive Analysis

Perform multiple analyses in a single operation:

```bash
# REST API - Comprehensive analysis
curl -X POST "http://localhost:8000/research" \
     -H "Content-Type: application/json" \
     -d '{
       "task_type": "comprehensive_analysis",
       "parameters": {
         "excel_files": ["data/network_config.xlsx", "data/db_config.xlsx"],
         "pdf_files": ["data/error_report.pdf"],
         "config_files": ["config/app.json", "config/database.yaml"],
         "links": ["https://api.example.com", "https://db.example.com"],
         "issue_description": "Performance degradation in production environment"
       },
       "priority": "high"
     }'
```

### Workspace Scanning

```bash
# Scan workspace for configuration files
curl -X GET "http://localhost:8000/workspace/scan"
```

### Real-time Updates with WebSocket

```javascript
// JavaScript WebSocket client
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received update:', data);
};

// Send analysis request
fetch('http://localhost:8000/research', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        task_type: 'excel_analysis',
        parameters: {file_path: 'data/config.xlsx'}
    })
});
```

## 🛠️ Configuration

### MCP Server Configuration

Edit `config/mcp_config.json`:

```json
{
  "mcp_server": {
    "tools": [
      {
        "name": "process_excel_config",
        "enabled": true,
        "timeout": 300
      }
    ]
  },
  "workspace": {
    "max_file_size": "50MB"
  }
}
```

### Validation Rules

Customize `config/validation_rules.yaml`:

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

### Environment Variables

Create `.env` file:

```bash
WORKSPACE_PATH=/workspace
LOG_LEVEL=INFO
API_PORT=8000
MAX_FILE_SIZE=50MB
```

## 🎯 Common Use Cases

### 1. Daily Configuration Audit

```bash
#!/bin/bash
# Daily audit script

echo "🔍 Starting daily configuration audit..."

# Scan workspace
python main.py validate --config config/

# Check critical links
python main.py validate --links \
  https://api.production.com \
  https://database.production.com

# Generate report
python main.py research --task comprehensive_analysis
```

### 2. Incident Response

```bash
# When an incident occurs:

# 1. Upload error logs (PDF)
curl -X POST "http://localhost:8000/upload/pdf" \
     -F "file=@incident_logs.pdf"

# 2. Analyze configuration
python main.py troubleshoot \
  --issue "Service unavailable errors" \
  --system-type network \
  --config-files config/nginx.conf config/app.json

# 3. Validate related links
python main.py validate --links https://api.service.com
```

### 3. Security Review

```bash
# Security-focused analysis
python main.py validate --config security/ --rules security

# Check for hardcoded credentials
python main.py analyze --excel security_configs.xlsx

# Validate SSL endpoints
python main.py validate --links \
  https://api.secure.com \
  https://auth.secure.com
```

## 📊 Understanding Results

### Excel Analysis Results

```json
{
  "extracted_data": {
    "sheet1": {
      "rows": 150,
      "columns": 8,
      "configuration_items": [
        {
          "key": "database_host",
          "value": "db.example.com",
          "type": "hostname"
        }
      ]
    }
  },
  "validation_results": {
    "security_issues": [
      {
        "type": "hardcoded_password",
        "severity": "high",
        "location": "Row 5, Column password"
      }
    ]
  }
}
```

### Configuration Validation Results

```json
{
  "summary": {
    "overall_status": "warning",
    "total_errors": 0,
    "total_warnings": 3,
    "security_score": 85,
    "performance_score": 90
  },
  "validation_results": {
    "security_validation": {
      "warnings": [
        "Hardcoded API key detected",
        "SSL not enabled for database connection"
      ]
    }
  }
}
```

### Troubleshooting Results

```json
{
  "troubleshooting_plan": {
    "immediate_actions": [
      "Check database service status",
      "Verify network connectivity"
    ],
    "investigation_steps": [
      "Review database logs",
      "Check connection pool settings"
    ],
    "estimated_time": "30-60 minutes"
  },
  "confidence_score": 0.85
}
```

## 🚨 Error Handling

### Common Error Scenarios

1. **File Not Found**
   ```json
   {
     "error": "Configuration file not found: /path/to/config.json",
     "suggestion": "Check file path and permissions"
   }
   ```

2. **Invalid Format**
   ```json
   {
     "error": "Invalid JSON format in configuration file",
     "suggestion": "Validate JSON syntax"
   }
   ```

3. **Timeout Errors**
   ```json
   {
     "error": "Request timed out after 30 seconds",
     "suggestion": "Increase timeout or check network connectivity"
   }
   ```

### Debugging

```bash
# Enable debug mode
python main.py server --debug

# Check logs
tail -f logs/agentic_config_research.log

# Test specific component
python test_system.py
```

## 🔄 Integration Patterns

### CI/CD Integration

```yaml
# GitHub Actions example
name: Configuration Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Validate configurations
        run: python main.py validate --config config/
```

### Monitoring Integration

```python
# Custom monitoring integration
import requests

def check_system_health():
    response = requests.get('http://localhost:8000/')
    return response.status_code == 200

def validate_critical_configs():
    response = requests.post('http://localhost:8000/research', json={
        'task_type': 'config_validation',
        'parameters': {'config_path': 'config/production.json'}
    })
    return response.json()
```

## 📈 Performance Optimization

### Best Practices

1. **File Size Limits**
   - Keep Excel files under 50MB
   - Process large files in chunks
   - Use streaming for PDF analysis

2. **Concurrent Processing**
   - Limit concurrent link validations
   - Use async processing for multiple files
   - Implement proper timeouts

3. **Caching**
   - Cache validation results
   - Store processed configurations
   - Implement result expiration

## 🔒 Security Considerations

1. **File Upload Security**
   - Validate file types and sizes
   - Scan for malicious content
   - Isolate processing environment

2. **API Security**
   - Implement rate limiting
   - Use authentication for sensitive operations
   - Validate all inputs

3. **Configuration Security**
   - Never log sensitive data
   - Encrypt stored configurations
   - Use secure communication channels

## 📞 Support and Troubleshooting

For issues and questions:

1. Check the logs in `logs/` directory
2. Run the test suite: `python test_system.py`
3. Enable debug mode: `--debug` flag
4. Review configuration files for syntax errors
5. Check network connectivity for link validation

## 🔄 Updates and Maintenance

Regular maintenance tasks:

```bash
# Update validation rules
vim config/validation_rules.yaml

# Clean up old logs
find logs/ -name "*.log" -mtime +7 -delete

# Update dependencies
pip install -r requirements.txt --upgrade

# Test system after updates
python test_system.py
```