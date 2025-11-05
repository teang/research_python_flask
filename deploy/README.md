# Deployment Guide

## Quick Start with Docker Compose

### 1. Prepare Environment

```bash
# Copy environment file
cp .env.production.example .env

# Edit .env and fill in actual values
nano .env
```

### 2. Build and Start Services

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web
```

### 3. Initialize Database

```bash
# Run migrations
docker-compose exec web flask db upgrade

# Create admin user (optional)
docker-compose exec web flask create-admin
```

### 4. Access Application

- Application: http://localhost
- API: http://localhost/api/v1
- Admin: http://localhost/admin

## Manual Deployment (Ubuntu/Debian)

### Prerequisites

```bash
sudo apt update
sudo apt install python3.11 python3-pip python3-venv
sudo apt install postgresql postgresql-contrib
sudo apt install redis-server
sudo apt install nginx
```

### Installation

```bash
# 1. Clone repository
cd /var/www
sudo git clone <repository-url> research_python_flask
cd research_python_flask

# 2. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements/prod.txt

# 4. Configure environment
cp .env.production.example .env
nano .env

# 5. Initialize database
createdb research_db
flask db upgrade

# 6. Copy systemd service
sudo cp deploy/systemd/research-app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable research-app
sudo systemctl start research-app

# 7. Configure Nginx
sudo cp nginx/nginx.conf /etc/nginx/sites-available/research-app
sudo ln -s /etc/nginx/sites-available/research-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Automated Deployment

```bash
# Run deployment script
sudo bash deploy/scripts/deploy.sh
```

## Monitoring

### Health Check

```bash
curl http://localhost/health
```

### View Logs

```bash
# Application logs
journalctl -u research-app -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Docker logs
docker-compose logs -f web
```

### Service Status

```bash
# Systemd
systemctl status research-app

# Docker
docker-compose ps
```

## Backup & Restore

### Backup

```bash
# Database
docker-compose exec postgres pg_dump -U research_user research_db > backup.sql

# Uploaded files
tar -czf uploads_backup.tar.gz app/static/uploads/
```

### Restore

```bash
# Database
docker-compose exec -T postgres psql -U research_user research_db < backup.sql

# Uploaded files
tar -xzf uploads_backup.tar.gz
```

## SSL/HTTPS Setup

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Manual SSL

1. Place certificate files in `nginx/ssl/`
2. Uncomment SSL sections in `nginx/nginx.conf`
3. Restart Nginx

## Scaling

### Horizontal Scaling

```bash
# Scale web workers
docker-compose up -d --scale web=3

# Load balancer configuration needed
```

### Vertical Scaling

Edit `gunicorn.conf.py`:
```python
workers = 8  # Increase workers
```

## Troubleshooting

### Application won't start

```bash
# Check logs
docker-compose logs web

# Verify environment variables
docker-compose exec web env | grep FLASK
```

### Database connection errors

```bash
# Check PostgreSQL status
docker-compose exec postgres pg_isready

# Test connection
docker-compose exec web flask shell
>>> from app import db
>>> db.engine.execute('SELECT 1')
```

### Permission errors

```bash
# Fix upload directory permissions
sudo chown -R www-data:www-data app/static/uploads
sudo chmod -R 755 app/static/uploads
```

## Maintenance

### Update Application

```bash
# Pull latest code
git pull origin main

# Run deployment script
sudo bash deploy/scripts/deploy.sh
```

### Database Migrations

```bash
# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

### Clear Cache

```bash
# Redis
docker-compose exec redis redis-cli FLUSHALL

# Or with password
docker-compose exec redis redis-cli -a redis_pass FLUSHALL
```
