"""
Enhanced Splash Screen - Gobioeng HALog
Professional splash screen with animated loading and resource handling
"""

from PyQt5.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QProgressBar, QWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QRect  # Explicitly import QRect
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor, QLinearGradient, QBrush
from resource_helper import resource_path, generate_icon
import time
import os

class SplashScreen(QSplashScreen):
    finished = pyqtSignal()

    def __init__(self, app_version="0.0.1"):
        # Create pixmap for the splash screen
        pixmap = QPixmap(500, 350)
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.start_time = time.time()
        self.app_version = app_version
        self.minimum_display_time = 2.5  # seconds
        
        # Create a timer for animations
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.setInterval(100)
        self.animation_step = 0
        
        self.setupUI()
        self.animation_timer.start()

    def setupUI(self):
        # Get the pixmap for customization
        pixmap = self.pixmap()
        pixmap.fill(Qt.transparent)
        
        # Create a painter for drawing on the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw gradient background
        gradient = QLinearGradient(0, 0, 0, pixmap.height())
        gradient.setColorAt(0, QColor("#f5f6fa"))
        gradient.setColorAt(1, QColor("#e9ecef"))
        painter.fillRect(pixmap.rect(), QBrush(gradient))
        
        # Draw border
        painter.setPen(QColor("#e0e1e4"))
        painter.drawRect(0, 0, pixmap.width()-1, pixmap.height()-1)

        # Try to load logo from assets
        logo_path = resource_path("linac_logo.ico")
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            painter.drawPixmap(25, 25, logo_pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # Generate icon as fallback
            fallback_icon = generate_icon(64)
            painter.drawPixmap(25, 25, fallback_icon)
            
        # Draw application name
        painter.setPen(QColor("#2c3e50"))
        font = QFont("Arial", 22, QFont.Bold)
        painter.setFont(font)
        # Using explicitly created QRect instead of QRect literal
        app_name_rect = QRect(100, 30, 300, 40)
        painter.drawText(app_name_rect, Qt.AlignLeft | Qt.AlignVCenter, "HALog")
        
        # Draw version
        painter.setPen(QColor("#7f8c8d"))
        font = QFont("Arial", 12)
        painter.setFont(font)
        version_rect = QRect(100, 70, 300, 30)
        painter.drawText(version_rect, Qt.AlignLeft | Qt.AlignVCenter, f"Version {self.app_version}")
        
        # Draw tagline
        painter.setPen(QColor("#34495e"))
        font = QFont("Arial", 10)
        painter.setFont(font)
        tagline_rect = QRect(25, 120, 450, 20)
        painter.drawText(tagline_rect, Qt.AlignCenter, "Professional LINAC Water System Monitor")
        
        # Draw footer
        painter.setPen(QColor("#7f8c8d"))
        font = QFont("Arial", 9)
        painter.setFont(font)
        footer_rect = QRect(25, 320, 450, 20)
        painter.drawText(footer_rect, Qt.AlignCenter, "© 2025 gobioeng.com - All Rights Reserved")
        
        # Finish painting
        painter.end()
        
        # Set the modified pixmap back
        self.setPixmap(pixmap)
        
        # Setup progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(25, 280, 450, 20)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ecf0f1;
                border-radius: 5px;
                background-color: #34495e;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
                border-radius: 3px;
            }
        """)
        
        # Setup status label
        self.status_label = QLabel(self)
        self.status_label.setGeometry(25, 250, 450, 25)
        self.status_label.setStyleSheet("color: #2c3e50; font-size: 11px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setText("Initializing...")

    def update_animation(self):
        self.animation_step += 1
        
        # Update dots in status label for animation effect
        dots = "." * (self.animation_step % 4)
        message = self.status_label.text().rstrip('.') 
        if message.endswith("ing"):
            self.status_label.setText(f"{message}{dots}")
            
        # Update progress with a smooth animation
        current_value = self.progress_bar.value()
        if current_value < 95:  # Cap at 95% until explicitly completed
            self.progress_bar.setValue(min(current_value + 1, 95))

    def update_status(self, message, progress_value=None):
        self.status_label.setText(message)
        if progress_value is not None:
            self.progress_bar.setValue(progress_value)

    def finish(self, main_window):
        # Ensure minimum display time
        elapsed = time.time() - self.start_time
        if elapsed < self.minimum_display_time:
            QTimer.singleShot(int((self.minimum_display_time - elapsed) * 1000), 
                             lambda: self._do_finish(main_window))
        else:
            self._do_finish(main_window)
            
    def _do_finish(self, main_window):
        self.animation_timer.stop()
        self.update_status("Ready!", 100)
        
        # Short delay before hiding splash
        QTimer.singleShot(300, lambda: super().finish(main_window))
        self.finished.emit()
