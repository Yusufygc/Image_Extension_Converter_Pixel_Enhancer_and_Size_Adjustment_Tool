import os
from PIL import Image
from core.interfaces import IResizer
from utils.constants import AppConstants

class ResizerService(IResizer):
    def process(self, image_path: str, **kwargs) -> str:
        if 'width' in kwargs and 'height' in kwargs:
            return self.resize_by_dimensions(image_path, kwargs['width'], kwargs['height'])
        elif 'percentage' in kwargs:
            return self.resize_by_percentage(image_path, kwargs['percentage'])
        else:
            raise ValueError("Invalid arguments for resizing")

    def resize_by_dimensions(self, image_path: str, width: int, height: int) -> str:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")

        try:
            with Image.open(image_path) as img:
                # Use High Quality Resampling
                resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                directory = os.path.dirname(image_path)
                filename = os.path.splitext(os.path.basename(image_path))[0]
                output_path = os.path.join(directory, f"{filename}_resized_{width}x{height}.{img.format.lower()}")
                
                resized_img.save(output_path, quality=AppConstants.DEFAULT_QUALITY)
                return output_path
        except Exception as e:
            raise Exception(f"Resizing failed: {str(e)}")

    def resize_by_percentage(self, image_path: str, percentage: int) -> str:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")
            
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                new_width = int(width * (percentage / 100))
                new_height = int(height * (percentage / 100))
                
                return self.resize_by_dimensions(image_path, new_width, new_height)
        except Exception as e:
             raise Exception(f"Resizing failed: {str(e)}")
