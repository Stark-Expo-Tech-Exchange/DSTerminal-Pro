# -*- mode: python ; coding: utf-8 -*-

import os
import sys

a = Analysis(
    ['dsterminal.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('integrity_monitor.py', '.'),
        ('crypto_engine.py', '.'),
        ('edu_typing_engine.py', '.'),
        ('recon.py', '.'),
        ('recon_full.py', '.'),
        ('VERSION', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
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