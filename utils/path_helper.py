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
        # Nuitka might handle it differently, but usually __file__ relative is safe for dev,
        # and checking sys attributes is good for frozen apps.
        if getattr(sys, 'frozen', False):
             # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app 
            # path into variable _MEIPASS'.
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                 # Nuitka might just be the executable directory
                base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Error resolving path: {e}")
        return relative_path
