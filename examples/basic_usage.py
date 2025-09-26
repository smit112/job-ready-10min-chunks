"""
Basic usage examples for the Agentic AI Configuration Research System.
This file demonstrates the core functionality of the system.
"""
import asyncio
import sys
from pathlib import Path

# Add the workspace to the Python path
sys.path.append('/workspace')

from agents.config_research_agent import ConfigResearchAgent
from agents.troubleshooting_ai import TroubleshootingAI
from utils.validation_engine import ValidationEngine
from utils.excel_processor import ExcelProcessor
from utils.pdf_parser import PDFParser
from utils.link_analyzer import LinkAnalyzer


async def example_research_task():
    """Example of creating and executing a research task."""
    print("=== Research Task Example ===")
    
    # Initialize the research agent
    agent = ConfigResearchAgent()
    
    # Create a research task
    task_id = agent.create_research_task(
        name="Database Configuration Analysis",
        description="Analyze database configuration and validate settings",
        excel_files=[],  # Add Excel files here if available
        pdf_files=[],    # Add PDF files here if available
        links=[
            "https://docs.postgresql.org/",
            "https://dev.mysql.com/doc/",
            "https://docs.mongodb.com/"
        ],
        validation_rules={
            "required_fields": ["host", "port", "username", "password"],
            "port_range": {"min": 1, "max": 65535}
        }
    )
    
    print(f"Created research task: {task_id}")
    
    # Execute the task
    try:
        result = await agent.execute_research_task(task_id)
        print(f"Task completed in {result.processing_time:.2f} seconds")
        print(f"Overall status: {result.error_summary['total_errors']} errors found")
        
        # Print troubleshooting suggestions
        if result.troubleshooting_suggestions:
            print("\nTroubleshooting Suggestions:")
            for suggestion in result.troubleshooting_suggestions[:3]:
                print(f"- {suggestion['description']}")
        
    except Exception as e:
        print(f"Error executing task: {e}")


async def example_troubleshooting_case():
    """Example of creating a troubleshooting case and generating recommendations."""
    print("\n=== Troubleshooting Case Example ===")
    
    # Initialize the troubleshooting AI
    troubleshooting_ai = TroubleshootingAI()
    
    # Create a troubleshooting case
    case_id = troubleshooting_ai.create_troubleshooting_case(
        title="Database Connection Timeout",
        description="Application cannot connect to database, getting timeout errors",
        error_messages=[
            "Connection timeout after 30 seconds",
            "Unable to establish connection to database server",
            "Network unreachable"
        ],
        configuration_context={
            "host": "localhost",
            "port": 5432,
            "database": "myapp",
            "timeout": 30,
            "max_connections": 100
        },
        environment_info={
            "os": "Linux",
            "python_version": "3.9",
            "database_version": "PostgreSQL 13",
            "network": "local"
        },
        severity="high"
    )
    
    print(f"Created troubleshooting case: {case_id}")
    
    # Generate recommendations
    try:
        recommendations = await troubleshooting_ai.generate_recommendations(case_id)
        print(f"Generated {len(recommendations)} recommendations")
        
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"\nRecommendation {i}:")
            print(f"Title: {rec.title}")
            print(f"Confidence: {rec.confidence_score:.2f}")
            print(f"Source: {rec.source}")
            print(f"Description: {rec.description}")
            
            if rec.steps:
                print("Steps:")
                for step in rec.steps[:2]:
                    print(f"  {step['step']}. {step['description']}")
                    
    except Exception as e:
        print(f"Error generating recommendations: {e}")


async def example_configuration_validation():
    """Example of validating a configuration."""
    print("\n=== Configuration Validation Example ===")
    
    # Initialize the validation engine
    validation_engine = ValidationEngine()
    
    # Sample configuration data
    config_data = {
        "host": "localhost",
        "port": 5432,
        "username": "admin",
        "password": "secret123",
        "database": "myapp",
        "timeout": 30,
        "max_connections": 100,
        "ssl_enabled": True
    }
    
    # Validate the configuration
    try:
        report = await validation_engine.validate_configuration(
            config_data=config_data,
            config_type="database",
            target_path="/tmp/sample_config.json"
        )
        
        print(f"Validation completed in {report.execution_time:.2f} seconds")
        print(f"Overall status: {report.overall_status}")
        print(f"Rules passed: {report.passed_rules}/{report.total_rules}")
        
        # Print failed validations
        failed_results = [r for r in report.results if r.status == "failed"]
        if failed_results:
            print("\nFailed validations:")
            for result in failed_results:
                print(f"- {result.rule_name}: {result.message}")
        
        # Print warnings
        warning_results = [r for r in report.results if r.status == "warning"]
        if warning_results:
            print("\nWarnings:")
            for result in warning_results:
                print(f"- {result.rule_name}: {result.message}")
                
    except Exception as e:
        print(f"Error validating configuration: {e}")


