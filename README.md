# HALog - LINAC Water System Monitor

Professional LINAC (Linear Accelerator) water system monitoring application with Material Design UI.

![HALog Logo](assets/linac_logo_256.png)

## Overview

HALog is a sophisticated monitoring and analysis tool for LINAC water systems, providing real-time data visualization, comprehensive analytics, and professional reporting capabilities. Built with PyQt5 and Material Design principles for a modern, intuitive user experience.

## Features

- **Real-time Monitoring**: Live data acquisition and visualization
- **Advanced Analytics**: Statistical analysis and anomaly detection
- **Interactive Graphs**: Zoom, hover tooltips, and export capabilities
- **Material Design UI**: Modern, professional interface
- **High Performance**: Multithreaded processing for large datasets
- **Export Capabilities**: Multiple format support (Excel, PDF, images)
- **Database Integration**: SQLite backend with efficient data management

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gobioeng/halog.git
   cd halog
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

### First Time Setup

1. Launch the application
2. Load sample data using the included `sample_halog_data.txt` file
3. Explore the analytics and visualization features

## System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB free space
- **Display**: 1280x720 minimum resolution

## Development

### Running from Source

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with debugging
python main.py --debug

# Run tests
pytest

# Code formatting
black *.py
flake8 *.py
```

### Building Executable

```bash
# Using PyInstaller
pyinstaller --windowed --icon=assets/linac_logo.ico main.py

# Using cx_Freeze
python setup.py build
```

## Project Structure

```
halog/
├── main.py              # Application entry point
├── ui_mainwindow.py     # Main window UI
├── linac_parser.py      # Data parsing logic
├── data_analyzer.py     # Analytics engine
├── plot_utils.py        # Graph generation
├── database.py          # Database management
├── worker_thread.py     # Background processing
├── assets/              # Images and icons
├── docs/                # Documentation
└── requirements.txt     # Dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is proprietary software developed by [gobioeng.com](https://gobioeng.com).

## Support

For technical support and questions:
- **Website**: [gobioeng.com](https://gobioeng.com)
- **Developer**: Tanmay Pandey
- **Version**: 0.0.1

## Changelog

### Version 0.0.1
- Initial release
- Material Design UI implementation
- Basic LINAC data parsing and visualization
- SQLite database integration
- Multithreaded processing capabilities
