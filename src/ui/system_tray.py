import pystray
from PIL import Image, ImageDraw
import threading
from ..utils.logger import logger

class SystemTrayIcon:
    """Manages the system tray icon and background presence."""
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.icon = None
        self.thread = None

    def _create_image(self):
        """Generates a simple icon image if no file is provided."""
        # Create a basic lightning bolt icon for "One Above All"
        image = Image.new('RGB', (64, 64), color=(30, 30, 46))
        dc = ImageDraw.Draw(image)
        # Simple lightning bolt shape
        points = [(32, 5), (10, 35), (28, 35), (20, 60), (55, 25), (35, 25)]
        dc.polygon(points, fill=(137, 180, 250))
        return image

    def _on_show(self, icon, item):
        logger.info("Tray: Show App clicked")
        self.app.show_overlay()

    def _on_exit(self, icon, item):
        logger.info("Tray: Exit clicked")
        self.app.quit()

    def setup(self):
        """Sets up the tray icon menu."""
        menu = pystray.Menu(
            pystray.MenuItem("Show Latest Answer", self._on_show, default=True),
            pystray.MenuItem("Exit", self._on_exit)
        )
        
        self.icon = pystray.Icon(
            "one_above_all",
            self._create_image(),
            "One Above All - AI Assistant",
            menu
        )

    def run(self):
        """Runs the tray icon in a separate thread."""
        if not self.icon:
            self.setup()
        
        # pystray blocks, so it must run in a thread or be the main thread
        # In a typical GUI app, the GUI loop is main, tray is thread (or vice-versa depending on OS limitations)
        # Windows handles threaded pystray well.
        self.thread = threading.Thread(target=self.icon.run, daemon=True)
        self.thread.start()
        logger.info("System tray icon started.")

    def stop(self):
        """Stops the tray icon."""
        if self.icon:
            self.icon.stop()
