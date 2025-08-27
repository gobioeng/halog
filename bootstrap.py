"""
Enhanced Bootstrap - Gobioeng HALog
Splash screen component for application startup
Developer: Tanmay Pandey
Company: gobioeng.com
Date: 2025-08-22 16:50:01 UTC
"""

from PyQt5.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont, QColor, QPainter
from resource_helper import resource_path


class SplashScreen(QWidget):
    """
    Enhanced splash screen with professional styling
    Developed by Tanmay Pandey - gobioeng.com
    """

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setFixedSize(500, 350)
        self.setStyleSheet("background: #2c3e50;")
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # --- App logo from assets (robust path) ---
        self.logo_label = QLabel()
        logo_pix = QPixmap(resource_path("linac_logo.ico"))
        if not logo_pix.isNull():
            self.logo_label.setPixmap(
                logo_pix.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.logo_label.setText("🏥")
            self.logo_label.setStyleSheet("font-size: 64px; color: gold;")
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # App name
        app_name = QLabel("Gobioeng HALog")
        app_name.setFont(QFont("Arial", 22, QFont.Bold))
        app_name.setStyleSheet("color: #ecf0f1; margin-top:8px;")
        app_name.setAlignment(Qt.AlignCenter)
        layout.addWidget(app_name)

        # Version
        version = QLabel("Version 0.0.1 beta")
        version.setFont(QFont("Arial", 12))
        version.setStyleSheet("color: #bdc3c7; margin-bottom:8px;")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        # Tagline
        tagline = QLabel("Professional LINAC water system monitor")
        tagline.setFont(QFont("Arial", 11))
        tagline.setStyleSheet("color: #95a5a6; margin-bottom:12px;")
        tagline.setAlignment(Qt.AlignCenter)
        layout.addWidget(tagline)

        # Designer/company footer with proper attribution
        designer = QLabel(
            "Designed & Developed by <b>Tanmay Pandey</b> • "
            "<a href='https://gobioeng.com'>gobioeng.com</a>"
        )
        designer.setOpenExternalLinks(True)
        designer.setFont(QFont("Arial", 11))
        designer.setStyleSheet("color: #ecf0f1; margin-top:24px;")
        designer.setAlignment(Qt.AlignCenter)
        layout.addWidget(designer)
