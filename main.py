"""
Gobioeng HALog 0.0.1 beta
Professional LINAC Water System Monitor
Company: gobioeng.com
Created: 2025-08-20 22:58:39 UTC
Updated: 2025-08-27 15:08:00 UTC
"""

import sys
import os
import time
from pathlib import Path
import traceback

# Define APP_VERSION globally so it's accessible everywhere
APP_VERSION = "0.0.1"

# Track startup time
startup_begin = time.time()

# Global module cache to prevent duplicate imports
_module_cache = {}


def lazy_import(module_name):
    """Lazy import a module only when needed"""
    if module_name in _module_cache:
        return _module_cache[module_name]
    try:
        if "." in module_name:
            parent_module, child_module = module_name.split(".", 1)
            parent = __import__(parent_module)
            module = getattr(
                __import__(parent_module, fromlist=[child_module]), child_module
            )
        else:
            module = __import__(module_name)
        _module_cache[module_name] = module
        return module
    except ImportError as e:
        print(f"Error importing {module_name}: {e}")
        raise


def setup_environment():
    """Setup environment with minimal imports"""
    os.environ["PYTHONOPTIMIZE"] = "2"
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ["NUMEXPR_MAX_THREADS"] = "8"

    # Set application path
    if getattr(sys, "frozen", False):
        app_dir = Path(sys.executable).parent
    else:
        app_dir = Path(__file__).parent.absolute()
    os.chdir(app_dir)
    if str(app_dir) not in sys.path:
        sys.path.insert(0, str(app_dir))

    # Configure warnings
    import warnings

    warnings.filterwarnings("ignore")

    # Ensure assets directory exists
    assets_dir = app_dir / "assets"
    if not assets_dir.exists():
        assets_dir.mkdir(exist_ok=True)
        print(f"Created assets directory: {assets_dir}")

    # Ensure application icon exists
    try:
        from resource_helper import ensure_app_icon

        ensure_app_icon()
    except Exception as e:
        print(f"Warning: Could not ensure app icon: {e}")


def test_icon_loading():
    """
    Test function to verify icon loading
    Debugging utility for Gobioeng HALog
    """
    from resource_helper import load_splash_icon, resource_path
    import os

    print("=== Icon Loading Test ===")

    # Check available files
    icon_files = [
        "linac_logo_256.png",
        "linac_logo_256.ico",
        "linac_logo_100.png",
        "linac_logo_100.ico",
        "linac_logo.png",
        "linac_logo.ico",
    ]

    print("Available icon files:")
    for icon_file in icon_files:
        path = resource_path(icon_file)
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        print(f"  {icon_file}: {'✓' if exists else '✗'} ({path}) - {size} bytes")

    # Test loading
    print("\nTesting icon loading...")
    icon = load_splash_icon(100)  # Back to 100px for better arrangement
    if icon and not icon.isNull():
        print(f"✓ Icon loaded successfully: {icon.size()}")
    else:
        print("✗ Icon loading failed")

    print("=== End Test ===")


