#!/bin/bash
# macOS Application Launcher - Double-click to run
cd "$(dirname "$0")"

echo "🤖 Agentic Configuration Research System"
echo "=========================================="
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    echo "   Download from: https://python.org"
    echo "   Or install with Homebrew: brew install python"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ Starting GUI application..."
echo
python3 gui_app.py

# Check exit status
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Application ended with error"
    read -p "Press Enter to exit..."
fi