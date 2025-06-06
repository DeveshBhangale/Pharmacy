from sqlalchemy import Column, String, Float, Integer, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel, TimestampMixin

class User(BaseModel, TimestampMixin):
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(String, default="customer")  # customer, pharmacist, admin
    
    # Relationships
    prescriptions = relationship("Prescription", back_populates="user")
    orders = relationship("Order", back_populates="user")

class Medicine(BaseModel, TimestampMixin):
    __tablename__ = "medicines"
    
    name = Column(String, index=True, nullable=False)
    generic_name = Column(String, index=True)
    manufacturer = Column(String)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    category = Column(String, index=True)
    requires_prescription = Column(Boolean, default=False)
    image_url = Column(String)
    metadata = Column(JSON)  # For additional medicine details
    
    # Relationships
    inventory_items = relationship("InventoryItem", back_populates="medicine")
    order_items = relationship("OrderItem", back_populates="medicine")

class InventoryItem(BaseModel, TimestampMixin):
    __tablename__ = "inventory_items"
    
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    batch_number = Column(String, nullable=False)
    expiry_date = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    purchase_price = Column(Float, nullable=False)
    supplier = Column(String)
    
    # Relationships
    medicine = relationship("Medicine", back_populates="inventory_items")

class Prescription(BaseModel, TimestampMixin):
    __tablename__ = "prescriptions"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_name = Column(String)
    prescription_date = Column(String)
    image_url = Column(String)
    status = Column(String, default="pending")  # pending, verified, rejected
    notes = Column(String)
    
    # Relationships
    user = relationship("User", back_populates="prescriptions")
    prescription_items = relationship("PrescriptionItem", back_populates="prescription")

class PrescriptionItem(BaseModel, TimestampMixin):
    __tablename__ = "prescription_items"
    
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    dosage = Column(String)
    frequency = Column(String)
    duration = Column(String)
    
    # Relationships
    prescription = relationship("Prescription", back_populates="prescription_items")
    medicine = relationship("Medicine")

class Order(BaseModel, TimestampMixin):
    __tablename__ = "orders"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, processing, completed, cancelled
    payment_status = Column(String, default="pending")  # pending, paid, failed
    shipping_address = Column(String)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(BaseModel, TimestampMixin):
    __tablename__ = "order_items"
    
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    medicine = relationship("Medicine", back_populates="order_items") 