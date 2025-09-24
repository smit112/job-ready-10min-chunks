#!/usr/bin/env python3
"""
Quick test script to verify system structure without external dependencies
"""

import sys
import json
from pathlib import Path


def test_project_structure():
    """Test that all required files and directories exist"""
    print("🔍 Testing project structure...")
    
    required_files = [
        "main.py",
        "setup.py", 
        "demo.py",
        "test_system.py",
        "requirements.txt",
        "pyproject.toml",
        "README.md",
        "USAGE_GUIDE.md",
        "src/__init__.py",
        "src/mcp_server/__init__.py",
        "src/mcp_server/server.py",
        "src/processors/__init__.py",
        "src/processors/excel_processor.py",
        "src/processors/pdf_analyzer.py",
        "src/validators/__init__.py",
        "src/validators/link_validator.py",
        "src/validators/config_validator.py",
        "src/agents/__init__.py",
        "src/agents/config_agent.py",
        "src/integration/__init__.py",
        "src/integration/cursor_integration.py",
        "config/mcp_config.json",
        "config/validation_rules.yaml",
        "data/sample_config.json",
        "data/sample_links.txt"
    ]
    
    required_dirs = [
        "src",
        "src/mcp_server",
        "src/processors", 
        "src/validators",
        "src/agents",
        "src/integration",
        "config",
        "data",
        "data/excel",
        "data/pdfs",
        "data/links"
    ]
    
    missing_files = []
    missing_dirs = []
    
    # Check files
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    # Check directories
    for dir_path in required_dirs:
        if not Path(dir_path).is_dir():
            missing_dirs.append(dir_path)
        else:
            print(f"📁 {dir_path}/")
    
    if missing_files:
        print(f"\n❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
    
    if missing_dirs:
        print(f"\n❌ Missing directories:")
        for dir_path in missing_dirs:
            print(f"   - {dir_path}/")
    
    return len(missing_files) == 0 and len(missing_dirs) == 0


def test_configuration_files():
    """Test that configuration files are valid"""
    print("\n🔧 Testing configuration files...")
    
    # Test JSON config
    try:
        with open("config/mcp_config.json", "r") as f:
            config = json.load(f)
        print("✅ MCP configuration JSON is valid")
        print(f"   Server name: {config.get('mcp_server', {}).get('name', 'unknown')}")
        print(f"   Tools configured: {len(config.get('mcp_server', {}).get('tools', []))}")
    except Exception as e:
        print(f"❌ MCP configuration error: {e}")
        return False
    
    # Test sample config
    try:
        with open("data/sample_config.json", "r") as f:
            sample_config = json.load(f)
        print("✅ Sample configuration JSON is valid")
        print(f"   Application: {sample_config.get('application', {}).get('name', 'unknown')}")
    except Exception as e:
        print(f"❌ Sample configuration error: {e}")
        return False
    
    # Test YAML config (basic check)
    try:
        with open("config/validation_rules.yaml", "r") as f:
            yaml_content = f.read()
        if "validation_rules:" in yaml_content:
            print("✅ Validation rules YAML structure looks correct")
        else:
            print("⚠️  Validation rules YAML may have structure issues")
    except Exception as e:
        print(f"❌ Validation rules error: {e}")
        return False
    
    return True


def test_python_files():
    """Test that Python files have basic syntax"""
    print("\n🐍 Testing Python file syntax...")
    
    python_files = [
        "main.py",
        "setup.py",
        "demo.py",
        "test_system.py",
        "src/__init__.py",
        "src/mcp_server/server.py",
        "src/processors/excel_processor.py",
        "src/processors/pdf_analyzer.py",
        "src/validators/link_validator.py",
        "src/validators/config_validator.py",
        "src/agents/config_agent.py",
        "src/integration/cursor_integration.py"
    ]
    
    syntax_errors = []
    
    for file_path in python_files:
        try:
            with open(file_path, "r") as f:
                source_code = f.read()
            
            # Basic syntax check using compile
            compile(source_code, file_path, "exec")
            print(f"✅ {file_path}")
            
        except SyntaxError as e:
            print(f"❌ {file_path} - Syntax Error: {e}")
            syntax_errors.append(file_path)
        except Exception as e:
            print(f"⚠️  {file_path} - Warning: {e}")
    
    return len(syntax_errors) == 0


def test_requirements():
    """Test requirements file"""
    print("\n📦 Testing requirements...")
    
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read().strip().split('\n')
        
        print(f"✅ Requirements file contains {len(requirements)} packages")
        
        # Show key packages
        key_packages = ['fastapi', 'pandas', 'PyPDF2', 'loguru', 'aiohttp']
        found_packages = []
        
        for req in requirements:
            for key_pkg in key_packages:
                if key_pkg.lower() in req.lower():
                    found_packages.append(key_pkg)
        
        print(f"   Key packages found: {', '.join(found_packages)}")
        
        return True
    except Exception as e:
        print(f"❌ Requirements file error: {e}")
        return False


def calculate_project_stats():
    """Calculate project statistics"""
    print("\n📊 Project Statistics")
    print("-" * 30)
    
    # Count files by type
    stats = {
        "Python files": len(list(Path(".").rglob("*.py"))),
        "JSON files": len(list(Path(".").rglob("*.json"))),
        "YAML files": len(list(Path(".").rglob("*.yaml"))),
        "Markdown files": len(list(Path(".").rglob("*.md"))),
        "Text files": len(list(Path(".").rglob("*.txt"))),
        "Total files": len(list(Path(".").rglob("*.*")))
    }
    
    for stat_name, count in stats.items():
        print(f"   {stat_name}: {count}")
    
    # Calculate total lines of code
    total_lines = 0
    python_files = list(Path(".").rglob("*.py"))
    
    for py_file in python_files:
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                lines = len(f.readlines())
                total_lines += lines
        except:
            pass
    
    print(f"   Total Python LOC: {total_lines:,}")


def main():
    """Main test function"""
    print("🧪 Agentic Configuration Research System - Quick Structure Test")
    print("=" * 70)
    
    tests = [
        ("Project Structure", test_project_structure),
        ("Configuration Files", test_configuration_files), 
        ("Python Syntax", test_python_files),
        ("Requirements", test_requirements)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    # Show statistics
    calculate_project_stats()
    
    # Final summary
    print(f"\n{'='*70}")
    print(f"🎯 Test Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All structure tests passed!")
        print("\n🚀 Next steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Run full tests: python3 test_system.py")
        print("   3. Start the system: python3 main.py server")
        print("   4. Try the demo: python3 demo.py")
        return True
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)