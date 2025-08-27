"""
Gobioeng HALog - Enhanced Build Script with Source Protection and ZIP Packaging
Builds PyInstaller EXE with improved asset handling, icon validation and ZIP distribution.
Author: gobioeng
Date: 2025-08-22 15:02:08
User: gobioengi
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import zipfile
import time

APP_NAME = "HALog"
APP_VERSION = "0.0.1"
DIST_DIR = f"HALog_Windows_v{APP_VERSION}"
SPEC_FILE = "HALog.spec"
ZIP_NAME = f"{DIST_DIR}.zip"

def print_header(text):
    """Print styled header text"""
    print("\n" + "=" * 70)
    print(f" {text}")
    print("=" * 70)

def ensure_version_file():
    """Create version file for executable metadata if missing"""
    version_file = Path('version_file.txt')
    if not version_file.exists():
        with open(version_file, 'w') as f:
            f.write(f"""[Version]
FileVersion={APP_VERSION}.0
ProductVersion={APP_VERSION}
CompanyName=gobioeng.com
FileDescription=LINAC Water System Monitor
LegalCopyright=(c) {time.strftime('%Y')} gobioeng.com
""")
        print("✓ Created version_file.txt")
    else:
        print("✓ Version file already exists")

def ensure_icon():
    """Ensure application icon exists, generating if missing"""
    ico_path = Path("assets") / "linac_logo.ico"
    if not ico_path.exists():
        print("🔍 Icon not found, creating...")
        
        # Create assets directory if needed
        ico_path.parent.mkdir(exist_ok=True)
        
        # Generate a basic icon
        try:
            # Try to import PyQt5 for icon generation
            from PyQt5.QtGui import QIcon, QPixmap, QImage, QPainter, QColor
            
            # Create a simple colored square
            img = QImage(256, 256, QImage.Format_ARGB32)
            img.fill(QColor(52, 152, 219))  # Blue
            img.save(str(ico_path))
            print(f"✓ Created icon: {ico_path}")
        except Exception as e:
            print(f"Error creating icon: {e}")
            # Create an empty file as last resort
            with open(ico_path, 'wb') as f:
                f.write(b'')
            print("⚠️ Created empty icon file")
    else:
        print(f"✓ Icon found: {ico_path}")

def clean_previous_builds():
    """Clean previous build artifacts"""
    print("Cleaning previous build files...")
    
    for folder in [DIST_DIR, "build", "dist"]:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"✓ Removed previous: {folder}/")
            except Exception as e:
                print(f"⚠️ Could not remove {folder}: {e}")
    
    if os.path.exists(ZIP_NAME):
        try:
            os.remove(ZIP_NAME)
            print(f"✓ Removed previous ZIP: {ZIP_NAME}")
        except Exception as e:
            print(f"⚠️ Could not remove {ZIP_NAME}: {e}")

def create_spec_file():
    """Create a PyInstaller spec file if none exists"""
    print(f"Creating spec file: {SPEC_FILE}")
    
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-
# HALog PyInstaller spec file
# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
# User: {os.getlogin()}

import sys
from pathlib import Path

block_cipher = None

# Determine assets path
assets_path = Path('assets')
sample_data_path = Path('sample_halog_data.txt')

# Define data files to include
datas = []

# Add assets directory if it exists
if assets_path.exists():
    datas.append(('assets', 'assets'))

# Add sample data if it exists
if sample_data_path.exists():
    datas.append(('sample_halog_data.txt', '.'))

a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=datas,
             hiddenimports=['pandas', 'numpy', 'matplotlib', 'scipy', 'sklearn', 'PyQt5'],
             hookspath=[],
             hooksconfig={{}},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='{APP_NAME}',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='assets/linac_logo.ico' if Path('assets/linac_logo.ico').exists() else None)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='{APP_NAME}')
"""

    try:
        with open(SPEC_FILE, 'w') as f:
            f.write(spec_content)
        print(f"✓ Created spec file: {SPEC_FILE}")
        return True
    except Exception as e:
        print(f"❌ Failed to create spec file: {e}")
        return False

def run_pyinstaller():
    """Run PyInstaller with the spec file or create one"""
    print("📦 Running PyInstaller...")
    
    # Create spec file if it doesn't exist
    if not Path(SPEC_FILE).exists():
        if not create_spec_file():
            return False
    
    # Run PyInstaller with the spec file
    try:
        print(f"📦 Running PyInstaller with {SPEC_FILE}...")
        subprocess.run([sys.executable, "-m", "PyInstaller", SPEC_FILE], check=True)
        print("✓ PyInstaller completed successfully")
        
        # Rename dist directory if needed
        if os.path.exists(f"dist/{APP_NAME}") and f"dist/{APP_NAME}" != DIST_DIR:
            if os.path.exists(DIST_DIR):
                shutil.rmtree(DIST_DIR)
            shutil.move(f"dist/{APP_NAME}", DIST_DIR)
            print(f"✓ Renamed output directory to {DIST_DIR}")
            
        return True
    except Exception as e:
        print(f"❌ PyInstaller failed: {e}")
        return False

