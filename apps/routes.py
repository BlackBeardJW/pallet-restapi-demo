# API Routes for the application for managing pallets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import PalletCreate, PalletUpdate, PalletResponse, Pallet # Importing the Pallet model and schemas
from .db import get_db


router = APIRouter()

@router.post("/pallets/", response_model=PalletResponse)
def create_pallet(pallet: PalletCreate, db: Session = Depends(get_db)):
    db_pallet = Pallet(**pallet.dict())
    db.add(db_pallet)
    db.commit()
    db.refresh(db_pallet)
    return db_pallet

@router.get("/pallets/{pallet_id}", response_model=PalletResponse)
def read_pallet(pallet_id: int, db: Session = Depends(get_db)):
    db_pallet = db.query(Pallet).filter(Pallet.id.__eq__(pallet_id)).first()
    if not db_pallet:
        raise HTTPException(status_code=404, detail="Pallet not found")
    return db_pallet
@router.put("/pallets/{pallet_id}", response_model=PalletResponse)
def update_pallet(pallet_id: int, pallet: PalletUpdate, db: Session = Depends(get_db)):
    db_pallet = db.query(Pallet).filter(Pallet.id == pallet_id).first()
    if not db_pallet:
        raise HTTPException(status_code=404, detail="Pallet not found")
    
    for key, value in pallet.dict(exclude_unset=True).items():
        setattr(db_pallet, key, value)
    
    db.commit()
    db.refresh(db_pallet)
    return db_pallet
@router.delete("/pallets/{pallet_id}", response_model=PalletResponse)
def delete_pallet(pallet_id: int, db: Session = Depends(get_db)):
    db_pallet = db.query(Pallet).filter(Pallet.id == pallet_id).first()
    if not db_pallet:
        raise HTTPException(status_code=404, detail="Pallet not found")
    
    db.delete(db_pallet)
    db.commit()
    return db_pallet