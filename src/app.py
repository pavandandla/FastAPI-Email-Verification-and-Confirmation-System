# app.py
from fastapi import FastAPI
from routes.user_bp import user_bp
from config.database import init_db
from config.config import create_app

# Create the FastAPI app
app = create_app()

# Initialize the database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Include user routes
app.include_router(user_bp)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
