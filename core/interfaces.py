from abc import ABC, abstractmethod
from typing import Tuple, Any

class IImageProcessor(ABC):
    """
    Base generic interface for image processing services.
    """
    @abstractmethod
    def process(self, image_path: str, **kwargs) -> Any:
        pass

class IConverter(IImageProcessor):
    """
    Interface for image format conversion.
    """
    @abstractmethod
    def convert(self, image_path: str, output_format: str, output_path: str = None) -> str:
        """
        Convert image to target format.
        Args:
            image_path: Source image path.
            output_format: Target format (e.g., 'PNG', 'JPEG').
            output_path: Optional specific output path.
        Returns:
            Path to the saved file.
        """
        pass

class IResizer(IImageProcessor):
    """
    Interface for image resizing.
    """
    @abstractmethod
    def resize_by_dimensions(self, image_path: str, width: int, height: int) -> Any:
        pass

    @abstractmethod
    def resize_by_percentage(self, image_path: str, percentage: int) -> Any:
        pass

class IEnhancer(IImageProcessor):
    """
    Interface for image enhancement (resolution upscaling etc).
    """
    @abstractmethod
    def enhance_resolution(self, image_path: str, factor: float) -> Any:
        pass
