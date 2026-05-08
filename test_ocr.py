# test_ocr.py
import pytesseract
from config import TESSERACT_PATH

print(f"Using Tesseract at: {TESSERACT_PATH}")
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

try:
    version = pytesseract.get_tesseract_version()
    print(f"✅ Tesseract version: {version}")
    print("Tesseract is working!")
except Exception as e:
    print(f"❌ Tesseract error: {e}")
    print("\nTry these fixes:")
    print("1. Reinstall Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
    print("2. Make sure to check 'Add to PATH' during installation")
    print("3. Or manually add the install folder to System PATH")