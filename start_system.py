#!/usr/bin/env python3
"""
Startup script for the Agentic AI Configuration Research System.
This script initializes and starts all system components.
"""
import asyncio
import logging
import sys
from pathlib import Path
import subprocess
import time
import signal
import os

# Add workspace to Python path
sys.path.append('/workspace')

from configs.settings import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class SystemManager:
    """Manages the startup and shutdown of system components."""
    
    def __init__(self):
        self.processes = []
        self.running = False
    
    def start_dashboard(self):
        """Start the web dashboard."""
        try:
            logger.info("Starting web dashboard...")
            
            # Change to dashboard directory
            dashboard_dir = Path("/workspace/dashboard")
            
            # Start the dashboard
            process = subprocess.Popen([
                sys.executable, "app.py"
            ], cwd=dashboard_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes.append(("dashboard", process))
            logger.info(f"Dashboard started with PID {process.pid}")
            
            # Wait a moment for startup
            time.sleep(2)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start dashboard: {e}")
            return False
    
    def check_dependencies(self):
        """Check if all required dependencies are installed."""
        logger.info("Checking dependencies...")
        
        required_packages = [
            "fastapi", "uvicorn", "pandas", "openpyxl", "PyPDF2",
            "requests", "beautifulsoup4", "aiohttp", "pydantic"
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            logger.error(f"Missing required packages: {', '.join(missing_packages)}")
            logger.error("Please install them using: pip install -r requirements.txt")
            return False
        
        logger.info("All required dependencies are installed")
        return True
    
    def create_directories(self):
        """Create necessary directories."""
        logger.info("Creating necessary directories...")
        
        directories = [
            settings.data_dir,
            settings.excel_templates_dir,
            settings.excel_output_dir,
            settings.pdf_docs_dir,
            settings.pdf_errors_dir,
            settings.link_cache_dir,
            "/workspace/logs",
            "/workspace/data/uploads",
            "/workspace/dashboard/static",
            "/workspace/dashboard/templates"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created directory: {directory}")
        
        logger.info("All directories created successfully")
    
    def initialize_components(self):
        """Initialize system components."""
        logger.info("Initializing system components...")
        
        try:
            # Import and initialize components
            from agents.config_research_agent import ConfigResearchAgent
            from agents.troubleshooting_ai import TroubleshootingAI
            from utils.validation_engine import ValidationEngine
            
            # Initialize components
            config_agent = ConfigResearchAgent()
            troubleshooting_ai = TroubleshootingAI()
            validation_engine = ValidationEngine()
            
            logger.info("System components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            return False
    
    def start_system(self):
        """Start the entire system."""
        logger.info("Starting Agentic AI Configuration Research System...")
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Create directories
        self.create_directories()
        
        # Initialize components
        if not self.initialize_components():
            return False
        
        # Start dashboard
        if not self.start_dashboard():
            return False
        
        self.running = True
        logger.info("System started successfully!")
        logger.info(f"Dashboard available at: http://{settings.dashboard_host}:{settings.dashboard_port}")
        logger.info("Press Ctrl+C to stop the system")
        
        return True
    
    def stop_system(self):
        """Stop all system components."""
        logger.info("Stopping system components...")
        
        for name, process in self.processes:
            try:
                logger.info(f"Stopping {name} (PID: {process.pid})")
                process.terminate()
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning(f"Force killing {name}")
                process.kill()
            except Exception as e:
                logger.error(f"Error stopping {name}: {e}")
        
        self.processes.clear()
        self.running = False
        logger.info("System stopped")
    
    def run(self):
        """Run the system with signal handling."""
        def signal_handler(signum, frame):
            logger.info("Received shutdown signal")
            self.stop_system()
            sys.exit(0)
        
        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start the system
        if not self.start_system():
            logger.error("Failed to start system")
            sys.exit(1)
        
        try:
            # Keep the system running
            while self.running:
                time.sleep(1)
                
                # Check if processes are still running
                for name, process in self.processes[:]:
                    if process.poll() is not None:
                        logger.error(f"{name} process died unexpectedly")
                        self.processes.remove((name, process))
                        
                        # Restart dashboard if it died
                        if name == "dashboard":
                            logger.info("Restarting dashboard...")
                            if self.start_dashboard():
                                logger.info("Dashboard restarted successfully")
                            else:
                                logger.error("Failed to restart dashboard")
                                self.running = False
                                break
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        finally:
            self.stop_system()


def main():
    """Main entry point."""
    print("Agentic AI Configuration Research System")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("/workspace").exists():
        print("Error: /workspace directory not found")
        print("Please run this script from the correct directory")
        sys.exit(1)
    
    # Create and run system manager
    system_manager = SystemManager()
    system_manager.run()


if __name__ == "__main__":
    main()