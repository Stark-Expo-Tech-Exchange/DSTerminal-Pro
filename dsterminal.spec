# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Exclude heavy/unnecessary modules (removed 'tkinter')
excludes = [
    'unittest', 'pytest', 'PyQt5', 'PyQt6', 
    'IPython', 'jupyter', 'matplotlib.tests', 'numpy.tests', 
    'pandas.tests', 'scipy', 'scipy.tests', 'setuptools.tests',
    'distutils.tests', '_posixshmem', 'resource', 'fcntl'
]

# Collect data files from directories
def collect_dir(src, dest):
    datas = []
    if os.path.exists(src):
        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            if os.path.isfile(src_path):
                datas.append((src_path, dest))
            elif os.path.isdir(src_path):
                for root, dirs, files in os.walk(src_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, src)
                        datas.append((file_path, os.path.join(dest, rel_path)))
    return datas

datas = []

# Add directories
for dir_name in ['config', 'data', 'docs', 'installer_assets', 'logo_path', 
                  'footer_logo_path', 'redist', 'scans', 'templates', 'tools', 
                  'update', 'DSTerminal_Workspace']:
    datas.extend(collect_dir(dir_name, dir_name))

# Add individual files
files = [
    'VERSION', 'license.txt', 'README.md',
    'version_info.txt',
    'icon-removebg-preview.ico', 'financial_forensics.py',
    'crypto_engine.py', 'integrity_monitor.py', 'recon.py', 'recon_full.py',
    'vt_scan.py', 'edu_typing_engine.py',
    'deletion_protection.py'
]

for file in files:
    if os.path.exists(file):
        datas.append((file, '.'))

a = Analysis(
    ['dsterminal.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'rich', 'rich.console', 'rich.panel', 'rich.align', 'rich.table',
        'rich.live', 'rich.layout', 'rich.progress', 'rich.syntax', 'rich.traceback',
        'colorama', 'requests', 'json', 'os', 'sys', 'time', 'random', 'datetime',
        'pathlib', 'shutil', 'platform', 'subprocess', 'threading', 'hashlib',
        'win32api', 'win32com', 'win32ctypes.pywin32', 'win32ctypes.pywin32.win32api',
        'tqdm', 'pygments', 'cryptography', 'psutil', 'prompt_toolkit', 'pyfiglet',
        'textual', 'tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],  # Removed custom hook-rich.py
    excludes=excludes,
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='dsterminal_win-2026_v2.0.113_x64-amd64',
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
    icon='installer_assets/3486-removebg-preview.ico' if os.path.exists('installer_assets/3486-removebg-preview.ico') else None,
    uac_admin=False,
)