#!/bin/bash

# Veera Vaanji Martial Arts Academy - Flask Application Startup Script

echo "========================================="
echo "Veera Vaanji Martial Arts Academy"
echo "Flask Application Startup"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3."
    exit 1
fi

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "🗄️  Initializing database..."
python3 -c "from database import create_database; create_database()"

# Run the Flask application
echo ""
echo "========================================="
echo "✨ Starting Flask Application..."
echo "========================================="
echo "🚀 Application will be available at:"
echo "   http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================="
echo ""

python3 app.py
