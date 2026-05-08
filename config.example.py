# config.example.py
import os

# Groq API (COMPLETELY FREE - No credit card needed)
# Get your free key at: https://console.groq.com/keys
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"  # Replace with your key
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Hotkey Configuration
ACTIVATION_HOTKEY = "shift+caps lock+a"  # Hold Shift + CapsLock + A
CLOSE_OVERLAY_HOTKEY = "shift+caps lock+q"  # Hold Shift + CapsLock + Q

# OCR Configuration
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Screen Capture Settings
CAPTURE_REGION = None  # None = full screen

# AI Model Settings
AI_MODEL = "llama-3.3-70b-versatile"  # Groq's most powerful free model