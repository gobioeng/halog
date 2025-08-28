#!/usr/bin/env python3
"""
Quick test script to show the enhanced UI changes for trend tabs
"""
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main_window import Ui_MainWindow

class TestMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Set to the Trends tab by default
        self.ui.tabWidget.setCurrentIndex(1)  # Index 1 should be Trends tab

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create and show the window
    window = TestMainWindow()
    window.show()
    
    # Take a screenshot after a brief delay
    from PyQt5.QtCore import QTimer
    
    def take_screenshot():
        pixmap = window.grab()
        pixmap.save("/home/runner/work/halog/halog/enhanced_trends_ui.png")
        print("Screenshot saved as enhanced_trends_ui.png")
        app.quit()
    
    QTimer.singleShot(2000, take_screenshot)  # Take screenshot after 2 seconds
    
    sys.exit(app.exec_())