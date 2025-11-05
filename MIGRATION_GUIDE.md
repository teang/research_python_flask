# Database Migration Guide

This project uses Flask-Migrate (Alembic) for database schema management.

## Initial Setup

### 1. Initialize Migrations (First Time Only)

```bash
# Initialize migrations directory
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### 2. Initialize Default Data

```bash
# Create default categories, roles, and permissions
flask init-db

# Create admin user
flask create-admin
# Follow prompts to enter username, email, and password
```

## Common Migration Commands

### Create a New Migration

After modifying models in `app/models.py`:

```bash
# Auto-generate migration from model changes
flask db migrate -m "Description of changes"

# Review the generated migration file in migrations/versions/
# Edit if necessary

# Apply migration
flask db upgrade
```

### Rollback Migration

```bash
# Rollback one migration
flask db downgrade

# Rollback to specific revision
flask db downgrade <revision_id>

# Rollback all migrations
flask db downgrade base
```

### View Migration History

```bash
# Show current revision
flask db current

# Show migration history
flask db history

# Show pending migrations
flask db heads
```

### Upgrade/Downgrade

```bash
# Upgrade to latest
flask db upgrade

# Upgrade to specific revision
flask db upgrade <revision_id>

# Downgrade one step
flask db downgrade -1
```

## Custom CLI Commands

### Database Management

```bash
# Show database statistics
flask db-status

# Create admin user (interactive)
flask create-admin

# Create test user for development
flask create-test-user

# Initialize database with default data
flask init-db

# Reset database (WARNING: deletes all data)
flask reset-db
```

### Export/Import

```bash
# Export database to JSON
flask export-db output.json
```

### Utility Commands

```bash
# List all application routes
flask list-routes
```

## Migration Workflow Example

### Scenario: Adding a new field to User model

1. **Modify the model** (`app/models.py`):
```python
class User(db.Model):
    # ... existing fields ...
    phone_number = db.Column(db.String(20), nullable=True)  # New field
```

2. **Create migration**:
```bash
flask db migrate -m "Add phone_number to User model"
```

3. **Review migration file** in `migrations/versions/`:
```python
# Check the generated migration
# Modify if needed (e.g., add data migration logic)
```

4. **Apply migration**:
```bash
flask db upgrade
```

5. **Verify**:
```bash
flask db current
flask db-status
```

### Scenario: Data Migration

For complex data migrations, edit the generated migration file:

```python
def upgrade():
    # Schema changes
    op.add_column('research', sa.Column('status', sa.String(20)))

    # Data migration
    from app.models import Research, db
    connection = op.get_bind()

    # Update existing records
    connection.execute(
        "UPDATE research SET status = 'published' WHERE status IS NULL"
    )

def downgrade():
    op.drop_column('research', 'status')
```

## Docker Environment

### Running Migrations in Docker

```bash
# Create migration
docker-compose exec web flask db migrate -m "Migration description"

# Apply migrations
docker-compose exec web flask db upgrade

# Initialize database
docker-compose exec web flask init-db

# Create admin user
docker-compose exec web flask create-admin
```

## Production Deployment

### Best Practices

1. **Always backup before migration**:
```bash
# PostgreSQL backup
pg_dump research_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

2. **Test migrations on staging first**:
```bash
# On staging
flask db upgrade
# Test application
# If OK, proceed to production
```

3. **Run migrations during deployment**:
```bash
# In deployment script
flask db upgrade
systemctl restart research-app
```

4. **Keep migration files in version control**:
```bash
git add migrations/versions/*.py
git commit -m "Add migration: description"
```

## Troubleshooting

### Migration conflicts

If you have multiple heads:
```bash
# Show heads
flask db heads

# Merge heads
flask db merge <head1> <head2> -m "Merge migrations"
```

### Reset migrations (development only)

```bash
# Drop all tables
flask reset-db

# Remove migrations
rm -rf migrations/

# Start fresh
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask init-db
```

### Stamp database

If migrations are out of sync:
```bash
# Mark database at specific revision without running migrations
flask db stamp <revision_id>

# Stamp to head
flask db stamp head
```

## Migration File Structure

```
migrations/
├── alembic.ini              # Alembic configuration
├── env.py                   # Migration environment
├── script.py.mako           # Migration template
├── README                   # Auto-generated README
└── versions/                # Migration scripts
    ├── 001_initial.py
    ├── 002_add_field.py
    └── 003_data_migration.py
```

## Tips

1. **Always review auto-generated migrations** before applying
2. **Use descriptive migration messages**: `flask db migrate -m "Add user email verification"`
3. **Test migrations locally** before deploying to production
4. **Keep migrations small and focused** - one logical change per migration
5. **Don't modify applied migrations** - create a new migration instead
6. **Backup production database** before running migrations
7. **Use transactions** in data migrations for safety

## Example: Complete Development Workflow

```bash
# 1. Start development
git checkout -b feature/new-field

# 2. Modify models
# Edit app/models.py

# 3. Create migration
flask db migrate -m "Add new field to Research model"

# 4. Review and test
flask db upgrade
python -m pytest tests/

# 5. Commit
git add migrations/versions/*.py
git commit -m "Add new field migration"

# 6. Deploy
git push origin feature/new-field
# Create PR, merge to main
# On production:
git pull origin main
flask db upgrade
systemctl restart research-app
```
