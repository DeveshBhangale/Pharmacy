from typing import List, Dict, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from ..models.models import Medicine, Order, OrderItem
from ..schemas.schemas import MedicineResponse

class RecommendationEngine:
    def __init__(self, db: Session):
        self.db = db
        self.tfidf = TfidfVectorizer(stop_words='english')
        
    def _prepare_content_features(self, medicines: List[Medicine]) -> np.ndarray:
        """
        Prepare content features for content-based filtering using medicine descriptions
        """
        descriptions = [f"{m.name} {m.description} {m.category}" for m in medicines]
        return self.tfidf.fit_transform(descriptions)
    
    def _get_user_medicine_matrix(self, user_id: int) -> Dict[int, List[float]]:
        """
        Create user-medicine interaction matrix for collaborative filtering
        """
        # Get all orders for the user
        orders = self.db.query(Order).filter(Order.user_id == user_id).all()
        
        # Create medicine rating dictionary
        medicine_ratings = {}
        for order in orders:
            for item in order.items:
                if item.medicine_id not in medicine_ratings:
                    medicine_ratings[item.medicine_id] = []
                # Use quantity as an implicit rating
                medicine_ratings[item.medicine_id].append(float(item.quantity))
        
        # Average the ratings
        return {
            med_id: [sum(ratings) / len(ratings)]
            for med_id, ratings in medicine_ratings.items()
        }
    
    def get_content_based_recommendations(
        self,
        medicine_id: int,
        num_recommendations: int = 5
    ) -> List[MedicineResponse]:
        """
        Get content-based recommendations based on medicine description similarity
        """
        # Get all medicines
        medicines = self.db.query(Medicine).all()
        if not medicines:
            return []
            
        # Prepare features
        content_features = self._prepare_content_features(medicines)
        
        # Find the index of the target medicine
        target_idx = None
        for idx, med in enumerate(medicines):
            if med.id == medicine_id:
                target_idx = idx
                break
                
        if target_idx is None:
            return []
            
        # Calculate similarity scores
        similarity_scores = cosine_similarity(
            content_features[target_idx:target_idx+1],
            content_features
        ).flatten()
        
        # Get indices of top similar medicines
        similar_indices = similarity_scores.argsort()[::-1][1:num_recommendations+1]
        
        # Convert to MedicineResponse
        recommendations = []
        for idx in similar_indices:
            med = medicines[idx]
            recommendations.append(
                MedicineResponse(
                    id=med.id,
                    name=med.name,
                    description=med.description,
                    price=med.price,
                    quantity=med.quantity,
                    category=med.category,
                    similarity_score=float(similarity_scores[idx])
                )
            )
            
        return recommendations
    
    def get_collaborative_recommendations(
        self,
        user_id: int,
        num_recommendations: int = 5
    ) -> List[MedicineResponse]:
        """
        Get collaborative filtering recommendations based on user purchase history
        """
        # Get user-medicine matrix
        user_matrix = self._get_user_medicine_matrix(user_id)
        if not user_matrix:
            return []
            
        # Get all medicines
        all_medicines = self.db.query(Medicine).all()
        if not all_medicines:
            return []
            
        # Calculate average rating for each medicine
        medicine_scores = {}
        for medicine in all_medicines:
            if medicine.id not in user_matrix:  # Only recommend unseen medicines
                # Calculate similarity with purchased medicines
                similarity_sum = 0
                weight_sum = 0
                
                for purchased_id, rating in user_matrix.items():
                    # Simple similarity metric based on category
                    similarity = 1.0 if medicine.category == purchased_id else 0.5
                    similarity_sum += similarity * rating[0]
                    weight_sum += similarity
                    
                if weight_sum > 0:
                    medicine_scores[medicine.id] = similarity_sum / weight_sum
        
        # Sort medicines by score
        sorted_medicines = sorted(
            medicine_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:num_recommendations]
        
        # Convert to MedicineResponse
        recommendations = []
        for med_id, score in sorted_medicines:
            med = next((m for m in all_medicines if m.id == med_id), None)
            if med:
                recommendations.append(
                    MedicineResponse(
                        id=med.id,
                        name=med.name,
                        description=med.description,
                        price=med.price,
                        quantity=med.quantity,
                        category=med.category,
                        similarity_score=float(score)
                    )
                )
                
        return recommendations
    
    def get_hybrid_recommendations(
        self,
        user_id: int,
        medicine_id: Optional[int] = None,
        num_recommendations: int = 5
    ) -> List[MedicineResponse]:
        """
        Get hybrid recommendations combining both content-based and collaborative filtering
        """
        content_recs = []
        if medicine_id:
            content_recs = self.get_content_based_recommendations(
                medicine_id,
                num_recommendations
            )
            
        collab_recs = self.get_collaborative_recommendations(
            user_id,
            num_recommendations
        )
        
        # Combine and deduplicate recommendations
        seen_ids = set()
        hybrid_recs = []
        
        # Alternate between content and collaborative recommendations
        content_idx = 0
        collab_idx = 0
        
        while len(hybrid_recs) < num_recommendations:
            # Add content-based recommendation
            if content_idx < len(content_recs):
                rec = content_recs[content_idx]
                if rec.id not in seen_ids:
                    hybrid_recs.append(rec)
                    seen_ids.add(rec.id)
                content_idx += 1
                
            # Add collaborative recommendation
            if collab_idx < len(collab_recs):
                rec = collab_recs[collab_idx]
                if rec.id not in seen_ids:
                    hybrid_recs.append(rec)
                    seen_ids.add(rec.id)
                collab_idx += 1
                
            # Break if we've exhausted both recommendation sources
            if content_idx >= len(content_recs) and collab_idx >= len(collab_recs):
                break
                
        return hybrid_recs[:num_recommendations] 