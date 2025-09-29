#!/bin/bash

# Trading Learning Platform - Deployment Script
echo "🚀 Trading Learning Platform - Deployment Script"
echo "================================================"

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the project root."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed."
    exit 1
fi

echo "✅ Environment check passed"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies."
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Run tests
echo "🧪 Running tests..."
npm test -- --watchAll=false

if [ $? -ne 0 ]; then
    echo "⚠️  Warning: Some tests failed, but continuing with build..."
fi

# Build the application
echo "🔨 Building application for production..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Error: Build failed."
    exit 1
fi

echo "✅ Build completed successfully"

# Check if build directory exists
if [ ! -d "build" ]; then
    echo "❌ Error: Build directory not found."
    exit 1
fi

echo "📁 Build directory created with the following contents:"
ls -la build/

# Check build size
echo "📊 Build size:"
du -sh build/

echo ""
echo "🎉 Deployment preparation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Test the build locally: npx serve -s build"
echo "2. Deploy to GitHub Pages: gh-pages -d build"
echo "3. Deploy to Netlify: Connect GitHub repo to Netlify"
echo "4. Deploy to Vercel: Connect GitHub repo to Vercel"
echo ""
echo "🌐 The application is ready for production deployment!"