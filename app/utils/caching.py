# app/utils/caching.py
from functools import wraps
from flask import current_app
import pickle
import hashlib


def cached(timeout=300, key_prefix="view/"):
    """Advanced caching decorator with automatic invalidation"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = (
                key_prefix
                + hashlib.md5(
                    f"{f.__module__}.{f.__name__}:{args}:{kwargs}".encode()
                ).hexdigest()
            )

            # Try to get from cache
            cached = cache.get(cache_key)
            if cached is not None:
                return pickle.loads(cached)

            # Execute function
            result = f(*args, **kwargs)

            # Store in cache
            cache.set(cache_key, pickle.dumps(result), timeout=timeout)

            return result

        return decorated_function

    return decorator


class RedisCache:
    """Custom Redis cache implementation"""

    def __init__(self, redis_client):
        self.redis = redis_client

    def get_or_set(self, key, callback, timeout=300):
        """Get from cache or set using callback"""
        value = self.redis.get(key)
        if value:
            return pickle.loads(value)

        value = callback()
        self.redis.setex(key, timeout, pickle.dumps(value))
        return value
