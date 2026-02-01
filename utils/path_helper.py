import os
import sys

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, works for dev and for PyInstaller/Nuitka.
    
    Args:
        relative_path (str): The relative path to the resource (e.g., "assets/icons/icon.png").
        
    Returns:
        str: The absolute path to the resource.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            # Works for development and Nuitka (Standalone & Onefile)
            # In Nuitka Onefile, __file__ points to the temporary extracted directory,
            # whereas sys.executable points to the original exe file.
            # Since our assets are bundled inside the temp dir, we must use __file__.
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Error resolving path: {e}")
        return relative_path
