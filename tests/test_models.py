"""
Unit tests for database models
"""
import pytest
from datetime import datetime
from app.models import User, Research, Category, Tag, Comment, Bookmark, Role, Permission


class TestUserModel:
    """Test User model"""

    def test_create_user(self, db_session):
        """Test user creation"""
        user = User(
            username='newuser',
            email='new@test.com',
            full_name='New User'
        )
        user.set_password('password123')
        db_session.add(user)
        db_session.commit()

        assert user.id is not None
        assert user.username == 'newuser'
        assert user.email == 'new@test.com'
        assert user.check_password('password123')
        assert not user.is_admin

    def test_password_hashing(self, regular_user):
        """Test password hashing"""
        assert regular_user.password_hash is not None
        assert regular_user.password_hash != 'test123'
        assert regular_user.check_password('test123')
        assert not regular_user.check_password('wrongpassword')

    def test_unique_username(self, db_session, regular_user):
        """Test username uniqueness"""
        duplicate_user = User(
            username=regular_user.username,
            email='different@test.com'
        )
        db_session.add(duplicate_user)

        with pytest.raises(Exception):
            db_session.commit()

    def test_unique_email(self, db_session, regular_user):
        """Test email uniqueness"""
        duplicate_user = User(
            username='different',
            email=regular_user.email
        )
        db_session.add(duplicate_user)

        with pytest.raises(Exception):
            db_session.commit()

    def test_user_researches_relationship(self, db_session, regular_user, research):
        """Test user-research relationship"""
        assert len(regular_user.researches) == 1
        assert regular_user.researches[0].id == research.id

    def test_user_roles(self, db_session, regular_user, role):
        """Test user roles"""
        regular_user.roles.append(role)
        db_session.commit()

        assert regular_user.has_role('editor')
        assert not regular_user.has_role('admin')


class TestResearchModel:
    """Test Research model"""

    def test_create_research(self, db_session, regular_user, category):
        """Test research creation"""
        research = Research(
            title='New Research',
            title_en='New Research EN',
            authors='Jane Doe',
            abstract='Abstract text',
            keywords='keyword1, keyword2',
            year=2024,
            publication_type='conference',
            user_id=regular_user.id,
            category_id=category.id
        )
        db_session.add(research)
        db_session.commit()

        assert research.id is not None
        assert research.title == 'New Research'
        assert research.view_count == 0
        assert research.download_count == 0
        assert research.created_at is not None

    def test_research_tags(self, db_session, research, tag):
        """Test research-tag relationship"""
        research.tags.append(tag)
        db_session.commit()

        assert len(research.tags) == 1
        assert research.tags[0].name == 'Machine Learning'

    def test_research_category(self, research, category):
        """Test research-category relationship"""
        assert research.category.id == category.id
        assert research.category.name == 'Computer Science'

    def test_average_rating(self, db_session, research, regular_user):
        """Test average rating calculation"""
        comment1 = Comment(
            content='Great!',
            rating=5,
            user_id=regular_user.id,
            research_id=research.id
        )
        comment2 = Comment(
            content='Good',
            rating=4,
            user_id=regular_user.id,
            research_id=research.id
        )
        db_session.add_all([comment1, comment2])
        db_session.commit()

        avg = research.average_rating()
        assert avg == 4.5


class TestCategoryModel:
    """Test Category model"""

    def test_create_category(self, db_session):
        """Test category creation"""
        cat = Category(
            name='Physics',
            description='Physics Research'
        )
        db_session.add(cat)
        db_session.commit()

        assert cat.id is not None
        assert cat.name == 'Physics'

    def test_unique_category_name(self, db_session, category):
        """Test category name uniqueness"""
        duplicate = Category(name=category.name)
        db_session.add(duplicate)

        with pytest.raises(Exception):
            db_session.commit()


class TestTagModel:
    """Test Tag model"""

    def test_create_tag(self, db_session):
        """Test tag creation"""
        tag = Tag(name='Deep Learning')
        db_session.add(tag)
        db_session.commit()

        assert tag.id is not None
        assert tag.created_at is not None

    def test_unique_tag_name(self, db_session, tag):
        """Test tag name uniqueness"""
        duplicate = Tag(name=tag.name)
        db_session.add(duplicate)

        with pytest.raises(Exception):
            db_session.commit()


class TestCommentModel:
    """Test Comment model"""

    def test_create_comment(self, db_session, research, regular_user):
        """Test comment creation"""
        comment = Comment(
            content='Excellent research!',
            rating=5,
            user_id=regular_user.id,
            research_id=research.id
        )
        db_session.add(comment)
        db_session.commit()

        assert comment.id is not None
        assert comment.rating == 5
        assert comment.created_at is not None


class TestBookmarkModel:
    """Test Bookmark model"""

    def test_create_bookmark(self, db_session, research, regular_user):
        """Test bookmark creation"""
        bookmark = Bookmark(
            user_id=regular_user.id,
            research_id=research.id
        )
        db_session.add(bookmark)
        db_session.commit()

        assert bookmark.id is not None
        assert bookmark.created_at is not None

    def test_unique_user_research_bookmark(self, db_session, research, regular_user):
        """Test bookmark uniqueness constraint"""
        bookmark1 = Bookmark(user_id=regular_user.id, research_id=research.id)
        bookmark2 = Bookmark(user_id=regular_user.id, research_id=research.id)

        db_session.add(bookmark1)
        db_session.commit()

        db_session.add(bookmark2)
        with pytest.raises(Exception):
            db_session.commit()


class TestRolePermissionModels:
    """Test Role and Permission models"""

    def test_create_role(self, db_session):
        """Test role creation"""
        role = Role(
            name='moderator',
            display_name='Moderator',
            description='Can moderate content'
        )
        db_session.add(role)
        db_session.commit()

        assert role.id is not None

    def test_create_permission(self, db_session):
        """Test permission creation"""
        perm = Permission(
            name='delete_comment',
            display_name='Delete Comment',
            description='Can delete comments',
            category='comment'
        )
        db_session.add(perm)
        db_session.commit()

        assert perm.id is not None

    def test_role_permissions(self, db_session, role, permission):
        """Test role-permission relationship"""
        role.permissions.append(permission)
        db_session.commit()

        assert len(role.permissions) == 1
        assert role.permissions[0].name == 'edit_research'
