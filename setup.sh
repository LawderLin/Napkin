#!/bin/bash

# Napkin Setup Script
# This script helps set up the Napkin note-taking application

set -e

echo "🚀 Napkin Setup Script"
echo "======================"
echo ""

# Check if Docker is installed
if command -v docker &> /dev/null; then
    # Check for docker compose (new) or docker-compose (legacy)
    if docker compose version &> /dev/null; then
        DOCKER_COMPOSE="docker compose"
    elif command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE="docker-compose"
    else
        echo "Docker is installed but Docker Compose is not found."
        echo "Please install Docker Compose."
        DOCKER_COMPOSE=""
    fi
    
    if [ -n "$DOCKER_COMPOSE" ]; then
        echo "✓ Docker and Docker Compose are installed"
        echo ""
        echo "Starting Napkin with Docker..."
        echo ""
        $DOCKER_COMPOSE up -d
        echo ""
        echo "✅ Napkin is running!"
        echo ""
        echo "Frontend: http://localhost:8080"
        echo "Backend API: http://localhost:5000"
        echo ""
        echo "To stop: $DOCKER_COMPOSE down"
        exit 0
    fi
fi

echo "Docker not found. Setting up manually..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi
echo "✓ Python 3 is installed"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi
echo "✓ Node.js is installed"

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL client is not installed. Please install PostgreSQL 15 or higher."
    echo "You can still continue, but you'll need to set up PostgreSQL manually."
fi

echo ""
echo "Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Created Python virtual environment"
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
echo "✓ Installed Python dependencies"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file"
fi

cd ..

echo ""
echo "Setting up frontend..."
cd frontend

# Install Node.js dependencies
npm install
echo "✓ Installed Node.js dependencies"

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure PostgreSQL is running and create a database named 'napkin'"
echo "   createdb napkin"
echo ""
echo "2. Start the backend (in one terminal):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "3. Start the frontend (in another terminal):"
echo "   cd frontend"
echo "   npm run serve"
echo ""
echo "4. Open your browser to http://localhost:8080"
