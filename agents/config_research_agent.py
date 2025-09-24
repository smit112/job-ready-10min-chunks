"""
Main configuration research agent with MCP integration.
Orchestrates Excel, PDF, and Link analysis for automated troubleshooting and validation.
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import json
from datetime import datetime
from dataclasses import dataclass, asdict
import uuid

# Import our utility modules
import sys
sys.path.append('/workspace')
from utils.excel_processor import ExcelProcessor, ExcelConfig
from utils.pdf_parser import PDFParser, PDFDocument
from utils.link_analyzer import LinkAnalyzer, LinkInfo
from configs.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class ResearchTask:
    """Represents a configuration research task."""
    task_id: str
    name: str
    description: str
    excel_files: List[str]
    pdf_files: List[str]
    links: List[str]
    validation_rules: Dict[str, Any]
    created_at: str
    status: str = "pending"
    results: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


@dataclass
class ResearchResult:
    """Comprehensive research result."""
    task_id: str
    excel_results: Dict[str, Any]
    pdf_results: Dict[str, Any]
    link_results: Dict[str, Any]
    validation_results: Dict[str, Any]
    troubleshooting_suggestions: List[Dict[str, Any]]
    configuration_recommendations: List[Dict[str, Any]]
    error_summary: Dict[str, Any]
    created_at: str
    processing_time: float


class ConfigResearchAgent:
    """Main agent for configuration research and validation."""
    
    def __init__(self):
        self.excel_processor = ExcelProcessor(
            settings.excel_templates_dir,
            settings.excel_output_dir
        )
        self.pdf_parser = PDFParser(
            settings.pdf_docs_dir,
            settings.pdf_errors_dir
        )
        self.link_analyzer = LinkAnalyzer(
            settings.link_cache_dir,
            settings.max_link_depth,
            settings.link_timeout
        )
        
        # Task storage
        self.tasks: Dict[str, ResearchTask] = {}
        self.results: Dict[str, ResearchResult] = {}
        
        # Knowledge base for troubleshooting
        self.troubleshooting_kb = {}
        self.configuration_patterns = {}
        
        logger.info("Configuration Research Agent initialized")
    
    def create_research_task(self,
                           name: str,
                           description: str,
                           excel_files: List[str] = None,
                           pdf_files: List[str] = None,
                           links: List[str] = None,
                           validation_rules: Dict[str, Any] = None) -> str:
        """
        Create a new configuration research task.
        
        Args:
            name: Task name
            description: Task description
            excel_files: List of Excel file paths
            pdf_files: List of PDF file paths
            links: List of URLs to analyze
            validation_rules: Validation rules to apply
            
        Returns:
            Task ID
        """
        task_id = str(uuid.uuid4())
        
        task = ResearchTask(
            task_id=task_id,
            name=name,
            description=description,
            excel_files=excel_files or [],
            pdf_files=pdf_files or [],
            links=links or [],
            validation_rules=validation_rules or {},
            created_at=datetime.now().isoformat()
        )
        
        self.tasks[task_id] = task
        logger.info(f"Created research task: {task_id}")
        
        return task_id
    
    async def execute_research_task(self, task_id: str) -> ResearchResult:
        """
        Execute a configuration research task.
        
        Args:
            task_id: ID of the task to execute
            
        Returns:
            ResearchResult object
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        task.status = "running"
        
        start_time = datetime.now()
        
        try:
            # Execute all research components in parallel
            excel_results, pdf_results, link_results = await asyncio.gather(
                self._process_excel_files(task.excel_files),
                self._process_pdf_files(task.pdf_files),
                self._process_links(task.links),
                return_exceptions=True
            )
            
            # Handle exceptions
            if isinstance(excel_results, Exception):
                excel_results = {"error": str(excel_results)}
            if isinstance(pdf_results, Exception):
                pdf_results = {"error": str(pdf_results)}
            if isinstance(link_results, Exception):
                link_results = {"error": str(link_results)}
            
            # Perform validation
            validation_results = await self._perform_validation(
                excel_results, pdf_results, link_results, task.validation_rules
            )
            
            # Generate troubleshooting suggestions
            troubleshooting_suggestions = await self._generate_troubleshooting_suggestions(
                excel_results, pdf_results, link_results, validation_results
            )
            
            # Generate configuration recommendations
            config_recommendations = await self._generate_configuration_recommendations(
                excel_results, pdf_results, link_results
            )
            
            # Create error summary
            error_summary = self._create_error_summary(
                excel_results, pdf_results, link_results, validation_results
            )
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Create result
            result = ResearchResult(
                task_id=task_id,
                excel_results=excel_results,
                pdf_results=pdf_results,
                link_results=link_results,
                validation_results=validation_results,
                troubleshooting_suggestions=troubleshooting_suggestions,
                configuration_recommendations=config_recommendations,
                error_summary=error_summary,
                created_at=datetime.now().isoformat(),
                processing_time=processing_time
            )
            
            self.results[task_id] = result
            task.status = "completed"
            task.results = asdict(result)
            
            logger.info(f"Completed research task: {task_id} in {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            task.status = "failed"
            task.error_message = str(e)
            logger.error(f"Failed research task {task_id}: {str(e)}")
            raise
    
    async def _process_excel_files(self, excel_files: List[str]) -> Dict[str, Any]:
        """Process Excel files for configuration data."""
        if not excel_files:
            return {"message": "No Excel files to process"}
        
        results = {
            "files_processed": 0,
            "configurations": {},
            "validation_rules": {},
            "errors": []
        }
        
        for file_path in excel_files:
            try:
                if not Path(file_path).exists():
                    results["errors"].append(f"File not found: {file_path}")
                    continue
                
                # Process Excel file
                configs = self.excel_processor.read_excel_file(file_path)
                
                for sheet_name, config in configs.items():
                    results["configurations"][f"{file_path}:{sheet_name}"] = {
                        "headers": config.headers,
                        "data": config.data,
                        "metadata": config.metadata
                    }
                    
                    if config.validation_rules:
                        results["validation_rules"][f"{file_path}:{sheet_name}"] = config.validation_rules
                
                results["files_processed"] += 1
                
            except Exception as e:
                results["errors"].append(f"Error processing {file_path}: {str(e)}")
        
        return results
    
    async def _process_pdf_files(self, pdf_files: List[str]) -> Dict[str, Any]:
        """Process PDF files for error documentation and troubleshooting."""
        if not pdf_files:
            return {"message": "No PDF files to process"}
        
        results = {
            "files_processed": 0,
            "documents": {},
            "error_patterns": [],
            "troubleshooting_steps": [],
            "configuration_snippets": [],
            "errors": []
        }
        
        for file_path in pdf_files:
            try:
                if not Path(file_path).exists():
                    results["errors"].append(f"File not found: {file_path}")
                    continue
                
                # Parse PDF file
                pdf_doc = self.pdf_parser.parse_pdf(file_path)
                
                # Store document info
                results["documents"][file_path] = {
                    "title": pdf_doc.title,
                    "page_count": len(pdf_doc.pages),
                    "content_length": len(pdf_doc.content),
                    "hash": pdf_doc.hash
                }
                
                # Collect error patterns
                results["error_patterns"].extend(pdf_doc.error_patterns)
                
                # Collect troubleshooting steps
                results["troubleshooting_steps"].extend(pdf_doc.troubleshooting_steps)
                
                # Collect configuration snippets
                results["configuration_snippets"].extend(pdf_doc.configuration_snippets)
                
                results["files_processed"] += 1
                
            except Exception as e:
                results["errors"].append(f"Error processing {file_path}: {str(e)}")
        
        return results
    
    async def _process_links(self, links: List[str]) -> Dict[str, Any]:
        """Process links for external resource validation."""
        if not links:
            return {"message": "No links to process"}
        
        results = {
            "links_processed": 0,
            "valid_links": 0,
            "link_info": [],
            "domain_statistics": {},
            "errors": []
        }
        
        try:
            # Analyze links
            link_infos = self.link_analyzer.analyze_links(links, extract_content=True)
            
            for link_info in link_infos:
                results["link_info"].append(asdict(link_info))
                if link_info.is_valid:
                    results["valid_links"] += 1
                results["links_processed"] += 1
            
            # Get domain statistics
            results["domain_statistics"] = self.link_analyzer.get_domain_statistics(link_infos)
            
        except Exception as e:
            results["errors"].append(f"Error processing links: {str(e)}")
        
        return results
    
    async def _perform_validation(self,
                                excel_results: Dict[str, Any],
                                pdf_results: Dict[str, Any],
                                link_results: Dict[str, Any],
                                validation_rules: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive validation across all data sources."""
        validation_results = {
            "excel_validation": {},
            "pdf_validation": {},
            "link_validation": {},
            "cross_reference_validation": {},
            "overall_status": "passed"
        }
        
        # Validate Excel configurations
        if "configurations" in excel_results:
            for config_key, config_data in excel_results["configurations"].items():
                if config_key in excel_results.get("validation_rules", {}):
                    rules = excel_results["validation_rules"][config_key]
                    errors = self.excel_processor.validate_configuration(config_data["data"], rules)
                    validation_results["excel_validation"][config_key] = {
                        "errors": errors,
                        "status": "passed" if not errors else "failed"
                    }
        
        # Validate PDF content
        if "error_patterns" in pdf_results:
            validation_results["pdf_validation"] = {
                "error_patterns_found": len(pdf_results["error_patterns"]),
                "troubleshooting_steps_found": len(pdf_results.get("troubleshooting_steps", [])),
                "configuration_snippets_found": len(pdf_results.get("configuration_snippets", []))
            }
        
        # Validate links
        if "link_info" in link_results:
            valid_count = link_results.get("valid_links", 0)
            total_count = link_results.get("links_processed", 0)
            validation_results["link_validation"] = {
                "validity_rate": valid_count / total_count if total_count > 0 else 0,
                "total_links": total_count,
                "valid_links": valid_count
            }
        
        # Cross-reference validation
        validation_results["cross_reference_validation"] = await self._cross_reference_validation(
            excel_results, pdf_results, link_results
        )
        
        # Determine overall status
        has_errors = any(
            validation_results["excel_validation"].get(key, {}).get("status") == "failed"
            for key in validation_results["excel_validation"]
        )
        
        if has_errors or validation_results["link_validation"].get("validity_rate", 1) < 0.8:
            validation_results["overall_status"] = "failed"
        
        return validation_results
    
    async def _cross_reference_validation(self,
                                        excel_results: Dict[str, Any],
                                        pdf_results: Dict[str, Any],
                                        link_results: Dict[str, Any]) -> Dict[str, Any]:
        """Perform cross-reference validation between different data sources."""
        cross_ref_results = {
            "configuration_consistency": [],
            "error_pattern_matches": [],
            "troubleshooting_coverage": []
        }
        
        # Check configuration consistency between Excel and PDF
        excel_configs = excel_results.get("configurations", {})
        pdf_snippets = pdf_results.get("configuration_snippets", [])
        
        for config_key, config_data in excel_configs.items():
            for snippet in pdf_snippets:
                # Simple consistency check (can be enhanced)
                if any(header.lower() in snippet["content"].lower() for header in config_data["headers"]):
                    cross_ref_results["configuration_consistency"].append({
                        "excel_config": config_key,
                        "pdf_snippet": snippet["content"][:100] + "...",
                        "match_type": "header_match"
                    })
        
        # Check error pattern matches
        excel_errors = []
        for config_key, config_data in excel_results.get("configurations", {}).items():
            for row in config_data.get("data", []):
                for value in row.values():
                    if isinstance(value, str) and any(keyword in value.lower() for keyword in ["error", "fail", "invalid"]):
                        excel_errors.append(value)
        
        pdf_errors = pdf_results.get("error_patterns", [])
        for excel_error in excel_errors:
            for pdf_error in pdf_errors:
                if any(word in pdf_error.get("pattern", "").lower() for word in excel_error.lower().split()):
                    cross_ref_results["error_pattern_matches"].append({
                        "excel_error": excel_error,
                        "pdf_error": pdf_error["pattern"],
                        "match_type": "keyword_match"
                    })
        
        return cross_ref_results
    
    async def _generate_troubleshooting_suggestions(self,
                                                  excel_results: Dict[str, Any],
                                                  pdf_results: Dict[str, Any],
                                                  link_results: Dict[str, Any],
                                                  validation_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate AI-powered troubleshooting suggestions."""
        suggestions = []
        
        # Analyze validation errors
        for config_key, validation in validation_results.get("excel_validation", {}).items():
            if validation.get("status") == "failed":
                for field, errors in validation.get("errors", {}).items():
                    for error in errors:
                        suggestions.append({
                            "type": "validation_error",
                            "priority": "high",
                            "description": f"Validation error in {config_key}: {error}",
                            "suggested_action": f"Review and fix the {field} field in {config_key}",
                            "source": "excel_validation"
                        })
        
        # Analyze PDF error patterns
        for error_pattern in pdf_results.get("error_patterns", []):
            if error_pattern.get("severity") in ["CRITICAL", "ERROR"]:
                suggestions.append({
                    "type": "error_pattern",
                    "priority": "high" if error_pattern.get("severity") == "CRITICAL" else "medium",
                    "description": f"Error pattern found: {error_pattern.get('pattern')}",
                    "suggested_action": error_pattern.get("solution", "Review error documentation"),
                    "source": "pdf_analysis"
                })
        
        # Analyze link validation issues
        link_validity = link_results.get("valid_links", 0) / max(link_results.get("links_processed", 1), 1)
        if link_validity < 0.8:
            suggestions.append({
                "type": "link_validation",
                "priority": "medium",
                "description": f"Low link validity rate: {link_validity:.1%}",
                "suggested_action": "Check and update broken links in documentation",
                "source": "link_analysis"
            })
        
        return suggestions
    
    async def _generate_configuration_recommendations(self,
                                                    excel_results: Dict[str, Any],
                                                    pdf_results: Dict[str, Any],
                                                    link_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate configuration recommendations based on analysis."""
        recommendations = []
        
        # Analyze Excel configurations
        for config_key, config_data in excel_results.get("configurations", {}).items():
            headers = config_data.get("headers", [])
            
            # Check for missing common configuration fields
            common_fields = ["host", "port", "username", "password", "database", "timeout"]
            missing_fields = [field for field in common_fields if not any(field in header.lower() for header in headers)]
            
            if missing_fields:
                recommendations.append({
                    "type": "missing_fields",
                    "priority": "medium",
                    "description": f"Missing common configuration fields in {config_key}",
                    "suggested_fields": missing_fields,
                    "source": "excel_analysis"
                })
        
        # Analyze PDF configuration snippets
        for snippet in pdf_results.get("configuration_snippets", []):
            if snippet.get("type") == "CONFIGURATION":
                recommendations.append({
                    "type": "configuration_snippet",
                    "priority": "low",
                    "description": f"Configuration snippet found in documentation",
                    "snippet_preview": snippet["content"][:200] + "...",
                    "source": "pdf_analysis"
                })
        
        # Analyze link content for configuration best practices
        for link_info in link_results.get("link_info", []):
            if link_info.get("is_valid") and "config" in link_info.get("title", "").lower():
                recommendations.append({
                    "type": "external_resource",
                    "priority": "low",
                    "description": f"Configuration resource found: {link_info.get('title')}",
                    "url": link_info.get("url"),
                    "source": "link_analysis"
                })
        
        return recommendations
    
    def _create_error_summary(self,
                            excel_results: Dict[str, Any],
                            pdf_results: Dict[str, Any],
                            link_results: Dict[str, Any],
                            validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of all errors found."""
        error_summary = {
            "total_errors": 0,
            "error_categories": {
                "excel_errors": 0,
                "pdf_errors": 0,
                "link_errors": 0,
                "validation_errors": 0
            },
            "critical_errors": [],
            "warning_errors": [],
            "info_errors": []
        }
        
        # Count Excel errors
        excel_errors = excel_results.get("errors", [])
        error_summary["error_categories"]["excel_errors"] = len(excel_errors)
        error_summary["total_errors"] += len(excel_errors)
        
        # Count PDF errors
        pdf_errors = pdf_results.get("errors", [])
        error_summary["error_categories"]["pdf_errors"] = len(pdf_errors)
        error_summary["total_errors"] += len(pdf_errors)
        
        # Count link errors
        link_errors = link_results.get("errors", [])
        error_summary["error_categories"]["link_errors"] = len(link_errors)
        error_summary["total_errors"] += len(link_errors)
        
        # Count validation errors
        validation_errors = 0
        for config_key, validation in validation_results.get("excel_validation", {}).items():
            if validation.get("status") == "failed":
                for field, errors in validation.get("errors", {}).items():
                    validation_errors += len(errors)
        
        error_summary["error_categories"]["validation_errors"] = validation_errors
        error_summary["total_errors"] += validation_errors
        
        # Categorize errors by severity
        for error in excel_errors + pdf_errors + link_errors:
            if "critical" in error.lower() or "fatal" in error.lower():
                error_summary["critical_errors"].append(error)
            elif "warning" in error.lower():
                error_summary["warning_errors"].append(error)
            else:
                error_summary["info_errors"].append(error)
        
        return error_summary
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get the status of a research task."""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        return {
            "task_id": task_id,
            "name": task.name,
            "status": task.status,
            "created_at": task.created_at,
            "error_message": task.error_message,
            "has_results": task.results is not None
        }
    
    def get_task_result(self, task_id: str) -> Optional[ResearchResult]:
        """Get the result of a completed research task."""
        return self.results.get(task_id)
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all research tasks."""
        return [
            {
                "task_id": task_id,
                "name": task.name,
                "status": task.status,
                "created_at": task.created_at
            }
            for task_id, task in self.tasks.items()
        ]
    
    def save_results(self, task_id: str, output_file: Optional[str] = None) -> Path:
        """Save research results to JSON file."""
        if task_id not in self.results:
            raise ValueError(f"No results found for task {task_id}")
        
        result = self.results[task_id]
        
        if output_file is None:
            output_file = Path(settings.data_dir) / f"research_result_{task_id}.json"
        else:
            output_file = Path(output_file)
        
        # Convert to dictionary for JSON serialization
        result_dict = asdict(result)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved research results to: {output_file}")
        return output_file