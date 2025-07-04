# Main application entry point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.db import engine, Base
from apps.routes import router as pallet_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the pallet router
app.include_router(pallet_router)
# Initialize the database
Base.metadata.create_all(bind=engine)