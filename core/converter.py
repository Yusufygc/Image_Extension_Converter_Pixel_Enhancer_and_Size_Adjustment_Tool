import os
from PIL import Image
from core.interfaces import IConverter
from utils.constants import AppConstants

class ConverterService(IConverter):
    def process(self, image_path: str, **kwargs) -> str:
        output_format = kwargs.get('output_format')
        return self.convert(image_path, output_format)

    def convert(self, image_path: str, output_format: str, output_path: str = None) -> str:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")

        try:
            with Image.open(image_path) as img:
                # Convert mode logic (e.g. RGBA to RGB for JPEG)
                if output_format.upper() in ["JPEG", "JPG", "BMP"] and img.mode == "RGBA":
                    img = img.convert("RGB")
                
                if output_path is None:
                    # Generate default output path
                    directory = os.path.dirname(image_path)
                    filename = os.path.splitext(os.path.basename(image_path))[0]
                    output_path = os.path.join(directory, f"{filename}_converted.{output_format.lower()}")

                # ICO specific handling
                if output_format.upper() == "ICO":
                    # ICO usually needs specific sizes
                    img.save(output_path, format=output_format.upper(), sizes=[(256, 256)])
                else:
                    img.save(output_path, format=output_format.upper(), quality=AppConstants.DEFAULT_QUALITY)
                
                return output_path
        except Exception as e:
            # Clean up logic could go here if partial file created
            raise Exception(f"Conversion failed: {str(e)}")
