# File: run.py (in project root)

"""
#!/usr/bin/env python3

Production entry point for the audio emotion detection API.

Usage:
    python run.py
"""

import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    # Run the application
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=os.getenv("RELOAD", "false").lower() == "true"
    )