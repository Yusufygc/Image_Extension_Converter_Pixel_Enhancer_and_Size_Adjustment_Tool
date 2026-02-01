from PySide6.QtWidgets import QApplication
from utils.path_helper import get_resource_path
import os

class ThemeManager:
    @staticmethod
    def apply_theme(app: QApplication):
        """
        Loads the main.qss file, replaces placeholders with actual paths,
        and applies it to the application.
        """
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            qss_path = os.path.join(current_dir, "main.qss")
            
            if os.path.exists(qss_path):
                with open(qss_path, "r", encoding='utf-8') as f:
                    qss = f.read()
                    
                    # Dynamically replace resource paths
                    # For QSS, we need forward slashes even on Windows
                    # ComboBox Arrow
                    icon_down_path = get_resource_path("assets/icons/down-arrow.svg").replace("\\", "/")
                    qss = qss.replace("@icon_down_arrow", icon_down_path)

                    # SpinBox Arrows
                    icon_spin_up = get_resource_path("assets/icons/up-arrow.svg").replace("\\", "/")
                    icon_spin_down = get_resource_path("assets/icons/down-arrow.svg").replace("\\", "/")
                    
                    qss = qss.replace("@icon_spin_up", icon_spin_up)
                    qss = qss.replace("@icon_spin_down", icon_spin_down)
                    
                    app.setStyleSheet(qss)
            else:
                print(f"Warning: Stylesheet not found at {qss_path}")
        except Exception as e:
            print(f"Error applying theme: {e}")