class HALogApp:
    """
    Gobioeng HALog Application with optimized startup
    Professional LINAC Water System Monitor - gobioeng.com
    """

    def __init__(self):
        self.splash = None
        self.window = None
        self.splash_progress = 0
        self.splash_animation_timer = None
        self.min_splash_time = 2000  # Reduced for better UX
        self.load_times = {}
        self.app_version = APP_VERSION
        self.status_label = None
        self.progress_bar = None

    def create_splash(self):
        """
        Create professional splash screen with optimized layout
        Gobioeng HALog Implementation
        Developer: gobioeng.com
        """
        # Import everything explicitly
        QtWidgets = lazy_import("PyQt5.QtWidgets")
        QtGui = lazy_import("PyQt5.QtGui")
        QtCore = lazy_import("PyQt5.QtCore")

        # Create a splash screen with optimized size
        pixmap = QtGui.QPixmap(500, 320)  # Reduced height for better proportions
        self.splash = QtWidgets.QSplashScreen(pixmap)
        self.splash.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
        )

        # Get the pixmap for customization
        pixmap = self.splash.pixmap()
        pixmap.fill(QtCore.Qt.transparent)

        # Create a painter for drawing on the pixmap
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)

        # Solid gray background as requested
        gray_color = QtGui.QColor("#808080")  # Medium gray
        painter.fillRect(pixmap.rect(), QtGui.QBrush(gray_color))

        # Load OPTIMIZED ICON with proper spacing
        try:
            from resource_helper import load_splash_icon

            # Load with optimized size for splash screen (100px)
            logo_pixmap = load_splash_icon(100)

            # Create card-like container for icon
            card_x = 30
            card_y = 30
            card_size = 140  # Smaller card for better proportion

            # Draw elevation shadow
            for i in range(6):  # Reduced shadow layers
                shadow_color = QtGui.QColor(0, 0, 0, 15 - i * 2)
                painter.setBrush(QtGui.QBrush(shadow_color))
                painter.setPen(QtCore.Qt.NoPen)
                painter.drawRoundedRect(
                    card_x + i, card_y + i, card_size, card_size, 12, 12
                )

            # Draw card background
            painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 250)))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRoundedRect(card_x, card_y, card_size, card_size, 12, 12)

            # Position icon in center of card
            icon_x = card_x + (card_size - logo_pixmap.width()) // 2
            icon_y = card_y + (card_size - logo_pixmap.height()) // 2

            painter.drawPixmap(icon_x, icon_y, logo_pixmap)

            print(f"Icon loaded successfully: {logo_pixmap.size()}")

        except Exception as e:
            print(f"Error loading icon: {e}")
            # Fallback to generated icon
            from resource_helper import generate_icon

            fallback_icon = generate_icon(100, high_quality=True, color="#1976D2")

            # Draw card for fallback too
            card_x, card_y, card_size = 30, 30, 140
            painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 250)))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRoundedRect(card_x, card_y, card_size, card_size, 12, 12)

            icon_x = card_x + (card_size - fallback_icon.width()) // 2
            icon_y = card_y + (card_size - fallback_icon.height()) // 2
            painter.drawPixmap(icon_x, icon_y, fallback_icon)
            print("Using generated fallback icon")

        # Professional Typography - Primary Text (adjusted font size)
        painter.setPen(QtGui.QColor("#FFFFFF"))  # White text on gray background
        font = QtGui.QFont("Segoe UI", 18, QtGui.QFont.Medium)  # Reduced from 28px
        painter.setFont(font)
        app_name_rect = QtCore.QRect(200, 50, 280, 40)  # Moved to avoid overlap
        painter.drawText(
            app_name_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, "HALog"
        )

        # Professional Typography - Secondary Text (adjusted font size)
        painter.setPen(QtGui.QColor("#F0F0F0"))  # Light gray for contrast
        font = QtGui.QFont("Segoe UI", 12, QtGui.QFont.Normal)  # Slightly smaller
        painter.setFont(font)
        version_rect = QtCore.QRect(200, 90, 280, 25)
        painter.drawText(
            version_rect,
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
            f"Version {self.app_version} beta",
        )

        # Professional Typography - Body Text (adjusted font size)
        painter.setPen(QtGui.QColor("#E0E0E0"))  # Light gray for contrast
        font = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Normal)  # Standardized size
        painter.setFont(font)
        tagline_rect = QtCore.QRect(30, 180, 440, 20)  # Better positioning
        painter.drawText(
            tagline_rect,
            QtCore.Qt.AlignCenter,
            "Professional LINAC Water System Monitor",
        )

        # Professional Typography - Caption (Developer Credit) (adjusted font size)
        painter.setPen(QtGui.QColor("#D0D0D0"))
        font = QtGui.QFont("Segoe UI", 9, QtGui.QFont.Normal)  # Standardized size
        painter.setFont(font)
        developer_rect = QtCore.QRect(30, 260, 440, 18)  # Adjusted for reduced height
        painter.drawText(
            developer_rect, QtCore.Qt.AlignCenter, "Developed by gobioeng.com"
        )

        # Professional Typography - Caption (Company) (adjusted font size)
        painter.setPen(QtGui.QColor("#C0C0C0"))
        font = QtGui.QFont("Segoe UI", 8, QtGui.QFont.Normal)  # Smaller for footer
        painter.setFont(font)
        company_rect = QtCore.QRect(30, 278, 440, 16)  # Adjusted for reduced height
        painter.drawText(
            company_rect,
            QtCore.Qt.AlignCenter,
            "© 2025 gobioeng.com - All Rights Reserved",
        )

        # Finish painting
        painter.end()

        # Set the modified pixmap back
        self.splash.setPixmap(pixmap)

        # Professional Progress Bar
        self.progress_bar = QtWidgets.QProgressBar(self.splash)
        self.progress_bar.setGeometry(50, 230, 400, 5)  # Thinner, better positioned
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)  # No text on Material progress bar
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: none;
                border-radius: 2px;
                background-color: rgba(255, 255, 255, 50);
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 2px;
                margin: 0px;
            }
        """
        )

        # Professional Status Label (updated for gray background)
        self.status_label = QtWidgets.QLabel(self.splash)
        self.status_label.setGeometry(50, 205, 400, 20)  # Better positioned
        self.status_label.setStyleSheet(
            """
            color: #FFFFFF; 
            font-family: 'Segoe UI'; 
            font-size: 11px; 
            font-weight: 500;
            background: transparent;
        """
        )
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setText("Initializing application...")

        # Setup animation timer
        self.splash_animation_timer = QtCore.QTimer()
        self.splash_animation_timer.timeout.connect(self._update_animation)
        self.splash_animation_timer.start(80)  # Smoother animation

        # Show splash
        self.splash.show()

        # Process events to make splash visible immediately
        QtWidgets.QApplication.instance().processEvents()

        return self.splash

    def _update_animation(self):
        """Update splash screen animation - FIXED"""
        if not hasattr(self, "animation_step"):
            self.animation_step = 0
        self.animation_step = (self.animation_step + 1) % 6  # Smoother animation cycle

        # Professional loading dots animation
        if self.status_label:
            message = self.status_label.text().split("•")[0].strip()
            dots = "•" * (self.animation_step % 4)
            self.status_label.setText(f"{message} {dots}")

        # Smooth progress increment - FIXED: Convert to int
        if self.progress_bar and self.progress_bar.value() < 95:
            current_value = self.progress_bar.value()
            # Convert float to int before passing to setValue
            new_value = int(
                min(current_value + 1, 95)
            )  # Changed from 0.5 to 1 for integer increment
            self.progress_bar.setValue(new_value)

        # Process events to update UI
        QtWidgets = lazy_import("PyQt5.QtWidgets")
        QtWidgets.QApplication.instance().processEvents()

    def update_splash_progress(self, value, message=None):
        """Update splash progress with professional styling"""
        if not self.splash:
            return

        if message and hasattr(self, "status_label") and self.status_label:
            self.status_label.setText(message)

        if hasattr(self, "progress_bar") and self.progress_bar:
            # Ensure value is integer
            self.progress_bar.setValue(int(value))

        QtWidgets = lazy_import("PyQt5.QtWidgets")
        QtWidgets.QApplication.instance().processEvents()

    def create_main_window(self):
        """Create professional main application window"""
        start_window = time.time()
        QtWidgets = lazy_import("PyQt5.QtWidgets")
        QtCore = lazy_import("PyQt5.QtCore")
        QtGui = lazy_import("PyQt5.QtGui")

        self.update_splash_progress(30, "Loading interface...")

        # Import resources first to ensure icon is available
        try:
            from resource_helper import get_app_icon

            app_icon = get_app_icon()
        except Exception as e:
            print(f"Warning: Could not load app icon: {e}")
            app_icon = None

        # Import main components
        from main_window import Ui_MainWindow
        from database import DatabaseManager

        # Pre-optimize pandas if used
        try:
            import pandas as pd

            pd.set_option("compute.use_numexpr", True)
        except Exception as e:
            print(f"Warning: Could not configure pandas: {e}")

        # Set numpy thread control
        try:
            import numpy as np

            os.environ["OMP_NUM_THREADS"] = str(min(8, os.cpu_count() or 4))
            os.environ["MKL_NUM_THREADS"] = str(min(8, os.cpu_count() or 4))
            os.environ["NUMEXPR_NUM_THREADS"] = str(min(8, os.cpu_count() or 4))
        except Exception as e:
            print(f"Warning: Could not configure numpy: {e}")

        self.update_splash_progress(50, "Preparing interface components...")

        class HALogMaterialApp(QtWidgets.QMainWindow):
            """
            Main Gobioeng HALog Application Window
            Professional LINAC Log Analysis System - gobioeng.com
            """

            def __init__(self, parent=None):
                super().__init__(parent)

                # FIRST: Create the UI
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self)

                # SECOND: Set window properties
                self.setWindowTitle(
                    f"HALog {APP_VERSION} • Professional LINAC Monitor • gobioeng.com"
                )
                if app_icon:
                    self.setWindowIcon(app_icon)

                # THIRD: Apply professional styling
                try:
                    self.apply_professional_styles()
                except Exception as e:
                    print(f"Warning: Could not load professional styles: {e}")

                # FOURTH: Initialize actions AFTER UI is created
                self._init_actions()

                # FIFTH: Initialize database and components
                try:
                    self.db = DatabaseManager("halog_water.db")
                    import pandas as pd

                    self.df = pd.DataFrame()

                    # Initialize unified parser for fault codes and other data
                    from unified_parser import UnifiedParser
                    self.fault_parser = UnifiedParser()
                    
                    # Load fault code databases from core data directory
                    hal_fault_path = os.path.join(os.path.dirname(__file__), 'data', 'HALfault.txt')
                    tb_fault_path = os.path.join(os.path.dirname(__file__), 'data', 'TBFault.txt')
                    
                    # Load fault codes from both databases
                    hal_loaded = self.fault_parser.load_fault_codes_from_uploaded_file(hal_fault_path)
                    if hal_loaded:
                        print("✓ HAL fault codes loaded successfully")
                    
                    # Load TB fault codes (append to existing)
                    if os.path.exists(tb_fault_path):
                        try:
                            with open(tb_fault_path, 'r', encoding='utf-8') as file:
                                for line_num, line in enumerate(file, 1):
                                    line = line.strip()
                                    if not line or line.startswith('#'):
                                        continue
                                    fault_info = self.fault_parser._parse_fault_code_line(line)
                                    if fault_info:
                                        code = fault_info['code']
                                        self.fault_parser.fault_codes[code] = {
                                            'description': fault_info['description'],
                                            'source': 'tb',
                                            'line_number': line_num
                                        }
                            print(f"✓ TB fault codes loaded successfully")
                        except Exception as e:
                            print(f"Warning: Could not load TB fault codes: {e}")
                    
                    self._initialize_fault_code_tab()

                    # Initialize short data parser for enhanced parameters
                    self.shortdata_parser = self.fault_parser  # Use same unified parser instance
                    self.shortdata_parameters = self.shortdata_parser.parse_short_data_file(
                        os.path.join(os.path.dirname(__file__), 'data', 'shortdata.txt')
                    )
                    self._initialize_trend_controls()

                    # Setup UI components
                    self.load_dashboard()
                    self.ui.tabWidget.currentChanged.connect(self.on_tab_changed)
                    self._optimize_database()
                except Exception as e:
                    print(f"Error initializing database: {e}")
                    traceback.print_exc()

                # Setup memory monitoring
                self.memory_timer = QtCore.QTimer()
                self.memory_timer.timeout.connect(self._update_memory_usage)
                self.memory_timer.start(30000)

                # Setup branding in status bar
                self._setup_branding()

            def apply_professional_styles(self):
                """Apply comprehensive professional styling with VISIBLE MENU BAR"""
                material_stylesheet = """
                /* Professional Global Styles */
                QMainWindow {
                    background-color: #FAFAFA;
                    color: #1C1B1F;
                    font-family: 'Segoe UI', 'Roboto', 'Google Sans', 'Helvetica Neue', Arial, sans-serif;
                    font-size: 13px;
                    font-weight: 400;
                    line-height: 1.4;
                }
                
                /* HIGHLY VISIBLE Professional Menu Bar - FORCED VISIBILITY */
                                
                /* OPTIMIZED Professional Tab Widget */
                QTabWidget {
                    border: none;
                    background-color: transparent;
                }
                QTabWidget::pane {
                    border: none;
                    background-color: #FFFFFF;
                    border-radius: 12px;
                    margin-top: 8px;
                }
                QTabBar {
                    background-color: transparent;
                }
                QTabBar::tab {
                    background-color: transparent;
                    color: #79747E;
                    padding: 12px 20px;
                    margin-right: 2px;
                    border-radius: 8px 8px 0px 0px;
                    font-weight: 500;
                    font-size: 13px;
                    min-width: 100px;
                    border: none;
                }
                QTabBar::tab:selected {
                    background-color: #FFFFFF;
                    color: #1976D2;
                    font-weight: 600;
                    border-bottom: 2px solid #1976D2;
                }
                QTabBar::tab:hover:!selected {
                    background-color: #F7F2FA;
                    color: #1C1B1F;
                }
                
                /* OPTIMIZED Professional Cards (Group Boxes) */
                QGroupBox {
                    font-weight: 600;
                    color: #1C1B1F;
                    border: none;
                    border-radius: 12px;
                    margin-top: 24px;
                    padding-top: 20px;
                    background-color: #FFFFFF;
                    font-size: 14px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    left: 20px;
                    top: 8px;
                    padding: 8px 16px;
                    background-color: #E8F5E8;
                    color: #006A6B;
                    font-size: 14px;
                    font-weight: 600;
                    border-radius: 8px;
                    margin-top: -12px;
                }
                
                /* OPTIMIZED Professional Buttons */
                QPushButton {
                    background-color: #1976D2;
                    color: #FFFFFF;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 8px;
                    font-weight: 500;
                    font-size: 13px;
                    min-width: 100px;
                    min-height: 16px;
                    letter-spacing: 0.1px;
                }
                QPushButton:hover {
                    background-color: #1565C0;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
                QPushButton:disabled {
                    background-color: #E0E0E0;
                    color: #9E9E9E;
                }
                
                /* Danger Button */
                QPushButton#dangerButton {
                    background-color: #D32F2F;
                }
                QPushButton#dangerButton:hover {
                    background-color: #C62828;
                }
                QPushButton#dangerButton:pressed {
                    background-color: #B71C1C;
                }
                
                /* Success Button */
                QPushButton#successButton {
                    background-color: #388E3C;
                }
                QPushButton#successButton:hover {
                    background-color: #2E7D32;
                }
                QPushButton#successButton:pressed {
                    background-color: #1B5E20;
                }
                
                /* OPTIMIZED Professional Combo Boxes */
                QComboBox {
                    border: 1px solid #E0E0E0;
                    border-radius: 8px;
                    padding: 8px 12px;
                    background-color: #FAFAFA;
                    color: #1C1B1F;
                    min-width: 120px;
                    font-size: 13px;
                    font-weight: 500;
                }
                QComboBox:focus {
                    border: 2px solid #1976D2;
                    background-color: #FFFFFF;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 30px;
                }
                QComboBox::down-arrow {
                    border: none;
                    width: 0px;
                    height: 0px;
                }
                
                /* OPTIMIZED Professional Table Headers */
                QHeaderView::section {
                    background-color: #1976D2;
                    color: #FFFFFF;
                    padding: 8px 6px;
                    border: none;
                    font-weight: 600;
                    font-size: 12px;
                    border-radius: 0px;
                }
                
                /* OPTIMIZED Professional Tables */
                QTableWidget {
                    background-color: #FFFFFF;
                    alternate-background-color: #F8F9FA;
                    border: none;
                    border-radius: 8px;
                    gridline-color: #E0E0E0;
                    font-size: 12px;
                }
                QTableWidget::item {
                    padding: 6px 8px;
                    border-bottom: 1px solid #F0F0F0;
                }
                QTableWidget::item:selected {
                    background-color: #E3F2FD;
                    color: #1976D2;
                }
                
                /* OPTIMIZED Professional Labels */
                QLabel {
                    color: #1C1B1F;
                    font-size: 13px;
                    font-weight: 500;
                }
                QLabel#titleLabel {
                    color: #1976D2;
                    font-size: 24px;
                    font-weight: 700;
                    margin: 16px 0;
                }
                QLabel#subtitleLabel {
                    color: #49454F;
                    font-size: 16px;
                    font-weight: 500;
                    margin: 8px 0;
                }
                QLabel#captionLabel {
                    color: #79747E;
                    font-size: 11px;
                    font-weight: 400;
                }
                
                /* OPTIMIZED Professional Plot Frames */
                QFrame#plotFrame {
                    border: none;
                    border-radius: 12px;
                    background-color: #FFFFFF;
                    margin: 8px;
                    padding: 12px;
                }
                
                /* OPTIMIZED Professional Progress Bars */
                QProgressBar {
                    border: none;
                    border-radius: 4px;
                    background-color: #E0E0E0;
                    text-align: center;
                    color: #1C1B1F;
                    font-weight: 600;
                    height: 8px;
                }
                QProgressBar::chunk {
                    background-color: #1976D2;
                    border-radius: 4px;
                }
                
                /* OPTIMIZED Professional Status Bar */
                QStatusBar {
                    background-color: #FFFFFF;
                    border-top: 1px solid #E0E0E0;
                    color: #79747E;
                    font-size: 11px;
                    padding: 4px;
                }
                """

                self.setStyleSheet(material_stylesheet)

            def _init_actions(self):
                """Initialize all UI actions including MENU ACTIONS - COMPREHENSIVE CONNECTION"""
                try:
                    print("Connecting menu actions...")

                    # VERIFY MENU ITEMS EXIST
                    if not hasattr(self.ui, "actionOpen_Log_File"):
                        print("ERROR: actionOpen_Log_File not found in UI!")
                        return
                    if not hasattr(self.ui, "actionExit"):
                        print("ERROR: actionExit not found in UI!")
                        return
                    if not hasattr(self.ui, "actionAbout"):
                        print("ERROR: actionAbout not found in UI!")
                        return
                    if not hasattr(self.ui, "actionRefresh"):
                        print("ERROR: actionRefresh not found in UI!")
                        return

                    # MAIN MENU ACTIONS - FILE MENU
                    self.ui.actionOpen_Log_File.triggered.connect(self.import_log_file)
                    self.ui.actionExit.triggered.connect(self.close)
                    print("✓ File menu actions connected")

                    # VIEW MENU ACTIONS
                    self.ui.actionRefresh.triggered.connect(self.load_dashboard)
                    print("✓ View menu actions connected")

                    # DATA MENU ACTIONS
                    if hasattr(self.ui, "actionClearAllData"):
                        self.ui.actionClearAllData.triggered.connect(self.clear_all_data)
                        print("✓ Clear data action connected")
                    
                    if hasattr(self.ui, "actionOptimizeDatabase"):
                        self.ui.actionOptimizeDatabase.triggered.connect(self.optimize_database)
                        print("✓ Optimize database action connected")

                    # HELP MENU ACTIONS
                    self.ui.actionAbout.triggered.connect(self.show_about_dialog)
                    print("✓ Help menu actions connected")

                    # OPTIONAL MENU ACTIONS (if they exist)
                    if hasattr(self.ui, "actionExport_Data"):
                        self.ui.actionExport_Data.triggered.connect(self.export_data)
                        print("✓ Export action connected")

                    if hasattr(self.ui, "actionSettings"):
                        self.ui.actionSettings.triggered.connect(self.show_settings)
                        print("✓ Settings action connected")

                    if hasattr(self.ui, "actionAbout_Qt"):
                        self.ui.actionAbout_Qt.triggered.connect(
                            lambda: QtWidgets.QApplication.aboutQt()
                        )
                        print("✓ About Qt action connected")

                    # BUTTON ACTIONS
                    self.ui.btnClearDB.clicked.connect(self.clear_database)
                    self.ui.btnRefreshData.clicked.connect(self.load_dashboard)
                    
                    # Legacy trend controls (keep for backward compatibility)
                    if hasattr(self.ui, 'comboTrendSerial'):
                        self.ui.comboTrendSerial.currentIndexChanged.connect(self.update_trend)
                    if hasattr(self.ui, 'comboTrendParam'):
                        self.ui.comboTrendParam.currentIndexChanged.connect(self.update_trend)
                    
                    # NEW TREND SUB-TAB ACTIONS
                    if hasattr(self.ui, 'btnRefreshWater'):
                        self.ui.btnRefreshWater.clicked.connect(lambda: self.refresh_trend_tab('flow'))
                    if hasattr(self.ui, 'btnRefreshVoltage'):
                        self.ui.btnRefreshVoltage.clicked.connect(lambda: self.refresh_trend_tab('voltage'))
                    if hasattr(self.ui, 'btnRefreshTemp'):
                        self.ui.btnRefreshTemp.clicked.connect(lambda: self.refresh_trend_tab('temperature'))
                    if hasattr(self.ui, 'btnRefreshHumidity'):
                        self.ui.btnRefreshHumidity.clicked.connect(lambda: self.refresh_trend_tab('humidity'))
                    if hasattr(self.ui, 'btnRefreshFan'):
                        self.ui.btnRefreshFan.clicked.connect(lambda: self.refresh_trend_tab('fan_speed'))
                    
                    # NEW TREND DROPDOWN CHANGE EVENTS (auto-update on selection)
                    if hasattr(self.ui, 'comboWaterTopGraph'):
                        self.ui.comboWaterTopGraph.currentIndexChanged.connect(lambda: self.refresh_trend_tab('flow'))
                    if hasattr(self.ui, 'comboWaterBottomGraph'):
                        self.ui.comboWaterBottomGraph.currentIndexChanged.connect(lambda: self.refresh_trend_tab('flow'))
                    if hasattr(self.ui, 'comboVoltageTopGraph'):
                        self.ui.comboVoltageTopGraph.currentIndexChanged.connect(lambda: self.refresh_trend_tab('voltage'))
                    if hasattr(self.ui, 'comboVoltageBottomGraph'):
                        self.ui.comboVoltageBottomGraph.currentIndexChanged.connect(lambda: self.refresh_trend_tab('voltage'))
                    if hasattr(self.ui, 'comboTempTopGraph'):
                        self.ui.comboTempTopGraph.currentIndexChanged.connect(lambda: self.refresh_trend_tab('temperature'))
                    if hasattr(self.ui, 'comboTempBottomGraph'):
                        self.ui.comboTempBottomGraph.currentIndexChanged.connect(lambda: self.refresh_trend_tab('temperature'))
                    if hasattr(self.ui, 'comboHumidityTopGraph'):
                        self.ui.comboHumidityTopGraph.currentIndexChanged.connect(lambda: self.refresh_trend_tab('humidity'))
                    if hasattr(self.ui, 'comboHumidityBottomGraph'):
                        self.ui.comboHumidityBottomGraph.currentIndexChanged.connect(lambda: self.refresh_trend_tab('humidity'))
                    if hasattr(self.ui, 'comboFanTopGraph'):
                        self.ui.comboFanTopGraph.currentIndexChanged.connect(lambda: self.refresh_trend_tab('fan_speed'))
                    if hasattr(self.ui, 'comboFanBottomGraph'):
                        self.ui.comboFanBottomGraph.currentIndexChanged.connect(lambda: self.refresh_trend_tab('fan_speed'))
                    print("✓ Trend dropdown change events connected")
                    
                    # MPC TAB ACTIONS - Updated for new single-data approach
                    if hasattr(self.ui, 'btnRefreshMPC'):
                        self.ui.btnRefreshMPC.clicked.connect(self.refresh_latest_mpc)
                        
                        # Connect MPC date selection dropdowns
                        if hasattr(self.ui, 'comboMPCDateA'):
                            self.ui.comboMPCDateA.currentIndexChanged.connect(self.refresh_latest_mpc)
                        if hasattr(self.ui, 'comboMPCDateB'):
                            self.ui.comboMPCDateB.currentIndexChanged.connect(self.refresh_latest_mpc)
                    
                    # ANALYSIS TAB ACTIONS - Enhanced controls
                    if hasattr(self.ui, 'btnRefreshAnalysis'):
                        self.ui.btnRefreshAnalysis.clicked.connect(self.update_analysis_tab)
                    if hasattr(self.ui, 'comboAnalysisFilter'):
                        self.ui.comboAnalysisFilter.currentIndexChanged.connect(self._filter_analysis_results)
                    
                    # FAULT CODE TAB ACTIONS
                    if hasattr(self.ui, 'btnSearchCode'):
                        self.ui.btnSearchCode.clicked.connect(self.search_fault_code)
                        print("✓ Fault code search button connected")
                    
                    if hasattr(self.ui, 'btnSearchDescription'):
                        self.ui.btnSearchDescription.clicked.connect(self.search_fault_description)
                        print("✓ Fault description search button connected")
                    
                    if hasattr(self.ui, 'txtFaultCode'):
                        self.ui.txtFaultCode.returnPressed.connect(self.search_fault_code)
                        print("✓ Fault code input Enter key connected")
                    
                    if hasattr(self.ui, 'txtSearchDescription'):
                        self.ui.txtSearchDescription.returnPressed.connect(self.search_fault_description)
                        print("✓ Fault description input Enter key connected")
                    
                    print("✓ Button actions connected")

                    print("✓ ALL ACTIONS CONNECTED SUCCESSFULLY")

                except Exception as e:
                    print(f"ERROR connecting actions: {e}")
                    traceback.print_exc()

            def export_data(self):
                """Export data functionality (placeholder)"""
                QtWidgets.QMessageBox.information(
                    self,
                    "Export Data",
                    "Export functionality will be implemented in a future version.",
                )

            def show_settings(self):
                """Show settings dialog (placeholder)"""
                QtWidgets.QMessageBox.information(
                    self,
                    "Settings",
                    "Settings dialog will be implemented in a future version.",
                )

            def _initialize_fault_code_tab(self):
                """Initialize the fault code tab with statistics"""
                try:
                    if not hasattr(self, 'fault_parser'):
                        return
                    
                    stats = self.fault_parser.get_fault_code_statistics()
                    
                    if hasattr(self.ui, 'lblTotalCodes'):
                        # Calculate breakdown by source
                        hal_codes = sum(1 for code_info in self.fault_parser.fault_codes.values() if code_info.get('source') == 'uploaded')
                        tb_codes = sum(1 for code_info in self.fault_parser.fault_codes.values() if code_info.get('source') == 'tb')
                        self.ui.lblTotalCodes.setText(f"Total Codes: {stats['total_codes']} (HAL: {hal_codes}, TB: {tb_codes})")
                    
                    if hasattr(self.ui, 'lblFaultTypes'):
                        sources_text = f"Sources: {', '.join(stats['sources'])}"
                        self.ui.lblFaultTypes.setText(sources_text)
                    
                    print(f"✓ Fault code tab initialized with {stats['total_codes']} codes")
                    
                except Exception as e:
                    print(f"Error initializing fault code tab: {e}")

            def _initialize_trend_controls(self):
                """Initialize the trend controls with available parameters from database"""
                try:
                    if not hasattr(self, 'df') or self.df.empty:
                        print("⚠️ No database data available for trend controls")
                        return
                    
                    # Get unique serial numbers from database
                    if 'serial_number' in self.df.columns:
                        serial_numbers = sorted(list(set(self.df['serial_number'].astype(str).unique())))
                    elif 'serial' in self.df.columns:
                        serial_numbers = sorted(list(set(self.df['serial'].astype(str).unique())))
                    else:
                        serial_numbers = ['All']
                    
                    # Get all available parameters from database
                    param_column = 'parameter_type' if 'parameter_type' in self.df.columns else 'param'
                    all_params = list(self.df[param_column].unique())
                    
                    print(f"🔧 Initializing trend controls with {len(all_params)} parameters")
                    
                    # Categorize parameters by type
                    flow_params = []
                    voltage_params = []
                    temp_params = []
                    humidity_params = []
                    fan_params = []
                    
                    for param in all_params:
                        param_lower = param.lower()
                        if any(keyword in param_lower for keyword in ['flow', 'pump', 'water', 'magnetron']):
                            flow_params.append(param)
                        elif any(keyword in param_lower for keyword in ['volt', '_v_', '24v', '48v', '5v', 'bank', 'adc']):
                            voltage_params.append(param)
                        elif any(keyword in param_lower for keyword in ['temp', 'temperature']):
                            temp_params.append(param)
                        elif any(keyword in param_lower for keyword in ['humidity', 'humid']):
                            humidity_params.append(param)
                        elif any(keyword in param_lower for keyword in ['fan', 'speed']):
                            fan_params.append(param)
                    
                    # Populate dropdown controls with actual parameters
                    dropdown_configs = [
                        ('comboWaterTopGraph', flow_params),
                        ('comboWaterBottomGraph', flow_params),
                        ('comboVoltageTopGraph', voltage_params),
                        ('comboVoltageBottomGraph', voltage_params),
                        ('comboTempTopGraph', temp_params),
                        ('comboTempBottomGraph', temp_params),
                        ('comboHumidityTopGraph', humidity_params),
                        ('comboHumidityBottomGraph', humidity_params),
                        ('comboFanTopGraph', fan_params),
                        ('comboFanBottomGraph', fan_params),
                    ]
                    
                    for combo_name, params in dropdown_configs:
                        if hasattr(self.ui, combo_name):
                            combo = getattr(self.ui, combo_name)
                            combo.clear()
                            combo.addItem("Select parameter...")
                            if params:
                                # Use simplified names for display
                                for param in params[:10]:  # Limit to first 10
                                    display_name = self._get_display_name_for_param(param)
                                    combo.addItem(display_name)
                    
                    print(f"✓ Trend controls populated:")
                    print(f"  - Flow parameters: {len(flow_params)}")
                    print(f"  - Voltage parameters: {len(voltage_params)}")
                    print(f"  - Temperature parameters: {len(temp_params)}")
                    print(f"  - Humidity parameters: {len(humidity_params)}")
                    print(f"  - Fan parameters: {len(fan_params)}")
                    
                    # Initialize default trend graphs after controls are setup
                    QtCore.QTimer.singleShot(200, self._initialize_default_trend_displays)
                    
                except Exception as e:
                    print(f"Error initializing trend controls: {e}")
                    import traceback
                    traceback.print_exc()
            
            def _get_display_name_for_param(self, param_name):
                """Convert raw parameter name to user-friendly display name"""
                param_lower = param_name.lower()
                
                if 'magnetronflow' in param_lower:
                    return "Mag Flow"
                elif 'targetandcirculatorflow' in param_lower:
                    return "Flow Target"
                elif 'remotetemp' in param_lower:
                    return "Temp Room"
                elif 'humidity' in param_lower:
                    return "Room Humidity"
                elif 'magnetrontemp' in param_lower:
                    return "Temp Magnetron"
                elif 'banka' in param_lower and '24v' in param_lower:
                    return "MLC Bank A 24V"
                elif 'bankb' in param_lower and '24v' in param_lower:
                    return "MLC Bank B 24V"
                elif 'speed1' in param_lower or 'fan1' in param_lower:
                    return "Speed FAN 1"
                elif 'speed2' in param_lower or 'fan2' in param_lower:
                    return "Speed FAN 2"
                elif 'speed3' in param_lower or 'fan3' in param_lower:
                    return "Speed FAN 3"
                elif 'speed4' in param_lower or 'fan4' in param_lower:
                    return "Speed FAN 4"
                else:
                    # Return shortened version of original name
                    if len(param_name) > 50:
                        return param_name.split('::')[-1] if '::' in param_name else param_name[:50] + '...'
                    return param_name

            def refresh_trend_tab(self, group_name):
                """Refresh trend data for specific parameter group with new dropdown structure"""
                try:
                    if not hasattr(self, 'shortdata_parser'):
                        print(f"⚠️ Shortdata parser not available for {group_name}")
                        return
                    
                    # Get the appropriate combo boxes and graph widgets based on group
                    top_combo = None
                    bottom_combo = None
                    graph_top = None
                    graph_bottom = None
                    
                    if group_name == 'flow':  # Water System
                        top_combo = getattr(self.ui, 'comboWaterTopGraph', None)
                        bottom_combo = getattr(self.ui, 'comboWaterBottomGraph', None)
                        graph_top = getattr(self.ui, 'waterGraphTop', None)
                        graph_bottom = getattr(self.ui, 'waterGraphBottom', None)
                    elif group_name == 'voltage':
                        top_combo = getattr(self.ui, 'comboVoltageTopGraph', None)
                        bottom_combo = getattr(self.ui, 'comboVoltageBottomGraph', None)
                        graph_top = getattr(self.ui, 'voltageGraphTop', None)
                        graph_bottom = getattr(self.ui, 'voltageGraphBottom', None)
                    elif group_name == 'temperature':
                        top_combo = getattr(self.ui, 'comboTempTopGraph', None)
                        bottom_combo = getattr(self.ui, 'comboTempBottomGraph', None)
                        graph_top = getattr(self.ui, 'tempGraphTop', None)
                        graph_bottom = getattr(self.ui, 'tempGraphBottom', None)
                    elif group_name == 'humidity':
                        top_combo = getattr(self.ui, 'comboHumidityTopGraph', None)
                        bottom_combo = getattr(self.ui, 'comboHumidityBottomGraph', None)
                        graph_top = getattr(self.ui, 'humidityGraphTop', None)
                        graph_bottom = getattr(self.ui, 'humidityGraphBottom', None)
                    elif group_name == 'fan_speed':
                        top_combo = getattr(self.ui, 'comboFanTopGraph', None)
                        bottom_combo = getattr(self.ui, 'comboFanBottomGraph', None)
                        graph_top = getattr(self.ui, 'fanGraphTop', None)
                        graph_bottom = getattr(self.ui, 'fanGraphBottom', None)
                    
                    if not all([top_combo, bottom_combo, graph_top, graph_bottom]):
                        print(f"⚠️ Dropdown or graph widgets not found for {group_name}")
                        return
                    
                    # Get selected parameters from dropdowns
                    selected_top_param = top_combo.currentText() if top_combo.currentIndex() > 0 else None
                    selected_bottom_param = bottom_combo.currentText() if bottom_combo.currentIndex() > 0 else None
                    
                    # If no parameters selected, use default ones for this group
                    if not selected_top_param or selected_top_param == "Select parameter...":
                        if group_name == 'flow':
                            selected_top_param = "Mag Flow"
                        elif group_name == 'voltage':
                            selected_top_param = "MLC Bank A 24V"
                        elif group_name == 'temperature':
                            selected_top_param = "Temp Room"
                        elif group_name == 'humidity':
                            selected_top_param = "Room Humidity"
                        elif group_name == 'fan_speed':
                            selected_top_param = "Speed FAN 1"
                    
                    if not selected_bottom_param or selected_bottom_param == "Select parameter...":
                        if group_name == 'flow':
                            selected_bottom_param = "Flow Chiller Water"
                        elif group_name == 'voltage':
                            selected_bottom_param = "MLC Bank B 24V"
                        elif group_name == 'temperature':
                            selected_bottom_param = "Temp Magnetron"
                        elif group_name == 'humidity':
                            selected_bottom_param = "Temp Room"  # Fallback if only humidity param available
                        elif group_name == 'fan_speed':
                            selected_bottom_param = "Speed FAN 2"
                    
                    print(f"🔄 Refreshing {group_name} trends - Top: {selected_top_param}, Bottom: {selected_bottom_param}")
                    
                    # Import plotting utilities
                    from utils_plot import PlotUtils
                    import pandas as pd
                    
                    # Plot top graph
                    if selected_top_param and selected_top_param != "Select parameter...":
                        data_top = self._get_parameter_data_by_description(selected_top_param)
                        if not data_top.empty:
                            PlotUtils._plot_parameter_data_single(graph_top, data_top, selected_top_param)
                        else:
                            PlotUtils._plot_parameter_data_single(graph_top, pd.DataFrame(), f"No data available for {selected_top_param}")
                    else:
                        PlotUtils._plot_parameter_data_single(graph_top, pd.DataFrame(), "Select a parameter from dropdown")
                    
                    # Plot bottom graph  
                    if selected_bottom_param and selected_bottom_param != "Select parameter...":
                        data_bottom = self._get_parameter_data_by_description(selected_bottom_param)
                        if not data_bottom.empty:
                            PlotUtils._plot_parameter_data_single(graph_bottom, data_bottom, selected_bottom_param)
                        else:
                            PlotUtils._plot_parameter_data_single(graph_bottom, pd.DataFrame(), f"No data available for {selected_bottom_param}")
                    else:
                        PlotUtils._plot_parameter_data_single(graph_bottom, pd.DataFrame(), "Select a parameter from dropdown")
                    
                    print(f"✓ Successfully refreshed {group_name} trends")
                    
                except Exception as e:
                    print(f"❌ Error refreshing {group_name} trends: {e}")
                    import traceback
                    traceback.print_exc()

            def _get_parameter_data_by_description(self, parameter_description):
                """Get parameter data by its user-friendly description from the database"""
                try:
                    if not hasattr(self, 'df') or self.df.empty:
                        print("⚠️ No data available in database")
                        return pd.DataFrame()
                    
                    print(f"🔍 DataFrame columns: {list(self.df.columns)}")
                    print(f"🔍 DataFrame shape: {self.df.shape}")
                    
                    # Check which column name exists in the DataFrame
                    param_column = None
                    possible_columns = ['param', 'parameter_type', 'parameter_name']
                    
                    for col in possible_columns:
                        if col in self.df.columns:
                            param_column = col
                            break
                    
                    if not param_column:
                        print(f"⚠️ No parameter column found in DataFrame. Available columns: {list(self.df.columns)}")
                        return pd.DataFrame()
                    
                    print(f"🔍 Using parameter column: '{param_column}'")
                    
                    # Enhanced mapping to match actual database format with full parameter names
                    description_to_patterns = {
                        "Mag Flow": ["magnetronFlow"],
                        "Flow Target": ["targetAndCirculatorFlow"],
                        "Flow Chiller Water": ["cityWaterFlow"],
                        "Temp Room": ["FanremoteTempStatistics"],
                        "Room Humidity": ["FanhumidityStatistics"],
                        "Temp Magnetron": ["magnetronTemp"],
                        "Speed FAN 1": ["fanSpeed1"],
                        "Speed FAN 2": ["fanSpeed2"],
                        "Speed FAN 3": ["fanSpeed3"],
                        "Speed FAN 4": ["fanSpeed4"],
                        "MLC Bank A 24V": ["BANKA"],
                        "MLC Bank B 24V": ["BANKB"],
                    }
                    
                    # Get all available parameters
                    all_params = self.df[param_column].unique()
                    print(f"🔍 Available parameters: {all_params[:10]}")
                    
                    # Find matching parameter by searching within the full parameter names
                    matching_params = []
                    patterns = description_to_patterns.get(parameter_description, [parameter_description])
                    
                    print(f"🔍 Looking for patterns: {patterns}")
                    
                    # Search for patterns within the full parameter names
                    for pattern in patterns:
                        for param in all_params:
                            # Check if pattern exists anywhere in the parameter name
                            if pattern in param:
                                matching_params.append(param)
                                print(f"✓ Pattern '{pattern}' matched parameter: '{param}'")
                                break  # Take first match for each pattern
                    
                    # If no exact matches found, try case-insensitive search
                    if not matching_params:
                        print(f"🔍 No exact matches found, trying case-insensitive search...")
                        for pattern in patterns:
                            pattern_lower = pattern.lower()
                            for param in all_params:
                                if pattern_lower in param.lower():
                                    matching_params.append(param)
                                    print(f"✓ Case-insensitive match: '{param}' for pattern '{pattern}'")
                                    break
                    
                    # If still no matches, try partial keyword matching
                    if not matching_params:
                        print(f"🔍 No matches found, trying keyword search...")
                        keyword_mapping = {
                            "Mag Flow": ["magnetron", "flow"],
                            "Flow Target": ["target", "flow"],
                            "Flow Chiller Water": ["water", "flow", "city"],
                            "Temp Room": ["remote", "temp", "fan"],
                            "Room Humidity": ["humidity", "fan"],
                            "Temp Magnetron": ["magnetron", "temp"],
                        }
                        
                        if parameter_description in keyword_mapping:
                            keywords = keyword_mapping[parameter_description]
                            for param in all_params:
                                param_lower = param.lower()
                                # Check if all keywords are present
                                if all(keyword.lower() in param_lower for keyword in keywords):
                                    matching_params.append(param)
                                    print(f"✓ Keyword match: '{param}' for '{parameter_description}'")
                                    break
                    
                    if matching_params:
                        # Use the first matching parameter
                        selected_param = matching_params[0]
                        param_data = self.df[self.df[param_column] == selected_param].copy()
                        print(f"✓ Using parameter: '{selected_param}'")
                    else:
                        print(f"⚠️ No data found for parameter '{parameter_description}'")
                        print(f"⚠️ Available parameters: {all_params}")
                        return pd.DataFrame()
                    
                    if param_data.empty:
                        print(f"⚠️ Parameter data is empty for '{selected_param}'")
                        return pd.DataFrame()
                    
                    # Sort by datetime and return in the format expected by plotting functions
                    param_data = param_data.sort_values('datetime')
                    
                    # Check which value column exists
                    value_column = None
                    possible_value_columns = ['avg_value', 'avg', 'average', 'value']
                    
                    for col in possible_value_columns:
                        if col in param_data.columns:
                            value_column = col
                            break
                    
                    if not value_column:
                        print(f"⚠️ No value column found in DataFrame. Available columns: {list(param_data.columns)}")
                        return pd.DataFrame()
                    
                    # Rename columns to match plotting expectations
                    result_df = pd.DataFrame({
                        'datetime': param_data['datetime'],
                        'avg': param_data[value_column],
                        'parameter_name': [parameter_description] * len(param_data)
                    })
                    
                    print(f"✓ Retrieved {len(result_df)} data points for '{parameter_description}'")
                    return result_df
                    
                except Exception as e:
                    print(f"❌ Error getting parameter data for '{parameter_description}': {e}")
                    import traceback
                    traceback.print_exc()
                    return pd.DataFrame()

            def refresh_latest_mpc(self):
                """Load and display MPC results from database with date selection"""
                try:
                    print("🔄 Loading MPC data from database...")
                    
                    # Update available dates in dropdowns
                    self._populate_mpc_date_dropdowns()
                    
                    # Get selected dates
                    date_a = None
                    date_b = None
                    
                    if hasattr(self.ui, 'comboMPCDateA') and self.ui.comboMPCDateA.currentIndex() > 0:
                        date_a = self.ui.comboMPCDateA.currentText()
                    
                    if hasattr(self.ui, 'comboMPCDateB') and self.ui.comboMPCDateB.currentIndex() > 0:
                        date_b = self.ui.comboMPCDateB.currentText()
                    
                    # Get MPC data for comparison
                    mpc_data = self._get_mpc_comparison_data(date_a, date_b)
                    
                    if not mpc_data:
                        # Show helpful message about what data is needed
                        QtWidgets.QMessageBox.information(
                            self, "No MPC Data", 
                            "No machine performance data available.\n\n"
                            "Import log files containing machine performance parameters "
                            "(magnetron flow, temperature readings, voltage levels, etc.) "
                            "to enable MPC analysis."
                        )
                        return
                    
                    # Update the last update info
                    if hasattr(self.ui, 'lblLastMPCUpdate'):
                        from datetime import datetime
                        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        date_info = ""
                        if date_a and date_b:
                            date_info = f" (Comparing {date_a} vs {date_b})"
                        elif date_a:
                            date_info = f" (Date A: {date_a})"
                        elif date_b:
                            date_info = f" (Date B: {date_b})"
                        self.ui.lblLastMPCUpdate.setText(f"Last MPC Update: {update_time}{date_info}")
                    
                    # Update the MPC table with comparison data
                    self._populate_mpc_comparison_table(mpc_data, date_a, date_b)
                    
                    print("✅ MPC data loaded successfully")
                    
                except Exception as e:
                    print(f"❌ Error loading MPC data: {e}")
                    import traceback
                    traceback.print_exc()
                    QtWidgets.QMessageBox.critical(
                        self, "MPC Load Error", 
                        f"Error loading MPC data: {str(e)}"
                    )

            def _populate_mpc_date_dropdowns(self):
                """Populate MPC date selection dropdowns with available dates from database"""
                try:
                    if not hasattr(self, 'df') or self.df.empty:
                        print("No data available for MPC date selection")
                        return
                    
                    # Get unique dates from the database
                    unique_dates = sorted(self.df['datetime'].dt.date.unique(), reverse=True)
                    date_strings = [date.strftime('%Y-%m-%d') for date in unique_dates]
                    
                    # Update Date A dropdown
                    if hasattr(self.ui, 'comboMPCDateA'):
                        current_a = self.ui.comboMPCDateA.currentText()
                        self.ui.comboMPCDateA.blockSignals(True)
                        self.ui.comboMPCDateA.clear()
                        self.ui.comboMPCDateA.addItem("Select Date A...")
                        self.ui.comboMPCDateA.addItems(date_strings)
                        
                        # Restore selection if it still exists
                        if current_a in date_strings:
                            index = self.ui.comboMPCDateA.findText(current_a)
                            if index >= 0:
                                self.ui.comboMPCDateA.setCurrentIndex(index)
                        
                        self.ui.comboMPCDateA.blockSignals(False)
                    
                    # Update Date B dropdown
                    if hasattr(self.ui, 'comboMPCDateB'):
                        current_b = self.ui.comboMPCDateB.currentText()
                        self.ui.comboMPCDateB.blockSignals(True)
                        self.ui.comboMPCDateB.clear()
                        self.ui.comboMPCDateB.addItem("Select Date B...")
                        self.ui.comboMPCDateB.addItems(date_strings)
                        
                        # Restore selection if it still exists
                        if current_b in date_strings:
                            index = self.ui.comboMPCDateB.findText(current_b)
                            if index >= 0:
                                self.ui.comboMPCDateB.setCurrentIndex(index)
                        
                        self.ui.comboMPCDateB.blockSignals(False)
                    
                    print(f"Updated MPC date dropdowns with {len(date_strings)} dates")
                    
                except Exception as e:
                    print(f"Error populating MPC date dropdowns: {e}")

            def _get_mpc_comparison_data(self, date_a=None, date_b=None):
                """Get MPC data for comparison between two dates"""
                try:
                    if not hasattr(self, 'df') or self.df.empty:
                        return None
                    
                    # Define key MPC parameters to monitor
                    mpc_params = [
                        'magnetronFlow', 'magnetronTemp', 'targetAndCirculatorFlow', 'targetAndCirculatorTemp',
                        'FanremoteTempStatistics', 'FanhumidityStatistics', 
                        'FanfanSpeed1Statistics', 'FanfanSpeed2Statistics', 'FanfanSpeed3Statistics', 'FanfanSpeed4Statistics',
                        'MLC_ADC_CHAN_TEMP_BANKA_STAT_24V', 'MLC_ADC_CHAN_TEMP_BANKB_STAT_24V'
                    ]
                    
                    import pandas as pd
                    results = []
                    
                    for param in mpc_params:
                        param_data = self.df[self.df['param'] == param]
                        
                        if param_data.empty:
                            continue
                        
                        # Get description from parser mapping if available
                        description = param
                        if hasattr(self, 'parser') and hasattr(self.parser, 'parameter_mapping'):
                            mapping = self.parser.parameter_mapping.get(param, {})
                            description = mapping.get('description', param)
                        
                        value_a = "NA"
                        value_b = "NA"
                        status = "NA"
                        
                        # Get data for Date A
                        if date_a:
                            date_a_data = param_data[param_data['datetime'].dt.date == pd.to_datetime(date_a).date()]
                            if not date_a_data.empty:
                                value_a = f"{date_a_data['average'].iloc[-1]:.2f}"
                        
                        # Get data for Date B  
                        if date_b:
                            date_b_data = param_data[param_data['datetime'].dt.date == pd.to_datetime(date_b).date()]
                            if not date_b_data.empty:
                                value_b = f"{date_b_data['average'].iloc[-1]:.2f}"
                        
                        # Determine status based on comparison
                        if value_a != "NA" and value_b != "NA":
                            try:
                                diff_percent = abs((float(value_a) - float(value_b)) / float(value_a)) * 100
                                if diff_percent < 5:  # Within 5% tolerance
                                    status = "PASS"
                                elif diff_percent < 10:  # Within 10% tolerance
                                    status = "WARNING"
                                else:
                                    status = "FAIL"
                            except:
                                status = "CHECK"
                        elif value_a != "NA" or value_b != "NA":
                            status = "PARTIAL"
                        
                        results.append({
                            'parameter': description,
                            'date_a_value': value_a,
                            'date_b_value': value_b,
                            'status': status
                        })
                    
                    return results if results else None
                    
                except Exception as e:
                    print(f"Error getting MPC comparison data: {e}")
                    import traceback
                    traceback.print_exc()
                    return None

            def _populate_mpc_comparison_table(self, mpc_data, date_a, date_b):
                """Populate MPC table with comparison data"""
                try:
                    if not mpc_data:
                        self.ui.tableMPC.setRowCount(0)
                        return
                    
                    self.ui.tableMPC.setRowCount(len(mpc_data))
                    
                    for row, data in enumerate(mpc_data):
                        # Parameter name
                        param_item = QtWidgets.QLabel(data['parameter'])
                        param_item.setWordWrap(True)
                        param_item.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                        param_item.setMargin(5)
                        self.ui.tableMPC.setCellWidget(row, 0, param_item)
                        
                        # Date A value
                        date_a_item = QtWidgets.QTableWidgetItem(data['date_a_value'])
                        if data['date_a_value'] == "NA":
                            date_a_item.setBackground(Qt.lightGray)
                        date_a_item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableMPC.setItem(row, 1, date_a_item)
                        
                        # Date B value
                        date_b_item = QtWidgets.QTableWidgetItem(data['date_b_value'])
                        if data['date_b_value'] == "NA":
                            date_b_item.setBackground(Qt.lightGray)
                        date_b_item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableMPC.setItem(row, 2, date_b_item)
                        
                        # Status with color coding
                        status_item = QtWidgets.QLabel(data['status'])
                        status_item.setAlignment(Qt.AlignCenter)
                        
                        if data['status'] == "PASS":
                            status_item.setStyleSheet("color: green; font-weight: bold; background-color: #d4edda; padding: 4px; border-radius: 3px;")
                        elif data['status'] == "FAIL":
                            status_item.setStyleSheet("color: red; font-weight: bold; background-color: #f8d7da; padding: 4px; border-radius: 3px;")
                        elif data['status'] == "WARNING":
                            status_item.setStyleSheet("color: orange; font-weight: bold; background-color: #fff3cd; padding: 4px; border-radius: 3px;")
                        elif data['status'] == "NA":
                            status_item.setStyleSheet("color: gray; font-weight: bold; background-color: #f0f0f0; padding: 4px; border-radius: 3px;")
                        else:
                            status_item.setStyleSheet("color: blue; font-weight: bold; background-color: #cce7ff; padding: 4px; border-radius: 3px;")
                        
                        self.ui.tableMPC.setCellWidget(row, 3, status_item)
                    
                    # Resize rows to fit content
                    self.ui.tableMPC.resizeRowsToContents()
                    
                    # Update statistics
                    self._update_mpc_comparison_statistics(mpc_data)
                    
                except Exception as e:
                    print(f"Error populating MPC table: {e}")
                    import traceback
                    traceback.print_exc()

            def _update_mpc_comparison_statistics(self, mpc_data):
                """Update MPC statistics based on comparison data"""
                try:
                    if not mpc_data:
                        return
                    
                    total = len(mpc_data)
                    passed = sum(1 for item in mpc_data if item['status'] == 'PASS')
                    failed = sum(1 for item in mpc_data if item['status'] == 'FAIL')
                    warnings = sum(1 for item in mpc_data if item['status'] == 'WARNING')
                    na_count = sum(1 for item in mpc_data if item['status'] == 'NA')
                    
                    # Update statistics labels if they exist
                    if hasattr(self.ui, 'lblTotalParams'):
                        self.ui.lblTotalParams.setText(f"Total Parameters: {total}")
                    if hasattr(self.ui, 'lblPassedParams'):
                        self.ui.lblPassedParams.setText(f"Passed: {passed}")
                    if hasattr(self.ui, 'lblFailedParams'):
                        self.ui.lblFailedParams.setText(f"Failed: {failed}")
                    if hasattr(self.ui, 'lblWarningParams'):
                        self.ui.lblWarningParams.setText(f"Warnings: {warnings}")
                    
                    # Calculate pass rate excluding NA values
                    evaluated = total - na_count
                    pass_rate = (passed / evaluated * 100) if evaluated > 0 else 0
                    
                    print(f"MPC Statistics: {passed}/{evaluated} passed ({pass_rate:.1f}%), {warnings} warnings, {failed} failed, {na_count} NA")
                    
                except Exception as e:
                    print(f"Error updating MPC statistics: {e}")

            def _get_latest_mpc_data(self):
                """Get the latest MPC data from available sources"""
                try:
                    # In a real implementation, this would query the database for the latest MPC data
                    # For now, return simulated data with proper parameter names
                    import random
                    from datetime import datetime, timedelta
                    
                    # Enhanced MPC parameters with proper names and descriptions
                    mpc_parameters = [
                        {"name": "Magnetron Output Power", "result": f"{random.uniform(6.0, 6.2):.2f} MW", "status": "PASS"},
                        {"name": "Water Flow Rate Primary Loop", "result": f"{random.uniform(15.0, 18.0):.1f} L/min", "status": "PASS"},
                        {"name": "Water Temperature Inlet", "result": f"{random.uniform(18.0, 22.0):.1f} °C", "status": "PASS"},
                        {"name": "Water Temperature Outlet", "result": f"{random.uniform(25.0, 30.0):.1f} °C", "status": "PASS"},
                        {"name": "Cooling System Pressure", "result": f"{random.uniform(2.8, 3.2):.1f} bar", "status": "PASS"},
                        {"name": "MLC Bank A Voltage 48V", "result": f"{random.uniform(47.5, 48.5):.1f} V", "status": "PASS"},
                        {"name": "MLC Bank B Voltage 48V", "result": f"{random.uniform(47.5, 48.5):.1f} V", "status": "PASS"},
                        {"name": "MLC Bank A Voltage 24V", "result": f"{random.uniform(23.8, 24.2):.1f} V", "status": "PASS"},
                        {"name": "MLC Bank B Voltage 24V", "result": f"{random.uniform(23.8, 24.2):.1f} V", "status": "PASS"},
                        {"name": "Magnetron Temperature", "result": f"{random.uniform(35.0, 45.0):.1f} °C", "status": "PASS"},
                        {"name": "COL Board Temperature", "result": f"{random.uniform(30.0, 40.0):.1f} °C", "status": "PASS"},
                        {"name": "PDU Temperature", "result": f"{random.uniform(25.0, 35.0):.1f} °C", "status": "PASS"},
                        {"name": "Room Temperature", "result": f"{random.uniform(20.0, 25.0):.1f} °C", "status": "PASS"},
                        {"name": "Room Humidity Level", "result": f"{random.uniform(40.0, 60.0):.1f} %", "status": "PASS"},
                        {"name": "Fan Speed 1 (Cooling)", "result": f"{random.randint(2800, 3200)} RPM", "status": "PASS"},
                        {"name": "Fan Speed 2 (Exhaust)", "result": f"{random.randint(2700, 3100)} RPM", "status": "PASS"},
                        {"name": "Fan Speed 3 (Intake)", "result": f"{random.randint(2900, 3300)} RPM", "status": "PASS"},
                        {"name": "Fan Speed 4 (Circulation)", "result": f"{random.randint(2750, 3150)} RPM", "status": "PASS"},
                        {"name": "Water Tank Temperature", "result": f"{random.uniform(18.0, 24.0):.1f} °C", "status": "PASS"},
                        {"name": "Chiller Water Flow", "result": f"{random.uniform(12.0, 16.0):.1f} L/min", "status": "PASS"},
                    ]
                    
                    # Randomly set some parameters to warning/fail for realism
                    for param in random.sample(mpc_parameters, k=random.randint(0, 2)):
                        if random.random() < 0.7:  # 70% chance for warning, 30% for fail
                            param["status"] = "WARNING"
                        else:
                            param["status"] = "FAIL"
                    
                    return {
                        "timestamp": datetime.now() - timedelta(hours=random.randint(1, 24)),
                        "parameters": mpc_parameters
                    }
                    
                except Exception as e:
                    print(f"Error getting latest MPC data: {e}")
                    return None

            def _populate_mpc_table(self, mpc_data):
                """Populate the MPC table with the latest data"""
                try:
                    from PyQt5 import QtGui
                    from PyQt5.QtWidgets import QTableWidgetItem
                    from PyQt5.QtCore import Qt
                    
                    if not mpc_data or "parameters" not in mpc_data:
                        return
                    
                    parameters = mpc_data["parameters"]
                    self.ui.tableMPC.setRowCount(len(parameters))
                    
                    for row, param in enumerate(parameters):
                        # Parameter name (with word wrapping)
                        param_item = QTableWidgetItem(param["name"])
                        param_item.setFlags(param_item.flags() & ~Qt.ItemIsEditable)
                        self.ui.tableMPC.setItem(row, 0, param_item)
                        
                        # Result
                        result_item = QTableWidgetItem(param["result"])
                        result_item.setFlags(result_item.flags() & ~Qt.ItemIsEditable)
                        self.ui.tableMPC.setItem(row, 1, result_item)
                        
                        # Status with color coding
                        status_item = QTableWidgetItem(param["status"])
                        status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
                        
                        # Set color based on status
                        if param["status"] == "PASS":
                            status_item.setBackground(QtGui.QColor(200, 255, 200))  # Light green
                        elif param["status"] == "WARNING":
                            status_item.setBackground(QtGui.QColor(255, 255, 200))  # Light yellow
                        elif param["status"] == "FAIL":
                            status_item.setBackground(QtGui.QColor(255, 200, 200))  # Light red
                        
                        self.ui.tableMPC.setItem(row, 2, status_item)
                    
                    # Ensure proper row heights for text wrapping
                    self.ui.tableMPC.resizeRowsToContents()
                    
                except Exception as e:
                    print(f"Error populating MPC table: {e}")

            def _update_mpc_statistics(self, mpc_data):
                """Update MPC statistics display"""
                try:
                    if not mpc_data or "parameters" not in mpc_data:
                        return
                    
                    parameters = mpc_data["parameters"]
                    total = len(parameters)
                    passed = sum(1 for p in parameters if p["status"] == "PASS")
                    failed = sum(1 for p in parameters if p["status"] == "FAIL")
                    warnings = sum(1 for p in parameters if p["status"] == "WARNING")
                    
                    # Update summary labels
                    if hasattr(self.ui, 'lblTotalParams'):
                        self.ui.lblTotalParams.setText(f"Total Parameters: {total}")
                    if hasattr(self.ui, 'lblPassedParams'):
                        self.ui.lblPassedParams.setText(f"Passed: {passed}")
                    if hasattr(self.ui, 'lblFailedParams'):
                        self.ui.lblFailedParams.setText(f"Failed: {failed}")
                    if hasattr(self.ui, 'lblWarningParams'):
                        self.ui.lblWarningParams.setText(f"Warnings: {warnings}")
                    
                    # Update main statistics label
                    if hasattr(self.ui, 'lblMPCStats'):
                        pass_rate = (passed / total * 100) if total > 0 else 0
                        timestamp = mpc_data.get("timestamp", "Unknown")
                        if hasattr(timestamp, 'strftime'):
                            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            timestamp_str = str(timestamp)
                        
                        self.ui.lblMPCStats.setText(
                            f"MPC Check completed: {timestamp_str} | "
                            f"Pass Rate: {pass_rate:.1f}% | "
                            f"Total: {total}, Passed: {passed}, Failed: {failed}, Warnings: {warnings}"
                        )
                    
                except Exception as e:
                    print(f"Error updating MPC statistics: {e}")

            def compare_mpc_results(self):
                """Legacy function - kept for backward compatibility"""
                # This function is no longer needed but kept to avoid errors
                print("⚠️ MPC comparison function deprecated - using latest MPC data display instead")
                self.refresh_latest_mpc()

            def search_fault_code(self):
                """Search for a specific fault code"""
                try:
                    if not hasattr(self, 'fault_parser') or not hasattr(self.ui, 'txtFaultCode'):
                        return
                    
                    code = self.ui.txtFaultCode.text().strip()
                    if not code:
                        self.ui.txtFaultResult.setHtml(
                            "<p style='color: #f39c12;'><b>⚠️ Please enter a fault code</b></p>"
                        )
                        # Clear the HAL and TB description boxes
                        if hasattr(self.ui, 'txtHALDescription'):
                            self.ui.txtHALDescription.setPlainText("")
                        if hasattr(self.ui, 'txtTBDescription'):
                            self.ui.txtTBDescription.setPlainText("")
                        return
                    
                    result = self.fault_parser.search_fault_code(code)
                    
                    # Get descriptions from both databases
                    descriptions = self.fault_parser.get_fault_descriptions_by_database(code)
                    hal_description = descriptions['hal_description']
                    tb_description = descriptions['tb_description']
                    
                    # Update the HAL and TB description text boxes
                    if hasattr(self.ui, 'txtHALDescription'):
                        self.ui.txtHALDescription.setPlainText(hal_description)
                    if hasattr(self.ui, 'txtTBDescription'):
                        self.ui.txtTBDescription.setPlainText(tb_description)
                    
                    if result:
                        # Get database source information
                        db_desc = result.get('database_description', 'Unknown')
                        db_source = result.get('database', 'Unknown')
                        
                        html_result = f"""
                        <div style='background: #d4edda; border: 1px solid #c3e6cb; border-radius: 6px; padding: 12px; margin: 4px 0;'>
                            <h3 style='color: #155724; margin: 0 0 8px 0;'>✅ Fault Code Found</h3>
                            <p><b>Code:</b> {code}</p>
                            <p><b>Database Source:</b> <span style='background: #007bff; color: white; padding: 2px 8px; border-radius: 3px; font-weight: bold;'>{db_desc}</span></p>
                            <p><b>Type:</b> <span style='background: #e2e3e5; padding: 2px 6px; border-radius: 3px;'>{result['type']}</span></p>
                            <p><b>Description:</b></p>
                            <div style='background: #f8f9fa; border-left: 3px solid #6c757d; padding: 8px 12px; margin: 8px 0; font-family: monospace;'>
                                {result['description']}
                            </div>
                            <small style='color: #6c757d;'>Source: {db_source} database</small>
                        </div>
                        """
                        self.ui.txtFaultResult.setHtml(html_result)
                    else:
                        html_result = f"""
                        <div style='background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 6px; padding: 12px; margin: 4px 0;'>
                            <h3 style='color: #721c24; margin: 0 0 8px 0;'>❌ Code Not Found</h3>
                            <p>Fault code <b>{code}</b> was not found in either database.</p>
                            <p><b>Database Source:</b> <span style='background: #6c757d; color: white; padding: 2px 8px; border-radius: 3px; font-weight: bold;'>NA</span></p>
                            <p><small>Please check the code and try again. You can also try searching by description keywords.</small></p>
                        </div>
                        """
                        self.ui.txtFaultResult.setHtml(html_result)
                    
                except Exception as e:
                    error_html = f"""
                    <div style='background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 6px; padding: 12px;'>
                        <h3 style='color: #721c24; margin: 0 0 8px 0;'>🚫 Search Error</h3>
                        <p>An error occurred while searching: {str(e)}</p>
                    </div>
                    """
                    self.ui.txtFaultResult.setHtml(error_html)
                    print(f"Error in fault code search: {e}")

            def search_fault_description(self):
                """Search fault codes by description keywords"""
                try:
                    if not hasattr(self, 'fault_parser') or not hasattr(self.ui, 'txtSearchDescription'):
                        return
                    
                    search_term = self.ui.txtSearchDescription.text().strip()
                    if not search_term:
                        self.ui.txtFaultResult.setHtml(
                            "<p style='color: #f39c12;'><b>⚠️ Please enter keywords to search</b></p>"
                        )
                        return
                    
                    results = self.fault_parser.search_description(search_term)
                    
                    if results:
                        html_result = f"""
                        <div style='background: #d4edda; border: 1px solid #c3e6cb; border-radius: 6px; padding: 12px; margin: 4px 0;'>
                            <h3 style='color: #155724; margin: 0 0 8px 0;'>🔍 Found {len(results)} Results</h3>
                            <p><b>Search term:</b> "{search_term}"</p>
                        </div>
                        """
                        
                        for i, (fault_id, fault_data) in enumerate(results[:10]):  # Limit to first 10 results
                            db_desc = fault_data.get('database_description', fault_data.get('database', 'Unknown'))
                            if fault_data.get('database') == 'HAL':
                                db_desc = 'HAL Description'
                            elif fault_data.get('database') == 'TB':
                                db_desc = 'TB Description'
                            else:
                                db_desc = 'NA'
                                
                            html_result += f"""
                            <div style='background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 6px; padding: 10px; margin: 8px 0;'>
                                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;'>
                                    <b style='color: #495057;'>Code: {fault_id}</b>
                                    <div>
                                        <span style='background: #007bff; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px; margin-right: 4px;'>{db_desc}</span>
                                        <span style='background: #e2e3e5; padding: 2px 6px; border-radius: 3px; font-size: 11px;'>{fault_data['type']}</span>
                                    </div>
                                </div>
                                <div style='color: #6c757d; font-size: 13px; line-height: 1.4;'>
                                    {fault_data['description']}
                                </div>
                            </div>
                            """
                        
                        if len(results) > 10:
                            html_result += f"""
                            <div style='background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 6px; padding: 8px; margin: 8px 0; text-align: center;'>
                                <small>Showing first 10 of {len(results)} results. Refine your search for more specific results.</small>
                            </div>
                            """
                        
                        self.ui.txtFaultResult.setHtml(html_result)
                    else:
                        html_result = f"""
                        <div style='background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 6px; padding: 12px; margin: 4px 0;'>
                            <h3 style='color: #721c24; margin: 0 0 8px 0;'>❌ No Results Found</h3>
                            <p>No fault codes found containing <b>"{search_term}"</b>.</p>
                            <p><small>Try different keywords or check spelling.</small></p>
                        </div>
                        """
                        self.ui.txtFaultResult.setHtml(html_result)
                    
                except Exception as e:
                    error_html = f"""
                    <div style='background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 6px; padding: 12px;'>
                        <h3 style='color: #721c24; margin: 0 0 8px 0;'>🚫 Search Error</h3>
                        <p>An error occurred while searching: {str(e)}</p>
                    </div>
                    """
                    self.ui.txtFaultResult.setHtml(error_html)
                    print(f"Error in description search: {e}")

            def _optimize_database(self):
                """Apply database optimizations"""
                try:
                    if hasattr(self, "db"):
                        self.db.optimize_for_reading()
                except Exception as e:
                    print(f"Database optimization error: {e}")

            def _update_memory_usage(self):
                """Monitor and display memory usage"""
                try:
                    import psutil

                    process = psutil.Process()
                    memory_info = process.memory_info()
                    memory_mb = memory_info.rss / (1024 * 1024)

                    # Update status bar with memory usage
                    if hasattr(self, "memory_label"):
                        self.memory_label.setText(f"Memory: {memory_mb:.1f} MB")
                    else:
                        self.memory_label = QtWidgets.QLabel(
                            f"Memory: {memory_mb:.1f} MB"
                        )
                        self.statusBar().addPermanentWidget(self.memory_label)

                    # Force garbage collection if memory usage is too high
                    if memory_mb > 500:
                        import gc

                        gc.collect()
                except Exception:
                    pass

            def _setup_branding(self):
                """Setup branding elements in the status bar"""
                try:
                    # Create status bar with branding
                    status_bar = self.statusBar()
                    status_bar.setStyleSheet("""
                        QStatusBar {
                            background-color: #f8f9fa;
                            color: #6c757d;
                            border-top: 1px solid #dee2e6;
                            font-size: 11px;
                        }
                        QStatusBar::item {
                            border: none;
                        }
                    """)
                    
                    # Add branding label on the left
                    self.branding_label = QtWidgets.QLabel("Developed by gobioeng.com")
                    self.branding_label.setStyleSheet("""
                        QLabel {
                            color: #6c757d;
                            font-size: 11px;
                            padding: 2px 8px;
                        }
                    """)
                    status_bar.addWidget(self.branding_label)
                    
                    # Add stretch to push memory info to the right
                    status_bar.addWidget(QtWidgets.QLabel(), 1)  # Stretch
                    
                    print("✓ Branding setup complete")
                    
                except Exception as e:
                    print(f"Error setting up branding: {e}")

            def show_about_dialog(self):
                """Show professional about dialog"""
                try:
                    from about_dialog import AboutDialog

                    about_dialog = AboutDialog(self)
                    about_dialog.exec_()
                except ImportError as e:
                    print(f"Failed to load about dialog: {e}")
                    QtWidgets.QMessageBox.about(
                        self,
                        "Gobioeng HALog",
                        "HALog 0.0.1 beta\nProfessional LINAC Log Analysis System\nDeveloped by gobioeng.com\n© 2025 gobioeng.com",
                    )

            def load_dashboard(self):
                """Load dashboard with professional optimizations"""
                try:
                    if not hasattr(self, "db"):
                        print("Database not initialized")
                        return

                    # Use chunking for large datasets
                    try:
                        self.df = self.db.get_all_logs(chunk_size=10000)
                    except TypeError:
                        self.df = self.db.get_all_logs()

                    if not self.df.empty:
                        latest = self.df.sort_values("datetime").iloc[-1]
                        self.ui.lblSerial.setText(f"Serial: {latest['serial']}")
                        self.ui.lblDate.setText(f"Date: {latest['datetime'].date()}")

                        dt_min = self.df["datetime"].min()
                        dt_max = self.df["datetime"].max()
                        duration = dt_max - dt_min

                        self.ui.lblDuration.setText(f"Duration: {duration}")
                        self.ui.lblRecordCount.setText(
                            f"Total Records: {len(self.df):,}"
                        )

                        unique_params = self.df["param"].nunique()
                        self.ui.lblParameterCount.setText(
                            f"Parameters: {unique_params}"
                        )
                    else:
                        self.ui.lblSerial.setText("Serial: -")
                        self.ui.lblDate.setText("Date: -")
                        self.ui.lblDuration.setText("Duration: -")
                        self.ui.lblRecordCount.setText("Total Records: 0")
                        self.ui.lblParameterCount.setText("Parameters: 0")

                    # Update UI components
                    self.update_trend_combos()
                    self.update_data_table()
                    self.update_analysis_tab()
                    
                    # Initialize trend graphs with default parameters
                    QtCore.QTimer.singleShot(300, self._refresh_all_trends)
                    
                    # Initialize MPC tab with default data
                    QtCore.QTimer.singleShot(200, self.refresh_latest_mpc)

                except Exception as e:
                    print(f"Error loading dashboard: {e}")
                    traceback.print_exc()

            def _refresh_all_trends(self):
                """Refresh all trend graphs with default data"""
                try:
                    print("🔄 Refreshing all trend graphs with default data...")
                    
                    # Refresh each trend group with default parameters
                    trend_groups = ['flow', 'voltage', 'temperature', 'humidity', 'fan_speed']
                    
                    for group in trend_groups:
                        try:
                            self.refresh_trend_tab(group)
                        except Exception as e:
                            print(f"Error refreshing {group} trends: {e}")
                    
                    print("✅ All trend graphs refreshed")
                    
                except Exception as e:
                    print(f"Error refreshing trends: {e}")

            def clear_all_data(self):
                """Clear all imported data from the database"""
                try:
                    reply = QtWidgets.QMessageBox.question(
                        self, 
                        "Clear All Data", 
                        "Are you sure you want to clear all imported log data?\n\n"
                        "This action cannot be undone and will remove:\n"
                        "• All imported machine log data\n"
                        "• All file import history\n"
                        "• All trend and analysis data\n\n"
                        "Note: This will NOT affect the original log files.",
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                        QtWidgets.QMessageBox.No
                    )
                    
                    if reply == QtWidgets.QMessageBox.Yes:
                        if not hasattr(self, 'db'):
                            QtWidgets.QMessageBox.warning(self, "Error", "Database not initialized")
                            return
                        
                        # Clear the database
                        self.db.clear_all()
                        
                        # Clear UI data
                        import pandas as pd
                        if hasattr(self, 'df'):
                            self.df = pd.DataFrame()
                        
                        # Refresh UI
                        self.load_dashboard()
                        
                        QtWidgets.QMessageBox.information(
                            self, 
                            "Data Cleared", 
                            "All data has been successfully cleared from the database."
                        )
                        
                        print("✅ All data cleared successfully")
                    
                except Exception as e:
                    print(f"Error clearing data: {e}")
                    QtWidgets.QMessageBox.critical(
                        self, 
                        "Clear Data Error", 
                        f"Error clearing data: {str(e)}"
                    )

            def optimize_database(self):
                """Optimize the database for better performance"""
                try:
                    if not hasattr(self, 'db'):
                        QtWidgets.QMessageBox.warning(self, "Error", "Database not initialized")
                        return
                    
                    # Show progress dialog
                    progress = QtWidgets.QProgressDialog(
                        "Optimizing database...", None, 0, 100, self
                    )
                    progress.setWindowTitle("Database Optimization")
                    progress.setWindowModality(QtCore.Qt.WindowModal)
                    progress.show()
                    progress.setValue(25)
                    QtWidgets.QApplication.processEvents()
                    
                    # Get database size before optimization
                    size_before = self.db.get_database_size()
                    
                    progress.setValue(50)
                    progress.setLabelText("Running VACUUM operation...")
                    QtWidgets.QApplication.processEvents()
                    
                    # Optimize database
                    self.db.vacuum_database()
                    
                    progress.setValue(75)
                    progress.setLabelText("Applying reading optimizations...")
                    QtWidgets.QApplication.processEvents()
                    
                    # Apply reading optimizations
                    self.db.optimize_for_reading()
                    
                    progress.setValue(100)
                    QtWidgets.QApplication.processEvents()
                    
                    # Get database size after optimization
                    size_after = self.db.get_database_size()
                    size_saved = size_before - size_after
                    size_saved_mb = size_saved / (1024 * 1024) if size_saved > 0 else 0
                    
                    progress.close()
                    
                    QtWidgets.QMessageBox.information(
                        self, 
                        "Database Optimized", 
                        f"Database optimization completed successfully.\n\n"
                        f"Space saved: {size_saved_mb:.2f} MB\n"
                        f"Database should now perform better for queries and analysis."
                    )
                    
                    print(f"✅ Database optimized - saved {size_saved_mb:.2f} MB")
                    
                except Exception as e:
                    print(f"Error optimizing database: {e}")
                    QtWidgets.QMessageBox.critical(
                        self, 
                        "Optimization Error", 
                        f"Error optimizing database: {str(e)}"
                    )

            def update_trend_combos(self):
                """Update trend combo boxes with professional styling"""
                try:
                    if hasattr(self, "df") and not self.df.empty:
                        # Find correct column names dynamically
                        serial_col = None
                        param_col = None
                        
                        for col in self.df.columns:
                            if col in ['serial', 'serial_number']:
                                serial_col = col
                            elif col in ['param', 'parameter_type', 'parameter_name']:
                                param_col = col
                        
                        if serial_col:
                            serials = sorted(set(map(str, self.df[serial_col].unique())))
                        else:
                            serials = []
                            
                        if param_col:
                            params = sorted(set(map(str, self.df[param_col].unique())))
                        else:
                            params = []
                    else:
                        serials = []
                        params = []

                    # Check if the UI elements exist before accessing them
                    if hasattr(self.ui, 'comboTrendSerial'):
                        self.ui.comboTrendSerial.blockSignals(True)
                        self.ui.comboTrendSerial.clear()
                        self.ui.comboTrendSerial.addItems(["All"] + serials)
                        self.ui.comboTrendSerial.blockSignals(False)
                    
                    if hasattr(self.ui, 'comboTrendParam'):
                        self.ui.comboTrendParam.blockSignals(True)
                        self.ui.comboTrendParam.clear()
                        self.ui.comboTrendParam.addItems(["All"] + params)
                        self.ui.comboTrendParam.blockSignals(False)

                    self.update_trend()
                except Exception as e:
                    print(f"Error updating trend combos: {e}")

            def update_data_table(self, page_size=1000):
                """Update data table with professional styling"""
                try:
                    if not hasattr(self, "df") or self.df.empty:
                        self.ui.tableData.setRowCount(0)
                        self.ui.lblTableInfo.setText("No data available")
                        return

                    df_sorted = self.df.sort_values("datetime", ascending=False)
                    display_df = df_sorted.iloc[:page_size]

                    self.ui.tableData.setRowCount(len(display_df))
                    self.ui.tableData.setColumnCount(7)
                    self.ui.tableData.setHorizontalHeaderLabels(
                        [
                            "DateTime",
                            "Serial",
                            "Parameter",
                            "Average",
                            "Min",
                            "Max",
                            "Diff (Max-Min)",
                        ]
                    )

                    self.ui.tableData.setUpdatesEnabled(False)

                    # Map column names dynamically
                    serial_col = None
                    param_col = None
                    avg_col = None
                    min_col = None
                    max_col = None
                    
                    for col in display_df.columns:
                        if col in ['serial', 'serial_number']:
                            serial_col = col
                        elif col in ['param', 'parameter_type', 'parameter_name']:
                            param_col = col
                        elif col in ['avg', 'average', 'avg_value']:
                            avg_col = col
                        elif col in ['min', 'min_value']:
                            min_col = col
                        elif col in ['max', 'max_value']:
                            max_col = col

                    for i, (_, row) in enumerate(display_df.iterrows()):
                        self.ui.tableData.setItem(
                            i,
                            0,
                            QtWidgets.QTableWidgetItem(str(row.get("datetime", ""))),
                        )
                        self.ui.tableData.setItem(
                            i, 1, QtWidgets.QTableWidgetItem(str(row.get(serial_col, "")))
                        )
                        self.ui.tableData.setItem(
                            i, 2, QtWidgets.QTableWidgetItem(str(row.get(param_col, "")))
                        )
                        self.ui.tableData.setItem(
                            i, 3, QtWidgets.QTableWidgetItem(str(row.get(avg_col, "")))
                        )
                        self.ui.tableData.setItem(
                            i, 4, QtWidgets.QTableWidgetItem(str(row.get(min_col, "")))
                        )
                        self.ui.tableData.setItem(
                            i, 5, QtWidgets.QTableWidgetItem(str(row.get(max_col, "")))
                        )
                        
                        # Calculate diff if both min and max columns exist
                        diff_val = ""
                        if min_col and max_col:
                            try:
                                diff_val = float(row.get(max_col, 0)) - float(row.get(min_col, 0))
                                diff_val = f"{diff_val:.2f}"
                            except:
                                diff_val = row.get("diff", "")
                        
                        self.ui.tableData.setItem(
                            i, 6, QtWidgets.QTableWidgetItem(str(diff_val))
                        )

                    self.ui.tableData.setUpdatesEnabled(True)
                    total_records = len(self.df)
                    self.ui.lblTableInfo.setText(
                        f"Showing {min(page_size, total_records):,} of {total_records:,} records"
                    )

                except Exception as e:
                    print(f"Error updating data table: {e}")
                    traceback.print_exc()

            def update_analysis_tab(self):
                """Update analysis tab with professional progress"""
                try:
                    if not hasattr(self, "df") or self.df.empty:
                        self.ui.tableTrends.setRowCount(0)
                        return

                    if len(self.df) > 10000:
                        try:
                            from worker_thread import AnalysisWorker
                            from analyzer_data import DataAnalyzer

                            progress_dialog = QtWidgets.QProgressDialog(
                                "Analyzing data...", "Cancel", 0, 100, self
                            )
                            progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
                            progress_dialog.setMinimumDuration(0)
                            progress_dialog.setValue(0)
                            progress_dialog.show()

                            analyzer = DataAnalyzer()
                            worker = AnalysisWorker(analyzer, self.df)

                            worker.analysis_progress.connect(
                                lambda p, m: progress_dialog.setValue(p)
                            )
                            worker.analysis_finished.connect(
                                lambda results: self._display_analysis_results(
                                    results, progress_dialog
                                )
                            )
                            worker.analysis_error.connect(
                                lambda msg: self._handle_analysis_error(
                                    msg, progress_dialog
                                )
                            )

                            progress_dialog.canceled.connect(worker.cancel_analysis)
                            worker.start()
                        except Exception as e:
                            print(f"Error creating analysis worker: {e}")
                            self._direct_analysis()
                    else:
                        self._direct_analysis()

                except Exception as e:
                    print(f"Error updating analysis tab: {e}")
                    traceback.print_exc()

            def _direct_analysis(self):
                """Perform analysis directly without worker"""
                try:
                    from analyzer_data import DataAnalyzer

                    analyzer = DataAnalyzer()

                    analysis_df = self.df.copy()

                    if (
                        "param" in analysis_df.columns
                        and "parameter_type" not in analysis_df.columns
                    ):
                        analysis_df["parameter_type"] = analysis_df["param"]

                    if "statistic_type" not in analysis_df.columns:
                        if "stat_type" in analysis_df.columns:
                            analysis_df["statistic_type"] = analysis_df["stat_type"]
                        else:
                            analysis_df["statistic_type"] = "avg"

                    if (
                        "avg" in analysis_df.columns
                        and "value" not in analysis_df.columns
                    ):
                        analysis_df["value"] = analysis_df["avg"]

                    try:
                        trends_df = analyzer.calculate_advanced_trends(analysis_df)
                        self._populate_trends_table(trends_df)
                    except Exception as e:
                        print(f"Error calculating trends: {e}")
                        import pandas as pd

                        empty_trends = pd.DataFrame(
                            columns=[
                                "parameter_type",
                                "statistic_type",
                                "data_points",
                                "time_span_hours",
                                "trend_slope",
                                "trend_direction",
                                "trend_strength",
                            ]
                        )
                        self._populate_trends_table(empty_trends)

                except Exception as e:
                    print(f"Error in direct analysis: {e}")
                    traceback.print_exc()

            def _display_analysis_results(self, results, progress_dialog=None):
                """Display analysis results after worker completes"""
                try:
                    if progress_dialog:
                        progress_dialog.setValue(100)
                        progress_dialog.close()

                    if "trends" in results:
                        self._populate_trends_table(results["trends"])
                except Exception as e:
                    print(f"Error displaying analysis results: {e}")

            def _handle_analysis_error(self, error_message, progress_dialog=None):
                """Handle analysis errors from worker thread"""
                try:
                    if progress_dialog:
                        progress_dialog.close()

                    QtWidgets.QMessageBox.warning(
                        self,
                        "Analysis Error",
                        f"Error during data analysis: {error_message}",
                    )
                except Exception as e:
                    print(f"Error handling analysis error: {e}")

            def _populate_trends_table(self, trends_df):
                """Populate trends table with enhanced analysis results"""
                try:
                    from PyQt5 import QtGui
                    
                    if trends_df.empty:
                        self.ui.tableTrends.setRowCount(0)
                        return

                    self.ui.tableTrends.setRowCount(len(trends_df))
                    for i, (_, row) in enumerate(trends_df.iterrows()):
                        # Enhanced parameter name display
                        param_name = str(row.get("parameter_type", ""))
                        enhanced_name = self._get_enhanced_parameter_name(param_name)
                        
                        param_item = QtWidgets.QTableWidgetItem(enhanced_name)
                        param_item.setToolTip(f"Original: {param_name}")  # Show original name in tooltip
                        self.ui.tableTrends.setItem(i, 0, param_item)
                        
                        # Parameter group
                        group = self._get_parameter_group(param_name)
                        group_item = QtWidgets.QTableWidgetItem(group)
                        self.ui.tableTrends.setItem(i, 1, group_item)
                        
                        # Other columns
                        self.ui.tableTrends.setItem(
                            i, 2, QtWidgets.QTableWidgetItem(str(row.get("statistic_type", "")))
                        )
                        self.ui.tableTrends.setItem(
                            i, 3, QtWidgets.QTableWidgetItem(str(row.get("data_points", "")))
                        )
                        self.ui.tableTrends.setItem(
                            i, 4, QtWidgets.QTableWidgetItem(f"{row.get('time_span_hours', 0):.1f}")
                        )
                        
                        # Slope with color coding
                        slope = row.get('trend_slope', 0)
                        slope_item = QtWidgets.QTableWidgetItem(f"{slope:.4f}")
                        if slope > 0.01:
                            slope_item.setBackground(QtGui.QColor(255, 200, 200))  # Light red for increasing
                        elif slope < -0.01:
                            slope_item.setBackground(QtGui.QColor(200, 255, 200))  # Light green for decreasing
                        self.ui.tableTrends.setItem(i, 5, slope_item)
                        
                        # Direction with icons
                        direction = str(row.get("trend_direction", ""))
                        if direction.lower() == "increasing":
                            direction = "📈 Increasing"
                        elif direction.lower() == "decreasing":
                            direction = "📉 Decreasing"
                        elif direction.lower() == "stable":
                            direction = "➡️ Stable"
                        self.ui.tableTrends.setItem(i, 6, QtWidgets.QTableWidgetItem(direction))
                        
                        # Strength with color coding
                        strength = str(row.get("trend_strength", ""))
                        strength_item = QtWidgets.QTableWidgetItem(strength)
                        if strength.lower() == "strong":
                            strength_item.setBackground(QtGui.QColor(255, 255, 200))  # Light yellow
                        elif strength.lower() == "weak":
                            strength_item.setBackground(QtGui.QColor(240, 240, 240))  # Light gray
                        self.ui.tableTrends.setItem(i, 7, strength_item)
                        
                    # Ensure proper row heights
                    self.ui.tableTrends.resizeRowsToContents()
                    
                except Exception as e:
                    print(f"Error populating trends table: {e}")

            def _get_enhanced_parameter_name(self, param_name):
                """Map original parameter names to enhanced display names using parser mapping"""
                try:
                    # Try to get the enhanced name from the parser mapping first
                    from unified_parser import UnifiedParser
                    parser = UnifiedParser()
                    
                    # Check if this parameter has a mapping with description
                    if param_name in parser.parameter_mapping:
                        description = parser.parameter_mapping[param_name].get('description', param_name)
                        if description != param_name:
                            return description
                    
                    # Fallback to hardcoded mapping for compatibility
                    parameter_name_mapping = {
                        # Water System
                        "magnetronFlow": "Mag Flow",
                        "targetAndCirculatorFlow": "Flow Target",
                        "cityWaterFlow": "Flow Chiller Water", 
                        "pumpPressure": "Cooling Pump Pressure",
                        
                        # Voltages
                        "MLC_ADC_CHAN_TEMP_BANKA_STAT_48V": "MLC Bank A 48V",
                        "MLC_ADC_CHAN_TEMP_BANKB_STAT_48V": "MLC Bank B 48V",
                        "MLC_ADC_CHAN_TEMP_BANKA_STAT_24V": "MLC Bank A 24V",
                        "MLC_ADC_CHAN_TEMP_BANKB_STAT_24V": "MLC Bank B 24V",
                        "COL_ADC_CHAN_TEMP_24V_MON": "COL 24V Monitor",
                        "COL_ADC_CHAN_TEMP_5V_MON": "COL 5V Monitor",
                        
                        # Temperatures
                        "magnetronTemp": "Temp Magnetron",
                        "colBoardTemp": "Temp COL Board", 
                        "pduTemp": "Temp PDU",
                        "FanremoteTempStatistics": "Temp Room",
                        "waterTankTemp": "Temp Water Tank",
                        
                        # Fan Speeds
                        "FanfanSpeed1Statistics": "Speed FAN 1",
                        "FanfanSpeed2Statistics": "Speed FAN 2",
                        "FanfanSpeed3Statistics": "Speed FAN 3",
                        "FanfanSpeed4Statistics": "Speed FAN 4",
                        "FanSpeed1Statistics": "Speed FAN 1",
                        "FanSpeed2Statistics": "Speed FAN 2",
                        
                        # Humidity
                        "FanhumidityStatistics": "Room Humidity",
                    }
                    
                    # Return enhanced name if mapping exists, otherwise return original
                    return parameter_name_mapping.get(param_name, param_name)
                    
                except Exception as e:
                    print(f"Error getting enhanced parameter name for '{param_name}': {e}")
                    return param_name

            def _get_parameter_group(self, param_name):
                """Determine parameter group for categorization"""
                param_lower = param_name.lower()
                
                if any(term in param_lower for term in ['flow', 'pressure', 'pump']):
                    return "Water System"
                elif any(term in param_lower for term in ['volt', '_v_', '24v', '48v', '5v', 'mlc_adc', 'col_adc']):
                    return "Voltages"
                elif any(term in param_lower for term in ['temp', 'temperature']):
                    return "Temperatures"
                elif any(term in param_lower for term in ['fan', 'speed']):
                    return "Fan Speeds"
                elif any(term in param_lower for term in ['humidity']):
                    return "Humidity"
                else:
                    return "Other"

            def _filter_analysis_results(self):
                """Filter analysis results based on selected group"""
                try:
                    if not hasattr(self.ui, 'comboAnalysisFilter'):
                        return
                        
                    selected_filter = self.ui.comboAnalysisFilter.currentText()
                    
                    if selected_filter == "All Parameters":
                        # Show all rows
                        for row in range(self.ui.tableTrends.rowCount()):
                            self.ui.tableTrends.setRowHidden(row, False)
                    else:
                        # Hide rows that don't match the filter
                        filter_mapping = {
                            "Water System": "Water System",
                            "Voltages": "Voltages",
                            "Temperatures": "Temperatures", 
                            "Fan Speeds": "Fan Speeds",
                            "Humidity": "Humidity"
                        }
                        
                        target_group = filter_mapping.get(selected_filter, "")
                        
                        for row in range(self.ui.tableTrends.rowCount()):
                            group_item = self.ui.tableTrends.item(row, 1)  # Group is column 1
                            if group_item:
                                group_text = group_item.text()
                                should_hide = (target_group != group_text)
                                self.ui.tableTrends.setRowHidden(row, should_hide)
                                
                except Exception as e:
                    print(f"Error filtering analysis results: {e}")

            def on_tab_changed(self, index):
                """Handle tab changes with professional animations"""
                try:
                    if index == 1:  # Trends tab
                        self.update_trend()
                    elif index == 2:  # Data Table tab
                        self.update_data_table()
                    elif index == 3:  # Analysis tab
                        self.update_analysis_tab()
                except Exception as e:
                    print(f"Error handling tab change: {e}")

            def update_trend(self):
                """Update trend visualization with professional styling - Legacy compatibility"""
                try:
                    if not hasattr(self, "df") or self.df.empty:
                        return

                    # Check if legacy trend controls exist
                    if hasattr(self.ui, 'comboTrendSerial') and hasattr(self.ui, 'comboTrendParam'):
                        serial = self.ui.comboTrendSerial.currentText()
                        param = self.ui.comboTrendParam.currentText()

                        if serial == "All" and param == "All":
                            df_trend = self.df
                        else:
                            import numpy as np

                            mask = np.ones(len(self.df), dtype=bool)
                            if serial and serial != "All":
                                mask &= self.df["serial"] == serial
                            if param and param != "All":
                                mask &= self.df["param"] == param
                            df_trend = self.df[mask]

                        from utils_plot import plot_trend

                        # Check if legacy plotWidget exists
                        if hasattr(self.ui, 'plotWidget'):
                            if len(df_trend) > 10000:
                                print(f"Downsampling large trend data: {len(df_trend)} points")
                                plot_trend(self.ui.plotWidget, df_trend)
                            else:
                                plot_trend(self.ui.plotWidget, df_trend)
                        else:
                            print("Legacy plotWidget not found - using new trend system")
                    else:
                        # If legacy controls don't exist, initialize default trend displays for new system
                        print("Initializing trend displays with new system")
                        self._initialize_default_trends()

                except Exception as e:
                    print(f"Error updating trend: {e}")
                    traceback.print_exc()

            def _initialize_default_trend_displays(self):
                """Initialize default trend displays to show graphs at startup"""
                try:
                    print("🔄 Initializing default trend displays...")
                    # Check if we have shortdata_parser available
                    if hasattr(self, 'shortdata_parser') and self.shortdata_parser:
                        # Initialize each trend group with default displays
                        trend_groups = ['flow', 'voltage', 'temperature', 'humidity', 'fan_speed']
                        for group in trend_groups:
                            try:
                                self.refresh_trend_tab(group)
                                print(f"  ✓ {group} trend initialized")
                            except Exception as e:
                                print(f"  ⚠️ Failed to initialize {group} trend: {e}")
                    else:
                        print("  ⚠️ Shortdata parser not available for trend initialization")
                except Exception as e:
                    print(f"Error initializing default trend displays: {e}")

            def _initialize_default_trends(self):
                """Initialize default trend displays for the new trend tab system"""
                try:
                    # Trigger refresh for each trend tab group to show default graphs
                    trend_groups = ['flow', 'voltage', 'temperature', 'humidity', 'fan_speed']
                    for group in trend_groups:
                        self.refresh_trend_tab(group)
                except Exception as e:
                    print(f"Error initializing default trends: {e}")

            def import_log_file(self):
                """MAIN LOG FILE IMPORT FUNCTION - Enhanced with multi-file selection and filtering"""
                print("🔥 LOG FILE IMPORT TRIGGERED!")
                try:
                    # Enable multi-file selection
                    file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
                        self,
                        "Open LINAC Log Files (Select Multiple Files)",
                        "",
                        "Log Files (*.txt *.log);;Text Files (*.txt);;All Files (*)",
                    )

                    if not file_paths:
                        print("No files selected")
                        return

                    print(f"Selected {len(file_paths)} file(s):")
                    for file_path in file_paths:
                        print(f"  - {file_path}")

                    # Process each file
                    for file_path in file_paths:
                        file_size = os.path.getsize(file_path)
                        print(f"Processing file: {os.path.basename(file_path)} ({file_size} bytes)")
                        
                        filename = os.path.basename(file_path).lower()
                        
                        # Check if it's a shortdata file (sample only)
                        if 'shortdata' in filename:
                            print(f"⚠️ Treating {os.path.basename(file_path)} as sample data only (not permanently stored)")
                            self._process_sample_shortdata(file_path)
                        # Check if it's a fault file that should be filtered and stored permanently
                        elif 'tbfault' in filename or 'halfault' in filename:
                            print(f"🔍 Processing fault file with filtering: {os.path.basename(file_path)}")
                            if file_size < 5 * 1024 * 1024:
                                self._import_small_file_filtered(file_path)
                            else:
                                self._import_large_file_filtered(file_path, file_size)
                        else:
                            # Regular machine log file - import all data for MPC, trend, analysis
                            print(f"📊 Processing machine log file: {os.path.basename(file_path)}")
                            if file_size < 5 * 1024 * 1024:
                                self._import_small_file(file_path)
                            else:
                                self._import_large_file(file_path, file_size)
                        
                except Exception as e:
                    print(f"Error in import_log_file: {e}")
                    traceback.print_exc()
                    QtWidgets.QMessageBox.critical(
                        self, "Import Error", f"Error importing log file: {str(e)}"
                    )

            def _import_small_file(self, file_path):
                """Import small log file with professional progress"""
                try:
                    progress_dialog = QtWidgets.QProgressDialog(
                        "Processing file...", "Cancel", 0, 100, self
                    )
                    progress_dialog.setWindowTitle("Processing Log File")
                    progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
                    progress_dialog.show()
                    progress_dialog.setValue(10)
                    QtWidgets.QApplication.processEvents()

                    from unified_parser import UnifiedParser

                    parser = UnifiedParser()

                    progress_dialog.setValue(30)
                    QtWidgets.QApplication.processEvents()

                    df = parser.parse_linac_file(file_path)

                    progress_dialog.setValue(70)
                    QtWidgets.QApplication.processEvents()

                    records_inserted = self.db.insert_data_batch(df)

                    progress_dialog.setValue(90)
                    QtWidgets.QApplication.processEvents()

                    filename = os.path.basename(file_path)
                    parsing_stats_json = "{}"

                    self.db.insert_file_metadata(
                        filename=filename,
                        file_size=os.path.getsize(file_path),
                        records_imported=records_inserted,
                        parsing_stats=parsing_stats_json,
                    )

                    progress_dialog.setValue(100)
                    progress_dialog.close()

                    try:
                        self.df = self.db.get_all_logs(chunk_size=10000)
                    except TypeError:
                        self.df = self.db.get_all_logs()
                    self.load_dashboard()

                    QtWidgets.QMessageBox.information(
                        self,
                        "Import Successful",
                        f"Successfully imported {records_inserted:,} records.",
                    )

                    import gc

                    del df
                    gc.collect()

                except Exception as e:
                    QtWidgets.QMessageBox.critical(
                        self, "Processing Error", f"An error occurred: {str(e)}"
                    )
                    traceback.print_exc()

            def _import_large_file(self, file_path, file_size):
                """Import large log file with enhanced progress phases"""
                try:
                    from progress_dialog import ProgressDialog

                    self.progress_dialog = ProgressDialog(self)
                    self.progress_dialog.setWindowTitle("Processing LINAC Log File")
                    
                    # Start with uploading phase
                    self.progress_dialog.set_phase("uploading", 0)
                    self.progress_dialog.show()

                    from worker_thread import FileProcessingWorker

                    self.worker = FileProcessingWorker(file_path, file_size, self.db)
                    self.worker.chunk_size = 5000

                    # Enhanced progress handling with phases
                    def handle_progress_update(percentage, status_message="", lines_processed=0, total_lines=0, bytes_processed=0, total_bytes=0):
                        # Determine phase based on status message or progress
                        if "uploading" in status_message.lower() or "reading" in status_message.lower():
                            self.progress_dialog.set_phase("uploading", percentage)
                        elif "processing" in status_message.lower() or "parsing" in status_message.lower():
                            self.progress_dialog.set_phase("processing", percentage)
                        elif "finalizing" in status_message.lower() or "saving" in status_message.lower():
                            self.progress_dialog.set_phase("finalizing", percentage)
                        else:
                            # Default to processing phase
                            self.progress_dialog.set_phase("processing", percentage)
                    
                    self.worker.progress_update.connect(handle_progress_update)
                    self.worker.status_update.connect(
                        lambda msg: self.progress_dialog.setLabelText(msg)
                    )
                    self.worker.finished.connect(self.on_file_processing_finished)
                    self.worker.error.connect(self.on_file_processing_error)

                    self.progress_dialog.canceled.connect(self.worker.cancel_processing)

                    self.worker.start()
                except Exception as e:
                    QtWidgets.QMessageBox.critical(
                        self,
                        "Processing Error",
                        f"Error initializing file processing: {str(e)}",
                    )
                    traceback.print_exc()

            def _process_sample_shortdata(self, file_path):
                """Process shortdata as sample data and populate DataFrame for analysis"""
                try:
                    import pandas as pd
                    print(f"📋 Processing shortdata as sample: {os.path.basename(file_path)}")
                    
                    # Parse shortdata for trend analysis
                    from unified_parser import UnifiedParser
                    
                    parser = UnifiedParser()
                    parsed_data = parser.parse_short_data_file(file_path)
                    
                    if parsed_data and parsed_data.get('success'):
                        # Convert parsed data to DataFrame format for analysis
                        df_converted = parser.convert_short_data_to_dataframe(parsed_data)
                        
                        if not df_converted.empty:
                            # Store DataFrame for analysis and trends
                            self.df = df_converted
                            print(f"✓ DataFrame populated with {len(df_converted)} records")
                            
                            # Store in memory for trend controls
                            self.shortdata_parameters = parsed_data
                            self.shortdata_parser = parser
                            
                            # Initialize trend controls with the parsed data
                            self._initialize_trend_controls()
                            
                            # Update analysis tab to show the new data
                            self.update_analysis_tab()
                            
                            print(f"✓ Shortdata processed successfully for trend analysis and analysis tab")
                            QtWidgets.QMessageBox.information(
                                self,
                                "Sample Data Loaded", 
                                f"Shortdata loaded successfully!\n\n"
                                f"Parameters available: {len(parsed_data.get('parameters', []))}\n"
                                f"Records for analysis: {len(df_converted)}\n"
                                f"Unique parameters: {len(df_converted['parameter_type'].unique()) if not df_converted.empty else 0}\n\n"
                                f"Data is now available in:\n"
                                f"• Trend tab graphs\n"
                                f"• Analysis tab statistics"
                            )
                        else:
                            print("⚠️ DataFrame conversion failed - no data available")
                            QtWidgets.QMessageBox.warning(
                                self,
                                "Import Warning", 
                                "Shortdata file was processed but no data could be converted for analysis.\n"
                                "Please check the file format."
                            )
                    else:
                        print("⚠️ No data extracted from shortdata file")
                        QtWidgets.QMessageBox.warning(
                            self,
                            "Import Error", 
                            "No valid data could be extracted from the shortdata file.\n"
                            "Please check the file format."
                        )
                        
                except Exception as e:
                    print(f"Error processing shortdata: {e}")
                    traceback.print_exc()
                    QtWidgets.QMessageBox.critical(
                        self,
                        "Import Error", 
                        f"Error processing shortdata file: {str(e)}"
                    )

            def _import_small_file_filtered(self, file_path):
                """Import small log file with TB/HALfault filtering"""
                try:
                    progress_dialog = QtWidgets.QProgressDialog(
                        "Processing file with filtering...", "Cancel", 0, 100, self
                    )
                    progress_dialog.setWindowTitle("Processing Filtered Log File")
                    progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
                    progress_dialog.show()
                    progress_dialog.setValue(10)
                    QtWidgets.QApplication.processEvents()

                    # Read file and filter for TB/HALfault entries only
                    filtered_lines = []
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            line_lower = line.lower()
                            if 'tb' in line_lower or 'halfault' in line_lower or 'hal fault' in line_lower:
                                filtered_lines.append(line)

                    progress_dialog.setValue(30)
                    QtWidgets.QApplication.processEvents()

                    print(f"Filtered {len(filtered_lines)} relevant lines from file")

                    if filtered_lines:
                        # Create temporary filtered file
                        import tempfile
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                            temp_file.writelines(filtered_lines)
                            temp_path = temp_file.name

                        progress_dialog.setValue(50)
                        QtWidgets.QApplication.processEvents()

                        # Parse the filtered data
                        from unified_parser import UnifiedParser
                        parser = UnifiedParser()
                        df = parser.parse_linac_file(temp_path)

                        progress_dialog.setValue(70)
                        QtWidgets.QApplication.processEvents()

                        # Insert only the filtered data
                        records_inserted = self.db.insert_data_batch(df)

                        progress_dialog.setValue(90)
                        QtWidgets.QApplication.processEvents()

                        # Clean up temporary file
                        os.unlink(temp_path)

                        # Store metadata
                        filename = os.path.basename(file_path) + " (TB/HALfault filtered)"
                        parsing_stats_json = f'{{"filtered_lines": {len(filtered_lines)}, "total_records": {records_inserted}}}'

                        self.db.insert_file_metadata(
                            filename=filename,
                            file_size=len(''.join(filtered_lines)),
                            records_imported=records_inserted,
                            parsing_stats=parsing_stats_json,
                        )

                        progress_dialog.setValue(100)
                        progress_dialog.close()

                        # Refresh data
                        try:
                            self.df = self.db.get_all_logs(chunk_size=10000)
                        except TypeError:
                            self.df = self.db.get_all_logs()
                        self.load_dashboard()

                        QtWidgets.QMessageBox.information(
                            self,
                            "Import Successful",
                            f"Successfully imported {records_inserted:,} filtered records (TB/HALfault only).",
                        )
                    else:
                        progress_dialog.close()
                        QtWidgets.QMessageBox.information(
                            self,
                            "No Relevant Data",
                            "No TB or HALfault entries found in the selected file.",
                        )

                except Exception as e:
                    QtWidgets.QMessageBox.critical(
                        self, "Processing Error", f"An error occurred: {str(e)}"
                    )
                    traceback.print_exc()

            def _import_large_file_filtered(self, file_path, file_size):
                """Import large log file with TB/HALfault filtering"""
                try:
                    progress_dialog = QtWidgets.QProgressDialog(
                        "Processing large file with filtering...", "Cancel", 0, 100, self
                    )
                    progress_dialog.setWindowTitle("Processing Large Filtered Log File")
                    progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
                    progress_dialog.show()
                    
                    # Process file in chunks for large files
                    chunk_size = 1024 * 1024  # 1MB chunks
                    filtered_lines = []
                    processed_bytes = 0
                    
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        while True:
                            chunk = f.read(chunk_size)
                            if not chunk:
                                break
                                
                            processed_bytes += len(chunk.encode('utf-8'))
                            progress = min(50, int((processed_bytes / file_size) * 50))
                            progress_dialog.setValue(progress)
                            QtWidgets.QApplication.processEvents()
                            
                            if progress_dialog.wasCanceled():
                                return
                            
                            # Filter lines in chunk
                            lines = chunk.split('\n')
                            for line in lines:
                                line_lower = line.lower()
                                if 'tb' in line_lower or 'halfault' in line_lower or 'hal fault' in line_lower:
                                    filtered_lines.append(line + '\n')

                    print(f"Filtered {len(filtered_lines)} relevant lines from large file")
                    progress_dialog.setValue(60)
                    QtWidgets.QApplication.processEvents()

                    if filtered_lines:
                        # Process filtered data
                        import tempfile
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                            temp_file.writelines(filtered_lines)
                            temp_path = temp_file.name

                        progress_dialog.setValue(70)
                        QtWidgets.QApplication.processEvents()

                        # Use existing large file processing for filtered data
                        from unified_parser import UnifiedParser
                        parser = UnifiedParser()
                        df = parser.parse_linac_file(temp_path)

                        progress_dialog.setValue(85)
                        QtWidgets.QApplication.processEvents()

                        records_inserted = self.db.insert_data_batch(df)

                        # Clean up
                        os.unlink(temp_path)

                        # Store metadata
                        filename = os.path.basename(file_path) + " (TB/HALfault filtered)"
                        parsing_stats_json = f'{{"filtered_lines": {len(filtered_lines)}, "total_records": {records_inserted}}}'

                        self.db.insert_file_metadata(
                            filename=filename,
                            file_size=len(''.join(filtered_lines)),
                            records_imported=records_inserted,
                            parsing_stats=parsing_stats_json,
                        )

                        progress_dialog.setValue(100)
                        progress_dialog.close()

                        # Refresh data
                        try:
                            self.df = self.db.get_all_logs(chunk_size=10000)
                        except TypeError:
                            self.df = self.db.get_all_logs()
                        self.load_dashboard()

                        QtWidgets.QMessageBox.information(
                            self,
                            "Import Successful",
                            f"Successfully imported {records_inserted:,} filtered records (TB/HALfault only).",
                        )
                    else:
                        progress_dialog.close()
                        QtWidgets.QMessageBox.information(
                            self,
                            "No Relevant Data",
                            "No TB or HALfault entries found in the selected file.",
                        )

                except Exception as e:
                    QtWidgets.QMessageBox.critical(
                        self, "Processing Error", f"An error occurred: {str(e)}"
                    )
                    traceback.print_exc()

            def clear_database(self):
                """Clear database with professional confirmation"""
                try:
                    reply = QtWidgets.QMessageBox.question(
                        self,
                        "Confirm Clear Database",
                        "Are you sure you want to clear all data?",
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                        QtWidgets.QMessageBox.No,
                    )

                    if reply == QtWidgets.QMessageBox.Yes:
                        progress_dialog = QtWidgets.QProgressDialog(
                            "Clearing database...", "", 0, 100, self
                        )
                        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
                        progress_dialog.setCancelButton(None)
                        progress_dialog.setValue(10)
                        progress_dialog.show()
                        QtWidgets.QApplication.processEvents()

                        self.db.clear_all()

                        progress_dialog.setValue(50)
                        QtWidgets.QApplication.processEvents()

                        import pandas as pd

                        self.df = pd.DataFrame()

                        progress_dialog.setValue(70)
                        QtWidgets.QApplication.processEvents()

                        self.load_dashboard()

                        progress_dialog.setValue(100)
                        progress_dialog.close()

                        QtWidgets.QMessageBox.information(
                            self, "Database", "Data cleared successfully."
                        )

                        import gc

                        gc.collect()
                except Exception as e:
                    QtWidgets.QMessageBox.critical(
                        self, "Database Error", f"An error occurred: {str(e)}"
                    )
                    traceback.print_exc()

            def on_file_processing_finished(self, records_count, parsing_stats):
                """Handle completion of file processing"""
                try:
                    if hasattr(self, "progress_dialog") and self.progress_dialog:
                        self.progress_dialog.close()

                    if records_count > 0:
                        try:
                            self.df = self.db.get_all_logs(chunk_size=10000)
                        except TypeError:
                            self.df = self.db.get_all_logs()
                        self.load_dashboard()

                        QtWidgets.QMessageBox.information(
                            self,
                            "Import Successful",
                            f"Successfully imported {records_count:,} records.",
                        )

                        print(f"File processing completed: {parsing_stats}")
                    else:
                        QtWidgets.QMessageBox.warning(
                            self,
                            "Import Warning",
                            "No valid log entries found in the selected file.",
                        )

                    if hasattr(self, "worker"):
                        self.worker.deleteLater()
                        self.worker = None
                except Exception as e:
                    print(f"Error handling file processing completion: {e}")
                    traceback.print_exc()

            def on_file_processing_error(self, error_message):
                """Handle errors during file processing"""
                try:
                    if hasattr(self, "progress_dialog") and self.progress_dialog:
                        self.progress_dialog.close()

                    QtWidgets.QMessageBox.critical(
                        self, "Processing Error", f"An error occurred: {error_message}"
                    )

                    if hasattr(self, "worker"):
                        self.worker.deleteLater()
                        self.worker = None
                except Exception as e:
                    print(f"Error handling file processing error: {e}")
                    traceback.print_exc()

            def closeEvent(self, event):
                """Clean up resources when closing application"""
                try:
                    if hasattr(self, "memory_timer"):
                        self.memory_timer.stop()

                    if hasattr(self, "db"):
                        try:
                            self.db.vacuum_database()
                        except:
                            pass

                    import gc

                    gc.collect()

                    print("Window close event: cleaning up resources")
                    event.accept()
                except Exception as e:
                    print(f"Error during application close: {e}")
                    event.accept()

        self.window = HALogMaterialApp()
        self.update_splash_progress(80, "Finalizing interface...")
        self.load_times["window_creation"] = time.time() - start_window
        return self.window


def main():
    global startup_begin

    try:
        # Setup environment
        setup_environment()
        env_time = time.time() - startup_begin

        # Import Qt components
        QtWidgets = lazy_import("PyQt5.QtWidgets")
        QtCore = lazy_import("PyQt5.QtCore")
        QtGui = lazy_import("PyQt5.QtGui")

        # Create application with professional settings
        app = QtWidgets.QApplication(sys.argv)
        app.setApplicationName("Gobioeng HALog")
        app.setApplicationVersion(APP_VERSION)
        app.setOrganizationName("gobioeng.com")

        # Set professional font
        try:
            font = QtGui.QFont("Segoe UI", 9)  # Slightly smaller for better data focus
            app.setFont(font)
        except:
            pass

        qt_time = time.time() - startup_begin - env_time

        # Create HALog app
        halog_app = HALogApp()
        splash = halog_app.create_splash()
        splash_time = time.time() - startup_begin - env_time - qt_time

        # Create main window
        halog_app.update_splash_progress(20, "Creating interface...")
        window = halog_app.create_main_window()

        # Finalize startup
        halog_app.update_splash_progress(90, "Finalizing HALog...")

        # Schedule window display with smooth transition
        def finish_startup():
            if splash:
                splash.close()
            window.show()
            window.raise_()
            window.activateWindow()

        QtCore.QTimer.singleShot(600, finish_startup)  # Faster for better UX

        # Log startup timing
        total_time = time.time() - startup_begin
        print(f"🚀 Gobioeng HALog startup: {total_time:.3f}s")
        print(f"   Developed by gobioeng.com")
        print(f"   Professional LINAC Water System Monitor Complete")

        # Run application
        return app.exec_()

    except Exception as e:
        print(f"Error in startup: {e}")
        traceback.print_exc()

        # Try to show error dialog
        try:
            from PyQt5.QtWidgets import QApplication, QMessageBox

            app = QApplication.instance() or QApplication(sys.argv)
            QMessageBox.critical(
                None,
                "Startup Error",
                f"Error starting Gobioeng HALog: {str(e)}\n\nDeveloped by gobioeng.com\n\n{traceback.format_exc()}",
            )
        except:
            pass

        return 1


if __name__ == "__main__":
    # Uncomment this line to test icon loading:
    # test_icon_loading()
    sys.exit(main())
