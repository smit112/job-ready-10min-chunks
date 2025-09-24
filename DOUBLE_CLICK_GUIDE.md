# 🖱️ Double-Click Launch Guide

## 🎯 Overview

The Agentic Configuration Research System now includes **multiple ways to launch** the application with just a double-click! No command line knowledge required.

## 🚀 Quick Launch Options

### **Windows Users** 🪟
**Double-click:** `AgenticConfigResearch.bat`
- Automatically checks for Python
- Starts the system and opens web interface
- Shows user-friendly interface

### **macOS Users** 🍎  
**Double-click:** `Agentic Config Research.app` 
- Native macOS application bundle
- Opens Terminal and launches system
- Integrates with macOS Dock

### **Linux Users** 🐧
**Double-click:** `AgenticConfigResearch.sh`
- Works on most Linux distributions
- Checks dependencies automatically
- Opens system in terminal

### **Cross-Platform** 🌐
**Double-click:** `simple_launcher.py`
- Works on any platform with Python
- Web-based interface (no GUI dependencies)
- Interactive menu system

## 📋 What Happens When You Double-Click?

1. **System Check** ✅
   - Verifies Python 3.9+ is installed
   - Checks for required files
   - Shows clear error messages if issues found

2. **Automatic Startup** 🚀
   - Starts the backend server
   - Waits for system to be ready
   - Opens web interface in browser

3. **Interactive Interface** 🖥️
   - Menu-driven options
   - Web-based GUI at http://localhost:8000
   - API documentation at http://localhost:8000/docs

## 🛠️ Installation Requirements

### **Minimum Requirements:**
- **Python 3.9+** (Download from [python.org](https://python.org))
- **Web browser** (Chrome, Firefox, Safari, Edge)
- **5GB free disk space**

### **Optional (for full features):**
- Dependencies: `pip install -r requirements.txt`
- For GUI version: tkinter (usually included with Python)

## 🎪 Available Launch Methods

| Method | Platform | Description | Requirements |
|--------|----------|-------------|--------------|
| `AgenticConfigResearch.bat` | Windows | Batch file launcher | Python 3.9+ |
| `Agentic Config Research.app` | macOS | Native app bundle | Python 3.9+ |
| `AgenticConfigResearch.sh` | Linux | Shell script launcher | Python 3.9+, bash |
| `simple_launcher.py` | All | Python launcher | Python 3.9+ |
| `gui_app.py` | All | Full GUI application | Python 3.9+, tkinter |

## 🌐 Web Interface Features

Once launched, you can access:

### **Main Dashboard** (http://localhost:8000)
- System status overview
- Quick access to all features
- Real-time updates

### **API Documentation** (http://localhost:8000/docs)
- Interactive API explorer
- Complete endpoint documentation
- Test API calls directly

### **Core Features:**
- 📊 **Excel Analysis** - Upload and analyze configuration files
- 📄 **PDF Processing** - Analyze error documents
- 🔗 **Link Validation** - Check URL availability
- ✅ **Config Validation** - Validate configuration files
- 🔍 **Troubleshooting** - AI-powered issue analysis

## 📱 Usage Workflow

### **1. Launch the Application**
```
Double-click → AgenticConfigResearch.bat (Windows)
              AgenticConfigResearch.sh (Linux)
              Agentic Config Research.app (macOS)
```

### **2. Wait for Startup**
```
🚀 Starting server...
✅ Server is ready!
🌐 Opening web interface: http://localhost:8000
```

### **3. Use the Interface**
- **Web Interface:** Full-featured web application
- **Interactive Menu:** Terminal-based menu system
- **API Access:** Programmatic access via REST API

## 🔧 Troubleshooting

### **"Python not found" Error**
```bash
❌ Python not found. Please install Python 3.9+
   Download from: https://python.org
```
**Solution:** Install Python 3.9+ from python.org

### **"Module not found" Error**
```bash
⚠️ Some dependencies missing
```
**Solution:** Run `pip install -r requirements.txt`

### **"Port already in use" Error**
```bash
❌ Server failed to start: Port 8000 already in use
```
**Solution:** Close other applications using port 8000, or modify port in settings

### **Web Interface Won't Open**
1. Check if server started successfully
2. Manually open: http://localhost:8000
3. Try different browser
4. Check firewall settings

## 🎯 First-Time Setup

### **Windows Setup:**
1. Download and install Python from python.org
2. Download the application files
3. Double-click `AgenticConfigResearch.bat`
4. Follow on-screen instructions

### **macOS Setup:**
1. Install Python: `brew install python3` or download from python.org
2. Download the application files
3. Double-click `Agentic Config Research.app`
4. Allow app to run (System Preferences → Security)

### **Linux Setup:**
1. Install Python: `sudo apt-get install python3` (Ubuntu/Debian)
2. Download the application files
3. Make executable: `chmod +x AgenticConfigResearch.sh`
4. Double-click or run: `./AgenticConfigResearch.sh`

## 🚀 Advanced Usage

### **Command Line Options:**
```bash
# Start with custom settings
python3 simple_launcher.py --port 9000 --host 0.0.0.0

# Run specific components
python3 main.py server --port 8000
python3 demo.py
python3 test_system.py
```

### **Configuration:**
- Edit `config/mcp_config.json` for server settings
- Modify `config/validation_rules.yaml` for validation rules
- Set environment variables in `.env` file

## 📊 System Monitoring

### **Check System Status:**
- Web interface shows real-time status
- Interactive menu option "System Status"
- API endpoint: `GET /status`

### **View Logs:**
- Check `logs/` directory for detailed logs
- Terminal output shows real-time information
- Web interface displays recent activity

## 🔄 Updates and Maintenance

### **Updating the System:**
1. Download new version files
2. Replace old files (keep config/ and data/ directories)
3. Restart the application

### **Backup Important Data:**
- Configuration files in `config/`
- Uploaded files in `data/`
- Custom validation rules

## 🆘 Support

### **Getting Help:**
1. Check `README.md` for comprehensive documentation
2. Review `USAGE_GUIDE.md` for detailed usage instructions
3. Run `python3 test_system.py` to diagnose issues
4. Check logs in `logs/` directory

### **Common Solutions:**
- **Restart the application** - Fixes most issues
- **Clear browser cache** - Fixes web interface issues
- **Check Python version** - Ensure 3.9+ is installed
- **Verify file permissions** - Ensure scripts are executable

## 🎉 Success!

When everything is working correctly, you should see:

```
🤖 Agentic Configuration Research System
========================================

✅ Python found: Python 3.9.x
✅ Basic modules available
✅ MCP server module available
🚀 Starting server on localhost:8000...
⏳ Waiting for server to be ready...
✅ Server is ready!
🌐 Opening web interface: http://localhost:8000
📚 API Documentation: http://localhost:8000/docs

Select option (1-6):
1. 🌐 Open Web Interface
2. 📚 Open API Documentation
3. 🧪 Run Tests
4. 🎪 Run Demo
5. 📊 System Status
6. ❌ Exit
```

**Congratulations!** 🎊 Your Agentic Configuration Research System is now running and ready to use!

---

*For technical support and advanced configuration, see the complete documentation in README.md and USAGE_GUIDE.md*