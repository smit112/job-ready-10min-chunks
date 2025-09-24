"""
Configuration Agent for Automated Troubleshooting and Analysis
"""

import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from loguru import logger
from datetime import datetime
import re
import yaml


class ConfigurationAgent:
    """AI-powered configuration agent for automated troubleshooting"""
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        self.troubleshooting_patterns = self._initialize_troubleshooting_patterns()
        self.solution_templates = self._initialize_solution_templates()
        
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize the troubleshooting knowledge base"""
        return {
            "network": {
                "common_issues": {
                    "connection_timeout": {
                        "symptoms": ["timeout", "connection timed out", "no response"],
                        "causes": ["firewall blocking", "service down", "network congestion", "incorrect port"],
                        "solutions": ["check firewall rules", "verify service status", "test connectivity", "validate port configuration"]
                    },
                    "dns_resolution": {
                        "symptoms": ["host not found", "name resolution failed", "dns error"],
                        "causes": ["incorrect dns server", "dns cache issues", "network configuration"],
                        "solutions": ["flush dns cache", "check dns servers", "verify network settings"]
                    },
                    "port_issues": {
                        "symptoms": ["connection refused", "port unreachable", "service unavailable"],
                        "causes": ["service not running", "firewall blocking port", "incorrect port number"],
                        "solutions": ["start service", "open firewall port", "verify port configuration"]
                    }
                },
                "diagnostic_commands": {
                    "connectivity": ["ping", "traceroute", "telnet", "nslookup"],
                    "service_status": ["systemctl status", "service status", "netstat -an"],
                    "firewall": ["iptables -L", "ufw status", "firewall-cmd --list-all"]
                }
            },
            "database": {
                "common_issues": {
                    "connection_failed": {
                        "symptoms": ["connection failed", "cannot connect", "database unavailable"],
                        "causes": ["service down", "incorrect credentials", "network issues", "max connections reached"],
                        "solutions": ["restart database service", "verify credentials", "check connection limits"]
                    },
                    "authentication": {
                        "symptoms": ["authentication failed", "access denied", "login failed"],
                        "causes": ["wrong username/password", "user permissions", "account locked"],
                        "solutions": ["reset password", "check user permissions", "unlock account"]
                    },
                    "performance": {
                        "symptoms": ["slow queries", "timeout", "high cpu usage"],
                        "causes": ["missing indexes", "large result sets", "resource constraints"],
                        "solutions": ["optimize queries", "add indexes", "increase resources"]
                    }
                },
                "diagnostic_commands": {
                    "connection": ["mysql -u user -p", "psql -U user -d database", "sqlcmd -S server"],
                    "status": ["SHOW STATUS", "SELECT version()", "SHOW PROCESSLIST"],
                    "performance": ["EXPLAIN query", "SHOW SLOW LOG", "SELECT * FROM pg_stat_activity"]
                }
            },
            "system": {
                "common_issues": {
                    "resource_exhaustion": {
                        "symptoms": ["out of memory", "disk full", "high cpu usage"],
                        "causes": ["memory leaks", "insufficient resources", "runaway processes"],
                        "solutions": ["increase resources", "optimize applications", "kill problematic processes"]
                    },
                    "permission_errors": {
                        "symptoms": ["permission denied", "access forbidden", "unauthorized"],
                        "causes": ["incorrect file permissions", "wrong user context", "selinux policies"],
                        "solutions": ["fix file permissions", "run as correct user", "adjust selinux"]
                    },
                    "service_failures": {
                        "symptoms": ["service failed", "process crashed", "startup error"],
                        "causes": ["configuration errors", "dependency issues", "resource problems"],
                        "solutions": ["check configuration", "verify dependencies", "review logs"]
                    }
                },
                "diagnostic_commands": {
                    "resources": ["top", "htop", "free -h", "df -h"],
                    "processes": ["ps aux", "systemctl status", "journalctl -u service"],
                    "permissions": ["ls -la", "getfacl", "sestatus"]
                }
            }
        }
    
    def _initialize_troubleshooting_patterns(self) -> Dict[str, Any]:
        """Initialize patterns for automated troubleshooting"""
        return {
            "error_patterns": {
                "connection_issues": [
                    r"connection\s+(refused|timeout|failed|reset)",
                    r"unable\s+to\s+connect",
                    r"network\s+(unreachable|timeout)",
                    r"host\s+(not\s+found|unreachable)"
                ],
                "authentication_issues": [
                    r"authentication\s+(failed|error)",
                    r"(access|permission)\s+denied",
                    r"(login|logon)\s+failed",
                    r"invalid\s+(credentials|username|password)"
                ],
                "resource_issues": [
                    r"out\s+of\s+(memory|disk|space)",
                    r"insufficient\s+(memory|disk|resources)",
                    r"resource\s+(exhausted|unavailable)",
                    r"(memory|disk)\s+(full|error)"
                ],
                "configuration_issues": [
                    r"configuration\s+(error|invalid)",
                    r"config\s+(not\s+found|missing)",
                    r"invalid\s+(parameter|setting|option)",
                    r"syntax\s+error\s+in\s+config"
                ]
            },
            "severity_indicators": {
                "critical": [r"critical", r"fatal", r"emergency", r"system\s+down"],
                "high": [r"error", r"failed", r"exception", r"unavailable"],
                "medium": [r"warning", r"timeout", r"slow", r"degraded"],
                "low": [r"info", r"notice", r"debug", r"trace"]
            }
        }
    
    def _initialize_solution_templates(self) -> Dict[str, Any]:
        """Initialize solution templates for common issues"""
        return {
            "network": {
                "connection_timeout": {
                    "immediate": [
                        "Verify network connectivity: ping {target}",
                        "Check if service is running on target host",
                        "Test port accessibility: telnet {host} {port}"
                    ],
                    "investigation": [
                        "Review firewall rules on both client and server",
                        "Check network routing and DNS resolution",
                        "Analyze network traffic with packet capture"
                    ],
                    "resolution": [
                        "Configure firewall to allow traffic on required ports",
                        "Restart network services if necessary",
                        "Update network configuration files"
                    ]
                }
            },
            "database": {
                "connection_failed": {
                    "immediate": [
                        "Check database service status",
                        "Verify connection string and credentials",
                        "Test database connectivity from application server"
                    ],
                    "investigation": [
                        "Review database error logs",
                        "Check available connections and limits",
                        "Verify network connectivity between application and database"
                    ],
                    "resolution": [
                        "Restart database service if needed",
                        "Increase connection pool limits",
                        "Update connection configuration"
                    ]
                }
            },
            "system": {
                "resource_exhaustion": {
                    "immediate": [
                        "Check current resource usage: top, free, df",
                        "Identify resource-intensive processes",
                        "Free up resources by stopping non-essential services"
                    ],
                    "investigation": [
                        "Analyze resource usage trends over time",
                        "Review application logs for memory leaks",
                        "Check for runaway processes or scheduled jobs"
                    ],
                    "resolution": [
                        "Increase system resources (RAM, disk space)",
                        "Optimize applications to use resources efficiently",
                        "Implement resource monitoring and alerting"
                    ]
                }
            }
        }
    
    async def troubleshoot(self, issue_description: str, 
                          config_files: Optional[List[str]] = None,
                          error_logs: Optional[List[str]] = None,
                          system_type: str = "general") -> Dict[str, Any]:
        """Perform automated troubleshooting analysis"""
        try:
            logger.info(f"Starting troubleshooting analysis for: {issue_description[:100]}...")
            
            # Analyze the issue description
            issue_analysis = await self._analyze_issue_description(issue_description)
            
            # Process configuration files if provided
            config_analysis = {}
            if config_files:
                config_analysis = await self._analyze_configuration_files(config_files)
            
            # Process error logs if provided
            log_analysis = {}
            if error_logs:
                log_analysis = await self._analyze_error_logs(error_logs)
            
            # Generate troubleshooting plan
            troubleshooting_plan = await self._generate_troubleshooting_plan(
                issue_analysis, config_analysis, log_analysis, system_type
            )
            
            # Create comprehensive result
            result = {
                "analysis_timestamp": datetime.now().isoformat(),
                "issue_analysis": issue_analysis,
                "configuration_analysis": config_analysis,
                "log_analysis": log_analysis,
                "troubleshooting_plan": troubleshooting_plan,
                "system_type": system_type,
                "confidence_score": self._calculate_confidence_score(issue_analysis, config_analysis, log_analysis)
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in troubleshooting analysis: {str(e)}")
            raise
    
    async def _analyze_issue_description(self, description: str) -> Dict[str, Any]:
        """Analyze the issue description to identify patterns and categories"""
        analysis = {
            "detected_patterns": [],
            "issue_category": "unknown",
            "severity": "medium",
            "keywords": [],
            "potential_causes": [],
            "related_systems": []
        }
        
        try:
            description_lower = description.lower()
            
            # Detect error patterns
            for category, patterns in self.troubleshooting_patterns["error_patterns"].items():
                for pattern in patterns:
                    if re.search(pattern, description_lower, re.IGNORECASE):
                        analysis["detected_patterns"].append({
                            "category": category,
                            "pattern": pattern,
                            "matched_text": re.search(pattern, description_lower, re.IGNORECASE).group()
                        })
            
            # Determine primary issue category
            if analysis["detected_patterns"]:
                category_counts = {}
                for pattern in analysis["detected_patterns"]:
                    category = pattern["category"]
                    category_counts[category] = category_counts.get(category, 0) + 1
                analysis["issue_category"] = max(category_counts, key=category_counts.get)
            
            # Determine severity
            for severity, indicators in self.troubleshooting_patterns["severity_indicators"].items():
                for indicator in indicators:
                    if re.search(indicator, description_lower, re.IGNORECASE):
                        analysis["severity"] = severity
                        break
                if analysis["severity"] != "medium":
                    break
            
            # Extract keywords
            analysis["keywords"] = self._extract_keywords(description)
            
            # Identify potential causes based on knowledge base
            analysis["potential_causes"] = self._identify_potential_causes(
                analysis["issue_category"], analysis["keywords"]
            )
            
            # Identify related systems
            analysis["related_systems"] = self._identify_related_systems(description)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing issue description: {str(e)}")
            return analysis
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text"""
        # Technical keywords that might be relevant
        technical_keywords = [
            'database', 'connection', 'server', 'network', 'service', 'port', 'timeout',
            'authentication', 'permission', 'memory', 'disk', 'cpu', 'ssl', 'certificate',
            'firewall', 'dns', 'proxy', 'load balancer', 'cache', 'session', 'cookie',
            'api', 'http', 'https', 'tcp', 'udp', 'ssh', 'ftp', 'smtp', 'ldap',
            'config', 'configuration', 'setting', 'parameter', 'variable', 'environment'
        ]
        
        found_keywords = []
        text_lower = text.lower()
        
        for keyword in technical_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def _identify_potential_causes(self, issue_category: str, keywords: List[str]) -> List[str]:
        """Identify potential causes based on issue category and keywords"""
        potential_causes = []
        
        # Map issue categories to system types
        category_to_system = {
            "connection_issues": "network",
            "authentication_issues": "database",  # Could also be system
            "resource_issues": "system",
            "configuration_issues": "system"
        }
        
        system_type = category_to_system.get(issue_category)
        if system_type and system_type in self.knowledge_base:
            # Get causes from knowledge base
            for issue_type, issue_info in self.knowledge_base[system_type]["common_issues"].items():
                # Check if any keywords match the symptoms
                symptoms = issue_info.get("symptoms", [])
                if any(keyword in " ".join(symptoms) for keyword in keywords):
                    potential_causes.extend(issue_info.get("causes", []))
        
        return list(set(potential_causes))  # Remove duplicates
    
    def _identify_related_systems(self, description: str) -> List[str]:
        """Identify systems mentioned in the description"""
        system_indicators = {
            "database": ["mysql", "postgresql", "oracle", "sql server", "mongodb", "database", "db"],
            "web_server": ["apache", "nginx", "iis", "tomcat", "web server", "http"],
            "application": ["java", "python", "nodejs", ".net", "php", "application", "app"],
            "network": ["router", "switch", "firewall", "load balancer", "proxy", "network"],
            "storage": ["san", "nas", "disk", "storage", "filesystem", "mount"],
            "security": ["ssl", "tls", "certificate", "ldap", "active directory", "authentication"]
        }
        
        related_systems = []
        description_lower = description.lower()
        
        for system, indicators in system_indicators.items():
            if any(indicator in description_lower for indicator in indicators):
                related_systems.append(system)
        
        return related_systems
    
    async def _analyze_configuration_files(self, config_files: List[str]) -> Dict[str, Any]:
        """Analyze configuration files for potential issues"""
        analysis = {
            "files_analyzed": [],
            "configuration_issues": [],
            "security_concerns": [],
            "recommendations": []
        }
        
        try:
            for config_file in config_files:
                file_path = Path(config_file)
                if not file_path.exists():
                    analysis["configuration_issues"].append({
                        "file": config_file,
                        "issue": "File not found",
                        "severity": "high"
                    })
                    continue
                
                try:
                    file_analysis = await self._analyze_single_config_file(file_path)
                    analysis["files_analyzed"].append(file_analysis)
                    
                    # Aggregate issues
                    if file_analysis.get("issues"):
                        analysis["configuration_issues"].extend(file_analysis["issues"])
                    
                    if file_analysis.get("security_concerns"):
                        analysis["security_concerns"].extend(file_analysis["security_concerns"])
                    
                except Exception as e:
                    analysis["configuration_issues"].append({
                        "file": config_file,
                        "issue": f"Error analyzing file: {str(e)}",
                        "severity": "medium"
                    })
            
            # Generate recommendations
            analysis["recommendations"] = self._generate_config_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing configuration files: {str(e)}")
            return analysis
    
    async def _analyze_single_config_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single configuration file"""
        analysis = {
            "file_path": str(file_path),
            "file_type": self._detect_config_type(file_path),
            "issues": [],
            "security_concerns": [],
            "settings": {}
        }
        
        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8')
            
            # Parse based on file type
            if analysis["file_type"] == "json":
                analysis["settings"] = json.loads(content)
            elif analysis["file_type"] == "yaml":
                analysis["settings"] = yaml.safe_load(content)
            elif analysis["file_type"] == "ini":
                # Simple INI parsing
                analysis["settings"] = self._parse_ini_content(content)
            else:
                # Generic text analysis
                analysis["settings"] = {"raw_content": content[:1000]}  # First 1000 chars
            
            # Check for common issues
            issues = self._check_config_issues(content, analysis["file_type"])
            analysis["issues"] = issues
            
            # Check for security concerns
            security_concerns = self._check_security_concerns(content, analysis["settings"])
            analysis["security_concerns"] = security_concerns
            
            return analysis
            
        except Exception as e:
            analysis["issues"].append({
                "type": "parsing_error",
                "message": f"Error parsing configuration file: {str(e)}",
                "severity": "high"
            })
            return analysis
    
    def _detect_config_type(self, file_path: Path) -> str:
        """Detect configuration file type"""
        suffix = file_path.suffix.lower()
        name = file_path.name.lower()
        
        if suffix in ['.json']:
            return 'json'
        elif suffix in ['.yaml', '.yml']:
            return 'yaml'
        elif suffix in ['.ini', '.conf', '.cfg']:
            return 'ini'
        elif suffix in ['.xml']:
            return 'xml'
        elif suffix in ['.properties']:
            return 'properties'
        elif 'config' in name or 'conf' in name:
            return 'config'
        else:
            return 'unknown'
    
    def _parse_ini_content(self, content: str) -> Dict[str, Any]:
        """Simple INI file parsing"""
        settings = {}
        current_section = "default"
        
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith(';'):
                continue
            
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                if current_section not in settings:
                    settings[current_section] = {}
            elif '=' in line:
                key, value = line.split('=', 1)
                if current_section not in settings:
                    settings[current_section] = {}
                settings[current_section][key.strip()] = value.strip()
        
        return settings
    
    def _check_config_issues(self, content: str, file_type: str) -> List[Dict[str, Any]]:
        """Check for common configuration issues"""
        issues = []
        
        # Check for hardcoded sensitive values
        sensitive_patterns = [
            (r'password\s*=\s*["\']?[^"\'\s]+', 'hardcoded_password'),
            (r'api[_-]?key\s*=\s*["\']?[^"\'\s]+', 'hardcoded_api_key'),
            (r'secret\s*=\s*["\']?[^"\'\s]+', 'hardcoded_secret'),
            (r'token\s*=\s*["\']?[^"\'\s]+', 'hardcoded_token')
        ]
        
        for pattern, issue_type in sensitive_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                issues.append({
                    "type": issue_type,
                    "message": f"Found {len(matches)} instances of hardcoded sensitive values",
                    "severity": "high",
                    "matches": len(matches)
                })
        
        # Check for common misconfigurations
        if 'debug' in content.lower() and 'true' in content.lower():
            issues.append({
                "type": "debug_enabled",
                "message": "Debug mode appears to be enabled",
                "severity": "medium"
            })
        
        return issues
    
    def _check_security_concerns(self, content: str, settings: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for security concerns in configuration"""
        concerns = []
        
        # Check for weak SSL/TLS settings
        if 'ssl' in content.lower() and ('false' in content.lower() or 'disabled' in content.lower()):
            concerns.append({
                "type": "ssl_disabled",
                "message": "SSL/TLS appears to be disabled",
                "severity": "high"
            })
        
        # Check for default ports
        default_ports = ['3306', '5432', '1433', '27017', '6379']  # MySQL, PostgreSQL, SQL Server, MongoDB, Redis
        for port in default_ports:
            if port in content:
                concerns.append({
                    "type": "default_port",
                    "message": f"Using default port {port} - consider changing for security",
                    "severity": "low"
                })
        
        return concerns
    
    def _generate_config_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on configuration analysis"""
        recommendations = []
        
        if analysis["configuration_issues"]:
            recommendations.append("Review and fix identified configuration issues")
        
        if analysis["security_concerns"]:
            recommendations.append("Address security concerns in configuration files")
            recommendations.append("Use environment variables for sensitive values")
            recommendations.append("Enable SSL/TLS where possible")
        
        recommendations.extend([
            "Implement configuration validation in deployment pipeline",
            "Use configuration management tools for consistency",
            "Regular security audits of configuration files"
        ])
        
        return recommendations
    
    async def _analyze_error_logs(self, error_logs: List[str]) -> Dict[str, Any]:
        """Analyze error logs for patterns and insights"""
        analysis = {
            "log_entries_analyzed": 0,
            "error_patterns": {},
            "timeline_analysis": {},
            "severity_distribution": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "recommendations": []
        }
        
        try:
            all_entries = []
            
            # Process each log entry
            for log_entry in error_logs:
                entries = log_entry.split('\n')
                all_entries.extend(entries)
            
            analysis["log_entries_analyzed"] = len(all_entries)
            
            # Analyze patterns
            for entry in all_entries:
                if not entry.strip():
                    continue
                
                # Check for error patterns
                for category, patterns in self.troubleshooting_patterns["error_patterns"].items():
                    for pattern in patterns:
                        if re.search(pattern, entry, re.IGNORECASE):
                            if category not in analysis["error_patterns"]:
                                analysis["error_patterns"][category] = []
                            analysis["error_patterns"][category].append(entry.strip())
                
                # Check severity
                for severity, indicators in self.troubleshooting_patterns["severity_indicators"].items():
                    for indicator in indicators:
                        if re.search(indicator, entry, re.IGNORECASE):
                            analysis["severity_distribution"][severity] += 1
                            break
            
            # Generate recommendations
            analysis["recommendations"] = self._generate_log_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing error logs: {str(e)}")
            return analysis
    
    def _generate_log_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on log analysis"""
        recommendations = []
        
        if analysis["error_patterns"]:
            recommendations.append("Focus on resolving the most frequent error patterns")
            
            # Specific recommendations based on patterns
            if "connection_issues" in analysis["error_patterns"]:
                recommendations.append("Investigate network connectivity and service availability")
            
            if "authentication_issues" in analysis["error_patterns"]:
                recommendations.append("Review authentication configuration and credentials")
            
            if "resource_issues" in analysis["error_patterns"]:
                recommendations.append("Monitor and optimize resource usage")
        
        # Severity-based recommendations
        critical_count = analysis["severity_distribution"]["critical"]
        high_count = analysis["severity_distribution"]["high"]
        
        if critical_count > 0:
            recommendations.append(f"URGENT: Address {critical_count} critical errors immediately")
        
        if high_count > 0:
            recommendations.append(f"High priority: Resolve {high_count} high-severity errors")
        
        return recommendations
    
    async def _generate_troubleshooting_plan(self, issue_analysis: Dict[str, Any],
                                           config_analysis: Dict[str, Any],
                                           log_analysis: Dict[str, Any],
                                           system_type: str) -> Dict[str, Any]:
        """Generate a comprehensive troubleshooting plan"""
        plan = {
            "immediate_actions": [],
            "investigation_steps": [],
            "resolution_steps": [],
            "prevention_measures": [],
            "estimated_complexity": "medium",
            "estimated_time": "30-60 minutes"
        }
        
        try:
            issue_category = issue_analysis.get("issue_category", "unknown")
            severity = issue_analysis.get("severity", "medium")
            
            # Get solution template if available
            system_templates = self.solution_templates.get(system_type, {})
            issue_template = system_templates.get(issue_category, {})
            
            # Add template-based actions
            if issue_template:
                plan["immediate_actions"].extend(issue_template.get("immediate", []))
                plan["investigation_steps"].extend(issue_template.get("investigation", []))
                plan["resolution_steps"].extend(issue_template.get("resolution", []))
            
            # Add severity-based urgency
            if severity == "critical":
                plan["immediate_actions"].insert(0, "CRITICAL: Escalate to senior technical staff immediately")
                plan["estimated_complexity"] = "high"
                plan["estimated_time"] = "1-4 hours"
            elif severity == "high":
                plan["immediate_actions"].insert(0, "High priority: Address within 1 hour")
                plan["estimated_time"] = "1-2 hours"
            
            # Add configuration-specific steps
            if config_analysis.get("configuration_issues"):
                plan["investigation_steps"].append("Review configuration file issues identified")
                plan["resolution_steps"].append("Fix configuration file problems")
            
            # Add log-specific steps
            if log_analysis.get("error_patterns"):
                plan["investigation_steps"].append("Analyze error log patterns for root cause")
                plan["resolution_steps"].append("Address issues identified in error logs")
            
            # Add prevention measures
            plan["prevention_measures"] = [
                "Implement comprehensive monitoring and alerting",
                "Regular system health checks and maintenance",
                "Document configuration changes and procedures",
                "Establish backup and recovery procedures",
                "Conduct regular security and performance audits"
            ]
            
            # Add diagnostic commands based on system type
            if system_type in self.knowledge_base:
                diagnostic_commands = self.knowledge_base[system_type].get("diagnostic_commands", {})
                if diagnostic_commands:
                    plan["diagnostic_commands"] = diagnostic_commands
            
            return plan
            
        except Exception as e:
            logger.error(f"Error generating troubleshooting plan: {str(e)}")
            return plan
    
    def _calculate_confidence_score(self, issue_analysis: Dict[str, Any],
                                  config_analysis: Dict[str, Any],
                                  log_analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for the troubleshooting analysis"""
        try:
            score = 0.5  # Base confidence
            
            # Increase confidence based on detected patterns
            if issue_analysis.get("detected_patterns"):
                score += 0.2
            
            # Increase confidence if we have configuration data
            if config_analysis.get("files_analyzed"):
                score += 0.15
            
            # Increase confidence if we have log data
            if log_analysis.get("error_patterns"):
                score += 0.15
            
            # Ensure score is between 0 and 1
            return min(1.0, max(0.0, score))
            
        except Exception:
            return 0.5  # Default confidence