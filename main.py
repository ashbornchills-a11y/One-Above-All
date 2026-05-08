# main.py
import time
import threading
import keyboard
import mss
import pytesseract
import requests
import json
from PIL import Image
import tkinter as tk
from tkinter import ttk
import numpy as np
import cv2
import sys
import os

# Import config
from config import *

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

class OneAboveAll:
    def __init__(self):
        """Initialize the One Above All AI Assistant"""
        self.is_processing = False
        self.overlay_window = None
        
        print("[One Above All] Initializing...")
        print(f"[One Above All] Tesseract v{pytesseract.get_tesseract_version()} ready")
        print(f"[One Above All] AI Backend: Groq (FREE)")
        print(f"[One Above All] Model: {AI_MODEL}")
        
        self.create_overlay_window()
        self.register_hotkeys()
        
        print(f"\n[One Above All] ✅ READY!")
        print(f"[One Above All] Press {ACTIVATION_HOTKEY} to scan screen")
        print(f"[One Above All] Press {CLOSE_OVERLAY_HOTKEY} to close overlay")
        print("[One Above All] 💰 All API calls are 100% FREE\n")
    
    def create_overlay_window(self):
        """Create a sleek transparent overlay window"""
        self.overlay = tk.Tk()
        self.overlay.title("One Above All")
        
        # Window settings
        self.overlay.attributes('-topmost', True)
        self.overlay.attributes('-alpha', 0.93)
        self.overlay.overrideredirect(True)
        self.overlay.configure(bg='#1a1a2e')
        
        # Position in bottom-right corner
        screen_w = self.overlay.winfo_screenwidth()
        screen_h = self.overlay.winfo_screenheight()
        win_w = 480
        win_h = 400
        x = screen_w - win_w - 25
        y = screen_h - win_h - 50
        
        self.overlay.geometry(f"{win_w}x{win_h}+{x}+{y}")
        
        # Make it slightly rounded look (using a frame)
        main_frame = tk.Frame(
            self.overlay,
            bg='#1a1a2e',
            highlightbackground='#00ff88',
            highlightthickness=1
        )
        main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Title bar
        title_frame = tk.Frame(main_frame, bg='#16213e', height=40)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="⚡ ONE ABOVE ALL",
            font=('Segoe UI', 11, 'bold'),
            bg='#16213e',
            fg='#00ff88'
        )
        title_label.pack(side=tk.LEFT, padx=15, pady=8)
        
        # Status indicator
        self.status_label = tk.Label(
            title_frame,
            text="● Ready",
            font=('Segoe UI', 9),
            bg='#16213e',
            fg='#00ff88'
        )
        self.status_label.pack(side=tk.RIGHT, padx=15, pady=8)
        
        # Answer display area
        text_frame = tk.Frame(main_frame, bg='#1a1a2e')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            bg='#0f0f1e',
            fg='#e0e0e0',
            font=('Consolas', 10),
            padx=15,
            pady=15,
            relief='flat',
            borderwidth=0,
            insertbackground='#00ff88',
            selectbackground='#00ff88',
            selectforeground='#000000'
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame, bg='#16213e')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_widget.yview)
        
        # Bottom control bar
        control_frame = tk.Frame(main_frame, bg='#16213e', height=35)
        control_frame.pack(fill=tk.X, side=tk.BOTTOM)
        control_frame.pack_propagate(False)
        
        # Close button
        close_btn = tk.Button(
            control_frame,
            text="✕ Close",
            command=self.hide_overlay,
            bg='#e94560',
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            relief='flat',
            padx=15,
            pady=3,
            cursor='hand2'
        )
        close_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Copy button
        copy_btn = tk.Button(
            control_frame,
            text="📋 Copy",
            command=self.copy_answer,
            bg='#0f3460',
            fg='white',
            font=('Segoe UI', 9),
            relief='flat',
            padx=15,
            pady=3,
            cursor='hand2'
        )
        copy_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Initially hidden
        self.overlay.withdraw()
    
    def copy_answer(self):
        """Copy answer to clipboard"""
        try:
            answer_text = self.text_widget.get(1.0, tk.END).strip()
            self.overlay.clipboard_clear()
            self.overlay.clipboard_append(answer_text)
            self.status_label.config(text="● Copied!", fg='#00ff88')
            self.overlay.after(2000, lambda: self.status_label.config(text="● Ready", fg='#00ff88'))
        except:
            pass
    
    def register_hotkeys(self):
        """Register global hotkeys"""
        try:
            keyboard.add_hotkey(ACTIVATION_HOTKEY, self.on_activation_hotkey)
            keyboard.add_hotkey(CLOSE_OVERLAY_HOTKEY, self.hide_overlay)
        except Exception as e:
            print(f"[One Above All] ⚠️ Hotkey error: {e}")
            print("[One Above All] Try running as Administrator")
    
    def on_activation_hotkey(self):
        """Handle activation hotkey"""
        if self.is_processing:
            print("[One Above All] Already processing, please wait...")
            return
        
        print("\n[One Above All] 🔍 Hotkey pressed! Scanning...")
        self.is_processing = True
        
        # Show scanning status
        self.show_status("🔍 Scanning...", "#ffd700")
        
        # Process in background
        threading.Thread(target=self.process_screen, daemon=True).start()
    
    def show_status(self, message, color="#00ff88"):
        """Update overlay status"""
        try:
            self.status_label.config(text=f"● {message}", fg=color)
            self.overlay.deiconify()
            self.overlay.lift()
        except:
            pass
    
    def capture_screen(self):
        """Capture entire screen"""
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                print(f"[One Above All] 📸 Screen captured: {img.size[0]}x{img.size[1]}")
                return img
        except Exception as e:
            print(f"[One Above All] ❌ Capture error: {e}")
            return None
    
    def extract_text_from_image(self, image):
        """Extract text using OCR with preprocessing"""
        try:
            img_array = np.array(image)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Multiple OCR passes
            text1 = pytesseract.image_to_string(gray, lang='eng')
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            text2 = pytesseract.image_to_string(thresh, lang='eng')
            denoised = cv2.fastNlMeansDenoising(gray)
            text3 = pytesseract.image_to_string(denoised, lang='eng')
            
            texts = [text1, text2, text3]
            best_text = max(texts, key=len)
            
            print(f"[One Above All] 📝 Extracted {len(best_text)} characters")
            
            if best_text.strip():
                preview = best_text[:200].replace('\n', ' ')
                print(f"[One Above All] Preview: {preview}...")
            
            return best_text.strip()
            
        except Exception as e:
            print(f"[One Above All] ❌ OCR error: {e}")
            return ""
    
    def query_ai(self, screen_text):
        """Send text to Groq AI (FREE) and get answer"""
        try:
            print("[One Above All] 🤖 Asking AI (Free Groq API)...")
            
            system_prompt = """You are "One Above All", an advanced AI assistant that analyzes screen content to help users.

            Your task:
            1. Identify any questions in the captured screen text
            2. For multiple choice questions: state the correct answer with explanation
            3. For programming questions: provide code solutions with comments
            4. For factual questions: give accurate, concise answers
            5. Format responses cleanly with emojis and line breaks for readability
            6. If no clear question is found, summarize the key information visible

            Be direct, accurate, and helpful. Use markdown formatting with **bold** for important points."""
            
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": AI_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this screen content and help me:\n\n{screen_text[:4000]}"}
                ],
                "temperature": 0.7,
                "max_tokens": 800,
                "top_p": 0.9
            }
            
            response = requests.post(
                GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content']
                
                usage = result.get('usage', {})
                tokens_used = usage.get('total_tokens', 'N/A')
                print(f"[One Above All] ✅ Response received!")
                print(f"[One Above All] Tokens used: {tokens_used}")
                print(f"[One Above All] 💰 Cost: $0.00 (FREE)")
                
                return answer
            elif response.status_code == 401:
                return "❌ **Invalid API Key**\n\nPlease get your free Groq API key at:\nhttps://console.groq.com/keys"
            elif response.status_code == 429:
                return "⏳ **Rate Limit**\n\nFree tier: 30 requests/minute. Please wait."
            else:
                error_msg = response.json().get('error', {}).get('message', 'Unknown error')
                return f"❌ **API Error {response.status_code}**\n\n{error_msg[:200]}"
                    
        except requests.exceptions.Timeout:
            return "⏱️ **Request Timed Out**\n\nPlease try again."
        except Exception as e:
            return f"❌ **Connection Error**\n\n{str(e)[:200]}"
    
    def show_overlay(self, answer):
        """Display answer in the overlay"""
        try:
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(1.0, answer)
            self.overlay.deiconify()
            self.overlay.lift()
            self.overlay.focus_force()
            self.status_label.config(text="● Answer Ready", fg='#00ff88')
        except Exception as e:
            print(f"[One Above All] Display error: {e}")
    
    def hide_overlay(self):
        """Hide the overlay window"""
        try:
            self.overlay.withdraw()
            self.status_label.config(text="● Ready", fg='#00ff88')
        except:
            pass
    
    def process_screen(self):
        """Complete processing pipeline"""
        try:
            # Step 1: Capture
            self.show_status("📸 Capturing...", "#ffd700")
            screen_img = self.capture_screen()
            
            if screen_img is None:
                self.show_overlay("❌ **Failed to capture screen**")
                self.is_processing = False
                return
            
            # Step 2: OCR
            self.show_status("🔍 Reading text...", "#ffd700")
            screen_text = self.extract_text_from_image(screen_img)
            
            if not screen_text or len(screen_text.strip()) < 5:
                self.show_overlay("❌ **No readable text found**\n\nMake sure:\n• Text is clear and large enough\n• Screen has readable content")
                self.is_processing = False
                return
            
            # Step 3: AI Query (FREE)
            self.show_status("🤖 AI Thinking...", "#ffd700")
            answer = self.query_ai(screen_text)
            
            # Step 4: Display
            self.show_overlay(answer)
            print("[One Above All] ✅ Done!\n")
            
        except Exception as e:
            self.show_overlay(f"❌ **Unexpected Error**\n\n{str(e)}")
            print(f"[One Above All] Error: {e}")
        
        finally:
            self.is_processing = False
    
    def run(self):
        """Start the application"""
        try:
            self.overlay.mainloop()
        except KeyboardInterrupt:
            print("\n[One Above All] Shutting down gracefully...")
        finally:
            try:
                keyboard.unhook_all()
            except:
                pass
            print("[One Above All] Goodbye!")

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════╗
    ║           ⚡ ONE ABOVE ALL ⚡                ║
    ║     AI-Powered Screen Assistant v1.0        ║
    ║     💰 100% FREE - No API Costs!           ║
    ╚══════════════════════════════════════════════╝
    """)
    
    # Check if API key is set
    if GROQ_API_KEY == "gsk_PASTE_YOUR_GROQ_KEY_HERE":
        print("❌ ERROR: Please set your Groq API key in config.py!")
        print("1. Go to: https://console.groq.com/keys")
        print("2. Create a free API key")
        print("3. Paste it in config.py")
        print("\nPress Enter to exit...")
        input()
        sys.exit(1)
    
    try:
        app = OneAboveAll()
        app.run()
    except Exception as e:
        print(f"\n[One Above All] Fatal error: {e}")
        print("Press Enter to exit...")
        input()