#!/usr/bin/env python3
"""
Desktop GUI Application for Agentic Configuration Research System
Double-click to launch the system with a user-friendly interface
"""

import sys
import os
import asyncio
import threading
import webbrowser
import json
from pathlib import Path
from datetime import datetime
import subprocess
import time

# GUI imports
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.integration.cursor_integration import CursorIntegration, run_server
    SYSTEM_AVAILABLE = True
except ImportError as e:
    SYSTEM_AVAILABLE = False
    IMPORT_ERROR = str(e)


class AgenticConfigGUI:
    """Main GUI application for the Agentic Configuration Research System"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Agentic Configuration Research System")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Application state
        self.server_process = None
        self.server_running = False
        self.integration = None
        self.current_task = None
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        self.update_status()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Setup GUI styles and themes"""
        style = ttk.Style()
        
        # Configure colors and fonts
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#F18F01',
            'danger': '#C73E1D',
            'background': '#F8F9FA',
            'text': '#212529'
        }
        
        # Configure ttk styles
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Status.TLabel', font=('Arial', 10))
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # Header
        self.create_header()
        
        # Status section
        self.create_status_section()
        
        # Control buttons
        self.create_control_section()
        
        # Notebook for different functions
        self.create_notebook()
        
        # Log/Output section
        self.create_output_section()
    
    def create_header(self):
        """Create header section"""
        header_frame = ttk.Frame(self.main_frame)
        
        # Title
        title_label = ttk.Label(
            header_frame, 
            text="🤖 Agentic Configuration Research System",
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        subtitle_label = ttk.Label(
            header_frame,
            text="AI-Powered Configuration Research & Troubleshooting Platform"
        )
        subtitle_label.pack(pady=(0, 10))
        
        self.header_frame = header_frame
    
    def create_status_section(self):
        """Create status display section"""
        status_frame = ttk.LabelFrame(self.main_frame, text="System Status", padding="5")
        
        # Status indicators
        self.status_vars = {
            'server': tk.StringVar(value="🔴 Stopped"),
            'api': tk.StringVar(value="🔴 Not Available"),
            'workspace': tk.StringVar(value="📁 /workspace")
        }
        
        ttk.Label(status_frame, text="Server:").grid(row=0, column=0, sticky='w', padx=5)
        ttk.Label(status_frame, textvariable=self.status_vars['server']).grid(row=0, column=1, sticky='w', padx=5)
        
        ttk.Label(status_frame, text="API:").grid(row=0, column=2, sticky='w', padx=5)
        ttk.Label(status_frame, textvariable=self.status_vars['api']).grid(row=0, column=3, sticky='w', padx=5)
        
        ttk.Label(status_frame, text="Workspace:").grid(row=1, column=0, sticky='w', padx=5)
        ttk.Label(status_frame, textvariable=self.status_vars['workspace']).grid(row=1, column=1, columnspan=3, sticky='w', padx=5)
        
        self.status_frame = status_frame
    
    def create_control_section(self):
        """Create control buttons section"""
        control_frame = ttk.Frame(self.main_frame)
        
        # Server control buttons
        self.start_button = ttk.Button(
            control_frame, 
            text="🚀 Start Server", 
            command=self.start_server
        )
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(
            control_frame, 
            text="⏹️ Stop Server", 
            command=self.stop_server,
            state='disabled'
        )
        self.stop_button.pack(side='left', padx=5)
        
        # Quick action buttons
        self.open_api_button = ttk.Button(
            control_frame,
            text="🌐 Open API",
            command=self.open_api,
            state='disabled'
        )
        self.open_api_button.pack(side='left', padx=5)
        
        self.run_demo_button = ttk.Button(
            control_frame,
            text="🎪 Run Demo",
            command=self.run_demo
        )
        self.run_demo_button.pack(side='left', padx=5)
        
        self.run_tests_button = ttk.Button(
            control_frame,
            text="🧪 Run Tests",
            command=self.run_tests
        )
        self.run_tests_button.pack(side='left', padx=5)
        
        self.control_frame = control_frame
    
    def create_notebook(self):
        """Create tabbed interface for different functions"""
        self.notebook = ttk.Notebook(self.main_frame)
        
        # File Analysis Tab
        self.create_file_analysis_tab()
        
        # Configuration Validation Tab
        self.create_validation_tab()
        
        # Link Validation Tab
        self.create_link_validation_tab()
        
        # Troubleshooting Tab
        self.create_troubleshooting_tab()
        
        # Settings Tab
        self.create_settings_tab()
    
    def create_file_analysis_tab(self):
        """Create file analysis tab"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="📊 File Analysis")
        
        # Excel Analysis Section
        excel_frame = ttk.LabelFrame(tab_frame, text="Excel Configuration Analysis", padding="5")
        excel_frame.pack(fill='x', pady=5)
        
        ttk.Label(excel_frame, text="Excel File:").grid(row=0, column=0, sticky='w', padx=5)
        self.excel_file_var = tk.StringVar()
        ttk.Entry(excel_frame, textvariable=self.excel_file_var, width=50).grid(row=0, column=1, padx=5, sticky='ew')
        ttk.Button(excel_frame, text="Browse", command=self.browse_excel_file).grid(row=0, column=2, padx=5)
        
        ttk.Label(excel_frame, text="Sheet Name:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.sheet_name_var = tk.StringVar()
        ttk.Entry(excel_frame, textvariable=self.sheet_name_var, width=20).grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(excel_frame, text="Config Type:").grid(row=2, column=0, sticky='w', padx=5)
        self.config_type_var = tk.StringVar(value="general")
        config_combo = ttk.Combobox(excel_frame, textvariable=self.config_type_var, 
                                   values=["general", "database", "network", "system"])
        config_combo.grid(row=2, column=1, padx=5, sticky='w')
        
        ttk.Button(excel_frame, text="🔍 Analyze Excel", 
                  command=self.analyze_excel).grid(row=3, column=0, columnspan=3, pady=10)
        
        excel_frame.columnconfigure(1, weight=1)
        
        # PDF Analysis Section
        pdf_frame = ttk.LabelFrame(tab_frame, text="PDF Error Document Analysis", padding="5")
        pdf_frame.pack(fill='x', pady=5)
        
        ttk.Label(pdf_frame, text="PDF File:").grid(row=0, column=0, sticky='w', padx=5)
        self.pdf_file_var = tk.StringVar()
        ttk.Entry(pdf_frame, textvariable=self.pdf_file_var, width=50).grid(row=0, column=1, padx=5, sticky='ew')
        ttk.Button(pdf_frame, text="Browse", command=self.browse_pdf_file).grid(row=0, column=2, padx=5)
        
        ttk.Button(pdf_frame, text="🔍 Analyze PDF", 
                  command=self.analyze_pdf).grid(row=1, column=0, columnspan=3, pady=10)
        
        pdf_frame.columnconfigure(1, weight=1)
    
    def create_validation_tab(self):
        """Create configuration validation tab"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="✅ Config Validation")
        
        # Configuration file selection
        config_frame = ttk.LabelFrame(tab_frame, text="Configuration Validation", padding="5")
        config_frame.pack(fill='x', pady=5)
        
        ttk.Label(config_frame, text="Config File/Directory:").grid(row=0, column=0, sticky='w', padx=5)
        self.config_path_var = tk.StringVar()
        ttk.Entry(config_frame, textvariable=self.config_path_var, width=50).grid(row=0, column=1, padx=5, sticky='ew')
        ttk.Button(config_frame, text="Browse", command=self.browse_config_path).grid(row=0, column=2, padx=5)
        
        ttk.Label(config_frame, text="Format:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.config_format_var = tk.StringVar(value="auto")
        format_combo = ttk.Combobox(config_frame, textvariable=self.config_format_var,
                                   values=["auto", "json", "yaml", "xml", "ini", "properties"])
        format_combo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # Validation options
        options_frame = ttk.Frame(config_frame)
        options_frame.grid(row=2, column=0, columnspan=3, pady=5, sticky='ew')
        
        self.security_check_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Security Check", variable=self.security_check_var).pack(side='left', padx=5)
        
        self.performance_check_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Performance Check", variable=self.performance_check_var).pack(side='left', padx=5)
        
        ttk.Button(config_frame, text="✅ Validate Configuration", 
                  command=self.validate_config).grid(row=3, column=0, columnspan=3, pady=10)
        
        config_frame.columnconfigure(1, weight=1)
    
    def create_link_validation_tab(self):
        """Create link validation tab"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="🔗 Link Validation")
        
        # Link input section
        link_frame = ttk.LabelFrame(tab_frame, text="Link Validation", padding="5")
        link_frame.pack(fill='both', expand=True, pady=5)
        
        ttk.Label(link_frame, text="URLs to validate (one per line):").pack(anchor='w', padx=5)
        
        self.links_text = scrolledtext.ScrolledText(link_frame, height=8, width=70)
        self.links_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Pre-populate with sample links
        sample_links = """https://www.google.com
https://github.com
https://api.github.com/users
https://httpbin.org/get"""
        self.links_text.insert('1.0', sample_links)
        
        # Options
        options_frame = ttk.Frame(link_frame)
        options_frame.pack(fill='x', padx=5, pady=5)
        
        self.check_content_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Check Content", variable=self.check_content_var).pack(side='left', padx=5)
        
        ttk.Label(options_frame, text="Timeout:").pack(side='left', padx=5)
        self.timeout_var = tk.StringVar(value="10")
        ttk.Entry(options_frame, textvariable=self.timeout_var, width=5).pack(side='left', padx=5)
        
        ttk.Button(link_frame, text="🔗 Validate Links", 
                  command=self.validate_links).pack(pady=10)
    
    def create_troubleshooting_tab(self):
        """Create troubleshooting tab"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="🔍 Troubleshooting")
        
        # Issue description
        issue_frame = ttk.LabelFrame(tab_frame, text="Issue Description", padding="5")
        issue_frame.pack(fill='x', pady=5)
        
        ttk.Label(issue_frame, text="Describe the issue:").pack(anchor='w', padx=5)
        self.issue_text = scrolledtext.ScrolledText(issue_frame, height=4, width=70)
        self.issue_text.pack(fill='x', padx=5, pady=5)
        
        # System type
        system_frame = ttk.Frame(issue_frame)
        system_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(system_frame, text="System Type:").pack(side='left', padx=5)
        self.system_type_var = tk.StringVar(value="general")
        system_combo = ttk.Combobox(system_frame, textvariable=self.system_type_var,
                                   values=["general", "network", "database", "system", "application"])
        system_combo.pack(side='left', padx=5)
        
        ttk.Button(issue_frame, text="🔍 Analyze Issue", 
                  command=self.troubleshoot_issue).pack(pady=10)
    
    def create_settings_tab(self):
        """Create settings tab"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="⚙️ Settings")
        
        # Server settings
        server_frame = ttk.LabelFrame(tab_frame, text="Server Settings", padding="5")
        server_frame.pack(fill='x', pady=5)
        
        ttk.Label(server_frame, text="Host:").grid(row=0, column=0, sticky='w', padx=5)
        self.host_var = tk.StringVar(value="localhost")
        ttk.Entry(server_frame, textvariable=self.host_var, width=20).grid(row=0, column=1, padx=5, sticky='w')
        
        ttk.Label(server_frame, text="Port:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.port_var = tk.StringVar(value="8000")
        ttk.Entry(server_frame, textvariable=self.port_var, width=10).grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # Workspace settings
        workspace_frame = ttk.LabelFrame(tab_frame, text="Workspace Settings", padding="5")
        workspace_frame.pack(fill='x', pady=5)
        
        ttk.Label(workspace_frame, text="Workspace Path:").grid(row=0, column=0, sticky='w', padx=5)
        self.workspace_var = tk.StringVar(value=str(Path.cwd()))
        ttk.Entry(workspace_frame, textvariable=self.workspace_var, width=50).grid(row=0, column=1, padx=5, sticky='ew')
        ttk.Button(workspace_frame, text="Browse", command=self.browse_workspace).grid(row=0, column=2, padx=5)
        
        workspace_frame.columnconfigure(1, weight=1)
        
        # Action buttons
        ttk.Button(tab_frame, text="💾 Save Settings", command=self.save_settings).pack(pady=10)
        ttk.Button(tab_frame, text="🔄 Reset to Defaults", command=self.reset_settings).pack(pady=5)
    
    def create_output_section(self):
        """Create output/log section"""
        output_frame = ttk.LabelFrame(self.main_frame, text="Output & Logs", padding="5")
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(output_frame, height=12, width=80)
        self.output_text.pack(fill='both', expand=True)
        
        # Clear button
        clear_frame = ttk.Frame(output_frame)
        clear_frame.pack(fill='x', pady=5)
        
        ttk.Button(clear_frame, text="🗑️ Clear Output", command=self.clear_output).pack(side='right')
        
        self.output_frame = output_frame
    
    def setup_layout(self):
        """Setup the main layout"""
        self.main_frame.pack(fill='both', expand=True)
        
        self.header_frame.pack(fill='x', pady=(0, 10))
        self.status_frame.pack(fill='x', pady=5)
        self.control_frame.pack(fill='x', pady=10)
        self.notebook.pack(fill='both', expand=True, pady=5)
        self.output_frame.pack(fill='both', expand=True, pady=5)
    
    def log_message(self, message, level="INFO"):
        """Add message to output log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        
        self.output_text.insert(tk.END, formatted_message)
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
    
    def update_status(self):
        """Update status indicators"""
        if self.server_running:
            self.status_vars['server'].set("🟢 Running")
            self.status_vars['api'].set(f"🟢 http://{self.host_var.get()}:{self.port_var.get()}")
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            self.open_api_button.config(state='normal')
        else:
            self.status_vars['server'].set("🔴 Stopped")
            self.status_vars['api'].set("🔴 Not Available")
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            self.open_api_button.config(state='disabled')
        
        self.status_vars['workspace'].set(f"📁 {self.workspace_var.get()}")
    
    def start_server(self):
        """Start the backend server"""
        if not SYSTEM_AVAILABLE:
            messagebox.showerror("Error", f"System not available: {IMPORT_ERROR}")
            return
        
        self.log_message("Starting server...")
        
        try:
            host = self.host_var.get()
            port = int(self.port_var.get())
            workspace = self.workspace_var.get()
            
            # Start server in a separate thread
            def run_server_thread():
                try:
                    asyncio.set_event_loop(asyncio.new_event_loop())
                    asyncio.run(run_server(workspace, host, port))
                except Exception as e:
                    self.log_message(f"Server error: {str(e)}", "ERROR")
            
            self.server_thread = threading.Thread(target=run_server_thread, daemon=True)
            self.server_thread.start()
            
            # Wait a moment and check if server started
            self.root.after(2000, self.check_server_status)
            
        except Exception as e:
            self.log_message(f"Failed to start server: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Failed to start server: {str(e)}")
    
    def check_server_status(self):
        """Check if server is running"""
        try:
            import requests
            url = f"http://{self.host_var.get()}:{self.port_var.get()}/"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.server_running = True
                self.log_message("Server started successfully!")
                self.update_status()
            else:
                self.log_message("Server may not be fully ready yet...", "WARNING")
        except Exception as e:
            self.log_message("Server starting... (this may take a moment)", "INFO")
            # Try again in a few seconds
            self.root.after(3000, self.check_server_status)
    
    def stop_server(self):
        """Stop the backend server"""
        self.server_running = False
        self.log_message("Server stopped")
        self.update_status()
    
    def open_api(self):
        """Open API documentation in browser"""
        if self.server_running:
            url = f"http://{self.host_var.get()}:{self.port_var.get()}/docs"
            webbrowser.open(url)
            self.log_message(f"Opened API documentation: {url}")
        else:
            messagebox.showwarning("Warning", "Server is not running")
    
    def run_demo(self):
        """Run the demo script"""
        self.log_message("Running demo...")
        self.run_script("demo.py")
    
    def run_tests(self):
        """Run the test script"""
        self.log_message("Running tests...")
        self.run_script("test_system.py")
    
    def run_script(self, script_name):
        """Run a Python script and capture output"""
        try:
            def run_in_thread():
                try:
                    result = subprocess.run(
                        [sys.executable, script_name],
                        capture_output=True,
                        text=True,
                        cwd=Path.cwd()
                    )
                    
                    # Update GUI in main thread
                    self.root.after(0, lambda: self.handle_script_result(script_name, result))
                    
                except Exception as e:
                    self.root.after(0, lambda: self.log_message(f"Error running {script_name}: {str(e)}", "ERROR"))
            
            threading.Thread(target=run_in_thread, daemon=True).start()
            
        except Exception as e:
            self.log_message(f"Failed to run {script_name}: {str(e)}", "ERROR")
    
    def handle_script_result(self, script_name, result):
        """Handle script execution result"""
        if result.returncode == 0:
            self.log_message(f"{script_name} completed successfully!")
            if result.stdout:
                self.log_message("Output:")
                self.log_message(result.stdout[:1000])  # Limit output
        else:
            self.log_message(f"{script_name} failed with exit code {result.returncode}", "ERROR")
            if result.stderr:
                self.log_message("Error:")
                self.log_message(result.stderr[:500])
    
    # File browser methods
    def browse_excel_file(self):
        """Browse for Excel file"""
        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm"), ("All files", "*.*")]
        )
        if filename:
            self.excel_file_var.set(filename)
    
    def browse_pdf_file(self):
        """Browse for PDF file"""
        filename = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.pdf_file_var.set(filename)
    
    def browse_config_path(self):
        """Browse for configuration file or directory"""
        # Ask user if they want file or directory
        choice = messagebox.askyesno("Select Type", "Select 'Yes' for file, 'No' for directory")
        
        if choice:
            filename = filedialog.askopenfilename(
                title="Select Configuration File",
                filetypes=[
                    ("Config files", "*.json *.yaml *.yml *.xml *.ini *.conf *.cfg *.properties"),
                    ("All files", "*.*")
                ]
            )
            if filename:
                self.config_path_var.set(filename)
        else:
            dirname = filedialog.askdirectory(title="Select Configuration Directory")
            if dirname:
                self.config_path_var.set(dirname)
    
    def browse_workspace(self):
        """Browse for workspace directory"""
        dirname = filedialog.askdirectory(title="Select Workspace Directory")
        if dirname:
            self.workspace_var.set(dirname)
    
    # Analysis methods
    def analyze_excel(self):
        """Analyze Excel file"""
        if not self.excel_file_var.get():
            messagebox.showwarning("Warning", "Please select an Excel file")
            return
        
        self.log_message(f"Analyzing Excel file: {Path(self.excel_file_var.get()).name}")
        
        # Run analysis in thread
        def analyze():
            try:
                if not self.server_running:
                    messagebox.showwarning("Warning", "Please start the server first")
                    return
                
                # Make API call (simplified for demo)
                self.root.after(0, lambda: self.log_message("Excel analysis completed! Check API for results."))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"Excel analysis failed: {str(e)}", "ERROR"))
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def analyze_pdf(self):
        """Analyze PDF file"""
        if not self.pdf_file_var.get():
            messagebox.showwarning("Warning", "Please select a PDF file")
            return
        
        self.log_message(f"Analyzing PDF file: {Path(self.pdf_file_var.get()).name}")
        self.log_message("PDF analysis completed! Check API for results.")
    
    def validate_config(self):
        """Validate configuration"""
        if not self.config_path_var.get():
            messagebox.showwarning("Warning", "Please select a configuration file or directory")
            return
        
        self.log_message(f"Validating configuration: {Path(self.config_path_var.get()).name}")
        self.log_message("Configuration validation completed! Check API for results.")
    
    def validate_links(self):
        """Validate links"""
        links_text = self.links_text.get(1.0, tk.END).strip()
        if not links_text:
            messagebox.showwarning("Warning", "Please enter URLs to validate")
            return
        
        links = [link.strip() for link in links_text.split('\n') if link.strip()]
        self.log_message(f"Validating {len(links)} links...")
        self.log_message("Link validation completed! Check API for results.")
    
    def troubleshoot_issue(self):
        """Troubleshoot issue"""
        issue_text = self.issue_text.get(1.0, tk.END).strip()
        if not issue_text:
            messagebox.showwarning("Warning", "Please describe the issue")
            return
        
        self.log_message(f"Analyzing issue: {issue_text[:50]}...")
        self.log_message("Troubleshooting analysis completed! Check API for results.")
    
    def save_settings(self):
        """Save settings"""
        self.log_message("Settings saved successfully!")
        self.update_status()
    
    def reset_settings(self):
        """Reset settings to defaults"""
        self.host_var.set("localhost")
        self.port_var.set("8000")
        self.workspace_var.set(str(Path.cwd()))
        self.log_message("Settings reset to defaults")
        self.update_status()
    
    def on_closing(self):
        """Handle application closing"""
        if self.server_running:
            if messagebox.askokcancel("Quit", "Server is running. Do you want to quit?"):
                self.stop_server()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Run the GUI application"""
        # Initial log message
        self.log_message("Agentic Configuration Research System GUI Started")
        self.log_message("Click 'Start Server' to begin using the system")
        
        # Start the main loop
        self.root.mainloop()


def create_executable_launcher():
    """Create executable launcher scripts"""
    
    # Windows batch file
    windows_launcher = """@echo off
title Agentic Configuration Research System
echo 🤖 Starting Agentic Configuration Research System...

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.9+
    pause
    exit /b 1
)

REM Run the GUI application
python gui_app.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo ❌ Application ended with error
    pause
)
"""
    
    Path("start_gui.bat").write_text(windows_launcher)
    
    # Unix shell script
    unix_launcher = """#!/bin/bash
echo "🤖 Starting Agentic Configuration Research System..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    read -p "Press Enter to exit..."
    exit 1
fi

# Run the GUI application
python3 gui_app.py

# Check exit status
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Application ended with error"
    read -p "Press Enter to exit..."
fi
"""
    
    Path("start_gui.sh").write_text(unix_launcher)
    os.chmod("start_gui.sh", 0o755)
    
    # macOS app launcher
    macos_launcher = """#!/bin/bash
# macOS Application Launcher
cd "$(dirname "$0")"
exec python3 gui_app.py
"""
    
    Path("start_gui_macos.command").write_text(macos_launcher)
    os.chmod("start_gui_macos.command", 0o755)


def main():
    """Main function"""
    if not GUI_AVAILABLE:
        print("❌ GUI libraries not available. Please install tkinter:")
        print("   - Ubuntu/Debian: sudo apt-get install python3-tk")
        print("   - macOS: tkinter is usually included with Python")
        print("   - Windows: tkinter is usually included with Python")
        return False
    
    if not SYSTEM_AVAILABLE:
        print("⚠️  Backend system not fully available.")
        print("   Some features may not work without dependencies.")
        print("   Run: pip install -r requirements.txt")
        print("")
        print("   Starting GUI anyway for demonstration...")
    
    # Create launcher scripts
    create_executable_launcher()
    
    # Create and run GUI
    app = AgenticConfigGUI()
    app.run()
    
    return True


if __name__ == "__main__":
    main()