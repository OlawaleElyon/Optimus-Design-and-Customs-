"""
Optimus Design & Customs API Server
Production-ready with ONLY Resend + Supabase
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from pathlib import Path

# Import appointment router
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
    description="Appointment booking system powered by Supabase and Resend",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
cors_origins = os.environ.get("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins[0] != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include appointment router
app.include_router(appointment_router)


@app.on_event("startup")
async def startup_event():
    """Validate configuration on startup."""
    logger.info("="*80)
    logger.info("OPTIMUS DESIGN & CUSTOMS API - STARTING")
    logger.info("="*80)
    
    # Check Supabase
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_ANON_KEY")
    if supabase_url and supabase_key:
        logger.info("✅ Supabase configured")
    else:
        logger.error("❌ Supabase NOT configured - app will not work!")
    
    # Check Resend (optional but recommended)
    resend_key = os.environ.get("RESEND_API_KEY")
    if resend_key and resend_key.strip():
        logger.info("✅ Resend configured")
    else:
        logger.warning("⚠️  Resend NOT configured - emails disabled")
    
    logger.info(f"🌐 CORS: {cors_origins}")
    logger.info("="*80)


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Optimus Design & Customs API",
        "version": "2.0.0",
        "stack": ["Supabase", "Resend", "FastAPI"]
    }


@app.get("/api/")
async def root():
    """Root endpoint."""
    return {
        "message": "Optimus Design & Customs API",
        "endpoints": {
            "health": "/api/health",
            "appointment": "POST /api/appointment",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
