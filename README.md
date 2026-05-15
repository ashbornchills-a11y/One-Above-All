<div align="center">
  <h1>⚡ One Above All</h1>
  <p><b>Your Omniscient AI Screen Assistant</b></p>
  
  <p>
    <a href="https://github.com/ashbornchills-a11y/One-Above-All/stargazers"><img src="https://img.shields.io/github/stars/ashbornchills-a11y/One-Above-All?color=A6E3A1&style=for-the-badge" alt="Stars"></a>
    <a href="https://github.com/ashbornchills-a11y/One-Above-All/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-89B4FA?style=for-the-badge" alt="License"></a>
    <img src="https://img.shields.io/badge/Python-3.10+-F9E2AF?style=for-the-badge&logo=python&logoColor=black" alt="Python Version">
    <img src="https://img.shields.io/badge/Status-Production_Ready-CBA6F7?style=for-the-badge" alt="Status">
  </p>

  <p><i>Press a hotkey. Get intelligent answers about anything on your screen. Zero cost.</i></p>
</div>

<br/>

## 🎯 The Vision

**One Above All** bridges the gap between what you see and what you need to know. Whether you are coding, reading complex documents, or navigating UI elements, a single keyboard shortcut (`Shift + CapsLock + A`) summons a state-of-the-art AI model (Llama 3.3 70B) to analyze your screen and provide immediate, context-aware answers.

Designed with a sleek, non-intrusive UI and architected for performance, it runs silently in your system tray until you need it.

## ✨ Premium Features

- 🔍 **Omniscient Vision (OCR)**: High-performance, OpenCV-enhanced screen reading that captures text with extreme accuracy, even from images or videos.
- 🧠 **Elite Intelligence**: Powered by **Llama 3.3 70B** via the blazing-fast Groq API, delivering answers faster than you can type the question.
- 🎨 **Glassmorphism UI**: A beautifully crafted, draggable, dark-themed overlay built with `customtkinter`. It looks native and premium.
- ⚡ **Zero Friction**: Runs in the background (system tray). No clunky terminal windows. One hotkey activation.
- 💸 **100% Free Architecture**: Engineered to utilize the free tier of the Groq API, meaning zero running costs for enterprise-grade AI.

## 🏗️ Architecture

The codebase has been meticulously structured for scalability and maintainability:

```text
src/
├── core/
│   ├── ai_backend.py      # LLM integration & prompt engineering
│   ├── ocr_engine.py      # OpenCV preprocessing & Tesseract pipeline
│   └── screen_capture.py  # High-speed MSS frame grabbing
├── ui/
│   ├── overlay_window.py  # CustomTkinter glassmorphism UI
│   └── system_tray.py     # Background lifecycle management
└── utils/
    ├── config_manager.py  # .env & JSON settings state
    └── logger.py          # Professional rotation logging
```

## 🚀 Quick Setup

### Prerequisites
- **Python 3.10+**
- **Tesseract OCR**: 
  - Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
  - *Note: Remember to note your installation path if it differs from the default.*

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ashbornchills-a11y/One-Above-All.git
   cd One-Above-All
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   - Copy `.env.example` to `.env`.
   - Get your free API key from [Groq Console](https://console.groq.com/keys).
   - Add your key to the `.env` file:
     ```env
     GROQ_API_KEY=gsk_your_key_here
     ```

4. **Launch:**
   ```bash
   python app.py
   ```
   *The application will minimize to your system tray automatically.*

## ⚙️ Configuration

You can customize the application behavior by modifying `settings.json` (created automatically on first run):

```json
{
    "activation_hotkey": "shift+caps lock+a",
    "close_hotkey": "shift+caps lock+q",
    "tesseract_path": "C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
    "theme": "dark-blue",
    "overlay_alpha": 0.95
}
```

## 👨‍💻 Author

Built by **Aditya**.
- **Portfolio**: [portfolio-eu8d.vercel.app](https://portfolio-eu8d.vercel.app/)
- **Specialization**: Full-Stack Development | AI Automation | Bot Engineering

---
<div align="center">
  <i>If you find this project useful, consider giving it a ⭐</i>
</div>