# Napkin Deployment Guide

This guide covers how to deploy Napkin to production.

## Prerequisites

- A server with Docker and Docker Compose installed
- PostgreSQL database (can use Docker)
- Domain name (optional, but recommended)

## Deployment with Docker (Recommended)

### 1. Prepare Your Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y
```

### 2. Clone the Repository

```bash
git clone https://github.com/LawderLin/Napkin.git
cd Napkin
```

### 3. Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
cd backend
cp .env.example .env
nano .env
```

Update the database credentials for production:

```env
DB_NAME=napkin
DB_USER=napkin_user
DB_PASSWORD=your_secure_password_here
DB_HOST=postgres
DB_PORT=5432
```

### 4. Update Docker Compose for Production

Edit `docker-compose.yml` to use production settings:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: napkin
      POSTGRES_USER: napkin_user
      POSTGRES_PASSWORD: your_secure_password_here
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  backend:
    build: ./backend
    environment:
      DB_NAME: napkin
      DB_USER: napkin_user
      DB_PASSWORD: your_secure_password_here
      DB_HOST: postgres
      DB_PORT: 5432
    depends_on:
      - postgres
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:8080"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
```

### 5. Start the Application

```bash
docker-compose up -d
```

### 6. Verify Deployment

```bash
# Check if all containers are running
docker-compose ps

# Check logs
docker-compose logs -f

# Test the application
curl http://localhost/api/health
```

## Manual Deployment

### Backend

1. Set up Python environment:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with production values
```

3. Run with Gunicorn (production WSGI server):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend

1. Build for production:
```bash
cd frontend
npm install
npm run build
```

2. Serve with Nginx:
```bash
# Install Nginx
sudo apt install nginx

# Copy built files
sudo cp -r dist/* /var/www/html/

# Configure Nginx
sudo nano /etc/nginx/sites-available/napkin
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/napkin /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL/HTTPS Setup (Recommended)

### Using Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

## Database Backup

### Automatic Backups

Create a backup script:

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/napkin"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

docker exec napkin_postgres_1 pg_dump -U napkin_user napkin > "$BACKUP_DIR/napkin_$DATE.sql"

# Keep only last 7 days of backups
find $BACKUP_DIR -name "napkin_*.sql" -mtime +7 -delete
```

Add to crontab:
```bash
crontab -e
# Add line: 0 2 * * * /path/to/backup.sh
```

## Monitoring

### Health Check Endpoint

Monitor the health endpoint:
```bash
curl http://your-domain.com/api/health
```

### Log Monitoring

```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Or use a logging service like:
# - ELK Stack
# - Splunk
# - DataDog
```

## Scaling

### Horizontal Scaling

To scale the backend:

```yaml
# In docker-compose.yml
backend:
  # ... existing config
  deploy:
    replicas: 3
```

### Load Balancer

Use Nginx or HAProxy as a load balancer:

```nginx
upstream backend {
    server backend1:5000;
    server backend2:5000;
    server backend3:5000;
}
```

## Security Best Practices

1. **Use HTTPS**: Always use SSL/TLS in production
2. **Strong Passwords**: Use strong database passwords
3. **Firewall**: Configure firewall to only allow necessary ports
4. **Regular Updates**: Keep all dependencies updated
5. **Database Access**: Restrict database access to backend only
6. **Rate Limiting**: Implement rate limiting to prevent abuse
7. **Backups**: Regular automated backups
8. **Monitoring**: Set up monitoring and alerts

## Environment-Specific Configuration

### Development
- Debug mode enabled
- Verbose logging
- Auto-reload

### Production
- Debug mode disabled
- Error logging only
- No auto-reload
- Performance optimizations
- Security headers

## Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Verify credentials in .env
```

### Backend Not Starting
```bash
# Check backend logs
docker-compose logs backend

# Verify Python dependencies
docker-compose exec backend pip list
```

### Frontend Build Issues
```bash
# Clear cache and rebuild
rm -rf node_modules package-lock.json
npm install
npm run build
```

## Maintenance

### Update Application
```bash
git pull origin main
docker-compose down
docker-compose build
docker-compose up -d
```

### Database Cleanup
```bash
# Delete expired notes (run periodically)
docker exec napkin_postgres_1 psql -U napkin_user napkin -c "DELETE FROM notes WHERE expires_at < NOW();"
```

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Contact maintainers

---

Remember to customize these instructions based on your specific infrastructure and requirements!
