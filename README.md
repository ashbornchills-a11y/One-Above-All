# ⚡ One Above All - AI Screen Assistant

> Press a hotkey. Get AI answers. Any screen. Zero cost.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 🎯 What It Does

One Above All captures your screen, reads text via OCR, sends it to AI, and displays the answer in a minimal overlay - all triggered by one keyboard shortcut.

## ✨ Features

- 🔍 Full Screen OCR - Reads any text visible on your monitor
- 🤖 AI-Powered Answers - Uses Llama 3.3 70B via Groq (free API)
- 🎨 Minimal Overlay - Subtle, non-intrusive display
- ⌨️ Custom Hotkeys - Activate with Shift+CapsLock+A
- 💰 100% Free - No paid APIs, no hidden costs
- 🖥️ Works on Any Screen - Browsers, PDFs, apps, anywhere

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12 |
| Screen Capture | MSS |
| OCR Engine | Tesseract 5.5 |
| AI Backend | Groq API (Llama 3.3 70B) |
| GUI Framework | Tkinter |
| Image Processing | OpenCV + NumPy |

## 🚀 Quick Setup

### Prerequisites
- Python 3.10+
- Tesseract OCR

### Installation

```bash
# Clone the repository
git clone https://github.com/ashbornchills-a11y/One-Above-All.git
cd One-Above-All

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR
# Download: https://github.com/UB-Mannheim/tesseract/wiki
# IMPORTANT: Check "Add to PATH" during installation

# Get free Groq API key
# 1. Go to https://console.groq.com
# 2. Sign up (free, no credit card)
# 3. Create API key
# 4. Copy config.example.py to config.py and paste your key

# Run it
python main.py