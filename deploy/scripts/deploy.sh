#!/bin/bash
# Deployment script for Research Management System

set -e

echo "🚀 Starting deployment..."

# Configuration
APP_DIR="/var/www/research_python_flask"
VENV_DIR="$APP_DIR/venv"
BACKUP_DIR="$APP_DIR/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root or with sudo"
    exit 1
fi

# Backup database
echo "📦 Creating database backup..."
mkdir -p "$BACKUP_DIR"
sudo -u postgres pg_dump research_db > "$BACKUP_DIR/db_backup_$TIMESTAMP.sql"
print_success "Database backed up to $BACKUP_DIR/db_backup_$TIMESTAMP.sql"

# Pull latest code
echo "📥 Pulling latest code..."
cd "$APP_DIR"
git pull origin main
print_success "Code updated"

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements/prod.txt
print_success "Dependencies installed"

# Run database migrations
echo "🗄️  Running database migrations..."
flask db upgrade
print_success "Migrations completed"

# Collect static files (if needed)
# flask collect-static

# Run tests (optional)
if [ "$RUN_TESTS" = "true" ]; then
    echo "🧪 Running tests..."
    pytest tests/ -v
    print_success "Tests passed"
fi

# Restart services
echo "🔄 Restarting services..."
systemctl restart research-app
systemctl restart nginx
print_success "Services restarted"

# Health check
echo "🏥 Performing health check..."
sleep 5
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health)
if [ "$HEALTH_RESPONSE" = "200" ]; then
    print_success "Health check passed"
else
    print_error "Health check failed (HTTP $HEALTH_RESPONSE)"
    exit 1
fi

echo ""
print_success "🎉 Deployment completed successfully!"
echo ""
echo "📊 Service status:"
systemctl status research-app --no-pager -l
