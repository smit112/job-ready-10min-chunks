#!/usr/bin/env python3
"""
Setup script for Agentic Configuration Research System
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False


def create_directories():
    """Create necessary directories"""
    directories = [
        "logs",
        "data/excel",
        "data/pdfs", 
        "data/links",
        "data/uploads",
        "config/schemas",
        "tests/unit",
        "tests/integration",
        "tmp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")


def install_dependencies():
    """Install Python dependencies"""
    print("🔄 Installing Python dependencies...")
    
    # Check if pip is available
    if not run_command("pip --version", "Checking pip"):
        print("❌ pip is not available. Please install pip first.")
        return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        print("❌ Failed to install requirements. Please check requirements.txt")
        return False
    
    return True


def setup_environment():
    """Setup environment variables and configuration"""
    env_file = Path(".env")
    
    if not env_file.exists():
        env_content = """# Agentic Configuration Research System Environment Variables
WORKSPACE_PATH=/workspace
LOG_LEVEL=INFO
API_PORT=8000
WEBSOCKET_PORT=8001
MCP_SERVER_PORT=8002

# AI Integration (optional)
# ANTHROPIC_API_KEY=your_key_here
# OPENAI_API_KEY=your_key_here

# Security (optional)
# SSL_ENABLED=false
# JWT_SECRET=your_jwt_secret_here

# Performance
MAX_FILE_SIZE=50MB
MAX_CONCURRENT_REQUESTS=100
REQUEST_TIMEOUT=300
"""
        env_file.write_text(env_content)
        print("📝 Created .env file with default settings")
    else:
        print("✅ .env file already exists")


def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    # Test basic import
    try:
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from src.mcp_server.server import MCPServer
        print("✅ MCP Server import successful")
        
        from src.integration.cursor_integration import CursorIntegration
        print("✅ Integration layer import successful")
        
        from src.processors.excel_processor import ExcelProcessor
        print("✅ Excel processor import successful")
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    
    # Test sample configuration validation
    try:
        if Path("data/sample_config.json").exists():
            print("✅ Sample configuration file found")
        else:
            print("⚠️  Sample configuration file not found")
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False
    
    return True


def create_startup_scripts():
    """Create startup scripts for different platforms"""
    
    # Unix/Linux startup script
    unix_script = """#!/bin/bash
# Agentic Configuration Research System Startup Script

echo "🚀 Starting Agentic Configuration Research System..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Start the system
python main.py server --host 0.0.0.0 --port 8000
"""
    
    Path("start.sh").write_text(unix_script)
    os.chmod("start.sh", 0o755)
    print("📝 Created start.sh script")
    
    # Windows startup script
    windows_script = """@echo off
REM Agentic Configuration Research System Startup Script

echo 🚀 Starting Agentic Configuration Research System...

REM Activate virtual environment if it exists
if exist "venv\\Scripts\\activate.bat" (
    echo 📦 Activating virtual environment...
    call venv\\Scripts\\activate.bat
)

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Start the system
python main.py server --host 0.0.0.0 --port 8000
"""
    
    Path("start.bat").write_text(windows_script)
    print("📝 Created start.bat script")


def main():
    """Main setup function"""
    print("🎯 Agentic Configuration Research System Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required. Current version:", sys.version)
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Create startup scripts
    create_startup_scripts()
    
    # Test installation
    if not test_installation():
        print("⚠️  Setup completed but tests failed. Please check the installation manually.")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Review configuration files in config/")
    print("2. Start the system: python main.py server")
    print("3. Access the API: http://localhost:8000")
    print("4. View documentation: http://localhost:8000/docs")
    print("\n🔧 Quick commands:")
    print("  ./start.sh                    # Unix/Linux")
    print("  start.bat                     # Windows")
    print("  python main.py --help        # View all options")
    
    print("\n📚 For more information, see README.md")


if __name__ == "__main__":
    main()