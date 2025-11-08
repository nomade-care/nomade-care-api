<div align="center">

<img src="https://nomadcare.vercel.app/nomadcare-logo.png" alt="NomadCare Logo" width="300">

</div>

# NomadCare API - Audio Emotion Detection

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121+-green.svg)](https://fastapi.tiangolo.com/)

A powerful REST API for real-time audio emotion detection using state-of-the-art machine learning models. Built with FastAPI, this service analyzes audio files to identify emotional content such as happiness, sadness, anger, and more.

## Table of Contents

- [Features](#features)
- [Built With](#built-with)
- [Supported Audio Formats](#supported-audio-formats)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [API Usage Guidelines](#api-usage-guidelines)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Development](#development)
- [Roadmap](#roadmap)
- [FAQ](#faq)
- [Support](#support)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Authors](#authors)

## Features

- **Real-time Emotion Detection**: Upload audio files and receive instant emotion analysis
- **AI-Powered Insights**: LLM-generated human-readable interpretations with emojis
- **High Accuracy**: Powered by Hugging Face transformers and specialized audio models
- **RESTful API**: Clean, documented endpoints using FastAPI
- **Audio Format Support**: Handles various audio formats with automatic resampling
- **Confidence Scores**: Provides probability scores for each detected emotion
- **Asynchronous Processing**: Non-blocking requests for better performance
- **Docker Ready**: Easy containerization for deployment

## 🛠️ Built With

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework for building APIs
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) - State-of-the-art ML models
- [Librosa](https://librosa.org/) - Audio and music processing library
- [PyTorch](https://pytorch.org/) - Deep learning framework
- [Uvicorn](https://www.uvicorn.org/) - Lightning-fast ASGI server
- [SpeechBrain](https://speechbrain.github.io/) - Speech processing toolkit

## 🎵 Supported Audio Formats

The API supports various audio formats including:
- WAV
- MP3
- FLAC
- OGG
- M4A

Audio files are automatically resampled to 16kHz for optimal model performance.

## Prerequisites

- Python 3.13 or higher
- pip or uv package manager
- Git (for cloning the repository)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nomade-care/nomade-care-api.git
   cd nomade-care-api
   ```

2. **Install dependencies using uv (recommended):**
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -e .
   ```

3. **Set up environment variables:**
   Copy `.env.example` to `.env` and fill in your values:
   ```bash
   cp .env.example .env
   ```

   Required environment variables:
   ```env
   # Hugging Face Configuration
   HF_HUB_DISABLE_IMPLICIT_TOKEN=1
   HF_TOKEN=your_huggingface_token_here

   # Application Settings
   ENV=development
   HOST=0.0.0.0
   PORT=8000
   RELOAD=true

   # Frontend URL (for CORS)
   FRONTEND_URL=http://localhost:3000
   ```

## Usage

### Running the Server

Start the API server:

```bash
python run.py
```

The server will start on `http://localhost:8000` by default.

### API Endpoints

#### POST /api/audio/analyze

Upload an audio file for emotion analysis.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `audio` (file)

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/api/audio/analyze" \
     -F "audio=@/path/to/your/audio.wav"
```

**Response:**
```json
{
  "audio_id": "unique-id",
  "detected_emotion": "happy",
  "confidence": 0.85,
  "top_predictions": [
    {
      "emotion": "happy",
      "confidence": 0.85
    },
    {
      "emotion": "sad",
      "confidence": 0.12
    }
  ],
  "processing_time": 2.34,
  "timestamp": "2025-11-08T10:15:30.123456",
  "insights": "🏥 Clinical Assessment:\nPrimary Emotion: Happiness (85%)\nProfile: High valence positive affect with moderate arousal\nBehavioral Indicators: Tone elevation, rhythmic speech patterns\nPsychological Context: Possible social engagement or achievement satisfaction\nRecommendations: Monitor for sustained positive affect"
}
```

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

## 📋 API Usage Guidelines

- **Maximum file size**: 50MB
- **Supported sample rates**: Auto-converted to 16kHz for optimal performance
- **Rate limit**: 100 requests per minute (configurable)
- **Response time**: Typically <2 seconds for audio files <10MB
- **Authentication**: API token required for production use
- **Content-Type**: Use `multipart/form-data` for file uploads

## Configuration

The application can be configured using environment variables:

- `HF_HUB_DISABLE_IMPLICIT_TOKEN`: Disable implicit token for Hugging Face Hub (set to `1`)
- `HF_TOKEN`: Your Hugging Face API token for accessing models
- `ENV`: Environment mode (`development` or `production`)
- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `8000`)
- `RELOAD`: Enable auto-reload for development (default: `true` in dev, `false` in prod)
- `FRONTEND_URL`: Frontend URL for CORS configuration

## 🚀 Deployment

### Local Deployment
```bash
python run.py
```

### Using Docker
```bash
# Build the image
docker build -t nomadcare-audio-emotion-detector .

# Run the container
docker run -p 8000:8000 nomadcare-audio-emotion-detector
```

### Cloud Deployment
The API can be deployed to:
- **AWS**: Lambda, EC2, or ECS
- **Google Cloud**: Cloud Run or App Engine
- **Azure**: Functions or App Service
- **Heroku**: Direct deployment
- **DigitalOcean**: App Platform

### Production Considerations
- Set `RELOAD=false` in production
- Configure proper logging
- Set up monitoring and alerts
- Use environment-specific configurations

## Development

### Project Structure

```
nomade-care-api/
├── controllers/          # Request handlers
├── dto/                  # Data transfer objects
├── routers/              # API route definitions
├── services/             # Business logic
├── src/                  # Main application code
├── data/                 # Sample data
├── output/               # Generated outputs
├── run.py                # Application entry point
├── pyproject.toml        # Project configuration
├── uv.lock               # Dependency lock file
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── LICENSE               # Apache 2.0 License
└── CONTRIBUTING.md       # Contributing guidelines & contributors
```

### Running Tests

```bash
# Install test dependencies
uv sync --dev

# Run tests
pytest
```

### Code Quality

```bash
# Lint code
flake8

# Format code
black .
```

## 🗺️ Roadmap

- [ ] Real-time audio streaming support
- [ ] Batch processing for multiple files
- [ ] Additional emotion models (multilingual support)
- [ ] Web dashboard for visualization
- [ ] Mobile SDK for iOS/Android
- [ ] Integration with popular audio platforms
- [ ] Advanced analytics and reporting

## ❓ FAQ

**Q: The API returns an error for my audio file?**  
A: Ensure your audio file is in a supported format (WAV, MP3, FLAC, OGG, M4A) and under 50MB.

**Q: How accurate is the emotion detection?**  
A: Accuracy varies by emotion and audio quality, typically 70-90% for clear speech in optimal conditions.

**Q: Can I use this for real-time streaming?**  
A: Currently supports file uploads; real-time streaming support is planned for future versions.

**Q: What emotions can be detected?**  
A: The model detects emotions like happy, sad, angry, fearful, disgusted, surprised, and neutral.

**Q: Is the API free to use?**  
A: The API is open-source. Usage costs may apply for cloud deployments or hosted services.

## 📞 Support

If you have questions or need help:

- 📧 **Email**: nomadengenuity@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/nomade-care/nomade-care-api/issues)
- 📖 **Documentation**: [Full API Docs](https://nomadcare.vercel.app/docs)

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

We would like to thank:

- **Hugging Face** for providing excellent ML models and the transformers library
- **FastAPI** community for the amazing web framework
- **PyTorch** team for the powerful deep learning framework
- **Librosa** contributors for audio processing tools
- All open-source contributors who make projects like this possible

## Authors

- **NomadCare** - *Initial work*

---

*Built with ❤️ using FastAPI and Hugging Face Transformers*
