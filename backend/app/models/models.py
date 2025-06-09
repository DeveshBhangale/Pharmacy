from typing import List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table, Text, Enum
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from .base import Base, TimestampMixin

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class PrescriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    FULFILLED = "fulfilled"

# Association tables
order_medicine = Table(
    'order_medicine',
    Base.metadata,
    Column('order_id', UUID(as_uuid=True), ForeignKey('order.id')),
    Column('medicine_id', UUID(as_uuid=True), ForeignKey('medicine.id')),
    Column('quantity', Integer, nullable=False),
    Column('unit_price', Float, nullable=False)
)

prescription_medicine = Table(
    'prescription_medicine',
    Base.metadata,
    Column('prescription_id', UUID(as_uuid=True), ForeignKey('prescription.id')),
    Column('medicine_id', UUID(as_uuid=True), ForeignKey('medicine.id')),
    Column('dosage', String, nullable=False)
)

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(50), default="customer")  # customer, pharmacist, admin
    is_active = Column(Boolean, default=True)
    
    # Relationships
    orders = relationship("Order", back_populates="user")
    prescriptions = relationship("Prescription", back_populates="user")

class Medicine(Base, TimestampMixin):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    category = Column(String(100))
    image_url = Column(String(500))
    requires_prescription = Column(Boolean, default=False)
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="medicine")
    prescription_items = relationship("PrescriptionItem", back_populates="medicine")

class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="pending")  # pending, confirmed, shipped, delivered
    total_amount = Column(Float, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base, TimestampMixin):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    medicine = relationship("Medicine", back_populates="order_items")

class Prescription(Base, TimestampMixin):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_name = Column(String(255), nullable=False)
    diagnosis = Column(Text)
    issued_date = Column(String(50), nullable=False)
    valid_until = Column(String(50))
    status = Column(String(50), default="pending")  # pending, approved, rejected
    
    # Relationships
    user = relationship("User", back_populates="prescriptions")
    items = relationship("PrescriptionItem", back_populates="prescription")

class PrescriptionItem(Base, TimestampMixin):
    __tablename__ = "prescription_items"

    id = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    dosage = Column(String(100))
    duration = Column(String(100))
    instructions = Column(Text)
    
    # Relationships
    prescription = relationship("Prescription", back_populates="items")
    medicine = relationship("Medicine", back_populates="prescription_items") 