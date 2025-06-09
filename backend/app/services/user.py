from typing import Optional
from sqlalchemy.orm import Session
from ..models.models import User
from ..core.hashing import get_password_hash, verify_password
from .base import BaseService
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "customer"

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None

class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, *, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            role=obj_in.role,
            is_active=True
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def authenticate(self, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        return user.is_active
    
    def is_superuser(self, user: User) -> bool:
        return user.role == "admin" 