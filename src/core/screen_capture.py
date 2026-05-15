import mss
from PIL import Image
from ..utils.logger import logger

class ScreenCapture:
    """Handles high-performance screen capturing."""
    
    @staticmethod
    def capture_full_screen():
        """Captures the primary monitor."""
        try:
            with mss.mss() as sct:
                # monitor 1 is the primary monitor
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                
                # Convert to PIL Image
                img = Image.frombytes(
                    "RGB", 
                    screenshot.size, 
                    screenshot.bgra, 
                    "raw", 
                    "BGRX"
                )
                logger.info(f"Screen captured: {img.size[0]}x{img.size[1]}")
                return img
        except Exception as e:
            logger.error(f"Screen capture failed: {e}")
            return None

    @staticmethod
    def capture_region(left, top, width, height):
        """Captures a specific region of the screen."""
        try:
            with mss.mss() as sct:
                region = {"top": top, "left": left, "width": width, "height": height}
                screenshot = sct.grab(region)
                img = Image.frombytes(
                    "RGB", 
                    screenshot.size, 
                    screenshot.bgra, 
                    "raw", 
                    "BGRX"
                )
                return img
        except Exception as e:
            logger.error(f"Region capture failed: {e}")
            return None
