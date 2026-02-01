import os
import io
from PIL import Image, UnidentifiedImageError
from PySide6.QtGui import QImageReader
from PySide6.QtCore import QBuffer, QIODevice

def load_image(image_path: str) -> Image.Image:
    """
    Loads an image from the given path, with fallback to QImage for formats
    that Pillow doesn't support natively (like SVG or some ICOs).
    
    Args:
        image_path (str): The absolute path to the image file.
        
    Returns:
        PIL.Image.Image: The loaded Pillow Image object.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: If the image format is unsupported or cannot be loaded.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")

    img = None
    try:
        # Try opening with Pillow first
        img = Image.open(image_path)
        img.load() # Force load to check validity
    except UnidentifiedImageError:
        # Fallback: Try QImage (helpful for SVG or formats Pillow misses)
        reader = QImageReader(image_path)
        if reader.canRead():
            qimg = reader.read()
            if not qimg.isNull():
                # Convert QImage to PIL Image via QBuffer -> BytesIO
                buffer = QBuffer()
                buffer.open(QIODevice.ReadWrite)
                qimg.save(buffer, "PNG")
                
                bytes_io = io.BytesIO(buffer.data().data())
                img = Image.open(bytes_io)
                img.load()
                buffer.close()
    
    if img is None:
        raise Exception(f"Unsupported or invalid image format: {image_path}")
        
    return img
