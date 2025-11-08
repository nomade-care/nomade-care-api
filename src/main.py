# File: src/main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import audio_router

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# --- Cria a instância principal do FastAPI ---
app = FastAPI(
    title="Audio Emotion Detection API",
    description="""
    Real-time audio emotion detection API using transformer-based models.
    
    ## Features
    - 🎵 Support for multiple audio formats (WAV, MP3, OGG, FLAC, M4A)
    - 🧠 Powered by Hugging Face transformer models
    - 📈 Top 3 emotion predictions with confidence scores
    - ⚡ Fast processing with pre-loaded models
    - 📊 Detailed response with processing metrics
    
    ## Usage
    Upload an audio file to `/api/audio/analyze` to receive emotion analysis.
    """,
    version="1.0.0",
    contact={
        "name": "Nomade Engenuity Team",
        "url": "https://nomadengenuity.com",
        "email": "support@nomadengenuity.com"
    },
    license_info={
        "name": "NomadEngenuity Proprietary - All rights reserved",
        "url": "https://nomadengenuity.com/license"
    },
    # Desativa documentação em produção
    docs_url="/docs" if os.getenv("ENV") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENV") != "production" else None
)

# --- Configuração de Middlewares (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:9002",
        os.getenv("FRONTEND_URL", "*")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Inclusão dos Roteadores ---
app.include_router(audio_router.router)

# --- Health Check Endpoints ---
@app.get("/", tags=["Health"])
async def root():
    """API health check endpoint."""
    return {
        "status": "healthy",
        "message": "Audio Emotion Detection API is running",
        "docs": "/docs" if os.getenv("ENV") != "production" else None
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check with service status."""
    return {
        "status": "healthy",
        "service": "audio-emotion-detection",
        "version": "1.0.0",
        "model_loaded": True
    }

# --- Startup Events ---
@app.on_event("startup")
async def startup_event():
    """Pré-carrega o modelo na inicialização para eliminar cold start."""
    from services.emotion_service import EmotionDetectionService
    
    # Pré-aquece o modelo
    service = EmotionDetectionService()
    service.load_model()
    
    print("[STARTUP] ✓ Emotion detection model pré-carregado")

