"""
PDF Analyzer for Error Document Processing and Troubleshooting
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from loguru import logger
import PyPDF2
from datetime import datetime


class PDFAnalyzer:
    """Analyze PDF error documents for troubleshooting automation"""
    
    def __init__(self):
        self.error_patterns = {
            'network': {
                'connection_timeout': r'(?i)(connection.*timeout|timeout.*connection|network.*timeout)',
                'connection_refused': r'(?i)(connection.*refused|refused.*connection|cannot.*connect)',
                'dns_error': r'(?i)(dns.*error|name.*resolution|host.*not.*found|nslookup.*failed)',
                'port_unreachable': r'(?i)(port.*unreachable|unreachable.*port|port.*closed)',
                'ssl_error': r'(?i)(ssl.*error|certificate.*error|handshake.*failed|tls.*error)'
            },
            'database': {
                'connection_failed': r'(?i)(database.*connection.*failed|failed.*connect.*database|db.*connection.*error)',
                'authentication_error': r'(?i)(authentication.*failed|login.*failed|invalid.*credentials|access.*denied)',
                'query_error': r'(?i)(sql.*error|query.*failed|syntax.*error|invalid.*query)',
                'timeout_error': r'(?i)(query.*timeout|command.*timeout|execution.*timeout)',
                'deadlock': r'(?i)(deadlock|lock.*timeout|blocking|resource.*unavailable)'
            },
            'system': {
                'memory_error': r'(?i)(out.*of.*memory|memory.*error|insufficient.*memory|oom)',
                'disk_error': r'(?i)(disk.*full|no.*space|disk.*error|storage.*full)',
                'permission_error': r'(?i)(permission.*denied|access.*denied|unauthorized|forbidden)',
                'service_error': r'(?i)(service.*failed|service.*stopped|daemon.*error|process.*crashed)',
                'configuration_error': r'(?i)(config.*error|configuration.*invalid|setting.*error|parameter.*invalid)'
            },
            'application': {
                'startup_error': r'(?i)(startup.*failed|initialization.*error|boot.*error|launch.*failed)',
                'runtime_error': r'(?i)(runtime.*error|execution.*error|application.*error|crash)',
                'dependency_error': r'(?i)(dependency.*missing|module.*not.*found|library.*error|import.*error)',
                'version_conflict': r'(?i)(version.*conflict|compatibility.*error|version.*mismatch)',
                'license_error': r'(?i)(license.*error|license.*expired|activation.*failed|invalid.*license)'
            }
        }
        
        self.solution_patterns = {
            'restart': r'(?i)(restart|reboot|reload|refresh)',
            'reinstall': r'(?i)(reinstall|uninstall.*install|remove.*install)',
            'update': r'(?i)(update|upgrade|patch|latest.*version)',
            'configure': r'(?i)(configure|reconfigure|setup|modify.*setting)',
            'check': r'(?i)(check|verify|validate|test|examine)',
            'replace': r'(?i)(replace|substitute|change|swap)',
            'repair': r'(?i)(repair|fix|correct|resolve)',
            'contact': r'(?i)(contact.*support|call.*support|technical.*support|help.*desk)'
        }
        
        self.severity_patterns = {
            'critical': r'(?i)(critical|fatal|severe|emergency|urgent)',
            'high': r'(?i)(high|major|important|significant)',
            'medium': r'(?i)(medium|moderate|warning|caution)',
            'low': r'(?i)(low|minor|info|information|notice)'
        }
    
    async def analyze_document(self, file_path: str, error_type: Optional[str] = None,
                              extract_solutions: bool = True) -> Dict[str, Any]:
        """Analyze PDF error document and extract troubleshooting information"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"PDF file not found: {file_path}")
            
            if file_path.suffix.lower() != '.pdf':
                raise ValueError(f"File is not a PDF: {file_path}")
            
            logger.info(f"Analyzing PDF document: {file_path}")
            
            # Extract text from PDF
            text_content = await self._extract_text_from_pdf(file_path)
            
            # Analyze document structure
            document_info = await self._analyze_document_structure(file_path, text_content)
            
            # Extract errors and issues
            errors_analysis = await self._extract_errors(text_content, error_type)
            
            # Extract solutions if requested
            solutions_analysis = {}
            if extract_solutions:
                solutions_analysis = await self._extract_solutions(text_content, errors_analysis)
            
            # Generate troubleshooting recommendations
            recommendations = await self._generate_recommendations(errors_analysis, solutions_analysis)
            
            result = {
                "document_info": document_info,
                "errors_analysis": errors_analysis,
                "solutions_analysis": solutions_analysis,
                "recommendations": recommendations,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing PDF document {file_path}: {str(e)}")
            raise
    
    async def _extract_text_from_pdf(self, file_path: Path) -> str:
        """Extract text content from PDF file"""
        try:
            text_content = ""
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_content += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                    except Exception as e:
                        logger.warning(f"Could not extract text from page {page_num + 1}: {str(e)}")
                        continue
            
            return text_content
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise
    
    async def _analyze_document_structure(self, file_path: Path, text_content: str) -> Dict[str, Any]:
        """Analyze PDF document structure and metadata"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                metadata = pdf_reader.metadata or {}
                
                document_info = {
                    "file_path": str(file_path),
                    "file_size": file_path.stat().st_size,
                    "total_pages": len(pdf_reader.pages),
                    "text_length": len(text_content),
                    "metadata": {
                        "title": metadata.get('/Title', 'Unknown'),
                        "author": metadata.get('/Author', 'Unknown'),
                        "subject": metadata.get('/Subject', 'Unknown'),
                        "creator": metadata.get('/Creator', 'Unknown'),
                        "creation_date": str(metadata.get('/CreationDate', 'Unknown')),
                        "modification_date": str(metadata.get('/ModDate', 'Unknown'))
                    }
                }
                
                # Analyze text structure
                lines = text_content.split('\n')
                document_info["text_analysis"] = {
                    "total_lines": len(lines),
                    "non_empty_lines": len([line for line in lines if line.strip()]),
                    "average_line_length": sum(len(line) for line in lines) / len(lines) if lines else 0
                }
                
                return document_info
                
        except Exception as e:
            logger.error(f"Error analyzing document structure: {str(e)}")
            return {"error": str(e)}
    
    async def _extract_errors(self, text_content: str, error_type: Optional[str] = None) -> Dict[str, Any]:
        """Extract errors and issues from the document text"""
        errors_analysis = {
            "detected_errors": {},
            "error_summary": {},
            "error_locations": [],
            "severity_analysis": {}
        }
        
        try:
            lines = text_content.split('\n')
            
            # Determine which error patterns to use
            if error_type and error_type in self.error_patterns:
                patterns_to_check = {error_type: self.error_patterns[error_type]}
            else:
                patterns_to_check = self.error_patterns
            
            # Search for error patterns
            for category, patterns in patterns_to_check.items():
                category_errors = {}
                
                for error_name, pattern in patterns.items():
                    matches = []
                    
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line):
                            matches.append({
                                "line_number": line_num,
                                "text": line.strip(),
                                "context": self._get_context_lines(lines, line_num - 1, 2)
                            })
                    
                    if matches:
                        category_errors[error_name] = {
                            "count": len(matches),
                            "matches": matches
                        }
                
                if category_errors:
                    errors_analysis["detected_errors"][category] = category_errors
            
            # Generate error summary
            total_errors = 0
            error_types = []
            for category, errors in errors_analysis["detected_errors"].items():
                for error_type, error_data in errors.items():
                    total_errors += error_data["count"]
                    error_types.append(f"{category}.{error_type}")
            
            errors_analysis["error_summary"] = {
                "total_errors_found": total_errors,
                "error_categories": len(errors_analysis["detected_errors"]),
                "error_types": error_types,
                "most_common_category": self._get_most_common_category(errors_analysis["detected_errors"])
            }
            
            # Analyze severity
            severity_analysis = await self._analyze_error_severity(text_content, errors_analysis["detected_errors"])
            errors_analysis["severity_analysis"] = severity_analysis
            
            return errors_analysis
            
        except Exception as e:
            logger.error(f"Error extracting errors: {str(e)}")
            return errors_analysis
    
    def _get_context_lines(self, lines: List[str], line_index: int, context_size: int) -> List[str]:
        """Get context lines around a specific line"""
        start = max(0, line_index - context_size)
        end = min(len(lines), line_index + context_size + 1)
        return lines[start:end]
    
    def _get_most_common_category(self, detected_errors: Dict[str, Any]) -> Optional[str]:
        """Get the category with the most errors"""
        if not detected_errors:
            return None
        
        category_counts = {}
        for category, errors in detected_errors.items():
            total_count = sum(error_data["count"] for error_data in errors.values())
            category_counts[category] = total_count
        
        return max(category_counts, key=category_counts.get) if category_counts else None
    
    async def _analyze_error_severity(self, text_content: str, detected_errors: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the severity of detected errors"""
        severity_analysis = {
            "severity_distribution": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "severity_details": []
        }
        
        try:
            lines = text_content.split('\n')
            
            # Check each line for severity indicators
            for line_num, line in enumerate(lines, 1):
                for severity, pattern in self.severity_patterns.items():
                    if re.search(pattern, line):
                        severity_analysis["severity_distribution"][severity] += 1
                        severity_analysis["severity_details"].append({
                            "line_number": line_num,
                            "severity": severity,
                            "text": line.strip()
                        })
            
            # If no explicit severity found, infer from error types
            if sum(severity_analysis["severity_distribution"].values()) == 0:
                severity_analysis = self._infer_severity_from_errors(detected_errors)
            
            return severity_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing severity: {str(e)}")
            return severity_analysis
    
    def _infer_severity_from_errors(self, detected_errors: Dict[str, Any]) -> Dict[str, Any]:
        """Infer severity from error types when not explicitly stated"""
        severity_mapping = {
            'network': {'connection_timeout': 'medium', 'connection_refused': 'high', 'dns_error': 'medium', 'ssl_error': 'high'},
            'database': {'connection_failed': 'high', 'authentication_error': 'high', 'deadlock': 'critical'},
            'system': {'memory_error': 'critical', 'disk_error': 'high', 'permission_error': 'medium', 'service_error': 'high'},
            'application': {'startup_error': 'high', 'runtime_error': 'medium', 'dependency_error': 'high'}
        }
        
        severity_distribution = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        severity_details = []
        
        for category, errors in detected_errors.items():
            for error_type, error_data in errors.items():
                severity = severity_mapping.get(category, {}).get(error_type, 'medium')
                count = error_data["count"]
                severity_distribution[severity] += count
                
                for match in error_data["matches"]:
                    severity_details.append({
                        "line_number": match["line_number"],
                        "severity": severity,
                        "error_type": f"{category}.{error_type}",
                        "text": match["text"]
                    })
        
        return {
            "severity_distribution": severity_distribution,
            "severity_details": severity_details
        }
    
    async def _extract_solutions(self, text_content: str, errors_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract solution recommendations from the document"""
        solutions_analysis = {
            "detected_solutions": {},
            "solution_summary": {},
            "solution_locations": []
        }
        
        try:
            lines = text_content.split('\n')
            
            # Search for solution patterns
            for solution_type, pattern in self.solution_patterns.items():
                matches = []
                
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern, line):
                        matches.append({
                            "line_number": line_num,
                            "text": line.strip(),
                            "context": self._get_context_lines(lines, line_num - 1, 3)
                        })
                
                if matches:
                    solutions_analysis["detected_solutions"][solution_type] = {
                        "count": len(matches),
                        "matches": matches
                    }
            
            # Generate solution summary
            total_solutions = sum(data["count"] for data in solutions_analysis["detected_solutions"].values())
            solution_types = list(solutions_analysis["detected_solutions"].keys())
            
            solutions_analysis["solution_summary"] = {
                "total_solutions_found": total_solutions,
                "solution_types": solution_types,
                "most_common_solution": max(solution_types, 
                    key=lambda x: solutions_analysis["detected_solutions"][x]["count"]) if solution_types else None
            }
            
            return solutions_analysis
            
        except Exception as e:
            logger.error(f"Error extracting solutions: {str(e)}")
            return solutions_analysis
    
    async def _generate_recommendations(self, errors_analysis: Dict[str, Any], 
                                      solutions_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate troubleshooting recommendations based on analysis"""
        recommendations = {
            "immediate_actions": [],
            "investigation_steps": [],
            "preventive_measures": [],
            "escalation_criteria": []
        }
        
        try:
            detected_errors = errors_analysis.get("detected_errors", {})
            severity_analysis = errors_analysis.get("severity_analysis", {})
            
            # Generate immediate actions based on severity
            critical_count = severity_analysis.get("severity_distribution", {}).get("critical", 0)
            high_count = severity_analysis.get("severity_distribution", {}).get("high", 0)
            
            if critical_count > 0:
                recommendations["immediate_actions"].append("CRITICAL: Immediate attention required - system may be unstable")
                recommendations["escalation_criteria"].append("Escalate to senior technical staff immediately")
            
            if high_count > 0:
                recommendations["immediate_actions"].append("High priority issues detected - address within 1 hour")
            
            # Generate specific recommendations based on error categories
            for category, errors in detected_errors.items():
                category_recommendations = self._get_category_recommendations(category, errors)
                recommendations["investigation_steps"].extend(category_recommendations)
            
            # Add solution-based recommendations
            if solutions_analysis.get("detected_solutions"):
                most_common = solutions_analysis.get("solution_summary", {}).get("most_common_solution")
                if most_common:
                    recommendations["immediate_actions"].append(
                        f"Consider {most_common} as primary solution approach"
                    )
            
            # Add preventive measures
            recommendations["preventive_measures"] = [
                "Implement comprehensive monitoring and alerting",
                "Regular system health checks and maintenance",
                "Document all configuration changes",
                "Maintain up-to-date system documentation",
                "Regular backup and recovery testing"
            ]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return recommendations
    
    def _get_category_recommendations(self, category: str, errors: Dict[str, Any]) -> List[str]:
        """Get specific recommendations for error categories"""
        recommendations_map = {
            'network': [
                "Check network connectivity and firewall settings",
                "Verify DNS configuration and resolution",
                "Test port accessibility and service availability",
                "Review network logs for additional details"
            ],
            'database': [
                "Verify database service status and connectivity",
                "Check authentication credentials and permissions",
                "Review database logs for detailed error information",
                "Monitor database performance and resource usage"
            ],
            'system': [
                "Check system resource utilization (CPU, memory, disk)",
                "Verify file system permissions and access rights",
                "Review system logs and event viewer",
                "Ensure adequate storage space and system resources"
            ],
            'application': [
                "Verify application dependencies and requirements",
                "Check application configuration and settings",
                "Review application logs for detailed error traces",
                "Ensure proper application permissions and access"
            ]
        }
        
        return recommendations_map.get(category, ["Review error details and consult documentation"])