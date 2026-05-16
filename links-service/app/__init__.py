from flask import Flask
from flask_cors import CORS
from .config import Config
from .db import init_pool, close_conn
from .models import init_schema

from flask import Response, request, g
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import os
def create_app():
    app = Flask(__name__)
   
    app.config.from_object(Config)
    CORS(app, resources={r'/*': {'origins': '*'}})
    init_pool(app.config['DATABASE_URL'])
    app.teardown_appcontext(close_conn)
    
    SERVICE_NAME = "link-service"  

    REQUEST_COUNT = Counter(
        "http_requests_total",
        "Total HTTP requests",
        ["service", "method", "endpoint", "status"]
    )

    REQUEST_LATENCY = Histogram(
        "http_request_duration_seconds",
        "HTTP request latency",
        ["service", "endpoint"]
    )
    
    
    @app.before_request
    def before_request():
        g.start_time = time.time()


    @app.after_request
    def after_request(response):
        endpoint = request.path

        REQUEST_COUNT.labels(
            service=SERVICE_NAME,
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()

        if hasattr(g, "start_time"):
            REQUEST_LATENCY.labels(
                service=SERVICE_NAME,
                endpoint=endpoint
            ).observe(time.time() - g.start_time)
        response.headers["X-Service-Instance"] = os.getenv("INSTANCE_NAME", "unknown")
        return response
    with app.app_context():
        init_schema()
    from .routes import bp
    app.register_blueprint(bp)
    return app


