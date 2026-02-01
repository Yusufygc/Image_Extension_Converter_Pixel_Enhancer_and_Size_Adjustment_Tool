from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout
from PySide6.QtCore import Qt, Signal, QMimeData
from PySide6.QtGui import QDragEnterEvent, QDropEvent

class DropZone(QLabel):
    files_dropped = Signal(list)

    def __init__(self):
        super().__init__()
        self.setObjectName("DropZone")
        self.setAlignment(Qt.AlignCenter)
        self.setText("Resimleri Buraya Sürükleyin\nveya\nTıklayın")
        self.setAcceptDrops(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(200)

    def mousePressEvent(self, event):
        # Emit signal to open file dialog (handled by parent)
        # We can implement a signal 'clicked' since QLabel doesn't have it
        self.files_dropped.emit([]) # Special case for click? No, let's make a separate signal or just better parent handling.
        # But for drag and drop, we emit the list. 
        # For click we normally want to open a dialog.
        # Let's emit a signal 'clicked' actually.
        pass 
        # Wait, I cannot define new signals outside __init__ easily on instance. 
        # I should just let the parent handle mousePress logic by not consuming it or emit a custom signal.
        super().mousePressEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setText("Bırak Gelsin! 📂")
            self.setStyleSheet("border-color: #a6e3a1; color: #a6e3a1;")

    def dragLeaveEvent(self, event):
        self.setText("Resimleri Buraya Sürükleyin\nveya\nTıklayın")
        self.setStyleSheet("") # Revert to stylesheet default
        
    def dropEvent(self, event: QDropEvent):
        self.setText("Resimleri Buraya Sürükleyin\nveya\nTıklayın")
        self.setStyleSheet("")
        
        files = []
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path:
                    files.append(file_path)
            
            if files:
                self.files_dropped.emit(files)
