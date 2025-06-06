from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Any
from pydantic import BaseModel
from datetime import datetime, UTC
import boto3
from botocore.exceptions import ClientError
import os

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.config import settings
from app.models.pharmacy import User, Prescription, PrescriptionItem, Medicine

router = APIRouter()

# Pydantic models
class PrescriptionItemBase(BaseModel):
    medicine_id: int
    dosage: str
    frequency: str
    duration: str

class PrescriptionBase(BaseModel):
    doctor_name: str
    prescription_date: str
    notes: str | None = None

class PrescriptionCreate(PrescriptionBase):
    items: List[PrescriptionItemBase]

class PrescriptionUpdate(BaseModel):
    status: str
    notes: str | None = None

class PrescriptionItemResponse(PrescriptionItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PrescriptionResponse(PrescriptionBase):
    id: int
    user_id: int
    image_url: str | None
    status: str
    created_at: datetime
    updated_at: datetime
    items: List[PrescriptionItemResponse]

    class Config:
        from_attributes = True

# S3 client for file uploads
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

async def upload_file_to_s3(file: UploadFile, user_id: int) -> str:
    try:
        file_extension = os.path.splitext(file.filename)[1]
        s3_key = f"prescriptions/{user_id}/{datetime.now(UTC).timestamp()}{file_extension}"
        
        # Upload file to S3
        s3_client.upload_fileobj(
            file.file,
            settings.AWS_S3_BUCKET,
            s3_key,
            ExtraArgs={'ContentType': file.content_type}
        )
        
        # Generate presigned URL for the uploaded file
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_S3_BUCKET,
                'Key': s3_key
            },
            ExpiresIn=3600  # URL expires in 1 hour
        )
        
        return url
    except ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )

@router.post("/upload", response_model=PrescriptionResponse)
async def upload_prescription(
    *,
    db: Session = Depends(get_db),
    prescription_in: PrescriptionCreate,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    # Upload prescription image to S3
    image_url = await upload_file_to_s3(file, current_user.id)
    
    # Create prescription record
    prescription = Prescription(
        user_id=current_user.id,
        doctor_name=prescription_in.doctor_name,
        prescription_date=prescription_in.prescription_date,
        image_url=image_url,
        status="pending",
        notes=prescription_in.notes
    )
    db.add(prescription)
    db.flush()  # Get prescription ID without committing
    
    # Create prescription items
    for item in prescription_in.items:
        # Verify medicine exists
        medicine = db.query(Medicine).filter(Medicine.id == item.medicine_id).first()
        if not medicine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medicine with ID {item.medicine_id} not found"
            )
        
        prescription_item = PrescriptionItem(
            prescription_id=prescription.id,
            medicine_id=item.medicine_id,
            dosage=item.dosage,
            frequency=item.frequency,
            duration=item.duration
        )
        db.add(prescription_item)
    
    db.commit()
    db.refresh(prescription)
    return prescription

@router.get("/", response_model=List[PrescriptionResponse])
async def read_prescriptions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    prescriptions = db.query(Prescription).filter(
        Prescription.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return prescriptions

@router.get("/{prescription_id}", response_model=PrescriptionResponse)
async def read_prescription(
    *,
    db: Session = Depends(get_db),
    prescription_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    prescription = db.query(Prescription).filter(
        Prescription.id == prescription_id,
        Prescription.user_id == current_user.id
    ).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    return prescription

@router.put("/{prescription_id}", response_model=PrescriptionResponse)
async def update_prescription(
    *,
    db: Session = Depends(get_db),
    prescription_id: int,
    prescription_in: PrescriptionUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    prescription = db.query(Prescription).filter(
        Prescription.id == prescription_id,
        Prescription.user_id == current_user.id
    ).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    for field, value in prescription_in.model_dump().items():
        setattr(prescription, field, value)
    
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return prescription

@router.delete("/{prescription_id}")
async def delete_prescription(
    *,
    db: Session = Depends(get_db),
    prescription_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    prescription = db.query(Prescription).filter(
        Prescription.id == prescription_id,
        Prescription.user_id == current_user.id
    ).first()
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found"
        )
    
    # Delete prescription items first
    db.query(PrescriptionItem).filter(
        PrescriptionItem.prescription_id == prescription_id
    ).delete()
    
    # Delete prescription
    db.delete(prescription)
    db.commit()
    
    return {"status": "success"} 