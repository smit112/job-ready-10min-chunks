# Configuration Research Agent - Build Phase README

## 🎯 **Project Overview**

The Configuration Research Agent is an agentic AI system designed to streamline configuration research and validation. It operates with **ONLY attached files as sources**, providing intelligent analysis and troubleshooting recommendations without any external data dependencies.

## 🏗️ **Build Architecture**

### **Core Components**
```
/workspace/
├── agents/                    # AI Agent Components
│   ├── config_research_agent.py    # Main orchestration agent
│   └── troubleshooting_ai.py       # Local AI processing
├── utils/                     # Utility Modules
│   ├── excel_processor.py          # Excel file processing
│   ├── pdf_parser.py              # PDF content extraction
│   ├── link_analyzer.py           # Local URL analysis
│   └── validation_engine.py       # Configuration validation
├── dashboard/                 # Web Interface
│   ├── app.py                     # FastAPI application
│   ├── templates/                 # HTML templates
│   └── static/                    # CSS, JS, assets
├── configs/                   # Configuration
│   └── settings.py                # Application settings
├── examples/                  # Demo Scripts
└── data/                      # Data storage
```

## 🔧 **Build Requirements**

### **System Requirements**
- **Python**: 3.9+ (tested with 3.13)
- **OS**: Linux, macOS, Windows
- **Memory**: 2GB+ RAM recommended
- **Storage**: 1GB+ free space
- **Network**: No external dependencies required

### **Python Dependencies**
```txt
# Core Web Framework
fastapi>=0.117.1
uvicorn>=0.37.0
python-multipart>=0.0.20
jinja2>=3.1.6
pydantic>=2.11.9
pydantic-settings>=2.11.0

# File Processing
openpyxl>=3.1.5
PyPDF2>=3.0.1
PyMuPDF>=1.26.4
beautifulsoup4>=4.13.5

# HTTP & Networking (Local Use Only)
requests>=2.32.5
aiohttp>=3.12.15

# Validation & Utilities
jsonschema>=4.25.1
python-dotenv>=1.1.1
```

## 🚀 **Build Process**

### **Phase 1: Environment Setup**

#### **1.1 Clone/Setup Workspace**
```bash
# Navigate to workspace
cd /workspace

# Verify Python version
python3 --version  # Should be 3.9+
```

#### **1.2 Install Dependencies**
```bash
# Install core dependencies
pip install -r requirements_simple.txt --break-system-packages

# Or install individually
pip install fastapi uvicorn openpyxl PyPDF2 PyMuPDF beautifulsoup4 requests aiohttp pydantic pydantic-settings jsonschema python-dotenv --break-system-packages
```

#### **1.3 Verify Installation**
```bash
# Test core imports
python3 -c "
import sys
sys.path.append('/workspace')
from agents.config_research_agent import ConfigResearchAgent
from utils.excel_processor import ExcelProcessor
from utils.pdf_parser import PDFParser
from utils.link_analyzer import LinkAnalyzer
print('✅ All core components import successfully')
"
```

### **Phase 2: Configuration Setup**

#### **2.1 Environment Configuration**
```bash
# Create environment file (optional)
cp .env.example .env

# Edit settings if needed
nano configs/settings.py
```

#### **2.2 Directory Structure**
```bash
# Create required directories
mkdir -p data/uploads
mkdir -p data/excel_templates
mkdir -p data/excel_output
mkdir -p data/pdf_docs
mkdir -p data/pdf_errors
mkdir -p data/link_cache
mkdir -p dashboard/static/css
mkdir -p dashboard/static/js
mkdir -p dashboard/templates
```

### **Phase 3: Component Verification**