def example_excel_processing():
    """Example of Excel file processing."""
    print("\n=== Excel Processing Example ===")
    
    # Initialize the Excel processor
    processor = ExcelProcessor(
        templates_dir="/workspace/data/excel_templates",
        output_dir="/workspace/data/excel_output"
    )
    
    # Create a sample configuration template
    try:
        template_path = processor.create_configuration_template(
            template_name="sample_database_config",
            config_schema={
                "host": {
                    "type": "string",
                    "required": True,
                    "description": "Database host address"
                },
                "port": {
                    "type": "integer",
                    "required": True,
                    "description": "Database port number",
                    "min": 1,
                    "max": 65535
                },
                "username": {
                    "type": "string",
                    "required": True,
                    "description": "Database username"
                },
                "password": {
                    "type": "string",
                    "required": True,
                    "description": "Database password"
                },
                "database": {
                    "type": "string",
                    "required": True,
                    "description": "Database name"
                },
                "timeout": {
                    "type": "integer",
                    "required": False,
                    "description": "Connection timeout in seconds",
                    "default": 30
                }
            }
        )
        
        print(f"Created configuration template: {template_path}")
        
        # Validate sample configuration
        sample_config = {
            "host": "localhost",
            "port": 5432,
            "username": "admin",
            "password": "secret123",
            "database": "myapp",
            "timeout": 30
        }
        
        validation_rules = {
            "host": {"required": True, "type": "string"},
            "port": {"required": True, "type": "integer", "min": 1, "max": 65535},
            "username": {"required": True, "type": "string"},
            "password": {"required": True, "type": "string"},
            "database": {"required": True, "type": "string"},
            "timeout": {"required": False, "type": "integer", "min": 1, "max": 300}
        }
        
        errors = processor.validate_configuration(sample_config, validation_rules)
        
        if errors:
            print("Validation errors found:")
            for field, field_errors in errors.items():
                print(f"  {field}: {', '.join(field_errors)}")
        else:
            print("Configuration validation passed!")
            
    except Exception as e:
        print(f"Error in Excel processing: {e}")


def example_link_analysis():
    """Example of link analysis."""
    print("\n=== Link Analysis Example ===")
    
    # Initialize the link analyzer
    analyzer = LinkAnalyzer(
        cache_dir="/workspace/data/link_cache",
        max_depth=2,
        timeout=30
    )
    
    # Sample URLs to analyze
    urls = [
        "https://docs.python.org/3/",
        "https://fastapi.tiangolo.com/",
        "https://pandas.pydata.org/docs/"
    ]
    
    try:
        # Analyze links
        print("Analyzing links...")
        link_infos = analyzer.analyze_links(urls, extract_content=True)
        
        print(f"Analyzed {len(link_infos)} links")
        
        # Print results
        for link_info in link_infos:
            print(f"\nURL: {link_info.url}")
            print(f"Status: {'Valid' if link_info.is_valid else 'Invalid'}")
            print(f"Title: {link_info.title}")
            print(f"Response time: {link_info.response_time:.2f}s")
            print(f"Content length: {link_info.content_length} bytes")
            
            if link_info.links_found:
                print(f"Links found: {len(link_info.links_found)}")
            
            if link_info.error_message:
                print(f"Error: {link_info.error_message}")
        
        # Get domain statistics
        stats = analyzer.get_domain_statistics(link_infos)
        print(f"\nDomain Statistics:")
        for domain, domain_stats in stats.items():
            print(f"  {domain}: {domain_stats['valid_count']}/{domain_stats['count']} valid")
            
    except Exception as e:
        print(f"Error in link analysis: {e}")


async def main():
    """Run all examples."""
    print("Agentic AI Configuration Research System - Examples")
    print("=" * 60)
    
    # Run examples
    await example_research_task()
    await example_troubleshooting_case()
    await example_configuration_validation()
    example_excel_processing()
    example_link_analysis()
    
    print("\n" + "=" * 60)
    print("Examples completed!")


if __name__ == "__main__":
    asyncio.run(main())