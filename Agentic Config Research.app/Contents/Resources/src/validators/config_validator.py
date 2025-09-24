"""
Configuration Validator for Automated Configuration Validation
"""

import json
import yaml
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from loguru import logger
import re
import configparser
from datetime import datetime
import jsonschema
from jsonschema import validate, ValidationError


class ConfigValidator:
    """Validate configuration files against best practices and standards"""
    
    def __init__(self):
        self.validation_rules = self._initialize_validation_rules()
        self.security_rules = self._initialize_security_rules()
        self.performance_rules = self._initialize_performance_rules()
        self.supported_formats = {
            'json': self._validate_json,
            'yaml': self._validate_yaml,
            'yml': self._validate_yaml,
            'xml': self._validate_xml,
            'ini': self._validate_ini,
            'conf': self._validate_ini,
            'cfg': self._validate_ini,
            'properties': self._validate_properties
        }
    
    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialize general validation rules"""
        return {
            "required_fields": {
                "database": ["host", "port", "database", "username"],
                "network": ["host", "port"],
                "application": ["name", "version"],
                "security": ["ssl_enabled", "authentication"]
            },
            "field_formats": {
                "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                "url": r'^https?://[^\s/$.?#].[^\s]*$',
                "ip_address": r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$',
                "port": r'^([1-9][0-9]{0,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$',
                "version": r'^\d+\.\d+(\.\d+)?(-[a-zA-Z0-9]+)?$'
            },
            "value_ranges": {
                "port": {"min": 1, "max": 65535},
                "timeout": {"min": 1, "max": 3600},
                "retry_count": {"min": 0, "max": 10},
                "pool_size": {"min": 1, "max": 1000}
            }
        }
    
    def _initialize_security_rules(self) -> Dict[str, Any]:
        """Initialize security validation rules"""
        return {
            "sensitive_fields": [
                "password", "passwd", "pwd", "secret", "key", "token",
                "api_key", "private_key", "certificate", "credential"
            ],
            "insecure_values": [
                "password", "123456", "admin", "root", "test", "default",
                "guest", "user", "changeme", "password123"
            ],
            "security_requirements": {
                "ssl_enabled": True,
                "encryption_enabled": True,
                "authentication_required": True,
                "password_complexity": True
            },
            "dangerous_settings": {
                "debug": False,
                "test_mode": False,
                "allow_all_origins": False,
                "disable_ssl_verification": False
            }
        }
    
    def _initialize_performance_rules(self) -> Dict[str, Any]:
        """Initialize performance validation rules"""
        return {
            "recommended_values": {
                "connection_timeout": {"min": 5, "max": 30, "recommended": 10},
                "read_timeout": {"min": 5, "max": 60, "recommended": 30},
                "pool_size": {"min": 5, "max": 100, "recommended": 20},
                "max_connections": {"min": 10, "max": 1000, "recommended": 100}
            },
            "performance_warnings": {
                "large_timeout_values": 300,
                "small_pool_size": 5,
                "excessive_retry_count": 5
            }
        }
    
    async def validate_config(self, config_path: str,
                            validation_rules: Optional[List[str]] = None,
                            config_format: Optional[str] = None) -> Dict[str, Any]:
        """Validate configuration file or directory"""
        try:
            config_path = Path(config_path)
            
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration path not found: {config_path}")
            
            logger.info(f"Validating configuration: {config_path}")
            
            if config_path.is_file():
                # Validate single file
                result = await self._validate_single_file(config_path, config_format, validation_rules)
            else:
                # Validate directory
                result = await self._validate_directory(config_path, validation_rules)
            
            return result
            
        except Exception as e:
            logger.error(f"Error validating configuration: {str(e)}")
            raise
    
    async def _validate_single_file(self, file_path: Path, 
                                   config_format: Optional[str] = None,
                                   validation_rules: Optional[List[str]] = None) -> Dict[str, Any]:
        """Validate a single configuration file"""
        try:
            # Determine format
            if not config_format:
                config_format = self._detect_format(file_path)
            
            if config_format not in self.supported_formats:
                raise ValueError(f"Unsupported configuration format: {config_format}")
            
            # Read and parse file
            content = file_path.read_text(encoding='utf-8')
            
            # Format-specific validation
            format_validation = await self.supported_formats[config_format](file_path, content)
            
            # General validation
            general_validation = await self._perform_general_validation(
                format_validation.get("parsed_data", {}), validation_rules
            )
            
            # Security validation
            security_validation = await self._perform_security_validation(
                content, format_validation.get("parsed_data", {})
            )
            
            # Performance validation
            performance_validation = await self._perform_performance_validation(
                format_validation.get("parsed_data", {})
            )
            
            # Compile results
            result = {
                "file_info": {
                    "path": str(file_path),
                    "format": config_format,
                    "size": file_path.stat().st_size,
                    "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                },
                "validation_results": {
                    "format_validation": format_validation,
                    "general_validation": general_validation,
                    "security_validation": security_validation,
                    "performance_validation": performance_validation
                },
                "summary": self._generate_validation_summary([
                    format_validation, general_validation, 
                    security_validation, performance_validation
                ]),
                "validation_timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error validating file {file_path}: {str(e)}")
            raise
    
    async def _validate_directory(self, dir_path: Path, 
                                validation_rules: Optional[List[str]] = None) -> Dict[str, Any]:
        """Validate all configuration files in a directory"""
        try:
            config_files = []
            
            # Find configuration files
            for pattern in ['*.json', '*.yaml', '*.yml', '*.xml', '*.ini', '*.conf', '*.cfg', '*.properties']:
                config_files.extend(dir_path.glob(pattern))
            
            if not config_files:
                return {
                    "directory_info": {
                        "path": str(dir_path),
                        "files_found": 0
                    },
                    "message": "No configuration files found in directory"
                }
            
            # Validate each file
            file_results = []
            for config_file in config_files:
                try:
                    file_result = await self._validate_single_file(config_file, None, validation_rules)
                    file_results.append(file_result)
                except Exception as e:
                    file_results.append({
                        "file_info": {"path": str(config_file)},
                        "error": str(e)
                    })
            
            # Generate directory summary
            directory_summary = self._generate_directory_summary(file_results)
            
            return {
                "directory_info": {
                    "path": str(dir_path),
                    "files_found": len(config_files),
                    "files_validated": len(file_results)
                },
                "file_results": file_results,
                "directory_summary": directory_summary,
                "validation_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error validating directory {dir_path}: {str(e)}")
            raise
    
    def _detect_format(self, file_path: Path) -> str:
        """Detect configuration file format"""
        suffix = file_path.suffix.lower().lstrip('.')
        
        if suffix in self.supported_formats:
            return suffix
        
        # Try to detect from filename
        name_lower = file_path.name.lower()
        if 'config' in name_lower or 'conf' in name_lower:
            return 'ini'
        
        return 'unknown'
    
    async def _validate_json(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Validate JSON configuration file"""
        validation_result = {
            "format": "json",
            "valid": False,
            "errors": [],
            "warnings": [],
            "parsed_data": {}
        }
        
        try:
            # Parse JSON
            parsed_data = json.loads(content)
            validation_result["parsed_data"] = parsed_data
            validation_result["valid"] = True
            
            # JSON-specific validations
            if not isinstance(parsed_data, dict):
                validation_result["warnings"].append("Root element is not an object")
            
            # Check for common JSON issues
            if self._has_duplicate_keys(content):
                validation_result["warnings"].append("Potential duplicate keys detected")
            
        except json.JSONDecodeError as e:
            validation_result["errors"].append(f"JSON parsing error: {str(e)}")
        except Exception as e:
            validation_result["errors"].append(f"Unexpected error: {str(e)}")
        
        return validation_result
    
    async def _validate_yaml(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Validate YAML configuration file"""
        validation_result = {
            "format": "yaml",
            "valid": False,
            "errors": [],
            "warnings": [],
            "parsed_data": {}
        }
        
        try:
            # Parse YAML
            parsed_data = yaml.safe_load(content)
            validation_result["parsed_data"] = parsed_data or {}
            validation_result["valid"] = True
            
            # YAML-specific validations
            if parsed_data is None:
                validation_result["warnings"].append("YAML file is empty or contains only null")
            
            # Check for YAML best practices
            if '\t' in content:
                validation_result["warnings"].append("YAML file contains tabs - use spaces for indentation")
            
        except yaml.YAMLError as e:
            validation_result["errors"].append(f"YAML parsing error: {str(e)}")
        except Exception as e:
            validation_result["errors"].append(f"Unexpected error: {str(e)}")
        
        return validation_result
    
    async def _validate_xml(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Validate XML configuration file"""
        validation_result = {
            "format": "xml",
            "valid": False,
            "errors": [],
            "warnings": [],
            "parsed_data": {}
        }
        
        try:
            # Parse XML
            root = ET.fromstring(content)
            validation_result["parsed_data"] = self._xml_to_dict(root)
            validation_result["valid"] = True
            
            # XML-specific validations
            if not root.tag:
                validation_result["warnings"].append("XML root element has no tag")
            
        except ET.ParseError as e:
            validation_result["errors"].append(f"XML parsing error: {str(e)}")
        except Exception as e:
            validation_result["errors"].append(f"Unexpected error: {str(e)}")
        
        return validation_result
    
    async def _validate_ini(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Validate INI configuration file"""
        validation_result = {
            "format": "ini",
            "valid": False,
            "errors": [],
            "warnings": [],
            "parsed_data": {}
        }
        
        try:
            # Parse INI
            config = configparser.ConfigParser()
            config.read_string(content)
            
            # Convert to dict
            parsed_data = {}
            for section in config.sections():
                parsed_data[section] = dict(config[section])
            
            validation_result["parsed_data"] = parsed_data
            validation_result["valid"] = True
            
            # INI-specific validations
            if not config.sections():
                validation_result["warnings"].append("INI file has no sections")
            
        except configparser.Error as e:
            validation_result["errors"].append(f"INI parsing error: {str(e)}")
        except Exception as e:
            validation_result["errors"].append(f"Unexpected error: {str(e)}")
        
        return validation_result
    
    async def _validate_properties(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Validate properties configuration file"""
        validation_result = {
            "format": "properties",
            "valid": False,
            "errors": [],
            "warnings": [],
            "parsed_data": {}
        }
        
        try:
            # Parse properties file
            parsed_data = {}
            for line_num, line in enumerate(content.split('\n'), 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#') or line.startswith('!'):
                    continue
                
                # Parse key-value pairs
                if '=' in line:
                    key, value = line.split('=', 1)
                    parsed_data[key.strip()] = value.strip()
                elif ':' in line:
                    key, value = line.split(':', 1)
                    parsed_data[key.strip()] = value.strip()
                else:
                    validation_result["warnings"].append(f"Line {line_num}: Invalid property format")
            
            validation_result["parsed_data"] = parsed_data
            validation_result["valid"] = True
            
        except Exception as e:
            validation_result["errors"].append(f"Properties parsing error: {str(e)}")
        
        return validation_result
    
    async def _perform_general_validation(self, parsed_data: Dict[str, Any],
                                        validation_rules: Optional[List[str]] = None) -> Dict[str, Any]:
        """Perform general configuration validation"""
        validation_result = {
            "errors": [],
            "warnings": [],
            "info": [],
            "checks_performed": []
        }
        
        try:
            # Check required fields
            if not validation_rules or "required_fields" in validation_rules:
                required_checks = self._check_required_fields(parsed_data)
                validation_result["errors"].extend(required_checks.get("errors", []))
                validation_result["warnings"].extend(required_checks.get("warnings", []))
                validation_result["checks_performed"].append("required_fields")
            
            # Check field formats
            if not validation_rules or "field_formats" in validation_rules:
                format_checks = self._check_field_formats(parsed_data)
                validation_result["errors"].extend(format_checks.get("errors", []))
                validation_result["warnings"].extend(format_checks.get("warnings", []))
                validation_result["checks_performed"].append("field_formats")
            
            # Check value ranges
            if not validation_rules or "value_ranges" in validation_rules:
                range_checks = self._check_value_ranges(parsed_data)
                validation_result["errors"].extend(range_checks.get("errors", []))
                validation_result["warnings"].extend(range_checks.get("warnings", []))
                validation_result["checks_performed"].append("value_ranges")
            
            return validation_result
            
        except Exception as e:
            validation_result["errors"].append(f"General validation error: {str(e)}")
            return validation_result
    
    async def _perform_security_validation(self, content: str, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform security validation"""
        validation_result = {
            "errors": [],
            "warnings": [],
            "info": [],
            "security_score": 100,
            "checks_performed": []
        }
        
        try:
            # Check for hardcoded sensitive values
            sensitive_checks = self._check_sensitive_values(content, parsed_data)
            validation_result["errors"].extend(sensitive_checks.get("errors", []))
            validation_result["warnings"].extend(sensitive_checks.get("warnings", []))
            validation_result["security_score"] -= len(sensitive_checks.get("errors", [])) * 20
            validation_result["security_score"] -= len(sensitive_checks.get("warnings", [])) * 10
            validation_result["checks_performed"].append("sensitive_values")
            
            # Check security requirements
            security_req_checks = self._check_security_requirements(parsed_data)
            validation_result["errors"].extend(security_req_checks.get("errors", []))
            validation_result["warnings"].extend(security_req_checks.get("warnings", []))
            validation_result["security_score"] -= len(security_req_checks.get("errors", [])) * 15
            validation_result["checks_performed"].append("security_requirements")
            
            # Check dangerous settings
            dangerous_checks = self._check_dangerous_settings(parsed_data)
            validation_result["errors"].extend(dangerous_checks.get("errors", []))
            validation_result["warnings"].extend(dangerous_checks.get("warnings", []))
            validation_result["security_score"] -= len(dangerous_checks.get("errors", [])) * 25
            validation_result["checks_performed"].append("dangerous_settings")
            
            # Ensure score doesn't go below 0
            validation_result["security_score"] = max(0, validation_result["security_score"])
            
            return validation_result
            
        except Exception as e:
            validation_result["errors"].append(f"Security validation error: {str(e)}")
            return validation_result
    
    async def _perform_performance_validation(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform performance validation"""
        validation_result = {
            "errors": [],
            "warnings": [],
            "info": [],
            "performance_score": 100,
            "checks_performed": []
        }
        
        try:
            # Check recommended values
            perf_checks = self._check_performance_settings(parsed_data)
            validation_result["warnings"].extend(perf_checks.get("warnings", []))
            validation_result["info"].extend(perf_checks.get("info", []))
            validation_result["performance_score"] -= len(perf_checks.get("warnings", [])) * 10
            validation_result["checks_performed"].append("performance_settings")
            
            # Check for performance anti-patterns
            antipattern_checks = self._check_performance_antipatterns(parsed_data)
            validation_result["warnings"].extend(antipattern_checks.get("warnings", []))
            validation_result["performance_score"] -= len(antipattern_checks.get("warnings", [])) * 15
            validation_result["checks_performed"].append("performance_antipatterns")
            
            # Ensure score doesn't go below 0
            validation_result["performance_score"] = max(0, validation_result["performance_score"])
            
            return validation_result
            
        except Exception as e:
            validation_result["errors"].append(f"Performance validation error: {str(e)}")
            return validation_result
    
    def _check_required_fields(self, parsed_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Check for required fields"""
        result = {"errors": [], "warnings": []}
        
        # This is a simplified check - in practice, you'd determine the config type
        # and check against specific requirements
        common_required = ["name", "version"]
        
        for field in common_required:
            if not self._find_field_in_data(parsed_data, field):
                result["warnings"].append(f"Recommended field '{field}' is missing")
        
        return result
    
    def _check_field_formats(self, parsed_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Check field formats against patterns"""
        result = {"errors": [], "warnings": []}
        
        def check_recursive(data, path=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # Check if this field has a format requirement
                    for format_name, pattern in self.validation_rules["field_formats"].items():
                        if format_name.lower() in key.lower() and isinstance(value, str):
                            if not re.match(pattern, value):
                                result["errors"].append(
                                    f"Field '{current_path}' has invalid {format_name} format: {value}"
                                )
                    
                    if isinstance(value, (dict, list)):
                        check_recursive(value, current_path)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    check_recursive(item, f"{path}[{i}]")
        
        check_recursive(parsed_data)
        return result
    
    def _check_value_ranges(self, parsed_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Check value ranges"""
        result = {"errors": [], "warnings": []}
        
        def check_recursive(data, path=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # Check if this field has range requirements
                    for range_name, range_info in self.validation_rules["value_ranges"].items():
                        if range_name.lower() in key.lower() and isinstance(value, (int, float)):
                            min_val = range_info.get("min")
                            max_val = range_info.get("max")
                            
                            if min_val is not None and value < min_val:
                                result["errors"].append(
                                    f"Field '{current_path}' value {value} is below minimum {min_val}"
                                )
                            elif max_val is not None and value > max_val:
                                result["errors"].append(
                                    f"Field '{current_path}' value {value} is above maximum {max_val}"
                                )
                    
                    if isinstance(value, (dict, list)):
                        check_recursive(value, current_path)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    check_recursive(item, f"{path}[{i}]")
        
        check_recursive(parsed_data)
        return result
    
    def _check_sensitive_values(self, content: str, parsed_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Check for hardcoded sensitive values"""
        result = {"errors": [], "warnings": []}
        
        # Check for sensitive field names with values
        for sensitive_field in self.security_rules["sensitive_fields"]:
            # Check in content (case-insensitive)
            pattern = rf'{sensitive_field}\s*[=:]\s*["\']?([^"\'\s\n]+)'
            matches = re.findall(pattern, content, re.IGNORECASE)
            
            for match in matches:
                if match and match not in ['', 'null', 'none', '${VAR}', '${' + sensitive_field.upper() + '}']:
                    result["errors"].append(
                        f"Hardcoded {sensitive_field} detected: {match[:10]}..."
                    )
        
        # Check for insecure default values
        def check_recursive(data, path=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    if isinstance(value, str) and value.lower() in self.security_rules["insecure_values"]:
                        result["warnings"].append(
                            f"Insecure default value detected at '{current_path}': {value}"
                        )
                    
                    if isinstance(value, (dict, list)):
                        check_recursive(value, current_path)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    check_recursive(item, f"{path}[{i}]")
        
        check_recursive(parsed_data)
        return result
    
    def _check_security_requirements(self, parsed_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Check security requirements"""
        result = {"errors": [], "warnings": []}
        
        for requirement, expected_value in self.security_rules["security_requirements"].items():
            found_value = self._find_field_in_data(parsed_data, requirement)
            
            if found_value is None:
                result["warnings"].append(f"Security setting '{requirement}' not found")
            elif found_value != expected_value:
                result["warnings"].append(
                    f"Security setting '{requirement}' should be {expected_value}, found {found_value}"
                )
        
        return result
    
    def _check_dangerous_settings(self, parsed_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Check for dangerous settings"""
        result = {"errors": [], "warnings": []}
        
        for setting, safe_value in self.security_rules["dangerous_settings"].items():
            found_value = self._find_field_in_data(parsed_data, setting)
            
            if found_value is not None and found_value != safe_value:
                severity = "errors" if setting in ["disable_ssl_verification", "allow_all_origins"] else "warnings"
                result[severity].append(
                    f"Dangerous setting '{setting}' is set to {found_value}, should be {safe_value}"
                )
        
        return result
    
    def _check_performance_settings(self, parsed_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Check performance settings"""
        result = {"warnings": [], "info": []}
        
        for setting, config in self.performance_rules["recommended_values"].items():
            found_value = self._find_field_in_data(parsed_data, setting)
            
            if found_value is not None and isinstance(found_value, (int, float)):
                recommended = config.get("recommended")
                min_val = config.get("min")
                max_val = config.get("max")
                
                if found_value < min_val:
                    result["warnings"].append(
                        f"Performance setting '{setting}' value {found_value} is below recommended minimum {min_val}"
                    )
                elif found_value > max_val:
                    result["warnings"].append(
                        f"Performance setting '{setting}' value {found_value} exceeds recommended maximum {max_val}"
                    )
                elif recommended and abs(found_value - recommended) > recommended * 0.5:
                    result["info"].append(
                        f"Performance setting '{setting}' value {found_value} differs significantly from recommended {recommended}"
                    )
        
        return result
    
    def _check_performance_antipatterns(self, parsed_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Check for performance anti-patterns"""
        result = {"warnings": []}
        
        # Check for specific anti-patterns
        timeout_value = self._find_field_in_data(parsed_data, "timeout")
        if timeout_value and isinstance(timeout_value, (int, float)):
            if timeout_value > self.performance_rules["performance_warnings"]["large_timeout_values"]:
                result["warnings"].append(f"Very large timeout value detected: {timeout_value} seconds")
        
        pool_size = self._find_field_in_data(parsed_data, "pool_size")
        if pool_size and isinstance(pool_size, (int, float)):
            if pool_size < self.performance_rules["performance_warnings"]["small_pool_size"]:
                result["warnings"].append(f"Small connection pool size may impact performance: {pool_size}")
        
        retry_count = self._find_field_in_data(parsed_data, "retry")
        if retry_count and isinstance(retry_count, (int, float)):
            if retry_count > self.performance_rules["performance_warnings"]["excessive_retry_count"]:
                result["warnings"].append(f"Excessive retry count may cause delays: {retry_count}")
        
        return result
    
    def _find_field_in_data(self, data: Any, field_name: str) -> Any:
        """Find a field in nested data structure (case-insensitive)"""
        if isinstance(data, dict):
            for key, value in data.items():
                if key.lower() == field_name.lower():
                    return value
                elif isinstance(value, (dict, list)):
                    result = self._find_field_in_data(value, field_name)
                    if result is not None:
                        return result
        elif isinstance(data, list):
            for item in data:
                result = self._find_field_in_data(item, field_name)
                if result is not None:
                    return result
        
        return None
    
    def _has_duplicate_keys(self, json_content: str) -> bool:
        """Check for duplicate keys in JSON (simplified check)"""
        try:
            # This is a basic check - a more sophisticated implementation
            # would parse the JSON while tracking keys
            keys_found = []
            key_pattern = r'"([^"]+)"\s*:'
            
            for match in re.finditer(key_pattern, json_content):
                key = match.group(1)
                if key in keys_found:
                    return True
                keys_found.append(key)
            
            return False
        except Exception:
            return False
    
    def _xml_to_dict(self, element) -> Dict[str, Any]:
        """Convert XML element to dictionary"""
        result = {}
        
        # Add attributes
        if element.attrib:
            result['@attributes'] = element.attrib
        
        # Add text content
        if element.text and element.text.strip():
            if len(element) == 0:  # No child elements
                return element.text.strip()
            else:
                result['#text'] = element.text.strip()
        
        # Add child elements
        for child in element:
            child_data = self._xml_to_dict(child)
            if child.tag in result:
                # Handle multiple children with same tag
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        return result
    
    def _generate_validation_summary(self, validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of validation results"""
        summary = {
            "overall_status": "passed",
            "total_errors": 0,
            "total_warnings": 0,
            "total_info": 0,
            "security_score": 100,
            "performance_score": 100,
            "recommendations": []
        }
        
        for result in validation_results:
            errors = result.get("errors", [])
            warnings = result.get("warnings", [])
            info = result.get("info", [])
            
            summary["total_errors"] += len(errors)
            summary["total_warnings"] += len(warnings)
            summary["total_info"] += len(info)
            
            # Update scores
            if "security_score" in result:
                summary["security_score"] = min(summary["security_score"], result["security_score"])
            if "performance_score" in result:
                summary["performance_score"] = min(summary["performance_score"], result["performance_score"])
        
        # Determine overall status
        if summary["total_errors"] > 0:
            summary["overall_status"] = "failed"
        elif summary["total_warnings"] > 0:
            summary["overall_status"] = "warning"
        
        # Generate recommendations
        if summary["total_errors"] > 0:
            summary["recommendations"].append("Fix all validation errors before deployment")
        if summary["total_warnings"] > 0:
            summary["recommendations"].append("Review and address validation warnings")
        if summary["security_score"] < 80:
            summary["recommendations"].append("Improve security configuration")
        if summary["performance_score"] < 80:
            summary["recommendations"].append("Optimize performance settings")
        
        return summary
    
    def _generate_directory_summary(self, file_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary for directory validation"""
        summary = {
            "files_with_errors": 0,
            "files_with_warnings": 0,
            "total_errors": 0,
            "total_warnings": 0,
            "average_security_score": 0,
            "average_performance_score": 0,
            "overall_status": "passed"
        }
        
        security_scores = []
        performance_scores = []
        
        for result in file_results:
            if "error" in result:
                summary["files_with_errors"] += 1
                continue
            
            validation_summary = result.get("summary", {})
            
            if validation_summary.get("total_errors", 0) > 0:
                summary["files_with_errors"] += 1
                summary["total_errors"] += validation_summary["total_errors"]
            
            if validation_summary.get("total_warnings", 0) > 0:
                summary["files_with_warnings"] += 1
                summary["total_warnings"] += validation_summary["total_warnings"]
            
            # Collect scores
            security_score = validation_summary.get("security_score", 100)
            performance_score = validation_summary.get("performance_score", 100)
            
            security_scores.append(security_score)
            performance_scores.append(performance_score)
        
        # Calculate averages
        if security_scores:
            summary["average_security_score"] = sum(security_scores) / len(security_scores)
        if performance_scores:
            summary["average_performance_score"] = sum(performance_scores) / len(performance_scores)
        
        # Determine overall status
        if summary["files_with_errors"] > 0:
            summary["overall_status"] = "failed"
        elif summary["files_with_warnings"] > 0:
            summary["overall_status"] = "warning"
        
        return summary