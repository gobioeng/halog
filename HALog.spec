# -*- mode: python ; coding: utf-8 -*-
# HALog PyInstaller spec file
# Generated: 2025-08-22 16:03:20
# User: BlackBox

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
             hooksconfig={},
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
          name='HALog',
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
               name='HALog')