def run_direct_pyinstaller():
    """Run PyInstaller directly without using a spec file"""
    print("📦 Running PyInstaller directly...")
    
    icon_path = Path("assets") / "linac_logo.ico"
    icon_option = []
    if icon_path.exists():
        icon_option = ["--icon", str(icon_path)]
    
    # Build command
    cmd = [
        sys.executable, 
        "-m", 
        "PyInstaller",
        "--name", APP_NAME,
        "--onedir",  # Use onedir for more reliable asset loading
        "--windowed",
        "--add-data", f"assets{os.pathsep}assets",
    ]
    
    # Add sample data if it exists
    if Path("sample_halog_data.txt").exists():
        cmd.extend(["--add-data", f"sample_halog_data.txt{os.pathsep}."])
    
    # Add icon if it exists
    cmd.extend(icon_option)
    
    # Add main.py
    cmd.append("main.py")
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ PyInstaller completed successfully")
        
        # Rename dist directory if needed
        if os.path.exists(f"dist/{APP_NAME}") and f"dist/{APP_NAME}" != DIST_DIR:
            if os.path.exists(DIST_DIR):
                shutil.rmtree(DIST_DIR)
            shutil.move(f"dist/{APP_NAME}", DIST_DIR)
            print(f"✓ Renamed output directory to {DIST_DIR}")
            
        return True
    except Exception as e:
        print(f"❌ PyInstaller failed: {e}")
        return False

def remove_py_files_from_output():
    """Remove all .py files from output directory for source protection."""
    if not os.path.exists(DIST_DIR):
        print("⚠️ Output directory not found, skipping .py cleanup")
        return
        
    print("🛡️ Removing .py files from build output for source protection...")
    count = 0
    for py_file in Path(DIST_DIR).rglob('*.py'):
        try:
            py_file.unlink()
            count += 1
        except Exception as e:
            print(f"⚠️ Could not remove {py_file}: {e}")
    print(f"✓ Removed {count} .py files.")

def make_zip_of_output():
    """Zip the output folder for distribution."""
    if not os.path.exists(DIST_DIR):
        print("⚠️ Output directory not found, skipping ZIP creation")
        return
        
    print(f"📦 Creating ZIP archive: {ZIP_NAME}")
    try:
        zipf = zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED)
        file_count = 0
        for root, dirs, files in os.walk(DIST_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(DIST_DIR))
                zipf.write(file_path, arcname)
                file_count += 1
        zipf.close()
        print(f"✓ ZIP archive created: {ZIP_NAME} with {file_count} files")
    except Exception as e:
        print(f"❌ Failed to create ZIP: {e}")

def check_assets_in_output():
    """Check that assets (especially icon) are present in the output folder."""
    if not os.path.exists(DIST_DIR):
        print("⚠️ Output directory not found, skipping asset check")
        return
        
    assets_out = Path(DIST_DIR) / "assets"
    ico_out = assets_out / "linac_logo.ico"
    if not assets_out.exists():
        print(f"⚠️ WARNING: Assets directory not found in output: {assets_out}")
        print("   Creating assets directory in output...")
        try:
            assets_out.mkdir(exist_ok=True)
            # Copy icon if exists
            if Path("assets/linac_logo.ico").exists():
                shutil.copy("assets/linac_logo.ico", assets_out)
                print(f"✓ Copied icon to output: {ico_out}")
        except Exception as e:
            print(f"⚠️ Could not create assets directory: {e}")
    elif not ico_out.exists():
        print(f"⚠️ WARNING: Icon file not found in output: {ico_out}")
        # Copy icon if exists
        if Path("assets/linac_logo.ico").exists():
            try:
                shutil.copy("assets/linac_logo.ico", assets_out)
                print(f"✓ Copied icon to output: {ico_out}")
            except Exception as e:
                print(f"⚠️ Could not copy icon: {e}")
    else:
        print(f"✓ Icon present in output: {ico_out}")

def main():
    print_header(f"HALog Build & ZIP - Source Protected v{APP_VERSION}")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} detected")
    except ImportError:
        print("❌ PyInstaller not found. Please install it with:")
        print("   pip install pyinstaller")
        return False
    
    ensure_version_file()
    ensure_icon()
    clean_previous_builds()
    
    # Try both methods
    if not run_pyinstaller():
        print("\n⚠️ Spec file method failed, trying direct PyInstaller...")
        if not run_direct_pyinstaller():
            print("\n❌ Build failed with both methods!")
            return False
    
    check_assets_in_output()
    remove_py_files_from_output()
    make_zip_of_output()
    
    print("\n🎉 Build complete!")
    print(f"📁 Output: {DIST_DIR}/")
    print(f"📦 Distribution ZIP: {ZIP_NAME}")
    print("Ready to share: send the ZIP file for easy installation.")
    return True

if __name__ == "__main__":
    success = main()
    print("=" * 70)
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
