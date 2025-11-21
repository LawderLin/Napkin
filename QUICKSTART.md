# Napkin Quick Start Guide

Get Napkin running in 5 minutes! ⚡

## Option 1: Docker (Easiest)

**Requirements**: Docker and Docker Compose installed

```bash
# Clone the repository
git clone https://github.com/LawderLin/Napkin.git
cd Napkin

# Start everything
docker-compose up -d

# Wait about 30 seconds for services to start, then visit:
# http://localhost:8080
```

That's it! Napkin is now running.

To stop:
```bash
docker-compose down
```

## Option 2: Manual Setup

**Requirements**: Python 3.11+, Node.js 18+, PostgreSQL 15+

### Step 1: Database Setup

```bash
# Create database
createdb napkin

# Or using psql
psql -U postgres
CREATE DATABASE napkin;
\q
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env if needed (default values work for local PostgreSQL)

# Initialize database
python init_db.py

# Start backend (in one terminal)
python app.py
```

Backend will run at `http://localhost:5000`

### Step 3: Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start frontend
npm run serve
```

Frontend will run at `http://localhost:8080`

### Step 4: Use Napkin!

Open your browser to `http://localhost:8080` and start creating notes!

## Using the Setup Script

For Unix-based systems (Linux/Mac):

```bash
chmod +x setup.sh
./setup.sh
```

This will guide you through the setup process.

## Testing the Installation

### Test Backend
```bash
cd backend
python test_app.py  # Unit tests
```

### Test API (with backend running)
```bash
cd backend
python test_api.py  # Integration tests
```

## Creating Your First Note

1. Visit `http://localhost:8080`
2. Type your note in the text area (Markdown supported!)
3. (Optional) Add a password
4. (Optional) Set expiration time
5. Click "Create Note"
6. Copy and share the generated link!

## Example Note

Try this in the editor:

```markdown
# My First Note 📝

This is a **test note** with *markdown* support!

## Features I Love:
- No login required
- Password protection
- Auto-expire
- Easy sharing

\`\`\`python
print("Hello, Napkin!")
\`\`\`
```

## Common Issues

### Port Already in Use

If port 8080 or 5000 is already in use:

**Backend**: Edit `backend/app.py` and change port 5000 to another port
**Frontend**: Edit `frontend/vue.config.js` and change port 8080 to another port

### Database Connection Failed

Make sure PostgreSQL is running:
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Start PostgreSQL if needed
sudo systemctl start postgresql
```

### Dependencies Installation Failed

Make sure you have the required versions:
```bash
python --version  # Should be 3.11+
node --version    # Should be 18+
psql --version    # Should be 15+
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [DEMO.md](DEMO.md) for usage examples
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Getting Help

- Check existing issues on GitHub
- Open a new issue if you find a bug
- Read the full documentation in README.md

Enjoy using Napkin! 🎉
