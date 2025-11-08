# File: dto/audio_dto.py

from pydantic import BaseModel, Field
from typing import List, Optional


class EmotionPrediction(BaseModel):
    """Single emotion prediction with confidence score."""
    emotion: str = Field(..., description="Detected emotion label")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class AudioAnalysisResult(BaseModel):
    """Complete audio analysis result."""
    audio_id: str = Field(..., description="Unique audio identifier")
    detected_emotion: str = Field(..., description="Primary detected emotion")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Primary confidence score")
    top_predictions: List[EmotionPrediction] = Field(..., description="Top 3 emotion predictions")
    processing_time: float = Field(..., description="Processing time in seconds")
    timestamp: str = Field(..., description="Analysis timestamp")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
