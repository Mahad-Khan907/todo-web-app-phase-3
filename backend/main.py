import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import create_db_and_tables
from src.routers import auth, tasks, chat

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Todo Web App API", version="1.0.0")

# Setup CORS middleware to allow http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Auth, Task, and Chat routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(chat.router)

@app.on_event("startup")
async def on_startup():
    logger.info("Application startup event triggered.")
    """
    Startup event handler.
    Creates database tables on application startup.
    """
    import threading
    import asyncio

    # Run database initialization in a separate thread to avoid blocking startup
    def init_db():
        try:
            create_db_and_tables()
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            print("Application will continue running but database features may be limited.")

    # Start database initialization in a background thread
    thread = threading.Thread(target=init_db, daemon=True)
    thread.start()

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    """
    Root endpoint for health check.
    """
    return {"message": "Todo Web App API is running!"}

@app.get("/health")
def health_check():
    logger.info("Health check endpoint accessed.")
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "Todo Web App API"}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server.")
    uvicorn.run(app, host="0.0.0.0", port=8000)
