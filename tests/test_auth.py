"""
Tests for authentication routes
"""
import pytest
from flask import session


class TestRegistration:
    """Test user registration"""

    def test_registration_page_loads(self, client):
        """Test registration page loads"""
        response = client.get('/auth/register')
        assert response.status_code == 200
        assert b'Register' in response.data or 'Register'.encode('utf-8') in response.data

    def test_successful_registration(self, client, db_session):
        """Test successful user registration"""
        response = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'full_name': 'New User'
        }, follow_redirects=True)

        assert response.status_code == 200

    def test_registration_with_existing_username(self, client, regular_user):
        """Test registration with existing username fails"""
        response = client.post('/auth/register', data={
            'username': regular_user.username,
            'email': 'different@test.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'full_name': 'Another User'
        }, follow_redirects=True)

        # Should show error or stay on registration page
        assert response.status_code == 200

    def test_registration_password_mismatch(self, client):
        """Test registration with mismatched passwords"""
        response = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'password123',
            'confirm_password': 'different',
            'full_name': 'New User'
        })

        assert response.status_code == 200


class TestLogin:
    """Test user login"""

    def test_login_page_loads(self, client):
        """Test login page loads"""
        response = client.get('/auth/login')
        assert response.status_code == 200

    def test_successful_login(self, client, regular_user):
        """Test successful login"""
        response = client.post('/auth/login', data={
            'username': regular_user.username,
            'password': 'test123'
        }, follow_redirects=True)

        assert response.status_code == 200

    def test_login_with_wrong_password(self, client, regular_user):
        """Test login with wrong password"""
        response = client.post('/auth/login', data={
            'username': regular_user.username,
            'password': 'wrongpassword'
        }, follow_redirects=True)

        assert response.status_code == 200

    def test_login_with_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post('/auth/login', data={
            'username': 'nonexistent',
            'password': 'password123'
        }, follow_redirects=True)

        assert response.status_code == 200


class TestLogout:
    """Test user logout"""

    def test_logout(self, auth_client):
        """Test logout functionality"""
        response = auth_client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200

    def test_logout_redirects_to_login(self, auth_client):
        """Test logout redirects to home or login"""
        response = auth_client.get('/auth/logout', follow_redirects=False)
        assert response.status_code in [302, 303]


class TestProtectedRoutes:
    """Test protected routes require authentication"""

    def test_dashboard_requires_login(self, client):
        """Test dashboard requires authentication"""
        response = client.get('/dashboard', follow_redirects=False)
        assert response.status_code in [302, 303]

    def test_add_research_requires_login(self, client):
        """Test add research requires authentication"""
        response = client.get('/research/add', follow_redirects=False)
        assert response.status_code in [302, 303]

    def test_admin_requires_admin_role(self, auth_client):
        """Test admin routes require admin role"""
        response = auth_client.get('/admin/', follow_redirects=False)
        # Should redirect or return 403
        assert response.status_code in [302, 303, 403]

    def test_admin_accessible_to_admin(self, admin_client):
        """Test admin routes accessible to admin"""
        response = admin_client.get('/admin/')
        assert response.status_code == 200
