# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_all, collect_data_files

# Collect all rich data files
rich_datas = collect_data_files('rich')
rich_hiddenimports = [
    'rich._unicode_data.unicode17-0-0',
    'rich._unicode_data.unicode16-0-0',
    'rich._unicode_data.unicode15-1-0',
    'rich._unicode_data.unicode15-0-0',
    'rich._unicode_data.unicode14-0-0',
    'rich._unicode_data.unicode13-0-0',
    'rich._unicode_data.unicode12-1-0',
    'rich._unicode_data.unicode12-0-0',
    'rich._unicode_data.unicode11-0-0',
    'rich._unicode_data.unicode10-0-0',
    'rich._unicode_data.unicode9-0-0',
    'rich._unicode_data.unicode8-0-0',
    'rich._unicode_data.unicode7-0-0',
    'rich._unicode_data.unicode6-3-0',
    'rich._unicode_data.unicode6-2-0',
    'rich._unicode_data.unicode6-1-0',
    'rich._unicode_data.unicode6-0-0',
    'rich._unicode_data.unicode5-2-0',
    'rich._unicode_data.unicode5-1-0',
    'rich._unicode_data.unicode5-0-0',
    'rich._unicode_data.unicode4-1-0',
    'rich.console',
    'rich.progress',
    'rich.panel',
    'rich.table',
    'rich.layout',
    'rich.live',
    'rich.text',
    'rich.align',
    'rich.columns',
]

# Python files to include
python_files = [
    'integrity_monitor.py',
    'crypto_engine.py',
    'edu_typing_engine.py',
    'recon.py',
    'recon_full.py',
]

# Create datas list
datas = []
for file in python_files:
    if os.path.exists(file):
        datas.append((file, '.'))

# Also include VERSION and requirements
if os.path.exists('VERSION'):
    datas.append(('VERSION', '.'))
if os.path.exists('requirements.txt'):
    datas.append(('requirements.txt', '.'))

# Add rich datas
datas.extend(rich_datas)

print(f"Total data files to include: {len(datas)}")

a = Analysis(
    ['dsterminal.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=rich_hiddenimports + [
        'integrity_monitor',
        'crypto_engine',
        'edu_typing_engine',
        'recon',
        'recon_full',
        'rich',
        'tqdm',
        'pygments',
        'colorama',
        'prompt_toolkit',
        'watchdog',
        'watchdog.observers',
        'watchdog.events',
        'psutil',
        'netifaces',
        'cryptography',
        'OpenSSL',
        'reportlab',
        'fpdf',
        'queue',
        'threading',
        'shutil',
        'glob',
        'json',
        'hashlib',
        'socket',
        'uuid',
        'ssl',
        'subprocess',
        'datetime',
        'platform',
        'random',
        're',
        'math',
        'time',
        'os',
        'sys',
        'importlib',
        'importlib.util',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='dsterminal_win-2025_v2.0.113_x64-amd64',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='installer_assets/icon-removebg-preview.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    a.zipfiles,
    a.scripts,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='dsterminal_win-2025_v2.0.113_x64-amd64'
)