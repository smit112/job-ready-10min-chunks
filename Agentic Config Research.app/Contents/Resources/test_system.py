#!/usr/bin/env python3
"""
Test script for Agentic Configuration Research System
"""

import asyncio
import sys
import json
from pathlib import Path
from loguru import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.integration.cursor_integration import CursorIntegration
from src.processors.excel_processor import ExcelProcessor
from src.validators.config_validator import ConfigValidator
from src.validators.link_validator import LinkValidator


async def test_config_validation():
    """Test configuration validation"""
    print("🧪 Testing Configuration Validation...")
    
    try:
        validator = ConfigValidator()
        result = await validator.validate_config("data/sample_config.json")
        
        print(f"✅ Configuration validation completed")
        print(f"   Overall status: {result.get('summary', {}).get('overall_status', 'unknown')}")
        print(f"   Total errors: {result.get('summary', {}).get('total_errors', 0)}")
        print(f"   Total warnings: {result.get('summary', {}).get('total_warnings', 0)}")
        print(f"   Security score: {result.get('summary', {}).get('security_score', 0)}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {str(e)}")
        return False


async def test_link_validation():
    """Test link validation"""
    print("🧪 Testing Link Validation...")
    
    try:
        test_links = [
            "https://www.google.com",
            "https://github.com",
            "https://this-domain-does-not-exist-12345.com"
        ]
        
        async with LinkValidator() as validator:
            result = await validator.validate_links(test_links, timeout=5)
        
        summary = result.get("summary", {})
        print(f"✅ Link validation completed")
        print(f"   Total links: {summary.get('total_links', 0)}")
        print(f"   Successful: {summary.get('successful', 0)}")
        print(f"   Failed: {summary.get('failed', 0)}")
        print(f"   Success rate: {summary.get('success_rate', 0):.1f}%")
        
        return True
    except Exception as e:
        print(f"❌ Link validation failed: {str(e)}")
        return False


async def test_integration_layer():
    """Test integration layer"""
    print("🧪 Testing Integration Layer...")
    
    try:
        integration = CursorIntegration("/workspace")
        
        # Test workspace scan
        scan_result = await integration._scan_workspace()
        print(f"✅ Workspace scan completed")
        print(f"   Total files found: {scan_result.get('total_files', 0)}")
        print(f"   Config files: {len(scan_result.get('config_files', []))}")
        
        # Test configuration validation
        if scan_result.get('config_files'):
            config_file = scan_result['config_files'][0]['path']
            validation_result = await integration._handle_config_validation({
                "config_path": config_file
            })
            print(f"✅ Integration config validation completed")
            print(f"   File: {Path(config_file).name}")
        
        return True
    except Exception as e:
        print(f"❌ Integration layer test failed: {str(e)}")
        return False


async def test_troubleshooting():
    """Test troubleshooting functionality"""
    print("🧪 Testing Troubleshooting...")
    
    try:
        integration = CursorIntegration("/workspace")
        
        result = await integration._handle_troubleshooting({
            "issue_description": "Database connection timeout error",
            "system_type": "database"
        })
        
        troubleshooting_result = result.get("troubleshooting_result", {})
        plan = troubleshooting_result.get("troubleshooting_plan", {})
        
        print(f"✅ Troubleshooting analysis completed")
        print(f"   Issue category: {troubleshooting_result.get('issue_analysis', {}).get('issue_category', 'unknown')}")
        print(f"   Confidence score: {troubleshooting_result.get('confidence_score', 0):.2f}")
        print(f"   Immediate actions: {len(plan.get('immediate_actions', []))}")
        print(f"   Investigation steps: {len(plan.get('investigation_steps', []))}")
        
        return True
    except Exception as e:
        print(f"❌ Troubleshooting test failed: {str(e)}")
        return False


async def run_comprehensive_test():
    """Run comprehensive system test"""
    print("🎯 Running Comprehensive System Test")
    print("=" * 50)
    
    test_results = []
    
    # Run individual tests
    tests = [
        ("Configuration Validation", test_config_validation),
        ("Link Validation", test_link_validation),
        ("Integration Layer", test_integration_layer),
        ("Troubleshooting", test_troubleshooting)
    ]
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            success = await test_func()
            test_results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            test_results.append((test_name, False))
    
    # Summary
    print(f"\n📊 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, success in test_results if success)
    total = len(test_results)
    
    for test_name, success in test_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for use.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        return False


async def main():
    """Main test function"""
    # Setup basic logging
    logger.remove()
    logger.add(sys.stderr, level="WARNING")
    
    print("🧪 Agentic Configuration Research System Test Suite")
    print("=" * 60)
    
    # Check if required files exist
    required_files = [
        "data/sample_config.json",
        "config/mcp_config.json",
        "config/validation_rules.yaml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\nPlease run setup.py first or ensure all files are present.")
        return False
    
    print("✅ All required files present")
    
    # Run comprehensive test
    success = await run_comprehensive_test()
    
    if success:
        print("\n🚀 System is ready! You can now:")
        print("   1. Start the server: python main.py server")
        print("   2. Access the API: http://localhost:8000")
        print("   3. View docs: http://localhost:8000/docs")
        print("   4. Use CLI tools: python main.py --help")
    else:
        print("\n🔧 Please fix the issues above before using the system.")
    
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)