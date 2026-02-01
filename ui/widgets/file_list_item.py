from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QPixmap
from utils.path_helper import get_resource_path
from utils.image_loader import load_image
import os

class FileListItemWidget(QWidget):
    remove_clicked = Signal(str) # Emits file path to remove

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # Thumbnail
        self.thumb_label = QLabel()
        self.thumb_label.setFixedSize(40, 40)
        self.thumb_label.setStyleSheet("background-color: #313244; border-radius: 4px;")
        self.thumb_label.setAlignment(Qt.AlignCenter)
        
        self.load_thumbnail()
        layout.addWidget(self.thumb_label)

        # File Info Container
        info_layout = QHBoxLayout() # Or VBox for name + size
        
        # Name & Size
        try:
            name = os.path.basename(self.file_path)
            size_bytes = os.path.getsize(self.file_path)
            size_str = self.format_size(size_bytes)
            
            self.name_label = QLabel(name)
            self.name_label.setStyleSheet("font-weight: bold; color: #cdd6f4;")
            
            self.size_label = QLabel(f"({size_str})")
            self.size_label.setStyleSheet("color: #a6adc8; font-size: 12px;")
            
            info_layout.addWidget(self.name_label)
            info_layout.addWidget(self.size_label)
            info_layout.addStretch()
        except Exception:
            self.name_label = QLabel(os.path.basename(self.file_path))
            info_layout.addWidget(self.name_label)
        
        layout.addLayout(info_layout, stretch=1)

        # Remove Button
        self.btn_remove = QPushButton()
        self.btn_remove.setFixedSize(24, 24)
        self.btn_remove.setCursor(Qt.PointingHandCursor)
        self.btn_remove.setObjectName("IconOnlyButton")
        
        icon_path = get_resource_path("assets/icons/delete_icon.svg")
        if os.path.exists(icon_path):
            self.btn_remove.setIcon(QIcon(icon_path))
            self.btn_remove.setIconSize(QSize(16, 16))
        else:
            self.btn_remove.setText("X")
            
        self.btn_remove.clicked.connect(self.on_remove)
        self.btn_remove.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(243, 139, 168, 0.2);
            }
        """)
        
        layout.addWidget(self.btn_remove)

    def load_thumbnail(self):
        # Async loading would be better but keeping it simple for now
        # Small performance hit if many large files.
        try:
            # First check if it's an image
            ext = os.path.splitext(self.file_path)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.ico', '.webp']:
                # Use QIcon default caching or load small
                # Using QPixmap from path directly might be slow for big images
                # Try creating a thumbnail
                pixmap = QPixmap(self.file_path)
                if not pixmap.isNull():
                    scaled = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.thumb_label.setPixmap(scaled)
                    return
            elif ext == '.svg':
                 # SVG support
                 pixmap = QPixmap(self.file_path)
                 if not pixmap.isNull():
                    scaled = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.thumb_label.setPixmap(scaled)
                    return

            # Fallback icon
            fallback_path = get_resource_path("assets/icons/file_icon.svg")
            if os.path.exists(fallback_path):
                 self.thumb_label.setPixmap(QPixmap(fallback_path).scaled(24, 24, Qt.KeepAspectRatio))
            else:
                 self.thumb_label.setText("📄")

        except Exception:
            self.thumb_label.setText("?")

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def on_remove(self):
        self.remove_clicked.emit(self.file_path)
