from PyQt5.QtWidgets import QProgressDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
import time

class ProgressDialog(QProgressDialog):
    """Enhanced progress dialog with detailed progress tracking and professional styling"""
    
    canceled = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()
        self.start_time = time.time()
        self.last_update_time = time.time()
        
        # Update timer for ETA calculations
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_eta)
        self.timer.start(1000)  # Update every second
        
    def setupUI(self):
        """Setup the enhanced progress dialog UI"""
        self.setWindowTitle("Processing LINAC Log File")
        self.setWindowModality(Qt.WindowModal)
        self.setMinimumWidth(450)
        self.setMaximum(100)
        self.setValue(0)
        
        # Styling
        self.setStyleSheet("""
            QProgressDialog {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 8px;
            }
            QProgressBar {
                border: 2px solid #dee2e6;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
                background-color: #e9ecef;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #007bff, stop: 1 #0056b3);
                border-radius: 3px;
            }
            QLabel {
                color: #495057;
                font-size: 11px;
                padding: 2px;
            }
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        
        # Initialize labels for detailed progress
        self.current_operation_label = QLabel("Initializing...")
        self.progress_details_label = QLabel("")
        self.eta_label = QLabel("")
        self.speed_label = QLabel("")
        
        # Set label fonts
        font = QFont()
        font.setPointSize(9)
        self.current_operation_label.setFont(font)
        self.progress_details_label.setFont(font)
        self.eta_label.setFont(font)
        self.speed_label.setFont(font)
        
        self.lines_processed = 0
        self.total_lines = 0
        self.bytes_processed = 0
        self.total_bytes = 0
        
    def update_progress(self, percentage: float, status_message: str = "", 
                       lines_processed: int = 0, total_lines: int = 0,
                       bytes_processed: int = 0, total_bytes: int = 0):
        """Update progress with detailed information"""
        self.setValue(int(percentage))
        
        if status_message:
            self.setLabelText(status_message)
            
        # Update detailed progress information
        self.lines_processed = lines_processed
        self.total_lines = total_lines
        self.bytes_processed = bytes_processed
        self.total_bytes = total_bytes
        
        # Update detail labels
        if total_lines > 0:
            self.progress_details_label.setText(
                f"Lines: {lines_processed:,} / {total_lines:,} "
                f"({lines_processed/total_lines*100:.1f}%)"
            )
        
        if total_bytes > 0:
            self.speed_label.setText(
                f"Size: {self.format_bytes(bytes_processed)} / {self.format_bytes(total_bytes)}"
            )
        
        self.last_update_time = time.time()
    
    def update_eta(self):
        """Update estimated time remaining"""
        if self.value() > 0 and self.value() < 100:
            elapsed_time = time.time() - self.start_time
            progress_ratio = self.value() / 100.0
            
            if progress_ratio > 0:
                estimated_total_time = elapsed_time / progress_ratio
                remaining_time = estimated_total_time - elapsed_time
                
                if remaining_time > 0:
                    self.eta_label.setText(f"ETA: {self.format_time(remaining_time)}")
                else:
                    self.eta_label.setText("ETA: Almost done...")
        else:
            self.eta_label.setText("")
    
    def format_time(self, seconds: float) -> str:
        """Format time in human readable format"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            return f"{seconds//60:.0f}m {seconds%60:.0f}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours:.0f}h {minutes:.0f}m"
    
    def format_bytes(self, bytes_count: int) -> str:
        """Format bytes in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_count < 1024.0:
                return f"{bytes_count:.1f} {unit}"
            bytes_count /= 1024.0
        return f"{bytes_count:.1f} TB"
    
    def closeEvent(self, event):
        """Handle close event"""
        self.timer.stop()
        self.canceled.emit()
        super().closeEvent(event)
    
    def reject(self):
        """Handle reject (cancel) event"""
        self.timer.stop()
        self.canceled.emit()
        super().reject()
