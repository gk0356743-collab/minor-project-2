#!/bin/bash

# Student Marks Analysis - Streamlit App Launcher

echo "🚀 Starting Student Marks Analysis Dashboard..."
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

echo "✓ Dependencies installed"
echo ""
echo "🎯 Launching Streamlit app..."
echo ""
echo "App will be available at: http://localhost:8501"
echo "Press Ctrl+C to stop the app"
echo ""

streamlit run streamlit_app.py
