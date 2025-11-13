from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class AppointmentCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    serviceType: str
    preferredDate: str
    message: Optional[str] = ""

class Appointment(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: str
    serviceType: str
    preferredDate: str
    message: Optional[str] = ""
    status: str = "pending"
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

# Appointment Routes
@api_router.post("/appointments", response_model=Appointment)
async def create_appointment(appointment_data: AppointmentCreate):
    try:
        appointment_dict = appointment_data.model_dump()
        appointment_obj = Appointment(**appointment_dict)
        
        # Convert to dict and serialize datetime to ISO string for MongoDB
        doc = appointment_obj.model_dump()
        doc['createdAt'] = doc['createdAt'].isoformat()
        
        # Insert into database
        result = await db.appointments.insert_one(doc)
        
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create appointment")
        
        return appointment_obj
    except Exception as e:
        logging.error(f"Error creating appointment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/appointments", response_model=List[Appointment])
async def get_appointments():
    try:
        # Exclude MongoDB's _id field from the query results
        appointments = await db.appointments.find({}, {"_id": 0}).sort("createdAt", -1).to_list(1000)
        
        # Convert ISO string timestamps back to datetime objects
        for appointment in appointments:
            if isinstance(appointment['createdAt'], str):
                appointment['createdAt'] = datetime.fromisoformat(appointment['createdAt'])
        
        return appointments
    except Exception as e:
        logging.error(f"Error fetching appointments: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str):
    try:
        # Exclude MongoDB's _id field from the query results
        appointment = await db.appointments.find_one({"id": appointment_id}, {"_id": 0})
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        # Convert ISO string timestamp back to datetime object
        if isinstance(appointment['createdAt'], str):
            appointment['createdAt'] = datetime.fromisoformat(appointment['createdAt'])
        
        return Appointment(**appointment)
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching appointment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()