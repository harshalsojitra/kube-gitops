from fastapi import FastAPI, Response
import os
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# 1. Initialize the Counter
# Note: I added labels so you can see which page gets the most hits later!
REQUEST_COUNT = Counter('app_requests_total', 'Total app requests', ['endpoint'])

app = FastAPI()

@app.get("/")
def read_root():
    # 2. Increment the counter when this page is visited
    REQUEST_COUNT.labels(endpoint='/').inc()
    
    env_name = os.getenv("APP_ENVIRONMENT", "Local-Machine")
    db_pass = os.getenv("DATABASE_PASSWORD", "No-Secret-Found")
    
    return {
        "message": f"Hello from the {env_name}!",
        "secret_status": "Secret Loaded" if db_pass == "super-secret-password-123" else "Secret Missing",
        "version": "2.1.0", # Incremented version to track deployment
        "status": "Running"
    }

@app.get("/healthz")
def healthz():
    return {"status": "healthy"}

# 3. ADD THIS ROUTE - This is what Prometheus looks for!
@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)