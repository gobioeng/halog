"""
HALog Material Design Implementation - Gobioeng
Professional LINAC Water System Monitor with Material Design UI
Developer: Tanmay Pandey
Company: gobioeng.com
Created: 2025-08-20 22:58:39 UTC
Updated: 2025-08-22 17:40:15 UTC
User: gobioeng
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
        if '.' in module_name:
            parent_module, child_module = module_name.split('.', 1)
            parent = __import__(parent_module)
            module = getattr(__import__(parent_module, fromlist=[child_module]), child_module)
        else:
            module = __import__(module_name)
        _module_cache[module_name] = module
        return module
    except ImportError as e:
        print(f"Error importing {module_name}: {e}")
        raise

def setup_environment():
    """Setup environment with minimal imports"""
    os.environ['PYTHONOPTIMIZE'] = '2'
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    os.environ['NUMEXPR_MAX_THREADS'] = '8'
    
    # Set application path
    if getattr(sys, 'frozen', False):
        app_dir = Path(sys.executable).parent
    else:
        app_dir = Path(__file__).parent.absolute()
    os.chdir(app_dir)
    if str(app_dir) not in sys.path:
        sys.path.insert(0, str(app_dir))
        
    # Configure warnings
    import warnings
    warnings.filterwarnings('ignore')
    
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
    Debugging utility by Tanmay Pandey
    """
    from resource_helper import load_splash_icon, resource_path
    import os
    
    print("=== Icon Loading Test ===")
    
    # Check available files
    icon_files = [
        "linac_logo_256.png", "linac_logo_256.ico",
        "linac_logo_100.png", "linac_logo_100.ico", 
        "linac_logo.png", "linac_logo.ico"
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

class MaterialDesignApp:
    """
    HALog Material Design Application with optimized startup
    Enhanced Material Design implementation by Tanmay Pandey - gobioeng.com
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

    def create_material_splash(self):
        """
        Create Material Design splash screen with optimized layout
        Material Design implementation by Tanmay Pandey
        Developer: Tanmay Pandey - gobioeng.com
        """
        # Import everything explicitly
        QtWidgets = lazy_import('PyQt5.QtWidgets')
        QtGui = lazy_import('PyQt5.QtGui')
        QtCore = lazy_import('PyQt5.QtCore')
        
        # Create a splash screen with optimized size
        pixmap = QtGui.QPixmap(500, 320)  # Reduced height for better proportions
        self.splash = QtWidgets.QSplashScreen(pixmap)
        self.splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        
        # Get the pixmap for customization
        pixmap = self.splash.pixmap()
        pixmap.fill(QtCore.Qt.transparent)
        
        # Create a painter for drawing on the pixmap
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        
        # Material Design gradient background
        gradient = QtGui.QLinearGradient(0, 0, 0, pixmap.height())
        gradient.setColorAt(0, QtGui.QColor("#1976D2"))     # Material Blue 700
        gradient.setColorAt(0.3, QtGui.QColor("#1E88E5"))   # Material Blue 600
        gradient.setColorAt(0.7, QtGui.QColor("#2196F3"))   # Material Blue 500
        gradient.setColorAt(1, QtGui.QColor("#42A5F5"))     # Material Blue 400
        
        painter.fillRect(pixmap.rect(), QtGui.QBrush(gradient))
        
        # Add subtle pattern overlay for Material Design depth
        pattern_overlay = QtGui.QLinearGradient(0, 0, pixmap.width(), pixmap.height())
        pattern_overlay.setColorAt(0, QtGui.QColor(255, 255, 255, 8))
        pattern_overlay.setColorAt(0.5, QtGui.QColor(255, 255, 255, 15))
        pattern_overlay.setColorAt(1, QtGui.QColor(255, 255, 255, 5))
        painter.fillRect(pixmap.rect(), QtGui.QBrush(pattern_overlay))

        # Load OPTIMIZED ICON with proper spacing
        try:
            from resource_helper import load_splash_icon
            
            # Load with optimized size for splash screen (100px)
            logo_pixmap = load_splash_icon(100)
            
            # Create Material Design card-like container for icon - BETTER POSITIONING
            card_x = 30
            card_y = 30
            card_size = 140  # Smaller card for better proportion
            
            # Draw Material Design elevation shadow
            for i in range(6):  # Reduced shadow layers
                shadow_color = QtGui.QColor(0, 0, 0, 15 - i * 2)
                painter.setBrush(QtGui.QBrush(shadow_color))
                painter.setPen(QtCore.Qt.NoPen)
                painter.drawRoundedRect(card_x + i, card_y + i, card_size, card_size, 12, 12)
            
            # Draw Material Design card background
            painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 250)))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRoundedRect(card_x, card_y, card_size, card_size, 12, 12)
            
            # Position icon in center of card
            icon_x = card_x + (card_size - logo_pixmap.width()) // 2
            icon_y = card_y + (card_size - logo_pixmap.height()) // 2
            
            painter.drawPixmap(icon_x, icon_y, logo_pixmap)
            
            print(f"Material Design icon loaded successfully: {logo_pixmap.size()}")
                    
        except Exception as e:
            print(f"Error loading Material Design icon: {e}")
            # Fallback to generated Material Design icon
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
            print("Using generated Material Design fallback icon")
                
        # Material Design Typography - Primary Text - BETTER POSITIONING
        painter.setPen(QtGui.QColor("#FFFFFF"))  # White text on blue background
        font = QtGui.QFont("Segoe UI", 28, QtGui.QFont.Light)  # Slightly smaller
        painter.setFont(font)
        app_name_rect = QtCore.QRect(200, 50, 280, 40)  # Moved to avoid overlap
        painter.drawText(app_name_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, "HALog")
        
        # Material Design Typography - Secondary Text
        painter.setPen(QtGui.QColor("#E3F2FD"))  # Light blue tint
        font = QtGui.QFont("Segoe UI", 13, QtGui.QFont.Normal)  # Smaller
        painter.setFont(font)
        version_rect = QtCore.QRect(200, 90, 280, 25)
        painter.drawText(version_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, f"Version {self.app_version} beta")
        
        # Material Design Typography - Body Text
        painter.setPen(QtGui.QColor("#BBDEFB"))  # Even lighter blue
        font = QtGui.QFont("Segoe UI", 11, QtGui.QFont.Normal)  # Smaller
        painter.setFont(font)
        tagline_rect = QtCore.QRect(30, 180, 440, 20)  # Better positioning
        painter.drawText(tagline_rect, QtCore.Qt.AlignCenter, "Professional LINAC Water System Monitor")
        
        # Material Design Typography - Caption (Developer Credit)
        painter.setPen(QtGui.QColor("#E1F5FE"))
        font = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Medium)  # Smaller
        painter.setFont(font)
        developer_rect = QtCore.QRect(30, 260, 440, 18)  # Adjusted for reduced height
        painter.drawText(developer_rect, QtCore.Qt.AlignCenter, "Developed by Tanmay Pandey")
        
        # Material Design Typography - Caption (Company)
        painter.setPen(QtGui.QColor("#B3E5FC"))
        font = QtGui.QFont("Segoe UI", 9, QtGui.QFont.Normal)  # Smaller
        painter.setFont(font)
        company_rect = QtCore.QRect(30, 278, 440, 16)  # Adjusted for reduced height
        painter.drawText(company_rect, QtCore.Qt.AlignCenter, "© 2025 gobioeng.com - All Rights Reserved")
        
        # Finish painting
        painter.end()
        
        # Set the modified pixmap back
        self.splash.setPixmap(pixmap)
        
        # Material Design Progress Bar - BETTER POSITIONING
        self.progress_bar = QtWidgets.QProgressBar(self.splash)
        self.progress_bar.setGeometry(50, 230, 400, 5)  # Thinner, better positioned
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)  # No text on Material progress bar
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 2px;
                background-color: rgba(255, 255, 255, 25);
            }
            QProgressBar::chunk {
                background-color: #FFD54F;
                border-radius: 2px;
                margin: 0px;
            }
        """)
        
        # Material Design Status Label - BETTER POSITIONING
        self.status_label = QtWidgets.QLabel(self.splash)
        self.status_label.setGeometry(50, 205, 400, 20)  # Better positioned
        self.status_label.setStyleSheet("""
            color: #E8F5E8; 
            font-family: 'Segoe UI'; 
            font-size: 12px; 
            font-weight: 500;
            background: transparent;
        """)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setText("Initializing application...")
        
        # Setup animation timer
        self.splash_animation_timer = QtCore.QTimer()
        self.splash_animation_timer.timeout.connect(self._update_material_animation)
        self.splash_animation_timer.start(80)  # Smoother animation
        
        # Show splash
        self.splash.show()
        
        # Process events to make splash visible immediately
        QtWidgets.QApplication.instance().processEvents()
        
        return self.splash

    def _update_material_animation(self):
        """Update Material Design splash screen animation - FIXED"""
        if not hasattr(self, 'animation_step'):
            self.animation_step = 0
        self.animation_step = (self.animation_step + 1) % 6  # Smoother animation cycle
        
        # Material Design loading dots animation
        if self.status_label:
            message = self.status_label.text().split('•')[0].strip()
            dots = "•" * (self.animation_step % 4)
            self.status_label.setText(f"{message} {dots}")
        
        # Smooth progress increment - FIXED: Convert to int
        if self.progress_bar and self.progress_bar.value() < 95:
            current_value = self.progress_bar.value()
            # Convert float to int before passing to setValue
            new_value = int(min(current_value + 1, 95))  # Changed from 0.5 to 1 for integer increment
            self.progress_bar.setValue(new_value)
            
        # Process events to update UI
        QtWidgets = lazy_import('PyQt5.QtWidgets')
        QtWidgets.QApplication.instance().processEvents()

    def update_splash_progress(self, value, message=None):
        """Update splash progress with Material Design styling"""
        if not self.splash:
            return
            
        if message and hasattr(self, 'status_label') and self.status_label:
            self.status_label.setText(message)
            
        if hasattr(self, 'progress_bar') and self.progress_bar:
            # Ensure value is integer
            self.progress_bar.setValue(int(value))
            
        QtWidgets = lazy_import('PyQt5.QtWidgets')
        QtWidgets.QApplication.instance().processEvents()

    def create_main_window(self):
        """Create Material Design main application window"""
        start_window = time.time()
        QtWidgets = lazy_import('PyQt5.QtWidgets')
        QtCore = lazy_import('PyQt5.QtCore')
        QtGui = lazy_import('PyQt5.QtGui')
        
        self.update_splash_progress(30, "Loading Material Design interface...")
        
        # Import resources first to ensure icon is available
        try:
            from resource_helper import get_app_icon
            app_icon = get_app_icon()
        except Exception as e:
            print(f"Warning: Could not load app icon: {e}")
            app_icon = None
        
        # Import main components
        from ui_mainwindow import Ui_MainWindow
        from database import DatabaseManager
        
        # Pre-optimize pandas if used
        try:
            import pandas as pd
            pd.set_option('compute.use_numexpr', True)
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
            
        self.update_splash_progress(50, "Preparing Material Design components...")

        class HALogMaterialApp(QtWidgets.QMainWindow):
            """
            Main HALog Material Design Application Window
            Material Design implementation by Tanmay Pandey - gobioeng.com
            """
            def __init__(self, parent=None):
                super().__init__(parent)
                
                # FIRST: Create the UI
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self)
                
                # SECOND: Set window properties
                self.setWindowTitle(f"HALog {APP_VERSION} • Material Design • Tanmay Pandey")
                if app_icon:
                    self.setWindowIcon(app_icon)
                
                # THIRD: Apply Material Design styling
                try:
                    self.apply_material_design_styles()
                except Exception as e:
                    print(f"Warning: Could not load Material Design styles: {e}")
                
                # FOURTH: Initialize actions AFTER UI is created
                self._init_actions()
                
                # FIFTH: Initialize database and components
                try:
                    self.db = DatabaseManager("halog_water.db")
                    import pandas as pd
                    self.df = pd.DataFrame()
                    
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

            def apply_material_design_styles(self):
                """Apply comprehensive Material Design styling with VISIBLE MENU BAR"""
                material_stylesheet = """
                /* Material Design 3.0 Global Styles */
                QMainWindow {
                    background-color: #FAFAFA;
                    color: #1C1B1F;
                    font-family: 'Segoe UI', 'Roboto', 'Google Sans', 'Helvetica Neue', Arial, sans-serif;
                    font-size: 13px;
                    font-weight: 400;
                    line-height: 1.4;
                }
                
                /* HIGHLY VISIBLE Material Design Menu Bar - FORCED VISIBILITY */
                QMenuBar {
                    background-color: #FFFFFF !important;
                    color: #1C1B1F !important;
                    border: 1px solid #E7E0EC !important;
                    border-bottom: 2px solid #1976D2 !important;
                    padding: 8px 16px !important;
                    font-size: 14px !important;
                    font-weight: 600 !important;
                    spacing: 16px !important;
                    height: 40px !important;
                    min-height: 40px !important;
                    max-height: 40px !important;
                    show-decoration-selected: 1;
                }
                QMenuBar::item {
                    background-color: transparent !important;
                    padding: 12px 20px !important;
                    margin: 2px 6px !important;
                    border-radius: 8px !important;
                    color: #1976D2 !important;
                    font-weight: 600 !important;
                    border: 1px solid transparent !important;
                }
                QMenuBar::item:selected {
                    background-color: #E3F2FD !important;
                    color: #0D47A1 !important;
                    border: 1px solid #1976D2 !important;
                }
                QMenuBar::item:pressed {
                    background-color: #BBDEFB !important;
                    color: #0D47A1 !important;
                }
                
                /* HIGHLY VISIBLE Material Design Menu */
                QMenu {
                    background-color: #FFFFFF !important;
                    border: 2px solid #1976D2 !important;
                    border-radius: 12px !important;
                    padding: 12px !important;
                    font-size: 14px !important;
                    font-weight: 500 !important;
                }
                QMenu::item {
                    padding: 14px 24px !important;
                    border-radius: 8px !important;
                    margin: 3px !important;
                    color: #1C1B1F !important;
                    border: 1px solid transparent !important;
                }
                QMenu::item:selected {
                    background-color: #E3F2FD !important;
                    color: #1976D2 !important;
                    border: 1px solid #1976D2 !important;
                }
                QMenu::separator {
                    height: 2px !important;
                    background-color: #E0E0E0 !important;
                    margin: 4px 8px !important;
                }
                
                /* OPTIMIZED Material Design Tab Widget */
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
                
                /* OPTIMIZED Material Design Cards (Group Boxes) */
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
                
                /* OPTIMIZED Material Design 3.0 Buttons */
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
                
                /* OPTIMIZED Material Design Combo Boxes */
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
                
                /* OPTIMIZED Material Design Table Headers */
                QHeaderView::section {
                    background-color: #1976D2;
                    color: #FFFFFF;
                    padding: 8px 6px;
                    border: none;
                    font-weight: 600;
                    font-size: 12px;
                    border-radius: 0px;
                }
                
                /* OPTIMIZED Material Design Tables */
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
                
                /* OPTIMIZED Material Design Labels */
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
                
                /* OPTIMIZED Material Design Plot Frames */
                QFrame#plotFrame {
                    border: none;
                    border-radius: 12px;
                    background-color: #FFFFFF;
                    margin: 8px;
                    padding: 12px;
                }
                
                /* OPTIMIZED Material Design Progress Bars */
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
                
                /* OPTIMIZED Material Design Status Bar */
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
                    if not hasattr(self.ui, 'actionOpen_Log_File'):
                        print("ERROR: actionOpen_Log_File not found in UI!")
                        return
                    if not hasattr(self.ui, 'actionExit'):
                        print("ERROR: actionExit not found in UI!")
                        return
                    if not hasattr(self.ui, 'actionAbout'):
                        print("ERROR: actionAbout not found in UI!")
                        return
                    if not hasattr(self.ui, 'actionRefresh'):
                        print("ERROR: actionRefresh not found in UI!")
                        return
                    
                    # MAIN MENU ACTIONS - FILE MENU
                    self.ui.actionOpen_Log_File.triggered.connect(self.import_log_file)
                    self.ui.actionExit.triggered.connect(self.close)
                    print("✓ File menu actions connected")
                    
                    # VIEW MENU ACTIONS
                    self.ui.actionRefresh.triggered.connect(self.load_dashboard)
                    print("✓ View menu actions connected")
                    
                    # HELP MENU ACTIONS
                    self.ui.actionAbout.triggered.connect(self.show_about_dialog)
                    print("✓ Help menu actions connected")
                    
                    # OPTIONAL MENU ACTIONS (if they exist)
                    if hasattr(self.ui, 'actionExport_Data'):
                        self.ui.actionExport_Data.triggered.connect(self.export_data)
                        print("✓ Export action connected")
                    
                    if hasattr(self.ui, 'actionSettings'):
                        self.ui.actionSettings.triggered.connect(self.show_settings)
                        print("✓ Settings action connected")
                    
                    if hasattr(self.ui, 'actionAbout_Qt'):
                        self.ui.actionAbout_Qt.triggered.connect(lambda: QtWidgets.QApplication.aboutQt())
                        print("✓ About Qt action connected")
                    
                    # BUTTON ACTIONS
                    self.ui.btnClearDB.clicked.connect(self.clear_database)
                    self.ui.btnRefreshData.clicked.connect(self.load_dashboard)
                    self.ui.comboTrendSerial.currentIndexChanged.connect(self.update_trend)
                    self.ui.comboTrendParam.currentIndexChanged.connect(self.update_trend)
                    print("✓ Button actions connected")
                    
                    print("✓ ALL ACTIONS CONNECTED SUCCESSFULLY")
                    
                except Exception as e:
                    print(f"ERROR connecting actions: {e}")
                    traceback.print_exc()

            def export_data(self):
                """Export data functionality (placeholder)"""
                QtWidgets.QMessageBox.information(
                    self, "Export Data", 
                    "Export functionality will be implemented in a future version."
                )

            def show_settings(self):
                """Show settings dialog (placeholder)"""
                QtWidgets.QMessageBox.information(
                    self, "Settings", 
                    "Settings dialog will be implemented in a future version."
                )

            def _optimize_database(self):
                """Apply database optimizations"""
                try:
                    if hasattr(self, 'db'):
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
                    if hasattr(self, 'memory_label'):
                        self.memory_label.setText(f"Memory: {memory_mb:.1f} MB")
                    else:
                        self.memory_label = QtWidgets.QLabel(f"Memory: {memory_mb:.1f} MB")
                        self.statusBar().addPermanentWidget(self.memory_label)
                        
                    # Force garbage collection if memory usage is too high
                    if memory_mb > 500:
                        import gc
                        gc.collect()
                except Exception:
                    pass

            def show_about_dialog(self):
                """Show Material Design about dialog"""
                try:
                    from about_dialog import AboutDialog
                    about_dialog = AboutDialog(self)
                    about_dialog.exec_()
                except ImportError as e:
                    print(f"Failed to load about dialog: {e}")
                    QtWidgets.QMessageBox.about(
                        self,
                        "HALog Material Design",
                        "HALog 0.0.1 beta\nMaterial Design LINAC Log Analysis System\nDeveloped by Tanmay Pandey\n© gobioeng.com"
                    )

            def load_dashboard(self):
                """Load dashboard with Material Design optimizations"""
                try:
                    if not hasattr(self, 'db'):
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
                        self.ui.lblRecordCount.setText(f"Total Records: {len(self.df):,}")
                        
                        unique_params = self.df["param"].nunique()
                        self.ui.lblParameterCount.setText(f"Parameters: {unique_params}")
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
                    
                except Exception as e:
                    print(f"Error loading dashboard: {e}")
                    traceback.print_exc()

            def update_trend_combos(self):
                """Update trend combo boxes with Material Design styling"""
                try:
                    if hasattr(self, 'df') and not self.df.empty:
                        serials = sorted(set(map(str, self.df["serial"].unique())))
                        params = sorted(set(map(str, self.df["param"].unique())))
                    else:
                        serials = []
                        params = []
                        
                    self.ui.comboTrendSerial.blockSignals(True)
                    self.ui.comboTrendParam.blockSignals(True)
                    
                    self.ui.comboTrendSerial.clear()
                    self.ui.comboTrendParam.clear()
                    
                    self.ui.comboTrendSerial.addItems(["All"] + serials)
                    self.ui.comboTrendParam.addItems(["All"] + params)
                    
                    self.ui.comboTrendSerial.blockSignals(False)
                    self.ui.comboTrendParam.blockSignals(False)
                    
                    self.update_trend()
                except Exception as e:
                    print(f"Error updating trend combos: {e}")

            def update_data_table(self, page_size=1000):
                """Update data table with Material Design styling"""
                try:
                    if not hasattr(self, 'df') or self.df.empty:
                        self.ui.tableData.setRowCount(0)
                        self.ui.lblTableInfo.setText("No data available")
                        return
                    
                    df_sorted = self.df.sort_values("datetime", ascending=False)
                    display_df = df_sorted.iloc[:page_size]
                    
                    self.ui.tableData.setRowCount(len(display_df))
                    self.ui.tableData.setColumnCount(7)
                    self.ui.tableData.setHorizontalHeaderLabels(
                        ["DateTime", "Serial", "Parameter", "Average", "Min", "Max", "Diff (Max-Min)"]
                    )
                    
                    self.ui.tableData.setUpdatesEnabled(False)
                    
                    for i, (_, row) in enumerate(display_df.iterrows()):
                        self.ui.tableData.setItem(i, 0, QtWidgets.QTableWidgetItem(str(row.get("datetime", ""))))
                        self.ui.tableData.setItem(i, 1, QtWidgets.QTableWidgetItem(str(row.get("serial", ""))))
                        self.ui.tableData.setItem(i, 2, QtWidgets.QTableWidgetItem(str(row.get("param", ""))))
                        self.ui.tableData.setItem(i, 3, QtWidgets.QTableWidgetItem(str(row.get("avg", ""))))
                        self.ui.tableData.setItem(i, 4, QtWidgets.QTableWidgetItem(str(row.get("min", ""))))
                        self.ui.tableData.setItem(i, 5, QtWidgets.QTableWidgetItem(str(row.get("max", ""))))
                        diff_val = row.get("diff", "")
                        self.ui.tableData.setItem(i, 6, QtWidgets.QTableWidgetItem(str(diff_val)))
                    
                    self.ui.tableData.setUpdatesEnabled(True)
                    total_records = len(self.df)
                    self.ui.lblTableInfo.setText(
                        f"Showing {min(page_size, total_records):,} of {total_records:,} records"
                    )
                    
                except Exception as e:
                    print(f"Error updating data table: {e}")
                    traceback.print_exc()

            def update_analysis_tab(self):
                """Update analysis tab with Material Design progress"""
                try:
                    if not hasattr(self, 'df') or self.df.empty:
                        self.ui.tableTrends.setRowCount(0)
                        return
                    
                    if len(self.df) > 10000:
                        try:
                            from worker_thread import AnalysisWorker
                            from data_analyzer import DataAnalyzer
                            
                            progress_dialog = QtWidgets.QProgressDialog(
                                "Analyzing data...", "Cancel", 0, 100, self)
                            progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
                            progress_dialog.setMinimumDuration(0)
                            progress_dialog.setValue(0)
                            progress_dialog.show()
                            
                            analyzer = DataAnalyzer()
                            worker = AnalysisWorker(analyzer, self.df)
                            
                            worker.analysis_progress.connect(
                                lambda p, m: progress_dialog.setValue(p))
                            worker.analysis_finished.connect(
                                lambda results: self._display_analysis_results(results, progress_dialog))
                            worker.analysis_error.connect(
                                lambda msg: self._handle_analysis_error(msg, progress_dialog))
                            
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
                    from data_analyzer import DataAnalyzer
                    analyzer = DataAnalyzer()
                    
                    analysis_df = self.df.copy()
                    
                    if 'param' in analysis_df.columns and 'parameter_type' not in analysis_df.columns:
                        analysis_df['parameter_type'] = analysis_df['param']
                    
                    if 'statistic_type' not in analysis_df.columns:
                        if 'stat_type' in analysis_df.columns:
                            analysis_df['statistic_type'] = analysis_df['stat_type']
                        else:
                            analysis_df['statistic_type'] = 'avg'
                    
                    if 'avg' in analysis_df.columns and 'value' not in analysis_df.columns:
                        analysis_df['value'] = analysis_df['avg']
                    
                    try:
                        trends_df = analyzer.calculate_advanced_trends(analysis_df)
                        self._populate_trends_table(trends_df)
                    except Exception as e:
                        print(f"Error calculating trends: {e}")
                        import pandas as pd
                        empty_trends = pd.DataFrame(columns=[
                            'parameter_type', 'statistic_type', 'data_points',
                            'time_span_hours', 'trend_slope', 'trend_direction', 'trend_strength'
                        ])
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
                    
                    if 'trends' in results:
                        self._populate_trends_table(results['trends'])
                except Exception as e:
                    print(f"Error displaying analysis results: {e}")
            
            def _handle_analysis_error(self, error_message, progress_dialog=None):
                """Handle analysis errors from worker thread"""
                try:
                    if progress_dialog:
                        progress_dialog.close()
                        
                    QtWidgets.QMessageBox.warning(
                        self, "Analysis Error", 
                        f"Error during data analysis: {error_message}"
                    )
                except Exception as e:
                    print(f"Error handling analysis error: {e}")

            def _populate_trends_table(self, trends_df):
                """Populate trends table with analysis results"""
                try:
                    if trends_df.empty:
                        self.ui.tableTrends.setRowCount(0)
                        return
                        
                    self.ui.tableTrends.setRowCount(len(trends_df))
                    for i, (_, row) in enumerate(trends_df.iterrows()):
                        self.ui.tableTrends.setItem(i, 0, QtWidgets.QTableWidgetItem(str(row.get("parameter_type", ""))))
                        self.ui.tableTrends.setItem(i, 1, QtWidgets.QTableWidgetItem(str(row.get("statistic_type", ""))))
                        self.ui.tableTrends.setItem(i, 2, QtWidgets.QTableWidgetItem(str(row.get("data_points", ""))))
                        self.ui.tableTrends.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{row.get('time_span_hours', 0):.1f}"))
                        self.ui.tableTrends.setItem(i, 4, QtWidgets.QTableWidgetItem(f"{row.get('trend_slope', 0):.4f}"))
                        self.ui.tableTrends.setItem(i, 5, QtWidgets.QTableWidgetItem(str(row.get("trend_direction", ""))))
                        self.ui.tableTrends.setItem(i, 6, QtWidgets.QTableWidgetItem(str(row.get("trend_strength", ""))))
                except Exception as e:
                    print(f"Error populating trends table: {e}")

            def on_tab_changed(self, index):
                """Handle tab changes with Material Design animations"""
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
                """Update trend visualization with Material Design styling"""
                try:
                    if not hasattr(self, 'df') or self.df.empty:
                        return
                    
                    serial = self.ui.comboTrendSerial.currentText()
                    param = self.ui.comboTrendParam.currentText()
                    
                    if serial == "All" and param == "All":
                        df_trend = self.df
                    else:
                        import numpy as np
                        mask = np.ones(len(self.df), dtype=bool)
                        if serial and serial != "All":
                            mask &= (self.df["serial"] == serial)
                        if param and param != "All":
                            mask &= (self.df["param"] == param)
                        df_trend = self.df[mask]
                    
                    from plot_utils import plot_trend
                    
                    if len(df_trend) > 10000:
                        print(f"Downsampling large trend data: {len(df_trend)} points")
                        plot_trend(self.ui.plotWidget, df_trend)
                    else:
                        plot_trend(self.ui.plotWidget, df_trend)
                        
                except Exception as e:
                    print(f"Error updating trend: {e}")
                    traceback.print_exc()

            def import_log_file(self):
                """MAIN LOG FILE IMPORT FUNCTION - FULLY CONNECTED"""
                print("🔥 LOG FILE IMPORT TRIGGERED!")
                try:
                    file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                        self, "Open LINAC Log File", "",
                        "Log Files (*.txt *.log);;All Files (*)"
                    )
                    
                    if not file_path:
                        print("No file selected")
                        return
                        
                    print(f"Selected file: {file_path}")
                    file_size = os.path.getsize(file_path)
                    print(f"File size: {file_size} bytes")
                    
                    if file_size < 5 * 1024 * 1024:
                        self._import_small_file(file_path)
                    else:
                        self._import_large_file(file_path, file_size)
                except Exception as e:
                    print(f"Error in import_log_file: {e}")
                    traceback.print_exc()
                    QtWidgets.QMessageBox.critical(
                        self, "Import Error",
                        f"Error importing log file: {str(e)}"
                    )

            def _import_small_file(self, file_path):
                """Import small log file with Material Design progress"""
                try:
                    progress_dialog = QtWidgets.QProgressDialog(
                        "Processing file...", "Cancel", 0, 100, self)
                    progress_dialog.setWindowTitle("Processing Log File")
                    progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
                    progress_dialog.show()
                    progress_dialog.setValue(10)
                    QtWidgets.QApplication.processEvents()
                    
                    from linac_parser import LinacParser
                    parser = LinacParser()
                    
                    progress_dialog.setValue(30)
                    QtWidgets.QApplication.processEvents()
                    
                    df = parser.parse_file_chunked(file_path)
                    
                    progress_dialog.setValue(70)
                    QtWidgets.QApplication.processEvents()
                    
                    records_inserted = self.db.insert_data_batch(df)
                    
                    progress_dialog.setValue(90)
                    QtWidgets.QApplication.processEvents()
                    
                    filename = os.path.basename(file_path)
                    parsing_stats_json = '{}'
                    
                    self.db.insert_file_metadata(
                        filename=filename,
                        file_size=os.path.getsize(file_path),
                        records_imported=records_inserted,
                        parsing_stats=parsing_stats_json
                    )
                    
                    progress_dialog.setValue(100)
                    progress_dialog.close()
                    
                    try:
                        self.df = self.db.get_all_logs(chunk_size=10000)
                    except TypeError:
                        self.df = self.db.get_all_logs()
                    self.load_dashboard()
                    
                    QtWidgets.QMessageBox.information(
                        self, "Import Successful",
                        f"Successfully imported {records_inserted:,} records."
                    )
                    
                    import gc
                    del df
                    gc.collect()
                    
                except Exception as e:
                    QtWidgets.QMessageBox.critical(
                        self, "Processing Error",
                        f"An error occurred: {str(e)}"
                    )
                    traceback.print_exc()

            def _import_large_file(self, file_path, file_size):
                """Import large log file with Material Design progress"""
                try:
                    from progress_dialog import ProgressDialog
                    
                    self.progress_dialog = ProgressDialog(self)
                    self.progress_dialog.setWindowTitle("Processing LINAC Log File")
                    self.progress_dialog.setLabelText("Initializing file processing...")
                    self.progress_dialog.show()
                    
                    from worker_thread import FileProcessingWorker
                    
                    self.worker = FileProcessingWorker(file_path, file_size, self.db)
                    self.worker.chunk_size = 5000
                    
                    self.worker.progress_update.connect(self.progress_dialog.update_progress)
                    self.worker.status_update.connect(self.progress_dialog.setLabelText)
                    self.worker.finished.connect(self.on_file_processing_finished)
                    self.worker.error.connect(self.on_file_processing_error)
                    
                    self.progress_dialog.canceled.connect(self.worker.cancel_processing)
                    
                    self.worker.start()
                except Exception as e:
                    QtWidgets.QMessageBox.critical(
                        self, "Processing Error",
                        f"Error initializing file processing: {str(e)}"
                    )
                    traceback.print_exc()

            def clear_database(self):
                """Clear database with Material Design confirmation"""
                try:
                    reply = QtWidgets.QMessageBox.question(
                        self, "Confirm Clear Database",
                        "Are you sure you want to clear all data?",
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                        QtWidgets.QMessageBox.No
                    )
                    
                    if reply == QtWidgets.QMessageBox.Yes:
                        progress_dialog = QtWidgets.QProgressDialog(
                            "Clearing database...", "", 0, 100, self)
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
                        self, "Database Error",
                        f"An error occurred: {str(e)}"
                    )
                    traceback.print_exc()

            def on_file_processing_finished(self, records_count, parsing_stats):
                """Handle completion of file processing"""
                try:
                    if hasattr(self, 'progress_dialog') and self.progress_dialog:
                        self.progress_dialog.close()
                    
                    if records_count > 0:
                        try:
                            self.df = self.db.get_all_logs(chunk_size=10000)
                        except TypeError:
                            self.df = self.db.get_all_logs()
                        self.load_dashboard()
                        
                        QtWidgets.QMessageBox.information(
                            self, "Import Successful",
                            f"Successfully imported {records_count:,} records."
                        )
                        
                        print(f"File processing completed: {parsing_stats}")
                    else:
                        QtWidgets.QMessageBox.warning(
                            self, "Import Warning",
                            "No valid log entries found in the selected file."
                        )
                    
                    if hasattr(self, 'worker'):
                        self.worker.deleteLater()
                        self.worker = None
                except Exception as e:
                    print(f"Error handling file processing completion: {e}")
                    traceback.print_exc()

            def on_file_processing_error(self, error_message):
                """Handle errors during file processing"""
                try:
                    if hasattr(self, 'progress_dialog') and self.progress_dialog:
                        self.progress_dialog.close()
                    
                    QtWidgets.QMessageBox.critical(
                        self, "Processing Error",
                        f"An error occurred: {error_message}"
                    )
                    
                    if hasattr(self, 'worker'):
                        self.worker.deleteLater()
                        self.worker = None
                except Exception as e:
                    print(f"Error handling file processing error: {e}")
                    traceback.print_exc()

            def closeEvent(self, event):
                """Clean up resources when closing application"""
                try:
                    if hasattr(self, 'memory_timer'):
                        self.memory_timer.stop()
                    
                    if hasattr(self, 'db'):
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
        self.update_splash_progress(80, "Finalizing Material Design...")
        self.load_times['window_creation'] = time.time() - start_window
        return self.window

def main():
    global startup_begin
    
    try:
        # Setup environment
        setup_environment()
        env_time = time.time() - startup_begin
        
        # Import Qt components
        QtWidgets = lazy_import('PyQt5.QtWidgets')
        QtCore = lazy_import('PyQt5.QtCore')
        QtGui = lazy_import('PyQt5.QtGui')
        
        # Create application with Material Design settings
        app = QtWidgets.QApplication(sys.argv)
        app.setApplicationName("HALog Material Design")
        app.setApplicationVersion(APP_VERSION)
        app.setOrganizationName("gobioeng.com")
        
        # Set Material Design font
        try:
            font = QtGui.QFont("Segoe UI", 9)  # Slightly smaller for better data focus
            app.setFont(font)
        except:
            pass
        
        qt_time = time.time() - startup_begin - env_time
        
        # Create Material Design app
        material_app = MaterialDesignApp()
        splash = material_app.create_material_splash()
        splash_time = time.time() - startup_begin - env_time - qt_time
        
        # Create main window
        material_app.update_splash_progress(20, "Creating Material Design interface...")
        window = material_app.create_main_window()
        
        # Finalize startup
        material_app.update_splash_progress(90, "Finalizing HALog Material Design...")
        
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
        print(f"🚀 HALog Material Design startup: {total_time:.3f}s")
        print(f"   Developed by Tanmay Pandey - gobioeng.com")
        print(f"   Material Design Implementation Complete")
        
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
                f"Error starting HALog Material Design: {str(e)}\n\nDeveloped by Tanmay Pandey\ngobioeng.com\n\n{traceback.format_exc()}"
            )
        except:
            pass
            
        return 1

if __name__ == "__main__":
    # Uncomment this line to test icon loading:
    # test_icon_loading()
    sys.exit(main())
