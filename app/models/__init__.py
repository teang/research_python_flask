from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models
from app.models.user import User
from app.models.role import Role, Permission
from app.models.research import Research
from app.models.category import Category

__all__ = ['db', 'User', 'Role', 'Permission', 'Research', 'Category']
