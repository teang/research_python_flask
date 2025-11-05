"""
Flask CLI commands for database management and utilities
"""
import click
from flask import current_app
from app.models import db, User, Role, Permission, Category
from werkzeug.security import generate_password_hash
import random
from datetime import datetime


def register_commands(app):
    """Register custom CLI commands"""

    @app.cli.command("create-admin")
    @click.option('--username', prompt=True, help='Admin username')
    @click.option('--email', prompt=True, help='Admin email')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Admin password')
    def create_admin(username, email, password):
        """Create an admin user"""
        try:
            # Check if user exists
            if User.query.filter_by(username=username).first():
                click.echo(f'Error: User {username} already exists')
                return

            if User.query.filter_by(email=email).first():
                click.echo(f'Error: Email {email} already exists')
                return

            # Create admin user
            admin = User(
                username=username,
                email=email,
                full_name='Administrator',
                is_admin=True
            )
            admin.set_password(password)

            db.session.add(admin)
            db.session.commit()

            click.echo(f'✓ Admin user {username} created successfully!')

        except Exception as e:
            db.session.rollback()
            click.echo(f'✗ Error creating admin user: {str(e)}')


    @app.cli.command("init-db")
    def init_db():
        """Initialize database with default data"""
        try:
            click.echo('Initializing database...')

            # Create default categories
            categories = [
                {'name': 'Computer Science', 'description': 'วิทยาการคอมพิวเตอร์'},
                {'name': 'Agriculture', 'description': 'เกษตรศาสตร์'},
                {'name': 'Engineering', 'description': 'วิศวกรรมศาสตร์'},
                {'name': 'Medicine', 'description': 'แพทยศาสตร์'},
                {'name': 'Social Sciences', 'description': 'สังคมศาสตร์'},
                {'name': 'Natural Sciences', 'description': 'วิทยาศาสตร์ธรรมชาติ'},
            ]

            for cat_data in categories:
                if not Category.query.filter_by(name=cat_data['name']).first():
                    category = Category(**cat_data)
                    db.session.add(category)
                    click.echo(f'  + Created category: {cat_data["name"]}')

            # Create default roles
            roles_data = [
                {
                    'name': 'admin',
                    'display_name': 'ผู้ดูแลระบบ',
                    'description': 'สิทธิ์เต็มในการจัดการระบบ'
                },
                {
                    'name': 'moderator',
                    'display_name': 'ผู้ดูแลเนื้อหา',
                    'description': 'ดูแลและตรวจสอบเนื้อหา'
                },
                {
                    'name': 'researcher',
                    'display_name': 'นักวิจัย',
                    'description': 'สามารถเผยแพร่งานวิจัย'
                },
                {
                    'name': 'viewer',
                    'display_name': 'ผู้อ่าน',
                    'description': 'อ่านและค้นหางานวิจัย'
                }
            ]

            for role_data in roles_data:
                if not Role.query.filter_by(name=role_data['name']).first():
                    role = Role(**role_data)
                    db.session.add(role)
                    click.echo(f'  + Created role: {role_data["name"]}')

            # Create default permissions
            permissions_data = [
                {'name': 'create_research', 'display_name': 'สร้างงานวิจัย', 'category': 'research'},
                {'name': 'edit_research', 'display_name': 'แก้ไขงานวิจัย', 'category': 'research'},
                {'name': 'delete_research', 'display_name': 'ลบงานวิจัย', 'category': 'research'},
                {'name': 'view_research', 'display_name': 'ดูงานวิจัย', 'category': 'research'},
                {'name': 'manage_users', 'display_name': 'จัดการผู้ใช้', 'category': 'admin'},
                {'name': 'manage_roles', 'display_name': 'จัดการบทบาท', 'category': 'admin'},
                {'name': 'view_audit_logs', 'display_name': 'ดู audit logs', 'category': 'admin'},
            ]

            for perm_data in permissions_data:
                if not Permission.query.filter_by(name=perm_data['name']).first():
                    perm = Permission(**perm_data)
                    db.session.add(perm)
                    click.echo(f'  + Created permission: {perm_data["name"]}')

            db.session.commit()
            click.echo('✓ Database initialized successfully!')

        except Exception as e:
            db.session.rollback()
            click.echo(f'✗ Error initializing database: {str(e)}')


    @app.cli.command("reset-db")
    @click.confirmation_option(prompt='Are you sure you want to reset the database? This will delete all data!')
    def reset_db():
        """Reset database (WARNING: Deletes all data)"""
        try:
            click.echo('Dropping all tables...')
            db.drop_all()
            click.echo('Creating all tables...')
            db.create_all()
            click.echo('✓ Database reset successfully!')
            click.echo('\nRun "flask init-db" to populate with default data')

        except Exception as e:
            click.echo(f'✗ Error resetting database: {str(e)}')


    @app.cli.command("db-status")
    def db_status():
        """Show database status and statistics"""
        try:
            click.echo('Database Status:')
            click.echo('-' * 50)

            # Count records
            from app.models import Research, Category, Tag, Comment, Bookmark

            stats = {
                'Users': User.query.count(),
                'Researches': Research.query.count(),
                'Categories': Category.query.count(),
                'Tags': Tag.query.count(),
                'Comments': Comment.query.count(),
                'Bookmarks': Bookmark.query.count(),
                'Roles': Role.query.count(),
                'Permissions': Permission.query.count(),
            }

            for table, count in stats.items():
                click.echo(f'  {table:.<40} {count:>5}')

            click.echo('-' * 50)

        except Exception as e:
            click.echo(f'✗ Error: {str(e)}')


    @app.cli.command("export-db")
    @click.argument('output_file')
    def export_db(output_file):
        """Export database to JSON file"""
        import json
        from app.models import Research, Category, Tag

        try:
            data = {
                'categories': [
                    {'id': c.id, 'name': c.name, 'description': c.description}
                    for c in Category.query.all()
                ],
                'tags': [
                    {'id': t.id, 'name': t.name}
                    for t in Tag.query.all()
                ],
                'researches': [
                    {
                        'id': r.id,
                        'title': r.title,
                        'authors': r.authors,
                        'year': r.year,
                        'category_id': r.category_id,
                    }
                    for r in Research.query.all()
                ]
            }

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            click.echo(f'✓ Database exported to {output_file}')

        except Exception as e:
            click.echo(f'✗ Error exporting database: {str(e)}')


    @app.cli.command("create-test-user")
    def create_test_user():
        """Create a test user for development"""
        try:
            username = 'testuser'

            if User.query.filter_by(username=username).first():
                click.echo(f'Test user {username} already exists')
                return

            user = User(
                username=username,
                email='test@example.com',
                full_name='Test User',
                is_admin=False
            )
            user.set_password('test123')

            db.session.add(user)
            db.session.commit()

            click.echo(f'✓ Test user created: username={username}, password=test123')

        except Exception as e:
            db.session.rollback()
            click.echo(f'✗ Error creating test user: {str(e)}')


    @app.cli.command("list-routes")
    def list_routes():
        """List all application routes"""
        click.echo('Application Routes:')
        click.echo('-' * 80)

        rules = sorted(current_app.url_map.iter_rules(), key=lambda r: r.rule)

        for rule in rules:
            methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
            click.echo(f'{rule.rule:.<50} {methods:>10} -> {rule.endpoint}')

        click.echo('-' * 80)
        click.echo(f'Total routes: {len(rules)}')
