from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QComboBox,
    QAction,
    QMenuBar,
    QFrame,
    QGroupBox,
    QGridLayout,
    QHeaderView,
    QAbstractItemView,
    QSizePolicy,
    QMenu,
    QLineEdit,
    QTextEdit,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Gobioeng HALog 0.0.1 beta")
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(800, 600)

        # Setup menu bar FIRST before anything else
        self.setup_menu_bar(MainWindow)

        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.setSpacing(16)
        self.main_layout.setContentsMargins(16, 16, 16, 16)

        self.setup_main_content()

    def setup_menu_bar(self, MainWindow):
        """Setup the menu bar with all menus and actions"""
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        # File Menu
        self.menuFile = self.menubar.addMenu("&File")
        self.actionOpen_Log_File = QAction(MainWindow)
        self.actionOpen_Log_File.setObjectName("actionOpen_Log_File")
        self.actionOpen_Log_File.setText("&Open Log File...")
        self.actionOpen_Log_File.setShortcut(QKeySequence("Ctrl+O"))
        self.actionOpen_Log_File.setStatusTip("Open a LINAC log file for analysis")
        self.menuFile.addAction(self.actionOpen_Log_File)
        self.menuFile.addSeparator()
        self.actionExport_Data = QAction(MainWindow)
        self.actionExport_Data.setObjectName("actionExport_Data")
        self.actionExport_Data.setText("&Export Data...")
        self.actionExport_Data.setShortcut(QKeySequence("Ctrl+E"))
        self.actionExport_Data.setStatusTip("Export analysis results")
        self.menuFile.addAction(self.actionExport_Data)
        self.menuFile.addSeparator()
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.setText("E&xit")
        self.actionExit.setShortcut(QKeySequence("Ctrl+Q"))
        self.actionExit.setStatusTip("Exit the application")
        self.menuFile.addAction(self.actionExit)

        # View Menu
        self.menuView = self.menubar.addMenu("&View")
        self.actionRefresh = QAction(MainWindow)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionRefresh.setText("&Refresh")
        self.actionRefresh.setShortcut(QKeySequence("F5"))
        self.actionRefresh.setStatusTip("Refresh all data")
        self.menuView.addAction(self.actionRefresh)

        # Help Menu
        self.menuHelp = self.menubar.addMenu("&Help")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setText("&About HALog...")
        self.actionAbout.setStatusTip("About this application")
        self.menuHelp.addAction(self.actionAbout)
        self.actionAbout_Qt = QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionAbout_Qt.setText("About &Qt...")
        self.actionAbout_Qt.setStatusTip("About Qt framework")
        self.menuHelp.addAction(self.actionAbout_Qt)

    def setup_main_content(self):
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.tabWidget)
        self.setup_dashboard_tab()
        self.setup_trends_tab()
        self.setup_data_table_tab()
        self.setup_analysis_tab()
        self.setup_mpc_tab()  # NEW MPC TAB
        self.setup_fault_code_tab()
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

        # Create sub-tabs for different parameter groups
        self.trendSubTabs = QTabWidget()
        self.trendSubTabs.setTabPosition(QTabWidget.North)
        layout.addWidget(self.trendSubTabs)

        # Water System tab
        self.setup_water_system_tab()
        
        # Voltages tab
        self.setup_voltages_tab()
        
        # Temperatures tab  
        self.setup_temperatures_tab()
        
        # Humidity tab
        self.setup_humidity_tab()
        
        # Fan Speeds tab (NEW)
        self.setup_fan_speeds_tab()

    def setup_water_system_tab(self):
        self.tabWaterSystem = QWidget()
        self.trendSubTabs.addTab(self.tabWaterSystem, "🌊 Water System")
        layout = QVBoxLayout(self.tabWaterSystem)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Controls
        controls_group = QGroupBox("Water System Controls")
        controls_layout = QHBoxLayout(controls_group)
        controls_layout.setSpacing(12)
        
        self.comboWaterSerial = QComboBox()
        self.comboWaterSerial.setMinimumWidth(120)
        controls_layout.addWidget(QLabel("Serial:"))
        controls_layout.addWidget(self.comboWaterSerial)
        
        self.comboWaterParam = QComboBox()
        self.comboWaterParam.setMinimumWidth(160)
        controls_layout.addWidget(QLabel("Parameter:"))
        controls_layout.addWidget(self.comboWaterParam)
        
        self.btnRefreshWater = QPushButton("Refresh")
        self.btnRefreshWater.setObjectName("primaryButton")
        controls_layout.addWidget(self.btnRefreshWater)
        controls_layout.addStretch()
        
        layout.addWidget(controls_group)
        
        # Two graphs layout (top and bottom)
        graphs_widget = QWidget()
        graphs_layout = QVBoxLayout(graphs_widget)
        graphs_layout.setSpacing(12)
        
        self.waterGraphTop = QFrame()
        self.waterGraphTop.setFrameStyle(QFrame.Box)
        self.waterGraphTop.setObjectName("plotFrame")
        self.waterGraphTop.setMinimumHeight(200)
        self.waterGraphTop.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        graphs_layout.addWidget(self.waterGraphTop)
        
        self.waterGraphBottom = QFrame()
        self.waterGraphBottom.setFrameStyle(QFrame.Box)
        self.waterGraphBottom.setObjectName("plotFrame")
        self.waterGraphBottom.setMinimumHeight(200)
        self.waterGraphBottom.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        graphs_layout.addWidget(self.waterGraphBottom)
        
        layout.addWidget(graphs_widget)

    def setup_voltages_tab(self):
        self.tabVoltages = QWidget()
        self.trendSubTabs.addTab(self.tabVoltages, "⚡ Voltages")
        layout = QVBoxLayout(self.tabVoltages)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Controls
        controls_group = QGroupBox("Voltage Controls")
        controls_layout = QHBoxLayout(controls_group)
        controls_layout.setSpacing(12)
        
        self.comboVoltageSerial = QComboBox()
        self.comboVoltageSerial.setMinimumWidth(120)
        controls_layout.addWidget(QLabel("Serial:"))
        controls_layout.addWidget(self.comboVoltageSerial)
        
        self.comboVoltageParam = QComboBox()
        self.comboVoltageParam.setMinimumWidth(160)
        controls_layout.addWidget(QLabel("Parameter:"))
        controls_layout.addWidget(self.comboVoltageParam)
        
        self.btnRefreshVoltage = QPushButton("Refresh")
        self.btnRefreshVoltage.setObjectName("primaryButton")
        controls_layout.addWidget(self.btnRefreshVoltage)
        controls_layout.addStretch()
        
        layout.addWidget(controls_group)
        
        # Two graphs layout (top and bottom)
        graphs_widget = QWidget()
        graphs_layout = QVBoxLayout(graphs_widget)
        graphs_layout.setSpacing(12)
        
        self.voltageGraphTop = QFrame()
        self.voltageGraphTop.setFrameStyle(QFrame.Box)
        self.voltageGraphTop.setObjectName("plotFrame")
        self.voltageGraphTop.setMinimumHeight(200)
        self.voltageGraphTop.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        graphs_layout.addWidget(self.voltageGraphTop)
        
        self.voltageGraphBottom = QFrame()
        self.voltageGraphBottom.setFrameStyle(QFrame.Box)
        self.voltageGraphBottom.setObjectName("plotFrame")
        self.voltageGraphBottom.setMinimumHeight(200)
        self.voltageGraphBottom.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        graphs_layout.addWidget(self.voltageGraphBottom)
        
        layout.addWidget(graphs_widget)

    def setup_temperatures_tab(self):
        self.tabTemperatures = QWidget()
        self.trendSubTabs.addTab(self.tabTemperatures, "🌡️ Temperatures")
        layout = QVBoxLayout(self.tabTemperatures)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Controls
        controls_group = QGroupBox("Temperature Controls")
        controls_layout = QHBoxLayout(controls_group)
        controls_layout.setSpacing(12)
        
        self.comboTempSerial = QComboBox()
        self.comboTempSerial.setMinimumWidth(120)
        controls_layout.addWidget(QLabel("Serial:"))
        controls_layout.addWidget(self.comboTempSerial)
        
        self.comboTempParam = QComboBox()
        self.comboTempParam.setMinimumWidth(160)
        controls_layout.addWidget(QLabel("Parameter:"))
        controls_layout.addWidget(self.comboTempParam)
        
        self.btnRefreshTemp = QPushButton("Refresh")
        self.btnRefreshTemp.setObjectName("primaryButton")
        controls_layout.addWidget(self.btnRefreshTemp)
        controls_layout.addStretch()
        
        layout.addWidget(controls_group)
        
        # Two graphs layout (top and bottom)
        graphs_widget = QWidget()
        graphs_layout = QVBoxLayout(graphs_widget)
        graphs_layout.setSpacing(12)
        
        self.tempGraphTop = QFrame()
        self.tempGraphTop.setFrameStyle(QFrame.Box)
        self.tempGraphTop.setObjectName("plotFrame")
        self.tempGraphTop.setMinimumHeight(200)
        self.tempGraphTop.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        graphs_layout.addWidget(self.tempGraphTop)
        
        self.tempGraphBottom = QFrame()
        self.tempGraphBottom.setFrameStyle(QFrame.Box)
        self.tempGraphBottom.setObjectName("plotFrame")
        self.tempGraphBottom.setMinimumHeight(200)
        self.tempGraphBottom.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        graphs_layout.addWidget(self.tempGraphBottom)
        
        layout.addWidget(graphs_widget)

    def setup_humidity_tab(self):
        self.tabHumidity = QWidget()
        self.trendSubTabs.addTab(self.tabHumidity, "💧 Humidity")
        layout = QVBoxLayout(self.tabHumidity)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Controls
        controls_group = QGroupBox("Humidity Controls")
        controls_layout = QHBoxLayout(controls_group)
        controls_layout.setSpacing(12)
        
        self.comboHumiditySerial = QComboBox()
        self.comboHumiditySerial.setMinimumWidth(120)
        controls_layout.addWidget(QLabel("Serial:"))
        controls_layout.addWidget(self.comboHumiditySerial)
        
        self.comboHumidityParam = QComboBox()
        self.comboHumidityParam.setMinimumWidth(160)
        controls_layout.addWidget(QLabel("Parameter:"))
        controls_layout.addWidget(self.comboHumidityParam)
        
        self.btnRefreshHumidity = QPushButton("Refresh")
        self.btnRefreshHumidity.setObjectName("primaryButton")
        controls_layout.addWidget(self.btnRefreshHumidity)
        controls_layout.addStretch()
        
        layout.addWidget(controls_group)
        
        # Two graphs layout (top and bottom)
        graphs_widget = QWidget()
        graphs_layout = QVBoxLayout(graphs_widget)
        graphs_layout.setSpacing(12)
        
        self.humidityGraphTop = QFrame()
        self.humidityGraphTop.setFrameStyle(QFrame.Box)
        self.humidityGraphTop.setObjectName("plotFrame")
        self.humidityGraphTop.setMinimumHeight(200)
        self.humidityGraphTop.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        graphs_layout.addWidget(self.humidityGraphTop)
        
        self.humidityGraphBottom = QFrame()
        self.humidityGraphBottom.setFrameStyle(QFrame.Box)
        self.humidityGraphBottom.setObjectName("plotFrame")
        self.humidityGraphBottom.setMinimumHeight(200)
        self.humidityGraphBottom.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        graphs_layout.addWidget(self.humidityGraphBottom)
        
        layout.addWidget(graphs_widget)

    def setup_fan_speeds_tab(self):
        self.tabFanSpeeds = QWidget()
        self.trendSubTabs.addTab(self.tabFanSpeeds, "🌀 Fan Speeds")
        layout = QVBoxLayout(self.tabFanSpeeds)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Controls
        controls_group = QGroupBox("Fan Speed Controls")
        controls_layout = QHBoxLayout(controls_group)
        controls_layout.setSpacing(12)
        
        self.comboFanSerial = QComboBox()
        self.comboFanSerial.setMinimumWidth(120)
        controls_layout.addWidget(QLabel("Serial:"))
        controls_layout.addWidget(self.comboFanSerial)
        
        self.comboFanParam = QComboBox()
        self.comboFanParam.setMinimumWidth(160)
        controls_layout.addWidget(QLabel("Parameter:"))
        controls_layout.addWidget(self.comboFanParam)
        
        self.btnRefreshFan = QPushButton("Refresh")
        self.btnRefreshFan.setObjectName("primaryButton")
        controls_layout.addWidget(self.btnRefreshFan)
        controls_layout.addStretch()
        
        layout.addWidget(controls_group)
        
        # Two graphs layout (top and bottom)
        graphs_widget = QWidget()
        graphs_layout = QVBoxLayout(graphs_widget)
        graphs_layout.setSpacing(12)
        
        self.fanGraphTop = QFrame()
        self.fanGraphTop.setFrameStyle(QFrame.Box)
        self.fanGraphTop.setObjectName("plotFrame")
        self.fanGraphTop.setMinimumHeight(200)
        self.fanGraphTop.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        graphs_layout.addWidget(self.fanGraphTop)
        
        self.fanGraphBottom = QFrame()
        self.fanGraphBottom.setFrameStyle(QFrame.Box)
        self.fanGraphBottom.setObjectName("plotFrame")
        self.fanGraphBottom.setMinimumHeight(200)
        self.fanGraphBottom.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        graphs_layout.addWidget(self.fanGraphBottom)
        
        layout.addWidget(graphs_widget)

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
        self.tableData.setHorizontalHeaderLabels(
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

        trends_group = QGroupBox("Parameter Trend Analysis")
        trends_layout = QVBoxLayout(trends_group)

        self.tableTrends = QTableWidget()
        self.tableTrends.setAlternatingRowColors(True)
        self.tableTrends.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tableTrends.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableTrends.setColumnCount(7)
        self.tableTrends.setHorizontalHeaderLabels(
            [
                "Parameter",
                "Statistic",
                "Data Points",
                "Time Span (hrs)",
                "Slope",
                "Direction",
                "Strength",
            ]
        )
        trends_layout.addWidget(self.tableTrends)
        layout.addWidget(trends_group)

    def setup_mpc_tab(self):
        self.tabMPC = QWidget()
        self.tabWidget.addTab(self.tabMPC, "🔧 MPC")
        layout = QVBoxLayout(self.tabMPC)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        header_label = QLabel("<h2>Machine Performance Check Results</h2>")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setWordWrap(True)
        layout.addWidget(header_label)

        # Date selection controls
        date_group = QGroupBox("Date Selection")
        date_layout = QHBoxLayout(date_group)
        date_layout.setSpacing(12)
        date_layout.setContentsMargins(16, 16, 16, 16)
        
        # Date A selection
        date_layout.addWidget(QLabel("Date A:"))
        self.comboDateA = QComboBox()
        self.comboDateA.setMinimumWidth(150)
        self.comboDateA.setPlaceholderText("Select first date...")
        date_layout.addWidget(self.comboDateA)
        
        # Date B selection  
        date_layout.addWidget(QLabel("Date B:"))
        self.comboDateB = QComboBox()
        self.comboDateB.setMinimumWidth(150)
        self.comboDateB.setPlaceholderText("Select second date...")
        date_layout.addWidget(self.comboDateB)
        
        # Compare button
        self.btnCompareMPC = QPushButton("Compare Results")
        self.btnCompareMPC.setObjectName("primaryButton")
        date_layout.addWidget(self.btnCompareMPC)
        
        date_layout.addStretch()
        layout.addWidget(date_group)

        # Results table
        results_group = QGroupBox("MPC Comparison Results")
        results_layout = QVBoxLayout(results_group)
        results_layout.setContentsMargins(16, 16, 16, 16)

        self.tableMPC = QTableWidget()
        self.tableMPC.setAlternatingRowColors(True)
        self.tableMPC.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tableMPC.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableMPC.setColumnCount(4)
        self.tableMPC.setHorizontalHeaderLabels([
            "Parameter",
            "Date A Result", 
            "Date B Result",
            "Status"
        ])
        
        # Set column widths
        header = self.tableMPC.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Parameter
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Date A
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Date B  
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Status
        
        self.tableMPC.setMinimumHeight(400)
        results_layout.addWidget(self.tableMPC)

        # Load sample MPC data
        self._populate_sample_mpc_data()
        
        layout.addWidget(results_group)

        # Statistics
        stats_group = QGroupBox("MPC Statistics")
        stats_layout = QHBoxLayout(stats_group)
        stats_layout.setContentsMargins(16, 16, 16, 16)

        self.lblMPCStats = QLabel("Select dates to view comparison statistics")
        self.lblMPCStats.setWordWrap(True)
        stats_layout.addWidget(self.lblMPCStats)

        stats_layout.addStretch()
        layout.addWidget(stats_group)

    def _populate_sample_mpc_data(self):
        """Populate sample MPC data for demonstration"""
        # Sample MPC check categories and parameters
        mpc_data = [
            # Geometric Checks
            ("Geometry", "Isocenter Radius (mm)", "0.8", "0.9", "PASS"),
            ("Geometry", "Gantry Accuracy (°)", "0.1", "0.2", "PASS"), 
            ("Geometry", "Collimator Accuracy (°)", "0.1", "0.1", "PASS"),
            ("Geometry", "Couch Accuracy (°)", "0.3", "0.4", "PASS"),
            ("Geometry", "Laser Alignment (mm)", "0.5", "0.8", "PASS"),
            
            # Dosimetric Checks
            ("Dosimetry", "Beam Output Constancy (%)", "0.2", "0.3", "PASS"),
            ("Dosimetry", "Beam Uniformity (%)", "1.2", "1.5", "PASS"),
            ("Dosimetry", "Center Shift (mm)", "0.3", "0.4", "PASS"),
            ("Dosimetry", "Energy Constancy (%)", "0.5", "0.8", "PASS"),
            ("Dosimetry", "Dose Rate Constancy (%)", "0.8", "1.0", "PASS"),
            
            # MLC Checks
            ("MLC", "Leaf Position Accuracy (mm)", "0.5", "0.7", "PASS"),
            ("MLC", "Leaf Speed Constancy (%)", "1.0", "1.2", "PASS"),
            ("MLC", "Leaf Gap Width (mm)", "0.1", "0.1", "PASS"),
            
            # Imaging Checks  
            ("Imaging", "Image Quality Score", "95", "93", "PASS"),
            ("Imaging", "Contrast Resolution (%)", "2.1", "2.3", "PASS"),
            ("Imaging", "Spatial Resolution (lp/mm)", "0.8", "0.8", "PASS"),
        ]

        self.tableMPC.setRowCount(len(mpc_data))
        
        for row, (category, param, date_a, date_b, status) in enumerate(mpc_data):
            # Parameter name with category
            param_item = QLabel(f"<b>[{category}]</b><br>{param}")
            param_item.setWordWrap(True)
            self.tableMPC.setCellWidget(row, 0, param_item)
            
            # Date A result
            self.tableMPC.setItem(row, 1, QTableWidgetItem(date_a))
            
            # Date B result  
            self.tableMPC.setItem(row, 2, QTableWidgetItem(date_b))
            
            # Status with color coding
            status_item = QLabel(status)
            if status == "PASS":
                status_item.setStyleSheet("color: green; font-weight: bold;")
            elif status == "FAIL":
                status_item.setStyleSheet("color: red; font-weight: bold;")
            else:
                status_item.setStyleSheet("color: orange; font-weight: bold;")
            status_item.setAlignment(Qt.AlignCenter)
            self.tableMPC.setCellWidget(row, 3, status_item)

        # Update statistics
        total_checks = len(mpc_data)
        passed_checks = sum(1 for _, _, _, _, status in mpc_data if status == "PASS")
        self.lblMPCStats.setText(
            f"Total Checks: {total_checks} | Passed: {passed_checks} | "
            f"Pass Rate: {(passed_checks/total_checks)*100:.1f}%"
        )

    def setup_fault_code_tab(self):
        self.tabFaultCode = QWidget()
        self.tabWidget.addTab(self.tabFaultCode, "🔍 Fault Code Viewer")
        layout = QVBoxLayout(self.tabFaultCode)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        header_label = QLabel("<h2>LINAC Fault Code Viewer</h2>")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setWordWrap(True)
        layout.addWidget(header_label)

        search_group = QGroupBox("Search Fault Codes")
        search_layout = QVBoxLayout(search_group)
        search_layout.setSpacing(12)
        search_layout.setContentsMargins(16, 16, 16, 16)

        code_input_layout = QHBoxLayout()
        code_label = QLabel("Enter Fault Code:")
        code_label.setMinimumWidth(120)
        code_input_layout.addWidget(code_label)

        self.txtFaultCode = QLineEdit()
        self.txtFaultCode.setPlaceholderText("e.g., 400027")
        self.txtFaultCode.setMaximumWidth(200)
        code_input_layout.addWidget(self.txtFaultCode)

        self.btnSearchCode = QPushButton("Search Code")
        self.btnSearchCode.setObjectName("primaryButton")
        self.btnSearchCode.setMaximumWidth(120)
        code_input_layout.addWidget(self.btnSearchCode)

        code_input_layout.addStretch()
        search_layout.addLayout(code_input_layout)

        desc_input_layout = QHBoxLayout()
        desc_label = QLabel("Search Description:")
        desc_label.setMinimumWidth(120)
        desc_input_layout.addWidget(desc_label)

        self.txtSearchDescription = QLineEdit()
        self.txtSearchDescription.setPlaceholderText("Enter keywords to search in descriptions...")
        desc_input_layout.addWidget(self.txtSearchDescription)

        self.btnSearchDescription = QPushButton("Search Description")
        self.btnSearchDescription.setObjectName("secondaryButton")
        self.btnSearchDescription.setMaximumWidth(150)
        desc_input_layout.addWidget(self.btnSearchDescription)

        search_layout.addLayout(desc_input_layout)
        layout.addWidget(search_group)

        results_group = QGroupBox("Search Results")
        results_layout = QVBoxLayout(results_group)
        results_layout.setContentsMargins(16, 16, 16, 16)

        self.txtFaultResult = QTextEdit()
        self.txtFaultResult.setReadOnly(True)
        self.txtFaultResult.setMinimumHeight(150)
        self.txtFaultResult.setPlaceholderText("Search results will appear here...")
        results_layout.addWidget(self.txtFaultResult)

        # Add HAL and TB Description text boxes
        descriptions_layout = QHBoxLayout()
        descriptions_layout.setSpacing(12)
        
        # HAL Description box
        hal_group = QGroupBox("HAL Description")
        hal_layout = QVBoxLayout(hal_group)
        hal_layout.setContentsMargins(8, 8, 8, 8)
        
        self.txtHALDescription = QTextEdit()
        self.txtHALDescription.setReadOnly(True)
        self.txtHALDescription.setMaximumHeight(120)
        self.txtHALDescription.setPlaceholderText("HAL fault description will appear here...")
        hal_layout.addWidget(self.txtHALDescription)
        
        # TB Description box
        tb_group = QGroupBox("TB Description")
        tb_layout = QVBoxLayout(tb_group)
        tb_layout.setContentsMargins(8, 8, 8, 8)
        
        self.txtTBDescription = QTextEdit()
        self.txtTBDescription.setReadOnly(True)
        self.txtTBDescription.setMaximumHeight(120)
        self.txtTBDescription.setPlaceholderText("TB fault description will appear here...")
        tb_layout.addWidget(self.txtTBDescription)
        
        descriptions_layout.addWidget(hal_group)
        descriptions_layout.addWidget(tb_group)
        
        results_layout.addLayout(descriptions_layout)
        layout.addWidget(results_group)

        stats_group = QGroupBox("Fault Code Statistics")
        stats_layout = QHBoxLayout(stats_group)
        stats_layout.setContentsMargins(16, 16, 16, 16)

        self.lblTotalCodes = QLabel("Total Codes: Loading...")
        self.lblTotalCodes.setWordWrap(True)
        stats_layout.addWidget(self.lblTotalCodes)

        self.lblFaultTypes = QLabel("Types: Loading...")
        self.lblFaultTypes.setWordWrap(True)
        stats_layout.addWidget(self.lblFaultTypes)

        stats_layout.addStretch()
        layout.addWidget(stats_group)

        layout.addStretch()

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
            "<p>Developed by <b>gobioeng.com</b></p>"
            "<p><a href='https://gobioeng.com'>gobioeng.com</a></p>"
            "<p>© 2025 Gobioeng. All rights reserved.</p>"
        )
        app_info.setAlignment(Qt.AlignCenter)
        app_info.setOpenExternalLinks(True)
        app_info.setWordWrap(True)
        layout.addWidget(app_info)
        layout.addStretch()
