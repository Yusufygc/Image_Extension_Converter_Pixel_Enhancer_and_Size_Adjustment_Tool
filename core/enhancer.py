import os
from PIL import Image, ImageFilter, ImageEnhance
from core.interfaces import IEnhancer
from utils.constants import AppConstants

class EnhancerService(IEnhancer):
    def process(self, image_path: str, **kwargs) -> str:
        factor = kwargs.get('factor', 2.0)
        return self.enhance_resolution(image_path, factor)

    def enhance_resolution(self, image_path: str, factor: float) -> str:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")

        try:
            with Image.open(image_path) as img:
                width, height = img.size
                new_width = int(width * factor)
                new_height = int(height * factor)
                
                # Step 1: High Quality Upscaling
                # LANCZOS is usually best for downscaling, but BICUBIC often preferred for upscaling unless downscaling too.
                # Actually LANCZOS is generally good.
                upscaled_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Step 2: Sharpening to simulate "enhancement" (restore edges)
                # Helps reduce the blur from interpolation
                enhanced_img = upscaled_img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

                # Step 3: Minimal Contrast/Color enhancement to make it "pop"
                enhancer = ImageEnhance.Contrast(enhanced_img)
                enhanced_img = enhancer.enhance(1.1)
                
                directory = os.path.dirname(image_path)
                filename = os.path.splitext(os.path.basename(image_path))[0]
                output_path = os.path.join(directory, f"{filename}_enhanced_x{factor}.{img.format.lower() if img.format else 'png'}")
                
                enhanced_img.save(output_path, quality=95) # Higher quality for enhanced images
                return output_path
        except Exception as e:
            raise Exception(f"Enhancement failed: {str(e)}")
