from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser, QPushButton
from PySide6.QtCore import Qt
from utils.constants import AppConstants

class InfoView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel(f"{AppConstants.APP_NAME}")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #89b4fa;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Version
        version = QLabel(f"Versiyon: {AppConstants.VERSION}")
        version.setStyleSheet("font-size: 16px; color: #a6adc8;")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        # Content (Instructions)
        content = QTextBrowser()
        content.setOpenExternalLinks(True)
        content.setStyleSheet("""
            QTextBrowser {
                background-color: rgba(30, 30, 46, 0.5);
                border: 1px solid #45475a;
                border-radius: 8px;
                padding: 15px;
                font-size: 16px;
                color: #cdd6f4;
            }
        """)
        
        html_content = """
        <h3 style="color: #fab387;">Nasıl Kullanılır?</h3>
        <ol style="margin-top: 0px;">
            <li><b>Resim Seçimi:</b> Dosyalarınızı sürükleyip bırakın veya 'Dosya Seç' butonunu kullanın.</li>
            <li><b>İşlem Seçimi:</b>
                <ul>
                    <li><b>Format Dönüştür:</b> Resimlerinizi JPG, PNG, WEBP, SVG gibi formatlara çevirin.</li>
                    <li><b>Yeniden Boyutlandırma:</b> Genişlik/Yükseklik veya Yüzde olarak boyutlandırın.</li>
                    <li><b>Kalite Artır:</b> Yapay zeka destekli algoritmalarla çözünürlüğü yükseltin.</li>
                </ul>
            </li>
            <li><b>Başlat:</b> Tüm ayarları yaptıktan sonra 'İŞLEMİ BAŞLAT' butonuna basın.</li>
        </ol>
        <p><i>İpucu: 'Seçilen dosyaları temizle' butonu ile listenizi sıfırlayabilirsiniz.</i></p>
        """
        content.setHtml(html_content)
        layout.addWidget(content)

        layout.addStretch()

        # Footer
        footer = QLabel("Geliştirici : MYY Yazılım")
        footer.setStyleSheet("font-size: 14px; color: #585b70; font-weight: bold;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
