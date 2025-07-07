# Pallet and PalletCreate Schema with SQLAlchemy ORM
from sqlalchemy import Column, Integer, String, Float, DateTime
from .db import Base, get_db  # Ensure Base and get_db are imported from the correct module
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

Base = Base  # Ensure Base is imported from the correct module

class Pallet(Base):
    __tablename__ = "pallets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    weight = Column(Float, nullable=False)
    dimensions = Column(String, nullable=False)  # e.g., "120x80x100"
    created_at = Column(DateTime, default=datetime.utcnow)
    
class PalletCreate(BaseModel):
    name: str = Field(..., description="Name of the pallet, e.g., 'Pallet A'")
    weight: float = Field(..., description="Weight of the pallet, e.g., 100.0")
    dimensions: str = Field(..., description="Dimensions of the pallet, e.g., '120x80x100'")

class PalletUpdate(BaseModel):
    name: Optional[str] = Field(default=None, description="Pallet A Updated")
    weight: Optional[float] = Field(default=None, description="120.0")
    dimensions: Optional[str] = Field(default=None, description="120x80x100")

class PalletResponse(BaseModel):
    id: int
    name: str
    weight: float
    dimensions: str
    created_at: datetime

    class Config:
        from_attributes = True  # This allows Pydantic to read data from SQLAlchemy models
