#!/usr/bin/env python3
"""
Simple Desktop Launcher for Agentic Configuration Research System
Works without GUI dependencies - opens web interface in browser
"""

import sys
import os
import subprocess
import time
import webbrowser
import threading
from pathlib import Path


class SimpleLauncher:
    """Simple launcher that starts the server and opens the web interface"""
    
    def __init__(self):
        self.server_process = None
        self.workspace = Path.cwd()
        self.host = "localhost"
        self.port = 8000
        
    def check_python(self):
        """Check if Python is available"""
        try:
            result = subprocess.run([sys.executable, "--version"], 
                                  capture_output=True, text=True)
            print(f"✅ Python found: {result.stdout.strip()}")
            return True
        except Exception as e:
            print(f"❌ Python check failed: {e}")
            return False
    
    def check_dependencies(self):
        """Check if basic dependencies are available"""
        try:
            # Try to import basic modules
            import json
            import asyncio
            print("✅ Basic modules available")
            
            # Check if our system modules can be imported
            sys.path.insert(0, str(self.workspace / "src"))
            try:
                from src.mcp_server.server import MCPServer
                print("✅ MCP server module available")
                return True
            except ImportError as e:
                print(f"⚠️  Some dependencies missing: {e}")
                print("   The system will work with basic functionality")
                return False
                
        except Exception as e:
            print(f"❌ Dependency check failed: {e}")
            return False
    
    def start_server(self):
        """Start the backend server"""
        print(f"🚀 Starting server on {self.host}:{self.port}...")
        
        try:
            # Start the main server
            cmd = [sys.executable, "main.py", "server", 
                   "--host", self.host, "--port", str(self.port)]
            
            self.server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.workspace
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def wait_for_server(self, timeout=30):
        """Wait for server to be ready"""
        print("⏳ Waiting for server to be ready...")
        
        for i in range(timeout):
            try:
                import urllib.request
                url = f"http://{self.host}:{self.port}/"
                
                with urllib.request.urlopen(url, timeout=2) as response:
                    if response.status == 200:
                        print("✅ Server is ready!")
                        return True
                        
            except Exception:
                time.sleep(1)
                if i % 5 == 0:
                    print(f"   Still waiting... ({i}/{timeout}s)")
        
        print("⚠️  Server may not be fully ready yet")
        return False
    
    def open_browser(self):
        """Open the web interface in browser"""
        url = f"http://{self.host}:{self.port}"
        docs_url = f"http://{self.host}:{self.port}/docs"
        
        print(f"🌐 Opening web interface: {url}")
        
        try:
            webbrowser.open(url)
            time.sleep(2)
            print(f"📚 API Documentation: {docs_url}")
            
            # Ask if user wants to open docs too
            return True
            
        except Exception as e:
            print(f"❌ Could not open browser: {e}")
            print(f"   Please manually open: {url}")
            return False
    
    def show_menu(self):
        """Show interactive menu"""
        while True:
            print("\n" + "="*50)
            print("🤖 Agentic Configuration Research System")
            print("="*50)
            print("1. 🌐 Open Web Interface")
            print("2. 📚 Open API Documentation") 
            print("3. 🧪 Run Tests")
            print("4. 🎪 Run Demo")
            print("5. 📊 System Status")
            print("6. ❌ Exit")
            print("="*50)
            
            try:
                choice = input("Select option (1-6): ").strip()
                
                if choice == "1":
                    self.open_browser()
                elif choice == "2":
                    webbrowser.open(f"http://{self.host}:{self.port}/docs")
                elif choice == "3":
                    self.run_script("test_system.py")
                elif choice == "4":
                    self.run_script("demo.py")
                elif choice == "5":
                    self.show_status()
                elif choice == "6":
                    break
                else:
                    print("❌ Invalid choice")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def run_script(self, script_name):
        """Run a Python script"""
        print(f"🔄 Running {script_name}...")
        
        try:
            result = subprocess.run([sys.executable, script_name], 
                                  cwd=self.workspace, timeout=60)
            if result.returncode == 0:
                print(f"✅ {script_name} completed successfully")
            else:
                print(f"⚠️  {script_name} finished with warnings")
                
        except subprocess.TimeoutExpired:
            print(f"⚠️  {script_name} timed out")
        except Exception as e:
            print(f"❌ Error running {script_name}: {e}")
    
    def show_status(self):
        """Show system status"""
        print("\n📊 System Status:")
        print("-" * 30)
        
        # Check server
        try:
            import urllib.request
            url = f"http://{self.host}:{self.port}/"
            with urllib.request.urlopen(url, timeout=2) as response:
                print(f"🟢 Server: Running on {url}")
        except:
            print(f"🔴 Server: Not responding on {self.host}:{self.port}")
        
        # Check files
        important_files = [
            "main.py", "gui_app.py", "src/", "config/", "data/"
        ]
        
        for file_path in important_files:
            path = self.workspace / file_path
            if path.exists():
                print(f"✅ {file_path}: Present")
            else:
                print(f"❌ {file_path}: Missing")
    
    def cleanup(self):
        """Cleanup resources"""
        if self.server_process:
            print("🛑 Stopping server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
    
    def run(self):
        """Run the launcher"""
        print("🚀 Agentic Configuration Research System Launcher")
        print("=" * 55)
        
        try:
            # Check prerequisites
            if not self.check_python():
                input("Press Enter to exit...")
                return False
            
            self.check_dependencies()
            
            # Start server
            if not self.start_server():
                input("Press Enter to exit...")
                return False
            
            # Wait for server and open browser
            if self.wait_for_server():
                self.open_browser()
            
            # Show interactive menu
            self.show_menu()
            
            return True
            
        except KeyboardInterrupt:
            print("\n❌ Cancelled by user")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        finally:
            self.cleanup()


def main():
    """Main function"""
    launcher = SimpleLauncher()
    success = launcher.run()
    
    print("\n👋 Thank you for using Agentic Configuration Research System!")
    if not success:
        input("Press Enter to exit...")
    
    return success


if __name__ == "__main__":
    main()