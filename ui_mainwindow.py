from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget, 
    QTableWidget, QComboBox, QAction, QMenuBar, QFrame, QGroupBox, QGridLayout, 
    QHeaderView, QAbstractItemView, QSizePolicy, QMenu
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Gobioeng HALog 0.0.1 beta")
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(800, 600)
        
        # CRITICAL: Setup menu bar FIRST before anything else
        self.setup_menu_bar(MainWindow)
        
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.setSpacing(16)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        
        # Setup main content
        self.setup_main_content()

    def setup_menu_bar(self, MainWindow):
        """Setup the complete menu bar with all menus and actions - PRIORITY FIX"""
        print("Setting up menu bar...")
        
        # Create menu bar and set it to MainWindow immediately
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        
        # CRITICAL: Set the menu bar to MainWindow
        MainWindow.setMenuBar(self.menubar)
        
        # Make menu bar visible with styling
        self.menubar.setStyleSheet("""
            QMenuBar {
                background-color: #FFFFFF;
                color: #1976D2;
                border: none;
                border-bottom: 2px solid #1976D2;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                height: 40px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 12px 20px;
                margin: 0px 4px;
                border-radius: 6px;
                color: #1976D2;
                font-weight: bold;
            }
            QMenuBar::item:selected {
                background-color: #E3F2FD;
                color: #0D47A1;
            }
            QMenuBar::item:pressed {
                background-color: #BBDEFB;
            }
        """)
        
        # File Menu
        self.menuFile = self.menubar.addMenu('&File')
        self.menuFile.setObjectName("menuFile")
        
        # File Menu Actions
        self.actionOpen_Log_File = QAction(MainWindow)
        self.actionOpen_Log_File.setObjectName("actionOpen_Log_File")
        self.actionOpen_Log_File.setText('&Open Log File...')
        self.actionOpen_Log_File.setShortcut(QKeySequence('Ctrl+O'))
        self.actionOpen_Log_File.setStatusTip('Open a LINAC log file for analysis')
        self.menuFile.addAction(self.actionOpen_Log_File)
        
        # Add separator
        self.menuFile.addSeparator()
        
        # Export Action
        self.actionExport_Data = QAction(MainWindow)
        self.actionExport_Data.setObjectName("actionExport_Data")
        self.actionExport_Data.setText('&Export Data...')
        self.actionExport_Data.setShortcut(QKeySequence('Ctrl+E'))
        self.actionExport_Data.setStatusTip('Export analysis results')
        self.menuFile.addAction(self.actionExport_Data)
        
        # Add separator
        self.menuFile.addSeparator()
        
        # Exit Action
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.setText('E&xit')
        self.actionExit.setShortcut(QKeySequence('Ctrl+Q'))
        self.actionExit.setStatusTip('Exit the application')
        self.menuFile.addAction(self.actionExit)
        
        # View Menu
        self.menuView = self.menubar.addMenu('&View')
        self.menuView.setObjectName("menuView")
        
        # View Menu Actions
        self.actionRefresh = QAction(MainWindow)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionRefresh.setText('&Refresh')
        self.actionRefresh.setShortcut(QKeySequence('F5'))
        self.actionRefresh.setStatusTip('Refresh all data')
        self.menuView.addAction(self.actionRefresh)
        
        # Help Menu
        self.menuHelp = self.menubar.addMenu('&Help')
        self.menuHelp.setObjectName("menuHelp")
        
        # Help Menu Actions
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setText('&About HALog...')
        self.actionAbout.setStatusTip('About this application')
        self.menuHelp.addAction(self.actionAbout)
        
        # About Qt
        self.actionAbout_Qt = QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionAbout_Qt.setText('About &Qt...')
        self.actionAbout_Qt.setStatusTip('About Qt framework')
        self.menuHelp.addAction(self.actionAbout_Qt)
        
        print(f"✓ Menu bar created with {self.menubar.actions()} actions")

    def setup_main_content(self):
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tabWidget.setStyleSheet("""
            QTabBar::tab {
                min-width: 120px;
                padding: 12px 20px;
                font-size: 13px;
                word-wrap: break-word;
                text-align: center;
            }
            QTabBar::tab:selected {
                font-weight: bold;
            }
        """)
        self.main_layout.addWidget(self.tabWidget)
        self.setup_dashboard_tab()
        self.setup_trends_tab()
        self.setup_data_table_tab()
        self.setup_analysis_tab()
        self.setup_about_tab()

    def setup_dashboard_tab(self):
        self.tabDashboard = QWidget()
        self.tabWidget.addTab(self.tabDashboard, "📊 Dashboard")
        layout = QVBoxLayout(self.tabDashboard)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header_label = QLabel("<h2>LINAC Water System Monitor</h2>")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setWordWrap(True)
        header_label.setStyleSheet("color: #2c3e50; margin: 10px; font-size:20px;")
        layout.addWidget(header_label)
        
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)
        
        status_group = QGroupBox("System Status")
        status_layout = QGridLayout(status_group)
        status_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.lblSerial = QLabel("Serial: -")
        self.lblSerial.setWordWrap(True)
        self.lblDate = QLabel("Date: -")
        self.lblDate.setWordWrap(True)
        self.lblDuration = QLabel("Duration: -")
        self.lblDuration.setWordWrap(True)
        
        status_layout.addWidget(self.lblSerial, 0, 0)
        status_layout.addWidget(self.lblDate, 1, 0)
        status_layout.addWidget(self.lblDuration, 2, 0)
        cards_layout.addWidget(status_group)
        
        data_group = QGroupBox("Data Summary")
        data_layout = QGridLayout(data_group)
        data_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.lblRecordCount = QLabel("Total Records: 0")
        self.lblRecordCount.setWordWrap(True)
        self.lblParameterCount = QLabel("Parameters: 0")
        self.lblParameterCount.setWordWrap(True)
        
        data_layout.addWidget(self.lblRecordCount, 0, 0)
        data_layout.addWidget(self.lblParameterCount, 1, 0)
        cards_layout.addWidget(data_group)
        cards_layout.addStretch()
        
        layout.addLayout(cards_layout)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.btnClearDB = QPushButton("Clear All Data")
        self.btnClearDB.setObjectName("dangerButton")
        self.btnClearDB.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        self.btnRefreshData = QPushButton("Refresh Data")
        self.btnRefreshData.setObjectName("successButton")
        self.btnRefreshData.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        button_layout.addWidget(self.btnClearDB)
        button_layout.addWidget(self.btnRefreshData)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()

    def setup_trends_tab(self):
        self.tabTrends = QWidget()
        self.tabWidget.addTab(self.tabTrends, "📈 Trends")
        layout = QVBoxLayout(self.tabTrends)
        layout.setContentsMargins(20, 20, 20, 20)
        
        controls_group = QGroupBox("Trend Analysis Controls")
        controls_layout = QHBoxLayout(controls_group)
        controls_layout.setSpacing(12)
        controls_layout.setContentsMargins(12, 12, 12, 12)
        
        serial_label = QLabel("Serial Number:")
        serial_label.setWordWrap(True)
        controls_layout.addWidget(serial_label)
        
        self.comboTrendSerial = QComboBox()
        self.comboTrendSerial.setMinimumWidth(120)
        self.comboTrendSerial.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        controls_layout.addWidget(self.comboTrendSerial)
        
        param_label = QLabel("Parameter:")
        param_label.setWordWrap(True)
        controls_layout.addWidget(param_label)
        
        self.comboTrendParam = QComboBox()
        self.comboTrendParam.setMinimumWidth(160)
        self.comboTrendParam.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        controls_layout.addWidget(self.comboTrendParam)
        controls_layout.addStretch()
        
        layout.addWidget(controls_group)
        
        self.plotWidget = QFrame()
        self.plotWidget.setFrameStyle(QFrame.Box)
        self.plotWidget.setObjectName("plotFrame")
        self.plotWidget.setMinimumHeight(400)
        self.plotWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.plotWidget)

    def setup_data_table_tab(self):
        self.tabDataTable = QWidget()
        self.tabWidget.addTab(self.tabDataTable, "📋 Data Table")
        layout = QVBoxLayout(self.tabDataTable)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.lblTableInfo = QLabel("No data available")
        self.lblTableInfo.setWordWrap(True)
        layout.addWidget(self.lblTableInfo)
        
        self.tableData = QTableWidget()
        self.tableData.setColumnCount(7)
        self.tableData.setHorizontalHeaderLabels([
            "DateTime", "Serial", "Parameter", "Average", "Min", "Max", "Diff (Max-Min)"
        ])
        self.tableData.setAlternatingRowColors(True)
        self.tableData.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableData.horizontalHeader().setStretchLastSection(True)
        self.tableData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableData.verticalHeader().setVisible(False)
        self.tableData.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tableData.setWordWrap(True)
        layout.addWidget(self.tableData)

    def setup_analysis_tab(self):
        self.tabAnalysis = QWidget()
        self.tabWidget.addTab(self.tabAnalysis, "🔬 Analysis")
        layout = QVBoxLayout(self.tabAnalysis)
        layout.setContentsMargins(20, 20, 20, 20)

        # Only Parameter Trend Analysis Group
        trends_group = QGroupBox("Parameter Trend Analysis")
        trends_layout = QVBoxLayout(trends_group)
        
        self.tableTrends = QTableWidget()
        self.tableTrends.setAlternatingRowColors(True)
        self.tableTrends.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tableTrends.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableTrends.setColumnCount(7)
        self.tableTrends.setHorizontalHeaderLabels([
            "Parameter",
            "Statistic",
            "Data Points",
            "Time Span (hrs)",
            "Slope",
            "Direction",
            "Strength"
        ])
        trends_layout.addWidget(self.tableTrends)
        layout.addWidget(trends_group)

    def setup_about_tab(self):
        self.tabAbout = QWidget()
        self.tabWidget.addTab(self.tabAbout, "ℹ️ About")
        layout = QVBoxLayout(self.tabAbout)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        
        logo_label = QLabel("🏥")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("font-size: 48px; margin: 20px;")
        layout.addWidget(logo_label)
        
        app_info = QLabel(
            "<h2>Gobioeng HALog 0.0.1 beta</h2>"
            "<p>A professional LINAC water system monitoring application</p>"
            "<p>Developed by <b>Tanmay Pandey</b></p>"
            "<p><a href='https://gobioeng.com'>gobioeng.com</a></p>"
            "<p>© 2025 Gobioeng. All rights reserved.</p>"
        )
        app_info.setAlignment(Qt.AlignCenter)
        app_info.setOpenExternalLinks(True)
        app_info.setWordWrap(True)
        layout.addWidget(app_info)
        layout.addStretch()
