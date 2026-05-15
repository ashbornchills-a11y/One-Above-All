import customtkinter as ctk
import tkinter as tk
from ..utils.logger import logger
from ..utils.config_manager import config

class OverlayWindow:
    """A modern, draggable overlay window using CustomTkinter."""
    
    def __init__(self, copy_callback=None, close_callback=None):
        self.copy_callback = copy_callback
        self.close_callback = close_callback
        
        # Configure CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme(config.get("theme", "dark-blue"))
        
        self.root = ctk.CTk()
        self.root.title("One Above All")
        
        # Make window borderless and transparent
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.alpha = config.get("overlay_alpha", 0.95)
        self.root.attributes("-alpha", self.alpha)
        
        # Size and Position
        self.win_width = 500
        self.win_height = 450
        self._center_window()
        
        self._build_ui()
        self._bind_events()
        
        # Hide initially
        self.root.withdraw()
        
        self.is_visible = False

    def _center_window(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        
        # Default to bottom right, slightly offset
        x = screen_w - self.win_width - 30
        y = screen_h - self.win_height - 60
        self.root.geometry(f"{self.win_width}x{self.win_height}+{x}+{y}")

    def _build_ui(self):
        # Main Frame (for styling and drag area)
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="#1E1E2E")
        self.main_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Header (Drag Handle)
        self.header = ctk.CTkFrame(self.main_frame, height=40, fg_color="#181825", corner_radius=15)
        self.header.pack(fill="x", padx=5, pady=5)
        self.header.pack_propagate(False)
        
        self.title_label = ctk.CTkLabel(
            self.header, 
            text="⚡ ONE ABOVE ALL", 
            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
            text_color="#89B4FA"
        )
        self.title_label.pack(side="left", padx=15)
        
        self.status_label = ctk.CTkLabel(
            self.header, 
            text="● Ready", 
            font=ctk.CTkFont(family="Inter", size=12),
            text_color="#A6E3A1"
        )
        self.status_label.pack(side="right", padx=15)
        
        # Content Area
        self.textbox = ctk.CTkTextbox(
            self.main_frame,
            wrap="word",
            font=ctk.CTkFont(family="Inter", size=13),
            fg_color="#11111B",
            text_color="#CDD6F4",
            corner_radius=10
        )
        self.textbox.pack(fill="both", expand=True, padx=15, pady=(5, 10))
        
        # Footer
        self.footer = ctk.CTkFrame(self.main_frame, height=40, fg_color="transparent")
        self.footer.pack(fill="x", padx=15, pady=(0, 10))
        
        self.close_btn = ctk.CTkButton(
            self.footer, 
            text="✕ Close", 
            width=100,
            fg_color="#F38BA8",
            hover_color="#E78284",
            text_color="#11111B",
            font=ctk.CTkFont(family="Inter", weight="bold"),
            command=self.hide
        )
        self.close_btn.pack(side="right", padx=(10, 0))
        
        self.copy_btn = ctk.CTkButton(
            self.footer, 
            text="📋 Copy", 
            width=100,
            fg_color="#89B4FA",
            hover_color="#8CAAEE",
            text_color="#11111B",
            font=ctk.CTkFont(family="Inter", weight="bold"),
            command=self.copy_to_clipboard
        )
        self.copy_btn.pack(side="right")

    def _bind_events(self):
        # Allow dragging window from header
        self.header.bind("<ButtonPress-1>", self._start_drag)
        self.header.bind("<B1-Motion>", self._do_drag)
        self.title_label.bind("<ButtonPress-1>", self._start_drag)
        self.title_label.bind("<B1-Motion>", self._do_drag)

    def _start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def _do_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def update_status(self, text, color="#A6E3A1"):
        """Updates the status label."""
        self.status_label.configure(text=f"● {text}", text_color=color)
        self.root.update_idletasks()

    def set_content(self, text):
        """Sets the AI answer text."""
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", text)
        self.textbox.configure(state="disabled")

    def copy_to_clipboard(self):
        """Copies content to clipboard."""
        text = self.textbox.get("0.0", "end").strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.update_status("Copied!", "#F9E2AF")
            if self.copy_callback:
                self.copy_callback()
            # Reset status after 2 seconds
            self.root.after(2000, lambda: self.update_status("Ready", "#A6E3A1"))

    def show(self):
        """Displays the overlay."""
        self.root.deiconify()
        self.root.attributes("-alpha", 0.0)
        self._fade_in()
        self.is_visible = True
        
    def _fade_in(self):
        alpha = self.root.attributes("-alpha")
        if alpha < self.alpha:
            alpha += 0.1
            self.root.attributes("-alpha", min(alpha, self.alpha))
            self.root.after(10, self._fade_in)

    def hide(self):
        """Hides the overlay."""
        self.is_visible = False
        self.root.withdraw()
        if self.close_callback:
            self.close_callback()
        self.update_status("Ready", "#A6E3A1")

    def run(self):
        """Starts the Tkinter main loop."""
        self.root.mainloop()
