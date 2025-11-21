# Security Policy

## Supported Versions

We currently support the latest version of Napkin with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Features

### Current Implementation

1. **Password Hashing**: SHA256 with random salts
   - Protects against rainbow table attacks
   - Each password gets a unique 16-byte salt
   - Salt and hash stored together in format: `salt:hash`

2. **Auto-Expiry**: Time-based note deletion
   - Notes automatically deleted when expired
   - Checked on every access attempt
   - Prevents long-term data exposure

3. **Secure IDs**: URL-safe random identifiers
   - Uses `secrets.token_urlsafe()` for cryptographically secure random IDs
   - 16-byte entropy makes IDs virtually unguessable

4. **Database Security**:
   - PostgreSQL not exposed outside Docker network
   - Connection credentials via environment variables
   - SQL injection protection via parameterized queries

5. **CORS Protection**: Configured on backend to prevent unauthorized cross-origin requests

6. **Modern Clipboard API**: Uses secure Clipboard API with proper fallbacks

### Production Security Recommendations

For production deployments requiring enhanced security, we recommend:

#### 1. Use Stronger Password Hashing

Replace SHA256 with bcrypt, scrypt, or Argon2:

```bash
# Install bcrypt
pip install bcrypt==4.0.1

# Use the production-ready version
python app_bcrypt.py
```

Or use the production requirements:
```bash
pip install -r requirements-production.txt
```

**Why?** 
- Bcrypt/scrypt/Argon2 are designed to be computationally expensive
- They provide better protection against brute-force attacks
- SHA256 is fast, which makes it easier to crack

#### 2. Enable HTTPS

Always use SSL/TLS certificates in production:

```bash
# Using Let's Encrypt (free)
sudo certbot --nginx -d your-domain.com
```

#### 3. Implement Rate Limiting

Protect against abuse and brute-force attacks:

```python
# Using Flask-Limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/notes', methods=['POST'])
@limiter.limit("10 per minute")
def create_note():
    # ...
```

#### 4. Add Input Validation

Implement comprehensive input validation:

```python
from flask import escape

# Validate content length
MAX_CONTENT_LENGTH = 100000  # 100KB

if len(content) > MAX_CONTENT_LENGTH:
    return jsonify({'error': 'Content too large'}), 400

# Sanitize content (optional, depends on requirements)
content = escape(content)
```

#### 5. Use Secrets Management

Never hardcode credentials:

```bash
# Use environment variables
export DB_PASSWORD="$(openssl rand -base64 32)"

# Or use a secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)
```

#### 6. Regular Updates

Keep all dependencies updated:

```bash
pip list --outdated
pip install --upgrade -r requirements.txt
```

#### 7. Enable Security Headers

Add security headers to responses:

```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

#### 8. Database Backups

Implement regular automated backups:

```bash
# Daily backup cron job
0 2 * * * /path/to/backup.sh
```

## Known Security Considerations

### Password Storage (Current Implementation)

**Current**: SHA256 with random salts
- ✅ Protects against rainbow table attacks
- ✅ Unique salt per password
- ⚠️ SHA256 is fast, making brute-force easier
- ⚠️ Not specifically designed for password hashing

**Recommendation for Production**: Use bcrypt, scrypt, or Argon2
- See `app_bcrypt.py` for bcrypt implementation
- Install with: `pip install -r requirements-production.txt`

### Note Access

**Current**: No rate limiting on note access
- Anyone with the URL can access a note (unless password protected)
- No limit on access attempts for password-protected notes

**Recommendation**: Implement rate limiting (see above)

### Data Persistence

**Current**: Notes stored indefinitely unless expired
- No automatic cleanup of expired notes (only on access)

**Recommendation**: Add a periodic cleanup job:

```bash
# Add to crontab
0 * * * * docker exec napkin_postgres_1 psql -U postgres napkin -c "DELETE FROM notes WHERE expires_at < NOW();"
```

## Reporting a Vulnerability

If you discover a security vulnerability in Napkin, please:

1. **DO NOT** open a public issue
2. Email the maintainers directly with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will:
- Acknowledge receipt within 48 hours
- Provide a detailed response within 7 days
- Work on a fix and release it as soon as possible
- Credit you in the release notes (if desired)

## Security Best Practices for Users

1. **Use strong passwords** for sensitive notes
2. **Set short expiration times** for sensitive data
3. **Never share passwords** through the same channel as the note link
4. **Verify HTTPS** before entering sensitive information
5. **Clear sensitive notes** manually after use (don't rely solely on expiration)

## License

This security policy is part of the Napkin project and is subject to the same MIT license.
