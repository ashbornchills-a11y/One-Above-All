import os
import json
from pathlib import Path
from dotenv import load_dotenv
from .logger import logger

class ConfigManager:
    """Manages application configuration, secrets, and persistent settings."""
    
    DEFAULT_SETTINGS = {
        "activation_hotkey": "shift+caps lock+a",
        "close_hotkey": "shift+caps lock+q",
        "tesseract_path": r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        "ai_model": "llama-3.3-70b-versatile",
        "overlay_alpha": 0.95,
        "theme": "dark-blue"
    }

    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.settings_path = self.base_path / "settings.json"
        self.env_path = self.base_path / ".env"
        
        # Load environment variables
        load_dotenv(self.env_path)
        
        # Load or create settings
        self.settings = self.load_settings()
        
        # Override with environment variables if present
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            logger.warning("GROQ_API_KEY not found in .env file!")

    def load_settings(self):
        """Loads settings from settings.json or creates defaults."""
        if self.settings_path.exists():
            try:
                with open(self.settings_path, 'r') as f:
                    return {**self.DEFAULT_SETTINGS, **json.load(f)}
            except Exception as e:
                logger.error(f"Failed to load settings: {e}")
                return self.DEFAULT_SETTINGS
        else:
            self.save_settings(self.DEFAULT_SETTINGS)
            return self.DEFAULT_SETTINGS

    def save_settings(self, settings=None):
        """Saves settings to settings.json."""
        if settings:
            self.settings = settings
        try:
            with open(self.settings_path, 'w') as f:
                json.dump(self.settings, f, indent=4)
            logger.info("Settings saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")

    def get(self, key, default=None):
        """Retrieves a setting value."""
        return self.settings.get(key, self.DEFAULT_SETTINGS.get(key, default))

# Global config instance
config = ConfigManager()
