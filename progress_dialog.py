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
        self.setWindowModality(Qt.ApplicationModal)  # Changed to ApplicationModal for better visibility
        self.setMinimumWidth(450)
        self.setMaximum(100)
        self.setValue(0)
        # Ensure dialog stays on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Simplified Windows 11 Theme Styling
        self.setStyleSheet(
            """
            QProgressDialog {
                background-color: #f3f3f3;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 16px;
            }
            QProgressBar {
                border: none;
                border-radius: 4px;
                text-align: center;
                font-weight: 400;
                background-color: #e6e6e6;
                color: #333333;
                font-size: 11px;
                min-height: 16px;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 4px;
            }
            QLabel {
                color: #323130;
                font-size: 11px;
                padding: 2px;
                font-weight: 400;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: 1px solid #0078d4;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 400;
                font-size: 11px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #106ebe;
                border: 1px solid #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
                border: 1px solid #005a9e;
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
