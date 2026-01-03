# app/auth/__init__.py
from functools import wraps
from flask import request, g, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
import secrets


def rate_limit(max_per_minute=60):
    """Advanced rate limiting decorator"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Implement Redis-based rate limiting
            client_ip = request.remote_addr
            key = f"rate_limit:{client_ip}:{request.endpoint}"

            # Check with Redis
            current = cache.get(key)
            if current and int(current) >= max_per_minute:
                return jsonify({"error": "Rate limit exceeded", "retry_after": 60}), 429

            # Increment counter
            if current:
                cache.incr(key)
            else:
                cache.set(key, 1, timeout=60)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


class SecurityMiddleware:
    """Security headers and protection"""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Add security headers
        def add_headers(status, headers, exc_info=None):
            headers.extend(
                [
                    ("X-Content-Type-Options", "nosniff"),
                    ("X-Frame-Options", "DENY"),
                    ("X-XSS-Protection", "1; mode=block"),
                    ("Content-Security-Policy", "default-src 'self'"),
                    ("Referrer-Policy", "strict-origin-when-cross-origin"),
                ]
            )
            return start_response(status, headers, exc_info)

        return self.app(environ, add_headers)
