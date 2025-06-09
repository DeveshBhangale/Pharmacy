from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,  # Enable connection pool "pre-ping" feature
    pool_size=5,  # Set initial pool size
    max_overflow=10,  # Allow up to 10 connections beyond pool_size
    pool_timeout=30,  # Timeout after 30 seconds waiting for a connection
    pool_recycle=1800,  # Recycle connections after 30 minutes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 