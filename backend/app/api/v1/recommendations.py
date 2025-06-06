from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
from datetime import datetime, UTC

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.pharmacy import User, Medicine, Prescription, PrescriptionItem

router = APIRouter()

# Load the trained model
try:
    model = tf.keras.models.load_model("app/ml/models/medicine_recommender.h5")
except:
    # Initialize a simple model for development
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(10,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(16, activation='softmax')
    ])

class RecommendationRequest(BaseModel):
    age: int
    gender: str
    medical_conditions: List[str]
    allergies: List[str]
    current_medications: List[int]  # List of medicine IDs

class RecommendationResponse(BaseModel):
    medicine_id: int
    name: str
    confidence_score: float
    reason: str

def preprocess_user_data(
    age: int,
    gender: str,
    medical_conditions: List[str],
    allergies: List[str],
    current_medications: List[int],
    db: Session
) -> np.ndarray:
    # Convert categorical data to numerical
    gender_encoded = 1 if gender.lower() == 'male' else 0
    
    # Get medicine embeddings
    medicine_embeddings = []
    for med_id in current_medications:
        medicine = db.query(Medicine).filter(Medicine.id == med_id).first()
        if medicine:
            # Simple embedding based on medicine category
            category_embedding = hash(medicine.category) % 10
            medicine_embeddings.append(category_embedding)
    
    # Pad or truncate medicine embeddings
    medicine_embeddings = medicine_embeddings[:5] + [0] * (5 - len(medicine_embeddings))
    
    # Combine all features
    features = [
        age / 100,  # Normalize age
        gender_encoded,
        len(medical_conditions) / 10,  # Normalize number of conditions
        len(allergies) / 10,  # Normalize number of allergies
    ] + medicine_embeddings
    
    return np.array(features).reshape(1, -1)

@router.post("/recommend", response_model=List[RecommendationResponse])
async def get_recommendations(
    *,
    db: Session = Depends(get_db),
    request: RecommendationRequest,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    # Preprocess user data
    user_data = preprocess_user_data(
        request.age,
        request.gender,
        request.medical_conditions,
        request.allergies,
        request.current_medications,
        db
    )
    
    # Get model predictions
    predictions = model.predict(user_data)[0]
    
    # Get top 5 medicine recommendations
    top_indices = np.argsort(predictions)[-5:][::-1]
    
    # Get medicine details
    recommendations = []
    for idx in top_indices:
        # In a real system, this would map to actual medicine IDs
        # For now, we'll use the index as a mock medicine ID
        medicine = db.query(Medicine).filter(Medicine.id == int(idx) + 1).first()
        if medicine:
            recommendations.append(
                RecommendationResponse(
                    medicine_id=medicine.id,
                    name=medicine.name,
                    confidence_score=float(predictions[idx]),
                    reason="Based on your medical history and current medications"
                )
            )
    
    return recommendations

@router.get("/similar/{medicine_id}", response_model=List[RecommendationResponse])
async def get_similar_medicines(
    *,
    db: Session = Depends(get_db),
    medicine_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    # Get the target medicine
    target_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not target_medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicine not found"
        )
    
    # Find similar medicines based on category and price range
    similar_medicines = db.query(Medicine).filter(
        Medicine.category == target_medicine.category,
        Medicine.id != medicine_id
    ).limit(5).all()
    
    recommendations = []
    for medicine in similar_medicines:
        # Calculate similarity score (simplified)
        price_diff = abs(medicine.price - target_medicine.price)
        similarity_score = 1.0 / (1.0 + price_diff)
        
        recommendations.append(
            RecommendationResponse(
                medicine_id=medicine.id,
                name=medicine.name,
                confidence_score=similarity_score,
                reason=f"Similar to {target_medicine.name} in the same category"
            )
        )
    
    return recommendations

@router.get("/personalized", response_model=List[RecommendationResponse])
async def get_personalized_recommendations(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    # Get user's prescription history
    prescriptions = db.query(Prescription).filter(
        Prescription.user_id == current_user.id,
        Prescription.status == "verified"
    ).all()
    
    # Extract medicine IDs from prescriptions
    medicine_ids = set()
    for prescription in prescriptions:
        for item in prescription.prescription_items:
            medicine_ids.add(item.medicine_id)
    
    # Get medicines from the same categories
    categories = db.query(Medicine.category).filter(
        Medicine.id.in_(medicine_ids)
    ).distinct().all()
    categories = [c[0] for c in categories]
    
    # Find similar medicines
    similar_medicines = db.query(Medicine).filter(
        Medicine.category.in_(categories),
        ~Medicine.id.in_(medicine_ids)  # Exclude already prescribed medicines
    ).limit(5).all()
    
    recommendations = []
    for medicine in similar_medicines:
        recommendations.append(
            RecommendationResponse(
                medicine_id=medicine.id,
                name=medicine.name,
                confidence_score=0.8,  # Placeholder score
                reason="Based on your prescription history"
            )
        )
    
    return recommendations 