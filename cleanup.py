#!/usr/bin/env python3
"""
HALog Codebase Cleanup Utility
Simple script to clean up temporary files and maintain repository
Developer: Tanmay Pandey
Company: gobioeng.com
"""

import os
import sys
import shutil
from pathlib import Path

def clean_pycache():
    """Remove Python cache files"""
    print("🧹 Cleaning Python cache files...")
    
    for root, dirs, files in os.walk('.'):
        # Remove __pycache__ directories
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            shutil.rmtree(cache_dir)
            print(f"  Removed: {cache_dir}")
        
        # Remove .pyc files
        for file in files:
            if file.endswith('.pyc') or file.endswith('.pyo'):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"  Removed: {file_path}")

def clean_temp_files():
    """Remove temporary files"""
    print("🧹 Cleaning temporary files...")
    
    temp_patterns = [
        '*.tmp', '*.temp', '*.bak', '*.backup', 
        '*~', '.DS_Store', 'Thumbs.db'
    ]
    
    for pattern in temp_patterns:
        for file_path in Path('.').rglob(pattern):
            try:
                if file_path.is_file():
                    file_path.unlink()
                    print(f"  Removed: {file_path}")
            except Exception as e:
                print(f"  Error removing {file_path}: {e}")

def clean_build_artifacts():
    """Remove build artifacts"""
    print("🧹 Cleaning build artifacts...")
    
    build_dirs = ['build', 'dist', '__pycache__', '.pytest_cache', '.coverage']
    
    for dir_name in build_dirs:
        for dir_path in Path('.').rglob(dir_name):
            if dir_path.is_dir():
                try:
                    shutil.rmtree(dir_path)
                    print(f"  Removed directory: {dir_path}")
                except Exception as e:
                    print(f"  Error removing {dir_path}: {e}")

def show_file_count():
    """Show current file count and structure"""
    print("📊 Current file structure:")
    
    py_files = list(Path('.').glob('*.py'))
    print(f"  Python files: {len(py_files)}")
    
    for py_file in sorted(py_files):
        lines = sum(1 for _ in open(py_file, 'r', encoding='utf-8', errors='ignore'))
        print(f"    {py_file.name}: {lines} lines")

def main():
    """Main cleanup function"""
    print("🚀 HALog Codebase Cleanup Utility")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--stats-only':
        show_file_count()
        return
    
    clean_pycache()
    clean_temp_files()
    clean_build_artifacts()
    
    print("\n📊 Cleanup summary:")
    show_file_count()
    
    print("\n✅ Cleanup completed!")
    print("\n💡 Usage:")
    print("  python cleanup.py           # Full cleanup")
    print("  python cleanup.py --stats-only  # Show stats only")

if __name__ == "__main__":
    main()