from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException
import boto3
from ..models.models import Medicine
from ..schemas.schemas import MedicineCreate, MedicineUpdate
from .base import BaseService

class MedicineService(BaseService[Medicine, MedicineCreate, MedicineUpdate]):
    def __init__(self, db: Session):
        super().__init__(Medicine, db)
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('pms-medicines')

    async def get_by_category(self, category: str) -> List[Medicine]:
        """Get medicines by category."""
        return self.db.query(self.model).filter(self.model.category == category).all()

    async def update_stock(self, id: Any, quantity: int) -> Medicine:
        """Update medicine stock."""
        medicine = self.get(id)
        if not medicine:
            raise HTTPException(status_code=404, detail="Medicine not found")
        
        if medicine.stock + quantity < 0:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        
        medicine.stock += quantity
        self.db.commit()
        self.db.refresh(medicine)
        
        # Sync with DynamoDB
        self._sync_to_dynamodb(medicine)
        
        return medicine

    async def get_recommendations(self, user_id: str) -> List[Medicine]:
        """Get AI-powered medicine recommendations."""
        from ..ml.recommendation import get_recommendations
        recommended_ids = await get_recommendations(user_id)
        return self.db.query(self.model).filter(self.model.id.in_(recommended_ids)).all()

    def _sync_to_dynamodb(self, medicine: Medicine) -> None:
        """Sync medicine data to DynamoDB."""
        try:
            item = {
                'id': str(medicine.id),
                'name': medicine.name,
                'category': medicine.category,
                'manufacturer': medicine.manufacturer,
                'price': medicine.price,
                'stock': medicine.stock,
                'requires_prescription': medicine.requires_prescription,
                'updated_at': medicine.updated_at.isoformat()
            }
            self.table.put_item(Item=item)
        except Exception as e:
            # Log the error but don't fail the transaction
            print(f"Error syncing to DynamoDB: {e}")

    async def search(
        self,
        *,
        name: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        in_stock: Optional[bool] = None,
        requires_prescription: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Medicine]:
        """Advanced search with multiple criteria."""
        query = self.db.query(self.model)
        
        if name:
            query = query.filter(self.model.name.ilike(f"%{name}%"))
        if category:
            query = query.filter(self.model.category == category)
        if min_price is not None:
            query = query.filter(self.model.price >= min_price)
        if max_price is not None:
            query = query.filter(self.model.price <= max_price)
        if in_stock is not None:
            query = query.filter(self.model.stock > 0 if in_stock else self.model.stock == 0)
        if requires_prescription is not None:
            query = query.filter(self.model.requires_prescription == requires_prescription)
        
        return query.offset(skip).limit(limit).all()

    async def bulk_update_prices(self, updates: Dict[Any, float]) -> List[Medicine]:
        """Bulk update medicine prices."""
        medicines = []
        for medicine_id, new_price in updates.items():
            medicine = self.get(medicine_id)
            if medicine:
                medicine.price = new_price
                medicines.append(medicine)
        
        if medicines:
            self.db.bulk_save_objects(medicines)
            self.db.commit()
            
            # Sync all updates to DynamoDB
            for medicine in medicines:
                self._sync_to_dynamodb(medicine)
        
        return medicines 