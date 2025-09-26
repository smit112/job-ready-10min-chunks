"""
Configuration settings for the agentic AI configuration research system.
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Local Processing Only - No External APIs
    local_processing_only: bool = True
    
    # Database
    database_url: str = "sqlite:///./config_research.db"
    redis_url: str = "redis://localhost:6379"
    
    # File paths
    data_dir: str = "/workspace/data"
    configs_dir: str = "/workspace/configs"
    agents_dir: str = "/workspace/agents"
    utils_dir: str = "/workspace/utils"
    
    # Excel processing
    excel_templates_dir: str = "/workspace/data/excel_templates"
    excel_output_dir: str = "/workspace/data/excel_output"
    
    # PDF processing
    pdf_docs_dir: str = "/workspace/data/pdf_docs"
    pdf_errors_dir: str = "/workspace/data/pdf_errors"
    
    # Link analysis
    link_cache_dir: str = "/workspace/data/link_cache"
    max_link_depth: int = 3
    link_timeout: int = 30
    
    # Local Processing settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = ['.xlsx', '.xls', '.pdf', '.json', '.yaml', '.yml', '.txt']
    
    # Validation settings
    validation_timeout: int = 60
    max_validation_attempts: int = 3
    
    # Dashboard settings
    dashboard_host: str = "0.0.0.0"
    dashboard_port: int = 8000
    debug: bool = False
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "/workspace/logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Create necessary directories
os.makedirs(settings.data_dir, exist_ok=True)
os.makedirs(settings.excel_templates_dir, exist_ok=True)
os.makedirs(settings.excel_output_dir, exist_ok=True)
os.makedirs(settings.pdf_docs_dir, exist_ok=True)
os.makedirs(settings.pdf_errors_dir, exist_ok=True)
os.makedirs(settings.link_cache_dir, exist_ok=True)
os.makedirs("/workspace/logs", exist_ok=True)