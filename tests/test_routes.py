"""
Tests for web routes
"""
import pytest
from io import BytesIO


class TestMainRoutes:
    """Test main routes"""

    def test_homepage(self, client):
        """Test homepage loads"""
        response = client.get('/')
        assert response.status_code == 200

    def test_dashboard_requires_login(self, client):
        """Test dashboard requires authentication"""
        response = client.get('/dashboard', follow_redirects=False)
        assert response.status_code in [302, 303]

    def test_dashboard_accessible_when_logged_in(self, auth_client):
        """Test dashboard accessible to authenticated users"""
        response = auth_client.get('/dashboard')
        assert response.status_code == 200


class TestResearchRoutes:
    """Test research routes"""

    def test_research_list(self, client, research):
        """Test research list page"""
        response = client.get('/research/')
        assert response.status_code == 200

    def test_research_detail(self, client, research):
        """Test research detail page"""
        response = client.get(f'/research/{research.id}')
        assert response.status_code == 200

    def test_add_research_page_requires_login(self, client):
        """Test add research page requires login"""
        response = client.get('/research/add', follow_redirects=False)
        assert response.status_code in [302, 303]

    def test_add_research_page_loads(self, auth_client):
        """Test add research page loads for authenticated user"""
        response = auth_client.get('/research/add')
        assert response.status_code == 200

    def test_edit_own_research(self, auth_client, research):
        """Test user can edit own research"""
        response = auth_client.get(f'/research/{research.id}/edit')
        assert response.status_code == 200

    def test_cannot_edit_others_research(self, client, regular_user, research, db_session):
        """Test user cannot edit others' research"""
        # Create another user
        from app.models import User
        other_user = User(username='other', email='other@test.com')
        other_user.set_password('pass123')
        db_session.add(other_user)
        db_session.commit()

        # Login as other user
        client.post('/auth/login', data={
            'username': 'other',
            'password': 'pass123'
        })

        response = client.get(f'/research/{research.id}/edit', follow_redirects=False)
        # Should redirect or return 403
        assert response.status_code in [302, 303, 403]

    def test_delete_research_requires_auth(self, client, research):
        """Test delete research requires authentication"""
        response = client.post(f'/research/{research.id}/delete', follow_redirects=False)
        assert response.status_code in [302, 303]

    def test_categories_page(self, client, category):
        """Test categories page"""
        response = client.get('/research/categories')
        assert response.status_code == 200


class TestBookmarkRoutes:
    """Test bookmark routes"""

    def test_bookmarks_page_requires_login(self, client):
        """Test bookmarks page requires login"""
        response = client.get('/research/bookmarks', follow_redirects=False)
        assert response.status_code in [302, 303]

    def test_bookmarks_page_loads(self, auth_client):
        """Test bookmarks page loads for authenticated user"""
        response = auth_client.get('/research/bookmarks')
        assert response.status_code == 200

    def test_toggle_bookmark_requires_login(self, client, research):
        """Test toggle bookmark requires login"""
        response = client.post(f'/research/{research.id}/bookmark', follow_redirects=False)
        assert response.status_code in [302, 303]


class TestExportRoutes:
    """Test export routes"""

    def test_export_csv(self, client, research):
        """Test CSV export"""
        response = client.get('/research/export/csv')
        assert response.status_code == 200
        assert response.content_type == 'text/csv; charset=utf-8'

    def test_export_excel(self, client, research):
        """Test Excel export"""
        response = client.get('/research/export/excel')
        assert response.status_code == 200
        assert 'spreadsheet' in response.content_type or 'excel' in response.content_type

    def test_export_bibtex(self, client, research):
        """Test BibTeX export"""
        response = client.get('/research/export/bibtex')
        assert response.status_code == 200

    def test_export_ris(self, client, research):
        """Test RIS export"""
        response = client.get('/research/export/ris')
        assert response.status_code == 200


class TestProfileRoutes:
    """Test profile routes"""

    def test_view_profile(self, client, regular_user):
        """Test view user profile"""
        response = client.get(f'/profile/{regular_user.username}')
        assert response.status_code == 200

    def test_edit_profile_requires_login(self, client):
        """Test edit profile requires login"""
        response = client.get('/profile/edit', follow_redirects=False)
        assert response.status_code in [302, 303]

    def test_edit_profile_page_loads(self, auth_client):
        """Test edit profile page loads"""
        response = auth_client.get('/profile/edit')
        assert response.status_code == 200


class TestAnalyticsRoutes:
    """Test analytics routes"""

    def test_analytics_requires_login(self, client):
        """Test analytics requires login"""
        response = client.get('/analytics', follow_redirects=False)
        assert response.status_code in [302, 303]

    def test_analytics_page_loads(self, auth_client):
        """Test analytics page loads"""
        response = auth_client.get('/analytics')
        assert response.status_code == 200


class TestAdminRoutes:
    """Test admin routes"""

    def test_admin_dashboard_requires_admin(self, auth_client):
        """Test admin dashboard requires admin role"""
        response = auth_client.get('/admin/', follow_redirects=False)
        assert response.status_code in [302, 303, 403]

    def test_admin_dashboard_accessible_to_admin(self, admin_client):
        """Test admin dashboard accessible to admin"""
        response = admin_client.get('/admin/')
        assert response.status_code == 200

    def test_admin_users_list(self, admin_client):
        """Test admin users list"""
        response = admin_client.get('/admin/users')
        assert response.status_code == 200

    def test_admin_audit_logs(self, admin_client):
        """Test admin audit logs"""
        response = admin_client.get('/admin/audit-logs')
        assert response.status_code == 200
