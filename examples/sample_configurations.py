"""
Sample configuration files and data for testing the system.
This file contains various configuration examples for different scenarios.
"""
import json
import yaml
from pathlib import Path


def create_sample_excel_config():
    """Create a sample Excel configuration file."""
    import pandas as pd
    
    # Sample database configuration
    db_config = {
        'Field': ['host', 'port', 'username', 'password', 'database', 'timeout', 'ssl_enabled'],
        'Value': ['localhost', 5432, 'admin', 'secret123', 'myapp', 30, True],
        'Type': ['string', 'integer', 'string', 'string', 'string', 'integer', 'boolean'],
        'Required': [True, True, True, True, True, False, False],
        'Description': [
            'Database host address',
            'Database port number',
            'Database username',
            'Database password',
            'Database name',
            'Connection timeout in seconds',
            'Enable SSL connection'
        ]
    }
    
    df = pd.DataFrame(db_config)
    
    # Create Excel file
    excel_path = Path("/workspace/data/excel_templates/sample_database_config.xlsx")
    excel_path.parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Configuration', index=False)
        
        # Add validation rules sheet
        validation_rules = {
            'Field': ['port', 'timeout', 'password'],
            'Rule': ['1-65535', '1-300', 'min_length_8'],
            'Error_Message': [
                'Port must be between 1 and 65535',
                'Timeout must be between 1 and 300 seconds',
                'Password must be at least 8 characters long'
            ]
        }
        
        validation_df = pd.DataFrame(validation_rules)
        validation_df.to_excel(writer, sheet_name='Validation_Rules', index=False)
    
    print(f"Created sample Excel configuration: {excel_path}")
    return str(excel_path)


def create_sample_json_configs():
    """Create sample JSON configuration files."""
    configs_dir = Path("/workspace/data/sample_configs")
    configs_dir.mkdir(parents=True, exist_ok=True)
    
    # Database configuration
    db_config = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "username": "admin",
            "password": "secret123",
            "database": "myapp",
            "timeout": 30,
            "max_connections": 100,
            "ssl_enabled": True,
            "pool_size": 10
        },
        "logging": {
            "level": "INFO",
            "file": "/var/log/myapp.log",
            "max_size": "10MB",
            "backup_count": 5
        }
    }
    
    db_config_path = configs_dir / "database_config.json"
    with open(db_config_path, 'w') as f:
        json.dump(db_config, f, indent=2)
    
    # API configuration
    api_config = {
        "api": {
            "host": "0.0.0.0",
            "port": 8000,
            "debug": False,
            "cors_origins": ["http://localhost:3000"],
            "rate_limit": {
                "requests_per_minute": 100,
                "burst_size": 20
            }
        },
        "authentication": {
            "secret_key": "your-secret-key-here",
            "algorithm": "HS256",
            "access_token_expire_minutes": 30
        }
    }
    
    api_config_path = configs_dir / "api_config.json"
    with open(api_config_path, 'w') as f:
        json.dump(api_config, f, indent=2)
    
    # Redis configuration
    redis_config = {
        "redis": {
            "host": "localhost",
            "port": 6379,
            "password": None,
            "db": 0,
            "timeout": 5,
            "max_connections": 20
        }
    }
    
    redis_config_path = configs_dir / "redis_config.json"
    with open(redis_config_path, 'w') as f:
        json.dump(redis_config, f, indent=2)
    
    print(f"Created sample JSON configurations in: {configs_dir}")
    return [str(db_config_path), str(api_config_path), str(redis_config_path)]


def create_sample_yaml_configs():
    """Create sample YAML configuration files."""
    configs_dir = Path("/workspace/data/sample_configs")
    configs_dir.mkdir(parents=True, exist_ok=True)
    
    # Docker Compose configuration
    docker_compose = {
        "version": "3.8",
        "services": {
            "web": {
                "build": ".",
                "ports": ["8000:8000"],
                "environment": {
                    "DATABASE_URL": "postgresql://admin:secret123@db:5432/myapp",
                    "REDIS_URL": "redis://redis:6379/0"
                },
                "depends_on": ["db", "redis"]
            },
            "db": {
                "image": "postgres:13",
                "environment": {
                    "POSTGRES_DB": "myapp",
                    "POSTGRES_USER": "admin",
                    "POSTGRES_PASSWORD": "secret123"
                },
                "volumes": ["postgres_data:/var/lib/postgresql/data"]
            },
            "redis": {
                "image": "redis:6-alpine",
                "ports": ["6379:6379"]
            }
        },
        "volumes": {
            "postgres_data": {}
        }
    }
    
    docker_compose_path = configs_dir / "docker-compose.yml"
    with open(docker_compose_path, 'w') as f:
        yaml.dump(docker_compose, f, default_flow_style=False)
    
    # Kubernetes configuration
    k8s_config = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": "myapp-deployment",
            "labels": {
                "app": "myapp"
            }
        },
        "spec": {
            "replicas": 3,
            "selector": {
                "matchLabels": {
                    "app": "myapp"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": "myapp"
                    }
                },
                "spec": {
                    "containers": [{
                        "name": "myapp",
                        "image": "myapp:latest",
                        "ports": [{
                            "containerPort": 8000
                        }],
                        "env": [{
                            "name": "DATABASE_URL",
                            "value": "postgresql://admin:secret123@postgres:5432/myapp"
                        }]
                    }]
                }
            }
        }
    }
    
    k8s_config_path = configs_dir / "k8s-deployment.yaml"
    with open(k8s_config_path, 'w') as f:
        yaml.dump(k8s_config, f, default_flow_style=False)
    
    print(f"Created sample YAML configurations in: {configs_dir}")
    return [str(docker_compose_path), str(k8s_config_path)]


