# Napkin 📝

A browser-based, no login required note taking tool, with functions like auto-expires, share, and password protect.

## Features

✨ **No Login Required** - Start taking notes immediately without any registration  
📝 **Markdown Support** - Write notes with full markdown syntax support  
🔒 **Password Protection** - Secure your notes with optional password protection  
⏰ **Auto-Expire** - Set automatic expiration times for your notes (1 hour to 30 days)  
🔗 **Easy Sharing** - Share notes via a simple URL  
👁️ **View Counter** - Track how many times your note has been viewed

## Tech Stack

- **Frontend**: Vue.js 3 with Vue Router
- **Backend**: Python Flask
- **Database**: PostgreSQL
- **Markdown**: Marked.js for rendering

## Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes
- **[Demo Guide](DEMO.md)** - Usage examples and features demonstration
- **[Deployment Guide](DEPLOYMENT.md)** - Production deployment instructions
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project

## Quick Start with Docker

The easiest way to run Napkin is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/LawderLin/Napkin.git
cd Napkin

# Start all services (use 'docker compose' or 'docker-compose' depending on your version)
docker compose up -d
# or: docker-compose up -d

# Access the application
# Frontend: http://localhost:8080
# Backend API: http://localhost:5000
```

## Manual Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

5. Create the PostgreSQL database:
```bash
createdb napkin
```

6. Run the backend server:
```bash
python app.py
```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run serve
```

The frontend will be available at `http://localhost:8080`

### Building for Production

Frontend:
```bash
cd frontend
npm run build
```

The built files will be in the `frontend/dist` directory.

## API Endpoints

### Create Note
```
POST /api/notes
Content-Type: application/json

{
  "content": "Your note content (markdown supported)",
  "password": "optional-password",
  "expire_hours": 24  // optional, in hours
}
```

### Get Note
```
GET /api/notes/:id?password=optional-password
```

### Check Note Status
```
GET /api/notes/:id/check
```

### Delete Note
```
DELETE /api/notes/:id
```

## Usage

1. **Create a Note**: 
   - Visit the homepage
   - Write your note (markdown supported)
   - Optionally add a password
   - Optionally set an expiration time
   - Click "Create Note"

2. **Share a Note**:
   - Copy the generated share link
   - Share it with anyone
   - Recipients can view the note without any login

3. **View a Note**:
   - Open the shared link
   - Enter password if required
   - View the rendered markdown or raw content

## Environment Variables

Backend (`.env` file):
```
DB_NAME=napkin
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

## Database Schema

```sql
CREATE TABLE notes (
    id VARCHAR(32) PRIMARY KEY,
    content TEXT NOT NULL,
    password_hash VARCHAR(128),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP,
    views INTEGER DEFAULT 0
);
```

## Security Features

- **Password Security**: Passwords are hashed using SHA256 with random salts (protects against rainbow table attacks)
- **Auto-Expiry**: Notes are automatically deleted when expired
- **Secure IDs**: Random URL-safe IDs generated for each note
- **CORS Protection**: CORS enabled on the backend for secure cross-origin requests
- **No Port Exposure**: PostgreSQL is not exposed outside Docker network

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
