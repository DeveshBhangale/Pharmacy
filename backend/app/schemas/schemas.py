from typing import List, Optional
from pydantic import BaseModel, EmailStr, UUID4, Field, ConfigDict
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class PrescriptionStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    FULFILLED = "fulfilled"

# Base Models
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True
    is_superuser: bool = False

class MedicineBase(BaseModel):
    name: str
    category: str
    manufacturer: str
    description: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    requires_prescription: bool = False

class OrderItemBase(BaseModel):
    medicine_id: UUID4
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)

class OrderBase(BaseModel):
    status: OrderStatus = OrderStatus.PENDING

class PrescriptionBase(BaseModel):
    doctor_name: str
    status: PrescriptionStatus = PrescriptionStatus.ACTIVE

# Create Request Models
class UserCreate(UserBase):
    password: str

class MedicineCreate(MedicineBase):
    pass

class OrderCreate(OrderBase):
    items: List[OrderItemBase]

class PrescriptionCreate(PrescriptionBase):
    medicine_ids: List[UUID4]
    dosages: List[str]

# Update Request Models
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    manufacturer: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    requires_prescription: Optional[bool] = None

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class PrescriptionUpdate(BaseModel):
    status: Optional[PrescriptionStatus] = None

# Response Models
class UserResponse(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MedicineResponse(MedicineBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class OrderItemResponse(OrderItemBase):
    subtotal: float
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(OrderBase):
    id: UUID4
    user_id: UUID4
    items: List[OrderItemResponse]
    total_amount: float
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PrescriptionResponse(PrescriptionBase):
    id: UUID4
    user_id: UUID4
    medicines: List[MedicineResponse]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Token Models
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    exp: datetime 