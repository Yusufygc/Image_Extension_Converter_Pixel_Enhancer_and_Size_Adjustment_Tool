from PySide6.QtWidgets import QApplication
from utils.path_helper import get_resource_path
import os

class ThemeManager:
    @staticmethod
    def apply_theme(app: QApplication):
        """
        Loads the main.qss file and applies it to the application.
        """
        try:
            # We assume main.qss is in ui/styles/ relative to this file? 
            # Or better, use get_resource_path if we bundle it.
            # But get_resource_path is relative to the *root* or where we run it.
            # Let's try to find it relative to this file first.
            
            # Since this file is in ui/styles/theme.py, main.qss is in the same dir.
            current_dir = os.path.dirname(os.path.abspath(__file__))
            qss_path = os.path.join(current_dir, "main.qss")
            
            if os.path.exists(qss_path):
                with open(qss_path, "r") as f:
                    qss = f.read()
                    app.setStyleSheet(qss)
            else:
                print(f"Warning: Stylesheet not found at {qss_path}")
        except Exception as e:
            print(f"Error applying theme: {e}")
