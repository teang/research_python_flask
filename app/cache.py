"""
Caching layer using Redis and Flask-Caching
"""
from flask_caching import Cache

cache = Cache()


def init_cache(app):
    """Initialize caching"""
    cache.init_app(app)
    app.logger.info(f'Cache initialized with type: {app.config.get("CACHE_TYPE")}')
    return cache


# Cache key generators
def make_cache_key_for_research_list(*args, **kwargs):
    """Generate cache key for research list based on query parameters"""
    from flask import request

    params = []
    if request.args.get('page'):
        params.append(f"page:{request.args.get('page')}")
    if request.args.get('search'):
        params.append(f"search:{request.args.get('search')}")
    if request.args.get('category_id'):
        params.append(f"cat:{request.args.get('category_id')}")
    if request.args.get('sort_by'):
        params.append(f"sort:{request.args.get('sort_by')}")

    return 'research_list:' + ':'.join(params) if params else 'research_list:default'


def clear_research_cache():
    """Clear all research-related cache"""
    cache.delete_memoized('get_popular_researches')
    cache.delete_memoized('get_research_stats')
    # Clear list cache with pattern
    with cache.cache._write_client.pipeline() as pipe:
        for key in cache.cache._read_client.scan_iter('research_list:*'):
            pipe.delete(key)
        pipe.execute()
