import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QFileDialog, QComboBox, 
                               QSpinBox, QDoubleSpinBox, QProgressBar, QMessageBox, QGroupBox, QListWidget, QStackedWidget)
from PySide6.QtCore import Qt, Slot, QSize

from ui.widgets.drop_zone import DropZone
from ui.styles.theme import ThemeManager
from ui.views.info_view import InfoView
from ui.worker import ProcessingWorker
from core.converter import ConverterService
from core.resizer import ResizerService
from core.enhancer import EnhancerService
from utils.constants import AppConstants, Styles
from utils.path_helper import get_resource_path

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app_instance = app
        self.setWindowTitle(AppConstants.APP_NAME)
        self.setMinimumSize(AppConstants.WINDOW_WIDTH, AppConstants.WINDOW_HEIGHT)
        
        # Set Application Icon
        from PySide6.QtGui import QIcon
        icon_path = get_resource_path("assets/icons/icon.ico")
        if os.path.exists(icon_path):
            self.app_instance.setWindowIcon(QIcon(icon_path))
            self.setWindowIcon(QIcon(icon_path))
        
        # Services
        self.converter_service = ConverterService()
        self.resizer_service = ResizerService()
        self.enhancer_service = EnhancerService()
        self.current_worker = None
        
        self.selected_files = []

        self.setup_ui()
        ThemeManager.apply_theme(self.app_instance)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header_layout = QHBoxLayout()
        
        # Dummy spacer to balance the right button (for perfect centering)
        dummy_btn = QWidget()
        dummy_btn.setFixedWidth(80) # Same width as the button
        header_layout.addWidget(dummy_btn)
        
        header_layout.addStretch() # Spacer Left
        
        title = QLabel(AppConstants.APP_NAME)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #89b4fa;")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        header_layout.addStretch() # Spacer Right
        
        # Info Button
        self.btn_info = QPushButton("Bilgi")
        self.btn_info.setFixedWidth(80)
        self.btn_info.clicked.connect(self.toggle_info_page)
        header_layout.addWidget(self.btn_info)
        
        main_layout.addLayout(header_layout)

        # Stacked Widget for Pages
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Page 1: Home (Original Content)
        self.page_home = QWidget()
        self.setup_home_page(self.page_home)
        self.stack.addWidget(self.page_home)

        # Page 2: Info
        self.page_info = InfoView()
        self.stack.addWidget(self.page_info)
        
        # Progress Bar (Should be visible on Home page only? Or global? 
        # Typically global but structurally it was at bottom. Let's keep it global if relevant, 
        # but logically it belongs to the 'processing' task on Home page. 
        # Making it part of Home page layout is safer visually.)
        
    def setup_home_page(self, parent_widget):
        layout = QVBoxLayout(parent_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # 1. Drop Zone & File List
        content_layout = QHBoxLayout()
        
        # Left Side: Inputs
        left_side_group = QGroupBox("1. Resim Seçimi")
        left_side_layout = QVBoxLayout()
        
        self.drop_zone = DropZone()
        self.drop_zone.files_dropped.connect(self.add_files)
        
        self.btn_browse = QPushButton("Dosya Seç")
        self.btn_browse.clicked.connect(self.browse_files)
        
        self.file_list = QListWidget()
        self.file_list.setMaximumHeight(150)
        self.file_list.setAlternatingRowColors(True)
        
        self.btn_clear = QPushButton("Seçilen dosyaları temizle")
        self.btn_clear.setObjectName("DangerButton")
        self.btn_clear.setMinimumHeight(45)
        self.btn_clear.clicked.connect(self.clear_files)

        left_side_layout.addWidget(self.drop_zone)
        left_side_layout.addWidget(self.btn_browse)
        left_side_layout.addWidget(QLabel("Seçilen Dosyalar:"))
        left_side_layout.addWidget(self.file_list)
        left_side_layout.addWidget(self.btn_clear)
        left_side_group.setLayout(left_side_layout)
        
        content_layout.addWidget(left_side_group, stretch=1)

        # Right Side: Operations
        op_group = QGroupBox("2. İşlem Seçimi")
        op_layout = QVBoxLayout()
        
        self.combo_operation = QComboBox()
        self.combo_operation.addItems(["Format Dönüştür", "Yeniden Boyutlandırma", "Kalite/Çözünürlük Artır"])
        self.combo_operation.currentIndexChanged.connect(self.update_options_ui)
        
        op_layout.addWidget(self.combo_operation)
        
        # Dynamic Options Stack
        self.options_container = QWidget()
        self.options_layout = QVBoxLayout(self.options_container)
        self.options_layout.setContentsMargins(0, 0, 0, 0)
        
        # --- Conversion Options ---
        self.widget_convert = QWidget()
        wc_layout = QHBoxLayout(self.widget_convert)
        wc_layout.addWidget(QLabel("Hedef Format:"))
        self.combo_format = QComboBox()
        self.combo_format.addItems(AppConstants.SUPPORTED_FORMATS)
        wc_layout.addWidget(self.combo_format)
        
        # --- Resize Options ---
        self.widget_resize = QWidget()
        self.widget_resize.setVisible(False)
        wr_layout = QVBoxLayout(self.widget_resize)
        
        type_layout = QHBoxLayout()
        self.combo_resize_type = QComboBox()
        self.combo_resize_type.addItems(["Boyut (px)", "Yüzde (%)"])
        self.combo_resize_type.currentIndexChanged.connect(self.toggle_resize_inputs)
        type_layout.addWidget(QLabel("Yöntem:"))
        type_layout.addWidget(self.combo_resize_type)
        wr_layout.addLayout(type_layout)
        
        self.input_resize_dims = QWidget()
        ird_layout = QHBoxLayout(self.input_resize_dims)
        self.spin_width = QSpinBox()
        self.spin_width.setRange(1, 10000)
        self.spin_width.setValue(1920)
        self.spin_height = QSpinBox()
        self.spin_height.setRange(1, 10000)
        self.spin_height.setValue(1080)
        ird_layout.addWidget(QLabel("Genişlik:"))
        ird_layout.addWidget(self.spin_width)
        ird_layout.addWidget(QLabel("Yükseklik:"))
        ird_layout.addWidget(self.spin_height)
        
        self.input_resize_percent = QWidget()
        self.input_resize_percent.setVisible(False)
        irp_layout = QHBoxLayout(self.input_resize_percent)
        self.spin_percent = QSpinBox()
        self.spin_percent.setRange(1, 500)
        self.spin_percent.setValue(50)
        irp_layout.addWidget(QLabel("Oran (%):"))
        irp_layout.addWidget(self.spin_percent)
        
        wr_layout.addWidget(self.input_resize_dims)
        wr_layout.addWidget(self.input_resize_percent)

        # --- Enhance Options ---
        self.widget_enhance = QWidget()
        self.widget_enhance.setVisible(False)
        we_layout = QHBoxLayout(self.widget_enhance)
        we_layout.addWidget(QLabel("Artış Çarpanı (x):"))
        self.spin_factor = QDoubleSpinBox()
        self.spin_factor.setRange(1.1, 4.0)
        self.spin_factor.setSingleStep(0.5)
        self.spin_factor.setValue(2.0)
        we_layout.addWidget(self.spin_factor)
        
        self.options_layout.addWidget(self.widget_convert)
        self.options_layout.addWidget(self.widget_resize)
        self.options_layout.addWidget(self.widget_enhance)
        
        op_layout.addWidget(self.options_container)
        
        self.btn_process = QPushButton("İŞLEMİ BAŞLAT")
        self.btn_process.setObjectName("PrimaryButton")
        self.btn_process.setMinimumHeight(50)
        self.btn_process.clicked.connect(self.start_processing)
        op_layout.addWidget(self.btn_process)
        
        op_group.setLayout(op_layout)
        
        content_layout.addWidget(op_group, stretch=1)
        layout.addLayout(content_layout)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.status_label = QLabel("Hazır")
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)

    def set_app_instance(self, app):
        self.app_instance = app
        ThemeManager.apply_theme(app)

    @Slot()
    def toggle_info_page(self):
        if self.stack.currentIndex() == 0:
            self.stack.setCurrentIndex(1)
            self.btn_info.setText("Geri")
        else:
            self.stack.setCurrentIndex(0)
            self.btn_info.setText("Bilgi")

    @Slot()
    def browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Resim Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg *.bmp *.webp *.ico *.tiff *.svg)")
        if files:
            self.add_files(files)

    def add_files(self, file_paths):
        for path in file_paths:
            if path not in self.selected_files:
                self.selected_files.append(path)
                self.file_list.addItem(os.path.basename(path))

    def clear_files(self):
        self.selected_files.clear()
        self.file_list.clear()

    @Slot(int)
    def update_options_ui(self, index):
        self.widget_convert.setVisible(index == 0)
        self.widget_resize.setVisible(index == 1)
        self.widget_enhance.setVisible(index == 2)

    @Slot(int)
    def toggle_resize_inputs(self, index):
        self.input_resize_dims.setVisible(index == 0)
        self.input_resize_percent.setVisible(index == 1)

    @Slot()
    def start_processing(self):
        if not self.selected_files:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce dosya seçin!")
            return

        operation_idx = self.combo_operation.currentIndex()
        service = None
        kwargs = {}

        if operation_idx == 0: # Convert
            service = self.converter_service
            kwargs['output_format'] = self.combo_format.currentText()
        elif operation_idx == 1: # Resize
            service = self.resizer_service
            if self.combo_resize_type.currentIndex() == 0:
                kwargs['width'] = self.spin_width.value()
                kwargs['height'] = self.spin_height.value()
            else:
                kwargs['percentage'] = self.spin_percent.value()
        elif operation_idx == 2: # Enhance
            service = self.enhancer_service
            kwargs['factor'] = self.spin_factor.value()

        self.btn_process.setEnabled(False)
        self.current_worker = ProcessingWorker(service, self.selected_files, **kwargs)
        self.current_worker.signals.progress.connect(self.update_progress)
        self.current_worker.signals.finished.connect(self.processing_finished)
        self.current_worker.signals.error.connect(self.processing_error)
        self.current_worker.start()

    def update_progress(self, val, msg):
        self.progress_bar.setValue(val)
        self.status_label.setText(msg)

    def processing_finished(self):
        self.btn_process.setEnabled(True)
        self.status_label.setText("İşlem Tamamlandı!")
        QMessageBox.information(self, "Başarılı", "Tüm işlemler tamamlandı.")

    def processing_error(self, err_msg):
        self.status_label.setText(f"Hata oluştu.")
        QMessageBox.critical(self, "Hata", err_msg)
