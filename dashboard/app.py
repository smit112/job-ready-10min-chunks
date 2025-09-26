"""
Web dashboard for configuration management and monitoring.
Provides a modern web interface for the agentic AI configuration research system.
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
from datetime import datetime, timedelta
import uuid

# Web framework imports
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import our components
import sys
sys.path.append('/workspace')
from agents.config_research_agent import ConfigResearchAgent, ResearchTask, ResearchResult
from agents.troubleshooting_ai import TroubleshootingAI, TroubleshootingCase, TroubleshootingRecommendation
from utils.validation_engine import ValidationEngine, ValidationReport
from utils.excel_processor import ExcelProcessor
from utils.pdf_parser import PDFParser
from utils.link_analyzer import LinkAnalyzer
from configs.settings import settings

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Configuration Research Dashboard",
    description="Agentic AI system for configuration research and validation",
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

# Initialize components
config_agent = ConfigResearchAgent()
troubleshooting_ai = TroubleshootingAI()
validation_engine = ValidationEngine()

# Create static and templates directories
static_dir = Path("/workspace/dashboard/static")
templates_dir = Path("/workspace/dashboard/templates")
static_dir.mkdir(parents=True, exist_ok=True)
templates_dir.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Initialize templates
templates = Jinja2Templates(directory=str(templates_dir))

# Pydantic models for API
class ResearchTaskRequest(BaseModel):
    name: str
    description: str
    excel_files: List[str] = []
    pdf_files: List[str] = []
    links: List[str] = []
    validation_rules: Dict[str, Any] = {}

class TroubleshootingCaseRequest(BaseModel):
    title: str
    description: str
    error_messages: List[str]
    configuration_context: Dict[str, Any]
    environment_info: Dict[str, Any]
    severity: str = "medium"

class ValidationRequest(BaseModel):
    config_data: Dict[str, Any]
    config_type: str = "generic"
    target_path: Optional[str] = None

# Dashboard routes
@app.get("/", response_class=HTMLResponse)
async def dashboard_home():
    """Main dashboard page."""
    return templates.TemplateResponse("dashboard.html", {
        "request": {},
        "title": "Configuration Research Dashboard",
        "stats": await get_dashboard_stats()
    })

@app.get("/chat", response_class=HTMLResponse)
async def chat_interface():
    """Chat interface for agent interaction."""
    return templates.TemplateResponse("chat.html", {
        "request": {},
        "title": "Configuration Research Agent - Chat",
        "current_time": datetime.now().strftime("%H:%M")
    })

@app.get("/api/stats")
async def get_dashboard_stats():
    """Get dashboard statistics."""
    try:
        # Get research task stats
        tasks = config_agent.list_tasks()
        task_stats = {
            "total_tasks": len(tasks),
            "completed_tasks": len([t for t in tasks if t["status"] == "completed"]),
            "running_tasks": len([t for t in tasks if t["status"] == "running"]),
            "failed_tasks": len([t for t in tasks if t["status"] == "failed"])
        }
        
        # Get troubleshooting stats
        kb_stats = troubleshooting_ai.get_knowledge_base_stats()
        
        # Get validation stats
        validation_history = validation_engine.get_validation_history(limit=100)
        validation_stats = {
            "total_validations": len(validation_history),
            "passed_validations": len([v for v in validation_history if v.overall_status == "passed"]),
            "failed_validations": len([v for v in validation_history if v.overall_status == "failed"]),
            "warning_validations": len([v for v in validation_history if v.overall_status == "warning"])
        }
        
        return {
            "task_stats": task_stats,
            "knowledge_base_stats": kb_stats,
            "validation_stats": validation_stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Research Task API endpoints
@app.post("/api/research-tasks")
async def create_research_task(request: ResearchTaskRequest):
    """Create a new research task."""
    try:
        task_id = config_agent.create_research_task(
            name=request.name,
            description=request.description,
            excel_files=request.excel_files,
            pdf_files=request.pdf_files,
            links=request.links,
            validation_rules=request.validation_rules
        )
        return {"task_id": task_id, "status": "created"}
    except Exception as e:
        logger.error(f"Error creating research task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/research-tasks")
async def list_research_tasks():
    """List all research tasks."""
    try:
        return config_agent.list_tasks()
    except Exception as e:
        logger.error(f"Error listing research tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/research-tasks/{task_id}")
async def get_research_task(task_id: str):
    """Get research task details."""
    try:
        return config_agent.get_task_status(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting research task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/research-tasks/{task_id}/execute")
async def execute_research_task(task_id: str, background_tasks: BackgroundTasks):
    """Execute a research task."""
    try:
        # Execute task in background
        background_tasks.add_task(config_agent.execute_research_task, task_id)
        return {"status": "executing", "task_id": task_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing research task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/research-tasks/{task_id}/results")
async def get_research_task_results(task_id: str):
    """Get research task results."""
    try:
        result = config_agent.get_task_result(task_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Results not found")
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting research task results: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Troubleshooting API endpoints
@app.post("/api/troubleshooting-cases")
async def create_troubleshooting_case(request: TroubleshootingCaseRequest):
    """Create a new troubleshooting case."""
    try:
        case_id = troubleshooting_ai.create_troubleshooting_case(
            title=request.title,
            description=request.description,
            error_messages=request.error_messages,
            configuration_context=request.configuration_context,
            environment_info=request.environment_info,
            severity=request.severity
        )
        return {"case_id": case_id, "status": "created"}
    except Exception as e:
        logger.error(f"Error creating troubleshooting case: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/troubleshooting-cases")
async def list_troubleshooting_cases():
    """List all troubleshooting cases."""
    try:
        cases = []
        for case in troubleshooting_ai.troubleshooting_cases.values():
            cases.append({
                "case_id": case.case_id,
                "title": case.title,
                "severity": case.severity,
                "status": case.status,
                "created_at": case.created_at
            })
        return cases
    except Exception as e:
        logger.error(f"Error listing troubleshooting cases: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/troubleshooting-cases/{case_id}")
async def get_troubleshooting_case(case_id: str):
    """Get troubleshooting case details."""
    try:
        if case_id not in troubleshooting_ai.troubleshooting_cases:
            raise HTTPException(status_code=404, detail="Case not found")
        
        case = troubleshooting_ai.troubleshooting_cases[case_id]
        return case
    except Exception as e:
        logger.error(f"Error getting troubleshooting case: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/troubleshooting-cases/{case_id}/recommendations")
async def generate_troubleshooting_recommendations(case_id: str):
    """Generate troubleshooting recommendations for a case."""
    try:
        recommendations = await troubleshooting_ai.generate_recommendations(case_id)
        return recommendations
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/troubleshooting-cases/{case_id}/recommendations")
async def get_troubleshooting_recommendations(case_id: str):
    """Get troubleshooting recommendations for a case."""
    try:
        recommendations = troubleshooting_ai.get_case_recommendations(case_id)
        return recommendations
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Validation API endpoints
@app.post("/api/validate")
async def validate_configuration(request: ValidationRequest):
    """Validate a configuration."""
    try:
        report = await validation_engine.validate_configuration(
            config_data=request.config_data,
            config_type=request.config_type,
            target_path=request.target_path
        )
        return report
    except Exception as e:
        logger.error(f"Error validating configuration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/validation-history")
async def get_validation_history(limit: int = 10):
    """Get validation history."""
    try:
        history = validation_engine.get_validation_history(limit=limit)
        return history
    except Exception as e:
        logger.error(f"Error getting validation history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# MCP Integration - File upload endpoints
@app.post("/api/upload/file")
async def upload_file(file: UploadFile = File(...), session_id: str = Form(...)):
    """Upload and process any supported file type."""
    try:
        # Save uploaded file
        upload_dir = Path("/workspace/data/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_dir / f"{session_id}_{uuid.uuid4()}_{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process file based on type
        processed_data = {}
        
        if file.filename.lower().endswith(('.xlsx', '.xls')):
            # Process Excel file
            excel_processor = ExcelProcessor(
                settings.excel_templates_dir,
                settings.excel_output_dir
            )
            configs = excel_processor.read_excel_file(file_path)
            processed_data = {
                "type": "excel",
                "sheets": list(configs.keys()),
                "configurations": {k: {
                    "headers": v.headers,
                    "row_count": len(v.data),
                    "validation_rules": v.validation_rules
                } for k, v in configs.items()}
            }
            
        elif file.filename.lower().endswith('.pdf'):
            # Process PDF file
            pdf_parser = PDFParser(
                settings.pdf_docs_dir,
                settings.pdf_errors_dir
            )
            pdf_doc = pdf_parser.parse_pdf(file_path)
            processed_data = {
                "type": "pdf",
                "title": pdf_doc.title,
                "page_count": len(pdf_doc.pages),
                "error_patterns": pdf_doc.error_patterns,
                "troubleshooting_steps": pdf_doc.troubleshooting_steps,
                "configuration_snippets": pdf_doc.configuration_snippets
            }
            
        elif file.filename.lower().endswith(('.json', '.yaml', '.yml')):
            # Process configuration file
            with open(file_path, 'r', encoding='utf-8') as f:
                if file.filename.lower().endswith('.json'):
                    import json
                    config_data = json.load(f)
                else:
                    import yaml
                    config_data = yaml.safe_load(f)
            
            processed_data = {
                "type": "config",
                "format": file.filename.split('.')[-1],
                "data": config_data,
                "keys": list(config_data.keys()) if isinstance(config_data, dict) else []
            }
            
        else:
            # Process as text file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            processed_data = {
                "type": "text",
                "content": content,
                "line_count": len(content.split('\n')),
                "word_count": len(content.split())
            }
        
        return {
            "file_path": str(file_path),
            "processed_data": processed_data,
            "status": "processed"
        }
        
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Legacy endpoints for backward compatibility
@app.post("/api/upload/excel")
async def upload_excel_file(file: UploadFile = File(...)):
    """Upload Excel file for processing."""
    return await upload_file(file, "legacy")

@app.post("/api/upload/pdf")
async def upload_pdf_file(file: UploadFile = File(...)):
    """Upload PDF file for processing."""
    return await upload_file(file, "legacy")

# Knowledge base endpoints
@app.get("/api/knowledge-base")
async def search_knowledge_base(query: str = "", limit: int = 10):
    """Search knowledge base."""
    try:
        if query:
            results = troubleshooting_ai.search_knowledge_base(query, limit=limit)
        else:
            results = list(troubleshooting_ai.knowledge_base.values())[:limit]
        
        return results
    except Exception as e:
        logger.error(f"Error searching knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/knowledge-base/stats")
async def get_knowledge_base_stats():
    """Get knowledge base statistics."""
    try:
        return troubleshooting_ai.get_knowledge_base_stats()
    except Exception as e:
        logger.error(f"Error getting knowledge base stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# MCP Integration - Agent Chat endpoint
class ChatRequest(BaseModel):
    session_id: str
    message: str
    files: List[Dict[str, Any]] = []

@app.post("/api/chat/agent")
async def chat_with_agent(request: ChatRequest):
    """Chat with the configuration research agent using MCP integration."""
    try:
        # Process the message and files using the agent
        response = await process_agent_request(request.message, request.files, request.session_id)
        return response
        
    except Exception as e:
        logger.error(f"Error in agent chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_agent_request(message: str, files: List[Dict[str, Any]], session_id: str):
    """Process agent request with MCP integration."""
    try:
        # Analyze the message and files
        analysis_result = await analyze_request(message, files)
        
        # Generate response using the agent
        response = await generate_agent_response(message, files, analysis_result, session_id)
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing agent request: {str(e)}")
        return {
            "message": f"I encountered an error processing your request: {str(e)}",
            "attachments": [],
            "metadata": {"error": True, "error_message": str(e)}
        }

async def analyze_request(message: str, files: List[Dict[str, Any]]):
    """Analyze the user request and uploaded files."""
    analysis = {
        "message_type": "general",
        "files_analysis": {},
        "keywords": [],
        "intent": "unknown"
    }
    
    # Analyze message intent
    message_lower = message.lower()
    if any(word in message_lower for word in ["analyze", "analysis", "examine"]):
        analysis["intent"] = "analysis"
    elif any(word in message_lower for word in ["validate", "validation", "check"]):
        analysis["intent"] = "validation"
    elif any(word in message_lower for word in ["troubleshoot", "error", "issue", "problem"]):
        analysis["intent"] = "troubleshooting"
    elif any(word in message_lower for word in ["recommend", "suggestion", "best practice"]):
        analysis["intent"] = "recommendation"
    
    # Analyze files
    for file_data in files:
        file_analysis = {
            "type": file_data.get("type", "unknown"),
            "processed_data": file_data.get("processed_data", {}),
            "insights": []
        }
        
        # Extract insights based on file type
        if file_data.get("type") == "excel":
            file_analysis["insights"] = analyze_excel_file(file_data.get("processed_data", {}))
        elif file_data.get("type") == "pdf":
            file_analysis["insights"] = analyze_pdf_file(file_data.get("processed_data", {}))
        elif file_data.get("type") == "config":
            file_analysis["insights"] = analyze_config_file(file_data.get("processed_data", {}))
        
        analysis["files_analysis"][file_data.get("name", "unknown")] = file_analysis
    
    return analysis

def analyze_excel_file(processed_data: Dict[str, Any]):
    """Analyze Excel file data."""
    insights = []
    
    if "configurations" in processed_data:
        for sheet_name, config in processed_data["configurations"].items():
            insights.append(f"Found configuration sheet '{sheet_name}' with {config.get('row_count', 0)} rows")
            
            if config.get("validation_rules"):
                insights.append(f"Sheet '{sheet_name}' has validation rules defined")
            
            headers = config.get("headers", [])
            if any("password" in h.lower() for h in headers):
                insights.append("⚠️ Password fields detected - consider security implications")
            
            if any("port" in h.lower() for h in headers):
                insights.append("🔌 Port configurations found - validate port ranges")
    
    return insights

def analyze_pdf_file(processed_data: Dict[str, Any]):
    """Analyze PDF file data."""
    insights = []
    
    if "error_patterns" in processed_data:
        error_count = len(processed_data["error_patterns"])
        if error_count > 0:
            insights.append(f"📋 Found {error_count} error patterns in documentation")
            
            # Categorize errors by severity
            critical_errors = [e for e in processed_data["error_patterns"] if e.get("severity") == "CRITICAL"]
            if critical_errors:
                insights.append(f"🚨 {len(critical_errors)} critical error patterns identified")
    
    if "troubleshooting_steps" in processed_data:
        steps_count = len(processed_data["troubleshooting_steps"])
        if steps_count > 0:
            insights.append(f"🛠️ Found {steps_count} troubleshooting steps")
    
    if "configuration_snippets" in processed_data:
        snippets_count = len(processed_data["configuration_snippets"])
        if snippets_count > 0:
            insights.append(f"⚙️ Found {snippets_count} configuration snippets")
    
    return insights

def analyze_config_file(processed_data: Dict[str, Any]):
    """Analyze configuration file data."""
    insights = []
    
    if "data" in processed_data:
        config_data = processed_data["data"]
        keys = processed_data.get("keys", [])
        
        insights.append(f"📄 Configuration file with {len(keys)} main sections")
        
        # Check for common configuration patterns
        if any("password" in k.lower() for k in keys):
            insights.append("🔐 Password configuration detected")
        
        if any("port" in k.lower() for k in keys):
            insights.append("🔌 Port configuration found")
        
        if any("database" in k.lower() for k in keys):
            insights.append("🗄️ Database configuration detected")
        
        if any("api" in k.lower() for k in keys):
            insights.append("🌐 API configuration detected")
    
    return insights

async def generate_agent_response(message: str, files: List[Dict[str, Any]], analysis: Dict[str, Any], session_id: str):
    """Generate intelligent response using the agent."""
    try:
        # Create a research task for comprehensive analysis
        task_id = config_agent.create_research_task(
            name=f"Chat Analysis - {session_id}",
            description=message,
            excel_files=[f["server_path"] for f in files if f.get("type") == "excel"],
            pdf_files=[f["server_path"] for f in files if f.get("type") == "pdf"],
            links=[],  # Could be extracted from message
            validation_rules={}
        )
        
        # Execute the research task
        result = await config_agent.execute_research_task(task_id)
        
        # Generate response based on analysis and results
        response_message = generate_response_message(message, analysis, result)
        
        # Create attachments from results
        attachments = create_response_attachments(result)
        
        return {
            "message": response_message,
            "attachments": attachments,
            "metadata": {
                "task_id": task_id,
                "intent": analysis["intent"],
                "files_processed": len(files),
                "analysis_complete": True
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating agent response: {str(e)}")
        return {
            "message": f"I analyzed your request and found some insights, but encountered an issue: {str(e)}",
            "attachments": [],
            "metadata": {"error": True, "error_message": str(e)}
        }

def generate_response_message(message: str, analysis: Dict[str, Any], result: ResearchResult):
    """Generate a comprehensive response message."""
    response_parts = []
    
    # Start with analysis summary
    if analysis["intent"] == "analysis":
        response_parts.append("📊 **Configuration Analysis Results**\n")
    elif analysis["intent"] == "validation":
        response_parts.append("✅ **Configuration Validation Results**\n")
    elif analysis["intent"] == "troubleshooting":
        response_parts.append("🛠️ **Troubleshooting Analysis**\n")
    else:
        response_parts.append("🔍 **Configuration Research Results**\n")
    
    # Add file insights
    if analysis["files_analysis"]:
        response_parts.append("**File Analysis:**")
        for file_name, file_analysis in analysis["files_analysis"].items():
            response_parts.append(f"\n📁 **{file_name}** ({file_analysis['type']})")
            for insight in file_analysis["insights"]:
                response_parts.append(f"  • {insight}")
    
    # Add validation results
    if result.validation_results.get("overall_status"):
        status = result.validation_results["overall_status"]
        if status == "passed":
            response_parts.append(f"\n✅ **Validation Status:** All validations passed")
        elif status == "failed":
            response_parts.append(f"\n❌ **Validation Status:** {result.validation_results.get('failed_rules', 0)} validation failures")
        else:
            response_parts.append(f"\n⚠️ **Validation Status:** {status}")
    
    # Add troubleshooting suggestions
    if result.troubleshooting_suggestions:
        response_parts.append(f"\n🛠️ **Troubleshooting Recommendations:**")
        for i, suggestion in enumerate(result.troubleshooting_suggestions[:3], 1):
            response_parts.append(f"\n{i}. **{suggestion['description']}**")
            response_parts.append(f"   *Suggested Action:* {suggestion['suggested_action']}")
            response_parts.append(f"   *Priority:* {suggestion['priority']}")
    
    # Add configuration recommendations
    if result.configuration_recommendations:
        response_parts.append(f"\n💡 **Configuration Recommendations:**")
        for i, rec in enumerate(result.configuration_recommendations[:3], 1):
            response_parts.append(f"\n{i}. **{rec['description']}**")
            if rec.get('suggested_fields'):
                response_parts.append(f"   *Missing fields:* {', '.join(rec['suggested_fields'])}")
    
    # Add error summary
    if result.error_summary.get("total_errors", 0) > 0:
        response_parts.append(f"\n⚠️ **Issues Found:** {result.error_summary['total_errors']} total issues")
        if result.error_summary.get("critical_errors"):
            response_parts.append(f"   🚨 Critical: {len(result.error_summary['critical_errors'])}")
        if result.error_summary.get("warning_errors"):
            response_parts.append(f"   ⚠️ Warnings: {len(result.error_summary['warning_errors'])}")
    
    return "\n".join(response_parts)

def create_response_attachments(result: ResearchResult):
    """Create response attachments from analysis results."""
    attachments = []
    
    # Add validation report attachment
    if result.validation_results:
        attachments.append({
            "name": "Validation Report",
            "icon": "📋",
            "description": f"Overall status: {result.validation_results.get('overall_status', 'unknown')}"
        })
    
    # Add troubleshooting recommendations attachment
    if result.troubleshooting_suggestions:
        attachments.append({
            "name": "Troubleshooting Guide",
            "icon": "🛠️",
            "description": f"{len(result.troubleshooting_suggestions)} recommendations"
        })
    
    # Add configuration recommendations attachment
    if result.configuration_recommendations:
        attachments.append({
            "name": "Configuration Recommendations",
            "icon": "💡",
            "description": f"{len(result.configuration_recommendations)} suggestions"
        })
    
    return attachments

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    # Create basic HTML template if it doesn't exist
    dashboard_template = templates_dir / "dashboard.html"
    if not dashboard_template.exists():
        dashboard_template.write_text("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-cogs"></i> Configuration Research Dashboard
            </a>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-12">
                <h1>Configuration Research Dashboard</h1>
                <p class="lead">Agentic AI system for configuration research and validation</p>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Research Tasks</h5>
                        <p class="card-text">Total: {{ stats.task_stats.total_tasks }}</p>
                        <p class="card-text">Completed: {{ stats.task_stats.completed_tasks }}</p>
                        <p class="card-text">Running: {{ stats.task_stats.running_tasks }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Knowledge Base</h5>
                        <p class="card-text">Entries: {{ stats.knowledge_base_stats.total_entries }}</p>
                        <p class="card-text">Categories: {{ stats.knowledge_base_stats.categories|length }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Validations</h5>
                        <p class="card-text">Total: {{ stats.validation_stats.total_validations }}</p>
                        <p class="card-text">Passed: {{ stats.validation_stats.passed_validations }}</p>
                        <p class="card-text">Failed: {{ stats.validation_stats.failed_validations }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">System Status</h5>
                        <p class="card-text text-success">
                            <i class="fas fa-check-circle"></i> Healthy
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5>Quick Actions</h5>
                    </div>
                    <div class="card-body">
                        <a href="/chat" class="btn btn-primary me-2">
                            <i class="fas fa-robot"></i> Chat with Agent
                        </a>
                        <a href="/api/docs" class="btn btn-outline me-2">
                            <i class="fas fa-book"></i> API Documentation
                        </a>
                        <button class="btn btn-success me-2" onclick="createResearchTask()">
                            <i class="fas fa-plus"></i> New Research Task
                        </button>
                        <button class="btn btn-warning me-2" onclick="createTroubleshootingCase()">
                            <i class="fas fa-bug"></i> New Troubleshooting Case
                        </button>
                        <button class="btn btn-info" onclick="validateConfiguration()">
                            <i class="fas fa-check"></i> Validate Configuration
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function createResearchTask() {
            alert('Research task creation form would open here');
        }
        
        function createTroubleshootingCase() {
            alert('Troubleshooting case creation form would open here');
        }
        
        function validateConfiguration() {
            alert('Configuration validation form would open here');
        }
    </script>
</body>
</html>
        """)
    
    # Run the application
    uvicorn.run(
        "app:app",
        host=settings.dashboard_host,
        port=settings.dashboard_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )