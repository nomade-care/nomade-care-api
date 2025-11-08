# File: routers/audio_router.py

from fastapi import APIRouter, UploadFile, File
from controllers.audio_controller import AudioController
from dto.audio_dto import AudioAnalysisResult, ErrorResponse

router = APIRouter(
    prefix="/api/audio",
    tags=["Audio Emotion Detection"]
)

# Initialize controller
audio_controller = AudioController()


@router.post(
    "/analyze",
    response_model=AudioAnalysisResult,
    summary="Analyze audio emotion",
    description="""
    Upload an audio file and receive emotion analysis results.
    
    **Supported formats:** WAV, MP3, OGG, FLAC, M4A
    
    **Response includes:**
    - Primary detected emotion with confidence score
    - Top 3 emotion predictions
    - Processing time and timestamp
    - Unique audio identifier
    
    **Example response:**
    ```json
    {
        "audio_id": "123e4567-e89b-12d3-a456-426614174000",
        "detected_emotion": "happy",
        "confidence": 0.8532,
        "top_predictions": [
            {"emotion": "happy", "confidence": 0.8532},
            {"emotion": "excited", "confidence": 0.0921},
            {"emotion": "neutral", "confidence": 0.0312}
        ],
        "processing_time": 1.234,
        "timestamp": "2025-11-08T10:30:00"
    }
    ```
    """,
    responses={
        200: {
            "description": "Successful emotion analysis",
            "model": AudioAnalysisResult
        },
        400: {
            "description": "Invalid file or request",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }
)
async def analyze_audio(
    audio_file: UploadFile = File(..., description="Audio file to analyze")
) -> AudioAnalysisResult:
    """
    Analyze audio emotion and return detection results.
    
    Processes the uploaded audio file through an emotion detection model
    and returns the detected emotions with confidence scores.
    """
    return await audio_controller.analyze_audio(audio_file)