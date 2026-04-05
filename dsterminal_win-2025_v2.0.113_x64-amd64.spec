# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('recon.py', '.'), ('recon_full.py', '.'), ('integrity_monitor.py', '.'), ('crypto_engine.py', '.'), ('edu_typing_engine.py', '.'), ('VERSION', '.'), ('requirements.txt', '.'), ('LICENSE.txt', '.'), ('vt_scan.py', '.'), ('README.md', '.')]
binaries = []
hiddenimports = ['recon', 'recon_full', 'watchdog', 'watchdog.observers', 'watchdog.events', 'psutil', 'netifaces', 'cryptography', 'OpenSSL', 'reportlab', 'colorama', 'prompt_toolkit', 'pyfiglet', 'rich', 'tqdm', 'PIL', 'PIL.Image', 'PIL.ImageTk', 'requests', 'dotenv', 'python_dotenv', '_tkinter']
tmp_ret = collect_all('rich')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('tqdm')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pygments')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['dsterminal.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
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
    icon=['installer_assets\\icon-removebg-preview.ico'],
)
