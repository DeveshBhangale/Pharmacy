from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ....core.deps import get_db, get_current_user
from ....schemas.schemas import (
    MedicineCreate,
    MedicineUpdate,
    MedicineResponse,
    UserResponse
)
from ....services.medicine import MedicineService

router = APIRouter()

@router.get("/", response_model=List[MedicineResponse])
async def list_medicines(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None,
    requires_prescription: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
) -> List[MedicineResponse]:
    """
    Retrieve medicines with optional filtering.
    """
    service = MedicineService(db)
    medicines = await service.search(
        name=name,
        category=category,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        requires_prescription=requires_prescription,
        skip=skip,
        limit=limit
    )
    return medicines

@router.post("/", response_model=MedicineResponse)
async def create_medicine(
    medicine_in: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
) -> MedicineResponse:
    """
    Create new medicine (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can create medicines"
        )
    
    service = MedicineService(db)
    return service.create(obj_in=medicine_in)

@router.get("/recommendations", response_model=List[MedicineResponse])
async def get_recommendations(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
) -> List[MedicineResponse]:
    """
    Get AI-powered medicine recommendations for the current user.
    """
    service = MedicineService(db)
    return await service.get_recommendations(str(current_user.id))

@router.get("/{medicine_id}", response_model=MedicineResponse)
async def get_medicine(
    medicine_id: str,
    db: Session = Depends(get_db)
) -> MedicineResponse:
    """
    Get medicine by ID.
    """
    service = MedicineService(db)
    medicine = service.get(medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

@router.put("/{medicine_id}", response_model=MedicineResponse)
async def update_medicine(
    medicine_id: str,
    medicine_in: MedicineUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
) -> MedicineResponse:
    """
    Update medicine (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can update medicines"
        )
    
    service = MedicineService(db)
    medicine = service.get(medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    return service.update(db_obj=medicine, obj_in=medicine_in)

@router.patch("/stock/{medicine_id}", response_model=MedicineResponse)
async def update_stock(
    medicine_id: str,
    quantity: int = Query(..., description="Quantity to add (positive) or remove (negative)"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
) -> MedicineResponse:
    """
    Update medicine stock (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can update stock"
        )
    
    service = MedicineService(db)
    return await service.update_stock(medicine_id, quantity)

@router.patch("/bulk-price-update", response_model=List[MedicineResponse])
async def bulk_update_prices(
    updates: Dict[str, float],
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
) -> List[MedicineResponse]:
    """
    Bulk update medicine prices (admin only).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can update prices"
        )
    
    service = MedicineService(db)
    return await service.bulk_update_prices(updates) 