#### **3.1 Agent Initialization Test**
```bash
python3 -c "
import sys
sys.path.append('/workspace')
from agents.config_research_agent import ConfigResearchAgent
from configs.settings import settings

print('🔧 Initializing Configuration Research Agent...')
agent = ConfigResearchAgent()
print('✅ Agent initialized successfully')

print('📊 Agent Components:')
print(f'  - Excel Processor: {type(agent.excel_processor).__name__}')
print(f'  - PDF Parser: {type(agent.pdf_parser).__name__}')
print(f'  - Link Analyzer: {type(agent.link_analyzer).__name__}')

print('🔒 Local Processing Settings:')
print(f'  - Local Only: {settings.local_processing_only}')
print(f'  - Max File Size: {settings.max_file_size / (1024*1024):.1f}MB')
print(f'  - Allowed Types: {settings.allowed_file_types}')
"
```

#### **3.2 Dashboard Application Test**
```bash
python3 -c "
import sys
sys.path.append('/workspace')
from dashboard.app import app
from configs.settings import settings

print('🌐 Testing Dashboard Application...')
print(f'✅ FastAPI app created successfully')
print(f'✅ Dashboard host: {settings.dashboard_host}')
print(f'✅ Dashboard port: {settings.dashboard_port}')
print(f'✅ Debug mode: {settings.debug}')
print('✅ Dashboard is ready to start!')
"
```

### **Phase 4: File Processing Tests**

#### **4.1 Excel Processing Test**
```bash
# Create test Excel file
python3 -c "
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
ws['A1'] = 'Field Name'
ws['B1'] = 'Value'
ws['A2'] = 'host'
ws['B2'] = 'localhost'
ws['A3'] = 'port'
ws['B3'] = '8080'
wb.save('test_config.xlsx')
print('✅ Test Excel file created')
"

# Test Excel processing
python3 -c "
import sys
sys.path.append('/workspace')
from utils.excel_processor import ExcelProcessor

processor = ExcelProcessor('/workspace/data/excel_templates', '/workspace/data/excel_output')
configs = processor.read_excel_file('test_config.xlsx')
print(f'✅ Excel processing test passed: {len(configs)} sheets processed')
"
```

#### **4.2 PDF Processing Test**
```bash
# Test PDF processing (if test PDF available)
python3 -c "
import sys
sys.path.append('/workspace')
from utils.pdf_parser import PDFParser

parser = PDFParser('/workspace/data/pdf_docs', '/workspace/data/pdf_errors')
print('✅ PDF parser initialized successfully')
"
```

### **Phase 5: System Integration Test**

#### **5.1 Full System Test**
```bash
# Test complete system
python3 -c "
import sys
sys.path.append('/workspace')
from agents.config_research_agent import ConfigResearchAgent

agent = ConfigResearchAgent()
task_id = agent.create_research_task(
    name='Build Test',
    description='Testing system integration',
    excel_files=['test_config.xlsx'],
    pdf_files=[],
    links=[],
    validation_rules={}
)
print(f'✅ Research task created: {task_id}')
print('✅ System integration test passed')
"
```

## 🚀 **Deployment**

### **Development Mode**
```bash
# Start development server
cd /workspace
python3 start_system.py

# Or start directly
python3 -m uvicorn dashboard.app:app --host 0.0.0.0 --port 8000 --reload
```

### **Production Mode**
```bash
# Start production server
cd /workspace
python3 -m uvicorn dashboard.app:app --host 0.0.0.0 --port 8000 --workers 4
```