def create_sample_error_scenarios():
    """Create sample error scenarios for testing."""
    error_scenarios = [
        {
            "title": "Database Connection Timeout",
            "description": "Application cannot connect to database",
            "error_messages": [
                "Connection timeout after 30 seconds",
                "Unable to establish connection to database server",
                "Network unreachable"
            ],
            "configuration_context": {
                "host": "localhost",
                "port": 5432,
                "timeout": 30
            },
            "environment_info": {
                "os": "Linux",
                "database_version": "PostgreSQL 13"
            },
            "severity": "high"
        },
        {
            "title": "Invalid API Configuration",
            "description": "API endpoints returning 404 errors",
            "error_messages": [
                "404 Not Found",
                "Invalid endpoint configuration",
                "Route not found"
            ],
            "configuration_context": {
                "base_url": "https://api.example.com",
                "endpoints": ["/users", "/orders", "/products"]
            },
            "environment_info": {
                "framework": "FastAPI",
                "python_version": "3.9"
            },
            "severity": "medium"
        },
        {
            "title": "File Permission Error",
            "description": "Application cannot write to log files",
            "error_messages": [
                "Permission denied",
                "Cannot write to log file",
                "Access denied"
            ],
            "configuration_context": {
                "log_file": "/var/log/myapp.log",
                "log_level": "INFO"
            },
            "environment_info": {
                "os": "Linux",
                "user": "appuser"
            },
            "severity": "medium"
        }
    ]
    
    scenarios_dir = Path("/workspace/data/error_scenarios")
    scenarios_dir.mkdir(parents=True, exist_ok=True)
    
    for i, scenario in enumerate(error_scenarios, 1):
        scenario_path = scenarios_dir / f"scenario_{i}.json"
        with open(scenario_path, 'w') as f:
            json.dump(scenario, f, indent=2)
    
    print(f"Created {len(error_scenarios)} error scenarios in: {scenarios_dir}")
    return [str(scenarios_dir / f"scenario_{i}.json") for i in range(1, len(error_scenarios) + 1)]


def create_sample_validation_rules():
    """Create sample validation rules."""
    validation_rules = {
        "database_rules": [
            {
                "name": "required_fields",
                "description": "Check for required database fields",
                "rule_type": "custom",
                "custom_function": "check_required_fields",
                "severity": "error",
                "enabled": True
            },
            {
                "name": "port_range",
                "description": "Validate port numbers are in valid range",
                "rule_type": "regex",
                "pattern": r"^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$",
                "severity": "error",
                "enabled": True
            },
            {
                "name": "password_strength",
                "description": "Check password strength",
                "rule_type": "custom",
                "custom_function": "check_password_strength",
                "severity": "warning",
                "enabled": True
            }
        ],
        "api_rules": [
            {
                "name": "url_format",
                "description": "Validate URL format",
                "rule_type": "regex",
                "pattern": r"^https?://[^\s/$.?#].[^\s]*$",
                "severity": "error",
                "enabled": True
            },
            {
                "name": "rate_limit_validation",
                "description": "Validate rate limit configuration",
                "rule_type": "custom",
                "custom_function": "validate_rate_limits",
                "severity": "warning",
                "enabled": True
            }
        ]
    }
    
    rules_dir = Path("/workspace/data/validation_rules")
    rules_dir.mkdir(parents=True, exist_ok=True)
    
    for rule_set_name, rules in validation_rules.items():
        rules_path = rules_dir / f"{rule_set_name}.json"
        with open(rules_path, 'w') as f:
            json.dump(rules, f, indent=2)
    
    print(f"Created validation rules in: {rules_dir}")
    return [str(rules_dir / f"{rule_set_name}.json") for rule_set_name in validation_rules.keys()]


def main():
    """Create all sample configurations and data."""
    print("Creating sample configurations and data...")
    print("=" * 50)
    
    # Create sample files
    excel_path = create_sample_excel_config()
    json_paths = create_sample_json_configs()
    yaml_paths = create_sample_yaml_configs()
    error_scenarios = create_sample_error_scenarios()
    validation_rules = create_sample_validation_rules()
    
    print("\nSample files created:")
    print(f"- Excel configuration: {excel_path}")
    print(f"- JSON configurations: {len(json_paths)} files")
    print(f"- YAML configurations: {len(yaml_paths)} files")
    print(f"- Error scenarios: {len(error_scenarios)} files")
    print(f"- Validation rules: {len(validation_rules)} files")
    
    print("\nYou can now use these sample files to test the system!")


if __name__ == "__main__":
    main()