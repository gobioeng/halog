#!/usr/bin/env python3
"""
Windows Directory-Based Installer for HALog Application
Creates portable directory installation with encrypted source protection
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
    encrypted_archive = Path('source_backup_encrypted_dir.zip')
    with zipfile.ZipFile(encrypted_archive, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in encrypted_dir.rglob('*.enc'):
            zipf.write(file_path, file_path.name)
    
    # Cleanup temp directory
    shutil.rmtree(temp_dir)
    
    print(f"✓ Source files encrypted and saved to {encrypted_archive}")
    return encrypted_archive

def create_cx_freeze_setup():
    """Create cx_Freeze setup script for directory-based build"""
    print("📝 Creating cx_Freeze setup script...")
    
    setup_content = '''import sys
import os
from cx_Freeze import setup, Executable
from pathlib import Path

# Determine if we're on Windows
is_windows = sys.platform == "win32"

# Build options for optimization
build_exe_options = {
    "packages": [
        "PyQt5.QtCore",
        "PyQt5.QtGui", 
        "PyQt5.QtWidgets",
        "pandas",
        "numpy",
        "matplotlib",
        "scipy",
        "sqlite3",
        "parser_fault_code",
        "parser_linac",
        "database",
        "analyzer_data",
        "worker_thread",
        "progress_dialog",
        "utils_plot",
        "about_dialog",
        "splash_screen",
        "styles",
        "resource_helper",
        "bootstrap"
    ],
    "excludes": [
        "tkinter",
        "test",
        "unittest",
        "doctest", 
        "pdb",
        "inspect",
        "difflib",
        "email",
        "urllib3",
        "requests",
        "xml",
        "html"
    ],
    "include_files": [
        ("data/", "data/"),
        ("assets/", "assets/") if Path("assets").exists() else None,
        "requirements.txt"
    ],
    "optimize": 2,  # Optimize bytecode
    "include_msvcrt": True if is_windows else False,
    "zip_include_packages": "*",  # Compress packages for smaller size
}

# Remove None entries from include_files
build_exe_options["include_files"] = [f for f in build_exe_options["include_files"] if f is not None]

# Executable configuration
base = "Win32GUI" if is_windows else None
icon_path = "assets/linac_logo.ico" if Path("assets/linac_logo.ico").exists() else None

executables = [
    Executable(
        "main.py",
        base=base,
        target_name="HALog.exe" if is_windows else "HALog",
        icon=icon_path,
        shortcut_name="HALog",
        shortcut_dir="DesktopFolder"
    )
]

setup(
    name="HALog",
    version="0.0.1",
    description="Professional LINAC Water System Monitor - gobioeng.com",
    author="gobioeng.com",
    author_email="support@gobioeng.com",
    url="https://gobioeng.com",
    options={"build_exe": build_exe_options},
    executables=executables
)
'''
    
    with open('setup_directory.py', 'w') as f:
        f.write(setup_content)
    
    print("✓ cx_Freeze setup script created: setup_directory.py")
    return Path('setup_directory.py')

def build_directory_installer():
    """Build the directory-based installer"""
    print("🔨 Building directory-based installer...")
    
    # Ensure cx_Freeze is available
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'cx_Freeze'], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to install cx_Freeze")
        return False
    
    # Create setup script
    setup_script = create_cx_freeze_setup()
    
    # Run cx_Freeze
    cmd = [sys.executable, str(setup_script), 'build']
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Build completed successfully")
        
        # Find the build directory
        build_dirs = list(Path('build').glob('exe.*'))
        if build_dirs:
            build_dir = build_dirs[0]
            print(f"✓ Build directory created: {build_dir}")
            return build_dir
        else:
            print("❌ Build directory not found")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return None

def create_launcher_scripts(install_dir):
    """Create optimized launcher scripts"""
    print("⚡ Creating launcher scripts...")
    
    # Windows batch launcher
    batch_launcher = '''@echo off
REM HALog Fast Directory Launcher
REM Developed by gobioeng.com

echo Starting HALog from directory installation...

REM Set environment variables for faster startup
set PYTHONOPTIMIZE=2
set PYTHONDONTWRITEBYTECODE=1
set NUMEXPR_MAX_THREADS=8
set PATH=%~dp0;%PATH%

REM Check for existing HALog process
tasklist /FI "IMAGENAME eq HALog.exe" 2>NUL | find /I /N "HALog.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo HALog is already running. Bringing to foreground...
    goto :bring_to_front
)

REM Change to HALog directory
cd /d "%~dp0"

REM Start HALog with high priority
echo Launching HALog with performance optimizations...
start /HIGH /B HALog.exe

echo HALog started successfully!
timeout /T 2 /NOBREAK >nul
goto :end

:bring_to_front
REM Use PowerShell to bring window to front
powershell -Command "Add-Type -TypeDefinition 'using System; using System.Diagnostics; using System.Runtime.InteropServices; public class Win32 { [DllImport(\\\"user32.dll\\\")] public static extern bool SetForegroundWindow(IntPtr hWnd); [DllImport(\\\"user32.dll\\\")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow); }'; $p = Get-Process -Name HALog -ErrorAction SilentlyContinue; if ($p) { [Win32]::ShowWindow($p.MainWindowHandle, 3); [Win32]::SetForegroundWindow($p.MainWindowHandle) }"
echo HALog window brought to foreground.
timeout /T 2 /NOBREAK >nul

:end
'''
    
    with open(install_dir / 'Launch_HALog_Fast.bat', 'w') as f:
        f.write(batch_launcher)
    
    # PowerShell launcher for advanced features
    ps_launcher = '''# HALog PowerShell Launcher
# Developed by gobioeng.com

Write-Host "HALog Advanced Launcher" -ForegroundColor Green
Write-Host "Developed by gobioeng.com" -ForegroundColor Cyan
Write-Host ""

# Set environment for optimization
$env:PYTHONOPTIMIZE = "2"
$env:PYTHONDONTWRITEBYTECODE = "1" 
$env:NUMEXPR_MAX_THREADS = "8"

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Check if HALog is already running
$existing = Get-Process -Name "HALog" -ErrorAction SilentlyContinue

if ($existing) {
    Write-Host "HALog is already running. Bringing window to front..." -ForegroundColor Yellow
    
    # Bring to foreground
    Add-Type -TypeDefinition @"
        using System;
        using System.Diagnostics;
        using System.Runtime.InteropServices;
        public class Win32 {
            [DllImport("user32.dll")]
            public static extern bool SetForegroundWindow(IntPtr hWnd);
            [DllImport("user32.dll")]
            public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        }
"@
    
    [Win32]::ShowWindow($existing.MainWindowHandle, 3)
    [Win32]::SetForegroundWindow($existing.MainWindowHandle)
    
    Write-Host "HALog window activated." -ForegroundColor Green
    Start-Sleep -Seconds 1
    exit 0
}

Write-Host "Starting HALog with optimizations..." -ForegroundColor Green

# Launch with high priority
$process = Start-Process -FilePath ".\\HALog.exe" -PassThru -WindowStyle Normal
$process.PriorityClass = "High"

Write-Host "HALog started successfully!" -ForegroundColor Green
Write-Host "Process ID: $($process.Id)" -ForegroundColor Gray

# Wait briefly to ensure startup
Start-Sleep -Seconds 2
'''
    
    with open(install_dir / 'Launch_HALog_Advanced.ps1', 'w') as f:
        f.write(ps_launcher)
    
    # Create desktop shortcut script
    shortcut_script = '''@echo off
REM Create Desktop Shortcut for HALog
REM Developed by gobioeng.com

echo Creating desktop shortcut for HALog...

set "script_dir=%~dp0"
set "target=%script_dir%Launch_HALog_Fast.bat"
set "desktop=%USERPROFILE%\\Desktop"
set "shortcut=%desktop%\\HALog - LINAC Monitor.lnk"

REM Create shortcut using PowerShell
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut%'); $Shortcut.TargetPath = '%target%'; $Shortcut.WorkingDirectory = '%script_dir%'; $Shortcut.Description = 'HALog - Professional LINAC Water System Monitor'; $Shortcut.Save()"

if exist "%shortcut%" (
    echo ✓ Desktop shortcut created successfully!
    echo Location: %shortcut%
) else (
    echo ❌ Failed to create desktop shortcut
)

pause
'''
    
    with open(install_dir / 'Create_Desktop_Shortcut.bat', 'w') as f:
        f.write(shortcut_script)
    
    print("✓ Launcher scripts created")

def create_portable_package(build_dir):
    """Create portable installation package"""
    print("📦 Creating portable package...")
    
    # Create portable directory
    portable_dir = Path('HALog_Portable_Windows')
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    portable_dir.mkdir()
    
    # Copy built application
    if build_dir:
        for item in build_dir.iterdir():
            if item.is_dir():
                shutil.copytree(item, portable_dir / item.name)
            else:
                shutil.copy2(item, portable_dir / item.name)
        print(f"✓ Copied application files from {build_dir}")
    
    # Create launcher scripts
    create_launcher_scripts(portable_dir)
    
    # Create installation instructions
    instructions = '''# HALog Portable Installation

## What is this?

HALog Portable is a directory-based installation that doesn't require 
administrator privileges or system installation. Just extract and run!

## Installation Instructions

1. Extract this entire folder to your desired location
2. Double-click "Launch_HALog_Fast.bat" to start the application
3. Optional: Run "Create_Desktop_Shortcut.bat" to add desktop shortcut

## Launch Options

- **Launch_HALog_Fast.bat**: Standard fast launcher (recommended)
- **Launch_HALog_Advanced.ps1**: PowerShell launcher with advanced features
- **HALog.exe**: Direct executable (slower startup)

## Fast Startup Features

- Environment optimization for faster loading
- Process checking to prevent multiple instances
- High priority execution for better performance  
- Window management for existing instances
- Automatic path configuration

## Advantages of Portable Installation

✓ No administrator rights required
✓ Can run from USB drive
✓ Multiple versions can coexist
✓ Easy to backup and move
✓ No registry changes
✓ Clean uninstall (just delete folder)

## System Requirements

- Windows 10/11 (64-bit)
- 4GB RAM minimum, 8GB recommended
- 200MB free disk space
- No additional software required

## Features

- Professional LINAC fault code database (HAL & TB)
- Enhanced progress tracking for large file processing
- Grouped parameter visualization by type
- Material Design 3.0 interface
- High-performance data analysis

## File Structure

```
HALog_Portable_Windows/
├── HALog.exe                    # Main application
├── Launch_HALog_Fast.bat        # Fast launcher
├── Launch_HALog_Advanced.ps1    # Advanced launcher
├── Create_Desktop_Shortcut.bat  # Shortcut creator
├── data/                        # Fault code databases
├── assets/                      # Application resources
├── lib/                         # Python libraries
└── README.txt                   # This file
```

## Troubleshooting

- If the app doesn't start, try running as administrator
- For performance issues, close other applications
- Check Windows Defender exclusions if startup is slow

## Support

Developed by gobioeng.com
Version: 0.0.1 beta
© 2025 gobioeng.com - All Rights Reserved

For technical support, visit: https://gobioeng.com
'''
    
    with open(portable_dir / 'README.txt', 'w') as f:
        f.write(instructions)
    
    # Create ZIP archive
    archive_name = 'HALog_Portable_Windows.zip'
    print(f"Creating archive: {archive_name}")
    
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in portable_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(portable_dir.parent)
                zipf.write(file_path, arcname)
                
    # Calculate size
    archive_size = Path(archive_name).stat().st_size / (1024 * 1024)
    print(f"✓ Created portable package: {archive_name} ({archive_size:.1f} MB)")
    
    return archive_name

def main():
    """Main build process for directory installer"""
    print("🚀 HALog Directory-Based Installer Builder")
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
        
        # Step 2: Build directory installer
        build_dir = build_directory_installer()
        if not build_dir:
            print("❌ Failed to build directory installer")
            sys.exit(1)
        
        # Step 3: Create portable package
        package_path = create_portable_package(build_dir)
        
        print()
        print("✅ Directory-based build completed successfully!")
        print(f"📦 Portable package: {package_path}")
        print(f"🔒 Encrypted source backup: {encrypted_archive}")
        print()
        print("🎯 Next steps:")
        print("1. Test the portable package on a clean Windows system")
        print("2. Distribute the ZIP file to users")
        print("3. Users can extract and run without installation")
        print("4. Keep the encrypted source backup secure")
        
    except Exception as e:
        print(f"❌ Build failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()