"""
Excel Processor for Configuration Data Extraction and Analysis
"""

import pandas as pd
import json
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from loguru import logger
import re


class ExcelProcessor:
    """Process Excel files for configuration data extraction and validation"""
    
    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls', '.xlsm']
        self.config_patterns = {
            'network': {
                'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
                'port': r'\b(?:[1-9][0-9]{0,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])\b',
                'mac_address': r'\b[0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}\b',
                'subnet': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\/[0-9]{1,2}\b'
            },
            'database': {
                'connection_string': r'(?i)(server|host|data source|database|uid|user id|pwd|password|port)',
                'table_name': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
                'sql_query': r'(?i)(select|insert|update|delete|create|alter|drop)',
            },
            'system': {
                'file_path': r'[A-Za-z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*|\/(?:[^\/\0]+\/)*[^\/\0]*',
                'environment_var': r'\$[A-Za-z_][A-Za-z0-9_]*|\%[A-Za-z_][A-Za-z0-9_]*\%',
                'service_name': r'\b[a-zA-Z][a-zA-Z0-9\-_]*\.service\b'
            }
        }
    
    async def process_file(self, file_path: str, sheet_name: Optional[str] = None, 
                          config_type: str = "general") -> Dict[str, Any]:
        """Process Excel file and extract configuration data"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"Excel file not found: {file_path}")
            
            if file_path.suffix.lower() not in self.supported_formats:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
            logger.info(f"Processing Excel file: {file_path}")
            
            # Read Excel file
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                sheets_data = {sheet_name: df}
            else:
                sheets_data = pd.read_excel(file_path, sheet_name=None)
            
            result = {
                "file_info": {
                    "path": str(file_path),
                    "size": file_path.stat().st_size,
                    "sheets": list(sheets_data.keys())
                },
                "extracted_data": {},
                "configuration_analysis": {},
                "validation_results": {}
            }
            
            # Process each sheet
            for sheet, df in sheets_data.items():
                logger.info(f"Processing sheet: {sheet}")
                
                sheet_result = await self._process_sheet(df, config_type, sheet)
                result["extracted_data"][sheet] = sheet_result["data"]
                result["configuration_analysis"][sheet] = sheet_result["analysis"]
                result["validation_results"][sheet] = sheet_result["validation"]
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing Excel file {file_path}: {str(e)}")
            raise
    
    async def _process_sheet(self, df: pd.DataFrame, config_type: str, sheet_name: str) -> Dict[str, Any]:
        """Process individual Excel sheet"""
        try:
            # Basic data extraction
            data_summary = {
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": df.columns.tolist(),
                "data_types": df.dtypes.to_dict(),
                "null_values": df.isnull().sum().to_dict(),
                "sample_data": df.head(3).to_dict('records') if not df.empty else []
            }
            
            # Configuration pattern analysis
            config_analysis = await self._analyze_configuration_patterns(df, config_type)
            
            # Data validation
            validation_results = await self._validate_configuration_data(df, config_type)
            
            return {
                "data": data_summary,
                "analysis": config_analysis,
                "validation": validation_results
            }
            
        except Exception as e:
            logger.error(f"Error processing sheet {sheet_name}: {str(e)}")
            raise
    
    async def _analyze_configuration_patterns(self, df: pd.DataFrame, config_type: str) -> Dict[str, Any]:
        """Analyze configuration patterns in the data"""
        analysis = {
            "detected_patterns": {},
            "configuration_items": [],
            "potential_issues": []
        }
        
        try:
            patterns = self.config_patterns.get(config_type, {})
            
            # Search for configuration patterns in all text columns
            for column in df.columns:
                if df[column].dtype == 'object':  # Text columns
                    column_analysis = {}
                    
                    for pattern_name, pattern_regex in patterns.items():
                        matches = []
                        for idx, value in df[column].items():
                            if pd.notna(value) and isinstance(value, str):
                                found_matches = re.findall(pattern_regex, value, re.IGNORECASE)
                                if found_matches:
                                    matches.extend([{
                                        "row": idx,
                                        "value": value,
                                        "matches": found_matches
                                    }])
                        
                        if matches:
                            column_analysis[pattern_name] = matches
                    
                    if column_analysis:
                        analysis["detected_patterns"][column] = column_analysis
            
            # Extract configuration items
            config_items = await self._extract_configuration_items(df, config_type)
            analysis["configuration_items"] = config_items
            
            # Identify potential issues
            issues = await self._identify_potential_issues(df, analysis["detected_patterns"])
            analysis["potential_issues"] = issues
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing configuration patterns: {str(e)}")
            return analysis
    
    async def _extract_configuration_items(self, df: pd.DataFrame, config_type: str) -> List[Dict[str, Any]]:
        """Extract specific configuration items from the data"""
        config_items = []
        
        try:
            # Look for key-value pairs in the data
            for idx, row in df.iterrows():
                for col in df.columns:
                    value = row[col]
                    if pd.notna(value):
                        # Check if this looks like a configuration item
                        if self._is_configuration_item(str(col), str(value), config_type):
                            config_items.append({
                                "row": idx,
                                "key": str(col),
                                "value": str(value),
                                "type": self._classify_config_item(str(col), str(value), config_type)
                            })
            
            return config_items
            
        except Exception as e:
            logger.error(f"Error extracting configuration items: {str(e)}")
            return []
    
    def _is_configuration_item(self, key: str, value: str, config_type: str) -> bool:
        """Check if a key-value pair represents a configuration item"""
        config_keywords = {
            'network': ['ip', 'port', 'host', 'server', 'gateway', 'dns', 'subnet', 'vlan'],
            'database': ['connection', 'server', 'database', 'table', 'user', 'password', 'port', 'timeout'],
            'system': ['path', 'directory', 'file', 'service', 'process', 'memory', 'cpu', 'disk'],
            'general': ['config', 'setting', 'parameter', 'option', 'value', 'property']
        }
        
        keywords = config_keywords.get(config_type, config_keywords['general'])
        key_lower = key.lower()
        
        return any(keyword in key_lower for keyword in keywords)
    
    def _classify_config_item(self, key: str, value: str, config_type: str) -> str:
        """Classify the type of configuration item"""
        key_lower = key.lower()
        value_lower = value.lower()
        
        # Network configurations
        if any(term in key_lower for term in ['ip', 'address']):
            return 'ip_address'
        elif 'port' in key_lower:
            return 'port'
        elif any(term in key_lower for term in ['host', 'server']):
            return 'hostname'
        
        # Database configurations
        elif 'connection' in key_lower:
            return 'connection_string'
        elif 'database' in key_lower:
            return 'database_name'
        elif any(term in key_lower for term in ['user', 'username']):
            return 'username'
        elif 'password' in key_lower:
            return 'password'
        
        # System configurations
        elif 'path' in key_lower:
            return 'file_path'
        elif 'service' in key_lower:
            return 'service_name'
        elif any(term in key_lower for term in ['memory', 'ram']):
            return 'memory_setting'
        elif 'cpu' in key_lower:
            return 'cpu_setting'
        
        return 'general'
    
    async def _validate_configuration_data(self, df: pd.DataFrame, config_type: str) -> Dict[str, Any]:
        """Validate configuration data for common issues"""
        validation = {
            "data_quality": {},
            "security_issues": [],
            "consistency_checks": {},
            "recommendations": []
        }
        
        try:
            # Data quality checks
            validation["data_quality"] = {
                "missing_values": df.isnull().sum().to_dict(),
                "duplicate_rows": df.duplicated().sum(),
                "empty_cells_percentage": (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            }
            
            # Security issue detection
            security_issues = []
            for column in df.columns:
                if df[column].dtype == 'object':
                    for idx, value in df[column].items():
                        if pd.notna(value) and isinstance(value, str):
                            # Check for hardcoded passwords
                            if 'password' in column.lower() and value not in ['', 'null', 'none']:
                                security_issues.append({
                                    "type": "hardcoded_password",
                                    "location": f"Row {idx}, Column {column}",
                                    "severity": "high",
                                    "description": "Hardcoded password detected"
                                })
                            
                            # Check for default credentials
                            if value.lower() in ['admin', 'administrator', 'root', 'password', '123456']:
                                security_issues.append({
                                    "type": "default_credentials",
                                    "location": f"Row {idx}, Column {column}",
                                    "severity": "high",
                                    "description": "Default/weak credentials detected"
                                })
            
            validation["security_issues"] = security_issues
            
            # Generate recommendations
            recommendations = []
            if validation["data_quality"]["empty_cells_percentage"] > 10:
                recommendations.append("Consider filling missing values or removing incomplete rows")
            
            if validation["data_quality"]["duplicate_rows"] > 0:
                recommendations.append("Remove duplicate rows to ensure data consistency")
            
            if security_issues:
                recommendations.append("Review and secure sensitive configuration data")
            
            validation["recommendations"] = recommendations
            
            return validation
            
        except Exception as e:
            logger.error(f"Error validating configuration data: {str(e)}")
            return validation
    
    async def _identify_potential_issues(self, df: pd.DataFrame, detected_patterns: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify potential configuration issues"""
        issues = []
        
        try:
            # Check for invalid IP addresses
            for column, patterns in detected_patterns.items():
                if 'ip_address' in patterns:
                    for match_info in patterns['ip_address']:
                        for ip in match_info['matches']:
                            if not self._is_valid_ip(ip):
                                issues.append({
                                    "type": "invalid_ip_address",
                                    "location": f"Row {match_info['row']}, Column {column}",
                                    "value": ip,
                                    "severity": "medium",
                                    "description": f"Invalid IP address format: {ip}"
                                })
                
                # Check for invalid ports
                if 'port' in patterns:
                    for match_info in patterns['port']:
                        for port in match_info['matches']:
                            try:
                                port_num = int(port)
                                if port_num < 1 or port_num > 65535:
                                    issues.append({
                                        "type": "invalid_port",
                                        "location": f"Row {match_info['row']}, Column {column}",
                                        "value": port,
                                        "severity": "medium",
                                        "description": f"Port number out of valid range: {port}"
                                    })
                            except ValueError:
                                issues.append({
                                    "type": "invalid_port_format",
                                    "location": f"Row {match_info['row']}, Column {column}",
                                    "value": port,
                                    "severity": "medium",
                                    "description": f"Invalid port format: {port}"
                                })
            
            return issues
            
        except Exception as e:
            logger.error(f"Error identifying potential issues: {str(e)}")
            return []
    
    def _is_valid_ip(self, ip: str) -> bool:
        """Validate IP address format"""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            
            return True
        except (ValueError, AttributeError):
            return False