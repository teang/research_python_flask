"""
Tests for REST API endpoints
"""
import pytest
import json


class TestResearchAPI:
    """Test Research API endpoints"""

    def test_get_all_researches(self, client, research):
        """Test GET /api/v1/researches"""
        response = client.get('/api/v1/researches')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'data' in data
        assert isinstance(data['data'], list)

    def test_get_single_research(self, client, research):
        """Test GET /api/v1/researches/<id>"""
        response = client.get(f'/api/v1/researches/{research.id}')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['id'] == research.id
        assert data['title'] == research.title

    def test_get_nonexistent_research(self, client):
        """Test GET /api/v1/researches/<invalid_id>"""
        response = client.get('/api/v1/researches/99999')
        assert response.status_code == 404

    def test_create_research_requires_auth(self, client):
        """Test POST /api/v1/researches requires authentication"""
        response = client.post('/api/v1/researches', json={
            'title': 'New Research',
            'authors': 'Test Author'
        })
        assert response.status_code in [401, 302, 303]

    def test_search_researches(self, client, research):
        """Test search functionality"""
        response = client.get('/api/v1/researches?search=Test')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'data' in data

    def test_filter_by_category(self, client, research, category):
        """Test filter by category"""
        response = client.get(f'/api/v1/researches?category_id={category.id}')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'data' in data

    def test_pagination(self, client, research):
        """Test pagination"""
        response = client.get('/api/v1/researches?page=1&per_page=5')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'pagination' in data
        assert data['pagination']['page'] == 1
        assert data['pagination']['per_page'] == 5


class TestCategoryAPI:
    """Test Category API endpoints"""

    def test_get_all_categories(self, client, category):
        """Test GET /api/v1/categories"""
        response = client.get('/api/v1/categories')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_get_single_category(self, client, category):
        """Test GET /api/v1/categories/<id>"""
        response = client.get(f'/api/v1/categories/{category.id}')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['name'] == category.name


class TestTagAPI:
    """Test Tag API endpoints"""

    def test_get_all_tags(self, client, tag):
        """Test GET /api/v1/tags"""
        response = client.get('/api/v1/tags')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert isinstance(data, list)


class TestBookmarkAPI:
    """Test Bookmark API endpoints"""

    def test_get_bookmarks_requires_auth(self, client):
        """Test GET /api/v1/bookmarks requires authentication"""
        response = client.get('/api/v1/bookmarks')
        assert response.status_code in [401, 302, 303]

    def test_add_bookmark_requires_auth(self, client, research):
        """Test POST /api/v1/bookmarks requires authentication"""
        response = client.post(f'/api/v1/bookmarks/{research.id}')
        assert response.status_code in [401, 302, 303]


class TestCommentAPI:
    """Test Comment API endpoints"""

    def test_get_research_comments(self, client, research):
        """Test GET /api/v1/researches/<id>/comments"""
        response = client.get(f'/api/v1/researches/{research.id}/comments')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_add_comment_requires_auth(self, client, research):
        """Test POST /api/v1/researches/<id>/comments requires auth"""
        response = client.post(f'/api/v1/researches/{research.id}/comments', json={
            'content': 'Great work!',
            'rating': 5
        })
        assert response.status_code in [401, 302, 303]


class TestStatisticsAPI:
    """Test Statistics API endpoint"""

    def test_get_statistics(self, client, research):
        """Test GET /api/v1/statistics"""
        response = client.get('/api/v1/statistics')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'total_research' in data
        assert 'total_users' in data
