"""
Configuration validation engine with automated testing.
Provides comprehensive validation capabilities for configuration research.
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional, Union, Callable
from pathlib import Path
import json
import re
import subprocess
import tempfile
from datetime import datetime
from dataclasses import dataclass, asdict
import yaml
import jsonschema
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)


@dataclass
class ValidationRule:
    """Represents a validation rule."""
    name: str
    description: str
    rule_type: str  # 'regex', 'schema', 'custom', 'command'
    pattern: Optional[str] = None
    schema: Optional[Dict[str, Any]] = None
    custom_function: Optional[str] = None
    command: Optional[str] = None
    severity: str = "error"  # 'error', 'warning', 'info'
    enabled: bool = True


@dataclass
class ValidationResult:
    """Result of a validation operation."""
    rule_name: str
    status: str  # 'passed', 'failed', 'warning', 'error'
    message: str
    details: Dict[str, Any]
    timestamp: str
    execution_time: float


@dataclass
class ValidationReport:
    """Comprehensive validation report."""
    validation_id: str
    target: str
    total_rules: int
    passed_rules: int
    failed_rules: int
    warning_rules: int
    results: List[ValidationResult]
    overall_status: str
    created_at: str
    execution_time: float


class ValidationEngine:
    """Engine for validating configurations with automated testing."""
    
    def __init__(self):
        self.rules: Dict[str, ValidationRule] = {}
        self.custom_validators: Dict[str, Callable] = {}
        self.validation_history: List[ValidationReport] = []
        
        # Load default validation rules
        self._load_default_rules()
        
        logger.info("Validation Engine initialized")
    
    def _load_default_rules(self):
        """Load default validation rules."""
        default_rules = [
            ValidationRule(
                name="required_fields",
                description="Check for required configuration fields",
                rule_type="custom",
                custom_function="check_required_fields",
                severity="error"
            ),
            ValidationRule(
                name="port_range",
                description="Validate port numbers are in valid range",
                rule_type="regex",
                pattern=r"^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$",
                severity="error"
            ),
            ValidationRule(
                name="url_format",
                description="Validate URL format",
                rule_type="regex",
                pattern=r"^https?://[^\s/$.?#].[^\s]*$",
                severity="error"
            ),
            ValidationRule(
                name="email_format",
                description="Validate email format",
                rule_type="regex",
                pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                severity="error"
            ),
            ValidationRule(
                name="json_syntax",
                description="Validate JSON syntax",
                rule_type="custom",
                custom_function="validate_json_syntax",
                severity="error"
            ),
            ValidationRule(
                name="yaml_syntax",
                description="Validate YAML syntax",
                rule_type="custom",
                custom_function="validate_yaml_syntax",
                severity="error"
            ),
            ValidationRule(
                name="password_strength",
                description="Check password strength",
                rule_type="custom",
                custom_function="check_password_strength",
                severity="warning"
            ),
            ValidationRule(
                name="file_permissions",
                description="Check file permissions",
                rule_type="custom",
                custom_function="check_file_permissions",
                severity="warning"
            )
        ]
        
        for rule in default_rules:
            self.rules[rule.name] = rule
    
    def add_validation_rule(self, rule: ValidationRule):
        """Add a new validation rule."""
        self.rules[rule.name] = rule
        logger.info(f"Added validation rule: {rule.name}")
    
    def remove_validation_rule(self, rule_name: str):
        """Remove a validation rule."""
        if rule_name in self.rules:
            del self.rules[rule_name]
            logger.info(f"Removed validation rule: {rule_name}")
    
    def register_custom_validator(self, name: str, validator_func: Callable):
        """Register a custom validator function."""
        self.custom_validators[name] = validator_func
        logger.info(f"Registered custom validator: {name}")
    
    async def validate_configuration(self,
                                   config_data: Dict[str, Any],
                                   config_type: str = "generic",
                                   target_path: Optional[str] = None) -> ValidationReport:
        """
        Validate a configuration against all applicable rules.
        
        Args:
            config_data: Configuration data to validate
            config_type: Type of configuration (e.g., 'database', 'api', 'web')
            target_path: Optional path to the configuration file
            
        Returns:
            ValidationReport object
        """
        validation_id = f"val_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = datetime.now()
        
        results = []
        passed_count = 0
        failed_count = 0
        warning_count = 0
        
        # Get applicable rules based on config type
        applicable_rules = self._get_applicable_rules(config_type)
        
        # Execute validation rules
        for rule_name, rule in applicable_rules.items():
            if not rule.enabled:
                continue
            
            try:
                result = await self._execute_rule(rule, config_data, target_path)
                results.append(result)
                
                if result.status == "passed":
                    passed_count += 1
                elif result.status == "failed":
                    failed_count += 1
                elif result.status == "warning":
                    warning_count += 1
                    
            except Exception as e:
                logger.error(f"Error executing rule {rule_name}: {str(e)}")
                results.append(ValidationResult(
                    rule_name=rule_name,
                    status="error",
                    message=f"Rule execution failed: {str(e)}",
                    details={"error": str(e)},
                    timestamp=datetime.now().isoformat(),
                    execution_time=0.0
                ))
                failed_count += 1
        
        # Determine overall status
        overall_status = "passed"
        if failed_count > 0:
            overall_status = "failed"
        elif warning_count > 0:
            overall_status = "warning"
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Create validation report
        report = ValidationReport(
            validation_id=validation_id,
            target=target_path or "in-memory",
            total_rules=len(applicable_rules),
            passed_rules=passed_count,
            failed_rules=failed_count,
            warning_rules=warning_count,
            results=results,
            overall_status=overall_status,
            created_at=datetime.now().isoformat(),
            execution_time=execution_time
        )
        
        self.validation_history.append(report)
        logger.info(f"Validation completed: {validation_id} - {overall_status}")
        
        return report
    
    def _get_applicable_rules(self, config_type: str) -> Dict[str, ValidationRule]:
        """Get rules applicable to the configuration type."""
        # For now, return all rules. Can be enhanced to filter based on config type
        return {name: rule for name, rule in self.rules.items() if rule.enabled}
    
    async def _execute_rule(self,
                          rule: ValidationRule,
                          config_data: Dict[str, Any],
                          target_path: Optional[str]) -> ValidationResult:
        """Execute a single validation rule."""
        start_time = datetime.now()
        
        try:
            if rule.rule_type == "regex":
                result = await self._validate_regex(rule, config_data)
            elif rule.rule_type == "schema":
                result = await self._validate_schema(rule, config_data)
            elif rule.rule_type == "custom":
                result = await self._validate_custom(rule, config_data, target_path)
            elif rule.rule_type == "command":
                result = await self._validate_command(rule, config_data, target_path)
            else:
                result = ValidationResult(
                    rule_name=rule.name,
                    status="error",
                    message=f"Unknown rule type: {rule.rule_type}",
                    details={},
                    timestamp=datetime.now().isoformat(),
                    execution_time=0.0
                )
            
            result.execution_time = (datetime.now() - start_time).total_seconds()
            return result
            
        except Exception as e:
            return ValidationResult(
                rule_name=rule.name,
                status="error",
                message=f"Rule execution error: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now().isoformat(),
                execution_time=(datetime.now() - start_time).total_seconds()
            )
    
    async def _validate_regex(self, rule: ValidationRule, config_data: Dict[str, Any]) -> ValidationResult:
        """Validate using regex pattern."""
        if not rule.pattern:
            return ValidationResult(
                rule_name=rule.name,
                status="error",
                message="No regex pattern defined",
                details={},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
        
        pattern = re.compile(rule.pattern)
        failed_fields = []
        
        for key, value in config_data.items():
            if isinstance(value, str) and not pattern.match(value):
                failed_fields.append({
                    "field": key,
                    "value": value,
                    "pattern": rule.pattern
                })
        
        if failed_fields:
            return ValidationResult(
                rule_name=rule.name,
                status="failed",
                message=f"Regex validation failed for {len(failed_fields)} fields",
                details={"failed_fields": failed_fields},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
        else:
            return ValidationResult(
                rule_name=rule.name,
                status="passed",
                message="Regex validation passed",
                details={},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
    
    async def _validate_schema(self, rule: ValidationRule, config_data: Dict[str, Any]) -> ValidationResult:
        """Validate using JSON schema."""
        if not rule.schema:
            return ValidationResult(
                rule_name=rule.name,
                status="error",
                message="No schema defined",
                details={},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
        
        try:
            validate(instance=config_data, schema=rule.schema)
            return ValidationResult(
                rule_name=rule.name,
                status="passed",
                message="Schema validation passed",
                details={},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
        except ValidationError as e:
            return ValidationResult(
                rule_name=rule.name,
                status="failed",
                message=f"Schema validation failed: {e.message}",
                details={"validation_error": str(e)},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
    
    async def _validate_custom(self,
                             rule: ValidationRule,
                             config_data: Dict[str, Any],
                             target_path: Optional[str]) -> ValidationResult:
        """Validate using custom function."""
        if not rule.custom_function:
            return ValidationResult(
                rule_name=rule.name,
                status="error",
                message="No custom function defined",
                details={},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
        
        # Check if custom validator is registered
        if rule.custom_function in self.custom_validators:
            try:
                result = await self.custom_validators[rule.custom_function](config_data, target_path)
                return result
            except Exception as e:
                return ValidationResult(
                    rule_name=rule.name,
                    status="error",
                    message=f"Custom validation error: {str(e)}",
                    details={"error": str(e)},
                    timestamp=datetime.now().isoformat(),
                    execution_time=0.0
                )
        
        # Try built-in custom validators
        if hasattr(self, f"_validate_{rule.custom_function}"):
            validator_func = getattr(self, f"_validate_{rule.custom_function}")
            try:
                result = await validator_func(config_data, target_path)
                return result
            except Exception as e:
                return ValidationResult(
                    rule_name=rule.name,
                    status="error",
                    message=f"Built-in validation error: {str(e)}",
                    details={"error": str(e)},
                    timestamp=datetime.now().isoformat(),
                    execution_time=0.0
                )
        
        return ValidationResult(
            rule_name=rule.name,
            status="error",
            message=f"Custom function '{rule.custom_function}' not found",
            details={},
            timestamp=datetime.now().isoformat(),
            execution_time=0.0
        )
    
    async def _validate_command(self,
                              rule: ValidationRule,
                              config_data: Dict[str, Any],
                              target_path: Optional[str]) -> ValidationResult:
        """Validate using external command."""
        if not rule.command:
            return ValidationResult(
                rule_name=rule.name,
                status="error",
                message="No command defined",
                details={},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
        
        try:
            # Create temporary file with config data
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(config_data, f)
                temp_file = f.name
            
            # Execute command
            cmd = rule.command.replace('{file}', temp_file)
            result = subprocess.run(
                cmd.split(),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Clean up temp file
            Path(temp_file).unlink()
            
            if result.returncode == 0:
                return ValidationResult(
                    rule_name=rule.name,
                    status="passed",
                    message="Command validation passed",
                    details={"stdout": result.stdout, "stderr": result.stderr},
                    timestamp=datetime.now().isoformat(),
                    execution_time=0.0
                )
            else:
                return ValidationResult(
                    rule_name=rule.name,
                    status="failed",
                    message=f"Command validation failed with return code {result.returncode}",
                    details={"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode},
                    timestamp=datetime.now().isoformat(),
                    execution_time=0.0
                )
                
        except subprocess.TimeoutExpired:
            return ValidationResult(
                rule_name=rule.name,
                status="error",
                message="Command validation timed out",
                details={},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
        except Exception as e:
            return ValidationResult(
                rule_name=rule.name,
                status="error",
                message=f"Command execution error: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
    
    # Built-in custom validators
    async def _validate_check_required_fields(self, config_data: Dict[str, Any], target_path: Optional[str]) -> ValidationResult:
        """Check for required fields in configuration."""
        required_fields = ["host", "port", "username", "password"]
        missing_fields = [field for field in required_fields if field not in config_data]
        
        if missing_fields:
            return ValidationResult(
                rule_name="check_required_fields",
                status="failed",
                message=f"Missing required fields: {', '.join(missing_fields)}",
                details={"missing_fields": missing_fields},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
        else:
            return ValidationResult(
                rule_name="check_required_fields",
                status="passed",
                message="All required fields present",
                details={},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
    
    async def _validate_validate_json_syntax(self, config_data: Dict[str, Any], target_path: Optional[str]) -> ValidationResult:
        """Validate JSON syntax."""
        try:
            json.dumps(config_data)
            return ValidationResult(
                rule_name="validate_json_syntax",
                status="passed",
                message="JSON syntax is valid",
                details={},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
        except (TypeError, ValueError) as e:
            return ValidationResult(
                rule_name="validate_json_syntax",
                status="failed",
                message=f"Invalid JSON syntax: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
    
    async def _validate_validate_yaml_syntax(self, config_data: Dict[str, Any], target_path: Optional[str]) -> ValidationResult:
        """Validate YAML syntax."""
        try:
            yaml.dump(config_data)
            return ValidationResult(
                rule_name="validate_yaml_syntax",
                status="passed",
                message="YAML syntax is valid",
                details={},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
        except yaml.YAMLError as e:
            return ValidationResult(
                rule_name="validate_yaml_syntax",
                status="failed",
                message=f"Invalid YAML syntax: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
    
    async def _validate_check_password_strength(self, config_data: Dict[str, Any], target_path: Optional[str]) -> ValidationResult:
        """Check password strength."""
        weak_passwords = []
        
        for key, value in config_data.items():
            if "password" in key.lower() and isinstance(value, str):
                if len(value) < 8:
                    weak_passwords.append({"field": key, "reason": "too_short"})
                elif not any(c.isupper() for c in value):
                    weak_passwords.append({"field": key, "reason": "no_uppercase"})
                elif not any(c.islower() for c in value):
                    weak_passwords.append({"field": key, "reason": "no_lowercase"})
                elif not any(c.isdigit() for c in value):
                    weak_passwords.append({"field": key, "reason": "no_digit"})
        
        if weak_passwords:
            return ValidationResult(
                rule_name="check_password_strength",
                status="warning",
                message=f"Weak passwords found in {len(weak_passwords)} fields",
                details={"weak_passwords": weak_passwords},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
        else:
            return ValidationResult(
                rule_name="check_password_strength",
                status="passed",
                message="All passwords meet strength requirements",
                details={},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
    
    async def _validate_check_file_permissions(self, config_data: Dict[str, Any], target_path: Optional[str]) -> ValidationResult:
        """Check file permissions."""
        if not target_path or not Path(target_path).exists():
            return ValidationResult(
                rule_name="check_file_permissions",
                status="warning",
                message="File path not provided or file does not exist",
                details={},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
        
        file_path = Path(target_path)
        stat_info = file_path.stat()
        
        # Check if file is readable by others (security concern)
        if stat_info.st_mode & 0o004:
            return ValidationResult(
                rule_name="check_file_permissions",
                status="warning",
                message="File is readable by others (security risk)",
                details={"permissions": oct(stat_info.st_mode)},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
        else:
            return ValidationResult(
                rule_name="check_file_permissions",
                status="passed",
                message="File permissions are secure",
                details={"permissions": oct(stat_info.st_mode)},
                timestamp=datetime.now().isoformat(),
                execution_time=0.0
            )
    
    def get_validation_history(self, limit: int = 10) -> List[ValidationReport]:
        """Get recent validation history."""
        return self.validation_history[-limit:]
    
    def save_validation_report(self, report: ValidationReport, output_file: Optional[str] = None) -> Path:
        """Save validation report to JSON file."""
        if output_file is None:
            output_file = Path("/workspace/data") / f"validation_report_{report.validation_id}.json"
        else:
            output_file = Path(output_file)
        
        # Convert to dictionary for JSON serialization
        report_dict = asdict(report)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved validation report to: {output_file}")
        return output_file
    
    def load_validation_rules(self, rules_file: Union[str, Path]):
        """Load validation rules from JSON file."""
        rules_file = Path(rules_file)
        
        with open(rules_file, 'r', encoding='utf-8') as f:
            rules_data = json.load(f)
        
        for rule_data in rules_data:
            rule = ValidationRule(**rule_data)
            self.rules[rule.name] = rule
        
        logger.info(f"Loaded {len(rules_data)} validation rules from {rules_file}")
    
    def save_validation_rules(self, output_file: Optional[str] = None) -> Path:
        """Save current validation rules to JSON file."""
        if output_file is None:
            output_file = Path("/workspace/data") / "validation_rules.json"
        else:
            output_file = Path(output_file)
        
        # Convert rules to dictionary
        rules_data = [asdict(rule) for rule in self.rules.values()]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(rules_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(rules_data)} validation rules to {output_file}")
        return output_file