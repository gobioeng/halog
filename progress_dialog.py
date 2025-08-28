from PyQt5.QtWidgets import (
    QProgressDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)
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
        
        # Progress phases
        self.current_phase = "initializing"
        self.phases = {
            "uploading": {"label": "Uploading file...", "progress_weight": 0.2},
            "processing": {"label": "Processing data...", "progress_weight": 0.8},
            "finalizing": {"label": "Finalizing...", "progress_weight": 0.05}
        }
        self.phase_progress = 0  # Progress within current phase (0-100)

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

        # Enhanced Material Design 3.0 Styling
        self.setStyleSheet(
            """
            QProgressDialog {
                background-color: #FFFBFE;
                border: 1px solid #E7E0EC;
                border-radius: 12px;
                padding: 20px;
            }
            QProgressBar {
                border: none;
                border-radius: 8px;
                text-align: center;
                font-weight: 500;
                background-color: #E8F5E8;
                color: #1976D2;
                font-size: 12px;
                min-height: 20px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #1976D2, stop: 1 #1565C0);
                border-radius: 8px;
            }
            QLabel {
                color: #1C1B1F;
                font-size: 12px;
                padding: 4px;
                font-weight: 400;
            }
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 20px;
                font-weight: 500;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1565C0;
                box-shadow: 0px 2px 4px rgba(25, 118, 210, 0.3);
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """
        )

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

    def update_progress(
        self,
        percentage: float,
        status_message: str = "",
        lines_processed: int = 0,
        total_lines: int = 0,
        bytes_processed: int = 0,
        total_bytes: int = 0,
    ):
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

    def set_phase(self, phase_name: str, phase_progress: float = 0):
        """Set the current processing phase"""
        if phase_name in self.phases:
            self.current_phase = phase_name
            self.phase_progress = max(0, min(100, phase_progress))
            self.update_overall_progress()
            
    def update_phase_progress(self, progress: float):
        """Update progress within the current phase"""
        self.phase_progress = max(0, min(100, progress))
        self.update_overall_progress()
        
    def update_overall_progress(self):
        """Calculate and update overall progress across all phases"""
        overall_progress = 0
        
        # Calculate progress based on completed phases and current phase
        phase_order = ["uploading", "processing", "finalizing"]
        current_index = phase_order.index(self.current_phase) if self.current_phase in phase_order else 0
        
        # Add progress from completed phases
        for i, phase in enumerate(phase_order):
            if i < current_index:
                overall_progress += self.phases[phase]["progress_weight"] * 100
            elif i == current_index:
                # Add partial progress from current phase
                phase_weight = self.phases[phase]["progress_weight"]
                overall_progress += phase_weight * self.phase_progress
                break
                
        # Update the progress bar
        self.setValue(int(overall_progress))
        
        # Update the label text
        phase_info = self.phases.get(self.current_phase, {"label": "Processing..."})
        self.setLabelText(f"{phase_info['label']} ({self.phase_progress:.0f}%)")

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
        for unit in ["B", "KB", "MB", "GB"]:
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
