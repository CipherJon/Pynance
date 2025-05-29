from flask_caching import Cache
import os

# Cache configuration
cache_config = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    'CACHE_DEFAULT_TIMEOUT': 300,  # 5 minutes
    'CACHE_KEY_PREFIX': 'pybudget_'
}

# Initialize cache
cache = Cache()

def init_cache(app):
    """Initialize cache with the Flask app."""
    cache.init_app(app, config=cache_config) 