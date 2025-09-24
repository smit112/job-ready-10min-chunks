"""
MCP Server for Configuration Research and Troubleshooting
Provides tools for Excel processing, PDF analysis, and link validation
"""

import json
import asyncio
from typing import Any, Dict, List, Optional
from pathlib import Path
from loguru import logger

from pydantic import BaseModel
import pandas as pd
from PyPDF2 import PdfReader
import requests
import validators

from ..processors.excel_processor import ExcelProcessor
from ..processors.pdf_analyzer import PDFAnalyzer
from ..validators.link_validator import LinkValidator
from ..agents.config_agent import ConfigurationAgent


class MCPTool(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]


class MCPServer:
    """MCP Server for configuration research and troubleshooting"""
    
    def __init__(self, workspace_path: str = "/workspace"):
        self.workspace_path = Path(workspace_path)
        self.excel_processor = ExcelProcessor()
        self.pdf_analyzer = PDFAnalyzer()
        self.link_validator = LinkValidator()
        self.config_agent = ConfigurationAgent()
        
        # Initialize tools
        self.tools = self._initialize_tools()
        
        logger.info(f"MCP Server initialized with workspace: {workspace_path}")
    
    def _initialize_tools(self) -> List[MCPTool]:
        """Initialize available MCP tools"""
        return [
            MCPTool(
                name="process_excel_config",
                description="Process Excel files to extract configuration data and validate settings",
                input_schema={
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path to Excel file"},
                        "sheet_name": {"type": "string", "description": "Sheet name to process"},
                        "config_type": {"type": "string", "description": "Type of configuration (network, database, system)"}
                    },
                    "required": ["file_path"]
                }
            ),
            MCPTool(
                name="analyze_error_pdf",
                description="Analyze PDF error documents to extract troubleshooting information",
                input_schema={
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path to PDF error document"},
                        "error_type": {"type": "string", "description": "Type of error to focus on"},
                        "extract_solutions": {"type": "boolean", "description": "Whether to extract solution recommendations"}
                    },
                    "required": ["file_path"]
                }
            ),
            MCPTool(
                name="validate_configuration_links",
                description="Validate links and external resources in configuration documents",
                input_schema={
                    "type": "object",
                    "properties": {
                        "links": {"type": "array", "items": {"type": "string"}, "description": "List of URLs to validate"},
                        "check_content": {"type": "boolean", "description": "Whether to check content availability"},
                        "timeout": {"type": "number", "description": "Request timeout in seconds", "default": 10}
                    },
                    "required": ["links"]
                }
            ),
            MCPTool(
                name="automated_troubleshooting",
                description="Perform automated troubleshooting analysis using AI agents",
                input_schema={
                    "type": "object",
                    "properties": {
                        "issue_description": {"type": "string", "description": "Description of the configuration issue"},
                        "config_files": {"type": "array", "items": {"type": "string"}, "description": "Paths to related configuration files"},
                        "error_logs": {"type": "array", "items": {"type": "string"}, "description": "Error log entries"},
                        "system_type": {"type": "string", "description": "Type of system (web, database, network, etc.)"}
                    },
                    "required": ["issue_description"]
                }
            ),
            MCPTool(
                name="configuration_validation",
                description="Validate configuration files against best practices and standards",
                input_schema={
                    "type": "object",
                    "properties": {
                        "config_path": {"type": "string", "description": "Path to configuration file or directory"},
                        "validation_rules": {"type": "array", "items": {"type": "string"}, "description": "Specific validation rules to apply"},
                        "config_format": {"type": "string", "description": "Configuration format (json, yaml, ini, xml)"}
                    },
                    "required": ["config_path"]
                }
            )
        ]
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP tool calls"""
        try:
            if tool_name == "process_excel_config":
                return await self._process_excel_config(**arguments)
            elif tool_name == "analyze_error_pdf":
                return await self._analyze_error_pdf(**arguments)
            elif tool_name == "validate_configuration_links":
                return await self._validate_configuration_links(**arguments)
            elif tool_name == "automated_troubleshooting":
                return await self._automated_troubleshooting(**arguments)
            elif tool_name == "configuration_validation":
                return await self._configuration_validation(**arguments)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            logger.error(f"Error handling tool call {tool_name}: {str(e)}")
            return {"error": f"Tool execution failed: {str(e)}"}
    
    async def _process_excel_config(self, file_path: str, sheet_name: Optional[str] = None, 
                                  config_type: str = "general") -> Dict[str, Any]:
        """Process Excel configuration files"""
        try:
            result = await self.excel_processor.process_file(
                file_path, sheet_name, config_type
            )
            return {
                "success": True,
                "data": result,
                "message": f"Successfully processed Excel file: {file_path}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _analyze_error_pdf(self, file_path: str, error_type: Optional[str] = None,
                               extract_solutions: bool = True) -> Dict[str, Any]:
        """Analyze PDF error documents"""
        try:
            result = await self.pdf_analyzer.analyze_document(
                file_path, error_type, extract_solutions
            )
            return {
                "success": True,
                "analysis": result,
                "message": f"Successfully analyzed PDF: {file_path}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _validate_configuration_links(self, links: List[str], check_content: bool = False,
                                          timeout: int = 10) -> Dict[str, Any]:
        """Validate configuration links"""
        try:
            result = await self.link_validator.validate_links(
                links, check_content, timeout
            )
            return {
                "success": True,
                "validation_results": result,
                "message": f"Validated {len(links)} links"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _automated_troubleshooting(self, issue_description: str, 
                                       config_files: Optional[List[str]] = None,
                                       error_logs: Optional[List[str]] = None,
                                       system_type: str = "general") -> Dict[str, Any]:
        """Perform automated troubleshooting"""
        try:
            result = await self.config_agent.troubleshoot(
                issue_description, config_files, error_logs, system_type
            )
            return {
                "success": True,
                "troubleshooting_result": result,
                "message": "Automated troubleshooting completed"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _configuration_validation(self, config_path: str,
                                      validation_rules: Optional[List[str]] = None,
                                      config_format: Optional[str] = None) -> Dict[str, Any]:
        """Validate configuration files"""
        try:
            from ..validators.config_validator import ConfigValidator
            validator = ConfigValidator()
            
            result = await validator.validate_config(
                config_path, validation_rules, config_format
            )
            return {
                "success": True,
                "validation_result": result,
                "message": f"Configuration validation completed for: {config_path}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools"""
        return [tool.model_dump() for tool in self.tools]


if __name__ == "__main__":
    server = MCPServer()
    logger.info("MCP Server for Configuration Research started")
    logger.info(f"Available tools: {[tool.name for tool in server.tools]}")