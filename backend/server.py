"""
Optimus Design & Customs API
Clean rebuild with only appointment functionality
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from pathlib import Path

# Import the new appointment router
from appointment_api import appointment_router

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Optimus Design & Customs API",
    description="Appointment booking API with Supabase and Resend",
    version="2.0.0"
)

# Configure CORS
cors_origins = os.environ.get("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include appointment router
app.include_router(appointment_router)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Optimus Design & Customs API v2.0",
        "endpoints": {
            "appointment": "/api/appointment"
        }
    }

@app.get("/api/")
async def root():
    """Root endpoint."""
    return {
        "message": "Optimus Design & Customs API v2.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
