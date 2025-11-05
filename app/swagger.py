"""
Swagger/OpenAPI documentation configuration
"""
from flasgger import Swagger

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/api/docs/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/api/docs/static",
    "swagger_ui": True,
    "specs_route": "/api/docs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Research Management API",
        "description": "API for managing research papers, users, and metadata",
        "contact": {
            "responsibleOrganization": "TARR",
            "responsibleDeveloper": "Development Team",
            "email": "dev@research.local",
            "url": "https://github.com/your-org/research-system",
        },
        "termsOfService": "http://research.local/terms",
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/api/v1",
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
        }
    },
}


def init_swagger(app):
    """Initialize Swagger documentation"""
    Swagger(app, config=swagger_config, template=swagger_template)
    app.logger.info('Swagger API documentation initialized at /api/docs/')