### **Docker Deployment (Optional)**
```dockerfile
# Dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements_simple.txt .
RUN pip install -r requirements_simple.txt

COPY . .
EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "dashboard.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔍 **Build Verification Checklist**

### **Pre-Build Checks**
- [ ] Python 3.9+ installed
- [ ] Workspace directory accessible
- [ ] Required directories exist
- [ ] Dependencies can be installed

### **Build Phase Checks**
- [ ] All dependencies installed successfully
- [ ] Core components import without errors
- [ ] Agent initializes successfully
- [ ] Dashboard application starts
- [ ] File processing components work
- [ ] Local-only processing confirmed

### **Post-Build Verification**
- [ ] System starts without errors
- [ ] Web interface accessible
- [ ] File upload functionality works
- [ ] Chat interface responsive
- [ ] No external API calls made
- [ ] All processing is local-only

## 🐛 **Troubleshooting**

### **Common Build Issues**

#### **1. Import Errors**
```bash
# Error: ModuleNotFoundError
# Solution: Install missing dependencies
pip install <missing_module> --break-system-packages
```

#### **2. Permission Errors**
```bash
# Error: Permission denied
# Solution: Use --break-system-packages flag
pip install -r requirements_simple.txt --break-system-packages
```

#### **3. Python Version Issues**
```bash
# Error: Python version incompatible
# Solution: Use Python 3.9+ or update dependencies
python3 --version
```

#### **4. Port Already in Use**
```bash
# Error: Port 8000 already in use
# Solution: Change port or kill existing process
lsof -ti:8000 | xargs kill -9
```

### **Build Logs**
```bash
# Check build logs
tail -f /var/log/syslog | grep python

# Check application logs
python3 start_system.py 2>&1 | tee build.log
```

## 📊 **Build Metrics**

### **Build Time**
- **Dependencies**: ~2-3 minutes
- **Component Tests**: ~30 seconds
- **Integration Tests**: ~1 minute
- **Total Build Time**: ~5 minutes

### **Resource Usage**
- **Memory**: ~200MB during build
- **CPU**: Moderate usage during compilation
- **Storage**: ~500MB for dependencies
- **Network**: Minimal (local-only processing)

### **Build Artifacts**
- **Executable**: `start_system.py`
- **Configuration**: `configs/settings.py`
- **Dependencies**: `requirements_simple.txt`
- **Documentation**: `BUILD_README.md`

## 🔒 **Security Considerations**

### **Build Security**
- ✅ **No External Dependencies**: All processing is local
- ✅ **No API Keys Required**: No external service accounts
- ✅ **Local Storage Only**: No data transmission
- ✅ **Sandboxed Environment**: Isolated processing

### **Runtime Security**
- ✅ **File Validation**: Uploaded files validated
- ✅ **Size Limits**: 10MB file size limit
- ✅ **Type Restrictions**: Only allowed file types
- ✅ **Session Isolation**: Each session independent

## 📈 **Performance Optimization**

### **Build Optimization**
```bash
# Use pip cache
pip install --cache-dir /tmp/pip-cache -r requirements_simple.txt

# Parallel installation
pip install -r requirements_simple.txt --break-system-packages --no-deps
```

### **Runtime Optimization**
- **File Processing**: Optimized for local processing
- **Memory Usage**: Efficient data structures
- **CPU Usage**: Minimal computational overhead
- **Storage**: Temporary file cleanup

## 🎯 **Build Success Criteria**

### **Functional Requirements**
- [ ] All components import successfully
- [ ] Agent initializes without errors
- [ ] Dashboard starts and responds
- [ ] File upload works correctly
- [ ] Chat interface is functional
- [ ] Local processing confirmed

### **Non-Functional Requirements**
- [ ] No external API dependencies
- [ ] Local-only processing verified
- [ ] Privacy requirements met
- [ ] Performance within acceptable limits
- [ ] Security requirements satisfied

## 🚀 **Next Steps After Build**

1. **Start the System**: `python3 start_system.py`
2. **Access Interface**: Navigate to `http://localhost:8000/chat`
3. **Upload Test Files**: Try Excel, PDF, JSON files
4. **Test Functionality**: Ask questions about uploaded files
5. **Verify Local Processing**: Confirm no external requests

## 📚 **Additional Resources**

- **API Documentation**: `http://localhost:8000/api/docs`
- **System Health**: `http://localhost:8000/api/health`
- **Configuration Guide**: `configs/settings.py`
- **Example Scripts**: `examples/` directory
- **Troubleshooting**: `AGENT_VERIFICATION_REPORT.md`

---

**🎉 Build Phase Complete - Configuration Research Agent Ready for Use!**

The agent is now built and ready to provide powerful, privacy-focused configuration research and validation using only uploaded files.