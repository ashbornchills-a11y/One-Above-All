import sys
import threading
import keyboard
import time

from src.utils.logger import logger
from src.utils.config_manager import config
from src.core.screen_capture import ScreenCapture
from src.core.ocr_engine import OCREngine
from src.core.ai_backend import AIBackend
from src.ui.overlay_window import OverlayWindow
from src.ui.system_tray import SystemTrayIcon

class AppOrchestrator:
    """Main application controller linking all components."""
    
    def __init__(self):
        logger.info("Initializing One Above All...")
        
        self.is_processing = False
        
        # Initialize Core Components
        self.ocr_engine = OCREngine()
        self.ai_backend = AIBackend()
        
        # Initialize UI Components
        self.overlay = OverlayWindow(
            copy_callback=self._on_copy,
            close_callback=self._on_close_overlay
        )
        self.tray = SystemTrayIcon(self)
        
        self.setup_hotkeys()
        logger.info("Application initialized successfully.")

    def setup_hotkeys(self):
        """Registers global keyboard shortcuts."""
        activation_key = config.get("activation_hotkey", "shift+caps lock+a")
        close_key = config.get("close_hotkey", "shift+caps lock+q")
        
        try:
            keyboard.add_hotkey(activation_key, self.on_activation)
            keyboard.add_hotkey(close_key, self.hide_overlay)
            logger.info(f"Hotkeys registered: Activate [{activation_key}], Close [{close_key}]")
        except Exception as e:
            logger.error(f"Failed to register hotkeys: {e}")
            logger.warning("Try running the application as Administrator.")

    def on_activation(self):
        """Triggered when the activation hotkey is pressed."""
        if self.is_processing:
            logger.info("Already processing. Ignoring hotkey.")
            return
            
        self.is_processing = True
        logger.info("Activation hotkey pressed. Starting pipeline.")
        
        # UI updates must happen in the main thread
        self.overlay.root.after(0, lambda: self.overlay.update_status("Capturing Screen...", "#F9E2AF")) # Yellow
        if not self.overlay.is_visible:
             self.overlay.root.after(0, self.overlay.show)
        
        # Run heavy processing in background
        threading.Thread(target=self._processing_pipeline, daemon=True).start()

    def _processing_pipeline(self):
        """The core logic flow: Capture -> OCR -> AI -> UI"""
        try:
            # 1. Capture
            time.sleep(0.2) # Slight delay to let UI updates settle
            img = ScreenCapture.capture_full_screen()
            if not img:
                self._update_ui_error("Failed to capture screen.")
                return
                
            # 2. OCR
            self.overlay.root.after(0, lambda: self.overlay.update_status("Reading Text...", "#89B4FA")) # Blue
            text = self.ocr_engine.extract_text(img)
            
            if len(text) < 10:
                self._update_ui_error("No readable text found on screen.")
                return
                
            # 3. AI Query
            self.overlay.root.after(0, lambda: self.overlay.update_status("AI is Thinking...", "#CBA6F7")) # Purple
            answer = self.ai_backend.query(text)
            
            # 4. Display
            self.overlay.root.after(0, lambda: self._display_answer(answer))
            
        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            self._update_ui_error("An unexpected error occurred.")
        finally:
            self.is_processing = False

    def _update_ui_error(self, message):
        """Helper to show errors safely from background thread."""
        def update():
            self.overlay.set_content(f"❌ **Error**\n\n{message}")
            self.overlay.update_status("Error", "#F38BA8") # Red
            self.overlay.show()
        self.overlay.root.after(0, update)

    def _display_answer(self, answer):
        """Helper to show success safely from background thread."""
        self.overlay.set_content(answer)
        self.overlay.update_status("Answer Ready", "#A6E3A1") # Green
        self.overlay.show()

    def show_overlay(self):
        """Shows the overlay (used by tray icon)."""
        self.overlay.show()

    def hide_overlay(self):
        """Hides the overlay (used by hotkey)."""
        self.overlay.root.after(0, self.overlay.hide)

    def _on_copy(self):
        """Callback for when user clicks Copy."""
        logger.info("Content copied to clipboard.")

    def _on_close_overlay(self):
        """Callback for when user clicks Close."""
        logger.info("Overlay closed by user.")

    def run(self):
        """Starts the application."""
        print(r"""
    ⚡ ONE ABOVE ALL ⚡
    AI-Powered Screen Assistant
    Starting up...
        """)
        
        # Check API key before starting
        if not config.groq_api_key or config.groq_api_key == "YOUR_GROQ_API_KEY_HERE":
            logger.critical("Groq API Key is not configured!")
            
            def show_key_error():
                self._update_ui_error("API Key missing.\n1. Get free key at: console.groq.com/keys\n2. Add it to .env file.")
            
            # Show error on startup
            self.overlay.root.after(1000, show_key_error)
            
        self.tray.run()
        
        try:
            # Tkinter mainloop must run in the main thread
            self.overlay.run()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received.")
            self.quit()

    def quit(self):
        """Cleans up and exits."""
        logger.info("Shutting down...")
        self.tray.stop()
        try:
            keyboard.unhook_all()
        except:
            pass
        self.overlay.root.quit()
        sys.exit(0)

if __name__ == "__main__":
    app = AppOrchestrator()
    app.run()
