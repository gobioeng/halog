"""
Windows launcher script for Gobioeng HALog
Handles environment setup and application launch
"""

import sys
import os
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        print(f"Current version: {platform.python_version()}")
        input("Press Enter to exit...")
        sys.exit(1)

    print(f"✓ Python {platform.python_version()} detected")


def check_dependencies():
    """Check and install required dependencies"""
    print("Checking dependencies...")

    required_packages = [
        "PyQt5",
        "pandas",
        "matplotlib",
        "scipy",
        "scikit-learn",
        "numpy",
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.lower().replace("-", "_"))
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} (missing)")

    if missing_packages:
        print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--upgrade"] + missing_packages
            )
            print("✓ All dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("Error: Failed to install dependencies")
            print("Please install manually using:")
            print(f"pip install {' '.join(missing_packages)}")
            input("Press Enter to exit...")
            sys.exit(1)


def setup_environment():
    """Setup application environment"""
    # Add current directory to Python path
    current_dir = Path(__file__).parent.absolute()
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))

    # Create necessary directories
    assets_dir = current_dir / "assets"
    if not assets_dir.exists():
        assets_dir.mkdir(exist_ok=True)
        print(f"✓ Created assets directory: {assets_dir}")

    print("✓ Environment setup complete")


def launch_application():
    """Launch the HALog application"""
    try:
        print("🚀 Launching Gobioeng HALog...")
        print("=" * 50)

        # Import and run the application
        from main import HALogApp
        from PyQt5.QtWidgets import QApplication

        app = QApplication(sys.argv)
        app.setApplicationName("Gobioeng HALog")
        app.setApplicationVersion("0.0.1")
        app.setOrganizationName("gobioeng.com")

        window = HALogApp()
        window.show()

        sys.exit(app.exec_())

    except Exception as e:
        print(f"Error launching application: {e}")
        print("Please check that all files are present and try again.")
        input("Press Enter to exit...")
        sys.exit(1)


def main():
    """Main entry point"""
    print("Gobioeng HALog 0.0.1 beta")
    print("LINAC Water System Monitor")
    print("Developed by gobioeng.com")
    print("=" * 50)

    try:
        check_python_version()
        check_dependencies()
        setup_environment()
        launch_application()

    except KeyboardInterrupt:
        print("\n\nApplication startup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
