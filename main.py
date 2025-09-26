#!/usr/bin/env python3
"""
Main entry point for Agentic Configuration Research System
"""

import asyncio
import argparse
import sys
from pathlib import Path
from loguru import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.integration.cursor_integration import run_server, CursorIntegration
from src.mcp_server.server import MCPServer


def setup_logging(debug: bool = False):
    """Setup logging configuration"""
    log_level = "DEBUG" if debug else "INFO"
    
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    # Add file logging
    logger.add(
        "logs/agentic_config_research.log",
        rotation="10 MB",
        retention="10 days",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )


async def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="Agentic Configuration Research System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py server                    # Start web server (default)
  python main.py server --port 9000       # Start on custom port
  python main.py mcp                       # Start MCP server only
  python main.py analyze --excel data.xlsx # Analyze Excel file
  python main.py validate --config app.json # Validate config file
        """
    )
    
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--workspace", default="/workspace", help="Workspace directory path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Server command
    server_parser = subparsers.add_parser("server", help="Start web server (default)")
    server_parser.add_argument("--host", default="0.0.0.0", help="Server host")
    server_parser.add_argument("--port", type=int, default=8000, help="Server port")
    
    # MCP server command
    mcp_parser = subparsers.add_parser("mcp", help="Start MCP server only")
    
    # Analysis commands
    analyze_parser = subparsers.add_parser("analyze", help="Analyze files")
    analyze_parser.add_argument("--excel", help="Excel file to analyze")
    analyze_parser.add_argument("--pdf", help="PDF file to analyze")
    analyze_parser.add_argument("--sheet", help="Excel sheet name")
    analyze_parser.add_argument("--config-type", default="general", help="Configuration type")
    
    # Validation commands
    validate_parser = subparsers.add_parser("validate", help="Validate configurations")
    validate_parser.add_argument("--config", help="Configuration file/directory to validate")
    validate_parser.add_argument("--links", nargs="+", help="Links to validate")
    validate_parser.add_argument("--format", help="Configuration format")
    
    # Troubleshooting command
    trouble_parser = subparsers.add_parser("troubleshoot", help="Automated troubleshooting")
    trouble_parser.add_argument("--issue", required=True, help="Issue description")
    trouble_parser.add_argument("--config-files", nargs="+", help="Related config files")
    trouble_parser.add_argument("--error-logs", nargs="+", help="Error log entries")
    trouble_parser.add_argument("--system-type", default="general", help="System type")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.debug)
    
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    
    logger.info("Starting Agentic Configuration Research System")
    logger.info(f"Workspace: {args.workspace}")
    
    try:
        if not args.command or args.command == "server":
            # Start web server (default)
            await run_server(args.workspace, args.host, args.port)
        
        elif args.command == "mcp":
            # Start MCP server only
            mcp_server = MCPServer(args.workspace)
            logger.info("MCP Server started - waiting for connections...")
            # Keep server running
            while True:
                await asyncio.sleep(1)
        
        elif args.command == "analyze":
            # Perform analysis
            integration = CursorIntegration(args.workspace)
            
            if args.excel:
                logger.info(f"Analyzing Excel file: {args.excel}")
                result = await integration._handle_excel_analysis({
                    "file_path": args.excel,
                    "sheet_name": args.sheet,
                    "config_type": args.config_type
                })
                print("\n=== EXCEL ANALYSIS RESULTS ===")
                print_analysis_result(result)
            
            elif args.pdf:
                logger.info(f"Analyzing PDF file: {args.pdf}")
                result = await integration._handle_pdf_analysis({
                    "file_path": args.pdf
                })
                print("\n=== PDF ANALYSIS RESULTS ===")
                print_analysis_result(result)
        
        elif args.command == "validate":
            # Perform validation
            integration = CursorIntegration(args.workspace)
            
            if args.config:
                logger.info(f"Validating configuration: {args.config}")
                result = await integration._handle_config_validation({
                    "config_path": args.config,
                    "config_format": args.format
                })
                print("\n=== CONFIGURATION VALIDATION RESULTS ===")
                print_analysis_result(result)
            
            elif args.links:
                logger.info(f"Validating {len(args.links)} links")
                result = await integration._handle_link_validation({
                    "links": args.links
                })
                print("\n=== LINK VALIDATION RESULTS ===")
                print_analysis_result(result)
        
        elif args.command == "troubleshoot":
            # Perform troubleshooting
            integration = CursorIntegration(args.workspace)
            
            logger.info(f"Performing troubleshooting analysis")
            result = await integration._handle_troubleshooting({
                "issue_description": args.issue,
                "config_files": args.config_files or [],
                "error_logs": args.error_logs or [],
                "system_type": args.system_type
            })
            print("\n=== TROUBLESHOOTING RESULTS ===")
            print_analysis_result(result)
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        if args.debug:
            raise
        sys.exit(1)


def print_analysis_result(result: dict):
    """Pretty print analysis results"""
    import json
    
    # Extract key information for display
    if "recommendations" in result and result["recommendations"]:
        print("\n📋 RECOMMENDATIONS:")
        for i, rec in enumerate(result["recommendations"][:10], 1):
            print(f"  {i}. {rec}")
    
    if "summary" in result:
        print(f"\n📊 SUMMARY:")
        summary = result["summary"]
        if isinstance(summary, dict):
            for key, value in summary.items():
                if key != "recommendations":
                    print(f"  {key}: {value}")
    
    # Show first few key results
    print(f"\n🔍 ANALYSIS TYPE: {result.get('type', 'unknown')}")
    
    if result.get("type") == "link_validation":
        validation_result = result.get("validation_result", {})
        summary = validation_result.get("summary", {})
        print(f"  Total links: {summary.get('total_links', 0)}")
        print(f"  Success rate: {summary.get('success_rate', 0):.1f}%")
        print(f"  Failed: {summary.get('failed', 0)}")
    
    # Offer to save full results
    print(f"\n💾 Full results available in JSON format")
    print(f"   Result keys: {list(result.keys())}")


if __name__ == "__main__":
    asyncio.run(main())