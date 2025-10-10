from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, quiet_time
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quiet Time API",
    description="Backend API for Quiet Time Application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(quiet_time.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Quiet Time API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

