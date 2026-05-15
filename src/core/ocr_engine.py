import cv2
import numpy as np
import pytesseract
from PIL import Image
from ..utils.logger import logger
from ..utils.config_manager import config

class OCREngine:
    """Handles text extraction from images using Tesseract OCR."""
    
    def __init__(self):
        self._setup_tesseract()

    def _setup_tesseract(self):
        """Configures the Tesseract executable path."""
        tesseract_path = config.get("tesseract_path")
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            try:
                version = pytesseract.get_tesseract_version()
                logger.info(f"Tesseract initialized (v{version})")
            except Exception as e:
                logger.error(f"Failed to initialize Tesseract at {tesseract_path}: {e}")
                logger.warning("Please ensure Tesseract OCR is installed and the path is correct in settings.json.")

    def extract_text(self, image: Image.Image) -> str:
        """Extracts text from a PIL Image with advanced preprocessing."""
        try:
            # Convert PIL image to OpenCV format
            img_array = np.array(image)
            
            # Convert RGB to BGR (OpenCV format) if needed, though grayscale doesn't strictly need it
            # But mss already returns BGRX, so let's handle the conversion cleanly
            if len(img_array.shape) == 3 and img_array.shape[2] == 4:
                # Drop alpha channel
                img_array = img_array[:, :, :3]
                
            gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            
            # Enhance image for OCR
            # 1. Scale image (improves OCR on small text)
            scaled = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            
            # 2. Denoise
            denoised = cv2.fastNlMeansDenoising(scaled, None, 10, 7, 21)
            
            # 3. Thresholding to make it purely black and white
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Run OCR on both preprocessed and raw grayscale to ensure we don't miss text
            text_raw = pytesseract.image_to_string(gray, lang='eng')
            text_processed = pytesseract.image_to_string(thresh, lang='eng')
            
            # Return the one with more characters (simple heuristic for better capture)
            best_text = text_processed if len(text_processed.strip()) > len(text_raw.strip()) else text_raw
            
            clean_text = best_text.strip()
            logger.info(f"Extracted {len(clean_text)} characters.")
            
            return clean_text
            
        except Exception as e:
            logger.error(f"OCR Extraction error: {e}")
            return ""
