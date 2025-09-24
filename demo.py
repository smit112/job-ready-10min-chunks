#!/usr/bin/env python3
"""
Demo script for Agentic Configuration Research System
Demonstrates key features with sample data
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.integration.cursor_integration import CursorIntegration


async def demo_configuration_validation():
    """Demo configuration validation"""
    print("🔧 Demo: Configuration Validation")
    print("-" * 40)
    
    integration = CursorIntegration("/workspace")
    
    # Validate sample configuration
    result = await integration._handle_config_validation({
        "config_path": "data/sample_config.json"
    })
    
    summary = result.get("validation_result", {}).get("summary", {})
    
    print(f"📊 Validation Results:")
    print(f"   Status: {summary.get('overall_status', 'unknown')}")
    print(f"   Security Score: {summary.get('security_score', 0)}/100")
    print(f"   Performance Score: {summary.get('performance_score', 0)}/100")
    print(f"   Errors: {summary.get('total_errors', 0)}")
    print(f"   Warnings: {summary.get('total_warnings', 0)}")
    
    recommendations = result.get("recommendations", [])[:3]
    if recommendations:
        print(f"\n💡 Top Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    
    return result


async def demo_link_validation():
    """Demo link validation"""
    print("\n🔗 Demo: Link Validation")
    print("-" * 40)
    
    integration = CursorIntegration("/workspace")
    
    # Test various types of links
    test_links = [
        "https://www.google.com",
        "https://github.com",
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404",
        "https://this-domain-definitely-does-not-exist-12345.com"
    ]
    
    result = await integration._handle_link_validation({
        "links": test_links,
        "check_content": True,
        "timeout": 10
    })
    
    validation_result = result.get("validation_result", {})
    summary = validation_result.get("summary", {})
    
    print(f"📊 Link Validation Results:")
    print(f"   Total Links: {summary.get('total_links', 0)}")
    print(f"   Successful: {summary.get('successful', 0)}")
    print(f"   Failed: {summary.get('failed', 0)}")
    print(f"   Success Rate: {summary.get('success_rate', 0):.1f}%")
    print(f"   Avg Response Time: {summary.get('average_response_time', 0):.0f}ms")
    
    # Show some example results
    successful = validation_result.get("successful_validations", [])[:2]
    failed = validation_result.get("failed_validations", [])[:2]
    
    if successful:
        print(f"\n✅ Successful Links:")
        for link in successful:
            print(f"   • {link['url']} ({link['status_code']}) - {link['response_time']:.0f}ms")
    
    if failed:
        print(f"\n❌ Failed Links:")
        for link in failed:
            print(f"   • {link['url']} - {link.get('error', 'Unknown error')}")
    
    return result


async def demo_troubleshooting():
    """Demo automated troubleshooting"""
    print("\n🔍 Demo: Automated Troubleshooting")
    print("-" * 40)
    
    integration = CursorIntegration("/workspace")
    
    # Simulate common troubleshooting scenarios
    scenarios = [
        {
            "issue": "Database connection timeout errors occurring frequently",
            "system_type": "database",
            "description": "Database Connection Issues"
        },
        {
            "issue": "SSL certificate validation failing for API endpoints",
            "system_type": "network",
            "description": "SSL/TLS Issues"
        },
        {
            "issue": "Application startup fails with memory allocation error",
            "system_type": "system",
            "description": "System Resource Issues"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🎯 Scenario: {scenario['description']}")
        print(f"   Issue: {scenario['issue']}")
        
        result = await integration._handle_troubleshooting({
            "issue_description": scenario["issue"],
            "system_type": scenario["system_type"]
        })
        
        troubleshooting_result = result.get("troubleshooting_result", {})
        issue_analysis = troubleshooting_result.get("issue_analysis", {})
        plan = troubleshooting_result.get("troubleshooting_plan", {})
        
        print(f"   Category: {issue_analysis.get('issue_category', 'unknown')}")
        print(f"   Severity: {issue_analysis.get('severity', 'unknown')}")
        print(f"   Confidence: {troubleshooting_result.get('confidence_score', 0):.2f}")
        
        immediate_actions = plan.get("immediate_actions", [])[:2]
        if immediate_actions:
            print(f"   Immediate Actions:")
            for action in immediate_actions:
                print(f"     • {action}")
    
    return result


async def demo_workspace_scan():
    """Demo workspace scanning"""
    print("\n📁 Demo: Workspace Scanning")
    print("-" * 40)
    
    integration = CursorIntegration("/workspace")
    
    result = await integration._scan_workspace()
    
    print(f"📊 Workspace Scan Results:")
    print(f"   Total Files: {result.get('total_files', 0)}")
    print(f"   Excel Files: {len(result.get('excel_files', []))}")
    print(f"   PDF Files: {len(result.get('pdf_files', []))}")
    print(f"   Config Files: {len(result.get('config_files', []))}")
    
    # Show some examples
    config_files = result.get('config_files', [])[:3]
    if config_files:
        print(f"\n📄 Sample Configuration Files:")
        for config_file in config_files:
            file_path = Path(config_file['path'])
            print(f"   • {file_path.name} ({config_file['type']}) - {config_file['size']} bytes")
    
    return result


async def demo_comprehensive_analysis():
    """Demo comprehensive analysis"""
    print("\n🎯 Demo: Comprehensive Analysis")
    print("-" * 40)
    
    integration = CursorIntegration("/workspace")
    
    # Perform comprehensive analysis with available resources
    result = await integration._handle_comprehensive_analysis({
        "config_files": ["data/sample_config.json"],
        "links": ["https://www.google.com", "https://github.com"],
        "issue_description": "System performance degradation and configuration review needed"
    })
    
    summary = result.get("summary", {})
    
    print(f"📊 Comprehensive Analysis Results:")
    print(f"   Files Processed:")
    files_processed = summary.get("files_processed", {})
    for file_type, count in files_processed.items():
        if count > 0:
            print(f"     {file_type.title()}: {count}")
    
    print(f"   Overall Health Score: {summary.get('overall_health_score', 0)}/100")
    
    issues = summary.get("issues_found", {})
    total_issues = sum(issues.values())
    if total_issues > 0:
        print(f"   Issues Found: {total_issues}")
        for severity, count in issues.items():
            if count > 0:
                print(f"     {severity.title()}: {count}")
    
    key_findings = summary.get("key_findings", [])[:3]
    if key_findings:
        print(f"\n🔍 Key Findings:")
        for finding in key_findings:
            print(f"   • {finding}")
    
    recommendations = result.get("recommendations", [])[:5]
    if recommendations:
        print(f"\n💡 Top Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    
    return result


async def main():
    """Main demo function"""
    print("🎪 Agentic Configuration Research System - Live Demo")
    print("=" * 60)
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Run demo scenarios
        demos = [
            demo_workspace_scan,
            demo_configuration_validation,
            demo_link_validation,
            demo_troubleshooting,
            demo_comprehensive_analysis
        ]
        
        for demo_func in demos:
            await demo_func()
            await asyncio.sleep(1)  # Brief pause between demos
        
        print("\n" + "=" * 60)
        print("🎉 Demo completed successfully!")
        print("\n🚀 Next steps:")
        print("   1. Start the server: python main.py server")
        print("   2. Access the API: http://localhost:8000")
        print("   3. Try the CLI: python main.py --help")
        print("   4. Run tests: python test_system.py")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        print("   Please ensure the system is properly set up:")
        print("   1. Run: python setup.py")
        print("   2. Run: python test_system.py")
        raise


if __name__ == "__main__":
    asyncio.run(main())