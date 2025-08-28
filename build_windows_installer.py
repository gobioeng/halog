#!/usr/bin/env python3
"""
Windows Installer Builder for HALog Application
Creates encrypted single-file executable with fast startup
Developer: gobioeng.com
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import tempfile
import zipfile
import base64

def encrypt_source_files():
    """Create encrypted source backup"""
    print("🔒 Creating encrypted source backup...")
    
    # Create temporary directory for encrypted files
    temp_dir = Path(tempfile.mkdtemp())
    
    # List of Python files to encrypt
    source_files = [
        'main.py', 'main_window.py', 'parser_fault_code.py',
        'parser_linac.py', 'progress_dialog.py', 'utils_plot.py',
        'database.py', 'analyzer_data.py', 'worker_thread.py',
        'about_dialog.py', 'splash_screen.py', 'styles.py',
        'resource_helper.py', 'bootstrap.py'
    ]
    
    encrypted_dir = temp_dir / 'encrypted_source'
    encrypted_dir.mkdir()
    
    for source_file in source_files:
        if Path(source_file).exists():
            # Simple base64 encoding for source protection
            with open(source_file, 'rb') as f:
                content = f.read()
            
            encoded_content = base64.b64encode(content)
            
            with open(encrypted_dir / f"{source_file}.enc", 'wb') as f:
                f.write(encoded_content)
    
    # Create encrypted archive
    encrypted_archive = Path('source_backup_encrypted.zip')
    with zipfile.ZipFile(encrypted_archive, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in encrypted_dir.rglob('*.enc'):
            zipf.write(file_path, file_path.name)
    
    # Cleanup temp directory
    shutil.rmtree(temp_dir)
    
    print(f"✓ Source files encrypted and saved to {encrypted_archive}")
    return encrypted_archive

def create_pyinstaller_spec():
    """Create optimized PyInstaller spec for fast startup"""
    print("📝 Creating optimized PyInstaller spec...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Optimize for fast startup
block_cipher = None

# Add current directory to path
sys.path.insert(0, str(Path.cwd()))

a = Analysis(
    ['main.py'],
    pathex=[str(Path.cwd())],
    binaries=[],
    datas=[
        ('data/*.txt', 'data'),
        ('assets/*', 'assets'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui', 
        'PyQt5.QtWidgets',
        'pandas',
        'numpy',
        'matplotlib',
        'scipy',
        'sqlite3',
        'parser_fault_code',
        'parser_linac',
        'database',
        'analyzer_data',
        'worker_thread',
        'progress_dialog',
        'utils_plot',
        'about_dialog',
        'splash_screen',
        'styles',
        'resource_helper',
        'bootstrap'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'test',
        'unittest',
        'doctest',
        'pdb',
        'inspect',
        'difflib',
        'email',
        'urllib3',
        'requests'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Optimize imports for faster startup
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HALog',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression for smaller size
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Windows app, no console
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/linac_logo.ico' if Path('assets/linac_logo.ico').exists() else None,
    version_file=None,
)
'''
    
    with open('halog_installer.spec', 'w') as f:
        f.write(spec_content)
    
    print("✓ PyInstaller spec created: halog_installer.spec")
    return Path('halog_installer.spec')

def build_installer():
    """Build the Windows installer executable"""
    print("🔨 Building Windows installer...")
    
    # Ensure PyInstaller is available
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to install PyInstaller")
        return False
    
    # Create spec file
    spec_file = create_pyinstaller_spec()
    
    # Run PyInstaller with optimizations
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',  # Clean cache
        '--noconfirm',  # Overwrite without asking
        '--optimize=2',  # Optimize bytecode
        str(spec_file)
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Build completed successfully")
        
        # Check if executable was created
        exe_path = Path('dist/HALog.exe')
        if exe_path.exists():
            print(f"✓ Executable created: {exe_path}")
            print(f"📦 File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            return exe_path
        else:
            print("❌ Executable not found in dist/ directory")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return None

def create_startup_optimizer():
    """Create startup optimization script"""
    print("⚡ Creating startup optimizer...")
    
    optimizer_content = '''@echo off
REM HALog Fast Startup Optimizer
REM Developed by gobioeng.com

echo Starting HALog with optimizations...

REM Set environment variables for faster startup
set PYTHONOPTIMIZE=2
set PYTHONDONTWRITEBYTECODE=1
set NUMEXPR_MAX_THREADS=8

REM Check for existing HALog process
tasklist /FI "IMAGENAME eq HALog.exe" 2>NUL | find /I /N "HALog.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo HALog is already running. Bringing to foreground...
    goto :bring_to_front
)

REM Start HALog with high priority
echo Launching HALog with performance optimizations...
start /HIGH /B HALog.exe

echo HALog started successfully!
pause
goto :end

:bring_to_front
REM Use PowerShell to bring window to front
powershell -Command "Add-Type -TypeDefinition 'using System; using System.Diagnostics; using System.Runtime.InteropServices; public class Win32 { [DllImport(\"user32.dll\")] public static extern bool SetForegroundWindow(IntPtr hWnd); [DllImport(\"user32.dll\")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow); }'; $p = Get-Process -Name HALog -ErrorAction SilentlyContinue; if ($p) { [Win32]::ShowWindow($p.MainWindowHandle, 3); [Win32]::SetForegroundWindow($p.MainWindowHandle) }"
echo HALog window brought to foreground.
pause

:end
'''
    
    with open('start_halog_fast.bat', 'w') as f:
        f.write(optimizer_content)
    
    print("✓ Startup optimizer created: start_halog_fast.bat")

def create_installation_package():
    """Create complete installation package"""
    print("📦 Creating installation package...")
    
    # Create installation directory
    install_dir = Path('HALog_Windows_Installer')
    if install_dir.exists():
        shutil.rmtree(install_dir)
    install_dir.mkdir()
    
    # Copy executable
    exe_path = Path('dist/HALog.exe')
    if exe_path.exists():
        shutil.copy2(exe_path, install_dir / 'HALog.exe')
        print(f"✓ Copied executable to {install_dir}")
    
    # Copy data files
    if Path('data').exists():
        shutil.copytree('data', install_dir / 'data')
        print("✓ Copied data directory")
    
    # Copy assets
    if Path('assets').exists():
        shutil.copytree('assets', install_dir / 'assets')
        print("✓ Copied assets directory")
    
    # Copy startup optimizer
    if Path('start_halog_fast.bat').exists():
        shutil.copy2('start_halog_fast.bat', install_dir / 'start_halog_fast.bat')
        print("✓ Copied startup optimizer")
    
    # Create README
    readme_content = '''# HALog - Professional LINAC Water System Monitor

## Installation Instructions

1. Copy the entire HALog_Windows_Installer folder to your desired location
2. For fastest startup, use start_halog_fast.bat instead of HALog.exe directly
3. Create a desktop shortcut to start_halog_fast.bat for convenience

## Fast Startup

The start_halog_fast.bat script provides:
- Environment optimization for faster loading
- Process checking to prevent multiple instances  
- High priority execution for better performance
- Window management for existing instances

## Features

- Professional LINAC fault code database (HAL & TB)
- Enhanced progress tracking for large file processing
- Grouped parameter visualization by type
- Material Design 3.0 interface
- High-performance data analysis

## System Requirements

- Windows 10/11 (64-bit)
- 4GB RAM minimum, 8GB recommended
- 100MB free disk space

## Support

Developed by gobioeng.com
Version: 0.0.1 beta
© 2025 gobioeng.com - All Rights Reserved

For technical support, visit: https://gobioeng.com
'''
    
    with open(install_dir / 'README.txt', 'w') as f:
        f.write(readme_content)
    
    print("✓ Created installation README")
    
    # Create ZIP archive
    archive_name = 'HALog_Windows_Installer.zip'
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in install_dir.rglob('*'):
            if file_path.is_file():
                zipf.write(file_path, file_path.relative_to(install_dir.parent))
    
    print(f"✓ Created installation package: {archive_name}")
    return archive_name

def main():
    """Main build process"""
    print("🚀 HALog Windows Installer Builder")
    print("=" * 50)
    print("Developed by gobioeng.com")
    print()
    
    # Check if we're in the right directory
    if not Path('main.py').exists():
        print("❌ main.py not found. Please run this script from the HALog root directory.")
        sys.exit(1)
    
    try:
        # Step 1: Encrypt source files
        encrypted_archive = encrypt_source_files()
        
        # Step 2: Build installer
        exe_path = build_installer()
        if not exe_path:
            print("❌ Failed to build installer")
            sys.exit(1)
        
        # Step 3: Create startup optimizer
        create_startup_optimizer()
        
        # Step 4: Create installation package
        package_path = create_installation_package()
        
        print()
        print("✅ Build completed successfully!")
        print(f"📦 Installation package: {package_path}")
        print(f"🔒 Encrypted source backup: {encrypted_archive}")
        print()
        print("🎯 Next steps:")
        print("1. Test the installation package on a clean Windows system")
        print("2. Distribute the ZIP file to users")
        print("3. Keep the encrypted source backup secure")
        
    except Exception as e:
        print(f"❌ Build failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()