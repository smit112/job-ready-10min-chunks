#!/usr/bin/env python3
"""
Application Builder for Agentic Configuration Research System
Creates executable applications for different platforms
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import zipfile
import json


def create_windows_executable():
    """Create Windows executable using PyInstaller"""
    print("🪟 Creating Windows executable...")
    
    try:
        # Check if PyInstaller is available
        subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
        
        # Create PyInstaller spec file
        spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gui_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),
        ('config', 'config'),
        ('data', 'data'),
        ('README.md', '.'),
        ('USAGE_GUIDE.md', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'asyncio',
        'threading',
        'webbrowser',
        'json',
        'pathlib',
        'datetime',
        'subprocess',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AgenticConfigResearch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if Path('icon.ico').exists() else None,
)
"""
        
        Path("gui_app.spec").write_text(spec_content)
        
        # Run PyInstaller
        result = subprocess.run([
            "pyinstaller", 
            "--onefile",
            "--windowed",
            "--name=AgenticConfigResearch",
            "gui_app.spec"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Windows executable created successfully!")
            if Path("dist/AgenticConfigResearch.exe").exists():
                print(f"   📁 Location: dist/AgenticConfigResearch.exe")
                return True
        else:
            print(f"❌ PyInstaller failed: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False
    except Exception as e:
        print(f"❌ Error creating Windows executable: {e}")
        return False


def create_macos_app():
    """Create macOS application bundle"""
    print("🍎 Creating macOS application bundle...")
    
    app_name = "Agentic Config Research"
    app_dir = Path(f"{app_name}.app")
    
    try:
        # Create app bundle structure
        contents_dir = app_dir / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"
        
        for dir_path in [contents_dir, macos_dir, resources_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create Info.plist
        info_plist = {
            "CFBundleName": app_name,
            "CFBundleDisplayName": app_name,
            "CFBundleIdentifier": "com.agentic.configresearch",
            "CFBundleVersion": "1.0.0",
            "CFBundleShortVersionString": "1.0.0",
            "CFBundleExecutable": "launch",
            "CFBundleIconFile": "icon.icns",
            "NSHighResolutionCapable": True,
            "LSMinimumSystemVersion": "10.12",
        }
        
        import plistlib
        with open(contents_dir / "Info.plist", "wb") as f:
            plistlib.dump(info_plist, f)
        
        # Create launcher script
        launcher_script = f"""#!/bin/bash
cd "$(dirname "$0")/../Resources"
python3 gui_app.py
"""
        
        launcher_path = macos_dir / "launch"
        launcher_path.write_text(launcher_script)
        launcher_path.chmod(0o755)
        
        # Copy application files
        files_to_copy = [
            "gui_app.py",
            "main.py", 
            "src",
            "config",
            "data",
            "README.md",
            "USAGE_GUIDE.md",
            "requirements.txt"
        ]
        
        for item in files_to_copy:
            src_path = Path(item)
            if src_path.exists():
                dst_path = resources_dir / item
                if src_path.is_dir():
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_path, dst_path)
        
        print(f"✅ macOS app bundle created: {app_dir}")
        print("   Double-click the .app to launch")
        return True
        
    except Exception as e:
        print(f"❌ Error creating macOS app: {e}")
        return False


def create_linux_appimage():
    """Create Linux AppImage"""
    print("🐧 Creating Linux AppImage...")
    
    try:
        app_dir = Path("AgenticConfigResearch.AppDir")
        
        # Create AppDir structure
        (app_dir / "usr" / "bin").mkdir(parents=True, exist_ok=True)
        (app_dir / "usr" / "share" / "applications").mkdir(parents=True, exist_ok=True)
        (app_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps").mkdir(parents=True, exist_ok=True)
        
        # Copy application files
        app_files_dir = app_dir / "usr" / "share" / "agentic-config-research"
        app_files_dir.mkdir(parents=True, exist_ok=True)
        
        files_to_copy = [
            "gui_app.py",
            "main.py",
            "src",
            "config", 
            "data",
            "README.md",
            "USAGE_GUIDE.md",
            "requirements.txt"
        ]
        
        for item in files_to_copy:
            src_path = Path(item)
            if src_path.exists():
                dst_path = app_files_dir / item
                if src_path.is_dir():
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_path, dst_path)
        
        # Create launcher script
        launcher_script = f"""#!/bin/bash
cd /usr/share/agentic-config-research
python3 gui_app.py
"""
        
        launcher_path = app_dir / "usr" / "bin" / "agentic-config-research"
        launcher_path.write_text(launcher_script)
        launcher_path.chmod(0o755)
        
        # Create AppRun
        apprun_script = """#!/bin/bash
cd "$(dirname "$0")/usr/share/agentic-config-research"
python3 gui_app.py
"""
        
        apprun_path = app_dir / "AppRun"
        apprun_path.write_text(apprun_script)
        apprun_path.chmod(0o755)
        
        # Create desktop entry
        desktop_entry = """[Desktop Entry]
Name=Agentic Config Research
Exec=agentic-config-research
Icon=agentic-config-research
Type=Application
Categories=Development;Utility;
Comment=AI-Powered Configuration Research & Troubleshooting
"""
        
        (app_dir / "agentic-config-research.desktop").write_text(desktop_entry)
        (app_dir / "usr" / "share" / "applications" / "agentic-config-research.desktop").write_text(desktop_entry)
        
        print(f"✅ Linux AppDir created: {app_dir}")
        print("   Use appimagetool to create AppImage")
        return True
        
    except Exception as e:
        print(f"❌ Error creating Linux AppImage: {e}")
        return False


def create_portable_package():
    """Create portable package for any platform"""
    print("📦 Creating portable package...")
    
    try:
        package_name = "AgenticConfigResearch-Portable"
        package_dir = Path(package_name)
        
        # Create package directory
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir()
        
        # Copy all necessary files
        files_to_copy = [
            "gui_app.py",
            "main.py",
            "setup.py",
            "demo.py", 
            "test_system.py",
            "quick_test.py",
            "src",
            "config",
            "data",
            "README.md",
            "USAGE_GUIDE.md",
            "INSTALLATION.md",
            "requirements.txt",
            "pyproject.toml"
        ]
        
        for item in files_to_copy:
            src_path = Path(item)
            if src_path.exists():
                dst_path = package_dir / item
                if src_path.is_dir():
                    shutil.copytree(src_path, dst_path)
                else:
                    shutil.copy2(src_path, dst_path)
        
        # Create launcher scripts
        create_launcher_scripts(package_dir)
        
        # Create installation instructions
        install_instructions = """# Agentic Configuration Research System - Portable Package

## Quick Start

### Windows:
1. Double-click `start_gui.bat`
2. Or open Command Prompt and run: `python gui_app.py`

### macOS/Linux:
1. Double-click `start_gui.sh` (or `start_gui_macos.command` on macOS)
2. Or open Terminal and run: `python3 gui_app.py`

## First Time Setup:
1. Install Python 3.9+ if not already installed
2. Run: `pip install -r requirements.txt`
3. Run: `python3 setup.py` (optional, for full setup)

## Features:
- 🤖 AI-powered configuration research
- 📊 Excel configuration analysis
- 📄 PDF error document processing
- 🔗 Link validation
- ✅ Configuration validation
- 🔍 Automated troubleshooting

## Support:
- See README.md for complete documentation
- See USAGE_GUIDE.md for detailed usage instructions
"""
        
        (package_dir / "QUICK_START.txt").write_text(install_instructions)
        
        # Create ZIP package
        zip_path = f"{package_name}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in package_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(package_dir.parent)
                    zipf.write(file_path, arcname)
        
        print(f"✅ Portable package created: {zip_path}")
        print(f"   📁 Directory: {package_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating portable package: {e}")
        return False


def create_launcher_scripts(target_dir):
    """Create launcher scripts in target directory"""
    
    # Windows batch file
    windows_launcher = """@echo off
title Agentic Configuration Research System
cd /d "%~dp0"

echo 🤖 Agentic Configuration Research System
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.9+
    echo    Download from: https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo ✅ Starting GUI application...
echo.
python gui_app.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo ❌ Application ended with error
    pause
)
"""
    
    (target_dir / "start_gui.bat").write_text(windows_launcher)
    
    # Unix shell script
    unix_launcher = """#!/bin/bash
cd "$(dirname "$0")"

echo "🤖 Agentic Configuration Research System"
echo "=========================================="
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    echo "   Ubuntu/Debian: sudo apt-get install python3"
    echo "   macOS: Install from python.org or use Homebrew"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if tkinter is available
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  tkinter not found. Installing..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install python3-tk
    else
        echo "❌ Please install python3-tk manually"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Check if dependencies are installed
python3 -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo "✅ Starting GUI application..."
echo
python3 gui_app.py

# Check exit status
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Application ended with error"
    read -p "Press Enter to exit..."
fi
"""
    
    launcher_path = target_dir / "start_gui.sh"
    launcher_path.write_text(unix_launcher)
    launcher_path.chmod(0o755)
    
    # macOS command file
    macos_launcher = """#!/bin/bash
# macOS Application Launcher
cd "$(dirname "$0")"
exec ./start_gui.sh
"""
    
    macos_path = target_dir / "start_gui_macos.command"
    macos_path.write_text(macos_launcher)
    macos_path.chmod(0o755)


def create_installer():
    """Create installer script"""
    print("🛠️ Creating installer...")
    
    installer_script = """#!/usr/bin/env python3
\"\"\"
Installer for Agentic Configuration Research System
\"\"\"

import sys
import subprocess
import os
from pathlib import Path

def install_dependencies():
    \"\"\"Install required dependencies\"\"\"
    print("📦 Installing dependencies...")
    
    try:
        # Install requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        
        print("✅ Dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_desktop_shortcut():
    \"\"\"Create desktop shortcut (Windows/Linux)\"\"\"
    print("🔗 Creating desktop shortcut...")
    
    try:
        if sys.platform == "win32":
            # Windows shortcut
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "Agentic Config Research.lnk")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = os.path.join(os.getcwd(), "start_gui.bat")
            shortcut.WorkingDirectory = os.getcwd()
            shortcut.IconLocation = os.path.join(os.getcwd(), "icon.ico")
            shortcut.save()
            
            print("✅ Desktop shortcut created!")
            
        elif sys.platform.startswith("linux"):
            # Linux desktop entry
            desktop_entry = f\"\"\"[Desktop Entry]
Name=Agentic Config Research
Exec={os.path.join(os.getcwd(), "start_gui.sh")}
Icon={os.path.join(os.getcwd(), "icon.png")}
Type=Application
Categories=Development;Utility;
Comment=AI-Powered Configuration Research & Troubleshooting
Path={os.getcwd()}
\"\"\"
            
            desktop_dir = Path.home() / "Desktop"
            if desktop_dir.exists():
                shortcut_path = desktop_dir / "Agentic Config Research.desktop"
                shortcut_path.write_text(desktop_entry)
                shortcut_path.chmod(0o755)
                print("✅ Desktop shortcut created!")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Could not create desktop shortcut: {e}")
        return False

def main():
    print("🤖 Agentic Configuration Research System Installer")
    print("=" * 55)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Installation failed!")
        return False
    
    # Setup desktop shortcut
    setup_desktop_shortcut()
    
    print("\\n🎉 Installation completed successfully!")
    print("\\n🚀 You can now:")
    print("   1. Double-click the desktop shortcut")
    print("   2. Run start_gui.bat (Windows) or start_gui.sh (Linux/macOS)")
    print("   3. Run: python gui_app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    input("\\nPress Enter to exit...")
    sys.exit(0 if success else 1)
"""
    
    Path("install.py").write_text(installer_script)
    
    print("✅ Installer script created: install.py")
    return True


def main():
    """Main function to create application packages"""
    print("🏗️ Agentic Configuration Research System - Application Builder")
    print("=" * 65)
    
    print("\nAvailable options:")
    print("1. Create portable package (recommended)")
    print("2. Create Windows executable (requires PyInstaller)")
    print("3. Create macOS app bundle")
    print("4. Create Linux AppImage structure")
    print("5. Create installer script")
    print("6. Create all packages")
    
    try:
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            create_portable_package()
        elif choice == "2":
            create_windows_executable()
        elif choice == "3":
            create_macos_app()
        elif choice == "4":
            create_linux_appimage()
        elif choice == "5":
            create_installer()
        elif choice == "6":
            print("Creating all packages...")
            create_portable_package()
            create_installer()
            create_windows_executable()
            create_macos_app()
            create_linux_appimage()
        else:
            print("Invalid choice")
            return False
        
        print("\n🎉 Application building completed!")
        print("\n📦 Available packages:")
        
        # List created packages
        packages = [
            ("AgenticConfigResearch-Portable.zip", "Portable package for all platforms"),
            ("dist/AgenticConfigResearch.exe", "Windows executable"),
            ("Agentic Config Research.app", "macOS application bundle"),
            ("AgenticConfigResearch.AppDir", "Linux AppImage structure"),
            ("install.py", "Installer script")
        ]
        
        for package_path, description in packages:
            if Path(package_path).exists():
                print(f"   ✅ {package_path} - {description}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == "__main__":
    main()