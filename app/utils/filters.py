"""Template filters"""
from datetime import datetime


def format_datetime(value, format='%d/%m/%Y %H:%M'):
    """Format datetime"""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return value.strftime(format)


def format_date(value, format='%d/%m/%Y'):
    """Format date"""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return value.strftime(format)


def thai_year(value):
    """Convert to Buddhist Era (Thai year)"""
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.year + 543
    if isinstance(value, int):
        return value + 543
    return value


def truncate_words(text, length=20):
    """Truncate text to specified word count"""
    if not text:
        return ""
    words = text.split()
    if len(words) <= length:
        return text
    return ' '.join(words[:length]) + '...'


def register_filters(app):
    """Register all custom filters"""
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['date'] = format_date
    app.jinja_env.filters['thai_year'] = thai_year
    app.jinja_env.filters['truncate_words'] = truncate_words
