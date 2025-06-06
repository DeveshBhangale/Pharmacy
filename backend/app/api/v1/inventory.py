from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_superuser
from app.models.pharmacy import User, Medicine, InventoryItem

router = APIRouter()

# Pydantic models for request/response
class MedicineBase(BaseModel):
    name: str
    generic_name: str
    manufacturer: str
    description: str
    price: float
    category: str
    requires_prescription: bool = False
    image_url: str | None = None
    metadata: dict | None = None

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(MedicineBase):
    pass

class MedicineResponse(MedicineBase):
    id: int
    stock_quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class InventoryItemBase(BaseModel):
    medicine_id: int
    batch_number: str
    expiry_date: str
    quantity: int
    purchase_price: float
    supplier: str

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemUpdate(InventoryItemBase):
    pass

class InventoryItemResponse(InventoryItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Medicine endpoints
@router.post("/medicines", response_model=MedicineResponse)
async def create_medicine(
    *,
    db: Session = Depends(get_db),
    medicine_in: MedicineCreate,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    medicine = Medicine(**medicine_in.model_dump())
    db.add(medicine)
    db.commit()
    db.refresh(medicine)
    return medicine

@router.get("/medicines", response_model=List[MedicineResponse])
async def read_medicines(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    medicines = db.query(Medicine).offset(skip).limit(limit).all()
    return medicines

@router.get("/medicines/{medicine_id}", response_model=MedicineResponse)
async def read_medicine(
    *,
    db: Session = Depends(get_db),
    medicine_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    return medicine

@router.put("/medicines/{medicine_id}", response_model=MedicineResponse)
async def update_medicine(
    *,
    db: Session = Depends(get_db),
    medicine_id: int,
    medicine_in: MedicineUpdate,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    for field, value in medicine_in.model_dump().items():
        setattr(medicine, field, value)
    
    db.add(medicine)
    db.commit()
    db.refresh(medicine)
    return medicine

@router.delete("/medicines/{medicine_id}")
async def delete_medicine(
    *,
    db: Session = Depends(get_db),
    medicine_id: int,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    db.delete(medicine)
    db.commit()
    return {"status": "success"}

# Inventory endpoints
@router.post("/inventory", response_model=InventoryItemResponse)
async def create_inventory_item(
    *,
    db: Session = Depends(get_db),
    inventory_in: InventoryItemCreate,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    # Verify medicine exists
    medicine = db.query(Medicine).filter(Medicine.id == inventory_in.medicine_id).first()
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    inventory_item = InventoryItem(**inventory_in.model_dump())
    db.add(inventory_item)
    
    # Update medicine stock quantity
    medicine.stock_quantity += inventory_in.quantity
    
    db.commit()
    db.refresh(inventory_item)
    return inventory_item

@router.get("/inventory", response_model=List[InventoryItemResponse])
async def read_inventory_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    inventory_items = db.query(InventoryItem).offset(skip).limit(limit).all()
    return inventory_items

@router.get("/inventory/{item_id}", response_model=InventoryItemResponse)
async def read_inventory_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    inventory_item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not inventory_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found"
        )
    return inventory_item

@router.put("/inventory/{item_id}", response_model=InventoryItemResponse)
async def update_inventory_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    inventory_in: InventoryItemUpdate,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    inventory_item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not inventory_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found"
        )
    
    # Update medicine stock quantity
    medicine = db.query(Medicine).filter(Medicine.id == inventory_item.medicine_id).first()
    medicine.stock_quantity -= inventory_item.quantity
    medicine.stock_quantity += inventory_in.quantity
    
    for field, value in inventory_in.model_dump().items():
        setattr(inventory_item, field, value)
    
    db.add(inventory_item)
    db.commit()
    db.refresh(inventory_item)
    return inventory_item

@router.delete("/inventory/{item_id}")
async def delete_inventory_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    inventory_item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not inventory_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found"
        )
    
    # Update medicine stock quantity
    medicine = db.query(Medicine).filter(Medicine.id == inventory_item.medicine_id).first()
    medicine.stock_quantity -= inventory_item.quantity
    
    db.delete(inventory_item)
    db.commit()
    return {"status": "success"} 