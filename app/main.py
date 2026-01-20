from fastapi import FastAPI
import os
REQUEST_COUNT = Counter('app_requests_total', 'Total app requests')

app = FastAPI()

@app.get("/")

def read_root():
    # os.getenv reads the variables we put in deployment.yaml
    env_name = os.getenv("APP_ENVIRONMENT", "Local-Machine")
    db_pass = os.getenv("DATABASE_PASSWORD", "No-Secret-Found")
    
    return {
        "message": f"Hello from the {env_name}!",
        "secret_status": "Secret Loaded" if db_pass == "super-secret-password-123" else "Secret Missing",
        "version": "2.0.0",
        "status": "Running"
    }

@app.get("/healthz")
def healthz():
    return {"status": "healthy"}