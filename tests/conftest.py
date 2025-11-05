"""
Pytest configuration and fixtures
"""
import os
import tempfile
import pytest
from app import create_app, db
from app.models import User, Research, Category, Tag, Role, Permission
from werkzeug.security import generate_password_hash


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    # Create temporary database
    db_fd, db_path = tempfile.mkstemp()

    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
        'UPLOAD_FOLDER': tempfile.mkdtemp(),
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Create CLI runner"""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def db_session(app):
    """Create database session for testing"""
    with app.app_context():
        # Clean database before each test
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

        yield db.session

        # Cleanup after test
        db.session.rollback()


@pytest.fixture
def admin_user(db_session):
    """Create admin user for testing"""
    admin = User(
        username='admin',
        email='admin@test.com',
        full_name='Admin User',
        is_admin=True
    )
    admin.set_password('admin123')
    db_session.add(admin)
    db_session.commit()
    return admin


@pytest.fixture
def regular_user(db_session):
    """Create regular user for testing"""
    user = User(
        username='testuser',
        email='user@test.com',
        full_name='Test User',
        is_admin=False
    )
    user.set_password('test123')
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def category(db_session):
    """Create test category"""
    cat = Category(
        name='Computer Science',
        description='Computer Science Research'
    )
    db_session.add(cat)
    db_session.commit()
    return cat


@pytest.fixture
def tag(db_session):
    """Create test tag"""
    tag = Tag(name='Machine Learning')
    db_session.add(tag)
    db_session.commit()
    return tag


@pytest.fixture
def research(db_session, regular_user, category):
    """Create test research"""
    research = Research(
        title='Test Research',
        title_en='Test Research EN',
        authors='John Doe',
        abstract='Test abstract',
        keywords='test, research',
        year=2024,
        publication_type='journal',
        user_id=regular_user.id,
        category_id=category.id
    )
    db_session.add(research)
    db_session.commit()
    return research


@pytest.fixture
def role(db_session):
    """Create test role"""
    role = Role(
        name='editor',
        display_name='Editor',
        description='Can edit content'
    )
    db_session.add(role)
    db_session.commit()
    return role


@pytest.fixture
def permission(db_session):
    """Create test permission"""
    perm = Permission(
        name='edit_research',
        display_name='Edit Research',
        description='Can edit research',
        category='research'
    )
    db_session.add(perm)
    db_session.commit()
    return perm


@pytest.fixture
def auth_client(client, regular_user):
    """Create authenticated client"""
    client.post('/auth/login', data={
        'username': regular_user.username,
        'password': 'test123'
    }, follow_redirects=True)
    return client


@pytest.fixture
def admin_client(client, admin_user):
    """Create admin authenticated client"""
    client.post('/auth/login', data={
        'username': admin_user.username,
        'password': 'admin123'
    }, follow_redirects=True)
    return client
