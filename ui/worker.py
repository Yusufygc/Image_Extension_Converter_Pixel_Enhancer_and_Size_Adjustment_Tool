from PySide6.QtCore import QThread, Signal, QObject

class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(str)
    progress = Signal(int, str) # value, message
    result = Signal(str) # output path

class ProcessingWorker(QThread):
    def __init__(self, service, files, **kwargs):
        super().__init__()
        self.service = service
        self.files = files
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self._is_running = True

    def run(self):
        total = len(self.files)
        for i, file_path in enumerate(self.files):
            if not self._is_running:
                break
            
            try:
                self.signals.progress.emit(int((i / total) * 100), f"İşleniyor: {file_path}...")
                output = self.service.process(file_path, **self.kwargs)
                self.signals.result.emit(output)
            except Exception as e:
                self.signals.error.emit(f"Hata ({file_path}): {str(e)}")
        
        self.signals.progress.emit(100, "Tamamlandı!")
        self.signals.finished.emit()

    def stop(self):
        self._is_running = False
