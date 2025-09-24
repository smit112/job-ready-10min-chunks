"""
Cursor AI Integration Layer for Configuration Research System
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from loguru import logger
from datetime import datetime
import websockets
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..mcp_server.server import MCPServer
from ..agents.config_agent import ConfigurationAgent
from ..processors.excel_processor import ExcelProcessor
from ..processors.pdf_analyzer import PDFAnalyzer
from ..validators.link_validator import LinkValidator
from ..validators.config_validator import ConfigValidator


class ConfigResearchRequest(BaseModel):
    """Request model for configuration research"""
    task_type: str
    parameters: Dict[str, Any]
    priority: str = "normal"
    context: Optional[Dict[str, Any]] = None


class ConfigResearchResponse(BaseModel):
    """Response model for configuration research"""
    task_id: str
    status: str
    result: Dict[str, Any]
    timestamp: str
    processing_time: float


class CursorIntegration:
    """Integration layer connecting all components with Cursor AI"""
    
    def __init__(self, workspace_path: str = "/workspace"):
        self.workspace_path = Path(workspace_path)
        self.mcp_server = MCPServer(str(workspace_path))
        self.config_agent = ConfigurationAgent()
        self.excel_processor = ExcelProcessor()
        self.pdf_analyzer = PDFAnalyzer()
        self.link_validator = LinkValidator()
        self.config_validator = ConfigValidator()
        
        # Task management
        self.active_tasks = {}
        self.task_counter = 0
        
        # WebSocket connections for real-time updates
        self.websocket_connections = set()
        
        # Initialize FastAPI app
        self.app = self._create_fastapi_app()
        
        logger.info("Cursor AI Integration Layer initialized")
    
    def _create_fastapi_app(self) -> FastAPI:
        """Create FastAPI application with all endpoints"""
        app = FastAPI(
            title="Agentic Configuration Research API",
            description="AI-powered configuration research and troubleshooting system",
            version="1.0.0"
        )
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Add routes
        self._add_routes(app)
        
        return app
    
    def _add_routes(self, app: FastAPI):
        """Add API routes to FastAPI app"""
        
        @app.get("/")
        async def root():
            return {
                "message": "Agentic Configuration Research API",
                "version": "1.0.0",
                "status": "active",
                "available_tools": [tool.name for tool in self.mcp_server.tools]
            }
        
        @app.post("/research", response_model=ConfigResearchResponse)
        async def perform_research(request: ConfigResearchRequest):
            """Perform configuration research task"""
            try:
                task_id = f"task_{self.task_counter}"
                self.task_counter += 1
                
                start_time = datetime.now()
                
                # Route to appropriate handler based on task type
                if request.task_type == "excel_analysis":
                    result = await self._handle_excel_analysis(request.parameters)
                elif request.task_type == "pdf_analysis":
                    result = await self._handle_pdf_analysis(request.parameters)
                elif request.task_type == "link_validation":
                    result = await self._handle_link_validation(request.parameters)
                elif request.task_type == "config_validation":
                    result = await self._handle_config_validation(request.parameters)
                elif request.task_type == "troubleshooting":
                    result = await self._handle_troubleshooting(request.parameters)
                elif request.task_type == "comprehensive_analysis":
                    result = await self._handle_comprehensive_analysis(request.parameters)
                else:
                    raise HTTPException(status_code=400, detail=f"Unknown task type: {request.task_type}")
                
                processing_time = (datetime.now() - start_time).total_seconds()
                
                response = ConfigResearchResponse(
                    task_id=task_id,
                    status="completed",
                    result=result,
                    timestamp=datetime.now().isoformat(),
                    processing_time=processing_time
                )
                
                # Send real-time update via WebSocket
                await self._broadcast_update({
                    "type": "task_completed",
                    "task_id": task_id,
                    "result": result
                })
                
                return response
                
            except Exception as e:
                logger.error(f"Error processing research request: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.post("/upload/excel")
        async def upload_excel(file: UploadFile = File(...)):
            """Upload and analyze Excel file"""
            try:
                # Save uploaded file
                upload_path = self.workspace_path / "data" / "excel" / file.filename
                upload_path.parent.mkdir(parents=True, exist_ok=True)
                
                content = await file.read()
                upload_path.write_bytes(content)
                
                # Analyze the file
                result = await self.excel_processor.process_file(str(upload_path))
                
                return {
                    "message": "Excel file uploaded and analyzed successfully",
                    "file_path": str(upload_path),
                    "analysis": result
                }
                
            except Exception as e:
                logger.error(f"Error uploading Excel file: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.post("/upload/pdf")
        async def upload_pdf(file: UploadFile = File(...)):
            """Upload and analyze PDF file"""
            try:
                # Save uploaded file
                upload_path = self.workspace_path / "data" / "pdfs" / file.filename
                upload_path.parent.mkdir(parents=True, exist_ok=True)
                
                content = await file.read()
                upload_path.write_bytes(content)
                
                # Analyze the file
                result = await self.pdf_analyzer.analyze_document(str(upload_path))
                
                return {
                    "message": "PDF file uploaded and analyzed successfully",
                    "file_path": str(upload_path),
                    "analysis": result
                }
                
            except Exception as e:
                logger.error(f"Error uploading PDF file: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/tools")
        async def get_available_tools():
            """Get list of available MCP tools"""
            return {
                "tools": self.mcp_server.get_available_tools(),
                "categories": {
                    "data_processing": ["process_excel_config", "analyze_error_pdf"],
                    "validation": ["validate_configuration_links", "configuration_validation"],
                    "troubleshooting": ["automated_troubleshooting"]
                }
            }
        
        @app.post("/tools/{tool_name}")
        async def execute_tool(tool_name: str, parameters: Dict[str, Any]):
            """Execute specific MCP tool"""
            try:
                result = await self.mcp_server.handle_tool_call(tool_name, parameters)
                return {
                    "tool": tool_name,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/workspace/scan")
        async def scan_workspace():
            """Scan workspace for configuration files"""
            try:
                result = await self._scan_workspace()
                return result
            except Exception as e:
                logger.error(f"Error scanning workspace: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.websocket("/ws")
        async def websocket_endpoint(websocket):
            """WebSocket endpoint for real-time updates"""
            await websocket.accept()
            self.websocket_connections.add(websocket)
            try:
                while True:
                    # Keep connection alive
                    await websocket.receive_text()
            except Exception as e:
                logger.info(f"WebSocket connection closed: {str(e)}")
            finally:
                self.websocket_connections.discard(websocket)
    
    async def _handle_excel_analysis(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Excel file analysis"""
        file_path = parameters.get("file_path")
        sheet_name = parameters.get("sheet_name")
        config_type = parameters.get("config_type", "general")
        
        if not file_path:
            raise ValueError("file_path parameter is required")
        
        result = await self.excel_processor.process_file(file_path, sheet_name, config_type)
        
        return {
            "type": "excel_analysis",
            "file_path": file_path,
            "analysis": result,
            "recommendations": self._generate_excel_recommendations(result)
        }
    
    async def _handle_pdf_analysis(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle PDF error document analysis"""
        file_path = parameters.get("file_path")
        error_type = parameters.get("error_type")
        extract_solutions = parameters.get("extract_solutions", True)
        
        if not file_path:
            raise ValueError("file_path parameter is required")
        
        result = await self.pdf_analyzer.analyze_document(file_path, error_type, extract_solutions)
        
        return {
            "type": "pdf_analysis",
            "file_path": file_path,
            "analysis": result,
            "recommendations": self._generate_pdf_recommendations(result)
        }
    
    async def _handle_link_validation(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle link validation"""
        links = parameters.get("links", [])
        check_content = parameters.get("check_content", False)
        timeout = parameters.get("timeout", 10)
        
        if not links:
            raise ValueError("links parameter is required")
        
        async with LinkValidator() as validator:
            result = await validator.validate_links(links, check_content, timeout)
        
        return {
            "type": "link_validation",
            "links_checked": len(links),
            "validation_result": result,
            "recommendations": result.get("recommendations", [])
        }
    
    async def _handle_config_validation(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle configuration validation"""
        config_path = parameters.get("config_path")
        validation_rules = parameters.get("validation_rules")
        config_format = parameters.get("config_format")
        
        if not config_path:
            raise ValueError("config_path parameter is required")
        
        result = await self.config_validator.validate_config(
            config_path, validation_rules, config_format
        )
        
        return {
            "type": "config_validation",
            "config_path": config_path,
            "validation_result": result,
            "recommendations": self._generate_config_recommendations(result)
        }
    
    async def _handle_troubleshooting(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle automated troubleshooting"""
        issue_description = parameters.get("issue_description")
        config_files = parameters.get("config_files", [])
        error_logs = parameters.get("error_logs", [])
        system_type = parameters.get("system_type", "general")
        
        if not issue_description:
            raise ValueError("issue_description parameter is required")
        
        result = await self.config_agent.troubleshoot(
            issue_description, config_files, error_logs, system_type
        )
        
        return {
            "type": "troubleshooting",
            "issue_description": issue_description,
            "troubleshooting_result": result,
            "recommendations": self._generate_troubleshooting_recommendations(result)
        }
    
    async def _handle_comprehensive_analysis(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle comprehensive analysis of multiple resources"""
        excel_files = parameters.get("excel_files", [])
        pdf_files = parameters.get("pdf_files", [])
        config_files = parameters.get("config_files", [])
        links = parameters.get("links", [])
        issue_description = parameters.get("issue_description")
        
        results = {
            "excel_analysis": [],
            "pdf_analysis": [],
            "config_validation": [],
            "link_validation": None,
            "troubleshooting": None
        }
        
        # Process Excel files
        for excel_file in excel_files:
            try:
                analysis = await self.excel_processor.process_file(excel_file)
                results["excel_analysis"].append({
                    "file": excel_file,
                    "analysis": analysis
                })
            except Exception as e:
                results["excel_analysis"].append({
                    "file": excel_file,
                    "error": str(e)
                })
        
        # Process PDF files
        for pdf_file in pdf_files:
            try:
                analysis = await self.pdf_analyzer.analyze_document(pdf_file)
                results["pdf_analysis"].append({
                    "file": pdf_file,
                    "analysis": analysis
                })
            except Exception as e:
                results["pdf_analysis"].append({
                    "file": pdf_file,
                    "error": str(e)
                })
        
        # Validate configuration files
        for config_file in config_files:
            try:
                validation = await self.config_validator.validate_config(config_file)
                results["config_validation"].append({
                    "file": config_file,
                    "validation": validation
                })
            except Exception as e:
                results["config_validation"].append({
                    "file": config_file,
                    "error": str(e)
                })
        
        # Validate links
        if links:
            try:
                async with LinkValidator() as validator:
                    results["link_validation"] = await validator.validate_links(links)
            except Exception as e:
                results["link_validation"] = {"error": str(e)}
        
        # Perform troubleshooting if issue description provided
        if issue_description:
            try:
                results["troubleshooting"] = await self.config_agent.troubleshoot(
                    issue_description, config_files, []
                )
            except Exception as e:
                results["troubleshooting"] = {"error": str(e)}
        
        # Generate comprehensive recommendations
        recommendations = self._generate_comprehensive_recommendations(results)
        
        return {
            "type": "comprehensive_analysis",
            "results": results,
            "recommendations": recommendations,
            "summary": self._generate_comprehensive_summary(results)
        }
    
    async def _scan_workspace(self) -> Dict[str, Any]:
        """Scan workspace for configuration files and resources"""
        scan_result = {
            "excel_files": [],
            "pdf_files": [],
            "config_files": [],
            "other_files": [],
            "total_files": 0,
            "scan_timestamp": datetime.now().isoformat()
        }
        
        try:
            # Scan for Excel files
            excel_patterns = ["*.xlsx", "*.xls", "*.xlsm"]
            for pattern in excel_patterns:
                for file_path in self.workspace_path.rglob(pattern):
                    scan_result["excel_files"].append({
                        "path": str(file_path),
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
            
            # Scan for PDF files
            for file_path in self.workspace_path.rglob("*.pdf"):
                scan_result["pdf_files"].append({
                    "path": str(file_path),
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
            
            # Scan for configuration files
            config_patterns = ["*.json", "*.yaml", "*.yml", "*.xml", "*.ini", "*.conf", "*.cfg", "*.properties"]
            for pattern in config_patterns:
                for file_path in self.workspace_path.rglob(pattern):
                    scan_result["config_files"].append({
                        "path": str(file_path),
                        "type": file_path.suffix.lstrip('.'),
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
            
            # Calculate totals
            scan_result["total_files"] = (
                len(scan_result["excel_files"]) +
                len(scan_result["pdf_files"]) +
                len(scan_result["config_files"])
            )
            
            return scan_result
            
        except Exception as e:
            logger.error(f"Error scanning workspace: {str(e)}")
            raise
    
    def _generate_excel_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on Excel analysis"""
        recommendations = []
        
        validation_results = analysis.get("validation_results", {})
        for sheet, results in validation_results.items():
            if results.get("security_issues"):
                recommendations.append(f"Address security issues in sheet '{sheet}'")
            
            recommendations.extend(results.get("recommendations", []))
        
        if not recommendations:
            recommendations.append("Excel file analysis completed successfully - no major issues found")
        
        return recommendations
    
    def _generate_pdf_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on PDF analysis"""
        recommendations = analysis.get("recommendations", {})
        
        all_recommendations = []
        all_recommendations.extend(recommendations.get("immediate_actions", []))
        all_recommendations.extend(recommendations.get("investigation_steps", []))
        all_recommendations.extend(recommendations.get("preventive_measures", []))
        
        return all_recommendations
    
    def _generate_config_recommendations(self, validation: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on configuration validation"""
        if isinstance(validation, dict) and "summary" in validation:
            return validation["summary"].get("recommendations", [])
        
        return ["Configuration validation completed"]
    
    def _generate_troubleshooting_recommendations(self, result: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on troubleshooting result"""
        plan = result.get("troubleshooting_plan", {})
        
        recommendations = []
        recommendations.extend(plan.get("immediate_actions", []))
        recommendations.extend(plan.get("investigation_steps", []))
        recommendations.extend(plan.get("resolution_steps", []))
        
        return recommendations
    
    def _generate_comprehensive_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate comprehensive recommendations from all analyses"""
        recommendations = []
        
        # Priority-based recommendations
        high_priority = []
        medium_priority = []
        low_priority = []
        
        # Analyze results and categorize recommendations
        if results.get("troubleshooting") and not results["troubleshooting"].get("error"):
            plan = results["troubleshooting"].get("troubleshooting_plan", {})
            high_priority.extend(plan.get("immediate_actions", []))
            medium_priority.extend(plan.get("investigation_steps", []))
        
        # Add Excel-specific recommendations
        for excel_result in results.get("excel_analysis", []):
            if not excel_result.get("error"):
                analysis = excel_result.get("analysis", {})
                validation_results = analysis.get("validation_results", {})
                for sheet_results in validation_results.values():
                    if sheet_results.get("security_issues"):
                        high_priority.append("Critical: Address security issues in Excel configurations")
        
        # Add PDF-specific recommendations
        for pdf_result in results.get("pdf_analysis", []):
            if not pdf_result.get("error"):
                analysis = pdf_result.get("analysis", {})
                pdf_recommendations = analysis.get("recommendations", {})
                high_priority.extend(pdf_recommendations.get("immediate_actions", []))
        
        # Add configuration validation recommendations
        for config_result in results.get("config_validation", []):
            if not config_result.get("error"):
                validation = config_result.get("validation", {})
                if isinstance(validation, dict) and "summary" in validation:
                    summary = validation["summary"]
                    if summary.get("overall_status") == "failed":
                        high_priority.append("Critical: Fix configuration validation errors")
                    elif summary.get("total_warnings", 0) > 0:
                        medium_priority.append("Review configuration warnings")
        
        # Add link validation recommendations
        if results.get("link_validation") and not results["link_validation"].get("error"):
            link_recommendations = results["link_validation"].get("recommendations", [])
            medium_priority.extend(link_recommendations)
        
        # Combine and prioritize
        if high_priority:
            recommendations.append("HIGH PRIORITY ACTIONS:")
            recommendations.extend([f"  • {rec}" for rec in high_priority[:5]])  # Top 5
        
        if medium_priority:
            recommendations.append("MEDIUM PRIORITY ACTIONS:")
            recommendations.extend([f"  • {rec}" for rec in medium_priority[:5]])  # Top 5
        
        # Add general recommendations
        recommendations.extend([
            "GENERAL RECOMMENDATIONS:",
            "  • Implement automated monitoring for configuration changes",
            "  • Regular security audits of configuration files",
            "  • Maintain documentation for all configuration changes",
            "  • Establish backup and recovery procedures"
        ])
        
        return recommendations
    
    def _generate_comprehensive_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive summary of all analyses"""
        summary = {
            "files_processed": {
                "excel": len(results.get("excel_analysis", [])),
                "pdf": len(results.get("pdf_analysis", [])),
                "config": len(results.get("config_validation", []))
            },
            "issues_found": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            },
            "overall_health_score": 100,
            "key_findings": [],
            "next_steps": []
        }
        
        # Analyze results for issues
        for excel_result in results.get("excel_analysis", []):
            if not excel_result.get("error"):
                analysis = excel_result.get("analysis", {})
                validation_results = analysis.get("validation_results", {})
                for sheet_results in validation_results.values():
                    if sheet_results.get("security_issues"):
                        summary["issues_found"]["critical"] += len(sheet_results["security_issues"])
                        summary["overall_health_score"] -= 10
        
        # Add key findings
        if summary["issues_found"]["critical"] > 0:
            summary["key_findings"].append(f"Found {summary['issues_found']['critical']} critical security issues")
            summary["next_steps"].append("Immediate action required for critical issues")
        
        if summary["files_processed"]["excel"] > 0:
            summary["key_findings"].append(f"Analyzed {summary['files_processed']['excel']} Excel configuration files")
        
        if summary["files_processed"]["pdf"] > 0:
            summary["key_findings"].append(f"Processed {summary['files_processed']['pdf']} PDF error documents")
        
        # Ensure health score doesn't go below 0
        summary["overall_health_score"] = max(0, summary["overall_health_score"])
        
        return summary
    
    async def _broadcast_update(self, message: Dict[str, Any]):
        """Broadcast update to all WebSocket connections"""
        if self.websocket_connections:
            disconnected = set()
            for websocket in self.websocket_connections:
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    logger.warning(f"Failed to send WebSocket message: {str(e)}")
                    disconnected.add(websocket)
            
            # Remove disconnected websockets
            self.websocket_connections -= disconnected
    
    async def start_server(self, host: str = "0.0.0.0", port: int = 8000):
        """Start the FastAPI server"""
        import uvicorn
        
        logger.info(f"Starting Cursor AI Integration server on {host}:{port}")
        
        config = uvicorn.Config(
            self.app,
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )
        
        server = uvicorn.Server(config)
        await server.serve()


# Utility functions for initialization
def create_integration_layer(workspace_path: str = "/workspace") -> CursorIntegration:
    """Create and configure the integration layer"""
    return CursorIntegration(workspace_path)


async def run_server(workspace_path: str = "/workspace", host: str = "0.0.0.0", port: int = 8000):
    """Run the integration server"""
    integration = create_integration_layer(workspace_path)
    await integration.start_server(host, port)