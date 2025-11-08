# File: controllers/audio_controller.py

import uuid
from fastapi import UploadFile, HTTPException
from services.emotion_service import EmotionDetectionService
from dto.audio_dto import AudioAnalysisResult


class AudioController:
    """Controller for audio emotion detection endpoints."""
    
    def __init__(self):
        """Initialize controller with emotion detection service."""
        self.emotion_service = EmotionDetectionService()
    
    async def analyze_audio(self, audio_file: UploadFile) -> AudioAnalysisResult:
        """
        Analyze audio file and return emotion detection results.

        Args:
            audio_file: Uploaded audio file

        Returns:
            AudioAnalysisResult with emotion predictions

        Raises:
            HTTPException: If file validation or processing fails
        """
        # Validate file type
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {audio_file.content_type}. Must be audio file."
            )

        # Generate unique ID for this analysis
        audio_id = str(uuid.uuid4())

        # Read audio bytes
        audio_bytes = await audio_file.read()

        if len(audio_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty audio file"
            )

        try:
            # Process audio
            result = await self.emotion_service.process_audio(audio_bytes, audio_id)
            return result

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Audio processing failed: {str(e)}"
            )

