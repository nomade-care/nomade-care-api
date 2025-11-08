# File: services/emotion_service.py

import time
import io
from datetime import datetime
import librosa
from transformers import pipeline
from dto.audio_dto import AudioAnalysisResult, EmotionPrediction
from services.llm_service import LLMService


class EmotionDetectionService:
    """Service for audio emotion detection using transformer models."""
    
    def __init__(self, model_name: str = "Hatman/audio-emotion-detection", llm_model: str = "qwen2.5:1.5b"):
        """
        Initialize emotion detection service.

        Args:
            model_name: HuggingFace model identifier
            llm_model: Ollama model for insights generation
        """
        self.model_name = model_name
        self.pipe = None
        self.llm_service = LLMService(llm_model)
        
    def load_model(self) -> None:
        """Load the emotion detection model pipeline."""
        if self.pipe is None:
            self.pipe = pipeline("audio-classification", model=self.model_name)
    
    async def process_audio(self, audio_bytes: bytes, audio_id: str) -> AudioAnalysisResult:
        """
        Process audio and return emotion analysis.
        
        Args:
            audio_bytes: Raw audio file bytes
            audio_id: Unique identifier for the audio
            
        Returns:
            AudioAnalysisResult with emotion predictions
            
        Raises:
            Exception: If processing fails
        """
        start_time = time.time()
        
        # Load and resample audio to 16kHz for model compatibility
        audio_data, sample_rate = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000
        )
        
        # Ensure model is loaded
        self.load_model()
        
        # Predict emotions
        predictions = self.pipe({
            "raw": audio_data,
            "sampling_rate": sample_rate
        })
        
        # Build result
        processing_time = time.time() - start_time
        
        # Convert predictions to dict format for LLM
        emotions_dict = [
            {"label": pred['label'], "score": round(pred['score'], 4)}
            for pred in predictions[:5]  # Top 5 for better context
        ]

        # Generate LLM insights
        try:
            insights = await self.llm_service.generate_insights(emotions_dict)
        except Exception as e:
            insights = f"🤔 Emotion analysis completed. AI insights temporarily unavailable. Error: {str(e)}"

        result = AudioAnalysisResult(
            audio_id=audio_id,
            detected_emotion=predictions[0]['label'],
            confidence=round(predictions[0]['score'], 4),
            top_predictions=[
                EmotionPrediction(
                    emotion=pred['label'],
                    confidence=round(pred['score'], 4)
                )
                for pred in predictions[:3]
            ],
            processing_time=round(processing_time, 3),
            timestamp=datetime.now().isoformat(),
            insights=insights
        )

        return result