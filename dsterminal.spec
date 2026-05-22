# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

# Exclude heavy/unnecessary modules
excludes = [
    'pytest', 'PyQt5', 'PyQt6', 
    'IPython', 'jupyter', 'matplotlib.tests', 'numpy.tests', 
    'pandas.tests', 'scipy', 'scipy.tests', 'setuptools.tests',
    'distutils.tests', '_posixshmem', 'resource', 'fcntl',
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
    'icon-removebg-preview.ico', 'financial_forensics.py', 'install_dependencies.sh', 'install_dependencies.bat', 'dependency_checker.py',
    'crypto_engine.py', 'integrity_monitor.py', 'recon.py', 'recon_full.py', 'install_dsterminal.py',
    'vt_scan.py', 'edu_typing_engine.py', 'soc_nmap_dashboard.py',
    'deletion_protection.py', 'hardening_dashboard.py', 'dst_footer.py', 'telemetry_engine.py', 'setupt.sh', 'setupt.bat',
    'install_nmap.ps1', 'install_python_packages.ps1', 'check_dependencies.ps1', 'install_metasploit.ps1', 'install_metasploit_wsl.ps1', 'install_all_dependencies.ps1',
    'install_nmap.bat', 'install_remaining_deps.ps1', 'install_remaining_deps.bat', 'check_deps.bat', 'install_chocolatey.ps1',
    'install_whois.ps1', 'install_sqlmap.ps1', 'install_nmap_admin.ps1', 'install_dsterminal.py',
]

for file in files:
    if os.path.exists(file):
        datas.append((file, '.'))

# Comprehensive hidden imports for all DSTerminal functionality
hiddenimports = [
    # Rich Console & UI
    'rich', 'rich.console', 'rich.panel', 'rich.align', 'rich.table',
    'rich.live', 'rich.layout', 'rich.progress', 'rich.syntax', 'rich.traceback',
    'rich.markdown', 'rich.columns', 'rich.tree', 'rich.prompt', 'rich.status',
    'rich.box', 'rich.text', 'rich.style', 'rich.color', 'rich.theme',
    'rich.segment', 'rich.measure', 'rich.padding', 'rich.control', 'unittest',
    'unittest.mock', 'unittest.case', 'unittest.suite',
    'unittest.loader', 'unittest.runner', 'unittest.result',
    'matplotlib', 
    'matplotlib.pyplot',
    'matplotlib.backends',
    'matplotlib.backends.backend_agg',
    'matplotlib.figure',
    'matplotlib.patches',
    'matplotlib.lines',
    'matplotlib.text',
    'matplotlib.collections',
    'matplotlib.path',
    'matplotlib.transforms',
    'matplotlib.axes',
    'matplotlib.axis',
    'matplotlib.spines',
    'matplotlib.legend',
    'matplotlib.ticker',
    'matplotlib.gridspec',
    'matplotlib.colors',
    'matplotlib.cm',
    'matplotlib.markers',
    'matplotlib.font_manager',
    'matplotlib.rcsetup',
    
    # Colorama for cross-platform colors
    'colorama', 'colorama.initialise', 'colorama.ansitowin32',
    
    # Core Python libraries
    'json', 'os', 'sys', 'time', 'random', 'datetime', 'threading',
    'pathlib', 'shutil', 'platform', 'subprocess', 'hashlib', 'base64',
    'logging', 're', 'collections', 'itertools', 'functools', 'glob',
    'tempfile', 'io', 'abc', 'weakref', 'copy', 'math', 'string',
    'typing', 'enum', 'dataclasses', 'contextlib', 'signal', 'atexit',
    
    # Network & Web
    'requests', 'requests.packages', 'requests.packages.urllib3',
    'urllib3', 'urllib.parse', 'socket', 'ssl', 'http.client', 'http.server',
    'webbrowser', 'email', 'email.mime', 'email.mime.text', 'email.mime.multipart',
    'smtplib', 'ftplib', 'telnetlib',
    
    # Data Processing
    'psutil', 'psutil._psutil_windows', 'psutil._common',
    
    # Reporting & PDF
    'fpdf', 'fpdf2', 'fpdf.enums', 'fpdf.table', 'fpdf.fonts',
    'reportlab', 'reportlab.pdfgen', 'reportlab.lib.pagesizes', 'reportlab.lib.units',
    'reportlab.lib.colors', 'reportlab.platypus', 'reportlab.platypus.tables',
    'reportlab.pdfbase', 'reportlab.pdfbase.pdfmetrics',
    
    # File System & Operations
    'shutil', 'filecmp', 'stat', 'fnmatch', 'pickle', 'shelve',
    
    # Windows Specific
    'win32api', 'win32com', 'win32com.client', 'win32com.shell', 'win32com.shell.shell',
    'win32ctypes', 'win32ctypes.pywin32', 'win32ctypes.pywin32.win32api',
    'win32security', 'win32file', 'win32con', 'win32process', 'win32event',
    'win32gui', 'win32ui', 'ctypes', 'ctypes.wintypes',
    
    # Terminal & Progress Bars
    'tqdm', 'tqdm.std', 'tqdm.rich', 'tqdm.asyncio',
    'prompt_toolkit', 'prompt_toolkit.shortcuts', 'prompt_toolkit.styles',
    'pyfiglet', 'pyfiglet.fonts',
    
    # Cryptography & Security
    'cryptography', 'cryptography.hazmat', 'cryptography.hazmat.primitives',
    'cryptography.hazmat.primitives.ciphers', 'cryptography.hazmat.primitives.hashes',
    'cryptography.hazmat.backends', 'cryptography.hazmat.backends.openssl',
    'cryptography.hazmat.primitives.asymmetric', 'cryptography.hazmat.primitives.kdf',
    'hashlib', 'hmac', 'secrets',
    
    # Web Scraping & APIs
    'urllib3', 'urllib3.poolmanager', 'urllib3.util', 'urllib3.util.retry',
    'json.decoder', 'json.encoder',
    
    # GUI & Dialog (for file dialogs)
    'tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox',
    'tkinter.simpledialog', 'tkinter.scrolledtext', 'tkinter.colorchooser',
    
    # Syntax Highlighting
    'pygments', 'pygments.lexers', 'pygments.formatters', 'pygments.styles',
    
    # Textual UI (if used)
    'textual', 'textual.app', 'textual.widgets', 'textual.containers',
    'textual.screen', 'textual.events', 'textual.messages',
    
    # Animation & Visual Effects
    'ascii_magic', 'ascii_magic._ascii_magic',
    
    # Financial Forensics specific
    'financial_forensics', 'crypto_engine', 'integrity_monitor',
    'recon', 'recon_full', 'vt_scan', 'edu_typing_engine',
    'deletion_protection',
    
    # Networking Tools
    'socket', 'ipaddress', 'dnspython', 'dns', 'dns.resolver',
    
    # Compression (if needed)
    'zipfile', 'tarfile', 'gzip', 'bz2', 'lzma',
    
    # XML/HTML Processing
    'xml', 'xml.etree', 'xml.etree.ElementTree', 'html', 'html.parser',
    
    # Date/Time
    'calendar', 'zoneinfo',
    
    # System Information
    'platform', 'sysconfig', 'site',
    
    # Additional Windows-specific
    'winreg', 'msvcrt', '_winapi',
]

# Collect hidden submodules from key packages
try:
    hiddenimports.extend(collect_submodules('rich'))
    hiddenimports.extend(collect_submodules('psutil'))
    hiddenimports.extend(collect_submodules('reportlab'))
except:
    pass

a = Analysis(
    ['dsterminal.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
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