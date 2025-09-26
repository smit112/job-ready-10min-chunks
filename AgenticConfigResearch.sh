#!/bin/bash

# Change to script directory
cd "$(dirname "$0")"

# Set terminal title
echo -e "\033]0;Agentic Configuration Research System\007"

# Clear screen and show header
clear
echo "
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @                                                                        @
    @           🤖 AGENTIC CONFIGURATION RESEARCH SYSTEM 🤖                @
    @                                                                        @
    @                   AI-Powered Configuration Research                   @
    @                        & Troubleshooting Platform                     @
    @                                                                        @
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    Starting system...
"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "    ❌ Python 3 not found!"
    echo "    Please install Python 3.9+ from your package manager"
    echo "    Ubuntu/Debian: sudo apt-get install python3"
    echo "    macOS: brew install python3 or download from python.org"
    echo ""
    read -p "    Press Enter to exit..."
    exit 1
fi

# Run the simple launcher
echo "    ✅ Python found, starting application..."
echo ""
python3 simple_launcher.py

# Pause on exit
echo ""
read -p "Press Enter to exit..."