# app/monitoring.py
from prometheus_client import Counter, Histogram, generate_latest
import time
from functools import wraps

# Metrics
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "HTTP request latency", ["endpoint"]
)


def monitor_request(f):
    """Decorator to monitor request metrics"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()

        try:
            response = f(*args, **kwargs)
            status_code = (
                response.status_code if hasattr(response, "status_code") else 200
            )
        except Exception:
            status_code = 500
            raise
        finally:
            duration = time.time() - start_time
            REQUEST_LATENCY.labels(request.endpoint).observe(duration)
            REQUEST_COUNT.labels(request.method, request.endpoint, status_code).inc()

        return response

    return decorated_function


@app.route("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {"Content-Type": "text/plain"}
