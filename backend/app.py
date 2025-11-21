from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import hashlib
import secrets
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'napkin'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

def get_db_connection():
    """Create and return a database connection"""
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

def init_db():
    """Initialize the database with the required schema"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id VARCHAR(32) PRIMARY KEY,
            content TEXT NOT NULL,
            password_hash VARCHAR(64),
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            expires_at TIMESTAMP,
            views INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

def hash_password(password):
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_note_id():
    """Generate a random note ID"""
    return secrets.token_urlsafe(16)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

@app.route('/api/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({'error': 'Content is required'}), 400
        
        note_id = generate_note_id()
        content = data['content']
        password = data.get('password')
        expire_hours = data.get('expire_hours')
        
        # Hash password if provided
        password_hash = hash_password(password) if password else None
        
        # Calculate expiry time
        expires_at = None
        if expire_hours:
            try:
                hours = int(expire_hours)
                expires_at = datetime.now() + timedelta(hours=hours)
            except (ValueError, TypeError):
                pass
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            '''INSERT INTO notes (id, content, password_hash, expires_at)
               VALUES (%s, %s, %s, %s)''',
            (note_id, content, password_hash, expires_at)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'id': note_id,
            'expires_at': expires_at.isoformat() if expires_at else None
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<note_id>', methods=['GET'])
def get_note(note_id):
    """Retrieve a note by ID"""
    try:
        password = request.args.get('password', '')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            'SELECT * FROM notes WHERE id = %s',
            (note_id,)
        )
        
        note = cur.fetchone()
        
        if not note:
            cur.close()
            conn.close()
            return jsonify({'error': 'Note not found'}), 404
        
        # Check if note has expired
        if note['expires_at'] and datetime.now() > note['expires_at']:
            cur.execute('DELETE FROM notes WHERE id = %s', (note_id,))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'error': 'Note has expired'}), 410
        
        # Check password if required
        if note['password_hash']:
            if not password or hash_password(password) != note['password_hash']:
                cur.close()
                conn.close()
                return jsonify({'error': 'Invalid password', 'requires_password': True}), 403
        
        # Increment view count
        cur.execute(
            'UPDATE notes SET views = views + 1 WHERE id = %s',
            (note_id,)
        )
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'id': note['id'],
            'content': note['content'],
            'created_at': note['created_at'].isoformat(),
            'expires_at': note['expires_at'].isoformat() if note['expires_at'] else None,
            'views': note['views'] + 1
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note by ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('DELETE FROM notes WHERE id = %s RETURNING id', (note_id,))
        deleted = cur.fetchone()
        
        conn.commit()
        cur.close()
        conn.close()
        
        if not deleted:
            return jsonify({'error': 'Note not found'}), 404
        
        return jsonify({'message': 'Note deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<note_id>/check', methods=['GET'])
def check_note(note_id):
    """Check if a note exists and if it requires a password"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            'SELECT id, password_hash, expires_at FROM notes WHERE id = %s',
            (note_id,)
        )
        
        note = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not note:
            return jsonify({'exists': False}), 404
        
        # Check if note has expired
        if note['expires_at'] and datetime.now() > note['expires_at']:
            return jsonify({'exists': False, 'expired': True}), 410
        
        return jsonify({
            'exists': True,
            'requires_password': bool(note['password_hash'])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
