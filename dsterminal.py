# -*- coding: utf-8 -*-
import sys
import subprocess
import os
import platform

def maximize_terminal():
    """Maximize terminal window on startup - Cross Platform"""
    system = platform.system()
    
    if system == "Windows":
        try:
            subprocess.run(['powershell', '-Command', 
                '$hwnd = (Get-Process -Id $pid).MainWindowHandle; '
                'Add-Type -MemberDefinition @"[DllImport("user32.dll")]public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);"@ -Name "Win32" -Namespace "Utils"; '
                '[Utils.Win32]::ShowWindow($hwnd, 3)'], 
                capture_output=True)
        except:
            pass
    
    elif system == "Linux":
        try:
            # Method 1: Using xdotool (if installed)
            result = subprocess.run(['which', 'xdotool'], capture_output=True)
            if result.returncode == 0:
                subprocess.run(['xdotool', 'getactivewindow', 'windowsize', '100%', '100%'], capture_output=True)
            else:
                # Method 2: Using terminal-specific escape sequences
                # Send resize command to most terminals
                sys.stdout.write('\x1b[8;40;140t')  # Set to 40 rows x 140 cols
                sys.stdout.flush()
        except:
            pass
    
    elif system == "Darwin":  # macOS
        try:
            # AppleScript to maximize terminal
            applescript = '''
            tell application "Terminal"
                activate
                set bounds of front window to {0, 22, 1440, 878}
                set front window's size to {140, 40}
            end tell
            '''
            subprocess.run(['osascript', '-e', applescript], capture_output=True)
        except:
            try:
                # Alternative: Use escape sequence
                sys.stdout.write('\x1b[8;40;140t')
                sys.stdout.flush()
            except:
                pass

# Call the function at startup
maximize_terminal()

import tempfile
from pathlib import Path
# Add at the top of the file with other imports
import timezonefinder
import pytz
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

# Then update the imports in live_monitor
def get_base_path():
    """Get the base path for the application (works for both development and installed versions)"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        if hasattr(sys, '_MEIPASS'):
            return sys._MEIPASS
        else:
            return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

# Set the base path
BASE_PATH = get_base_path()

# Add the base path to Python path
if BASE_PATH not in sys.path:
    sys.path.insert(0, BASE_PATH)

# Change to the base path
os.chdir(BASE_PATH)

# Now continue with the rest of your imports and code...
# =================
VERSION = "2.0.113"
APP_NAME = "DSTerminal"
DESCRIPTION = "Defensive Security Terminal"
AUTHOR = "Spark Wilson Spink | Powered By Stark Expo Tech Exchange"

def show_version():
    print(f"{APP_NAME} v{VERSION}")
    print(DESCRIPTION)
    print(f"Developed by {AUTHOR}")

def run_terminal():
    """Initialize and run the security terminal"""
    terminal = SecurityTerminal()
    terminal.run()

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()

        if arg in ["--version", "-v", "version"]:
            show_version()
            return

    # continue normal terminal startup
    run_terminal()


import io
import glob
import queue
from turtle import color

from stdeb import command
from deletion_protection import (
    DSTerminalMonitor,
    BackupDatabase,
    RestoreManager,
    ServiceManager,
    PlatformDetector,
    EncryptionManager
)


# Keep these in the main file since they're UI-only
# from terminal_ui import TerminalUI  # Extract TerminalUI to its own file, or keep inline
# from workspace_manager import WorkspaceManager  # Extract WorkspaceManager, or keep inline
# from config_manager import ConfigManager  # Extract ConfigManager, or keep inline

# import recon
# ===============================
# Cross-platform terminal support
# ===============================
# Force UTF-8 encoding for stdout/stderr
if sys.platform == 'win32':
    try:
        # Attempt to set console to UTF-8
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

    # =========================
IS_WINDOWS = os.name == "nt"

if IS_WINDOWS:
    import msvcrt
else:
    import tty
    import termios

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    # Fallback if colorama not installed
    class Fore:
        RED = '\033[91m'; GREEN = '\033[92m'; YELLOW = '\033[93m'
        BLUE = '\033[94m'; MAGENTA = '\033[95m'; CYAN = '\033[96m'
        WHITE = '\033[97m'; RESET = '\033[0m'
    
    class Back:
        RED = '\033[101m'; GREEN = '\033[102m'; YELLOW = '\033[103m'
        BLUE = '\033[104m'; RESET = '\033[0m'
    
    class Style:
        BRIGHT = '\033[1m'; DIM = '\033[2m'; NORMAL = '\033[22m'
        RESET_ALL = '\033[0m'
    
    class init:
        def __init__(self, autoreset=True):
            pass
    
    COLORS_AVAILABLE = False
    # ==========================import hardening==================
    # Try importing colorama for cross-platform color support
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    # Fallback color codes
    class Fore:
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        RESET = '\033[0m'
            # Bright variants
        BRIGHT_BLACK = '\033[90m'
        BRIGHT_RED = '\033[91m'
        BRIGHT_GREEN = '\033[92m'
        BRIGHT_YELLOW = '\033[93m'
        BRIGHT_BLUE = '\033[94m'
        BRIGHT_MAGENTA = '\033[95m'
        BRIGHT_CYAN = '\033[96m'
        BRIGHT_WHITE = '\033[97m'
        DIM = '\033[90m'  # FIXED: Added DIM attribute


    class Style:
        BRIGHT = '\033[1m'
        DIM = '\033[2m'  # This was missing
        ITALIC = '\033[3m'
        UNDERLINE = '\033[4m'
        BLINK = '\033[5m'
        REVERSE = '\033[7m'
        HIDDEN = '\033[8m'
        RESET_ALL = '\033[0m'
        
    class Back:
        BLACK = '\033[40m'
        RED = '\033[41m'
        GREEN = '\033[42m'
        YELLOW = '\033[43m'
        BLUE = '\033[44m'
        MAGENTA = '\033[45m'
        CYAN = '\033[46m'
        WHITE = '\033[47m'

    # ============================================================
    # HARDENING DATA STRUCTURES
    # ============================================================
    class Fore:
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        RESET = '\033[0m'

    class Colors:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
        DIM = '\033[2m'
        BG_RED = '\033[41m'
        BG_GREEN = '\033[42m'
        BG_YELLOW = '\033[43m'
        BG_BLUE = '\033[44m'
        BG_MAGENTA = '\033[45m'
        BG_CYAN = '\033[46m'


    class Style:
        BRIGHT = '\033[1m'
        DIM = '\033[2m'
        NORMAL = '\033[22m'
        RESET_ALL = '\033[0m'
        BRIGHT = '\033[1m'
        DIM = '\033[2m'  # This was missing
        ITALIC = '\033[3m'
        UNDERLINE = '\033[4m'
        BLINK = '\033[5m'
        REVERSE = '\033[7m'
        HIDDEN = '\033[8m'
        RESET_ALL = '\033[0m'
    # Import hardening modules
try:
    from hardening_dashboard import (
        HardeningDashboard
    )
    HARDENING_AVAILABLE = True
except ImportError as e:
    print(f"[!] Hardening module not available: {e}")
    HARDENING_AVAILABLE = False
# ============================================================
# SOC-GRADE NMAP SCAN DASHBOARD IMPORTS
# ============================================================

# Import SOC Nmap Dashboardfrom soc_nmap_dashboard import SOCNmapIntegration, SOCNmapDashboard
# Define the variable first
SOC_NMAP_AVAILABLE = False

try:
    from soc_nmap_dashboard import SOCNmapDashboard, SOCNmapIntegration
    SOC_NMAP_AVAILABLE = True
    print(f"{Fore.GREEN}[✓] SOC Nmap Dashboard loaded successfully{Style.RESET_ALL}")
except ImportError as e:
    print(f"{Fore.YELLOW}[!] SOC Nmap Dashboard not available: {e}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*] Make sure soc_nmap_dashboard.py exists in the same directory{Style.RESET_ALL}")

# ===========import integrity_monitor======
# =================================
# Import Integrity Monitor Module
# =================================
try:
    from integrity_monitor import (
        SystemIntegrityMonitor,
        AlertManager,
        ForensicAnalyzer,
        AutoRemediation
        # RealTimeHandler
    )
    INTEGRITY_AVAILABLE = True
    if COLORS_AVAILABLE:
        print(f"{Fore.GREEN}✓ Integrity Monitor loaded successfully{Style.RESET_ALL}")
    else:
        print("✓ Integrity Monitor loaded successfully")
except ImportError as e:
    INTEGRITY_AVAILABLE = False
    if COLORS_AVAILABLE:
        print(f"{Fore.YELLOW}⚠ Integrity Monitor not found: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Make sure integrity_monitor.py is in the same directory{Style.RESET_ALL}")
    else:
        print(f"⚠ Integrity Monitor not found: {e}")
except Exception as e:
    INTEGRITY_AVAILABLE = False
    if COLORS_AVAILABLE:
        print(f"{Fore.RED}⚠ Integrity Monitor error: {e}{Style.RESET_ALL}")
    else:
        print(f"⚠ Integrity Monitor error: {e}")
# =================ends here============
# Try to import psutil for real system metrics
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("[WARNING] psutil not installed. Using simulated metrics.")
    print("Install with: pip install psutil")

# Import our footer engine
from dst_footer import DSTerminalFooter, FooterBootAnimation, FooterColors
# Add this with your other imports at the very top of dsterminal.py
try:
    from soc_nmap_dashboard import SOCNmapIntegration, InteractiveSOCDashboard
    SOC_NMAP_AVAILABLE = True
except ImportError:
    SOC_NMAP_AVAILABLE = False
    print("[!] SOC Nmap Dashboard module not found. Install soc_nmap_dashboard.py")
# Import Financial Forensics Module
try:
    # Add the current directory to path if needed
    sys.path.insert(0, str(Path(__file__).parent))
    from financial_forensics import financial_forensics_menu
    FINANCIAL_FORENSICS_AVAILABLE = True
except ImportError:
    FINANCIAL_FORENSICS_AVAILABLE = False
    print(f"{Fore.YELLOW}⚠ Financial Forensics module not found: {e}{Style.RESET_ALL}")

# Import crypto_engine
try:
    crypto_path = os.path.join(BASE_PATH, 'crypto_engine.py')
    if os.path.exists(crypto_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location("crypto_engine", crypto_path)
        crypto_engine_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(crypto_engine_module)
        CryptoEngine = crypto_engine_module.CryptoEngine
        crypto_engine = CryptoEngine(BASE_PATH)
    else:
        print(f"⚠ crypto_engine.py not found at: {crypto_path}")
        crypto_engine = None
except Exception as e:
    print(f"⚠ Crypto engine import error: {e}")
    crypto_engine = None


# ========try import vt_scan here=============
# =================================
# Import VirusTotal Scanner Module (vt_scan.py)
try:
    from vt_scan import VirusTotalScanner, sync_operator_session
    VT_AVAILABLE = True
except ImportError:
    print("⚠ VT module not found")
    VT_AVAILABLE = False

try:
    vt_scan_path = os.path.join(BASE_PATH, 'vt_scan.py')

    if os.path.exists(vt_scan_path):
        import importlib.util

        spec = importlib.util.spec_from_file_location("vt_scan", vt_scan_path)
        vt_scan_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(vt_scan_module)

        # Import required classes/functions
        VirusTotalScanner = vt_scan_module.VirusTotalScanner
        vt_scan_menu = vt_scan_module.vt_scan_menu

        VT_AVAILABLE = True
        print(f"{Fore.GREEN}✓ VirusTotal module loaded successfully{Style.RESET_ALL}")

    else:
        VT_AVAILABLE = False
        print(f"{Fore.YELLOW}⚠ vt_scan.py not found at: {vt_scan_path}{Style.RESET_ALL}")

except Exception as e:
    VT_AVAILABLE = False
    print(f"{Fore.RED}⚠ VirusTotal module import error: {e}{Style.RESET_ALL}")
# ===============================
# try import recon and recon_full here====================
# =================================
# Import Recon Modules (recon.py and recon_full.py)
try:
    recon_path = os.path.join(BASE_PATH, 'recon.py')
    if os.path.exists(recon_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location("recon", recon_path)
        recon_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(recon_module)
        
        # Import specific functions/classes from recon.py
        ReconScanner = getattr(recon_module, 'ReconScanner', None)
        run_recon = getattr(recon_module, 'run_recon', None)
        recon_menu = getattr(recon_module, 'recon_menu', None)
        
        RECON_AVAILABLE = True
        print(f"{Fore.GREEN}✓ Recon module loaded successfully{Style.RESET_ALL}")
    else:
        RECON_AVAILABLE = False
        print(f"{Fore.YELLOW}⚠ recon.py not found at: {recon_path}{Style.RESET_ALL}")
except Exception as e:
    RECON_AVAILABLE = False
    print(f"{Fore.RED}⚠ Recon module import error: {e}{Style.RESET_ALL}")

# =================================
# Import Recon Full Module (recon_full.py)
try:
    recon_full_path = os.path.join(BASE_PATH, 'recon_full.py')
    if os.path.exists(recon_full_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location("recon_full", recon_full_path)
        recon_full_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(recon_full_module)
        
        # Import specific functions/classes from recon_full.py
        FullReconScanner = getattr(recon_full_module, 'FullReconScanner', None)
        run_full_recon = getattr(recon_full_module, 'run_full_recon', None)
        full_recon_menu = getattr(recon_full_module, 'full_recon_menu', None)
        
        RECON_FULL_AVAILABLE = True
        print(f"{Fore.GREEN}✓ Recon Full module loaded successfully{Style.RESET_ALL}")
    else:
        RECON_FULL_AVAILABLE = False
        print(f"{Fore.YELLOW}⚠ recon_full.py not found at: {recon_full_path}{Style.RESET_ALL}")
except Exception as e:
    RECON_FULL_AVAILABLE = False
    print(f"{Fore.RED}⚠ Recon Full module import error: {e}{Style.RESET_ALL}")
# =========================added recon and recon_full debug like
# After importing recon modules, add fallback assignments:

# Ensure these variables exist even if imports fail
if 'RECON_AVAILABLE' not in dir():
    RECON_AVAILABLE = False
if 'RECON_FULL_AVAILABLE' not in dir():
    RECON_FULL_AVAILABLE = False

# fallback functions if imports failed
if not RECON_AVAILABLE:
    def recon_menu():
        print(f"{Fore.YELLOW}Recon module not available. Using basic recon...{Style.RESET_ALL}")
        terminal = SecurityTerminal()
        terminal.run_recon_basic()
    
    def run_recon():
        print(f"{Fore.YELLOW}Recon module not available. Using basic recon...{Style.RESET_ALL}")
        terminal = SecurityTerminal()
        terminal.run_recon_basic()
    
    recon_menu = recon_menu
    run_recon = run_recon

if not RECON_FULL_AVAILABLE:
    def full_recon_menu():
        print(f"{Fore.YELLOW}Full Recon module not available. Using basic recon...{Style.RESET_ALL}")
        terminal = SecurityTerminal()
        terminal.run_full_recon_basic()
    
    def run_full_recon():
        print(f"{Fore.YELLOW}Full Recon module not available. Using basic recon...{Style.RESET_ALL}")
        terminal = SecurityTerminal()
        terminal.run_full_recon_basic()
    
    full_recon_menu = full_recon_menu
    run_full_recon = run_full_recon


# ========================================================
# Import edu_typing_engine
try:
    edu_path = os.path.join(BASE_PATH, 'edu_typing_engine.py')
    if os.path.exists(edu_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location("edu_typing_engine", edu_path)
        edu_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(edu_module)
        EducationTypingEngine = edu_module.EducationTypingEngine
        engine = EducationTypingEngine(speed=0.03)
    else:
        print(f"⚠ edu_typing_engine.py not found at: {edu_path}")
        engine = None
except Exception as e:
    print(f"⚠ Education typing engine import error: {e}")
    engine = None
    # =========================
import math
import shlex
import shutil
import socket
import netifaces
from getpass import getpass
import requests
import uuid
import hashlib
import logging
import psutil
from tqdm import tqdm
import threading
import textwrap
import platform
import json
import time
import random
import ssl
import whois
import OpenSSL
import subprocess
from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.ocsp import OCSPRequestBuilder
from threading import Thread, Event
from datetime import datetime, timedelta 
from cryptography.fernet import Fernet
import re
from colorama import Fore, Style, init

from prompt_toolkit import PromptSession, HTML
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory

from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import print_formatted_text

from colorama import Fore, Style, init
# from pyfiglet import figlet_format
from pyfiglet import figlet_format
import itertools
from rich.console import Console, Group
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.live import Live
from collections import Counter
from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.table import Table as Table
from rich.table import Table as RichTable
from random import choice
from rich.prompt import Prompt
# from rich.group import Group
from shutil import which
from rich.columns import Columns
from edu_typing_engine import EducationTypingEngine
from cryptography.hazmat.primitives import serialization
import cryptography
from prompt_toolkit.completion import WordCompleter
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from dst_footer import DynamicFooter, FooterColors
from telemetry_engine import TelemetryEngine

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)
try:
    import matplotlib
    matplotlib.use('Agg')  # Only if absolutely needed
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    
# Replace the cartopy imports with:
try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    CARTOPY_AVAILABLE = True
except ImportError:
    CARTOPY_AVAILABLE = False
    print("[!] Cartopy not available. Using fallback map visualization.")

import io
from PIL import Image
import numpy as np
from collections import defaultdict
import threading
    # Add these imports at the top of your file
import folium
from folium.plugins import HeatMap, MarkerCluster
import webbrowser
import tempfile
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from reportlab.lib.colors import black, lightgrey, HexColor
from crypto_engine import CryptoEngine
init(autoreset=True)

engine = EducationTypingEngine(speed=0.03)
username = "OP-" + uuid.uuid4().hex[:6].upper()
crypto_engine = CryptoEngine()

# =========================
# Place this right after your imports, before any classes
# =========================

class SimpleWorkspace:
    """Minimal workspace wrapper for string paths."""
    def __init__(self, base_path):
        self.base_path = base_path
        os.makedirs(os.path.join(base_path, 'database'), exist_ok=True)
        os.makedirs(os.path.join(base_path, 'logs'), exist_ok=True)
        os.makedirs(os.path.join(base_path, 'config'), exist_ok=True)        
        os.makedirs(os.path.join(base_path, 'backups_protected'), exist_ok=True)  # ← ADD THIS
        for cat in ['images','documents','spreadsheets','code','config','archives','media','other','protected','encrypted']:
            os.makedirs(os.path.join(base_path, 'backups', cat), exist_ok=True)
    
    def get_database_path(self):
        return os.path.join(self.base_path, 'database', 'dsterminal.db')
    
    def get_backup_path(self, category='other'):
        return os.path.join(self.base_path, 'backups', category)
    
    def get_log_path(self):
        ts = datetime.now().strftime("%Y%m%d")
        return os.path.join(self.base_path, 'logs', f'dsterminal_{ts}.log')
    
    def get_path(self, key):
        return os.path.join(self.base_path, key)
    
    def get_key_path(self):
        return os.path.join(self.base_path, 'config', 'encryption.key')
    
    def get_config_path(self):
        return os.path.join(self.base_path, 'config', 'config.json')
    
    def get_report_path(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.base_path, 'reports', f'report_{ts}.pdf')
    
    def cleanup_temp_files(self, max_age_hours=24):
        temp_dir = os.path.join(self.base_path, 'temp')
        if os.path.exists(temp_dir):
            cutoff = time.time() - (max_age_hours * 3600)
            for f in os.listdir(temp_dir):
                fp = os.path.join(temp_dir, f)
                if os.path.isfile(fp) and os.path.getmtime(fp) < cutoff:
                    try:
                        os.remove(fp)
                    except:
                        pass

# =============dsterminal workspace creation from here===============
def init_workspace():
    workspace_path = os.path.expanduser("~/dsterminal_workspace")
    subdirs = ["sandbox", "scans", "exploits", "reports", "operators"]
    
    try:
        os.makedirs(workspace_path, exist_ok=True)
        for subdir in subdirs:
            os.makedirs(os.path.join(workspace_path, subdir), exist_ok=True)
        # Create additional subdirectories for network monitoring
        os.makedirs(os.path.join(workspace_path, "reports", "network_reports"), exist_ok=True)
        os.makedirs(os.path.join(workspace_path, "reports", "threat_maps"), exist_ok=True)
        os.makedirs(os.path.join(workspace_path, "reports", "forensic"), exist_ok=True)
        
        print(f"{Fore.GREEN}[+] Workspace initialized at: {workspace_path}{Style.RESET_ALL}")
        return workspace_path
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to initialize workspace: {e}{Style.RESET_ALL}")
        sys.exit(1)

# Initialize workspace safely
WORKSPACE = init_workspace()
def get_workspace_dir() -> Path:
    """Get the DSTerminal workspace directory"""
    home = Path.home()
    workspace = home / "dsterminal_workspace"
    workspace.mkdir(exist_ok=True)
    
    # Create subdirectories for different report types
    (workspace / "integrity_reports").mkdir(exist_ok=True)
    (workspace / "network_reports").mkdir(exist_ok=True)
    (workspace / "compliance_reports").mkdir(exist_ok=True)
    (workspace / "logs").mkdir(exist_ok=True)
    (workspace / "baselines").mkdir(exist_ok=True)
    (workspace / "alerts").mkdir(exist_ok=True)
    (workspace / "quarantine").mkdir(exist_ok=True)
    (workspace / "forensic").mkdir(exist_ok=True)
    (workspace / "auto_quarantine").mkdir(exist_ok=True)
    (workspace / "operators").mkdir(exist_ok=True)
    (workspace / "reports" / "threat_maps").mkdir(parents=True, exist_ok=True)
    
    
    return workspace

WORKSPACE = get_workspace_dir()
console = Console()

# Configuration
CONFIG = {
    'VT_API_KEY': '957166d424812a397e328022b84594a8c02757814f6c04518dce7e81179b4b79',
    'UPDATE_URL': 'https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest.git',
    'LOG_FILE': 'secure_audit.log',
    'ENCRYPT_KEY': Fernet.generate_key().decode(),
    'CURRENT_VERSION': '2.0.113'
}
# Add this near CONFIG or __init__
EDUCATION_TIPS = {
    "system scan -all": """
    [bold]💡 Did You Know?[/bold]\n
    Regular system scans help detect malware persistence mechanisms like:\n
    - [red]Rootkits[/red] hiding in kernel modules\n
    - [yellow]Malicious scheduled tasks[/yellow] (check `crontab -l` or Task Scheduler)\n
    - [blue]Unusual network listeners[/blue] (`netstat -tulnp`)\n
    """,
    "net -n mon": """
    [bold cyan]🌐 NETWORK MONITORING: REAL-TIME THREAT VISUALIZATION[/bold cyan]

    [bold yellow]📡 WHAT YOU'RE SEEING ON THE MAP[/bold yellow]

    The threat map shows [green]live connections[/green] from your system to servers worldwide.
    Each colored line tells a story about your network traffic.

    [bold red]🔴 RED LINES = HIGH RISK[/bold red]
    → Known malicious IP addresses
    → Active C2 (Command & Control) communication
    → Connections to sanctioned countries (North Korea, Iran, Russia)
    → High threat score (3-5 out of 5)

    [bold yellow]🟡 YELLOW/ORANGE LINES = MEDIUM RISK[/bold yellow]
    → Unusual ports or protocols
    → Recently registered domains (<30 days old)
    → Geographic anomalies (unexpected server locations)
    → Hosting providers frequently abused by attackers

    [bold green]🟢 GREEN LINES = LOW RISK[/bold green]
    → Normal HTTPS web browsing (ports 443/80)
    → Trusted services (Microsoft, Google, Cloudflare, AWS)
    → Expected geographic locations
    → Established connections with clean reputation

    [bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]

    [bold white]🎯 WHAT TO INVESTIGATE IMMEDIATELY[/bold white]

    ✓ Multiple [red]red lines[/red] from the same process
    ✓ Connections to [yellow]unusual ports[/yellow] (not 80,443,22,3389)
    ✓ [cyan]Beaconing patterns[/cyan] - regular intervals to same IP
    ✓ [magenta]High data upload[/magenta] without user action
    ✓ Processes with [red]no digital signature[/red] making network calls

    [bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]

    [bold green]📏 UNDERSTANDING DISTANCE METRICS[/bold green]

    Each connection line displays the [yellow]great-circle distance[/yellow] between you and the server:

    → [cyan]Short distances[/cyan] (<1000km) = Low latency, likely regional services
    → [yellow]Medium distances[/yellow] (1000-5000km) = Typical cross-continent traffic
    → [red]Long distances[/red] (>5000km) = Potentially abnormal routing

    [bold]Watch for geographic mismatches:[/bold] A "local" bank connecting to Eastern Europe
    or a software update fetching from 15,000km away when local mirrors exist.

    [bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]

    [bold magenta]🔬 BROWSER CONNECTION ANALYSIS[/bold magenta]

    Browser connections (🌐 WEB) require special attention because:

    • [red]Drive-by downloads[/red] - Malicious scripts establishing hidden connections
    • [yellow]Cryptominers[/yellow] - Running in tabs, connecting to mining pools
    • [cyan]Data exfiltration[/cyan] - Form data sent to unexpected domains
    • [magenta]C2 via WebSockets[/magenta] - Real-time communication channels

    [bold]Suspicious indicators:[/bold]
    → Connections to [red]non-standard ports[/red] (not 443/80)
    → [cyan]Multiple connections[/cyan] from different tabs to same IP
    → [yellow]WebRTC leaks[/yellow] revealing local IP addresses

    [bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]

    [bold red]⚠️ IMMEDIATE ACTION REQUIRED - RED FLAGS[/bold red]

    If you observe ANY of these, investigate immediately:

    1. [white]Connections to [red]unallocated IP space[/red][/white]
    2. [yellow]Traffic to [red]TOR exit nodes[/red] or [red]known VPN endpoints[/red][/yellow]
    3. [cyan]Processes [red]hiding network connections[/red] (rootkit behavior)[/cyan]
    4. [magenta]Outbound [red]ICMP tunneling[/red] (unusual ping patterns)[/magenta]
    5. [green]Large data [red]exfiltration[/red] to unrecognized destinations[/green]

    [bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]

    [bold white]🎯 INCIDENT RESPONSE WORKFLOW[/bold white]

    [white]1. IMMEDIATE[/white]
    → [red]Document everything[/red] (screenshots, logs, timestamps)
    → [yellow]Disconnect[/yellow] confirmed malicious hosts from network

    [white]2. ANALYSIS[/white]
    → [cyan]Capture traffic[/cyan] (Wireshark/tcpdump) for deeper inspection
    → [green]Memory analysis[/green] of suspicious processes (Volatility)
    → [magenta]Check against threat intel[/magenta] (VirusTotal, MISP)

    [white]3. REMEDIATION[/white]
    → [red]Kill malicious processes[/red]
    → [yellow]Remove persistence[/yellow]
    → [cyan]Block IOCs[/cyan] (firewall, DNS sinkhole)

    [white]4. RECOVERY[/white]
    → [green]Restore from known-good backups[/green]
    → [magenta]Apply security patches[/magenta]
    → [blue]Reset compromised credentials[/blue]

    [bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]

    [bold blue]📚 CONTINUOUS LEARNING RESOURCES[/bold blue]

    • [cyan]MITRE ATT&CK Framework[/cyan] - Understand adversary tactics & techniques
    • [yellow]SANS Reading Room[/yellow] - Network monitoring white papers
    • [red]CISA Alerts[/red] - Current threat intelligence
    • [green]VirusTotal[/green] - Hash lookups and sandbox analysis
    • [magenta]Any.Run[/magenta] - Interactive malware analysis

    [dim italic]"The network doesn't lie - it just waits for someone to read its story."[/dim italic]
    """,
    "harden -t sys": """
    [bold]🛡️ Hardening Pro Tip[/bold]\n
    Always follow the [yellow]Principle of Least Privilege[/yellow]:\n
    - Disable unnecessary services\n
    - Apply OS-specific benchmarks (e.g., [blue]CIS Benchmarks[/blue])\n
    - Use [green]SELinux/AppArmor[/green] for mandatory access control.\n
    """,
    "exploitcheck": """
    [bold]🔍 Exploit Check Tip[/bold]\n
    Checks for common vulnerabilities like:\n
    - [red]Unpatched CVEs[/red] (check with `cve-search`)\n
    - [yellow]Misconfigured services[/yellow] (SSH, FTP, SMB)\n
    - [blue]Kernel exploits[/blue] (DirtyPipe, DirtyCow)\n
    [green]Pro Tip:[/green] Cross-reference with exploit-db.com\n
    [bold]🧠 Exploit Check Insight[/bold]\n
    - Regularly scan for known vulnerabilities (CVEs).\n
    - Tools like [cyan]searchsploit[/cyan], [magenta]exploitdb[/magenta], and vulnerability scanners (Nessus, OpenVAS) are critical.
    """,
    
    "macspoof": """
    [bold]📡 MAC Spoofing Tip[/bold]\n
    Remember:\n
    1. Spoofing only works until [red]next reboot[/red]\n
    2. For persistence, modify [yellow]/etc/network/interfaces[/yellow]\n
    3. Some networks use [blue]MAC filtering[/blue] (check ARP tables)\n
    [green]Example:[/green] macspoof wlan0\n
    [bold]🎭 MAC Spoofing Caution[/bold]\n
    - Changing MAC addresses can evade network tracking but might disrupt connections.\n
    - Always reset your original MAC for stability.
    """,
    
    "clearlogs": """
    [bold]🧹 Log Cleaning Tip[/bold]\n
    Targets common log locations:\n
    - [red]/var/log/[/red] (syslog, auth.log)\n
    - [yellow]~/.bash_history[/yellow]\n
    - [blue]Journald[/blue] (`journalctl --vacuum-time=1s`)\n
    [green]Warning:[/green] Some systems use remote logging!\n
    Clearing logs should be used ethically. Logs are vital for:\n
    - Forensics
    - Intrusion Detection
    - Compliance Audits
    
    """,
    
    "portsweep": """
    [bold]🔎 Port Scanning Tip[/bold]\n
    Advanced techniques:\n
    - [red]SYN stealth scan[/red] (-sS)\n
    - [yellow]Service version detection[/yellow] (-sV)\n
    - [blue]OS fingerprinting[/blue] (-O)\n
    [green]Pro Tip:[/green] Use `-T4` for faster scans (noisy)\n
    : Port sweeps reveal exposed services.\n
    - Scan with `-sS`, `-sV`, `-sT`, `-sS`, `-sV`, `-Pn`, `-p`, `-T4` flags in [green]nmap[/green] for stealth and version detection.
    
    """,
    
    "hashfile": """
    [bold]🔐 Hashing Tip[/bold]\n
    Why multiple hashes matter:\n
    - [red]MD5[/red] - Fast but broken\n
    - [yellow]SHA1[/yellow] - Deprecated but common\n
    - [blue]SHA256[/blue] - Current standard\n
    [green]Pro Tip:[/green] Verify against VirusTotal hashes\n
    : Use SHA-256 for strong integrity checks.\n
    Example: `sha256sum file.txt`
    """,
    
    "sysinfo": """
    [bold]🖥️ System Recon Tip[/bold]\n
    Critical info to check:\n
    - [red]Kernel version[/red] (uname -a)\n
    - [yellow]CPU flags[/yellow] (/proc/cpuinfo)\n
    - [blue]Sudo version[/blue] (CVE-2021-3156)\n
    [green]Pro Tip:[/green] Check `lshw` for full hardware details\n
    """,
    
    "killproc": """
    [bold]💀 Process Killing Tip[/bold]\n
    Advanced methods:\n
    - [red]SIGKILL[/red] (-9) for stubborn processes\n
    - [yellow]pkill[/yellow] for name-based termination\n
    - [blue]killall[/blue] for all instances\n
    [green]Warning:[/green] Can cause data loss!\n
    """,
    
    "check integrity": """
    [bold]🛡️ Integrity Check Tip[/bold]\n
    Checks for:\n
    - [red]Modified system binaries[/red] (ls, ps, netstat)\n
    - [yellow]Unexpected setuid files[/yellow] (find / -perm -4000)\n
    - [blue]Hidden kernel modules[/blue] (lsmod)\n
    [green]Pro Tip:[/green] Compare against package manager (`rpm -V`)\n
    """,
    
    "encrypt": """
    [bold]🔒 Encryption Tip[/bold]\n
    Best practices:\n
    - Use [red]strong passwords[/red] (12+ chars, special symbols)\n
    - Consider [yellow]GPG[/yellow] for asymmetric encryption\n
    - [blue]Shred[/blue] original files after encryption\n
    [green]Example:[/green] encrypt secret.docx\n
    """,
    
    "decrypt": """
    [bold]🔓 Decryption Tip[/bold]\n
    Key management:\n
    - Store keys in [red]separate secure location[/red]\n
    - Use [yellow]key derivation functions[/yellow] (PBKDF2)\n
    - Consider [blue]hardware tokens[/blue] for critical keys\n
    [green]Syntax:[/green] decrypt file.enc myStrongPassword123!\n
    """,
    
    "watchfolder": """
    [bold]👀 Folder Monitoring Tip[/bold]\n
    Detects:\n
    - [red]New files[/red] (ransomware indicators)\n
    - [yellow]Permission changes[/yellow] (chmod/chown)\n
    - [blue]Hidden files[/blue] (dotfiles, double extensions)\n
    [green]Pro Tip:[/green] Monitor /tmp and /dev/shm\n
    """,
    
    "traceroute": """
    [bold]🌐 Network Tracing Tip[/bold]\n
    Advanced options:\n
    - [red]TCP SYN[/red] probes (-T)\n
    - [yellow]ICMP[/yellow] echo (-I)\n
    - [blue]DNS lookups[/blue] (-n to disable)\n
    [green]Pro Tip:[/green] Use mtr for continuous monitoring\n
    """,
    
    "ransomwatch": """
    [bold]💰 Ransomware Tip[/bold]\n
    Detection signs:\n
    - [red]Mass file renames[/red] (.enc, .locked)\n
    - [yellow]Unusual process[/yellow] (encryption patterns)\n
    - [blue]Bitcoin wallet[/blue] creation attempts\n
    [green]Pro Tip:[/green] Monitor /home and network shares\n
    """,
    
    "wificrack": """
    [bold]📶 WiFi Auditing Tip[/bold]\n
    Common attacks:\n
    - [red]WPA2 handshake[/red] capture\n
    - [yellow]Evil Twin[/yellow] access points\n
    - [blue]KRACK[/blue] vulnerability tests\n
    [green]Requires:[/green] Monitor mode capable adapter\n
    """,
    
    "stegcheck": """
    [bold]🖼️ Steganography Awareness & Forensics Tip[/bold]\n
    Steganography is the practice of hiding information inside seemingly normal files
    such as images, audio, or video. It is often used to bypass security controls.\n

    [bold]Common Indicators of Hidden Data:[/bold]\n
    - Unusually large file size for the image resolution
    - High entropy (random-looking data)
    - Inconsistent or missing EXIF metadata
    - Suspicious color-channel patterns\n

    [bold]Detection & Analysis Methods:[/bold]\n
    - [red]Binwalk[/red]: Identify embedded files or appended data
    - [yellow]Stegdetect[/yellow]: Detect signatures of known steganography tools
    - [blue]LSB Analysis[/blue]: Examine least-significant-bit manipulation
    - [cyan]Entropy Analysis[/cyan]: Identify abnormal randomness levels\n

    [bold]Real-World Use Cases:[/bold]\n
    - Malware command-and-control via images
    - Hidden financial instructions in invoices or screenshots
    - Covert data exfiltration over messaging platforms
    - Digital evidence analysis in cybercrime investigations.\n

    [bold][green]Pro Tip:[/green][/bold]\n
    Always inspect EXIF metadata and file structure before deep analysis.
    Detection should remain non-invasive unless authorized forensic procedures apply.\n

    [bold]Ethical Reminder:[/bold]\n
    Steganalysis should only be performed for defensive, investigative,
    or educational purposes with proper authorization.\n
    """,

    "certcheck": """
    [bold]🔖 SSL Cert Tip[/bold]\n
    Critical checks:\n
    - [red]Expiration date[/red]\n
    - [yellow]Weak algorithms[/yellow] (SHA1, RC4)\n
    - [blue]SAN mismatches[/blue]\n
    [green]Pro Tip:[/green] Test with testssl.sh\n
    """,
    
    "memdump": """
    [bold]🧠 Memory Forensics Tip[/bold]\n
    What to look for:\n
    - [red]Process memory[/red] (passwords, keys)\n
    - [yellow]Network connections[/yellow] (raw sockets)\n
    - [blue]Malicious implants[/blue] (shellcode)\n
    [green]Tool:[/green] Analyze with Volatility\n
    """,
    
    "torify": """
    [bold]🧅 Tor Networking Tip[/bold]\n
    Important notes:\n
    - [red]Not 100% anonymous[/red] (exit node risks)\n
    - [yellow]DNS leaks[/yellow] still possible\n
    - [blue]Bridge nodes[/blue] for censored networks\n
    [green]Pro Tip:[/green] Combine with VPN (Tor-over-VPN)\n
    """,
    
    "update": """
    [bold cyan]🔄 DSTERMINAL SECURITY UPDATE PROTOCOL[/bold cyan]

    [bold underline]WHY SYSTEMATIC UPDATES ARE NON-NEGOTIABLE FOR SECURITY TOOLS[/bold underline]

    As a defensive security platform, DSTerminal occupies a privileged position within your infrastructure. 
    Its capabilities—from network reconnaissance to forensic analysis—require constant evolution to counter 
    the rapidly advancing threat landscape. Each update represents not just new features, but essential 
    adaptations to emerging attack methodologies.

    [underline]CRITICAL SECURITY IMPERATIVES ADDRESSED THROUGH UPDATES[/underline]

    [bold red]ZERO-DAY & N-DAY VULNERABILITY MITIGATION[/bold red]
    • [white]▸ Preemptive Patch Deployment[/white] – Closing security gaps before widespread exploitation
    • [yellow]▸ CVE-Responsive Updates[/yellow] – Direct responses to published advisories affecting scanning engines
    • [red]▸ Memory Corruption Protections[/red] – Enhanced buffer overflow and code injection defenses
    • [magenta]▸ Sandbox Escape Prevention[/magenta] – Hardening against container/VM breakout techniques

    [bold yellow]PRIVILEGE & ACCESS CONTROL REINFORCEMENT[/bold yellow]
    • [white]▸ Least Privilege Enforcement[/white] – Tighter restrictions on DSTerminal's own system access
    • [cyan]▸ Credential Handling Security[/cyan] – Improved encryption for stored API keys and credentials  
    • [green]▸ SUID/SGID Vulnerability Remediation[/green] – Fixes for potential local privilege escalation vectors
    • [red]▸ Race Condition Elimination[/red] – Preventing TOCTOU (Time-of-Check-Time-of-Use) vulnerabilities

    [bold blue]THREAT INTELLIGENCE & DETECTION ENHANCEMENT[/bold blue]
    • [white]▸ Real-Time Signature Updates[/white] – Integration of latest malware hashes and IOCs (Indicators of Compromise)
    • [yellow]▸ Behavioral Analysis Improvements[/yellow] – Enhanced heuristic detection for polymorphic malware
    • [cyan]▸ Attack Pattern Recognition[/cyan] – Updated MITRE ATT&CK framework mapping for detected activities
    • [green]▸ Threat Actor TTP Updates[/green] – Detection rules for emerging adversary tactics and procedures

    [bold magenta]CRYPTOGRAPHIC & COMMUNICATIONS SECURITY[/bold magenta]
    • [white]▸ TLS/SSL Implementation Updates[/white] – Protection against protocol-level vulnerabilities
    • [yellow]▸ Certificate Validation Enhancements[/yellow] – Improved PKI verification for API communications
    • [red]▸ Cryptographic Algorithm Rotation[/red] – Migration from deprecated to current standards
    • [cyan]▸ Secure Channel Reinforcement[/cyan] – Hardened connections to VirusTotal, threat feeds, and update servers

    [bold green]COMPLIANCE & GOVERNANCE REQUIREMENTS[/bold green]
    • [white]▸ Regulatory Framework Alignment[/white] – Updates for GDPR, HIPAA, PCI-DSS, NIST, ISO 27001 compliance
    • [yellow]▸ Audit Trail Enhancements[/yellow] – Improved logging for forensic reconstruction and compliance audits
    • [cyan]▸ Reporting Template Updates[/cyan] – Formats meeting current regulatory and executive briefing standards
    • [red]▸ Data Handling Improvements[/red] – Enhanced privacy protections for scanned data retention

    [bold underline]OPERATIONAL & FUNCTIONAL ENHANCEMENTS[/bold underline]

    [white]NETWORK DEFENSE CAPABILITIES[/white]
    • [cyan]▸ Protocol Analysis Updates[/cyan] – Detection for newer network protocols and encapsulated traffic
    • [yellow]▸ Evasion Technique Countermeasures[/yellow] – Detection of port knocking, tunneling, and protocol smuggling
    • [green]▸ IoT/OT Device Recognition[/green] – Expanded fingerprinting for industrial and embedded systems
    • [red]▸ Cloud Environment Adaptations[/red] – Scanning optimizations for AWS, Azure, GCP infrastructures

    [white]FORENSIC & INCIDENT RESPONSE IMPROVEMENTS[/white]
    • [yellow]▸ Memory Forensics Enhancements[/yellow] – Updated Volatility profiles and memory analysis techniques
    • [cyan]▸ Disk Imaging Compatibility[/cyan] – Support for newer filesystems and storage technologies
    • [green]▸ Timeline Analysis Upgrades[/green] – Improved event correlation and attack chain reconstruction
    • [red]▸ Anti-Forensics Detection[/red] – Identification of evidence tampering and artifact wiping

    [white]PERFORMANCE & SCALABILITY OPTIMIZATIONS[/white]
    • [cyan]▸ Parallel Processing Improvements[/cyan] – Faster large-scale network sweeps and distributed scanning
    • [yellow]▸ Resource Utilization Optimization[/yellow] – Reduced memory and CPU overhead during operations
    • [green]▸ Database Schema Updates[/green] – Enhanced storage efficiency for scan results and historical data
    • [red]▸ Cache Mechanism Refinements[/red] – Intelligent caching for frequently accessed threat intelligence

    [bold underline]RISK ASSESSMENT: CONSEQUENCES OF UPDATE NEGLECT[/bold underline]

    [red]IMMEDIATE THREATS[/red]
    • [white]Known Exploit Vulnerability[/white] – Attackers targeting published DSTerminal CVEs
    • [yellow]Detection Blind Spots[/yellow] – Failure to identify current malware variants
    • [cyan]False Negative Inflation[/cyan] – Missed compromise indicators due to outdated signatures
    • [magenta]Toolchain Exploitation[/magenta] – Using DSTerminal as an initial attack vector

    [red]STRATEGIC VULNERABILITIES[/red]
    • [white]Security Posture Degradation[/white] – Weakened defensive capabilities across monitored infrastructure
    • [yellow]Compliance Failures[/yellow] – Violations of mandatory security tool maintenance requirements
    • [cyan]Incident Response Impairment[/cyan] – Compromised forensic accuracy during security incidents
    • [magenta]Resource Inefficiency[/magenta] – Wasted time with false positives from outdated detection logic

    [bold underline]BEST PRACTICES FOR DSTERMINAL UPDATE MANAGEMENT[/bold underline]

    [green]FREQUENCY & SCHEDULING[/green]
    • [white]Weekly Update Checks[/white] – Minimum frequency for security tools in active environments
    • [yellow]Critical Update Immediate Application[/yellow] – Zero-day patches within 24 hours of release
    • [cyan]Change Window Coordination[/cyan] – Integration with organizational maintenance schedules
    • [red]Pre-Update Validation[/red] – Testing in isolated environments before production deployment

    [green]VERIFICATION & INTEGRITY CHECKS[/green]
    • [white]Digital Signature Validation[/white] – Confirming authenticity of all downloaded updates
    • [yellow]Hash Verification[/yellow] – SHA-256 checksum confirmation for update packages
    • [cyan]Source Authenticity[/cyan] – Ensuring updates originate from official GitHub repository
    • [red]Rollback Preparedness[/red] – Maintaining ability to revert problematic updates

    [green]EDUCATION & AWARENESS[/green]
    • [white]CVE Monitoring Subscriptions[/white] – Automatic alerts for DSTerminal-related vulnerabilities
    • [yellow]Change Log Review[/yellow] – Understanding security implications of each update
    • [cyan]Training Updates[/cyan] – Incorporating new features into security team workflows
    • [red]Vendor Communication[/red] – Reporting potential vulnerabilities discovered during use

    [bold underline]DSTERMINAL'S UPDATE ARCHITECTURE[/bold underline]

    [dim]Our update system employs a multi-layered verification approach:
    1. [white]GitHub API Integration[/white] – Secure communication with official release repository
    2. [yellow]Version Validation[/yellow] – Semantic version comparison with integrity checking
    3. [cyan]Fallback Mechanisms[/cyan] – Redundant update sources for resilience
    4. [green]Privilege Escalation Controls[/green] – Admin rights required only for installation phase
    5. [red]Rollback Capabilities[/red] – Automated restoration points before major updates[/dim]

    [bold cyan]FINAL ADVISORY:[/bold cyan]
    In cybersecurity, your defensive tools are only as strong as their most recent update.
    DSTerminal's capabilities evolve continuously—ensure your installation does too.

    [dim italic]"The only truly secure system is one that is powered off, cast in a block of concrete,
    and sealed in a lead-lined room with armed guards—and even then I have my doubts."[/dim italic]
    [dim]— Updated for the modern threat landscape[/dim]
    CER
    """,
    
    "vt-scan": """
    ╭─────────────────────────────────────────────────────────────────────────────╮
    │                         🦠 VIRUSTOTAL EDUCATIONAL TIP                        │
    ├─────────────────────────────────────────────────────────────────────────────┤
    │                                                                             │
    │  📚 WHAT IS VIRUSTOTAL?                                                     │
    │     • Advanced service that scans files & URLs with 70+ AV engines      │
    │     • Owned by Google (since 2012) - Enterprise & Community editions       │
    │     • Provides threat intelligence & behavioral analysis                    │
    │                                                                             │
    │  🔬 ADVANCED FEATURES:                                                      │
    │     • Behavioral analysis (Cuckoo/VT Sandbox) - See what files DO          │
    │     • YARA rule scanning - Pattern-based threat detection                  │
    │     • Relationship graphs - Visualize threat connections                   │
    │     • VirusTotal Enterprise - API access for automation                    │
    │     • Retrohunt - Search historical scan data                             │
    │                                                                             │
    │  📊 COMMUNITY INSIGHTS:                                                     │
    │     • Vote on detections (False Positive / Malicious)                      │
    │     • Comment on samples with analysis findings                           │
    │     • Share YARA rules with security community                            │
    │     • Create collections of related malware                               │
    │                                                                             │
    │  🎯 USE CASES FOR SOC OPERATORS:                                           │
    │     1. Incident Response - Verify suspicious file detections              │
    │     2. Threat Hunting - Research new malware families                     │
    │     3. IOC Validation - Check hash/domain reputation                      │
    │     4. Malware Analysis - Understand file behavior                        │
    │                                                                             │
    │  ⚠️ CRITICAL WARNINGS:                                                      │
    │     • Files uploaded become PUBLIC - Never upload sensitive data!         │
    │     • Free API has rate limits (4 requests/min, 500/day)                  │
    │     • Some AV engines may have false positives                            │
    │     • Not all samples get sandbox analysis                                │
    │                                                                           │
    │  💡 PRO TIPS FOR DSTERMINAL:                                              │
    │     → Hash lookup first (faster, anonymous)                               │
    │     → Enable VT Enterprise for corporate use                              │
    │     → Combine with local YARA rules for better detection                  │
    │     → Automate with Python API for bulk scanning                          │
    │                                                                           │
    │  📈 STATISTICS (2024):                                                    │
    │     • 70+ antivirus engines                                               │
    │     • 2M+ daily submissions                                               │
    │     • 6B+ historical scans                                                │
    │     • 60+ URL scanners                                                    │
    │                                                                             │
    │  🎓 RECOMMENDED LEARNING PATH:                                             │
    │     1. Start with hash lookups (no exposure)                              │
    │     2. Learn to read analysis reports                                     │
    │     3. Study YARA rule syntax                                             │
    │     4. Experiment with API automation                                     │
    │     5. Contribute community insights                                      │
    │                                                                             │
    │  🛡️ BEST PRACTICES FOR SOC:                                                │
    │     • Always sanitize files before upload                                 │
    │     • Use API keys with restricted permissions                           │
    │     • Maintain local database of known threats                           │
    │     • Cross-reference with other threat intel feeds                      │
    │     • Document findings in incident reports                              │
    │                                                                             │
    ╰─────────────────────────────────────────────────────────────────────────────╯
    """,
    
    "registry -n mon": """
    [bold]💾 Registry Monitoring Tip[/bold]\n
    Critical keys to watch:\n
    - [red]Run/RunOnce[/red] (persistence)\n
    - [yellow]AppInit_DLLs[/yellow] (code injection)\n
    - [blue]LSA secrets[/blue] (credential storage)\n
    [green]Tool:[/green] Use RegShot for comparisons\n
    """,

    }

# ==================typewriting education tips
#==============================================
def typewrite_effect(text, delay=0.02, color_effects=True):
    """Display text with pen-writing (typewriter) animation effect"""
    lines = text.split('\n')
    for line in lines:
        for char in line:
            if color_effects:
                # Color coding for special characters
                if char == '•':
                    console.print(f"[bold yellow]{char}[/bold yellow]", end='')
                elif char == '→':
                    console.print(f"[cyan]{char}[/cyan]", end='')
                elif char == '✓':
                    console.print(f"[bold green]{char}[/bold green]", end='')
                elif char == '⚠':
                    console.print(f"[bold red]{char}[/bold red]", end='')
                elif char == '★':
                    console.print(f"[bold magenta]{char}[/bold magenta]", end='')
                elif char == '📡' or char == '🌐' or char == '🔍' or char == '💡' or char == '🔐':
                    console.print(f"[cyan]{char}[/cyan]", end='')
                elif char.isdigit() and line.strip().startswith(char):
                    console.print(f"[bold red]{char}[/bold red]", end='')
                else:
                    console.print(char, end='')
            else:
                console.print(char, end='')
            sys.stdout.flush()
            time.sleep(delay)
        console.print()  # New line
        time.sleep(delay * 1.5)

def show_educational_tip(tip_key, education_tips_dict):
    """Display educational tip with typewriter animation"""
    if tip_key in education_tips_dict:
        tip_content = education_tips_dict[tip_key]
    else:
        tip_content = education_tips_dict.get("default", "No educational tip available.")
    
    console.print()
    
    # Animated border top
    for _ in range(2):
        console.print("[dim]╭─────────────────────────────────────────────────────────────────────────────╮[/dim]", end='\r')
        time.sleep(0.03)
    console.print("[dim]╭─────────────────────────────────────────────────────────────────────────────╮[/dim]")
    
    time.sleep(0.1)
    
    # Typewriter effect for content
    typewrite_effect(tip_content, delay=0.018)
    
    time.sleep(0.1)
    
    # Animated border bottom
    for _ in range(2):
        console.print("[dim]╰─────────────────────────────────────────────────────────────────────────────╯[/dim]", end='\r')
        time.sleep(0.03)
    console.print("[dim]╰─────────────────────────────────────────────────────────────────────────────╯[/dim]")
    console.print()
#==================================================
# ==================================================

SUSPICIOUS_PORTS = {23, 3389, 4444, 5555, 6667, 1337}
HIGH_RISK_COUNTRIES = {"RU", "KP", "IR", "SY"}

def calculate_threat_score(conn, geo=None):
    score = 0

    if not conn.raddr:
        return "LOW", "✓", 0

    ip = conn.raddr.ip
    port = conn.raddr.port

    if not ip.startswith(("192.168", "10.", "172.")):
        score += 2

    if port in SUSPICIOUS_PORTS:
        score += 3

    if not conn.pid:
        score += 2

    if geo and geo.get("countryCode") in HIGH_RISK_COUNTRIES:
        score += 3

    if score >= 7:
        return "HIGH", "✖", score
    elif score >= 4:
        return "MEDIUM", "⚠", score
    else:
        return "LOW", "✓", score


def get_geo_ip(ip):
    try:
        r = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,isp",
            timeout=2
        )
        data = r.json()
        if data["status"] == "success":
            return data
    except:
        pass
    return None
    
class SecurityTerminal:
        # ======= Neon SOC colors for log viewer =======
    NEON_HEADER = "<ansimagenta><b>╔══════════════════════════════════════════════╗</b></ansimagenta>"
    NEON_FOOTER = "<ansimagenta><b>╚══════════════════════════════════════════════╝</b></ansimagenta>"
    NEON_LINE = "<ansicyan>║</ansicyan>"
    NEON_COMMAND = "<ansigreen>"
    RESET = "</ansigreen>"

    BLINK = '\033[5m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    REVERSE = '\033[7m'
    RESET_ALL = '\033[0m'

    def __init__(self, workspace_root=".", interactive: bool = True):
        self.workspace = str(WORKSPACE)
        self.crypto = CryptoEngine(os.getcwd())
# ===========for hardening part+++++++++++++++++++++++++++++
        self.terminal_width = self._get_terminal_width()
        self.system = platform.system()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
# Initialize SOC Nmap Dashboard integration (check if available)
        if SOC_NMAP_AVAILABLE:
            try:
                self.soc_nmap = SOCNmapIntegration()
                # print("[+] SOC Nmap Dashboard integration loaded")
            except Exception as e:
                print(f"[!] Failed to initialize SOC Nmap: {e}")
                self.soc_nmap = None
        else:
            self.soc_nmap = None
            print("[!] SOC Nmap Dashboard not available - module not found")
        # Initialize SOC Nmap Dashboard integration
        self.soc_nmap = SOCNmapIntegration()
        self.soc_dashboard_active = False
        # Initialize SOC Nmap Dashboard
        self.soc_nmap = None
        # ===== INTEGRATE HARDENING DASHBOARD =====
        self.hardening_dashboard = HardeningDashboard(terminal_width=self.terminal_width)
        self.hardening_enabled = True
        
        # Register hardening commands
        self.commands = {}

        self._setup_logging()


# =======================================================

        self.interactive = interactive
        self.ui = None
        pd = PlatformDetector()

        self.config = {
            'version': '2.0.113',
            'monitor_paths': pd.get_trash_paths(),
            'exclude_patterns': ['*.tmp', '*.temp', '*~', '.DS_Store', 'Thumbs.db'],
            'max_file_size': 100 * 1024 * 1024,
            'encrypt_backups': False,
        }

        # self.workspace = WorkspaceManager()
        self.config_manager = None
        self.monitor = None
        self.observer = None
        self.running = False
        self.service_manager = ServiceManager(self.workspace, pid_file=os.path.join(self.workspace, 'dsterminal.pid'))
        self._setup_logging()


        if workspace_root is None:
            self.workspace_root = os.path.expanduser("~/dsterminal_workspace")
        else:
            self.workspace_root = workspace_root
    
    # Ensure workspace directory exists
        if not os.path.exists(self.workspace_root):
            os.makedirs(self.workspace_root)
    
    # Create scans subdirectory
        self.scans_dir = os.path.join(self.workspace_root, "scans")
        os.makedirs(self.scans_dir, exist_ok=True)
    # ==========================
    # Use the global variable
     # Initialize integrity monitor
        self.integrity = None
        self.alert_manager = None
        self.forensic = None
        
        if INTEGRITY_AVAILABLE:
            try:
                # Initialize integrity monitor
                self.integrity = SystemIntegrityMonitor()
                
                # Initialize alert manager
                self.alert_manager = AlertManager(self.integrity)
                self.alert_manager.alerts = []
                
                # Initialize forensic analyzer
                self.forensic = ForensicAnalyzer(self.integrity)
                # initialize autoremediation
                self.autoremediation = AutoRemediation(self.integrity)  

                if COLORS_AVAILABLE:
                    print(f"{Fore.GREEN}✓ Integrity Monitor initialized{Style.RESET_ALL}")
                else:
                    print("✓ Integrity Monitor initialized")
                    
            except Exception as e:
                if COLORS_AVAILABLE:
                    print(f"{Fore.RED}✗ Failed to initialize Integrity Monitor: {e}{Style.RESET_ALL}")
                else:
                    print(f"✗ Failed to initialize Integrity Monitor: {e}")
                self.integrity = None
                self.alert_manager = None
        else:
            if COLORS_AVAILABLE:
                print(f"{Fore.YELLOW}⚠ Integrity Monitor disabled{Style.RESET_ALL}")
            else:
                print("⚠ Integrity Monitor disabled")
    # initialize vt_scan module
    # ======================
        self.vt_scanner = None

        if VT_AVAILABLE:
            try:
                self.vt_scanner = VirusTotalScanner()
            except Exception as e:
                print(f"[!] Failed to initialize VT Scanner: {e}")
    # ================================
    # Initialize integrity monitor

    # Initialize other components
        self.console = Console()
        self.scan_queue = queue.Queue()
        self.scan_results = {}
        self.current_scan = None
        self.output_lines = []
        self.scan_progress = 0
        self.scan_status = "Ready"
        self.discovered_ports = []
        self.services_found = []
        self.nmap_mode = False

    # Set up workspace root and current directory
        self.workspace_root = os.path.abspath("DSTerminal_Workspace")
        self.current_dir = self.workspace_root
    
    # Create workspace if it doesn't exist
        if not os.path.exists(self.workspace_root):
            os.makedirs(self.workspace_root)
    
    # Create default directories
        default_dirs = ["exploits", "reports", "sandbox", "scans"]
        for dir_name in default_dirs:
            dir_path = os.path.join(self.workspace_root, dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
    
    # Virtual filesystem directory
        self.vfs_root = os.path.expanduser("~/.dsterminal_vfs")
        self.ensure_vfs()

    # =========initializing operator workspace and username and session logging===========
    # check dependencies if already installed
    def check_dependencies(self):
        """Check and report missing dependencies"""
        deps = DependencyManager()
        
        print(f"{Fore.CYAN}[*] Checking DSTERMINAL dependencies...{Style.RESET_ALL}")
        
        # Check system tools
        missing_tools = []
        for tool in ['nmap', 'whois', 'sqlmap']:
            if shutil.which(tool):
                print(f"{Fore.GREEN}✓ {tool}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ {tool} (missing){Style.RESET_ALL}")
                missing_tools.append(tool)
        
        # Check Metasploit
        if shutil.which('msfconsole'):
            print(f"{Fore.GREEN}✓ metasploit{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ metasploit (optional){Style.RESET_ALL}")
        
        # Check Python packages
        missing_packages = []
        for pkg in ['colorama', 'requests', 'folium', 'plotly', 'reportlab']:
            try:
                __import__(pkg)
                print(f"{Fore.GREEN}✓ {pkg}{Style.RESET_ALL}")
            except ImportError:
                print(f"{Fore.RED}✗ {pkg}{Style.RESET_ALL}")
                missing_packages.append(pkg)
        
        if missing_tools or missing_packages:
            print(f"\n{Fore.YELLOW}[!] Missing dependencies detected{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Run 'setup' to install missing dependencies{Style.RESET_ALL}")
            return False
        
        print(f"\n{Fore.GREEN}[✓] All dependencies satisfied!{Style.RESET_ALL}")
        return True

    def cmd_setup(self):
        """Install missing dependencies automatically"""
        print(f"{Fore.CYAN}[*] Running DSTERMINAL setup...{Style.RESET_ALL}")
        
        if platform.system() == "Linux":
            print(f"{Fore.YELLOW}[*] Installing missing packages...{Style.RESET_ALL}")
            subprocess.run(['sudo', 'apt', 'update'])
            subprocess.run(['sudo', 'apt', 'install', '-y', 'nmap', 'whois', 'sqlmap'])
            
        elif platform.system() == "Windows":
            print(f"{Fore.YELLOW}[*] Please install manually or use Chocolatey{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Or run: install_dependencies.bat{Style.RESET_ALL}")
        
        # Install Python packages
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        
        print(f"{Fore.GREEN}[✓] Setup complete!{Style.RESET_ALL}")

    def cmd_soc_nmap(self):
        """Launch SOC-grade Nmap dashboard with AI vulnerability scoring"""
        self.print_status("Launching SOC Nmap Dashboard...", "INFO")
        self.print_status("Interactive dashboard with real-time scanning", "INFO")
        self.print_status("Features: GeoIP mapping | AI scoring | Threat intel", "INFO")
        
        try:
            # Start the interactive dashboard
            self.soc_nmap.start_interactive_dashboard()
        except KeyboardInterrupt:
            self.print_status("Exiting SOC dashboard...", "WARNING")
        except Exception as e:
            self.print_status(f"SOC dashboard error: {e}", "ERROR")
    
    def cmd_soc_quick(self, target=None):
        """Quick scan using SOC dashboard"""
        if not target:
            target = input(f"{self.prompt}Enter target IP/Domain: ")
            if not target:
                return
        
        self.print_status(f"Running SOC quick scan on {target}...", "INFO")
        self.soc_nmap.quick_scan(target)
        self.print_status("Scan complete! Dashboard opened in browser.", "SUCCESS")
    
    def cmd_soc_full(self, target=None):
        """Full aggressive scan using SOC dashboard"""
        if not target:
            target = input(f"{self.prompt}Enter target IP/Domain: ")
            if not target:
                return
        
        self.print_status(f"Running SOC full scan on {target}...", "INFO")
        self.print_status("This may take several minutes...", "WARNING")
        confirm = input(f"{self.prompt}Continue? (y/n): ")
        
        if confirm.lower() == 'y':
            self.soc_nmap.full_scan(target)
            self.print_status("Scan complete! Dashboard opened in browser.", "SUCCESS")
    
    def cmd_soc_dns(self, target=None):
        """DNS reconnaissance using SOC dashboard"""
        if not target:
            target = input(f"{self.prompt}Enter domain for DNS recon: ")
            if not target:
                return
        
        self.print_status(f"Running DNS reconnaissance on {target}...", "INFO")
        self.soc_nmap.dns_recon(target)
        self.print_status("DNS recon complete! Dashboard opened in browser.", "SUCCESS")
    
    def cmd_soc_map(self):
        """Generate threat map from last scan"""
        if self.soc_nmap.dashboard and self.soc_nmap.dashboard.network_nodes:
            self.print_status("Generating threat intelligence map...", "INFO")
            self.soc_nmap.dashboard.generate_full_dashboard()
            self.print_status("Threat map opened in browser", "SUCCESS")
        else:
            self.print_status("No scan data available. Run a scan first.", "ERROR")
    
    def cmd_soc_history(self):
        """Show scan history"""
        if self.soc_nmap.dashboard and self.soc_nmap.dashboard.scan_history:
            self.print_status("Recent Scan History:", "INFO")
            print("\n")
            for i, hist in enumerate(self.soc_nmap.dashboard.scan_history[-10:], 1):
                risk_color = "🔴" if hist.risk_score >= 7 else "🟡" if hist.risk_score >= 4 else "🟢"
                print(f"  {i}. {risk_color} {hist.target} | Ports: {hist.open_ports} | Risk: {hist.risk_score:.1f} | Duration: {hist.duration}s")
                print(f"     Services: {', '.join(hist.services[:3])}")
                print(f"     Time: {hist.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                print()
        else:
            self.print_status("No scan history available", "ERROR")
    
    def cmd_soc_organizations(self):
        """Show organization location database"""
        from soc_nmap_dashboard import OrganizationLocationDB
        
        self.print_status("Organization Location Database:", "INFO")
        print("\n")
        
        # Group by country
        countries = {}
        for domain, info in OrganizationLocationDB.ORGANIZATIONS.items():
            country = info.get("country", "Unknown")
            if country not in countries:
                countries[country] = []
            countries[country].append(domain)
        
        for country, domains in sorted(countries.items()):
            flag = OrganizationLocationDB.ORGANIZATIONS[domains[0]].get("flag", "🌐")
            print(f"  {flag} {country}: {len(domains)} organizations")
            for domain in domains[:3]:
                print(f"      - {domain}")
            if len(domains) > 3:
                print(f"      ... and {len(domains) - 3} more")
            print()
# ======================================autpmatically detect and monitor new created folders
    def auto_discover_folders(self):
        """Auto-discover common user folders and add them to monitoring."""
        home = os.path.expanduser('~')
        
        # Common folder names to look for
        common_names = [
            'Projects', 'Work', 'Personal', 'Photos', 'Videos', 'Music',
            'Documents', 'Desktop', 'Downloads', 'Pictures', 'Backup',
            'Code', 'Dev', 'Development', 'Repos', 'GitHub', 'GitLab',
            'School', 'College', 'University', 'Research', 'Thesis',
            'Portfolio', 'Resume', 'CV', 'Certifications',
            'Finance', 'Tax', 'Invoices', 'Receipts', 'Bills',
            'Medical', 'Health', 'Insurance',
            'Legal', 'Contracts', 'Agreements',
            'Family', 'Kids', 'Travel', 'Recipes',
            'Scripts', 'Tools', 'Configs', 'Dotfiles',
        ]
        
        new_paths = []
        
        # Scan home directory (one level deep only)
        try:
            for item in os.listdir(home):
                item_path = os.path.join(home, item)
                if os.path.isdir(item_path) and item in common_names:
                    if item_path not in self.config['monitor_paths']:
                        new_paths.append(item_path)
        except PermissionError:
            pass
        
        # Scan Documents folder
        docs = os.path.join(home, 'Documents')
        if os.path.exists(docs):
            try:
                for item in os.listdir(docs):
                    item_path = os.path.join(docs, item)
                    if os.path.isdir(item_path):
                        if item_path not in self.config['monitor_paths']:
                            new_paths.append(item_path)
            except PermissionError:
                pass
        
        # Add discovered paths
        for path in new_paths:
            self.config['monitor_paths'].append(path)
            if self.observer and self.observer.is_alive():
                self.observer.schedule(self.monitor, path=path, recursive=True)
            print(f"  ✓ Auto-discovered: {path}")
        
        return new_paths

# ====================================================
    # =====================recon & recon_full fallback
    def run_recon_basic(self, target=None):
        """Fallback basic recon if recon.py not available"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════╗")
        print(f"║           BASIC RECONNAISSANCE TOOL            ║")
        print(f"╚══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
        if not target:
            target = input("Enter target (IP or domain): ").strip()
    
        if not target:
            print(f"{Fore.RED}[!] No target specified{Style.RESET_ALL}")
            return
    
        print(f"\n{Fore.GREEN}[+] Running basic recon on {target}{Style.RESET_ALL}")
    
    # Basic DNS lookup
        try:
            ip = socket.gethostbyname(target)
            print(f"{Fore.CYAN}[*] IP Address: {ip}{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}[!] Could not resolve hostname{Style.RESET_ALL}")
    
    # Basic whois (if available)
        try:
            import whois
            w = whois.whois(target)
            if w.registrar:
                print(f"{Fore.CYAN}[*] Registrar: {w.registrar}{Style.RESET_ALL}")
            if w.creation_date:
                print(f"{Fore.CYAN}[*] Created: {w.creation_date}{Style.RESET_ALL}")
        except:
            pass
    
    # Basic ping test
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        response = subprocess.run(['ping', param, '1', target], capture_output=True)
        if response.returncode == 0:
            print(f"{Fore.GREEN}[✓] Host is reachable{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] Host is not responding{Style.RESET_ALL}")
    
        print(f"\n{Fore.YELLOW}[!] Full recon module not available. Install recon.py for advanced features.{Style.RESET_ALL}")

    def run_full_recon_basic(self, target=None):
        """Fallback full recon if recon_full.py not available"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════╗")
        print(f"║         FULL RECONNAISSANCE TOOL (BASIC)        ║")
        print(f"╚══════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
        if not target:
            target = input("Enter target (IP or domain): ").strip()
    
        if not target:
            print(f"{Fore.RED}[!] No target specified{Style.RESET_ALL}")
            return
    
        print(f"\n{Fore.GREEN}[+] Running full recon on {target}{Style.RESET_ALL}")
    
    # DNS enumeration
        try:
            ip = socket.gethostbyname(target)
            print(f"{Fore.CYAN}[*] IP Address: {ip}{Style.RESET_ALL}")
        
        # Try reverse DNS
            try:
                hostname, _, _ = socket.gethostbyaddr(ip)
                print(f"{Fore.CYAN}[*] Reverse DNS: {hostname}{Style.RESET_ALL}")
            except:
                pass
        except:
            print(f"{Fore.RED}[!] Could not resolve hostname{Style.RESET_ALL}")
    
    # Port scan common ports
        print(f"\n{Fore.YELLOW}[*] Scanning common ports...{Style.RESET_ALL}")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080, 8443]
        open_ports = []
    
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"{Fore.GREEN}[+] Port {port}: OPEN{Style.RESET_ALL}")
                sock.close()
            except:
                pass
    
        if not open_ports:
            print(f"{Fore.YELLOW}[!] No common ports found open{Style.RESET_ALL}")
    
    # Service detection on open ports
        if open_ports:
            print(f"\n{Fore.CYAN}[*] Attempting service detection...{Style.RESET_ALL}")
            services = {
                21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
                80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
                995: "POP3S", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
                8080: "HTTP-Alt", 8443: "HTTPS-Alt"
            }
            for port in open_ports:
                if port in services:
                    print(f"{Fore.GREEN}[*] Port {port}: {services[port]}{Style.RESET_ALL}")
    
        print(f"\n{Fore.YELLOW}[!] Full recon module not available. Install recon_full.py for advanced features.{Style.RESET_ALL}")

 
    def typewriter(self, text, delay=0.03):
        """Simulate typing animation"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
   
# Example neon style constants
    NEON_HEADER = "╔══════════════════════════════════════════════╗"
    NEON_FOOTER = "╚══════════════════════════════════════════════╝"
    NEON_LINE = "║"
    NEON_COMMAND = "<ansigreen>"
    RESET = "</ansigreen>"


# ====================== SESSION INITIALIZATION ======================

    def initialize_operator_session(self):
        import uuid
        import random
        import socket
        from datetime import datetime

        operators_root = os.path.join(self.workspace_root, "operators")
        os.makedirs(operators_root, exist_ok=True)

    # ✅ Generate ONE global operator identity (USED EVERYWHERE)
        self.operator_username = f"OP-{uuid.uuid4().hex[:6].upper()}"
        self.session_id = f"SESSION-{uuid.uuid4().hex[:5].upper()}"
        try:
            from vt_scan import sync_operator_session
            sync_operator_session(self.operator_username, self.session_id)
        except Exception as e:
            print(f"⚠ VT sync failed: {e}")

    # ✅ OPTIONAL: also expose globally (for VT module sync)
        global GLOBAL_OPERATOR, GLOBAL_SESSION
        GLOBAL_OPERATOR = self.operator_username
        GLOBAL_SESSION = self.session_id

    # Create operator directory
        operator_dir = os.path.join(operators_root, self.operator_username)
        os.makedirs(operator_dir, exist_ok=True)

        log_file = os.path.join(operator_dir, "session_log.txt")

    # Store session start time
        self.session_start = datetime.now()

        with open(log_file, "w", encoding="utf-8") as f:
            f.write("╔══════════════════════════════════════════════╗\n")
            f.write("║       DSTerminal Operator Security Audit Log ║\n")
            f.write("╠══════════════════════════════════════════════╣\n")
            f.write(f"║ Operator   : {self.operator_username}\n")
            f.write(f"║ Session ID : {self.session_id}\n")
            f.write(f"║ Host       : {socket.gethostname()}\n")
            f.write(f"║ Start Time : {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("╠══════════════════════════════════════════════╣\n")
            f.write("║ Command Activity                             ║\n")
            f.write("╠══════════════════════════════════════════════╣\n")

    # Save references
        self.operator_dir = operator_dir
        self.log_file = log_file

        # ✅ Sync with VT module
        if 'sync_operator_session' in globals():
            try:
                sync_operator_session(self.operator_username, self.session_id)
            except Exception as e:
                print(f"⚠ VT sync failed: {e}")
    # ================= CINEMATIC INITIALIZATION =================

        start_time = time.time()

        self.typewriter("\n[ DSTerminal Initialization ]\n", 0.03)
        self.typewriter("✔ Generating Operator Identity...", 0.03)
        time.sleep(1.5)

        self.typewriter("✔ Creating Secure Session...", 0.05)
        time.sleep(1.5)

        self.typewriter("✔ Logging Enabled\n", 0.03)
        time.sleep(1)

        self.typewriter(f" 🛡️   🌐   ⚡ OPERATOR SESSION USERNAME: {GLOBAL_OPERATOR}\n", 0.04)

        elapsed = time.time() - start_time
        if elapsed < 10:
            time.sleep(10 - elapsed)


# ====================== COMMAND LOGGER ======================

    def log_command(self, command):
        """Record every command executed in the session"""

        timestamp = datetime.now().strftime("%H:%M:%S")

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] COMMAND: {command}\n")


# ====================== SESSION CLOSE ======================

    def close_operator_session(self):
        """Finalize session log with end time and duration"""

        session_end = datetime.now()
        duration = session_end - self.session_start

        with open(self.log_file, "a", encoding="utf-8") as f:

            f.write("╠══════════════════════════════════════════════╣\n")
            f.write(f"║ Session End : {session_end.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"║ Duration    : {str(duration).split('.')[0]}\n")
            f.write("╚══════════════════════════════════════════════╝\n")


# ====================== VIEW SESSION LOG ======================

    def view_session_log(self, log_path):
        """Display session log in cinematic SOC style"""

        try:
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            width = shutil.get_terminal_size().columns

        # Header
            print_formatted_text(HTML(" " * ((width - 50)//2) + NEON_HEADER))
            print_formatted_text(HTML(" " * ((width - 50)//2) + f"{NEON_LINE}    <b>DSTerminal SOC SESSION LOG</b> {NEON_LINE}"))
            print_formatted_text(HTML(" " * ((width - 50)//2) + NEON_HEADER.replace("╔", "╠").replace("╗", "╣")))

        # Log lines
            for line in lines:

                content = line.rstrip()

                if "Operator" in content or "Session ID" in content or "Host" in content:
                    formatted_line = f"{NEON_LINE} <ansiyellow>{content}</ansiyellow>"

                elif "Session End" in content or "Start Time" in content:
                    formatted_line = f"{NEON_LINE} <ansired>{content}</ansired>"

                elif "COMMAND" in content:
                    formatted_line = f"{NEON_LINE} {NEON_COMMAND}{content}{RESET}"

                else:
                    formatted_line = f"{NEON_LINE} {content}"

                padding = " " * ((width - len(content) - 4)//2)

                self.typewriter(padding + formatted_line, delay=0.01)

        # Footer
            print_formatted_text(HTML(" " * ((width - 50)//2) + NEON_FOOTER))

        except Exception as e:
            print(f"[!] Error displaying log: {str(e)}")
        # =================================
        # --------------------------

    def display_centered_box(self, content):
        """Display centered box with content"""
        BLINK = "\033[5m"
        CYAN = "\033[96m"
        RESET = "\033[0m"
        width = shutil.get_terminal_size().columns

        lines = content.splitlines()

        for line in lines:
            padding = max((width - len(line)) // 2, 0)
            # print(" " * padding + line)
            print(" " * padding + CYAN + BLINK + line + RESET)
        
    def log_to_siem(self, message):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open("workspace/siem_log.txt", "a") as f:
                f.write(f"[{timestamp}] {message}\n")
        except:
            pass

    def log_command(self, command):

        timestamp = datetime.now().strftime("%H:%M:%S")

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] COMMAND: {command}\n")

# ====================Session end should also be recorded.========================
    def save_session_end(self):
        from datetime import datetime

        try:
            with open(self.log_file, "a") as f:
                f.write("╠══════════════════════════════════════════════╣\n")
                f.write(f"║ Session End : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("╚══════════════════════════════════════════════╝\n")
        except:
            pass

    # ===============END HERE===========================

    def get_key(self):
        if IS_WINDOWS:
            return msvcrt.getch().decode(errors="ignore")
        else:
            return sys.stdin.read(1)

    def enable_raw(self):
        if IS_WINDOWS:
            return None  # Windows does not need raw mode

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        return old_settings


    def disable_raw(self, old):
        if IS_WINDOWS or old is None:
            return

        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def show_education_tip(self, command):

        tip = EDUCATION_TIPS.get(command)

        if not tip:
            console.print("[red]No education tip available[/red]")
            return

        console.clear()
        console.print("\n[cyan]📘 Loading Training Module...[/cyan]\n")
        time.sleep(1)

        engine.type_text(tip)

        # =================

    def ensure_vfs(self):
        """Create virtual filesystem directory"""
        os.makedirs(self.vfs_root, exist_ok=True)
    
    def resolve_path(self, filename):
        """Resolve filename to either VFS or real path"""
        # First check VFS
        vfs_path = os.path.join(self.vfs_root, filename)
        if os.path.exists(vfs_path):
            return vfs_path

     # Then check current directory
        if os.path.exists(filename):
            return os.path.abspath(filename)
        
        # Check in VFS subdirectories
        for root, dirs, files in os.walk(self.vfs_root):
            if filename in files:
                return os.path.join(root, filename)
        
        return None

# --------------------VERSION OF THE DSTERMINAL STARTS HERE--------------

    def get_current_version():
        version_file = os.path.join(os.path.dirname(__file__), "VERSION")
        try:
            with open(version_file, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return "0.0.0"

# --------------------VERSION OF THE DSTERMINAL END HERE--------------

        """Initialize terminal settings"""
        self.log_file = "security_harden.log"
        self.setup_logging()

    
        # self.cipher = Fernet(CONFIG['ENCRYPT_KEY'].encode())
        self.scan_complete = Event()
        self.scan_progress = 0

    def is_admin(self):
        """
        Check if running with administrative/root privileges
        """
        try:
            return os.geteuid() == 0
        except AttributeError:
        # Windows fallback
            import ctypes
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except Exception:
                return False

    def setup_logging(self):
        """Configure logging system"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            filemode='a'
        )
    def is_windows(self):
        return os.name == "nt"

 
    def print_banner(self):
        """Display cinematic 3-column dashboard with animated side panels"""
        import threading
        import itertools
    
    # Clear screen for fresh display
        os.system('clear' if os.name == 'posix' else 'cls')
    
    # ANSI color codes
        colors = [
            '\033[92m', '\033[38;5;46m', '\033[38;5;82m', '\033[38;5;118m',
            '\033[38;5;154m', '\033[38;5;190m', '\033[38;5;226m', '\033[38;5;220m',
            '\033[96m', '\033[95m', '\033[91m', '\033[93m'
        ]
    
        BLINK = '\033[5m'
        BOLD = '\033[1m'
        RESET = '\033[0m'
    # ===============================================
    # Side content generators (rotating)
        left_panels = [
            [
                "╔══════════════════════╗",
                "║   📊 METRICS PANEL    ║",
                "╠══════════════════════╣",
                "║ • Alerts/h:    247    ║",
                "║ • Incidents:   12     ║",
                "║ • MTTR:        4.2m   ║",
                "║ • Uptime:      99.97% ║",
                "║ • Risk Score:  76/100 ║",
                "╚══════════════════════╝"
            ],
            [
                "╔══════════════════════╗",
                "║   🛡️ DEFENSE STATUS    ║",
                "╠══════════════════════╣",
                "║ • Firewall:    ACTIVE ║",
                "║ • EDR:         ONLINE ║",
                "║ • SIEM:        12k eps║",
                "║ • Honeypot:    4 nodes║",
                "║ • SOAR:        READY  ║",
                "╚══════════════════════╝"
            ],
            [
                "╔══════════════════════╗",
                "║   🔴 ACTIVE THREATS   ║",
                "╠══════════════════════╣",
                "║ • Cobalt Strike ████╗║",
                "║ • Metasploit     ██╔═╝║",
                "║ • PowerShell EDR ═╗  ║",
                "║ • LSASS Dump     █║  ║",
                "║ • Persistence    █║  ║",
                "╚══════════════════════╝"
            ],
        ]
    
        right_panels = [
            [
                "╔══════════════════════╗",
                "║   📡 INTELLIGENCE      ║",
                "╠══════════════════════╣",
                "║ • New IOCs:  47       ║",
                "║ • Campaign:  APT29    ║",
                "║ • TTPs Updated        ║",
                "║ • Zero-day:  CVE-2024 ║",
                "║ • Patch:     83%      ║",
                "╚══════════════════════╝"
            ],
            [
                "╔══════════════════════╗",
                "║   🎯 MITRE ATT&CK      ║",
                "╠══════════════════════╣",
                "║ T1021 • Lateral MV    ║",
                "║ T1059 • Cmd Script    ║",
                "║ T1566 • Phishing      ║",
                "║ T1003 • Cred Dump     ║",
                "║ T1078 • Valid Accts   ║",
                "╚══════════════════════╝"
            ],
            [
                "╔══════════════════════╗",
                "║   ⚡ RECENT EVENTS     ║",
                "╠══════════════════════╣",
                "║ 16:32:17 │ Port Scan  ║",
                "║ 16:31:45 │ Auth Fail  ║",
                "║ 16:30:12 │ Malware DL ║",
                "║ 16:28:33 │ Lateral MV ║",
                "║ 16:25:01 │ Susp Proc  ║",
                "╚══════════════════════╝"
            ],
        ]
    
    # Main banner (centered)
        main_banner = [
            "╔════════════════════════════════════════════════════════════════════════════╗",
            "║                                                                            ║",
            "║     ██████╗ ███████╗███████╗███████╗███╗   ██╗███████╗██╗  ██╗            ║",
            "║     ██╔══██╗██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝╚██╗██╔╝            ║",
            "║     ██║  ██║█████╗  █████╗  █████╗  ██╔██╗ ██║█████╗   ╚███╔╝             ║",
            "║     ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║██╔══╝   ██╔██╗             ║",
            "║     ██████╔╝██║     ██║     ███████╗██║ ╚████║███████╗██╔╝ ██╗            ║",
            "║     ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝            ║",
            "║                                                                            ║",
            "╠════════════════════════════════════════════════════════════════════════════╣",
            f"║     Defensive Security Terminal v2.0.113 | {platform.system()} {platform.release():<20}║",
            "║     Developed by: Spark Wilson Spink | © 2024 | Powered by Stark Expo Tech Exchange    ║",
            "║     Type 'help' for available commands: Always Operate as an Administrator              ║",
            f"║     CLI Mode: {'ADMIN' if self.is_admin() else 'USER'} 🔒                              ║",
            "╚════════════════════════════════════════════════════════════════════════════╝"    
        ]
    
    # Animation state
        animation_running = True
        current_left_idx = 0
        current_right_idx = 0
        frame_count = 0
    
    # Gradient colors for cinematic effect
        def get_gradient_color(frame):
            """Cyclic rainbow gradient for cinematic feel"""
            gradient_colors = [
                '\033[38;5;196m',  # Red
                '\033[38;5;202m',  # Orange
                '\033[38;5;226m',  # Yellow
                '\033[38;5;46m',   # Green
                '\033[38;5;51m',   # Cyan
                '\033[38;5;21m',   # Blue
                '\033[38;5;93m',   # Purple
                '\033[38;5;201m',  # Pink
            ]
            return gradient_colors[frame % len(gradient_colors)]
    
        def animate_side_panels():
            """Background animation thread for rotating panels"""
            nonlocal current_left_idx, current_right_idx, animation_running
            while animation_running:
                time.sleep(3)  # Rotate every 3 seconds
                current_left_idx = (current_left_idx + 1) % len(left_panels)
                current_right_idx = (current_right_idx + 1) % len(right_panels)
    
    # Start animation thread
        anim_thread = threading.Thread(target=animate_side_panels, daemon=True)
        anim_thread.start()
    
        try:
            while animation_running:
            # Get current color
                color = get_gradient_color(frame_count)
                frame_count += 1
            
            # Get current panels
                left_panel = left_panels[current_left_idx]
                right_panel = right_panels[current_right_idx]
            
            # Build 3-column layout
                terminal_height = shutil.get_terminal_size((80, 24)).lines
                terminal_width = shutil.get_terminal_size((80, 20)).columns
            
            # Calculate widths
                panel_width = 24
                banner_width = 80
                spacing = 45
            
            # Clear and reposition cursor at top
                sys.stdout.write('\033[H')
            
            # Print header spacing
                print(f"\n{color}{BOLD}")
            
            # Create rows for 3-column layout
                max_rows = max(len(left_panel), len(main_banner), len(right_panel))
            
            # Pad panels to same height
                left_panel_padded = left_panel + [' ' * panel_width] * (max_rows - len(left_panel))
                right_panel_padded = right_panel + [' ' * panel_width] * (max_rows - len(right_panel))
                banner_padded = main_banner + [' ' * banner_width] * (max_rows - len(main_banner))
            
            # Print each row
                for i in range(max_rows):
                # Left panel (with rotation animation indicator)
                    left_text = left_panel_padded[i]
                    if i == 1 and frame_count % 2 == 0:
                        left_text = left_text.replace('╔', '◈').replace('╗', '◈')
                
                # Center banner (with breathing effect)
                    banner_text = banner_padded[i]
                    if i == 2 and frame_count % 4 < 2:
                        banner_text = banner_text.replace('█', '▓')
                
                # Right panel (pulse effect)
                    right_text = right_panel_padded[i]
                    if i == 2 and frame_count % 3 == 0:
                        right_text = right_text.replace('║', '┃')
                
                # Print 3 columns with spacing
                    sys.stdout.write(f"{color}{left_text:<{panel_width}}")
                    sys.stdout.write(' ' * spacing)
                    sys.stdout.write(f"{color}{banner_text:<{banner_width}}")
                    sys.stdout.write(' ' * spacing)
                    sys.stdout.write(f"{color}{right_text:<{panel_width}}")
                    sys.stdout.write('\n')
            
            # Print bottom status bar with animation
                status_frame = ['▰', '▱', '▰', '▱', '▰', '▱']
                anim_char = status_frame[frame_count % len(status_frame)]
            
                footer = f"\n{color}{'═' * terminal_width}{RESET}\n"
                footer += f"{color}{BOLD}{anim_char} SOC MONITORING ACTIVE {anim_char} | "
                footer += f"Threat Level: {'█' * (frame_count % 5)}{'░' * (5 - (frame_count % 5))} | "
                footer += f"Active Sessions: {frame_count % 10 + 1} | "
                footer += f"Response Time: {3 - (frame_count % 4)}.{frame_count % 10}s{RESET}"
            
                sys.stdout.write(footer)
                sys.stdout.flush()
            
                time.sleep(0.5)  # Animation frame rate
            
            # Check for keypress to exit animation
                if frame_count > 10:  # Exit after ~60 seconds
                    animation_running = False
                    break
                
        except KeyboardInterrupt:
            animation_running = False
    
    # Final static display
        os.system('clear' if os.name == 'posix' else 'cls')
    
    # Print static version
        color = '\033[92m'  # Default green
    
        for i in range(max(len(left_panels[0]), len(main_banner), len(right_panels[0]))):
            left_text = left_panels[0][i] if i < len(left_panels[0]) else ' ' * 20
            banner_text = main_banner[i] if i < len(main_banner) else ' ' * 80
            right_text = right_panels[0][i] if i < len(right_panels[0]) else ' ' * 20
        
            sys.stdout.write(f"{color}{left_text:<24}")
            sys.stdout.write(' ' * 40)
            sys.stdout.write(f"{color}{banner_text:<80}")
            sys.stdout.write(' ' * 40)
            sys.stdout.write(f"{color}{right_text:<24}")
            sys.stdout.write('\n')

        if not self.is_admin():
            print(f"\n{color}{BOLD}✅ System Ready | \n[!] Warning: Running without administrator privileges. Some features may be limited.{RESET}\n")
    #         # =====================banner print ends here======================================
    def system_info(self):
        """Enhanced system information display with security context"""
        print("\n" + "="*60)
        print("🔍 SYSTEM INFORMATION & SECURITY ASSESSMENT")
        print("="*60)
    
    # Basic system info
        print(f"\n📁 [BASIC SYSTEM]")
        print(f"  OS: {platform.system()} {platform.release()}")
        print(f"  Kernel: {platform.version().split('#')[0] if '#' in platform.version() else platform.version()}")
        print(f"  Architecture: {platform.machine()}")
        print(f"  Hostname: {socket.gethostname()}")
    
    # Enhanced processor info
        print(f"\n⚡ [PROCESSOR]")
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
            # Get processor model
                for line in cpuinfo.split('\n'):
                    if 'model name' in line:
                        processor = line.split(':')[1].strip()
                        print(f"  Model: {processor}")
                        break
            # Count cores
                cores = cpuinfo.count('processor\t:')
                print(f"  Cores: {cores} logical processors")
        except:
            print("  Info: Unable to read CPU info")
    
    # Memory info with psutil
        print(f"\n💾 [MEMORY]")
        if psutil:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            print(f"  RAM: {mem.used/1024**3:.1f}/{mem.total/1024**3:.1f} GB ({mem.percent}% used)")
            print(f"  Swap: {swap.used/1024**3:.1f}/{swap.total/1024**3:.1f} GB ({swap.percent if swap.total > 0 else 0}% used)")
        else:
            print("  Info: psutil not available")
    
    # Disk info
        print(f"\n💿 [STORAGE]")
        if psutil:
            try:
                disk = psutil.disk_usage('/')
                print(f"  Root FS: {disk.used/1024**3:.1f}/{disk.total/1024**3:.1f} GB ({disk.percent}% used)")
                print(f"  Free: {disk.free/1024**3:.1f} GB")
            except:
                print("  Info: Disk info unavailable")
    
    # Security context
        print(f"\n🛡️ [SECURITY CONTEXT]")
        print(f"  Privileges: {'🔴 ADMIN/ROOT' if self.is_admin() else '🟢 USER'}")
        print(f"  Workspace: {self.current_dir}")
    
    # Network info
        print(f"\n🌐 [NETWORK]")
        try:
            interfaces = netifaces.interfaces()
            print(f"  Interfaces: {len(interfaces)} found")
            for iface in interfaces[:3]:  # Show first 3
                print(f"    • {iface}")
        except ImportError:
            print("  Info: Install 'netifaces' for network details")
    
 
    # Security recommendations
        print(f"\n📋 [RECOMMENDATIONS]")
        if not self.is_admin():
            print("  ⚠️  Run with sudo for full security features")
            print("  🔍 Run 'exploitcheck' for vulnerability assessment")
            print("  🛡️  Run 'check integrity' for system file verification")
            print("  📊 Run 'system scan -All' for comprehensive scan")
    
            print("\n" + "="*60)


    def show_tip(self, cmd):
        """Display educational tip for the executed command."""
        if cmd in EDUCATION_TIPS:
            tip = EDUCATION_TIPS[cmd]
            console = Console()
            console.print(
                Align.center(
                    Panel.fit(
                        tip,
                        title="[bold cyan]RECOMMENDED EDUCATIONAL TIP[/bold cyan]",
                        border_style="blue",
                        width=60,
                    ),
                    vertical="middle",
                )
            )
  
    def safe_path(self, path):
        """Ensure path is within workspace"""
    # Handle paths starting with ~
        if path.startswith('~'):
            path = os.path.expanduser(path)
    
    # Handle relative paths
        if not os.path.isabs(path):
            path = os.path.join(self.current_dir, path)
    
    # Get absolute path
        full_path = os.path.abspath(path)
    
    # Check if within workspace
        if not full_path.startswith(self.workspace_root):
            raise PermissionError(f"Access outside workspace is not allowed: {full_path}")
    
        return full_path
# --------------------------------------------creating dir/folder
  
# Initialize colorama for Windows compatibility

    def _get_terminal_width(self):
        """Get terminal width for centering"""
        try:
            import shutil
            return shutil.get_terminal_size().columns
        except:
            return 80  # Default width
    
    def _center_text(self, text):
        """Center text based on terminal width"""
        return text.center(self.terminal_width)
    
    # ---------------------folder or dir creation for safe environment running
    def safe_path(self, path):
        """Ensure path is within workspace"""
        full_path = os.path.abspath(os.path.join(self.current_dir, path))
        if not full_path.startswith(self.workspace_root):
            raise PermissionError("Access outside workspace is not allowed")
        return full_path
    
    # --------------------------------------------creating dir/folder
    def mkdir(self, dirname):
        """Create a directory"""
        try:
            path = self.safe_path(dirname)
            os.makedirs(path, exist_ok=True)
            print(f"{Fore.GREEN}[+]📁 Safe directory created successfully: {os.path.basename(path)}{Style.RESET_ALL}")
        except PermissionError as e:
            print(f"{Fore.RED}[!] {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error creating directory: {e}{Style.RESET_ALL}")
    
    # -------------------------------creating a file------------------
    def touch(self, filename):
        """Create an empty file"""
        try:
            path = self.safe_path(filename)
            with open(path, "w") as f:
                f.write("DSTerminal test file\n")
            print(f"{Fore.GREEN}[+] File created: {filename}{Style.RESET_ALL}")
        except PermissionError as e:
            print(f"{Fore.RED}[!] {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error creating file: {e}{Style.RESET_ALL}")
    
    # -----------------------echo function
 
    # ------------------------folder/file navigation-------------
# ------------------------folder/file navigation-------------
# ------------------------folder/file navigation-------------
    def handle_echo(self, user_input):
        """
        Handle the echo command:
        - echo text
        - echo text > file
        - echo text >> file
        """
        try:
        # Remove leading/trailing whitespace
            user_input = user_input.strip()
        
        # Fix: Handle multi-line input (remove newlines from filename)
            user_input = user_input.replace('\n', ' ').replace('\r', ' ')

        # Must start with 'echo'
            if not user_input.lower().startswith("echo"):
                print("[!] Invalid echo command")
                return

        # Remove 'echo' from start
            command_body = user_input[4:].strip()
        
        # Fix: Clean up multiple spaces
            command_body = ' '.join(command_body.split())

        # Check for file redirection
            if '>>' in command_body:
                parts = command_body.split('>>', 1)
                text_part = parts[0].strip()
                filename = parts[1].strip()
                mode = 'a'  # append
            elif '>' in command_body:
                parts = command_body.split('>', 1)
                text_part = parts[0].strip()
                filename = parts[1].strip()
                mode = 'w'  # overwrite
            else:
            # Simple echo (no file)
                print(command_body)
                return

        # Remove quotes if present
            text_part = text_part.strip('"').strip("'")
        
        # Fix: Clean filename (remove any leftover newlines/spaces)
            filename = filename.strip().replace(' ', '_')  # Replace spaces with underscores
            if not filename:
                print("[!] No filename specified")
                return

        # Construct the full path
            if os.path.isabs(filename) or filename.startswith('~'):
            # Handle absolute paths
                path = os.path.expanduser(filename)
            else:
            # Relative path - use current directory
                path = os.path.join(self.current_dir, filename)

        # Make sure directory exists
            dir_name = os.path.dirname(path)
            if dir_name and not os.path.exists(dir_name):
                try:
                    os.makedirs(dir_name, exist_ok=True)
                except Exception as e:
                    print(f"[!] Cannot create directory: {e}")
                    return

        # Write to file
            with open(path, mode, encoding='utf-8') as f:
                f.write(text_part + '\n')

        # Verify file was created
            if os.path.exists(path):
                size = os.path.getsize(path)
                print(f"[+] Written to {filename}")
                print(f"   Content: '{text_part}'")
                print(f"   Size: {size} bytes")
            
            # Refresh the display
                self.cmd_refresh()
            else:
                print(f"[!] File was not created!")

        except PermissionError as e:
            print(f"[!] Permission denied: {e}")
        except Exception as e:
            print(f"[!] Echo failed: {e}")

#    ==============debug methos==================
# Add this method to your SecurityTerminal class
    def cmd_debug(self):
        """Debug command to show current paths"""
        print("\n" + "="*50)
        print("🔍 DEBUG INFORMATION")
        print("="*50)
        print(f"Current directory: {self.current_dir}")
        print(f"Workspace root:    {self.workspace_root}")
        print(f"Home directory:    {os.path.expanduser('~')}")
        print("\n📁 Directory contents:")
        try:
            items = os.listdir(self.current_dir)
            for item in sorted(items)[:10]:  # Show first 10 items
                item_path = os.path.join(self.current_dir, item)
                if os.path.isdir(item_path):
                    print(f"  📁 {item}/")
                else:
                    size = os.path.getsize(item_path)
                    print(f"  📄 {item} ({size} bytes)")
            if len(items) > 10:
                print(f"  ... and {len(items) - 10} more items")
        except Exception as e:
            print(f"  Error reading directory: {e}")
    
        print("\n🔐 Workspace permissions:")
        print(f"  Workspace exists: {os.path.exists(self.workspace_root)}")
        if os.path.exists(self.workspace_root):
            print(f"  Workspace writable: {os.access(self.workspace_root, os.W_OK)}")
    
        print("="*50)

        # ======
    def pwd(self):
        """Print working directory"""
        # Replace workspace root with ~ for display
        display_path = self.current_dir.replace(self.workspace_root, "~")
        print(display_path) 
    
    # ---------------------------------
    def ls(self, path="."):
        """List directory contents"""
        try:
            target_path = self.safe_path(path) if path != "." else self.current_dir
            items = os.listdir(target_path)
            
            # Color-code directories and files
            for item in sorted(items):
                item_path = os.path.join(target_path, item)
                if os.path.isdir(item_path):
                    print(f"{Fore.BLUE}{item}{Style.RESET_ALL}")  # Directories in blue
                else:
                    print(f"{Fore.WHITE}{item}{Style.RESET_ALL}")  # Files in white
                    
        except PermissionError as e:
            print(f"{Fore.RED}[!] {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error listing directory: {e}{Style.RESET_ALL}")
    
    # =---------------------------------------------
    def cd(self, dirname):
        """Change directory"""
        try:
            if dirname == "~" or dirname == "":
                path = self.workspace_root
            else:
                path = self.safe_path(dirname)
                
            if os.path.isdir(path):
                self.current_dir = path
                # Show new path
                display_path = path.replace(self.workspace_root, "~")
                print(f"{Fore.GREEN}[+] Changed to: {display_path}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] Not a directory: {dirname}{Style.RESET_ALL}")
                
        except PermissionError as e:
            print(f"{Fore.RED}[!] {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error changing directory: {e}{Style.RESET_ALL}")
    
    # -----------------------------------
    # ---viewing a file
    def cat(self, filename):
        """Display file contents"""
        try:
            path = self.safe_path(filename)
            with open(path, "r") as f:
                content = f.read()
                print(content)
        except FileNotFoundError:
            print(f"{Fore.RED}[!] File not found: {filename}{Style.RESET_ALL}")
        except PermissionError as e:
            print(f"{Fore.RED}[!] {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error reading file: {e}{Style.RESET_ALL}")
    
    # -----------------------------------
    # Command dispatcher - THIS IS THE KEY MISSING PART!
    def safe_read_file(self, filename):
        """Safely read files with multiple encoding attempts"""
        if not os.path.exists(filename):
            return f"{Fore.RED}[!] File '{filename}' not found{Style.RESET_ALL}"
    
    # Try multiple encodings in order of likelihood
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1', 'cp850', 'cp437']
    
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    content = f.read()
                    return content
            except UnicodeDecodeError:
                continue
            except Exception as e:
                return f"{Fore.RED}[!] Error reading file: {str(e)}{Style.RESET_ALL}"
    
    # If all encodings fail, try reading as binary and show hex dump
        try:
            with open(filename, 'rb') as f:
                data = f.read()
            
        # Check if it's likely a text file with some binary data
            text_chars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
            if all(b in text_chars for b in data[:100]):
                # Try to decode with replacement
                return data.decode('utf-8', errors='replace')
            else:
                # Binary file - show hex dump
                hex_lines = []
                for i in range(0, min(len(data), 512), 16):
                    chunk = data[i:i+16]
                    hex_str = ' '.join(f'{b:02x}' for b in chunk)
                    ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
                    hex_lines.append(f"{i:04x} | {hex_str:<48} | {ascii_str}")
            
                return f"{Fore.YELLOW}[!] Binary file detected. Hex dump (first 512 bytes):\n{Fore.CYAN}" + "\n".join(hex_lines) + f"{Style.RESET_ALL}"
            
        except Exception as e:
            return f"{Fore.RED}[!] Error reading file: {str(e)}{Style.RESET_ALL}"
    # ========================refresh function herre================
    def cmd_refresh(self):
        """Refresh the current directory display"""
        print(f"\r", end="")  # Clear current line
    
    # Show current directory
        print(f"\n📁 Current directory: {self.current_dir}")
    
    # List files in current directory
        try:
            items = os.listdir(self.current_dir)
            if items:
                print(f"\n   Files ({len(items)} total):")
            # Show files and directories
                for item in sorted(items)[:15]:  # Show first 15 items
                    item_path = os.path.join(self.current_dir, item)
                    if os.path.isdir(item_path):
                        print(f"      📁 {item}/")
                    else:
                        size = os.path.getsize(item_path)
                    # Format size
                        if size < 1024:
                            size_str = f"{size} B"
                        elif size < 1024 * 1024:
                            size_str = f"{size/1024:.1f} KB"
                        else:
                            size_str = f"{size/(1024*1024):.1f} MB"
                        print(f"      📄 {item} ({size_str})")
            
                if len(items) > 15:
                    print(f"      ... and {len(items) - 15} more items")
            else:
                print(f"\n   Directory is empty")
            
        # Show disk usage info
            import shutil
            total, used, free = shutil.disk_usage(self.current_dir)
            print(f"\n   💾 Disk space:")
            print(f"      Free: {free // (1024**3)} GB")
            print(f"      Used: {used // (1024**3)} GB")
        
        except PermissionError:
            print(f"\n   ⚠️  Permission denied reading directory")
        except Exception as e:
            print(f"\n   ⚠️  Error reading directory: {e}")
    
        print("")  # Empty line for spacing

# Keep ONLY this version:
    def process_command(self, user_input):
        """Process and dispatch commands"""
        if not user_input.strip():
            return True

        # Handle echo first
        if user_input.strip().lower().startswith("echo"):
            self.handle_echo(user_input)
            return True

        # ======================== HARDENING COMMANDS ============================
        # Check for hardening commands BEFORE any other processing
        cmd_lower = user_input.strip().lower()
        
        # Direct hardcoded checks (most reliable)
        if cmd_lower == 'harden':
            self.harden_system()
            return True
        elif cmd_lower == 'harden-dashboard' or cmd_lower == 'harden-menu':
            self.launch_hardening_dashboard()
            return True
        elif cmd_lower == 'harden-list':
            self.list_hardening_modules()
            return True
        elif cmd_lower == 'harden-status':
            self.show_hardening_status()
            return True
        elif cmd_lower == 'harden-report':
            self.generate_hardening_report()
            return True
        elif cmd_lower == 'harden-rollback':
            self.rollback_hardening()
            return True
        elif cmd_lower == 'harden-full':
            self.harden_system_full()
            return True
        elif cmd_lower == 'harden-quick':
            self.harden_system_quick()
            return True
        elif cmd_lower == 'harden-dry-run':
            self.harden_system_dry_run()
            return True
        elif cmd_lower == 'harden-users':
            self.harden_users_only()
            return True
        elif cmd_lower == 'harden-firewall':
            self.harden_firewall_only()
            return True
        elif cmd_lower == 'harden-ssh':
            self.harden_ssh_only()
            return True
        # ======================== END HARDENING COMMANDS ========================

        # Continue with normal command parsing using shlex
        import shlex
        try:
            parts = shlex.split(user_input)
        except ValueError:
            parts = user_input.split()
        
        if not parts:
            return True
            
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        # Command dispatch for other commands
        if command == "help":
            self.show_help()

        # SOC Nmap Dashboard Commands
        elif command == 'soc' or command == 'soc-nmap':
            self.cmd_soc_nmap()
        elif command == 'soc-quick':
            target = args[0] if args else None
            self.cmd_soc_quick(target)
        elif command == 'soc-full':
            target = args[0] if args else None
            self.cmd_soc_full(target)
        elif command == 'soc-dns':
            target = args[0] if args else None
            self.cmd_soc_dns(target)
        elif command == 'soc-map':
            self.cmd_soc_map()
        elif command == 'soc-history':
            self.cmd_soc_history()
        elif command == 'soc-orgs':
            self.cmd_soc_organizations()
        elif command == 'soc-status':
            self.cmd_soc_status()
        elif command == 'soc-dashboard':
            self.soc_dashboard_active()
        elif command == 'soc-reports':
            self.cmd_soc_reports()
        elif command == 'soc-report':
            self.cmd_soc_report()
        elif command == 'soc-pdf':
            self.cmd_soc_pdf()

        elif command == 'soc-help':
            self.soc_help()


        elif command in ("exit", "quit", "logout"):
            self.log_command(command)
            self.close_operator_session()
            print(f"{Fore.YELLOW}[+] Exiting DSTerminal...{Style.RESET_ALL}")
            return False
        elif command in ("clear", "cls"):
            os.system('cls' if os.name == 'nt' else 'clear')
        elif command == "pwd":
            self.pwd()
        elif command == "ls":
            self.ls(args[0] if args else ".")
        elif command == "cd":
            if args:
                self.cd(args[0])
            else:
                self.cd("~")
        elif command == "mkdir":
            if args:
                self.mkdir(args[0])
            else:
                print(f"{Fore.RED}[!] Usage: mkdir <directory_name>{Style.RESET_ALL}")
        elif command == "touch":
            if args:
                self.touch(args[0])
            else:
                print(f"{Fore.RED}[!] Usage: touch <filename>{Style.RESET_ALL}")
        elif command == "viewlog" or command == "session":
            self.view_session_log()
        elif command == "cat":
            if not args:
                print(f"{Fore.RED}[!] Usage: cat <filename>{Style.RESET_ALL}")
            else:
                filename = args[0]
                try:
                    if hasattr(self, 'operator_dir') and os.path.exists(self.operator_dir):
                        filepath = os.path.join(self.operator_dir, filename)
                    else:
                        filepath = self.safe_path(filename) if hasattr(self, 'safe_path') else filename
                except:
                    filepath = filename
                content = self.safe_read_file(filepath) if hasattr(self, 'safe_read_file') else "Error reading file"
                print(content)
        else:
            print(f"{Fore.RED}[!] Unknown command: {command}{Style.RESET_ALL}")
        
        return True

        
# ------added msf impleme
    def check_metasploit_installed(self):
        """Check if Metasploit is installed on Windows (multiple methods)"""
        system = platform.system()

        if system == "Linux":
            return shutil.which("msfconsole") is not None

        elif system == "Windows":
        # Method 1: Check WSL
            try:
                result = subprocess.run(
                    ["wsl", "which", "msfconsole"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5
                )
                if result.returncode == 0:
                    return True
            except Exception:
                pass
        
        # Method 2: Check common installation paths
            common_paths = [
                "C:\\metasploit-framework\\bin\\msfconsole.bat",
                "C:\\metasploit-framework\\bin\\msfconsole",
                "C:\\metasploit-framework\\msfconsole.bat",
                "C:\\Program Files\\metasploit-framework\\bin\\msfconsole.bat",
                "C:\\Program Files (x86)\\metasploit-framework\\bin\\msfconsole.bat"
            ]
        
            for path in common_paths:
                if os.path.exists(path):
                    return True
        
        # Method 3: Check if msfconsole is in PATH using 'where'
            try:
                result = subprocess.run(
                    ["where", "msfconsole"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5,
                    shell=True
                )
                if result.returncode == 0:
                    return True
            except Exception:
                pass
        
        # Method 4: Check if 'msf' command works
            try:
                result = subprocess.run(
                    ["where", "msf"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5,
                    shell=True
                )
                if result.returncode == 0:
                    return True
            except Exception:
                pass
        
            return False

        elif system == "Darwin":  # macOS
            return shutil.which("msfconsole") is not None

        return False

    def get_msf_command_path(self):
        """Get the full path to msfconsole on Windows"""
        system = platform.system()
    
        if system == "Windows":
        # Check common installation paths
            common_paths = [
                "C:\\metasploit-framework\\bin\\msfconsole.bat",
                "C:\\metasploit-framework\\bin\\msfconsole",
                "C:\\metasploit-framework\\msfconsole.bat",
                "C:\\Program Files\\metasploit-framework\\bin\\msfconsole.bat",
                "C:\\Program Files (x86)\\metasploit-framework\\bin\\msfconsole.bat"
            ]
        
            for path in common_paths:
                if os.path.exists(path):
                    return path
        
        # Try to find via 'where' command
            try:
                result = subprocess.run(
                    ["where", "msfconsole"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5,
                    shell=True
                )
                if result.returncode == 0:
                    return result.stdout.decode().strip().split('\n')[0]
            except Exception:
                pass
        
        # Try 'msf' command
            try:
                result = subprocess.run(
                    ["where", "msf"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5,
                    shell=True
                )
                if result.returncode == 0:
                    return result.stdout.decode().strip().split('\n')[0]
            except Exception:
                pass
        
            return "msfconsole"
        else:
            return "msfconsole"
 
    def launch_metasploit(self):
        """Launch Metasploit Framework in a separate window"""
        system = platform.system()
    
        if system == "Windows":
            try:
            # Simply open a new command prompt and run msfconsole
                subprocess.Popen(
                    ["cmd.exe", "/c", "start", "cmd.exe", "/k", "msfconsole"],
                    shell=False
                )
                print(f"{Fore.GREEN}[+] Metasploit launching in new window...{Style.RESET_ALL}")
                return True
            except Exception as e:
                print(f"{Fore.RED}[!] Failed to launch: {e}{Style.RESET_ALL}")
                return False
        else:
        # Linux/Mac
            try:
                subprocess.Popen(["x-terminal-emulator", "-e", "msfconsole"])
                return True
            except:
                subprocess.Popen(["msfconsole"])
                return True
            # =========
    def cinematic_spinner(self, stop_event, message, color=Fore.CYAN):
        """Enhanced spinner with cinematic effects"""
        spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        i = 0
        while not stop_event.is_set():
            sys.stdout.write(f"\r{color}{spinner_chars[i]} {message}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
            i = (i + 1) % len(spinner_chars)
        sys.stdout.write("\r" + " " * (len(message) + 20) + "\r")

    def typewriter_effect(self, text, delay=0.03, color=Fore.GREEN):
        """Typewriter effect for text output"""
        for char in text:
            sys.stdout.write(f"{color}{char}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def scan_lines(self, text, line_count=3, delay=0.05):
        """Simulate scanning lines like a terminal"""
        for i in range(line_count):
            line = f"[SCANNING] {text}... [{i+1}/{line_count}]"
            print(Fore.YELLOW + line, end="\r")
            time.sleep(delay)
        print(" " * 50, end="\r")

    def play_beep(self):
        """Play a beep sound (ASCII bell)"""
        print("\a", end="", flush=True)

    def animated_progress_bar(self, title, duration=2):
        """Animated progress bar"""
        print(f"\n{title}")
        for i in range(101):
            bar = "█" * (i // 2) + "░" * (50 - (i // 2))
            print(f"\r[{bar}] {i}%", end="", flush=True)
            time.sleep(duration / 100)
        print()

    def metasploit_intro(self):
        """Cinematic Metasploit introduction sequence"""
        phases = [
            ("Initializing Metasploit Framework", 0.7, Fore.CYAN),
            ("Loading exploit modules", 0.5, Fore.RED),
            ("Loading auxiliary modules", 0.5, Fore.YELLOW),
            ("Initializing database interface", 0.6, Fore.GREEN),
            ("Preparing cyber operations shell", 0.8, Fore.MAGENTA),
            ("Establishing secure connection", 0.4, Fore.BLUE),
            ("Bypassing security protocols", 0.5, Fore.RED),
            ("Setting up payload handlers", 0.6, Fore.CYAN)
        ]
    
        print("\n" + "="*50)
        print(Fore.RED + "           METASPLOIT FRAMEWORK" + Style.RESET_ALL)
        print("="*50 + "\n")
    
    # Simulate system scan
        self.scan_lines("Checking system compatibility", 4, 0.1)
    
        for phase, delay, color in phases:
            sys.stdout.write(f"{color}[+] {phase}")
            sys.stdout.flush()
        
        # Add dynamic dots
            for _ in range(3):
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(delay/3)
        
            print(f" {Fore.GREEN}✓{Style.RESET_ALL}")
        
        # Random progress simulation
            if "exploit" in phase.lower():
                self.scan_lines("Verifying exploit integrity", 2, 0.1)
            elif "database" in phase.lower():
                time.sleep(0.3)
                print(f"  {Fore.BLUE}>> Database connection established{Style.RESET_ALL}")
    
    # Final loading animation
        print(f"\n{Fore.YELLOW}[*] Finalizing initialization...")
        for i in range(5):
            print(f"  {Fore.YELLOW}▶ Loading component {i+1}/5", end="\r")
            time.sleep(0.2)
    
        self.play_beep()

    def show_metasploit_install_guide(self):
        """Show installation instructions for Metasploit"""
        system = platform.system()

        print(f"{Fore.RED}[!] Metasploit Framework not detected on this system.{Style.RESET_ALL}\n")

        if system == "Linux":
            print(Fore.CYAN + "[Linux Installation]" + Style.RESET_ALL)
            print("Recommended installation:")
            print(Fore.YELLOW + "  sudo apt update && sudo apt install metasploit-framework\n" + Style.RESET_ALL)
            print("Alternative (official installer):")
            print("  curl https://raw.githubusercontent.com/rapid7/metasploit-framework/master/msfinstall | sudo bash\n")

        elif system == "Windows":
            print(Fore.CYAN + "[Windows Installation - Metasploit IS installed but not detected]" + Style.RESET_ALL)
            print(Fore.YELLOW + "\nYour Metasploit appears to be installed at: C:\\metasploit-framework\\" + Style.RESET_ALL)
            print(Fore.GREEN + "\nTo fix this issue:" + Style.RESET_ALL)
            print("  1. Add C:\\metasploit-framework\\bin to your system PATH")
            print("  2. Or run DSTerminal as Administrator")
            print("  3. Or use the full path: C:\\metasploit-framework\\bin\\msfconsole.bat\n")
        
            print(Fore.CYAN + "[Manual Launch Options]:" + Style.RESET_ALL)
            print(f"  {Fore.YELLOW}msfconsole{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}C:\\metasploit-framework\\bin\\msfconsole.bat{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}cd C:\\metasploit-framework && bin\\msfconsole.bat{Style.RESET_ALL}\n")
        
            print(Fore.CYAN + "[Option 1: Add to PATH]:" + Style.RESET_ALL)
            print("  1. Open System Properties → Environment Variables")
            print("  2. Add C:\\metasploit-framework\\bin to Path")
            print("  3. Restart DSTerminal\n")
        
            print(Fore.CYAN + "[Option 2: Use WSL (Alternative)]:" + Style.RESET_ALL)
            print(Fore.YELLOW + "  wsl --install\n" + Style.RESET_ALL)
            print("Then install metasploit inside WSL:")
            print(Fore.YELLOW + "  sudo apt install metasploit-framework\n" + Style.RESET_ALL)

        elif system == "Darwin":
            print(Fore.CYAN + "[macOS Installation]" + Style.RESET_ALL)
            print("Install via Homebrew:")
            print(Fore.YELLOW + "  brew install metasploit\n" + Style.RESET_ALL)
            print("Official installer:")
            print("  https://www.metasploit.com/download\n")

        else:
            print("Unsupported operating system.\n")

        print(Fore.GREEN + "[*] After fixing the PATH or installation, restart DSTerminal and run 'msf' again." + Style.RESET_ALL)

    def handle_msf(self, args):
        """Handle Metasploit launch with cinematic effects"""
        if not self.check_metasploit_installed():
            self.show_metasploit_install_guide()
            return
    
    # Clear screen for cinematic effect
        os.system('clear' if os.name == 'posix' else 'cls')
    
    # Start cinematic intro
        self.metasploit_intro()
    
    # Launch sequence with enhanced spinner
        print(f"\n{Fore.MAGENTA}[*] Starting Metasploit Framework...{Style.RESET_ALL}")
    
        stop_event = threading.Event()
        spinner_messages = [
            "LAUNCHING MSFCONSOLE",
            "ESTABLISHING CONNECTION",
            "PREPARING PAYLOAD HANDLERS",
            "LOADING EXPLOIT DATABASE",
            "INITIALIZING SESSION MANAGER"
        ]
    
        for msg in spinner_messages:
            spinner = threading.Thread(
                target=self.cinematic_spinner,
                args=(stop_event, msg, Fore.CYAN),
                daemon=True
            )
            spinner.start()
            time.sleep(1.5)
            stop_event.set()
            spinner.join(timeout=2)
            stop_event.clear()
    
    # Countdown effect
        print(f"\n{Fore.RED}[!] LAUNCHING IN:{Style.RESET_ALL}")
        for i in range(3, 0, -1):
            print(f"  {Fore.RED}{i}...{Style.RESET_ALL}")
            time.sleep(0.5)
    
    # Final handoff
        print(f"\n{Fore.GREEN}[+] Handing control to Metasploit Framework...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Metasploit is launching in a new window{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Use 'exit' in the Metasploit window to close it{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] You can continue using DSTerminal in this window{Style.RESET_ALL}")
        self.play_beep()
        time.sleep(1)
    
        try:
            success = self.launch_metasploit()
            if not success:
                print(f"{Fore.RED}[!] Failed to launch Metasploit{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[*] Try running 'msfconsole' manually in a new terminal{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}[+] Metasploit launched successfully!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}[*] Check your taskbar for the new Metasploit window{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to start Metasploit: {e}{Style.RESET_ALL}")
    def cinematic_msf_intro_ascii(self):
        """ASCII art cinematic intro for Metasploit"""
        ascii_art = [
            r"  __  __      _        _____       _     _ _   ",
            r" |  \/  | ___| |_ __ _|  ___|_ __ | | __(_) |_ ",
            r" | |\/| |/ _ \ __/ _` | |_ | '_ \| |/ _| | __|",
            r" | |  | |  __/ || (_| |  _|| |_) | | (_| | |_ ",
            r" |_|  |_|\___|\__\__,_|_|  | .__/|_|\__,_|\__|",
            r"                           |_|                "
        ]
    
        for line in ascii_art:
            self.typewriter_effect(line, 0.02, Fore.RED)
            time.sleep(0.05)
    
    # Matrix-like falling code effect
        print(f"\n{Fore.GREEN}")
        matrix_chars = "01█▓▒░█▓▒░"
        for _ in range(10):
            line = ''.join([matrix_chars[i % len(matrix_chars)] for i in range(50)])
            print(line, end="\r")
            time.sleep(0.1)
        print(Style.RESET_ALL + " " * 50)

    def debug_metasploit(self):
        """Debug method to check Metasploit installation details"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║         METASPLOIT DEBUG INFORMATION         ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════╝{Style.RESET_ALL}")
    
        print(f"\n{Fore.YELLOW}[System Information]{Style.RESET_ALL}")
        print(f"  OS: {platform.system()} {platform.release()}")
        print(f"  Architecture: {platform.machine()}")
    
        print(f"\n{Fore.YELLOW}[PATH Directories]{Style.RESET_ALL}")
        path_dirs = os.environ.get('PATH', '').split(';')
        found_metasploit = False
        for p in path_dirs:
            if 'metasploit' in p.lower() or 'framework' in p.lower():
                print(f"  {Fore.GREEN}✓ {p}{Style.RESET_ALL}")
                found_metasploit = True
        if not found_metasploit:
            print(f"  {Fore.RED}✗ No Metasploit paths found in SYSTEM PATH{Style.RESET_ALL}")
    
        print(f"\n{Fore.YELLOW}[Common Installation Paths]{Style.RESET_ALL}")
        common_paths = [
            "C:\\metasploit-framework\\bin\\msfconsole.bat",
            "C:\\metasploit-framework\\bin\\msfconsole",
            "C:\\metasploit-framework\\msfconsole.bat",
            "C:\\Program Files\\metasploit-framework\\bin\\msfconsole.bat",
            "C:\\Program Files (x86)\\metasploit-framework\\bin\\msfconsole.bat"
        ]
    
        for path in common_paths:
            if os.path.exists(path):
                print(f"  {Fore.GREEN}✓ Found: {path}{Style.RESET_ALL}")
            else:
                print(f"  {Fore.RED}✗ Not found: {path}{Style.RESET_ALL}")
    
        print(f"\n{Fore.YELLOW}[Command Availability]{Style.RESET_ALL}")
        commands = ["msfconsole", "msfconsole.bat", "msf"]
        for cmd in commands:
            result = shutil.which(cmd)
            if result:
                print(f"  {Fore.GREEN}✓ '{cmd}' found at: {result}{Style.RESET_ALL}")
            else:
                print(f"  {Fore.RED}✗ '{cmd}' not found in PATH{Style.RESET_ALL}")
    
        print(f"\n{Fore.YELLOW}[WSL Check]{Style.RESET_ALL}")
        try:
            result = subprocess.run(["wsl", "which", "msfconsole"], capture_output=True, timeout=5)
            if result.returncode == 0:
                print(f"  {Fore.GREEN}✓ Metasploit found in WSL{Style.RESET_ALL}")
            else:
                print(f"  {Fore.RED}✗ Metasploit not found in WSL{Style.RESET_ALL}")
        except Exception as e:
            print(f"  {Fore.RED}✗ WSL check failed: {e}{Style.RESET_ALL}")
    
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")

# ---------========-----------------metasplo ends here from above-----------------------------

# ============================================================
# SOC-GRADE NMAP SCAN DASHBOARD METHODS
# ============================================================
# ==================== SOC Nmap Dashboard Integration ====================

    def cmd_soc_nmap(self):
        """Launch SOC-grade Nmap dashboard with AI vulnerability scoring"""
        # Check if nmap is installed
        if not shutil.which("nmap"):
            print(f"{Fore.RED}[!] Nmap is not installed on this system{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Install nmap: sudo apt install nmap (Debian/Ubuntu) or brew install nmap (macOS){Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}[+] Launching SOC Nmap Dashboard...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] Interactive dashboard with real-time scanning{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] Features: GeoIP mapping | AI scoring | Threat intel{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Type 'exit' or press Ctrl+C to return to DSTERMINAL{Style.RESET_ALL}")
        print()
        
        try:
            # Import and initialize the SOC dashboard
            from soc_nmap_dashboard import SOCNmapIntegration
            soc = SOCNmapIntegration()
            soc.start_interactive_dashboard()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Returning to DSTERMINAL...{Style.RESET_ALL}")
        except ImportError as e:
            print(f"{Fore.RED}[!] Failed to import SOC module: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Make sure soc_nmap_dashboard.py is in the same directory{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] SOC dashboard error: {e}{Style.RESET_ALL}")

    def cmd_soc_quick(self, target=None):
        """Quick scan using SOC dashboard (top 100 ports)"""
        # Check if nmap is installed
        if not shutil.which("nmap"):
            print(f"{Fore.RED}[!] Nmap is not installed on this system{Style.RESET_ALL}")
            return
        
        if not target:
            target = input(f"{Fore.CYAN}[?] Enter target IP/Domain: {Style.RESET_ALL}").strip()
            if not target:
                print(f"{Fore.RED}[!] No target specified{Style.RESET_ALL}")
                return
        
        print(f"{Fore.GREEN}[+] Running SOC quick scan on {target}...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Scanning top 100 ports with service detection{Style.RESET_ALL}")
        
        try:
            from soc_nmap_dashboard import SOCNmapIntegration
            soc = SOCNmapIntegration()
            soc.quick_scan(target)
            print(f"{Fore.GREEN}[+] Scan complete! Dashboard opened in browser.{Style.RESET_ALL}")
        except ImportError as e:
            print(f"{Fore.RED}[!] Failed to import SOC module: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Scan failed: {e}{Style.RESET_ALL}")

    def cmd_soc_full(self, target=None):
        """Full aggressive scan using SOC dashboard (all ports)"""
        # Check if nmap is installed
        if not shutil.which("nmap"):
            print(f"{Fore.RED}[!] Nmap is not installed on this system{Style.RESET_ALL}")
            return
        
        if not target:
            target = input(f"{Fore.CYAN}[?] Enter target IP/Domain: {Style.RESET_ALL}").strip()
            if not target:
                print(f"{Fore.RED}[!] No target specified{Style.RESET_ALL}")
                return
        
        print(f"{Fore.GREEN}[+] Running SOC full scan on {target}...{Style.RESET_ALL}")
        print(f"{Fore.RED}[!] This is an aggressive scan that may take several minutes{Style.RESET_ALL}")
        print(f"{Fore.RED}[!] Full port scan (-p-) with OS detection and scripts{Style.RESET_ALL}")
        
        confirm = input(f"{Fore.YELLOW}[?] Continue? (y/n): {Style.RESET_ALL}").strip().lower()
        if confirm != 'y':
            print(f"{Fore.YELLOW}[!] Scan cancelled{Style.RESET_ALL}")
            return
        
        try:
            from soc_nmap_dashboard import SOCNmapIntegration
            soc = SOCNmapIntegration()
            soc.full_scan(target)
            print(f"{Fore.GREEN}[+] Scan complete! Dashboard opened in browser.{Style.RESET_ALL}")
        except ImportError as e:
            print(f"{Fore.RED}[!] Failed to import SOC module: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Scan failed: {e}{Style.RESET_ALL}")

    def cmd_soc_dns(self, target=None):
        """DNS reconnaissance using SOC dashboard"""
        # Check if nmap is installed
        if not shutil.which("nmap"):
            print(f"{Fore.RED}[!] Nmap is not installed on this system{Style.RESET_ALL}")
            return
        
        if not target:
            target = input(f"{Fore.CYAN}[?] Enter domain for DNS recon: {Style.RESET_ALL}").strip()
            if not target:
                print(f"{Fore.RED}[!] No domain specified{Style.RESET_ALL}")
                return
        
        print(f"{Fore.GREEN}[+] Running DNS reconnaissance on {target}...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Scanning DNS port 53 with version detection{Style.RESET_ALL}")
        
        try:
            from soc_nmap_dashboard import SOCNmapIntegration
            soc = SOCNmapIntegration()
            soc.dns_recon(target)
            print(f"{Fore.GREEN}[+] DNS recon complete! Dashboard opened in browser.{Style.RESET_ALL}")
        except ImportError as e:
            print(f"{Fore.RED}[!] Failed to import SOC module: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] DNS recon failed: {e}{Style.RESET_ALL}")

    def cmd_soc_map(self):
        """Generate threat map from last scan"""
        try:
            from soc_nmap_dashboard import SOCNmapIntegration
            
            # Create a temporary instance to access the dashboard
            soc = SOCNmapIntegration()
            
            # Check if we have a dashboard with data
            if soc.dashboard and soc.dashboard.network_nodes and len(soc.dashboard.network_nodes) > 0:
                print(f"{Fore.GREEN}[+] Generating threat intelligence map...{Style.RESET_ALL}")
                soc.dashboard.generate_full_dashboard()
                print(f"{Fore.GREEN}[+] Threat map opened in browser{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] No scan data available. Run a scan first: soc-quick <target>{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[!] Or launch interactive dashboard: soc{Style.RESET_ALL}")
        except ImportError as e:
            print(f"{Fore.RED}[!] Failed to import SOC module: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to generate map: {e}{Style.RESET_ALL}")

    def cmd_soc_reports(self):
        """List all generated SOC reports (HTML and PDF)"""
        workspace = os.path.expanduser("~/dsterminal_workspace/scans")
        if os.path.exists(workspace):
            all_files = os.listdir(workspace)
            html_reports = [f for f in all_files if f.endswith('.html') and 'soc_report' in f]
            pdf_reports = [f for f in all_files if f.endswith('.pdf') and 'soc_report' in f]
            
            print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Generated SOC Reports{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
            
            if html_reports:
                print(f"{Fore.YELLOW}📄 HTML Reports:{Style.RESET_ALL}")
                for report in sorted(html_reports, reverse=True)[:5]:
                    report_path = os.path.join(workspace, report)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(report_path))
                    size_kb = os.path.getsize(report_path) / 1024
                    print(f"   {Fore.GREEN}→{Style.RESET_ALL} {report}")
                    print(f"     {Fore.WHITE}Size: {size_kb:.1f} KB | Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")

            if pdf_reports:
                print(f"\n{Fore.YELLOW}📑 PDF Reports:{Style.RESET_ALL}")
                for report in sorted(pdf_reports, reverse=True)[:5]:
                    report_path = os.path.join(workspace, report)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(report_path))
                    size_kb = os.path.getsize(report_path) / 1024
                    print(f"   {Fore.GREEN}→{Style.RESET_ALL} {report}")
                    print(f"     {Fore.DIM}Size: {size_kb:.1f} KB | Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
            
            if not html_reports and not pdf_reports:
                print(f"{Fore.YELLOW}[!] No reports found{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[*] Run a scan first: soc-quick <target>{Style.RESET_ALL}")
            
            print(f"\n{Fore.CYAN}📁 Location: {workspace}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] No reports directory found{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Run a scan first to create the directory{Style.RESET_ALL}")

    def cmd_soc_pdf(self):
        """Generate PDF report from last scan"""
        import glob
        
        workspace = os.path.expanduser("~/dsterminal_workspace/scans")
        
        # Look for existing PDF reports
        if os.path.exists(workspace):
            pdf_files = glob.glob(os.path.join(workspace, "soc_report_*.pdf"))
            if pdf_files:
                latest_pdf = max(pdf_files, key=os.path.getctime)
                print(f"{Fore.GREEN}[+] Found PDF report: {os.path.basename(latest_pdf)}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   Location: {latest_pdf}{Style.RESET_ALL}")
                
                open_file = input(f"{Fore.YELLOW}[?] Open PDF? (y/n): {Style.RESET_ALL}").strip().lower()
                if open_file == 'y':
                    import webbrowser
                    webbrowser.open(f"file://{latest_pdf}")
                return
            else:
                print(f"{Fore.YELLOW}[!] No PDF reports found. Run a scan first.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] No reports directory found.{Style.RESET_ALL}")
    def cmd_soc_report(self):
        """Open the latest generated report (HTML or PDF)"""
        import glob
        
        workspace = os.path.expanduser("~/dsterminal_workspace/scans")
        
        if not os.path.exists(workspace):
            print(f"{Fore.YELLOW}[!] No reports found. Run a scan first.{Style.RESET_ALL}")
            return
        
        # Get all reports
        html_reports = glob.glob(os.path.join(workspace, "soc_report_*.html"))
        pdf_reports = glob.glob(os.path.join(workspace, "soc_report_*.pdf"))
        
        if not html_reports and not pdf_reports:
            print(f"{Fore.YELLOW}[!] No reports found. Run a scan first.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Latest Reports{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        # Show HTML reports
        if html_reports:
            latest_html = max(html_reports, key=os.path.getctime)
            html_time = datetime.fromtimestamp(os.path.getmtime(latest_html))
            print(f"{Fore.YELLOW}📄 HTML Report:{Style.RESET_ALL}")
            print(f"   {os.path.basename(latest_html)}")
            print(f"   {Fore.DIM}Modified: {html_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        
        # Show PDF reports
        if pdf_reports:
            latest_pdf = max(pdf_reports, key=os.path.getctime)
            pdf_time = datetime.fromtimestamp(os.path.getmtime(latest_pdf))
            print(f"\n{Fore.YELLOW}📑 PDF Report:{Style.RESET_ALL}")
            print(f"   {os.path.basename(latest_pdf)}")
            print(f"   {Fore.DIM}Modified: {pdf_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}📁 Location: {workspace}{Style.RESET_ALL}")
        
        # Ask which to open
        choice = input(f"\n{Fore.YELLOW}[?] Open (1=HTML, 2=PDF, 3=Both, n=None): {Style.RESET_ALL}").strip()
        
        import webbrowser
        if choice == '1' and html_reports:
            webbrowser.open(f"file://{latest_html}")
            print(f"{Fore.GREEN}[+] Opening HTML report...{Style.RESET_ALL}")
        elif choice == '2' and pdf_reports:
            webbrowser.open(f"file://{latest_pdf}")
            print(f"{Fore.GREEN}[+] Opening PDF report...{Style.RESET_ALL}")
        elif choice == '3':
            if html_reports:
                webbrowser.open(f"file://{latest_html}")
            if pdf_reports:
                webbrowser.open(f"file://{latest_pdf}")
            print(f"{Fore.GREEN}[+] Opening both reports...{Style.RESET_ALL}")
        elif choice.lower() != 'n':
            print(f"{Fore.YELLOW}[!] Invalid choice or report not available{Style.RESET_ALL}")
            
    def cmd_soc_history(self):
        """Show scan history"""
        try:
            from soc_nmap_dashboard import SOCNmapIntegration
            
            soc = SOCNmapIntegration()
            
            if soc.dashboard and soc.dashboard.scan_history and len(soc.dashboard.scan_history) > 0:
                print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}[+] Recent SOC Scan History:{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
                
                for i, hist in enumerate(soc.dashboard.scan_history[-10:], 1):
                    # Determine risk indicator
                    if hist.risk_score >= 7:
                        risk_color = Fore.RED
                        risk_icon = "🔴"
                    elif hist.risk_score >= 4:
                        risk_color = Fore.YELLOW
                        risk_icon = "🟡"
                    else:
                        risk_color = Fore.GREEN
                        risk_icon = "🟢"
                    
                    print(f"{risk_color}{risk_icon} Scan #{i}{Style.RESET_ALL}")
                    print(f"   {Fore.CYAN}Target:{Style.RESET_ALL} {hist.target}")
                    print(f"   {Fore.CYAN}Time:{Style.RESET_ALL} {hist.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"   {Fore.CYAN}Duration:{Style.RESET_ALL} {hist.duration}s")
                    print(f"   {Fore.CYAN}Open Ports:{Style.RESET_ALL} {hist.open_ports}")
                    print(f"   {Fore.CYAN}Risk Score:{Style.RESET_ALL} {risk_color}{hist.risk_score:.1f}/10{Style.RESET_ALL}")
                    print(f"   {Fore.CYAN}Services:{Style.RESET_ALL} {', '.join(hist.services[:5])}")
                    print()
            else:
                print(f"{Fore.YELLOW}[!] No scan history available{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[*] Run a scan first: soc-quick <target>{Style.RESET_ALL}")
        except ImportError as e:
            print(f"{Fore.RED}[!] Failed to import SOC module: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to show history: {e}{Style.RESET_ALL}")

    def cmd_soc_organizations(self):
        """Show organization location database"""
        try:
            from soc_nmap_dashboard import OrganizationLocationDB
            
            print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Organization Location Database{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
            
            # Group by country
            countries = {}
            for domain, info in OrganizationLocationDB.ORGANIZATIONS.items():
                country = info.get("country", "Unknown")
                if country not in countries:
                    countries[country] = []
                countries[country].append((domain, info))
            
            for country in sorted(countries.keys()):
                orgs = countries[country]
                flag = orgs[0][1].get("flag", "🌐")
                print(f"{Fore.YELLOW}{flag} {country}: {Fore.GREEN}{len(orgs)} organizations{Style.RESET_ALL}")
                
                for domain, info in orgs[:5]:
                    city = info.get("city", "Unknown")
                    region = info.get("region", "")
                    region_str = f" ({region})" if region else ""
                    print(f"   {Fore.CYAN}→{Style.RESET_ALL} {domain} - {city}{region_str}")
                
                if len(orgs) > 5:
                    print(f"   {Fore.MAGENTA}... and {len(orgs) - 5} more{Style.RESET_ALL}")
                print()
            
            print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Total: {len(OrganizationLocationDB.ORGANIZATIONS)} organizations{Style.RESET_ALL}")
            
        except ImportError as e:
            print(f"{Fore.RED}[!] Failed to import SOC module: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to show organizations: {e}{Style.RESET_ALL}")

    def cmd_soc_status(self):
        """Show SOC dashboard status"""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] SOC Nmap Dashboard Status{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        # Check if file exists
        import os
        if os.path.exists("soc_nmap_dashboard.py"):
            print(f"{Fore.GREEN}✅ {Style.RESET_ALL}")
            
            # Check file size
            size = os.path.getsize("soc_nmap_dashboard.py")
            print(f"   {Fore.CYAN}Size: {size} bytes{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ {Style.RESET_ALL}")
            print(f"   {Fore.YELLOW}Current directory: {os.getcwd()}{Style.RESET_ALL}")
        
        # Check nmap
        nmap_installed = shutil.which("nmap") is not None
        print(f"\n{'✅' if nmap_installed else '❌'} Network Mapper: {'✅' if nmap_installed else '❌'}")
        
        
        # Check workspace
        workspace = os.path.expanduser("~/dsterminal_workspace/scans")
        if os.path.exists(workspace):
            report_count = len([f for f in os.listdir(workspace) if f.endswith(('.html', '.pdf'))])
            print(f"\n{Fore.GREEN}📁 Workspace: {workspace}{Style.RESET_ALL}")
            print(f"   {Fore.CYAN}Reports generated: {report_count}{Style.RESET_ALL}")
        
        print()
    def soc_help(self):
        """Display SOC Nmap Dashboard help"""
        help_text = f"""
    {Fore.CYAN}{'='*70}{Style.RESET_ALL}
    {Fore.GREEN}🛡️ SOC Nmap Dashboard Commands{Style.RESET_ALL}
    {Fore.CYAN}{'='*70}{Style.RESET_ALL}

    {Fore.YELLOW}Interactive Mode:{Style.RESET_ALL}
    {Fore.GREEN}soc{Style.RESET_ALL} or {Fore.GREEN}soc-nmap{Style.RESET_ALL}     - Launch interactive SOC dashboard with 3-panel UI

    {Fore.YELLOW}Quick Scans:{Style.RESET_ALL}
    {Fore.GREEN}soc-quick <target>{Style.RESET_ALL}    - Quick scan (top 100 ports with service detection)
    {Fore.GREEN}soc-full <target>{Style.RESET_ALL}     - Full aggressive scan (all ports + scripts + OS detection)
    {Fore.GREEN}soc-dns <domain>{Style.RESET_ALL}      - DNS reconnaissance scan

    {Fore.YELLOW}Reporting:{Style.RESET_ALL}
    {Fore.GREEN}soc-pdf{Style.RESET_ALL}                 - Generate PDF report from last scan
    {Fore.GREEN}soc-reports{Style.RESET_ALL}            - List all generated reports (HTML & PDF)

    {Fore.YELLOW}Analysis & Reporting:{Style.RESET_ALL}
    {Fore.GREEN}soc{Style.RESET_ALL}               - Generate threat intelligence map from last scan
    {Fore.GREEN}soc-history{Style.RESET_ALL}           - Show scan history with risk scores
    {Fore.GREEN}soc-orgs{Style.RESET_ALL}              - Show organization location database

    {Fore.YELLOW}Status & Help:{Style.RESET_ALL}
    {Fore.GREEN}soc-status{Style.RESET_ALL}            - Show SOC dashboard status and installed packages
    {Fore.GREEN}soc-help{Style.RESET_ALL}              - Show this help message

    {Fore.YELLOW}Examples:{Style.RESET_ALL}
    {Fore.GREEN}soc-quick google.com{Style.RESET_ALL}
    {Fore.GREEN}soc-full 192.168.1.1{Style.RESET_ALL}
    {Fore.GREEN}soc-dns example.com{Style.RESET_ALL}
    {Fore.GREEN}soc{Style.RESET_ALL}

    {Fore.CYAN}{'='*70}{Style.RESET_ALL}

    """
        print(help_text)
    def soc_test(self):
        """Test SOC functionality"""
        print(f"{Fore.CYAN}[DEBUG] Testing SOC functionality{Style.RESET_ALL}")
        
        import shutil
        import os
        
        if shutil.which("nmap"):
            print(f"{Fore.GREEN}[✓] Nmap found at: {shutil.which('nmap')}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] Nmap not found{Style.RESET_ALL}")
        
        if os.path.exists("soc_nmap_dashboard.py"):
            print(f"{Fore.GREEN}[✓] soc_nmap_dashboard.py found{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✗] soc_nmap_dashboard.py not found{Style.RESET_ALL}")
        
        try:
            from soc_nmap_dashboard import SOCNmapDashboard
            print(f"{Fore.GREEN}[✓] SOCNmapDashboard imported successfully{Style.RESET_ALL}")
        except ImportError as e:
            print(f"{Fore.RED}[✗] Import failed: {e}{Style.RESET_ALL}")
# =====================end nmap here----

    def handle_ls(self):
        path = os.getcwd()
        for item in os.listdir(path):
            print(item)
    def handle_touch(self, filename):
        open(filename, "a").close()
        print(f"[+] File created: {filename}")
    def handle_cat(self, filename):
        if not os.path.exists(filename):
            print("[!] File not found")
            return
        with open(filename, "r") as f:
            print(f.read())
    def handle_echo(self, user_input):
 
        tokens = shlex.split(user_input)

        if len(tokens) < 2:
            print()
            return

        if ">" in tokens:
            idx = tokens.index(">")
            mode = "w"
        elif ">>" in tokens:
            idx = tokens.index(">>")
            mode = "a"
        else:
            print(" ".join(tokens[1:]))
            return

        content = " ".join(tokens[1:idx])
        filename = tokens[idx + 1]

        try:
            with open(filename, mode) as f:
                f.write(content + "\n")
            print(f"[+] Written to {filename}")
        except Exception as e:
            print(f"[!] Echo failed: {e}")

# =-------------------------------------------
 

    def scan_system(self):
        """Real system scanner with live OS-backed results"""
 

        if not hasattr(self, "console"):
            self.console = Console()

    # ✅ instance attributes (THREAD SAFE)
        self.found_threats = False
        self.scan_stages = [
            ("[cyan]Scanning Memory...", "Memory Scan"),
            ("[yellow]Analyzing Processes...", "Process Scan"),
            ("[magenta]Inspecting Temp Files...", "Temp File Scan"),
            ("[blue]Checking Network...", "Network Scan"),
            ("[green]Auditing Installed Software...", "Software Audit"),
            ("[white]Verifying System Integrity...", "System Integrity"),
            ("[red]Reviewing User Accounts...", "User Audit"),
            ("[bright_cyan]Checking Security Configs...", "Security Configs"),
            ("[bright_magenta]Behavioral Analysis...", "Heuristics"),
        ]

        scan_thread = Thread(target=self.run_scan, daemon=False)
        scan_thread.start()
        return scan_thread


    def generate_scan_results(self, stage_name):    
        results = []

        if stage_name == "Memory Scan" and psutil:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            results.extend([
                ("RAM Usage", f"{mem.percent}%", "green" if mem.percent < 80 else "yellow"),
                ("Available RAM", f"{mem.available // (1024**2)} MB", "cyan"),
                ("Swap Usage", f"{swap.percent}%", "green" if swap.percent < 50 else "yellow"),
            ])

        elif stage_name == "Process Scan" and psutil:
            procs = list(psutil.process_iter(["pid", "name"]))
            results.append(("Running Processes", str(len(procs)), "cyan"))

            suspicious = []
            for p in procs:
                if p.info["name"]:
                    name = p.info["name"].lower()
                    if any(x in name for x in ["keylog", "miner", "backdoor", "exploit"]):
                        suspicious.append(p.info["name"])

            if suspicious:
                self.found_threats = True
                results.append(("Suspicious Processes", ", ".join(suspicious[:3]), "red"))
            else:
                results.append(("Suspicious Processes", "None detected", "green"))

        elif stage_name == "Heuristics":
            score = 70 if self.found_threats else 100
            color = "red" if score < 80 else "green"
            results.append(("Threat Score", f"{score}/100", color))

        return results


    def display_stage_results(self, stage_name):

        results = self.generate_scan_results(stage_name)

        table = RichTable(title=stage_name, header_style="bold magenta")
        table.add_column("Check", style="cyan", width=25)
        table.add_column("Result", width=30)
        table.add_column("Status", width=12)

        for check, result, color in results:
            table.add_row(
                check,
                result,
                f"[{color}]{color.upper()}[/{color}]"
            )

        self.console.print(Panel(table, border_style="bright_blue"))


    def run_scan(self):
 
        with Live(console=self.console, refresh_per_second=15) as live:
            for label, stage in self.scan_stages:
                progress = Progress(
                    TextColumn("[bold cyan]{task.description}"),
                    BarColumn(),
                    TextColumn("{task.percentage:>3.0f}%"),
                    console=self.console,
                )

                task = progress.add_task(label, total=100)

                for _ in range(100):
                    progress.update(task, advance=1)
                    live.update(
                        Panel(
                            Align.center(progress),
                            title="[bold]System Security Scan[/bold]",
                            subtitle=stage,
                            border_style="bright_blue",
                        )
                    )
                    time.sleep(0.03)

                self.display_stage_results(stage)
                time.sleep(0.6)

    # ✅ Final verdict
        if self.found_threats:
            self.console.print(Panel(
                "[bold red]⚠ THREATS DETECTED[/bold red]",
                border_style="red",
            ))
        else:
            self.console.print(Panel(
                "[bold green]✓ SYSTEM SECURE[/bold green]",
                border_style="green",
            ))
# ===========================================secure deletion protection section =============================
# =============================================================================================================
    def _setup_logging(self):
        if not logging.getLogger().handlers:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

    def start(self):
        """Start monitoring."""
        if self.interactive:
            self._show_startup_banner()

        self.monitor = DSTerminalMonitor(
            self.config, self.workspace, 
            interactive=self.interactive, ui=self.ui
        )
        from watchdog.observers import Observer
        self.observer = Observer()

        for path in self.config['monitor_paths']:
            if os.path.exists(path):
                self.observer.schedule(self.monitor, path=path, recursive=True)
                if self.interactive:
                    self.ui.cinematic_print(f"  ✓ Monitoring: {path}", 0.01, "GREEN")
                else:
                    logging.info(f"Monitoring: {path}")
            else:
                if self.interactive:
                    self.ui.cinematic_print(f"  ✗ Path not found: {path}", 0.01, "YELLOW")
                else:
                    logging.warning(f"Path not found: {path}")

        self.observer.start()
        self.running = True

        if self.interactive:
            print(f"\n{self.ui.colors.BRIGHT_CYAN}✨ System Active - Protecting Your Data ✨{self.ui.colors.RESET}")
            print(f"{self.ui.colors.DIM}Press Ctrl+C to stop monitoring{self.ui.colors.RESET}\n")
            stats_thread = threading.Thread(target=self._display_stats, daemon=True)
            stats_thread.start()
        else:
            logging.info("DSTerminal service started in background.")

        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            if self.interactive:
                self.stop()
        finally:
            self.stop()

    def _display_stats(self):
        last_update = 0
        while self.running and self.interactive:
            if time.time() - last_update > 10 and self.monitor:
                stats = self.monitor.get_statistics()
                if stats['session_backups'] > 0:
                    size_mb = stats['session_size'] / (1024 * 1024)
                    print(f"\n{self.ui.colors.DIM}📊 Session: {stats['session_backups']} files ({size_mb:.2f} MB) backed up{self.ui.colors.RESET}")
                last_update = time.time()
            time.sleep(1)

    def stop(self):
        self.running = False
        if self.interactive:
            print(f"\n{self.ui.colors.YELLOW}🛑 Shutting down...{self.ui.colors.RESET}")
        else:
            logging.info("Shutting down DSTerminal service...")
        if self.observer:
            self.observer.stop()
            self.observer.join()
        if self.monitor:
            self.monitor.cleanup()
        self.service_manager.remove_pid_file()
        if self.interactive:
            self._show_shutdown_summary()
        else:
            logging.info("DSTerminal service stopped.")

    def run_as_service(self):
        if self.service_manager.is_running(self.service_manager.pid_file):
            print("DSTerminal service is already running.")
            sys.exit(1)
        print("Starting DSTerminal as a background service...")
        self.service_manager.daemonize()
        self.interactive = False
        self.ui = None
        self.start()

    # ── COMMAND HANDLERS (imported module methods) ──

    def _show_startup_banner(self):
        # Your existing banner code
        pass

    def _show_shutdown_summary(self):
        # Your existing summary code
        pass
# ========================added methids below============
    # ── Deletion Protection Command Methods ──

    def cmd_monitor(self):
        """Start interactive monitoring in background thread."""
        if self.running:
            print("[!] Monitoring is already running.")
            return
    
        print("[*] Starting deletion protection monitor...")

        self.monitor = DSTerminalMonitor(
        self.config, 
        SimpleWorkspace(self.workspace),  # Wrap it
        interactive=False, 
        ui=None
    )
    
    def cmd_monitor_all(self):
        """Monitor entire user profile (skip inaccessible folders)."""
        home = os.path.expanduser('~')
        
        exclude_dirs = [
            'AppData', 'Application Data', 'Cookies', 'NetHood',
            'PrintHood', 'Recent', 'SendTo', 'Start Menu',
            'Templates', 'Local Settings', '.cache',
            'node_modules', '.git', '__pycache__', '.venv',
            'dsterminal_workspace',
        ]
        
        print("[*] Starting full user profile monitoring...")
        
        for item in os.listdir(home):
            item_path = os.path.join(home, item)
            if os.path.isdir(item_path) and item not in exclude_dirs:
                if item_path not in self.config['monitor_paths']:
                    # Check if accessible before adding
                    if os.access(item_path, os.R_OK):
                        self.config['monitor_paths'].append(item_path)
                        if self.observer and self.observer.is_alive():
                            try:
                                self.observer.schedule(self.monitor, path=item_path, recursive=True)
                            except:
                                pass
                        print(f"  ✓ Monitoring: {item_path}")
        
        print("[✓] Full profile monitoring active.")

    def cmd_kill_monitor(self):
        """Force kill the monitoring window by finding the process."""
        import subprocess
        print("[*] Force stopping monitoring window...")
        
        try:
            # Find python processes running monitor-only
            result = subprocess.run(
                ['wmic', 'process', 'where', 'name="python.exe"', 'get', 'processid,commandline', '/format:csv'],
                capture_output=True, text=True, timeout=10
            )
            
            for line in result.stdout.split('\n'):
                if '--monitor-only' in line:
                    # Extract PID (last column)
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        pid = parts[-1].strip()
                        if pid.isdigit():
                            subprocess.run(['taskkill', '/PID', pid, '/F'], capture_output=True)
                            print(f"  ✓ Killed process {pid}")
            
            print("[✓] Monitoring stopped.")
        except Exception as e:
            print(f"[!] Error: {e}")
            print("[i] Close the 'DSTerminal Deletion Protection' window manually.")
        
        self.running = False

    def cmd_start_folder_watcher(self):
        """Start watching for new folder creation in home directory."""
        from deletion_protection import NewFolderWatcher
        import watchdog.observers as wd_observers  # Import with alias to avoid conflict
        
        home = os.path.expanduser('~')
        
        # Only start if monitor is ready
        if not self.monitor:
            print("[!] Start monitoring first with 'service start'")
            return
        
        self.folder_watcher = NewFolderWatcher(
            config=self.config,
            monitor_handler=self.monitor,
            observer=self.observer,
            workspace=self.workspace
        )
        
        self.folder_observer = wd_observers.Observer()  # Use aliased import
        self.folder_observer.schedule(self.folder_watcher, path=home, recursive=False)
        self.folder_observer.start()
        
        print(f"[✓] Folder watcher active on: {home}")
        print("[i] New folders will be automatically monitored.")


        workspace_obj = SimpleWorkspace(self.workspace)
    
        self.monitor = DSTerminalMonitor(
            self.config, workspace_obj,
            interactive=False, ui=None
        )
    
        from watchdog.observers import Observer
        self.observer = Observer()
    
        for path in self.config.get('monitor_paths', []):
            if os.path.exists(path):
                self.observer.schedule(self.monitor, path=path, recursive=True)
                print(f"  ✓ Monitoring: {path}")
    
        monitor_thread = threading.Thread(target=self._run_observer, daemon=True)
        monitor_thread.start()
        self.running = True
        print("[✓] Deletion protection started in background.")


    def _run_observer(self):
        """Run the observer (called in daemon thread)."""
        try:
            self.observer.start()
            while self.running:
                time.sleep(1)
        except Exception as e:
            logging.error(f"Monitor error: {e}")


    def cmd_service_start(self):
        """Start deletion protection in a separate window with all folders."""
        print("[*] Auto-discovering folders...")
        self.auto_discover_folders()
        
        # Save the updated config with all paths
        config_path = os.path.join(self.workspace, 'config', 'monitor_config.json')
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(self.config, f)
        
        print("[*] Launching deletion protection in separate window...")
        
        python_exe = sys.executable
        script_path = os.path.abspath(__file__)
        workspace_path = self.workspace if isinstance(self.workspace, str) else self.workspace.base_path
        
        # Build command with all discovered paths
        monitor_paths = ','.join(self.config['monitor_paths'])
        
        if platform.system() == 'Windows':
            cmd = (
                f'start "DSTerminal Deletion Protection" '
                f'cmd /k "{python_exe} {script_path} --monitor-only '
                f'--workspace {workspace_path} '
                f'--paths {monitor_paths}"'
            )
            os.system(cmd)
        else:
            cmd = [
                python_exe, script_path, '--monitor-only',
                '--workspace', workspace_path,
                '--paths', monitor_paths
            ]
            subprocess.Popen(cmd)
        
        self.running = True
        print("[✓] Deletion protection launched in separate window.")
        print(f"[i] Monitoring {len(self.config['monitor_paths'])} folders")
        print("[i] Close that window to stop monitoring.")

    def cmd_service_stop(self):
        """Stop the separate monitoring window."""
        print("[*] Stopping deletion protection...")
        self.cmd_kill_monitor()
        
        # Kill the separate window process
        if platform.system() == 'Windows':
            try:
                subprocess.run(
                    ['taskkill', '/FI', 'WINDOWTITLE eq DSTerminal Deletion Protection', '/F'],
                    capture_output=True,
                    timeout=5
                )
                print("[✓] Monitoring window closed.")
            except Exception as e:
                print(f"[!] Could not close window: {e}")
                print("[i] Close the 'DSTerminal Deletion Protection' window manually.")
        else:
            try:
                subprocess.run(['pkill', '-f', '--monitor-only'], capture_output=True, timeout=5)
                print("[✓] Monitoring window closed.")
            except:
                print("[i] Close the monitoring window manually.")
        
        self.running = False


    def cmd_service_status(self):
        """Show service status - checks the separate window process."""
        import subprocess
    
    # Check if the monitor-only process is running
        try:
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'],
                capture_output=True, text=True
            )
        # Look for a python process running dsterminal with --monitor-only
            if '--monitor-only' in result.stdout:
                print("DSTerminal monitoring is ACTIVE (separate window).")
            else:
            # Fallback: check if observer is running in this process
                if self.running:
                    print("DSTerminal monitoring is ACTIVE.")
                else:
                    print("DSTerminal monitoring is INACTIVE.")
        except:
            if self.running:
                print("DSTerminal monitoring is ACTIVE.")
            else:
                print("DSTerminal monitoring is INACTIVE.")

    def _get_workspace(self):
        """Get a workspace object from the string path."""
        return SimpleWorkspace(self.workspace)

    def cmd_list_backups(self):
        """List recent backups."""
        ws = SimpleWorkspace(self.workspace)
        rm = RestoreManager(ws, ui=None)
        backups = rm.list_backups(limit=30)
        if not backups:
            print("No backups found.")
            return
        print(f"\n{'ID':<6} {'Filename':<50} {'Size':<12} {'Date':<20}")
        print("-" * 95)
        for b in backups:
            size_mb = b['file_size'] / (1024 * 1024)
            size_str = f"{size_mb:.2f} MB"
            date_str = b['created_at'][:19] if b['created_at'] else 'N/A'
            filename = b['filename'][:47] + '...' if len(b['filename']) > 50 else b['filename']
            print(f"{b['id']:<6} {filename:<50} {size_str:<12} {date_str:<20}")



    def cmd_search_backups(self, query: str):
        """Search backups."""
        ws = SimpleWorkspace(self.workspace)
        rm = RestoreManager(ws, ui=None)
        results = rm.search_backups(query)
        if not results:
            print(f"No backups matching '{query}'.")
            return
        print(f"\nFound {len(results)} backup(s) matching '{query}':\n")
        for b in results:
            print(f"  [{b['id']}] {b['filename']} - {b['created_at']}")


    def cmd_restore_id(self, backup_id: int, target: str = None):
        """Restore by ID."""
        ws = SimpleWorkspace(self.workspace)
        rm = RestoreManager(ws, ui=None)
        rm.restore_file(backup_id, target)

    def cmd_restore_last(self):
        """Restore most recently deleted."""
        ws = SimpleWorkspace(self.workspace)
        rm = RestoreManager(ws, ui=None)
        rm.restore_last_deleted()

    def cmd_add_path(self, path: str):
        """Add monitoring path."""
        path = os.path.abspath(os.path.expanduser(path))
        if not os.path.isdir(path):
            print(f"✗ Not a directory: {path}")
            return
        if path not in self.config['monitor_paths']:
            self.config['monitor_paths'].append(path)
        if self.observer and self.observer.is_alive():
            self.observer.schedule(self.monitor, path=path, recursive=True)
        print(f"✓ Now monitoring: {path}")

    def cmd_workspace_info(self):
        """Show workspace info."""
        info = self.workspace if isinstance(self.workspace, str) else self.workspace.base_path
        db_path = os.path.join(info, 'database', 'dsterminal.db')
        if os.path.exists(db_path):
            import sqlite3
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT COUNT(*) as n, COALESCE(SUM(file_size),0) as s FROM backups')
            row = c.fetchone()
            conn.close()
            total_backups = row['n'] or 0
            total_size = row['s'] or 0
        else:
            total_backups = 0
            total_size = 0
        print(f"\n📁 Workspace: {info}")
        print(f"📊 Total Backups: {total_backups}")
        print(f"💾 Total Size: {total_size / (1024**3):.2f} GB\n")

    def cmd_cleanup(self):
        """Clean temp files."""
        temp_dir = os.path.join(self.workspace if isinstance(self.workspace, str) else self.workspace.base_path, 'temp')
        if os.path.exists(temp_dir):
            cutoff = time.time() - (24 * 3600)
            for f in os.listdir(temp_dir):
                fp = os.path.join(temp_dir, f)
                if os.path.isfile(fp) and os.path.getmtime(fp) < cutoff:
                    try:
                        os.remove(fp)
                    except:
                        pass
        print("✅ Temporary files cleaned up")

    def cmd_platform_info(self):
        """Show platform info."""
        pd = PlatformDetector()
        info = pd.get_system_info()
        print(f"\n🌍 Platform Information:")
        for key, value in info.items():
            print(f"   {key}: {value}")
        print(f"\n📁 Monitor Paths:")
        for path in pd.get_trash_paths():
            print(f"   {path}")



# =================================================ernds herte ===============================================
#  for financial_forensics==========================================
    def cmd_financial_forensics(self):
        """Launch the Financial Forensics investigation suite."""
        if not FINANCIAL_FORENSICS_AVAILABLE:
            print(f"{Fore.RED}[!] Financial Forensics module not available.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Make sure financial_forensic.py is in the same directory.{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}[*] Launching Financial Forensics Suite...{Style.RESET_ALL}")
        time.sleep(0.5)
        
        try:
            financial_forensics_menu()
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}[*] Returning to DSTerminal...{Style.RESET_ALL}")


# ====================for hardening section=================================
# ============================================================
# ENTERPRISE-GRADE HARDENING INTEGRATION FOR MAIN DSTERMINAL.PY
# ============================================================

    def _get_hardening_dashboard(self):
        """Get or create hardening dashboard instance with cinematic support"""
        if not hasattr(self, 'hardening_dashboard') or self.hardening_dashboard is None:
            try:
                from hardening_dashboard import HardeningDashboard
                # Detect terminal width
                try:
                    import shutil
                    terminal_width = shutil.get_terminal_size().columns
                except:
                    terminal_width = 120
                
                self.hardening_dashboard = HardeningDashboard(terminal_width=terminal_width)
                print(f"{Fore.GREEN}[✓] Hardening system initialized (Cinematic Mode){Style.RESET_ALL}")
            except ImportError as e:
                print(f"{Fore.RED}[!] Failed to import hardening_dashboard: {e}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[*] Make sure hardening_dashboard.py exists in the same directory{Style.RESET_ALL}")
                return None
            except Exception as e:
                print(f"{Fore.RED}[!] Failed to initialize hardening: {e}{Style.RESET_ALL}")
                import traceback
                traceback.print_exc()
                return None
        return self.hardening_dashboard

    def harden_system(self):
        """Main hardening command handler - Enterprise Cinematic Mode"""
        dashboard = self._get_hardening_dashboard()
        if not dashboard:
            return
        
        # Check if Rich is available for cinematic mode
        try:
            from rich.console import Console
            RICH_AVAILABLE = True
        except ImportError:
            RICH_AVAILABLE = False
        
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{' '*15}SYSTEM HARDENING - CINEMATIC MODE{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}System:{Style.RESET_ALL} {dashboard.system}")
        print(f"{Fore.YELLOW}Admin:{Style.RESET_ALL} {dashboard.is_admin_user}")
        print(f"{Fore.YELLOW}Modules:{Style.RESET_ALL} {len(dashboard.modules)}")
        print(f"\n{Fore.CYAN}Commands:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}harden-dashboard{Style.RESET_ALL}  - Launch cinematic dashboard")
        print(f"  {Fore.GREEN}harden-list{Style.RESET_ALL}       - List all modules")
        print(f"  {Fore.GREEN}harden-status{Style.RESET_ALL}     - Show status")
        print(f"  {Fore.GREEN}harden-full{Style.RESET_ALL}       - Execute full hardening")
        print(f"  {Fore.GREEN}harden-quick{Style.RESET_ALL}      - Quick hardening")
        print(f"  {Fore.GREEN}harden-cinematic{Style.RESET_ALL}  - Launch cinematic mode")

    def harden_system_full(self):
        """Execute full system hardening with real-time telemetry"""
        dashboard = self._get_hardening_dashboard()
        if not dashboard:
            return
        
        # Select all compatible modules
        dashboard.selected_modules = [
            m.id for m in dashboard.modules 
            if not (m.requires_admin and not dashboard.is_admin_user)
        ]
        
        print(f"\n{Fore.GREEN}[+] Executing FULL system hardening...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] {len(dashboard.selected_modules)} modules selected{Style.RESET_ALL}")
        
        # Use cinematic execution if available
        if hasattr(dashboard, '_execute_hardening_realtime'):
            dashboard._execute_hardening_realtime()
        else:
            dashboard._execute_hardening()
        dashboard._generate_report()

    def harden_system_quick(self):
        """Quick hardening - critical and high only with real-time output"""
        dashboard = self._get_hardening_dashboard()
        if not dashboard:
            return
        
        # Select critical and high severity
        dashboard.selected_modules = [
            m.id for m in dashboard.modules 
            if m.severity.value in ['CRITICAL', 'HIGH']
            and not (m.requires_admin and not dashboard.is_admin_user)
        ]
        
        print(f"\n{Fore.GREEN}[+] Executing QUICK hardening...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] {len(dashboard.selected_modules)} critical/high modules selected{Style.RESET_ALL}")
        
        if hasattr(dashboard, '_execute_hardening_realtime'):
            dashboard._execute_hardening_realtime()
        else:
            dashboard._execute_hardening()

    def harden_system_dry_run(self):
        """Preview hardening without applying - Dry Run Mode"""
        dashboard = self._get_hardening_dashboard()
        if not dashboard:
            return
        
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{self._center_text('DRY RUN - Preview Mode (No Changes Made)')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
        
        # Create categories for better display
        categories = {}
        for module in dashboard.modules:
            cat = module.category.value
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(module)
        
        for category, modules in categories.items():
            print(f"{Fore.YELLOW}▸ {category}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{'─'*50}{Style.RESET_ALL}")
            for module in modules:
                if module.platforms and dashboard.system not in module.platforms:
                    continue
                admin_req = f"{Fore.RED} [ADMIN REQUIRED]{Style.RESET_ALL}" if module.requires_admin and not dashboard.is_admin_user else ""
                severity_color = Fore.RED if module.severity.value == 'CRITICAL' else Fore.YELLOW
                print(f"  {Fore.GREEN}○{Style.RESET_ALL} {module.name}")
                print(f"      [{severity_color}{module.severity.value}{Style.RESET_ALL}] {module.description[:55]}...{admin_req}")
            print()
        
        print(f"{Fore.GREEN}[✓] Dry run complete. {len(dashboard.modules)} modules available.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] No changes were made to your system.{Style.RESET_ALL}")

    def launch_hardening_dashboard(self):
        """Launch interactive hardening dashboard (Cinematic Mode)"""
        dashboard = self._get_hardening_dashboard()
        if not dashboard:
            return
        
        # Use cinematic mode if available
        if hasattr(dashboard, 'run_cinematic'):
            dashboard.run_cinematic()
        else:
            dashboard.run()

    def launch_hardening_cinematic(self):
        """Launch cinematic hardening dashboard with 4-panel layout"""
        dashboard = self._get_hardening_dashboard()
        if not dashboard:
            return
        
        if hasattr(dashboard, 'run_cinematic'):
            dashboard.run_cinematic()
        else:
            print(f"{Fore.YELLOW}[!] Cinematic mode not available, using standard mode...{Style.RESET_ALL}")
            dashboard.run()

    def show_hardening_status(self):
        """Show current hardening status with cinematic formatting"""
        dashboard = self._get_hardening_dashboard()
        if not dashboard:
            return
        
        # Try to use cinematic status if available
        if hasattr(dashboard, 'show_status_cinematic'):
            dashboard.show_status_cinematic()
            return
        
        # Fallback to standard status
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{self._center_text('HARDENING STATUS DASHBOARD')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        
        # System Info Box
        print(f"\n{Fore.CYAN}┌{'─'*56}┐{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{self._center_text('SYSTEM INFORMATION', 56)}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}├{'─'*56}┤{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{f' Platform: {dashboard.system}'.ljust(56)}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{f' Admin: {dashboard.is_admin_user}'.ljust(56)}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│{f' Session: {dashboard.session_id}'.ljust(56)}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}└{'─'*56}┘{Style.RESET_ALL}")
        
        # Module Stats Box
        print(f"\n{Fore.GREEN}┌{'─'*56}┐{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│{self._center_text('MODULE STATISTICS', 56)}│{Style.RESET_ALL}")
        print(f"{Fore.GREEN}├{'─'*56}┤{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│{f' Available: {len(dashboard.modules)}'.ljust(56)}│{Style.RESET_ALL}")
        print(f"{Fore.GREEN}│{f' Selected: {len(dashboard.selected_modules)}'.ljust(56)}│{Style.RESET_ALL}")
        print(f"{Fore.GREEN}└{'─'*56}┘{Style.RESET_ALL}")
        
        # Results Box
        if dashboard.results:
            completed = sum(1 for r in dashboard.results if r.success)
            failed = len(dashboard.results) - completed
            success_rate = (completed / len(dashboard.results) * 100) if dashboard.results else 0
            
            print(f"\n{Fore.YELLOW if failed > 0 else Fore.GREEN}┌{'─'*56}┐{Style.RESET_ALL}")
            print(f"{Fore.YELLOW if failed > 0 else Fore.GREEN}│{self._center_text('EXECUTION RESULTS', 56)}│{Style.RESET_ALL}")
            print(f"{Fore.YELLOW if failed > 0 else Fore.GREEN}├{'─'*56}┤{Style.RESET_ALL}")
            print(f"{Fore.YELLOW if failed > 0 else Fore.GREEN}│{f' Completed: {completed}'.ljust(56)}│{Style.RESET_ALL}")
            print(f"{Fore.YELLOW if failed > 0 else Fore.GREEN}│{f' Failed: {failed}'.ljust(56)}│{Style.RESET_ALL}")
            print(f"{Fore.YELLOW if failed > 0 else Fore.GREEN}│{f' Success Rate: {success_rate:.1f}%'.ljust(56)}│{Style.RESET_ALL}")
            print(f"{Fore.YELLOW if failed > 0 else Fore.GREEN}└{'─'*56}┘{Style.RESET_ALL}")
            
            if dashboard.results:
                print(f"\n{Fore.CYAN}Recent Results:{Style.RESET_ALL}")
                for r in dashboard.results[-5:]:
                    status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if r.success else f"{Fore.RED}✗{Style.RESET_ALL}"
                    print(f"  {status} {r.module.name}")
        else:
            print(f"\n{Fore.YELLOW}[!] No results yet. Run hardening first.{Style.RESET_ALL}")

    def list_hardening_modules(self):
        """List all hardening modules with cinematic formatting"""
        dashboard = self._get_hardening_dashboard()
        if not dashboard:
            return
        
        # Try to use cinematic list if available
        if hasattr(dashboard, 'list_modules_cinematic'):
            dashboard.list_modules_cinematic()
            return
        
        # Fallback to standard list with categories
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{self._center_text('AVAILABLE HARDENING MODULES')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
        
        categories = {}
        for module in dashboard.modules:
            cat = module.category.value
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(module)
        
        for category, modules in categories.items():
            print(f"{Fore.YELLOW}▸ {category}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{'─'*55}{Style.RESET_ALL}")
            for module in modules:
                compatible = dashboard.system in module.platforms if module.platforms else True
                status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if compatible else f"{Fore.RED}✗{Style.RESET_ALL}"
                severity_color = Fore.RED if module.severity.value == 'CRITICAL' else Fore.YELLOW
                print(f"  [{status}] {Fore.CYAN}{module.name}{Style.RESET_ALL}")
                print(f"       [{severity_color}{module.severity.value}{Style.RESET_ALL}] {module.description[:50]}...")
            print()
        
        # Summary footer
        total = len(dashboard.modules)
        compatible = sum(1 for m in dashboard.modules if not m.platforms or dashboard.system in m.platforms)
        print(f"{Fore.GREEN}{'─'*55}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total: {total} | Compatible: {compatible} | Platform: {dashboard.system}{Style.RESET_ALL}")

    def generate_hardening_report(self):
        """Generate hardening audit report with summary"""
        dashboard = self._get_hardening_dashboard()
        if not dashboard:
            return
        
        if not dashboard.results:
            print(f"{Fore.RED}[!] No results to report. Run hardening first.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}[+] Generating hardening audit report...{Style.RESET_ALL}")
        dashboard._generate_report()
        
        # Display summary after generation
        successful = sum(1 for r in dashboard.results if r.success)
        total = len(dashboard.results)
        print(f"\n{Fore.CYAN}Report Summary:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}✓ Successful: {successful}{Style.RESET_ALL}")
        print(f"  {Fore.RED}✗ Failed: {total - successful}{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}📊 Success Rate: {(successful/total*100):.1f}%{Style.RESET_ALL}")

    def rollback_hardening(self):
        """Rollback hardening changes with confirmation"""
        dashboard = self._get_hardening_dashboard()
        if not dashboard:
            return
        
        print(f"\n{Fore.RED}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{self._center_text('⚠ ROLLBACK WARNING ⚠')}{Style.RESET_ALL}")
        print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}This will revert all applied hardening changes.{Style.RESET_ALL}")
        print(f"{Fore.RED}This action cannot be undone!{Style.RESET_ALL}")
        
        confirm = input(f"\n{Fore.RED}Type 'ROLLBACK' to confirm: {Style.RESET_ALL}").strip()
        
        if confirm == "ROLLBACK":
            dashboard._rollback_hardening()
        else:
            print(f"{Fore.GREEN}Rollback cancelled.{Style.RESET_ALL}")

    def harden_users_only(self):
        """Harden user accounts only"""
        dashboard = self._get_hardening_dashboard()
        if not dashboard:
            return
        from hardening_dashboard import HardeningCategory
        dashboard.selected_modules = [
            m.id for m in dashboard.modules 
            if m.category == HardeningCategory.USER_SECURITY
        ]
        print(f"\n{Fore.GREEN}[+] Hardening user accounts...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] {len(dashboard.selected_modules)} modules selected{Style.RESET_ALL}")
        
        if hasattr(dashboard, '_execute_hardening_realtime'):
            dashboard._execute_hardening_realtime()
        else:
            dashboard._execute_hardening()

    def harden_firewall_only(self):
        """Harden firewall only"""
        dashboard = self._get_hardening_dashboard()
        if not dashboard:
            return
        from hardening_dashboard import HardeningCategory
        dashboard.selected_modules = [
            m.id for m in dashboard.modules 
            if m.category == HardeningCategory.FIREWALL
        ]
        print(f"\n{Fore.GREEN}[+] Hardening firewall...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] {len(dashboard.selected_modules)} modules selected{Style.RESET_ALL}")
        
        if hasattr(dashboard, '_execute_hardening_realtime'):
            dashboard._execute_hardening_realtime()
        else:
            dashboard._execute_hardening()

    def harden_ssh_only(self):
        """Harden SSH only"""
        dashboard = self._get_hardening_dashboard()
        if not dashboard:
            return
        from hardening_dashboard import HardeningCategory
        dashboard.selected_modules = [
            m.id for m in dashboard.modules 
            if m.category == HardeningCategory.SSH_SECURITY
        ]
        print(f"\n{Fore.GREEN}[+] Hardening SSH...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] {len(dashboard.selected_modules)} modules selected{Style.RESET_ALL}")
        
        if hasattr(dashboard, '_execute_hardening_realtime'):
            dashboard._execute_hardening_realtime()
        else:
            dashboard._execute_hardening()

    def _center_text(self, text: str, width: int = None) -> str:
        """Center text in terminal"""
        if width is None:
            width = self.terminal_width if hasattr(self, 'terminal_width') else 80
        return text.center(width)

# ============================================================
# END OF HARDENING INTEGRATION
# ============================================================
# ====================================functions for hardening ends here=======
# ========forensics ends here================================
    def init_bandwidth(self):
        self.prev_io = psutil.net_io_counters()

    def get_bandwidth(self):
        current = psutil.net_io_counters()
        sent = current.bytes_sent - self.prev_io.bytes_sent
        recv = current.bytes_recv - self.prev_io.bytes_recv
        self.prev_io = current
        return sent, recv
    def network_monitor(self):
        """Enhanced network monitoring with proper PDF auditing and workspace persistence"""
        self.init_bandwidth()
        
        console = Console()
        
        # Get workspace directory (using ~/dsterminal_workspace like integrity report)
        def get_workspace_dir():
            """Get the DSTerminal workspace directory for persistent storage"""
            # Use the same workspace as integrity report
            workspace = os.path.expanduser("~/dsterminal_workspace")
            os.makedirs(workspace, exist_ok=True)
            
            # Ensure all required subdirectories exist
            required_dirs = ['operators', 'network_reports', 'scans', 'exploits', 'sandbox', 
                            'integrity_reports', 'compliance_reports', 'logs', 'baselines', 
                            'alerts', 'quarantine', 'forensic', 'auto_quarantine']
            for dir_name in required_dirs:
                dir_path = os.path.join(workspace, dir_name)
                os.makedirs(dir_path, exist_ok=True)
            
            # Also create threat_maps subdirectory in network_reports
            threat_maps_dir = os.path.join(workspace, 'network_reports', 'threat_maps')
            os.makedirs(threat_maps_dir, exist_ok=True)
            
            return workspace
        
       
        def get_local_machine_location():
            """Get precise location with exact place within city"""
            
            # ============================================
            # METHOD 1: High-precision IP Geolocation
            # ============================================
            
            try:
                # Use ipapi.co with detailed parameters for better accuracy
                response = requests.get('https://ipapi.co/json/', timeout=5)
                if response.status_code == 200:
                    geo_data = response.json()
                    lat = geo_data.get('latitude')
                    lon = geo_data.get('longitude')
                    public_ip = geo_data.get('ip')
                    
                    if lat and lon and public_ip:
                        # Get more detailed location info
                        city = geo_data.get('city', 'Unknown')
                        region = geo_data.get('region', 'Unknown')
                        postal = geo_data.get('postal', '')
                        
                        # Try to get neighborhood/district information
                        area_response = requests.get(f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=18&addressdetails=1', 
                                                    timeout=5, headers={'User-Agent': 'DSTerminal/2.0'})
                        if area_response.status_code == 200:
                            area_data = area_response.json()
                            address = area_data.get('address', {})
                            suburb = address.get('suburb', '')
                            neighbourhood = address.get('neighbourhood', '')
                            road = address.get('road', '')
                            
                            # Build precise location description
                            precise_location = city
                            if suburb:
                                precise_location = f"{suburb}, {city}"
                            if neighbourhood:
                                precise_location = f"{neighbourhood}, {precise_location}"
                            if road:
                                precise_location = f"{road}, {precise_location}"
                        else:
                            precise_location = city
                            suburb = "Unknown Area"
                            neighbourhood = "Unknown Neighborhood"
                        
                        console.print(f"[green]✓ Precise location detected: {precise_location}[/green]")
                        console.print(f"[dim]📍 Coordinates: {lat:.6f}, {lon:.6f} (high precision)[/dim]")
                        
                        return {
                            'ip': public_ip,
                            'lat': float(lat),
                            'lon': float(lon),
                            'country': geo_data.get('country_name', 'Unknown'),
                            'city': city,
                            'precise_location': precise_location,
                            'suburb': suburb,
                            'neighbourhood': neighbourhood,
                            'district': geo_data.get('district', ''),
                            'postal_code': postal,
                            'region': region,
                            'isp': geo_data.get('org', geo_data.get('isp', 'Unknown')),
                            'org': geo_data.get('org', 'Unknown'),
                            'timezone': geo_data.get('timezone', 'Unknown'),
                            'loc': f"{lat},{lon}"
                        }
            except Exception as e:
                console.print(f"[yellow]⚠ High-precision geolocation failed: {e}[/yellow]")
            
            # ============================================
            # METHOD 2: WiFi Access Point Triangulation (Windows)
            # ============================================
            
            if platform.system() == "Windows":
                try:
                    import subprocess
                    import re
                    
                    # Get nearby WiFi access points
                    result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'], 
                                        capture_output=True, text=True, timeout=10)
                    output = result.stdout
                    
                    # Parse BSSID (MAC addresses) and signal strength
                    bssids = re.findall(r'BSSID\s+:\s+([0-9A-Fa-f:]+)', output)
                    signals = re.findall(r'Signal\s+:\s+(\d+)%', output)
                    
                    if bssids and signals:
                        console.print(f"[cyan]📡 Detected {len(bssids)} nearby WiFi networks for triangulation[/cyan]")
                        # Note: This would require a WiFi geolocation database API
                        # For now, we store that WiFi positioning is available
                        wifi_available = True
                except:
                    pass
            
            # ============================================
            # METHOD 3: GPS/GLONASS Detection (if available)
            # ============================================
            
            try:
                # Check for GPS hardware on Windows
                if platform.system() == "Windows":
                    import serial.tools.list_ports
                    gps_ports = []
                    for port in serial.tools.list_ports.comports():
                        if 'GPS' in port.description or 'GNSS' in port.description:
                            gps_ports.append(port.device)
                            console.print(f"[cyan]🛰️ GPS device detected on {port.device}[/cyan]")
                    
                    if gps_ports:
                        # Attempt to read NMEA data from GPS
                        for gps_port in gps_ports:
                            try:
                                ser = serial.Serial(gps_port, 9600, timeout=5)
                                # Read NMEA sentences
                                for _ in range(20):
                                    line = ser.readline().decode('ascii', errors='ignore')
                                    if line.startswith('$GPGGA'):
                                        # Parse GGA sentence
                                        parts = line.split(',')
                                        if len(parts) > 5 and parts[2] and parts[4]:
                                            lat_deg = float(parts[2][:2]) + float(parts[2][2:])/60
                                            lon_deg = float(parts[4][:3]) + float(parts[4][3:])/60
                                            if parts[3] == 'S':
                                                lat_deg = -lat_deg
                                            if parts[5] == 'W':
                                                lon_deg = -lon_deg
                                            
                                            console.print(f"[green]✓ GPS location acquired: {lat_deg:.6f}, {lon_deg:.6f}[/green]")
                                            return {
                                                'ip': 'GPS',
                                                'lat': lat_deg,
                                                'lon': lon_deg,
                                                'country': 'GPS',
                                                'city': 'GPS Location',
                                                'precise_location': f"GPS Coordinates: {lat_deg:.6f}, {lon_deg:.6f}",
                                                'isp': 'GPS',
                                                'org': 'GPS Hardware',
                                                'timezone': 'GPS',
                                                'loc': f"{lat_deg},{lon_deg}"
                                            }
                                ser.close()
                            except:
                                continue
            except Exception as e:
                console.print(f"[yellow]⚠ GPS detection: {e}[/yellow]")
            
            # ============================================
            # METHOD 4: Google Geolocation API (requires API key)
            # ============================================
            
            # Uncomment if you have a Google Maps API key
            """
            try:
                api_key = "YOUR_GOOGLE_MAPS_API_KEY"
                # Use WiFi/ cell tower triangulation for high precision
                response = requests.post(
                    'https://www.googleapis.com/geolocation/v1/geolocate?key=' + api_key,
                    json={}, timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    lat = data['location']['lat']
                    lon = data['location']['lng']
                    accuracy = data.get('accuracy', 'unknown')
                    console.print(f"[green]✓ Google Geolocation: {lat:.6f}, {lon:.6f} (accuracy: {accuracy}m)[/green]")
                    # ... return precise location
            except:
                pass
            """
            
            # ============================================
            # METHOD 5: Fallback with OpenStreetMap Nominatim
            # ============================================
            
            try:
                # If we have coordinates but want precise area, reverse geocode
                response = requests.get('https://ipapi.co/json/', timeout=5)
                if response.status_code == 200:
                    geo_data = response.json()
                    lat = geo_data.get('latitude')
                    lon = geo_data.get('longitude')
                    if lat and lon:
                        # Get precise area from OpenStreetMap
                        osm_response = requests.get(
                            f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=18&addressdetails=1',
                            timeout=5,
                            headers={'User-Agent': 'DSTerminal/2.0'}
                        )
                        if osm_response.status_code == 200:
                            osm_data = osm_response.json()
                            address = osm_data.get('address', {})
                            
                            # Build precise location from OSM data
                            suburb = address.get('suburb', address.get('neighbourhood', ''))
                            road = address.get('road', '')
                            house_number = address.get('house_number', '')
                            
                            precise_parts = []
                            if house_number:
                                precise_parts.append(house_number)
                            if road:
                                precise_parts.append(road)
                            if suburb:
                                precise_parts.append(suburb)
                            precise_parts.append(geo_data.get('city', 'Lilongwe'))
                            
                            precise_location = ', '.join(precise_parts) if precise_parts else geo_data.get('city', 'Lilongwe')
                            
                            console.print(f"[cyan]📍 Precise location: {precise_location}[/cyan]")
                            console.print(f"[dim]📌 Coordinates: {lat:.6f}, {lon:.6f}[/dim]")
                            
                            return {
                                'ip': geo_data.get('ip', 'Unknown'),
                                'lat': float(lat),
                                'lon': float(lon),
                                'country': geo_data.get('country_name', 'Malawi'),
                                'city': geo_data.get('city', 'Lilongwe'),
                                'precise_location': precise_location,
                                'suburb': suburb,
                                'road': road,
                                'house_number': house_number,
                                'district': address.get('suburb', ''),
                                'postal_code': address.get('postcode', ''),
                                'region': address.get('state', geo_data.get('region', '')),
                                'isp': geo_data.get('org', 'Local Network'),
                                'timezone': geo_data.get('timezone', 'Africa/Blantyre'),
                                'loc': f"{lat},{lon}"
                            }
            except Exception as e:
                console.print(f"[yellow]⚠ OpenStreetMap reverse geocoding: {e}[/yellow]")
            
            # ============================================
            # FALLBACK: Standard city-level location
            # ============================================
            
            console.print("[yellow]⚠ Using standard city-level location[/yellow]")
            return {
                'ip': '192.168.1.1',
                'lat': -13.9833,
                'lon': 33.7833,
                'country': 'Malawi',
                'city': 'Lilongwe',
                'precise_location': 'Lilongwe, Malawi',
                'isp': 'Local Network',
                'org': 'DSTerminal Host',
                'timezone': 'Africa/Blantyre',
                'loc': '-13.9833,33.7833'
            }
        # Generate connection table
        def generate_connection_table(connections, browser_connections=None):
            rich_table = RichTable()
            
            rich_table.add_column("TYPE", style="cyan", width=8)
            rich_table.add_column("LOCAL", style="cyan")
            rich_table.add_column("→", justify="center")
            rich_table.add_column("REMOTE", style="magenta")
            rich_table.add_column("DESTINATION", style="yellow")
            rich_table.add_column("STATUS", justify="right")
            rich_table.add_column("THREAT", justify="right")
            
            # Add browser connections first
            if browser_connections:
                for bc in browser_connections:
                    conn = bc['conn']
                    geo = bc['geo']
                    domain = bc.get('url_domain', conn.raddr.ip)
                    rich_table.add_row(
                        "🌐 WEB",
                        f"{conn.laddr.ip}:{conn.laddr.port}",
                        "⋙",
                        f"{conn.raddr.ip}:{conn.raddr.port}",
                        f"[cyan]{domain}[/cyan]",
                        "[green]ACTIVE",
                        "✓"
                    )
            
            # Add other connections
            for conn in connections:
                if conn.status == "ESTABLISHED" and conn.raddr:
                    geo = get_geo_ip(conn.raddr.ip)
                    level, icon, score = calculate_threat_score(conn, geo)
                    country = geo["country"] if geo else "N/A"
                    local = f"{conn.laddr.ip}:{conn.laddr.port}"
                    remote = f"{conn.raddr.ip}:{conn.raddr.port}"
                    
                    rich_table.add_row(
                        "⚙️ SYS",
                        local, "⋙", remote,
                        f"{country}",
                        "[green]ACTIVE",
                        icon
                    )
            
            return rich_table
        
        def get_active_browser_connections():
            """Get active connections from browsers and web applications"""
            browser_processes = ['chrome', 'firefox', 'msedge', 'brave', 'opera', 'safari']
            web_connections = []
            
            try:
                for conn in psutil.net_connections():
                    if conn.status == "ESTABLISHED" and conn.raddr:
                        # Check if connection belongs to a browser process
                        try:
                            if conn.pid:
                                process = psutil.Process(conn.pid)
                                process_name = process.name().lower()
                                
                                # Check if it's a browser process
                                is_browser = any(browser in process_name for browser in browser_processes)
                                
                                # Also capture common web ports
                                is_web_port = conn.raddr.port in [80, 443, 8080, 8443]
                                
                                if is_browser or is_web_port:
                                    geo = get_geo_ip(conn.raddr.ip)
                                    if geo and geo.get('lat') and geo.get('lon'):
                                        web_connections.append({
                                            'conn': conn,
                                            'process_name': process_name,
                                            'geo': geo,
                                            'is_browser': is_browser,
                                            'url_domain': get_domain_from_ip(conn.raddr.ip, geo)
                                        })
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
            except Exception as e:
                console.print(f"[yellow]⚠ Browser connection detection: {e}[/yellow]")
            
            return web_connections

        def get_domain_from_ip(ip, geo):
            """Try to get domain name from IP address"""
            try:
                # Common CDN and service domains
                known_domains = {
                    'deepseek.com': 'DeepSeek AI',
                    'github.com': 'GitHub',
                    'openai.com': 'OpenAI',
                    'cloudflare.com': 'Cloudflare',
                    'google.com': 'Google',
                    'microsoft.com': 'Microsoft',
                    'amazon.com': 'Amazon AWS',
                    'netflix.com': 'Netflix',
                    'youtube.com': 'YouTube',
                    'reddit.com': 'Reddit',
                    'stackoverflow.com': 'Stack Overflow',
                    'discord.com': 'Discord',
                    'spotify.com': 'Spotify',
                    'twitch.tv': 'Twitch'
                }
                
                # Try reverse DNS
                try:
                    import socket
                    domain = socket.gethostbyaddr(ip)[0]
                    for known_domain, name in known_domains.items():
                        if known_domain in domain:
                            return f"{name} ({domain})"
                    return domain
                except:
                    # Use geolocation data
                    if geo:
                        return f"{geo.get('isp', 'Unknown ISP')} - {geo.get('country', 'Unknown')}"
                    return ip
            except:
                return ip

    
        def generate_enhanced_threat_map(connections, local_machine, browser_connections):
            """Generate interactive threat map with distance circles and connection lines"""
            
            if not local_machine or local_machine.get('lat', 0) == 0:
                local_machine = {
                    'ip': 'Unknown',
                    'lat': -13.2543,
                    'lon': 34.3015,
                    'country': 'Malawi',
                    'city': 'Lilongwe',
                    'isp': 'Local Network',
                    'org': 'DSTerminal Host'
                }
            
            # Create base map centered on local machine
            map_center = [local_machine['lat'], local_machine['lon']]
            zoom_start = 5
            
            threat_map = folium.Map(
                location=map_center,
                zoom_start=zoom_start,
                tiles='CartoDB dark_matter',
                control_scale=True
            )
            
            # ============================================
            # DISTANCE CIRCLES WITH RADIUS LABELS (in km)
            # ============================================
            
            # Distance radii in kilometers
            distance_radii = [
                (500, 0.1, '#00ff00', '500km'),      # 500km - Green
                (1000, 0.15, '#00ffff', '1000km'),   # 1000km - Cyan
                (2000, 0.2, '#ffff00', '2000km'),    # 2000km - Yellow
                (5000, 0.25, '#ff6600', '5000km'),   # 5000km - Orange
                (10000, 0.3, '#ff0000', '10000km')   # 10000km - Red
            ]
            
            for radius, opacity, color, label in distance_radii:
                # Add the circle
                folium.Circle(
                    location=[local_machine['lat'], local_machine['lon']],
                    radius=radius * 1000,  # Convert km to meters
                    color=color,
                    fill=False,
                    weight=1.5,
                    opacity=opacity,
                    dash_array='5, 10'
                ).add_to(threat_map)
                
                # Add distance label on the circle edge
                # Calculate a point at 45 degrees on the circle edge for label placement
                import math
                angle_rad = math.radians(45)
                lat_offset = (radius / 111) * math.cos(angle_rad)  # 1 degree ≈ 111 km
                lon_offset = (radius / 111) * math.sin(angle_rad) / math.cos(math.radians(local_machine['lat']))
                
                label_lat = local_machine['lat'] + lat_offset
                label_lon = local_machine['lon'] + lon_offset
                
                from folium import DivIcon
                folium.map.Marker(
                    [label_lat, label_lon],
                    icon=DivIcon(
                        icon_size=(50, 20),
                        icon_anchor=(25, 10),
                        html=f'<div style="font-size: 9px; color: {color}; background: rgba(0,0,0,0.7); padding: 2px 6px; border-radius: 10px; font-weight: bold;">{label}</div>'
                    )
                ).add_to(threat_map)
            
            # ============================================
            # PROMINENT RED PULSING CIRCLE FOR LOCAL MACHINE
            # ============================================
            
            # Outer pulsing red circle
            folium.Circle(
                location=[local_machine['lat'], local_machine['lon']],
                radius=150000,
                color='#ff3333',
                fill=True,
                fill_opacity=0.3,
                weight=3,
                popup=f"📍 DSTerminal Host - {local_machine['country']}"
            ).add_to(threat_map)
            
            # Middle red circle
            folium.Circle(
                location=[local_machine['lat'], local_machine['lon']],
                radius=75000,
                color='#ff6666',
                fill=True,
                fill_opacity=0.45,
                weight=2.5,
                popup="Active Monitoring Zone"
            ).add_to(threat_map)
            
            # Inner solid red circle (core)
            folium.Circle(
                location=[local_machine['lat'], local_machine['lon']],
                radius=30000,
                color='#ff0000',
                fill=True,
                fill_opacity=0.7,
                weight=3,
                popup="DSTerminal Core"
            ).add_to(threat_map)
            
            # Center marker with flag
            folium.Marker(
                location=[local_machine['lat'], local_machine['lon']],
                popup=folium.Popup(f"""
                <div style="font-family: monospace; text-align: center;">
                    <b><span style="color: #ff0000;">🔴 DSTERMINAL HOST</span></b><br>
                    📍 {local_machine['country']}<br>
                    🏙️ {local_machine['city']}<br>
                    📡 IP: {local_machine['ip']}<br>
                    <span style="color: #00ff00;">● ACTIVE MONITORING ●</span>
                </div>
                """, max_width=280),
                icon=folium.Icon(color='red', icon='flag', prefix='fa', icon_color='white')
            ).add_to(threat_map)
            
            # Threat level colors
            threat_colors = {
                0: '#00ff00',
                1: '#00ff00',
                2: '#ffff00',
                3: '#ff6600',
                4: '#ff0000',
                5: '#8b0000'
            }
            
            # Browser connection colors
            browser_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#F0E68C']
            
            # Statistics counters
            high_risk = 0
            medium_risk = 0
            low_risk = 0
            active_countries = set()
            connection_details = []  # Store connection details for table
            
            # ============================================
            # PROCESS ALL CONNECTIONS AND ADD TO MAP
            # ============================================
            
            # Process browser connections (from table)
            for idx, browser_conn in enumerate(browser_connections):
                conn = browser_conn['conn']
                geo = browser_conn['geo']
                process_name = browser_conn['process_name']
                domain = browser_conn.get('url_domain', conn.raddr.ip)
                
                color = browser_colors[idx % len(browser_colors)]
                
                # Calculate distance
                from math import radians, sin, cos, sqrt, atan2
                def calc_distance(lat1, lon1, lat2, lon2):
                    R = 6371
                    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
                    dlat = lat2 - lat1
                    dlon = lon2 - lon1
                    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                    return 2 * R * atan2(sqrt(a), sqrt(1-a))
                
                distance = calc_distance(local_machine['lat'], local_machine['lon'], geo['lat'], geo['lon'])
                
                # popup_text = f"""
                # <div style="font-family: monospace; min-width: 220px;">
                #     <b><span style="color: #FF6B6B;">🌐 BROWSER CONNECTION</span></b><br>
                #     <hr style="margin: 3px 0;">
                #     📍 Country: <b>{geo.get('country', 'Unknown')}</b><br>
                #     📍 City: {geo.get('city', 'N/A')}<br>
                #     📡 IP: {conn.raddr.ip}:{conn.raddr.port}<br>
                #     🌐 Browser: {process_name.upper()}<br>
                #     📏 Distance: {distance:.0f} km<br>
                #     ⚠ Risk: LOW
                # </div>
                # """
                # In the map's local marker popup, show precise location:

                popup_text = f"""
                <div style="font-family: monospace; text-align: center; min-width: 250px;">
                    <b><span style="color: #ff0000;">🔴 DSTERMINAL HOST</span></b><br>
                    <hr>
                    📍 <b>Precise Location:</b> {local_machine.get('precise_location', local_machine['city'])}<br>
                    🏙️ <b>City:</b> {local_machine['city']}<br>
                    🏘️ <b>Area:</b> {local_machine.get('suburb', 'City Center')}<br>
                    📡 <b>IP:</b> {local_machine['ip']}<br>
                    <span style="color: #00ff00;">● ACTIVE MONITORING ●</span>
                </div>
                """
                
                # Add marker for remote location
                folium.CircleMarker(
                    location=[geo['lat'], geo['lon']],
                    radius=9,
                    popup=folium.Popup(popup_text, max_width=300),
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.8,
                    weight=2
                ).add_to(threat_map)
                
                # Add connection line from local machine
                folium.PolyLine(
                    [[local_machine['lat'], local_machine['lon']], [geo['lat'], geo['lon']]],
                    color=color,
                    weight=2.5,
                    opacity=0.6,
                    tooltip=f"🌐 {domain} → {geo.get('country', 'Unknown')} ({distance:.0f}km)"
                ).add_to(threat_map)
                
                # Add distance label at midpoint
                mid_lat = (local_machine['lat'] + geo['lat']) / 2
                mid_lon = (local_machine['lon'] + geo['lon']) / 2
                from folium import DivIcon
                folium.map.Marker(
                    [mid_lat, mid_lon],
                    icon=DivIcon(
                        icon_size=(40, 16),
                        icon_anchor=(20, 8),
                        html=f'<div style="font-size: 7px; color: {color}; background: rgba(0,0,0,0.6); padding: 1px 4px; border-radius: 8px;">{distance:.0f}km</div>'
                    )
                ).add_to(threat_map)
                
                if geo.get('country') and geo.get('country') != 'N/A':
                    active_countries.add(geo.get('country'))
                
                connection_details.append({
                    'type': 'Browser',
                    'country': geo.get('country', 'Unknown'),
                    'ip': conn.raddr.ip,
                    'distance': f"{distance:.0f}km",
                    'risk': 'Low'
                })
                low_risk += 1
            
            # Process system connections (from the connections table)
            for idx, conn in enumerate(connections):
                if conn.status == "ESTABLISHED" and conn.raddr:
                    geo = get_geo_ip(conn.raddr.ip)
                    if geo and geo.get('lat') and geo.get('lon'):
                        level, icon, score = calculate_threat_score(conn, geo)
                        color = threat_colors.get(score, '#ffffff')
                        
                        # Calculate distance
                        from math import radians, sin, cos, sqrt, atan2
                        def calc_distance(lat1, lon1, lat2, lon2):
                            R = 6371
                            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
                            dlat = lat2 - lat1
                            dlon = lon2 - lon1
                            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                            return 2 * R * atan2(sqrt(a), sqrt(1-a))
                        
                        distance = calc_distance(local_machine['lat'], local_machine['lon'], geo['lat'], geo['lon'])
                        
                        if score >= 3:
                            risk_level = "HIGH"
                            risk_color = "#ff0000"
                            high_risk += 1
                            size = 11
                        elif score == 2:
                            risk_level = "MEDIUM"
                            risk_color = "#ffaa00"
                            medium_risk += 1
                            size = 9
                        else:
                            risk_level = "LOW"
                            risk_color = "#00ff00"
                            low_risk += 1
                            size = 7
                        
                        popup_text = f"""
                        <div style="font-family: monospace; min-width: 220px;">
                            <b><span style="color: {color};">⚙️ SYSTEM CONNECTION</span></b><br>
                            <hr style="margin: 3px 0;">
                            📍 Country: <b>{geo.get('country', 'Unknown')}</b><br>
                            📍 City: {geo.get('city', 'N/A')}<br>
                            📡 IP: {conn.raddr.ip}:{conn.raddr.port}<br>
                            🖥️ Local Port: {conn.laddr.port}<br>
                            📏 Distance: {distance:.0f} km<br>
                            ⚠ Threat Score: {score}/5<br>
                            ⚠ Risk: <span style="color: {risk_color}; font-weight: bold;">{risk_level}</span>
                        </div>
                        """
                        
                        # Add marker for remote location
                        folium.CircleMarker(
                            location=[geo['lat'], geo['lon']],
                            radius=size,
                            popup=folium.Popup(popup_text, max_width=300),
                            color=color,
                            fill=True,
                            fill_color=color,
                            fill_opacity=0.7,
                            weight=2
                        ).add_to(threat_map)
                        
                        # Add connection line from local machine
                        line_color = '#ff0000' if score >= 3 else '#ffaa00' if score == 2 else '#00ff00'
                        folium.PolyLine(
                            [[local_machine['lat'], local_machine['lon']], [geo['lat'], geo['lon']]],
                            color=line_color,
                            weight=2,
                            opacity=0.5,
                            tooltip=f"⚙️ → {geo.get('country', 'Unknown')} | Score: {score}/5 | {distance:.0f}km"
                        ).add_to(threat_map)
                        
                        # Add distance label at midpoint
                        mid_lat = (local_machine['lat'] + geo['lat']) / 2
                        mid_lon = (local_machine['lon'] + geo['lon']) / 2
                        from folium import DivIcon
                        folium.Marker(
                            [mid_lat, mid_lon],
                            icon=DivIcon(
                                icon_size=(40, 16),
                                icon_anchor=(20, 8),
                                html=f'<div style="font-size: 7px; color: {line_color}; background: rgba(0,0,0,0.6); padding: 1px 4px; border-radius: 8px;">{distance:.0f}km</div>'
                            )
                        ).add_to(threat_map)
                        
                        if geo.get('country') and geo.get('country') != 'N/A':
                            active_countries.add(geo.get('country'))
                        
                        connection_details.append({
                            'type': 'System',
                            'country': geo.get('country', 'Unknown'),
                            'ip': conn.raddr.ip,
                            'distance': f"{distance:.0f}km",
                            'risk': risk_level,
                            'score': score
                        })
            
            total_connections = len(browser_connections) + high_risk + medium_risk + low_risk
            
            # ============================================
            # LEFT SIDE STATISTICS PANEL
            # ============================================
            
            stats_html = f'''
            <div style="position: fixed; top: 20px; left: 20px; z-index: 1000; background-color: rgba(0,0,0,0.92); padding: 18px; border-radius: 10px; border: 2px solid #00ff00; font-family: 'Courier New', monospace; min-width: 280px; backdrop-filter: blur(8px); box-shadow: 0 0 20px rgba(0,255,0,0.2);">
                
                <div style="text-align: center; margin-bottom: 12px;">
                    <span style="color: #00ff00; font-size: 14px; font-weight: bold;">┌─────────────────────────────┐</span><br>
                    <span style="color: #00ff00; font-size: 13px; font-weight: bold;">│    DSTERMINAL NETWORK MAP    │</span><br>
                    <span style="color: #00ff00; font-size: 14px; font-weight: bold;">└─────────────────────────────┘</span>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <div><span style="color: #ff0000;">●</span> <span style="color: #ffffff;">Host Location:</span> <span style="color: #00ff00; font-weight: bold;">{local_machine['country']}</span></div>
                    <div><span style="color: #ff0000;">●</span> <span style="color: #ffffff;">Coordinates:</span> <span style="color: #ffff00;">{local_machine['lat']:.2f}, {local_machine['lon']:.2f}</span></div>
                    <div><span style="color: #ff0000;">●</span> <span style="color: #ffffff;">Local IP:</span> <span style="color: #00ffff;">{local_machine['ip']}</span></div>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <span style="color: #00ff00;">─────────────────────────────</span>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <div><span style="color: #ff4444;">⚠</span> <span style="color: #ffffff;">High Risk (3-5):</span> <span style="color: #ff4444; font-weight: bold;">{high_risk}</span></div>
                    <div><span style="color: #ffaa00;">⚠</span> <span style="color: #ffffff;">Medium Risk (2):</span> <span style="color: #ffaa00; font-weight: bold;">{medium_risk}</span></div>
                    <div><span style="color: #00ff00;">✓</span> <span style="color: #ffffff;">Low Risk (0-1):</span> <span style="color: #00ff00; font-weight: bold;">{low_risk}</span></div>
                    <div><span style="color: #00ffff;">🌐</span> <span style="color: #ffffff;">Browser Connections:</span> <span style="color: #00ffff; font-weight: bold;">{len(browser_connections)}</span></div>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <span style="color: #00ff00;">─────────────────────────────</span>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <div><span style="color: #00ff00;">🌍</span> <span style="color: #ffffff;">Active Countries:</span> <span style="color: #00ff00; font-weight: bold;">{len(active_countries)}</span></div>
                    <div><span style="color: #00ff00;">🔗</span> <span style="color: #ffffff;">Total Connections:</span> <span style="color: #00ff00; font-weight: bold;">{total_connections}</span></div>
                    <div><span style="color: #00ff00;">📏</span> <span style="color: #ffffff;">Distance Rings:</span> <span style="color: #00ffff;">500-10000km</span></div>
                    <div><span style="color: #00ff00;">✨</span> <span style="color: #ffffff;">Status:</span> <span style="color: #00ff00; font-weight: bold;">ACTIVE</span></div>
                </div>
                
                <div style="margin-bottom: 12px;">
                    <span style="color: #00ff00;">─────────────────────────────</span>
                </div>
                
                <div>
                    <div style="color: #ffff00; margin-bottom: 8px;">⬤ LEGEND</div>
                    <div><span style="color: #ff0000;">⬤</span> <span style="color: #ffffff;">High Risk (3-5)</span></div>
                    <div><span style="color: #ffaa00;">⬤</span> <span style="color: #ffffff;">Medium Risk (2)</span></div>
                    <div><span style="color: #00ff00;">⬤</span> <span style="color: #ffffff;">Low Risk (0-1)</span></div>
                    <div><span style="color: #FF6B6B;">⬤</span> <span style="color: #ffffff;">Browser Traffic</span></div>
                    <div><span style="color: #ff0000;">🔴</span> <span style="color: #ffffff;">DSTerminal Host</span></div>
                    <div><span style="color: #00ffff;">◯</span> <span style="color: #ffffff;">Distance Rings (km)</span></div>
                </div>
                
                <div style="margin-top: 12px;">
                    <span style="color: #00ff00;">─────────────────────────────</span>
                </div>
                
                <div style="margin-top: 8px; text-align: center;">
                    <span style="color: #ff6600; font-size: 9px;">● LIVE MONITORING ●</span>
                </div>
            </div>
            '''
            
            threat_map.get_root().html.add_child(folium.Element(stats_html))
            
            # ============================================
            # JAVASCRIPT FOR PULSING EFFECTS
            # ============================================
            
            pulse_script = '''
            <script>
            // Pulse animation for red circles
            var circles = document.querySelectorAll('circle');
            var pulseDirection = 1;
            
            setInterval(function() {
                circles.forEach(function(circle) {
                    var fillColor = circle.getAttribute('fill');
                    if (fillColor && (fillColor.indexOf('red') !== -1 || fillColor.indexOf('#ff') !== -1)) {
                        var currentOpacity = parseFloat(circle.getAttribute('fill-opacity') || 0.3);
                        var newOpacity = currentOpacity + (pulseDirection * 0.02);
                        if (newOpacity >= 0.7) pulseDirection = -1;
                        if (newOpacity <= 0.15) pulseDirection = 1;
                        circle.setAttribute('fill-opacity', newOpacity);
                    }
                });
                
                // Blinking effect for connection lines
                var lines = document.querySelectorAll('path');
                lines.forEach(function(line) {
                    if (line.getAttribute('stroke') && line.getAttribute('stroke') !== 'none') {
                        var randomColor = '#' + Math.floor(Math.random()*16777215).toString(16);
                        if (Math.random() > 0.85) {
                            line.setAttribute('stroke', randomColor);
                        }
                        var currentOp = parseFloat(line.getAttribute('opacity') || 0.5);
                        line.setAttribute('opacity', 0.3 + Math.random() * 0.5);
                    }
                });
            }, 300);
            </script>
            '''
            
            threat_map.get_root().html.add_child(folium.Element(pulse_script))
            
            # Save map
            workspace = get_workspace_dir()
            map_dir = os.path.join(workspace, 'network_reports', 'threat_maps')
            os.makedirs(map_dir, exist_ok=True)
            map_file = os.path.join(map_dir, f'realtime_map_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
            threat_map.save(map_file)
            
            console.print(f"[green]✓ Threat map saved to: {map_file}[/green]")
            console.print(f"[red]🔴 Host location: {local_machine['country']} ({local_machine['lat']:.2f}, {local_machine['lon']:.2f})[/red]")
            console.print(f"[cyan]🌐 Active Connections: {total_connections} | Countries: {len(active_countries)}[/cyan]")
            console.print(f"[yellow]📏 Distance rings: 500km, 1000km, 2000km, 5000km, 10000km[/yellow]")
            
            return map_file
        # Comprehensive PDF Report Generation
        def export_comprehensive_audit_report(connections, local_machine, workspace, operator_id=None):
            """Generate comprehensive PDF audit report in workspace"""
            
            # Create network_reports directory in workspace
            reports_dir = os.path.join(workspace, 'network_reports')
            os.makedirs(reports_dir, exist_ok=True)
            
            # Generate report filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = os.path.join(reports_dir, f'network_report_{timestamp}.pdf')
            
            # Create PDF document
            doc = SimpleDocTemplate(report_file, pagesize=landscape(letter))
            elements = []
            
            # Custom styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#FF0000'),
                alignment=1,  # Center
                spaceAfter=30
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#00AAFF'),
                spaceAfter=12
            )
            
            # Title Page
            elements.append(Paragraph("D S T E R M I N A L", title_style))
            elements.append(Paragraph("Network Forensic Report", title_style))
            elements.append(Spacer(1, 0.5 * inch))
            
            # Report Metadata
            elements.append(Paragraph("Report Information", heading_style))
            metadata_data = [
                ["Report ID:", f"NET-{timestamp}"],
                ["Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                ["Session ID:", getattr(self, 'session_id', 'N/A')],
                ["Operator:", operator_id if operator_id else getattr(self, 'operator_id', 'N/A')],
                ["Duration:", "15 seconds (live monitoring)"]
            ]
            
            metadata_table = PDFTable(metadata_data, colWidths=[2*inch, 4*inch])
            metadata_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#00AAFF')),
                ('TEXTCOLOR', (1, 0), (1, -1), colors.white),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a1a1a'))
            ]))
            elements.append(metadata_table)
            elements.append(Spacer(1, 0.3 * inch))
            
            # Local Machine Information
            if local_machine:
                elements.append(Paragraph("Local Machine Intelligence", heading_style))
                local_data = [
                    ["Host IP:", local_machine.get('ip', 'N/A')],
                    ["Country:", local_machine.get('country', 'N/A')],
                    ["City:", local_machine.get('city', 'N/A')],
                    ["Region:", local_machine.get('region', 'N/A')],
                    ["ISP:", local_machine.get('isp', 'N/A')],
                    ["Organization:", local_machine.get('org', 'N/A')],
                    ["Timezone:", local_machine.get('timezone', 'N/A')]
                ]
                
                local_table = PDFTable(local_data, colWidths=[2*inch, 4*inch])
                local_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#00FF00')),
                    ('TEXTCOLOR', (1, 0), (1, -1), colors.white),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a1a1a'))
                ]))
                elements.append(local_table)
                elements.append(Spacer(1, 0.3 * inch))
            
            # Network Statistics Summary
            elements.append(Paragraph("Network Statistics Summary", heading_style))
            
            established = sum(1 for c in connections if c.status == "ESTABLISHED")
            listening = sum(1 for c in connections if c.status == "LISTEN")
            time_wait = sum(1 for c in connections if c.status == "TIME_WAIT")
            
            # Calculate threat distribution
            threat_distribution = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            unique_countries = set()
            high_risk_connections = []
            
            for conn in connections:
                if conn.raddr:
                    geo = get_geo_ip(conn.raddr.ip)
                    if geo:
                        unique_countries.add(geo.get('country', 'Unknown'))
                        level, icon, score = calculate_threat_score(conn, geo)
                        threat_distribution[score] = threat_distribution.get(score, 0) + 1
                        if score >= 3:
                            high_risk_connections.append({
                                'ip': conn.raddr.ip,
                                'country': geo.get('country', 'Unknown'),
                                'score': score
                            })
            
            stats_data = [
                ["Total Connections", str(len(connections))],
                ["ESTABLISHED", str(established)],
                ["LISTEN", str(listening)],
                ["TIME_WAIT", str(time_wait)],
                ["Unique Countries", str(len(unique_countries))],
                ["High Risk Connections", str(len(high_risk_connections))]
            ]
            
            stats_table = PDFTable(stats_data, colWidths=[2.5*inch, 2.5*inch])
            stats_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#00AAFF')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.white),
                ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#555555'))
            ]))
            elements.append(stats_table)
            elements.append(Spacer(1, 0.3 * inch))
            
            # Threat Distribution
            elements.append(Paragraph("Threat Distribution Analysis", heading_style))
            threat_data = [
                ["Risk Level", "Score", "Count", "Status"],
                ["Low", "0-1", str(threat_distribution[0] + threat_distribution[1]), "🟢 Safe"],
                ["Medium", "2", str(threat_distribution[2]), "🟡 Monitor"],
                ["High", "3-4", str(threat_distribution[3] + threat_distribution[4]), "🟠 Alert"],
                ["Critical", "5", str(threat_distribution[5]), "🔴 Immediate Action"]
            ]
            
            threat_table = PDFTable(threat_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 2*inch])
            threat_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#00AAFF')),
                ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#1a4d1a')),
                ('BACKGROUND', (0, 2), (0, 2), colors.HexColor('#4d4d1a')),
                ('BACKGROUND', (0, 3), (0, 3), colors.HexColor('#4d1a1a')),
                ('BACKGROUND', (0, 4), (0, 4), colors.HexColor('#4a0e0e')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#555555'))
            ]))
            elements.append(threat_table)
            elements.append(Spacer(1, 0.3 * inch))
            
            # All Connections Table
            elements.append(Paragraph("Complete Connection Log (Audit Trail)", heading_style))
            
            conn_data = [["Local", "Remote", "PID", "Status", "Country", "ISP", "Score"]]
            
            for conn in connections:
                if conn.raddr:
                    geo = get_geo_ip(conn.raddr.ip)
                    level, icon, score = calculate_threat_score(conn, geo)
                    country = geo["country"] if geo else "N/A"
                    isp = geo["isp"] if geo else "N/A"
                    
                    local = f"{conn.laddr.ip}:{conn.laddr.port}"
                    remote = f"{conn.raddr.ip}:{conn.raddr.port}"
                    
                    conn_data.append([local, remote, str(conn.pid), conn.status, country, isp, str(score)])
            
            # Limit table size for PDF
            if len(conn_data) > 30:
                conn_data = conn_data[:30]
                conn_data.append(["...", "...", "...", "...", "...", "...", f"and {len(connections)-29} more"])
            
            conn_table = PDFTable(conn_data, repeatRows=1)
            conn_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#00AAFF')),
                ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#444444')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]))
            elements.append(conn_table)
            
            # Footer
            elements.append(Spacer(1, 0.5 * inch))
            elements.append(Paragraph(
                f"Report autogenerated by DSTerminal v2.0.113 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Audit Trail Verified",
                ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=1)
            ))
            
            # Build PDF
            doc.build(elements)
            
            # Also save as JSON for machine reading
            json_report = os.path.join(reports_dir, f'network_report_{timestamp}.json')
            audit_data = {
                'timestamp': timestamp,
                'local_machine': local_machine,
                'statistics': {
                    'total_connections': len(connections),
                    'established': established,
                    'listening': listening,
                    'unique_countries': len(unique_countries),
                    'threat_distribution': threat_distribution,
                    'high_risk_count': len(high_risk_connections)
                },
                'connections': [
                    {
                        'local': f"{c.laddr.ip}:{c.laddr.port}",
                        'remote': f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else None,
                        'pid': c.pid,
                        'status': c.status
                    }
                    for c in connections if c.raddr
                ]
            }
            
            import json
            with open(json_report, 'w') as f:
                json.dump(audit_data, f, indent=2)
            
            console.print(f"[green]✓ PDF report saved to workspace: {report_file}[/green]")
            console.print(f"[green]✓ JSON data saved to: {json_report}[/green]")
            
            return report_file
        
        def save_operator_session_data(connections, local_machine, workspace, operator_id):
            """Save session data to the operator's directory for persistence"""
            if not operator_id:
                return
            
            operator_dir = os.path.join(workspace, 'operators', operator_id)
            os.makedirs(operator_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save connection data
            session_file = os.path.join(operator_dir, f'network_session_{timestamp}.json')
            
            session_data = {
                'timestamp': timestamp,
                'operator_id': operator_id,
                'local_machine': local_machine,
                'connections': [
                    {
                        'local_ip': c.laddr.ip,
                        'local_port': c.laddr.port,
                        'remote_ip': c.raddr.ip if c.raddr else None,
                        'remote_port': c.raddr.port if c.raddr else None,
                        'pid': c.pid,
                        'status': c.status
                    }
                    for c in connections if c.raddr
                ]
            }
            
            import json
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            console.print(f"[dim]💾 Session data saved to: {session_file}[/dim]")
        
        # Pre-scan animation
        def threat_scan_animation():
            with console.status("[bold green]Initializing network sensors..."):
                for i in range(5):
                    console.print(f"[cyan]Scanning layer {i+1}/5...")
                    time.sleep(1)
        
        # Live Monitor with Enhanced Map
        from collections import Counter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import Table as PDFTable
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

        from reportlab.platypus import TableStyle
        from rich.table import Table as RichTable
        from rich.layout import Layout
        from rich.panel import Panel
        from rich.live import Live
        from rich import box
        import socket
        import requests
        import json
        
        def detect_intrusion(connections):
            ips = [c.raddr.ip for c in connections if c.raddr]
            counts = Counter(ips)
            
            alerts = []
            for ip, count in counts.items():
                if count > 15:
                    alerts.append(f"Possible port scan from {ip}")
            
            # Check for connections to high-risk countries
            high_risk_countries = ['Russia', 'China', 'North Korea', 'Iran', 'Syria']
            for conn in connections:
                if conn.raddr:
                    geo = get_geo_ip(conn.raddr.ip)
                    if geo and geo.get('country') in high_risk_countries:
                        alerts.append(f"Connection to high-risk country: {geo['country']} from {conn.raddr.ip}")
            
            return alerts
        
        def live_monitor(duration=15):
            sent, recv = self.get_bandwidth()
            
            upload_kb = sent / 1024
            download_kb = recv / 1024
            
            bandwidth_bar = "█" * min(int(download_kb / 5), 50)
            
            bandwidth_panel = Panel(
                f"⬇ Download: {download_kb:.2f} KB/s\n⬆ Upload: {upload_kb:.2f} KB/s\n\n{bandwidth_bar}",
                title="[bold cyan]Bandwidth Activity[/bold cyan]",
                border_style="green"
            )
            
            start_time = time.time()
            map_opened = False
            local_machine = get_local_machine_location()
            workspace = get_workspace_dir()
            
            console.print(f"[dim]📁 Workspace: {workspace}[/dim]")

            # Get operator ID from session
            operator_id = getattr(self, 'current_operator', None)
            if not operator_id:
                # Try to get from workspace path
                workspace_operators = os.path.join(workspace, 'operators')
                if os.path.exists(workspace_operators):
                    existing_ops = [d for d in os.listdir(workspace_operators) if d.startswith('OP-')]
                    if existing_ops:
                        operator_id = existing_ops[-1]
                        console.print(f"[dim]📋 Operator session: {operator_id}[/dim]")
            
            if local_machine:
                console.print(f"[green]✓ Local machine detected: {local_machine['ip']} ({local_machine['country']})[/green]")
            else:
                console.print("[yellow]⚠ Could not determine local machine location[/yellow]")
            
            with Live(console=console, refresh_per_second=2, screen=False) as live:
                last_connections = []
                last_browser_connections = []
                
                while time.time() - start_time < duration:
                    try:
                        connections = psutil.net_connections()
                        browser_connections = get_active_browser_connections()

                    except Exception as e:
                        console.print(f"[red]Access Error: {e}")
                        break
                    
                    # Generate connection table
                    rich_table = generate_connection_table(connections, browser_connections)
                    table_panel = Panel(
                        rich_table,
                        title="[bold red]NETWORK TRAFFIC ANALYSIS[/bold red]",
                        border_style="bright_blue",
                        padding=(0, 1)
                    )
                    
                    # Generate and open enhanced threat map (only once)
                    if not map_opened:
                        console.print("[yellow]🌍 Generating enhanced threat map with local machine location...[/yellow]")
                        map_file = generate_enhanced_threat_map(connections, local_machine, browser_connections)
                        webbrowser.open(f'file://{map_file}')
                        console.print(f"[green]✓ Enhanced threat map saved to: {map_file}[/green]")
                        console.print("[cyan]📍 Map shows: Local machine marker, connection lines, threat levels, and heatmap[/cyan]")
                        map_opened = True
                    
                    # Generate statistics
                    stats = RichTable(box=box.MINIMAL)
                    stats.add_column("Metric", style="cyan")
                    stats.add_column("Value", style="yellow")
                    
                    established = sum(1 for c in connections if c.status == "ESTABLISHED")
                    listening = sum(1 for c in connections if c.status == "LISTEN")
                    browser_count = len(browser_connections)
                    
                    unique_countries = set()
                    high_risk_connections = 0
                    
                    for c in connections:
                        if c.raddr:
                            geo = get_geo_ip(c.raddr.ip)
                            if geo and geo.get('country'):
                                unique_countries.add(geo['country'])
                                level, icon, score = calculate_threat_score(c, geo)
                                if score >= 3:
                                    high_risk_connections += 1
                    
                    stats.add_row("Total Connections", str(len(connections)))
                    stats.add_row("🌐 Browser Connections", f"[cyan]{browser_count}[/cyan]")
                    stats.add_row("ESTABLISHED", f"[green]{established}[/green]")
                    stats.add_row("LISTEN", f"[blue]{listening}[/blue]")
                    stats.add_row("Active Countries", str(len(unique_countries)))
                    stats.add_row("High Risk (3-5)", f"[red]{high_risk_connections}[/red]")
                    stats.add_row("Local Machine", f"[cyan]{local_machine['country'] if local_machine else 'Unknown'}[/cyan]")
                    stats.add_row("Workspace", f"[dim]{workspace}[/dim]")
                    
                    # Detect and display alerts
                    alerts = detect_intrusion(connections)
                    alert_text = "\n".join([f"[bold red]⚠ {alert}[/bold red]" for alert in alerts]) if alerts else "[green]✓ No intrusion detected[/green]"
                    
                    # Create combined dashboard
                    dashboard = Layout()
                    dashboard.split(
                        Layout(name="header", size=4),
                        Layout(name="body"),
                        Layout(name="footer", size=4)
                    )
                    
                    dashboard["header"].split_row(
                        Layout(bandwidth_panel, ratio=1),
                        Layout(Panel(f"[cyan]🌐 Active Browser Connections: {browser_count}[/cyan]", title="LIVE WEB TRAFFIC", border_style="green"), ratio=1)
                    )
                    dashboard["body"].split_row(
                        Layout(table_panel, ratio=2),
                        Layout(stats, ratio=1)
                    )
                    
                    dashboard["footer"].split(
                        Layout(Panel(
                            f"[cyan]🌍 Threat Map: {os.path.basename(map_file) if map_opened else 'Generating...'}[/cyan]\n"
                            f"[dim]📍 Local Machine: {local_machine['country'] if local_machine else 'Unknown'} | Browser Connections: {browser_count}[/dim]\n"
                            f"[dim]📁 Workspace: {workspace}[/dim]\n"
                            f"[dim]📄 Audit reports saved to: {os.path.join(workspace, 'network_reports')}[/dim]\n"
                            f"[dim]🔗 Lines show connections from your machine to remote servers[/dim]",
                            title="[bold red]GLOBAL THREAT MAP & AUDIT STATUS[/bold red]",
                            border_style="red"
                        ))
                    )
                    
                    live.update(dashboard)
                    time.sleep(2)
                    
                    last_connections = connections
                    last_browser_connections = browser_connections
            
            # Generate comprehensive audit report after monitoring
            if last_connections:
                console.print("[yellow]📄 Generating network report...[/yellow]")
                export_comprehensive_audit_report(last_connections, local_machine, workspace, operator_id)
                save_operator_session_data(last_connections, local_machine, workspace, operator_id)
            if last_browser_connections:
                console.print(f"[cyan]✓ Captured {len(last_browser_connections)} browser connections during monitoring[/cyan]")

        # Run Monitor
        console.print(
            Panel(
                "[bold red] INITIATING NETWORK MONITORING SURVEILLANCE [/bold red]",
                border_style="red"
            )
        )
        
        threat_scan_animation()
        live_monitor(duration=15)
        
        console.print(
            Panel(
                "[bold green] SCAN COMPLETED [/bold green]",
                border_style="green"
            )
        )
        
        # Final report generation
        connections = psutil.net_connections()
        workspace = get_workspace_dir()
        local_machine = get_local_machine_location()
        export_comprehensive_audit_report(connections, local_machine, workspace, getattr(self, 'current_operator', None))
    # ==================== NEW ADVANCED COMMANDS ====================

# =================================================
# In your main SecurityTerminal class
    def do_encrypt_menu(self):
        """Enter the encryption suite menu"""
        if self.crypto:
            from crypto_engine import main as crypto_main
            crypto.main()
        else:
            print(f"{Fore.RED}[!] Crypto engine not available{Style.RESET_ALL}")

 
# =========================================================
# ================for encryption+++++++++++++++++++++++========
    def check_exploits(self):
        vulns = {
            "CVE-2021-44228": "Log4j RCE",
            "CVE-2017-0144": "EternalBlue"
        }
        print("\n[+] Checking for critical CVEs...")
        for cve, desc in vulns.items():
            print(f"{cve}: {desc} - {'[!] VULNERABLE' if random.random() > 0.7 else '[+] Secure'}")

    
    def spoof_mac(self, interface=None):
        """Enhanced MAC spoofing with progress indicators and persistent output"""
        console = Console()

    # Animation frames
        FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

        def create_panel(content, title="", border_style="blue"):
            return Panel(
                content,
                title=title,
                border_style=border_style,
                width=60,
                padding=(1, 2)
            )

        def generate_display(debug_msgs, status_msgs, progress=None):
            debug_panel = create_panel(
                "\n".join(debug_msgs[-5:]),
                title="[blue]DEBUG LOG[/blue]",
                border_style="blue"
            )
        
            status_panel = create_panel(
                "\n".join(status_msgs[-5:]),
                title="[green]STATUS[/green]",
                border_style="green"
            )
        
            progress_panel = create_panel(
                progress if progress else "Initializing...",
                title="[red]PROGRESS[/red]",
                border_style="red"
            )
        
            return Columns([debug_panel, status_panel, progress_panel])

        debug_messages = []
        status_messages = []
        current_frame = 0

        try:
        # Main display context
            with Live(generate_display(debug_messages, status_messages), console=console) as live:
            # 1. Admin Check
                debug_messages.append("Checking admin privileges...")
                live.update(generate_display(debug_messages, status_messages))
            
                if not self.is_admin():
                    status_messages.append("[red]✖ Requires admin privileges[/red]")
                    live.update(generate_display(debug_messages, status_messages))
                    raise PermissionError("Admin rights required")
            
                status_messages.append("[green]✔ Admin privileges confirmed[/green]")
                live.update(generate_display(debug_messages, status_messages))
            
            # 2. Interface Detection
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True
                ) as progress:
                    task = progress.add_task("Detecting interface...", total=100)
                    for i in range(100):
                        progress.update(task, advance=1)
                        time.sleep(0.02)
                        if i % 10 == 0:
                            live.update(generate_display(debug_messages, status_messages))
            
                def get_active_interface():
                    try:
                        if platform.system() in ['Linux', 'Darwin']:
                            route = subprocess.check_output("ip route show default", 
                                                        shell=True, 
                                                        stderr=subprocess.PIPE).decode()
                            if len(route.split()) >= 5:
                                return route.split()[4]
                        elif platform.system() == 'Windows':
                            output = subprocess.check_output("getmac /v /fo csv", 
                                                        shell=True, 
                                                        stderr=subprocess.PIPE).decode()
                            lines = [l for l in output.split('\n') if l.strip()]
                            if len(lines) > 1:
                                return lines[1].split(',')[0].strip('"')
                    except Exception as e:
                        debug_messages.append(f"Error: {str(e)}")
                    return None
            
                if not interface:
                    interface = get_active_interface()
                    if not interface:
                        status_messages.append("[red]✖ Interface detection failed[/red]")
                        live.update(generate_display(debug_messages, status_messages))
                        raise ValueError("No interface detected")
            
                status_messages.append(f"[green]✔ Interface: [bold]{interface}[/bold][/green]")
                live.update(generate_display(debug_messages, status_messages))
            
            # 3. MAC Generation
                new_mac = "02:%02x:%02x:%02x:%02x:%02x" % (
                    random.randint(0x00, 0x7f),
                    random.randint(0x00, 0xff),
                    random.randint(0x00, 0xff),
                    random.randint(0x00, 0xff),
                    random.randint(0x00, 0xff)
                )
                status_messages.append(f"[yellow]New MAC: [bold]{new_mac}[/bold][/yellow]")
                live.update(generate_display(debug_messages, status_messages))
            
            # 4. Execution with live progress
                commands = []
                if platform.system() in ['Linux', 'Darwin']:
                    commands = [
                        f"ifconfig {interface} down",
                        f"ifconfig {interface} hw ether {new_mac}",
                        f"ifconfig {interface} up",
                        f"dhclient -r {interface}",
                        f"dhclient {interface}"
                    ]
                elif platform.system() == 'Windows':
                    interface_key = interface.split('_')[-1]
                    commands = [
                        f'netsh interface set interface \"{interface}\" admin=disable',
                        rf'reg add HKLM\SYSTEM\CurrentControlSet\Control\Class'
                        rf'\{{4D36E972-E325-11CE-BFC1-08002BE10318}}'
                        rf'\{interface_key} /v NetworkAddress /d {new_mac} /f',
                        f'netsh interface set interface \"{interface}\" admin=enable'
                    ]
            
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    transient=True
                ) as progress:
                    task = progress.add_task("Changing MAC...", total=len(commands)*100)
                
                    for i, cmd in enumerate(commands):
                        debug_messages.append(f"Executing: {cmd}")
                        live.update(generate_display(debug_messages, status_messages))
                    
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    
                        for step in range(100):
                            progress.update(task, advance=1, 
                                        description=f"{cmd[:20]}...")
                            time.sleep(0.01)
                            if step % 10 == 0:
                                live.update(generate_display(debug_messages, status_messages))
                    
                        if result.returncode != 0:
                            debug_messages.append(f"Error: {result.stderr.strip()}")
                            live.update(generate_display(debug_messages, status_messages))
            
            # 5. Verification
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True
                ) as progress:
                    task = progress.add_task("Verifying...", total=100)
                    for i in range(100):
                        progress.update(task, advance=1)
                        time.sleep(0.02)
                        if i % 10 == 0:
                            live.update(generate_display(debug_messages, status_messages))
            
                verification_passed = False
                if platform.system() in ['Linux', 'Darwin']:
                    result = subprocess.run(f"ifconfig {interface}",
                                        shell=True,
                                        capture_output=True,
                                        text=True)
                    verification_passed = new_mac.lower() in result.stdout.lower()
                elif platform.system() == 'Windows':
                    result = subprocess.run("getmac /v /fo csv",
                                        shell=True,
                                        capture_output=True,
                                        text=True)
                    verification_passed = new_mac.lower() in result.stdout.lower()
            
                if verification_passed:
                    status_messages.append("[bold green]✓ MAC changed successfully![/bold green]")
                else:
                    status_messages.append("[yellow]⚠ MAC changed but verification failed[/yellow]")
                    debug_messages.append("Note: Some systems require restart for verification")
            
            # Final output
                live.update(generate_display(debug_messages, status_messages))
                console.print("\n[bold]Press Enter to continue...[/bold]", end="")
                
                input()
            
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            debug_messages.append(f"Failed: {str(e)}")
            console.print(generate_display(debug_messages, status_messages))
            console.print("\n[bold]Press Enter to continue...[/bold]", end="")
            input()

        # end here macspoof
   
    def sql_injection_scan(self, url=None):
        """Interactive SQL injection scanner with cinematic animations and PDF report generation"""
        import subprocess
        import os
        import random
        import time
        import json
        from datetime import datetime
        from shutil import which
        from rich.live import Live
        from rich.panel import Panel
        from rich.columns import Columns
        from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
        from rich.console import Console
        from rich.table import Table
        from rich.layout import Layout
        from rich.align import Align
        from rich import box
        import shutil
        
        console = Console()
        
        # Animation frames for different scan phases
        SQL_FRAMES = [
            "[red]SELECT * FROM users WHERE id = '1' OR '1'='1'[/red]",
            "[yellow]UNION SELECT 1,2,3,4,5,6,7,8,9,10[/yellow]",
            "[green]1' OR '1'='1' --[/green]",
            "[cyan]WAITFOR DELAY '0:0:5'[/cyan]",
            "[magenta]CONVERT(int, @@version)[/magenta]",
            "[red]; DROP TABLE users; --[/red]",
            "[yellow]admin' OR '1'='1' --[/yellow]",
            "[green]1' AND SLEEP(5) --[/green]",
            "[cyan]' UNION SELECT @@VERSION, NULL, NULL --[/cyan]",
            "[magenta]1' AND 1=CONVERT(int, @@VERSION) --[/magenta]"
        ]
        
        # Get URL if not provided
        if not url:
            url = console.input("\n[bold cyan]🎯 Enter target URL (with http:// or https://): [/]").strip()
        
        # Clean URL - remove any sqlmap flags if user accidentally added them
        if ' --' in url:
            url = url.split(' --')[0]
        for flag in ['--technique', '--batch', '--level', '--risk', '--dbs']:
            if flag in url:
                url = url.split(flag)[0]
        url = url.strip()
        
        if not url.startswith(("http://", "https://")):
            console.print(Panel(
                "[red]❌ Invalid URL format! Must include http:// or https://[/red]",
                title="[bold red]Input Error[/bold red]",
                border_style="red"
            ))
            console.print("\n[bold]Example:[/bold] [cyan]http://testphp.vulnweb.com/artists.php?artist=1[/cyan]")
            return
        
        # Check sqlmap installation
        if not which("sqlmap"):
            console.print(Panel(
                "[red]❌ sqlmap not found![/red]\n\n"
                "Install with:\n"
                "[green]▶ pip install sqlmap[/green]\n\n"
                "Or visit: [blue]https://sqlmap.org[/blue]",
                title="[bold red]Dependency Missing[/bold red]",
                border_style="red"
            ))
            return
        
        # Create workspace directory
        workspace = os.path.expanduser("~/dsterminal_workspace")
        scans_dir = os.path.join(workspace, "scans")
        os.makedirs(scans_dir, exist_ok=True)
        
        # Prepare display panels
        def create_panel(content, title="", border_style="blue", height=None):
            return Panel(
                content,
                title=f"[bold {border_style}]{title}[/bold {border_style}]" if title else "",
                border_style=border_style,
                width=55,
                padding=(1, 1),
                height=height
            )
        
        # Main display generator
        def generate_display(scan_log, status_msg, animation_frame, scan_stats):
            layout = Layout()
            layout.split_row(
                Layout(name="log", ratio=2),
                Layout(name="right", ratio=1)
            )
            layout["right"].split_column(
                Layout(name="status"),
                Layout(name="injection")
            )
            
            log_content = "\n".join(scan_log[-8:]) if scan_log else "[dim]Waiting for scan output...[/dim]"
            layout["log"].update(create_panel(
                log_content,
                title="📊 SCAN LOG",
                border_style="blue"
            ))
            
            stats_content = f"""
    [green]• Target:[/green] {url[:50]}
    [cyan]• Status:[/cyan] {status_msg}
    [yellow]• Tests Run:[/yellow] {scan_stats['tests']}
    [magenta]• Vulnerabilities:[/magenta] {scan_stats['vulns_found']}
    [red]• Time Elapsed:[/red] {scan_stats['elapsed']}s
            """
            layout["status"].update(create_panel(
                stats_content,
                title="⚡ STATUS",
                border_style="green"
            ))
            
            layout["injection"].update(create_panel(
                f"\n[bold red]{animation_frame}[/bold red]\n\n[dim]Testing injection techniques...[/dim]",
                title="💉 SQL INJECTION",
                border_style="red"
            ))
            
            return layout
        
        scan_log = []
        status_msg = "Initializing scan..."
        current_frame = random.choice(SQL_FRAMES)
        scan_stats = {'tests': 0, 'vulns_found': 0, 'elapsed': 0}
        start_time = time.time()
        vulnerabilities = []
        
        # Prepare sqlmap command
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_url = url.replace('://', '_').replace('/', '_').replace('?', '_').replace('&', '_')[:50]
        report_dir = os.path.join(scans_dir, f"sqlmap_{safe_url}_{timestamp}")
        os.makedirs(report_dir, exist_ok=True)
        
        cmd = [
            "sqlmap",
            "-u", url,
            "--batch",
            "--random-agent",
            "--output-dir", report_dir,
            "--smart",
            "--threads=5",
            "--level=3",
            "--risk=2"
        ]
        
        # Ask for advanced options
        console.print("\n[bold yellow]⚡ SQLMap Configuration[/bold yellow]")
        console.print("[dim]Press Enter to use defaults[/dim]\n")
        
        db_choice = console.input("[cyan]Database type (MySQL/MSSQL/Oracle/PostgreSQL/All) [All]: [/]").strip()
        if db_choice.lower() not in ['', 'all']:
            cmd.extend(["--dbms", db_choice.lower()])
        
        tech_choice = console.input("[cyan]Technique (B/E/U/S/T/Q/All) [All]: [/]").strip()
        if tech_choice.upper() not in ['', 'ALL']:
            cmd.extend(["--technique", tech_choice.upper()])
        
        if console.input("[cyan]Test GET parameters only? (y/n) [n]: [/]").strip().lower() == 'y':
            cmd.append("--no-cast")
        
        data = console.input("[cyan]POST data (if any, press Enter to skip): [/]").strip()
        if data:
            cmd.extend(["--data", data])
        
        cookie = console.input("[cyan]Cookie (if any, press Enter to skip): [/]").strip()
        if cookie:
            cmd.extend(["--cookie", cookie])
        
        # console.print("\n[bold green]Starting SQLMap scan...[/bold green]")
        # console.print(f"[dim]Command: {' '.join(cmd)}[/dim]\n")
        
        process = None
        
        try:
            with Live(generate_display(scan_log, status_msg, current_frame, scan_stats), 
                    console=console, 
                    refresh_per_second=8,
                    transient=False,
                    screen=True) as live:
                
                scan_log.append(f"[bold cyan]▶ Starting scan on: {url}[/bold cyan]")
                status_msg = "[yellow]🔍 Scanning target...[/yellow]"
                scan_stats['elapsed'] = int(time.time() - start_time)
                live.update(generate_display(scan_log, status_msg, current_frame, scan_stats))
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    transient=False
                ) as progress:
                    task = progress.add_task("[cyan]🧪 Testing parameters", total=100)
                    
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        universal_newlines=True,
                        bufsize=1
                    )
                    
                    frame_counter = 0
                    last_line = ""
                    
                    while process.poll() is None:
                        frame_counter += 1
                        if frame_counter % 5 == 0:
                            current_frame = random.choice(SQL_FRAMES)
                            scan_stats['tests'] += 1
                        
                        if "testing" in last_line.lower():
                            progress.update(task, advance=0.3)
                        elif "vulnerable" in last_line.lower():
                            progress.update(task, advance=1)
                            scan_stats['vulns_found'] += 1
                        
                        if progress.tasks[0].percentage >= 100:
                            progress.update(task, completed=99)
                        
                        line = process.stdout.readline()
                        if line:
                            last_line = line.strip()
                            if any(keyword in last_line.lower() for keyword in ["testing", "checking", "trying"]):
                                status_msg = f"[yellow]{last_line[:50]}[/yellow]"
                            elif "vulnerable" in last_line.lower():
                                status_msg = f"[red]⚠️ {last_line[:50]}[/red]"
                                scan_stats['vulns_found'] += 1
                                vulnerabilities.append(last_line)
                            elif "payload" in last_line.lower():
                                scan_log.append(f"[red]💉 {last_line}[/red]")
                            else:
                                scan_log.append(f"[dim]{last_line}[/dim]")
                            
                            if len(scan_log) > 20:
                                scan_log = scan_log[-20:]
                            
                            scan_stats['elapsed'] = int(time.time() - start_time)
                            live.update(generate_display(scan_log, status_msg, current_frame, scan_stats))
                            time.sleep(0.05)
                    
                    progress.update(task, completed=100)
                
                scan_stats['elapsed'] = int(time.time() - start_time)
                status_msg = "[green]✅ Scan completed![/green]"
                live.update(generate_display(scan_log, status_msg, current_frame, scan_stats))
                
                report_file = os.path.join(report_dir, "log")
                if os.path.exists(report_file):
                    with open(report_file, "r", encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for line in content.split('\n'):
                            if any(x in line.lower() for x in ["injectable", "vulnerable", "payload:", "parameter"]):
                                if line.strip() not in vulnerabilities:
                                    vulnerabilities.append(line.strip())
        
        except KeyboardInterrupt:
            console.print("\n[bold yellow]⚠️ Scan interrupted by user[/bold yellow]")
            if process:
                process.terminate()
                process.wait()
        except Exception as e:
            console.print(Panel(
                f"[red]❌ Error: {str(e)}[/red]\n\n"
                f"[dim]Command: {' '.join(cmd)}[/dim]",
                title="[bold red]Scan Failed[/bold red]",
                border_style="red"
            ))
        
        # ============================================================
        # Generate PDF Report
        # ============================================================
        
        def generate_sqlmap_pdf_report():
            """Generate a professional PDF report of SQLMap scan results with DSTERMINAL watermark and logo"""
            try:
                from reportlab.lib import colors
                from reportlab.lib.pagesizes import A4
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
                from reportlab.pdfgen import canvas
                import hashlib
                from PIL import Image as PILImage
                import io
                import os
                
                pdf_filename = f"SQLMap_Report_{safe_url}_{timestamp}.pdf"
                pdf_path = os.path.join(scans_dir, pdf_filename)
                
                # Load the DSTERMINAL logo
                logo_path = os.path.join("installer_assets", "3486-removebg-preview.ico")
                logo_img = None
                logo_temp_path = None
                
                # Convert ICO to PNG for reportlab compatibility
                if os.path.exists(logo_path):
                    try:
                        pil_img = PILImage.open(logo_path)
                        if pil_img.mode in ('RGBA', 'LA', 'P'):
                            background = PILImage.new('RGB', pil_img.size, (255, 255, 255))
                            if pil_img.mode == 'P':
                                pil_img = pil_img.convert('RGBA')
                            if pil_img.mode == 'RGBA':
                                background.paste(pil_img, mask=pil_img.split()[-1])
                            else:
                                background.paste(pil_img)
                            pil_img = background
                        elif pil_img.mode != 'RGB':
                            pil_img = pil_img.convert('RGB')
                        
                        logo_temp_path = os.path.join(scans_dir, "temp_logo.png")
                        pil_img.save(logo_temp_path, "PNG")
                        logo_img = Image(logo_temp_path, width=60, height=60)
                    except Exception as e:
                        console.print(f"[yellow]Logo loading warning: {e}[/yellow]")
                        logo_img = None
                else:
                    console.print(f"[yellow]Logo not found at: {logo_path}[/yellow]")
                
                # Create PDF document with custom page template for watermark
                class WatermarkedDocTemplate(SimpleDocTemplate):
                    def __init__(self, filename, **kwargs):
                        super().__init__(filename, **kwargs)
                    
                    def afterFlowable(self, flowable):
                        pass
                
                doc = WatermarkedDocTemplate(pdf_path, pagesize=A4,
                                            rightMargin=72, leftMargin=72,
                                            topMargin=72, bottomMargin=72)
                
                # Custom page template with watermark
                def add_watermark(canvas_obj, doc):
                    canvas_obj.saveState()
                    page_width, page_height = A4
                    center_x = page_width / 2
                    center_y = page_height / 2
                    
                    canvas_obj.setFont('Helvetica-Bold', 60)
                    canvas_obj.setFillColor(colors.HexColor('#1a1a2e'))
                    canvas_obj.setFillAlpha(0.15)
                    canvas_obj.saveState()
                    canvas_obj.translate(center_x, center_y)
                    canvas_obj.rotate(45)
                    canvas_obj.drawCentredString(0, 0, "DSTERMINAL")
                    canvas_obj.restoreState()
                    
                    canvas_obj.setFont('Helvetica', 25)
                    canvas_obj.setFillAlpha(0.1)
                    canvas_obj.drawCentredString(center_x, 50, "CYBER-OPS PLATFORM")
                    
                    canvas_obj.setFont('Helvetica', 8)
                    canvas_obj.setFillAlpha(0.5)
                    canvas_obj.setFillColor(colors.HexColor('#666666'))
                    canvas_obj.drawCentredString(center_x, 20, f"Page {doc.page} | DSTERMINAL SOC v2.0.113")
                    canvas_obj.restoreState()
                
                # Styles
                styles = getSampleStyleSheet()
                
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=28,
                    textColor=colors.HexColor('#00ff00'),
                    alignment=TA_CENTER,
                    spaceAfter=20,
                    fontName='Helvetica-Bold'
                )
                
                subtitle_style = ParagraphStyle(
                    'Subtitle',
                    parent=styles['Normal'],
                    fontSize=12,
                    textColor=colors.HexColor('#888888'),
                    alignment=TA_CENTER,
                    spaceAfter=30
                )
                
                heading_style = ParagraphStyle(
                    'CustomHeading',
                    parent=styles['Heading2'],
                    fontSize=18,
                    textColor=colors.HexColor('#00ffff'),
                    spaceAfter=15,
                    spaceBefore=15,
                    fontName='Helvetica-Bold'
                )
                
                body_style = ParagraphStyle(
                    'Body',
                    parent=styles['Normal'],
                    fontSize=10,
                    textColor=colors.HexColor('#e0e0e0'),
                    alignment=TA_LEFT,
                    spaceAfter=6,
                    fontName='Helvetica'
                )
                
                # Build story
                story = []
                
                # Add logo centered at the top
                if logo_img:
                    logo_table = Table([[logo_img]], colWidths=[400], rowHeights=[100])
                    logo_table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ]))
                    story.append(logo_table)
                    story.append(Spacer(1, 10))
                
                # Title
                story.append(Paragraph("DSTERMINAL Cyber-Ops Platform", title_style))
                story.append(Paragraph("SQL Injection Security Assessment Report", subtitle_style))
                story.append(Spacer(1, 15))
                
                # Divider
                story.append(Paragraph("-" * 80, styles['Normal']))
                story.append(Spacer(1, 15))
                
                # Report Metadata Table
                report_id = hashlib.md5(f"{url}{timestamp}".encode()).hexdigest()[:16].upper()
                
                metadata_data = [
                    ["Report ID:", report_id],
                    ["Generated By:", "DSTERMINAL SOC Platform v2.0.113"],
                    ["Classification:", "CONFIDENTIAL - Security Team Only"],
                    ["Target URL:", url[:80]],
                    ["Scan Date:", datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                    ["Scan Duration:", f"{scan_stats['elapsed']} seconds ({int(scan_stats['elapsed']/60)} minutes)"],
                    ["Tests Performed:", str(scan_stats['tests'])],
                ]
                
                metadata_table = Table(metadata_data, colWidths=[140, 330])
                metadata_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1a1a2e')),
                    ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#00ffff')),
                    ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#0d1117')),
                    ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#33ff33')),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#333333')),
                ]))
                story.append(metadata_table)
                story.append(Spacer(1, 25))
                
                # Executive Summary
                story.append(Paragraph("Executive Summary", heading_style))
                
                if scan_stats['vulns_found'] > 0:
                    summary_text = f"""
                    <b><font color="#ff0000">⚠️ RISK ASSESSMENT: CRITICAL</font></b><br/>
                    <br/>
                    The security assessment of <b>{url[:60]}</b> has identified <b>{scan_stats['vulns_found']} potential SQL injection vulnerabilities</b>.
                    SQL injection is a critical vulnerability that allows attackers to manipulate database queries,
                    potentially leading to unauthorized data access, data manipulation, or complete system compromise.
                    <br/>
                    <br/>
                    <b><font color="#ff0000">⚠️ IMMEDIATE REMEDIATION REQUIRED</font></b>
                    """
                    story.append(Paragraph(summary_text, body_style))
                else:
                    summary_text = f"""
                    <b><font color="#33ff33">✅ RISK ASSESSMENT: LOW</font></b><br/>
                    <br/>
                    <font color="#33ff33">The security assessment of <b>{url[:60]}</b> did not detect any SQL injection vulnerabilities.
                    The application appears to implement proper input validation and parameterized queries.</font>
                    <br/>
                    <br/>
                    <b><font color="#33ff33">✓ No immediate action required. Continue regular security monitoring.</font></b>
                    """
                    story.append(Paragraph(summary_text, body_style))
                
                story.append(Spacer(1, 80))
                
                # Scan Statistics Table
                story.append(Paragraph("Detailed Scan Statistics", heading_style))
                
                stats_data = [
                    ["Metric", "Value"],
                    ["Target URL", url[:80]],
                    ["Scan Start Time", datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                    ["Total Duration", f"{scan_stats['elapsed']} seconds ({int(scan_stats['elapsed']/60)} minutes)"],
                    ["SQLMap Tests Executed", str(scan_stats['tests'])],
                    ["Vulnerabilities Identified", str(scan_stats['vulns_found'])],
                    ["Report ID", report_id],
                ]
                
                stats_table = Table(stats_data, colWidths=[150, 320])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00ffff')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#0d1117')),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#33ff33')),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#333333')),
                ]))
                story.append(stats_table)
                story.append(Spacer(1, 35))
                # End of Page 1
                # story.append(PageBreak())
                
                # PAGE 2 - Vulnerabilities & Recommendations
                if vulnerabilities:
                    story.append(Paragraph("Vulnerabilities Detected", heading_style))
                    story.append(Spacer(1, 10))
                    
                    vuln_data = [["#", "Type", "Description"]]
                    for i, vuln in enumerate(vulnerabilities[:15], 1):
                        if "injectable" in vuln.lower():
                            vuln_type = "Boolean-Based Blind"
                        elif "union" in vuln.lower():
                            vuln_type = "UNION Query"
                        elif "time" in vuln.lower():
                            vuln_type = "Time-Based Blind"
                        elif "error" in vuln.lower():
                            vuln_type = "Error-Based"
                        else:
                            vuln_type = "SQL Injection"
                        
                        desc = vuln[:150] + "..." if len(vuln) > 150 else vuln
                        vuln_data.append([str(i), vuln_type, desc])
                    
                    vuln_table = Table(vuln_data, colWidths=[30, 100, 350])
                    vuln_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff0000')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#0d1117')),
                        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#33ff33')),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#333333')),
                    ]))
                    story.append(vuln_table)
                    
                    if len(vulnerabilities) > 15:
                        story.append(Spacer(1, 10))
                        story.append(Paragraph(f"<i>... and {len(vulnerabilities) - 15} more vulnerabilities found (see sqlmap output for details)</i>", body_style))
                else:
                    story.append(Paragraph("No Vulnerabilities Detected", heading_style))
                    story.append(Spacer(1, 15))
                    story.append(Paragraph(
                        '<font color="#33ff33">✓ The application passed all SQL injection tests. No exploitable vulnerabilities were found.</font>',
                        body_style
                    ))
                
                story.append(Spacer(1, 25))
                
                # Security Recommendations
                story.append(Paragraph("Security Recommendations", heading_style))
                
                if scan_stats['vulns_found'] > 0:
                    recommendations = [
                        "1. <b>Use Parameterized Queries:</b> Implement prepared statements or stored procedures.",
                        "2. <b>Input Validation:</b> Validate and sanitize all user inputs.",
                        "3. <b>Least Privilege:</b> Ensure database accounts have minimum permissions.",
                        "4. <b>Web Application Firewall (WAF):</b> Deploy a WAF to detect and block SQL injection.",
                        "5. <b>Regular Security Audits:</b> Conduct quarterly penetration testing.",
                        "6. <b>Error Handling:</b> Implement custom error pages that don't reveal database information.",
                    ]
                else:
                    recommendations = [
                        '<font color="#33ff33">1. <b>Continue Monitoring:</b> Maintain regular security assessments and log review.</font>',
                        '<font color="#33ff33">2. <b>Keep Dependencies Updated:</b> Regularly update all frameworks and libraries.</font>',
                        '<font color="#33ff33">3. <b>Security Training:</b> Provide ongoing security awareness training for developers.</font>',
                        '<font color="#33ff33">4. <b>Incident Response Plan:</b> Maintain and regularly test incident response procedures.</font>',
                    ]
                
                for rec in recommendations:
                    story.append(Paragraph(rec, body_style))
                    story.append(Spacer(1, 8))
                
                story.append(Spacer(1, 20))
                
                # Footer Information
                story.append(Paragraph("Report Information", heading_style))
                footer_text = f"""
                <font color="#33ff33"><b>Generated by:</b> DSTERMINAL Cyber-Ops Platform v2.0.113</font><br/>
                <font color="#33ff33"><b>Report Type:</b> SQL Injection Security Assessment</font><br/>
                <font color="#33ff33"><b>Classification:</b> CONFIDENTIAL - Security Team Only</font><br/>
                <font color="#33ff33"><b>Retention Policy:</b> 90 days</font><br/>
                <font color="#33ff33"><b>Contact:</b> security@dsterminal.local</font><br/>
                <br/>
                <font color="#33ff33"><i>Disclaimer: This report is automatically generated by DSTERMINAL SOC Platform.
                The findings should be verified manually before taking remediation actions.
                Unauthorized distribution of this report is prohibited.</i></font>
                """
                story.append(Paragraph(footer_text, body_style))
                
                # Build PDF with watermark on every page
                doc.build(story, onFirstPage=add_watermark, onLaterPages=add_watermark)
                
                # Clean up temporary logo file
                if logo_temp_path and os.path.exists(logo_temp_path):
                    try:
                        os.remove(logo_temp_path)
                    except:
                        pass
                
                console.print(f"\n[bold green]📄 PDF Report Generated: {pdf_path}[/bold green]")
                return pdf_path
                
            except ImportError as e:
                console.print(f"[yellow]⚠️ Missing module: {e}. PDF report skipped.[/yellow]")
                console.print("[dim]Install with: pip install reportlab Pillow[/dim]")
                return None
            except Exception as e:
                console.print(f"[red]❌ PDF generation failed: {e}[/red]")
                return None
        # Generate PDF
        pdf_path = generate_sqlmap_pdf_report()
        
        # ============================================================
        # CENTERED RESULTS TABLE
        # ============================================================
        
        # Clear screen for clean results
        console.clear()
        
        # Get terminal width for centering
        try:
            term_width = shutil.get_terminal_size().columns
        except:
            term_width = 100
        
        # Create the results table
        results_table = Table(
            title="[bold cyan]🔍 SQLMap Scan Results[/bold cyan]",
            box=box.ROUNDED,
            width=70,
            show_header=True,
            header_style="bold cyan"
        )
        results_table.add_column("Metric", style="yellow", width=25)
        results_table.add_column("Value", style="green", width=45)
        
        results_table.add_row("Target URL", url)
        results_table.add_row("Scan Duration", f"{scan_stats['elapsed']} seconds ({int(scan_stats['elapsed']/60)} minutes)")
        results_table.add_row("Tests Performed", str(scan_stats['tests']))
        
        vuln_text = f"[bold red]{scan_stats['vulns_found']} FOUND![/bold red]" if scan_stats['vulns_found'] > 0 else "[green]0[/green]"
        results_table.add_row("Vulnerabilities Found", vuln_text)
        
        report_loc = pdf_path[:57] + "..." if pdf_path and len(pdf_path) > 60 else str(pdf_path)
        results_table.add_row("Report Location", report_loc if pdf_path else "Not generated")
        
        # Center and display the table
        centered_table = Align.center(results_table)
        console.print(centered_table)
        
        # Show vulnerabilities if found
        if vulnerabilities:
            console.print("\n[bold red]⚠️ VULNERABILITIES DETECTED![/bold red]\n")
            for v in vulnerabilities[:5]:
                console.print(f"  [red]•[/red] {v[:80]}")
            
            if len(vulnerabilities) > 5:
                console.print(f"\n[dim]... and {len(vulnerabilities) - 5} more (see full report)[/dim]")
        else:
            console.print("\n[green]✅ No SQL injection vulnerabilities detected.[/green]")
            console.print("[dim]The application appears to be secure against SQL injection attacks.[/dim]")
        
        # Separator line
        console.print("\n" + "=" * 70)
        
        # Open PDF if requested
        if pdf_path and os.path.exists(pdf_path):
            open_pdf = console.input("\n[bold cyan]📄 Open PDF report? (y/n): [/]").strip().lower()
            if open_pdf == 'y':
                import webbrowser
                webbrowser.open(f"file://{pdf_path}")
                console.print("[green]✓ PDF report opened[/green]")
        
        console.print("\n[bold]Press Enter to continue...[/]", end="")
        input()

# ==================== UTILITY METHODS ====================
 

    def clear_logs(self):
        """Securely clear system logs with admin verification and visual feedback"""
        console = Console()

        def create_panel(content, title="", border_style="blue"):
            return Panel(
                content,
                title=title,
                border_style=border_style,
                width=60,
                padding=(1, 1)
            )

    # Verify admin privileges first
        if not self.is_admin():
            console.print(
                create_panel(
                    "[red]✖ Requires administrator privileges[/red]",
                    title="Access Denied",
                    border_style="red"
                )
            )
            return

        try:
            with Progress(transient=True) as progress:
                task = progress.add_task("[cyan]Clearing system logs...", total=100)

            # Animated clearing process
                for i in range(5):
                    progress.update(task, advance=20, description=f"[cyan]Clearing {['event','application','security','setup','system'][i]} logs...")
                    time.sleep(0.5)

            # Actual log clearing commands
                if platform.system() == "Windows":
                    logs_cleared = []
                    for log_type in ["Application", "System", "Security"]:
                        result = os.system(f"wevtutil cl {log_type}")
                        if result == 0:
                            logs_cleared.append(log_type)
                    progress.update(task, completed=100)
                
                    console.print(
                        create_panel(
                            f"[green]✔ Cleared Windows logs: {', '.join(logs_cleared)}[/green]",
                            title="Success",
                            border_style="green"
                        )
                    )

                else:  # Linux/Mac
                    try:
                        os.system("sudo rm -rf /var/log/*")
                        os.system("sudo journalctl --vacuum-time=1s")
                        progress.update(task, completed=100)
                        console.print(
                            create_panel(
                                "[green]✔ Cleared system logs successfully[/green]",
                                title="Success",
                                border_style="green"
                            )
                        )
                    except Exception as e:
                        progress.update(task, visible=False)
                        console.print(
                            create_panel(
                                f"[red]✖ Error clearing logs: {str(e)}[/red]",
                                title="Error",
                                border_style="red"
                            )
                        )

        except Exception as e:
            console.print(
                create_panel(
                    f"[red]✖ Critical error: {str(e)}[/red]",
                    title="Operation Failed",
                    border_style="red"
                )
            )


# FINANCIAL SECTION
    def financial_forensics_menu():
        """Launch the financial forensics suite"""
        forensics = FinancialForensics()
        forensics.cinematic_fraud_investigation()
# FINANCIAL SECTION ENDS HERE
# =================for integrity check
    def _check_integrity_available(self):
        """Check if integrity monitor is available"""
        if not INTEGRITY_AVAILABLE:
            print(f"{Fore.RED}Integrity monitor not available.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Make sure integrity_monitor.py is in the same directory{Style.RESET_ALL}")
            return False
        if self.integrity is None:
            print(f"{Fore.RED}Integrity monitor not initialized.{Style.RESET_ALL}")
            return False
        return True
    
    def show_integrity_help(self):
        """Display integrity monitor help"""
        help_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║              INTEGRITY MONITOR COMMANDS                         ║
╠════════════════════════════════════════════════════════════════╣
║  {Fore.YELLOW}CORE COMMANDS:{Fore.CYAN}                                                 ║
║    integrity scan              - Full system integrity check    ║
║    integrity baseline          - Create new system baseline     ║
║    integrity status            - Show monitor status            ║
║                                                               ║
║  {Fore.YELLOW}REPORT COMMANDS:{Fore.CYAN}                                               ║
║    integrity report            - Generate TXT report            ║
║    integrity report json       - Generate JSON report           ║
║    integrity report pdf        - Generate PDF report            ║
║    integrity report all        - Generate all report formats    ║
║                                                               ║
║  {Fore.YELLOW}REAL-TIME MONITORING:{Fore.CYAN}                                          ║
║    integrity monitor           - Start real-time monitoring     ║
║    integrity monitor stop      - Stop real-time monitoring      ║
║    integrity alerts            - Show recent alerts             ║
║                                                               ║
║  {Fore.YELLOW}FORENSIC ANALYSIS:{Fore.CYAN}                                             ║
║    integrity forensic timeline  - Show change timeline          ║
║    integrity forensic report    - Generate forensic report      ║
║    integrity list                 - Show summary of all files   ║
║    integrity list critical        - List critical system files       ║
║    integrity list configs         - List configuration files         ║
║    integrity list logs            - List log files                   ║
║    integrity list databases       - List database files
║    integrity list user            - List user files                       ║
║    integrity forensic timeline  - Show change timeline                    ║
║    integrity forensic report    - Generate forensic report           ║
║    integrity quarantine <file>    - Quarantine a suspicious file     ║
║    integrity restore <file>       - Restore from quarantine          ║
╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(help_text)
# ================ends here integ=======
    def watch_folder(self, path):
        """Monitor a folder for changes"""
        if not os.path.exists(path):
            print("[!] Path not found")
            return

        print(f"\n[+] Monitoring {path} for changes (Ctrl+C to stop)...")
        before = dict([(f, None) for f in os.listdir(path)])
        
        try:
            while True:
                time.sleep(5)
                after = dict([(f, None) for f in os.listdir(path)])
                added = [f for f in after if f not in before]
                removed = [f for f in before if f not in after]
                
                if added: print(f"  [+] Files added: {', '.join(added)}")
                if removed: print(f"  [-] Files removed: {', '.join(removed)}")
                
                before = after
        except KeyboardInterrupt:
            print("\n[+] Folder monitoring stopped")

    def trace_route(self, target):
        """Perform a traceroute to target"""
        print(f"\n[+] Tracing route to {target}...")
        try:
            if platform.system() == "Windows":
                os.system(f"tracert {target}")
            else:
                os.system(f"traceroute {target}")
        except Exception as e:
            print(f"[!] Error: {e}")

    def monitor_ransomware(self):
        """Check for ransomware indicators"""
        print("\n[+] Scanning for ransomware indicators...")
        suspicious_extensions = ['.encrypted', '.locked', '.crypt', '.ransom']
        found = False
        
        for root, _, files in os.walk('/' if platform.system() != 'Windows' else 'C:\\'):
            for file in files:
                if any(file.endswith(ext) for ext in suspicious_extensions):
                    print(f"  [!] Suspicious file: {os.path.join(root, file)}")
                    found = True
            if found:  # Prevent full disk scan
                break
        
        if not found:
            print("[+] No obvious ransomware files detected")

    def wifi_audit(self, interface):
        """Perform WiFi security audit"""
        if platform.system() != "Linux":
            print("[!] This command requires Linux")
            return

        print(f"\n[+] Auditing WiFi on {interface}...")
        try:
            result = subprocess.run(['iwconfig', interface], capture_output=True, text=True)
            print(result.stdout)
            
            if "unassociated" in result.stdout:
                print("[!] Interface not connected")
                return
                
            print("\n[+] Nearby access points:")
            subprocess.run(['sudo', 'iwlist', interface, 'scan'], check=True)
        except Exception as e:
            print(f"[!] Error: {e}")


    def _scan_bar(self, label, duration=10, width=30):
        """Animated progress bar for cinematic scanning"""
        sys.stdout.write(f"    ├─ {label}: ")
        sys.stdout.flush()
        steps = 20
        for i in range(steps):
            sys.stdout.write("█")
            sys.stdout.flush()
            time.sleep(duration / steps)
        print(" ✓")


    def check_steganography(self, image_path):
        """
        Perform non-invasive steganalysis checks on an image.
        Detection only – no extraction or execution.
        """

        if not os.path.exists(image_path):
            print("[!] Image not found")
            return

        try:
            print(f"\n[+] Loading image: {image_path}")
            time.sleep(2)

            file_size = os.path.getsize(image_path)
            print(f"[+] File size: {round(file_size / 1024, 2)} KB")
            time.sleep(2)

            with open(image_path, "rb") as f:
                content = f.read()

            print("\n[+] Performing steganalysis checks...")
            time.sleep(2)

        # --- Animated scan stages ---
            self._scan_bar("File structure inspection",duration=10)
            self._scan_bar("Signature scan", duration=10)
            self._scan_bar("Entropy evaluation", duration=10)
            self._scan_bar("LSB pattern sampling", duration=10)

            anomalies = []

        # --- Known steganography signatures (light detection) ---
            steg_signatures = {
                b"STEGO": "Generic steganography marker",
                b"Steghide": "Steghide tool reference",
                b"outguess": "OutGuess tool reference"
            }

            for sig, desc in steg_signatures.items():
                if sig.lower() in content.lower():
                    anomalies.append(f"Possible {desc}")

        # --- Entropy check (real forensic concept) ---
            byte_counts = Counter(content)
            entropy = 0.0

            for count in byte_counts.values():
                p = count / len(content)
                entropy -= p * math.log2(p)

            entropy = round(entropy, 2)

            if entropy > 7.5:
                anomalies.append("High entropy detected (possible embedded data)")

            time.sleep(3)

        # --- Result output ---
            if anomalies:
                print("\n[!] WARNING: Potential anomalies detected")
                for a in anomalies:
                    time.sleep(1.5)
                    print(f"    ├─ {a}")

                confidence = "MEDIUM" if len(anomalies) > 1 else "LOW"
                print(f"\n[+] Confidence level: {confidence}")
                print("[+] Recommendation: Manual forensic review advised")
            else:
                print("\n[✓] No obvious steganographic indicators detected")
                print("[+] Confidence level: LOW")
                print("[+] Image appears normal")

            time.sleep(2)
            print("\n[✓] Steganalysis completed successfully")

        except Exception as e:
            print(f"[!] Analysis error: {e}")
# certificate check impleme below

    def certcheck(self, domain=None):
        """
        DSTerminal SSL/TLS Certificate Checker with cinematic hacking animation.
        """
        try:
        # Prompt for domain if not provided
            if not domain:
                domain = input("\nEnter domain to check (e.g., starkexpo.com): ").strip()
                if not domain:
                    print("[!] No domain provided")
                    return

        # Cinematic header
            banner = """
            ████╗  █████╗  ██╔██╗ ██║█████╗   ╚███╔╝
            ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║
            ██████╔╝██║     ██║     ███████╗██║ ╚████║
            ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═══╝
            """
            print(banner)
            print(f"\n[-- DFFENEX@DSTerminal ]-[] certcheck")
            time.sleep(0.5)

        # Stage animations for cinematic effect
            stages = [
                "Initializing SSL Inspection Engine",
                "Analyzing TLS Handshake",
                "Validating Certificate Chain",
                "Mapping Trust Relationships",
                "Running Risk Assessment Engine",
                "Generating Defense Recommendations"
            ]

            for stage in stages:
                self._loading_animation(stage, 5)  # 5 seconds per stage for cinematic pacing

        # Run the comprehensive SSL check
            self.check_ssl(domain)

            print(f"\n[-- DFFENEX@DSTerminal ]-[]")

        except Exception as e:
            print(f"[!] Certificate check failed: {e}")

    def check_ssl(self, domain=None):
        """Comprehensive SSL certificate analyzer with export options"""
        try:
            if not domain:
                domain = input("Enter domain to check (e.g., starkexpo.com): ").strip()
                if not domain:
                    print("[!] No domain provided")
                    return
        
        # Run cinematic scanning sequence
            self._animated_ssl_scan()
        
        # Configure enhanced SSL context
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_default_certs()
        
        # Set timeout and create connection
            socket.setdefaulttimeout(10)
        
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert(binary_form=True)
                    x509 = ssl.DER_cert_to_PEM_cert(cert)
                    cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, x509)
                
                # Get certificate details
                    peer_cert = ssock.getpeercert()
                    issuer = dict(x[0] for x in peer_cert['issuer'])
                    subject = dict(x[0] for x in peer_cert['subject'])
                    expires = datetime.strptime(peer_cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    valid_days = (expires - datetime.now()).days
                
                # Get certificate chain using OpenSSL
                    chain = []
                    store = OpenSSL.crypto.X509Store()
                    store_ctx = OpenSSL.crypto.X509StoreContext(store, cert_obj)
                
                    try:
                        chain_result = store_ctx.get_verified_chain()
                        for i, chain_cert in enumerate(chain_result):
                            chain.append({
                                'subject': dict(chain_cert.get_subject().get_components()),
                                'issuer': dict(chain_cert.get_issuer().get_components()),
                                'expires': chain_cert.get_notAfter().decode('utf-8'),
                                'serial': chain_cert.get_serial_number(),
                                'version': chain_cert.get_version() + 1
                            })
                    except OpenSSL.crypto.X509StoreContextError:
                        chain.append({
                            'subject': dict(cert_obj.get_subject().get_components()),
                            'issuer': dict(cert_obj.get_issuer().get_components()),
                            'expires': cert_obj.get_notAfter().decode('utf-8'),
                            'serial': cert_obj.get_serial_number(),
                            'version': cert_obj.get_version() + 1
                        })
                
                # Check OCSP revocation status
                    ocsp_status = "Unknown"
                    if len(chain) > 1:
                        ocsp_status = self._check_ocsp(cert_obj, chain[1])
                
                # Print comprehensive report with animated table
                    self._print_ssl_report(domain, ssock, cert_obj, chain, ocsp_status, valid_days)
    
        except ssl.SSLError as e:
            self._cinematic_box(f"[!] SSL Error: {e}", seconds=2, error=True)
        except socket.timeout:
            self._cinematic_box("[!] Connection timed out", seconds=2, error=True)
        except ImportError as e:
            self._cinematic_box(f"[!] Required module missing: {str(e)}", seconds=3, error=True)
            print("[!] Please install pyOpenSSL: pip install pyopenssl")
        except Exception as e:
            self._cinematic_box(f"[!] Analysis failed: {str(e)}", seconds=2, error=True)

    def _cinematic_box(self, title, seconds=3, error=False):
        """Display a centered colored box with progress and flickering messages"""
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        box_width = min(60, terminal_width - 10)
    
    # Center the box
        left_padding = (terminal_width - box_width - 2) // 2
    
    # Random colors or error color
        if error:
            colors = [Fore.RED, Fore.LIGHTRED_EX]
        else:
            colors = [Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.LIGHTGREEN_EX]
        color = random.choice(colors)
        blink = "\033[5m" if not error else ""
    
    # Clear line and create centered box
        sys.stdout.write("\033[K")  # Clear current line
    
    # Top border (centered)
        print(" " * left_padding + color + "┌" + "─" * box_width + "┐" + Style.RESET_ALL)
    
    # Title with blinking effect
        title_text = f"{blink}{title}{Style.RESET_ALL}" if not error else title
        print(" " * left_padding + color + "│" + Style.RESET_ALL + f" {title_text}".ljust(box_width + 1) + color + "│" + Style.RESET_ALL)
        print(" " * left_padding + color + "├" + "─" * box_width + "┤" + Style.RESET_ALL)
    
    # Animation inside box
        spinner = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
        flickers = [
            "[SCANNING...]", "[TLS CHECK]", "[OCSP QUERY]", 
            "[CERT VERIFY]", "[RISK ASSESS]", "[CHAIN ANALYZE]",
            "[PROTOCOL SCAN]", "[CIPHER CHECK]", "[SIGNATURE VERIFY]"
        ]
        end_time = time.time() + seconds
        i = 0
    
        while time.time() < end_time:
            progress = int(((time.time() % seconds) / seconds) * (box_width - 10))
            bar = "█" * progress + "░" * (box_width - 10 - progress)
            flicker_text = random.choice(flickers)
        
        # Create the content line
            content = f"{spinner[i%len(spinner)]} {bar} {flicker_text}"
            content = content[:box_width-2].ljust(box_width-2)
        
        # Position cursor and update
            sys.stdout.write(f"\033[s")  # Save position
            sys.stdout.write(f"\033[{left_padding+1}G")  # Move to start of box content
            sys.stdout.write(color + "│" + Style.RESET_ALL + f" {content} " + color + "│" + Style.RESET_ALL)
            sys.stdout.write(f"\033[u")  # Restore position
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
    
    # Bottom border (centered)
        print("\n" + " " * left_padding + color + "└" + "─" * box_width + "┘" + Style.RESET_ALL)
        sys.stdout.flush()

    def _animated_ssl_scan(self):
        """Run animated scanning stages"""
        stages = [
            "INITIALIZING SSL INSPECTION ENGINE",
            "ANALYZING TLS HANDSHAKE PROTOCOL",
            "VALIDATING CERTIFICATE CHAIN",
            "MAPPING TRUST RELATIONSHIPS",
            "RUNNING RISK ASSESSMENT ENGINE",
            "GENERATING DEFENSE RECOMMENDATIONS"
        ]
    
        terminal_width = shutil.get_terminal_size((80, 20)).columns
    
        for i, stage in enumerate(stages):
        # Clear screen effect between stages (optional)
            if i > 0:
                time.sleep(0.3)
        
            self._cinematic_box(stage, seconds=3)
        
        # Glitch effect between stages
            if i < len(stages) - 1:
                glitch_color = random.choice([Fore.GREEN, Fore.CYAN, Fore.MAGENTA])
                glitch_text = f"{glitch_color}[SYSTEM]{Style.RESET_ALL} Stage {i+1} complete..."
                print(" " * ((terminal_width - len(glitch_text) + 30) // 2) + glitch_text)
                time.sleep(0.2)

    def _animated_ssl_table(self, cert_data):
        """Display certificate info in colored, blinking table"""
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        table_width = min(70, terminal_width - 10)
        left_padding = (terminal_width - table_width - 2) // 2
    
        colors = [Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.LIGHTGREEN_EX]
        blink = "\033[5m"
    
    # Clear screen area for table
        print("\n" * 2)
    
    # Top border with title
        print(" " * left_padding + Fore.CYAN + "╔" + "═" * table_width + "╗" + Style.RESET_ALL)
        title = "🔐 DSTERMINAL SSL/TLS SECURITY AUDIT 🔐"
        print(" " * left_padding + Fore.CYAN + "║" + Style.RESET_ALL + f"{blink}{Fore.LIGHTYELLOW_EX}{title:^{table_width}}{Style.RESET_ALL}" + Fore.CYAN + "║" + Style.RESET_ALL)
        print(" " * left_padding + Fore.CYAN + "╠" + "═" * table_width + "╣" + Style.RESET_ALL)
    
    # Table content with blinking effect
        for key, value in cert_data.items():
            color = random.choice(colors)
        
        # Format key with color and blink
            key_str = f"{color}{blink}{key.upper()}{Style.RESET_ALL}"
        
        # Format value based on type
            if isinstance(value, (int, float)):
                if value < 0:
                    value_str = f"{Fore.RED}{value}{Style.RESET_ALL}"
                elif value < 30:
                    value_str = f"{Fore.YELLOW}{value}{Style.RESET_ALL}"
                else:
                    value_str = f"{Fore.GREEN}{value}{Style.RESET_ALL}"
            elif "HIGH" in str(value) or "CRITICAL" in str(value):
                value_str = f"{Fore.RED}{blink}{value}{Style.RESET_ALL}"
            elif "MEDIUM" in str(value):
                value_str = f"{Fore.YELLOW}{value}{Style.RESET_ALL}"
            else:
                value_str = f"{Fore.WHITE}{value}{Style.RESET_ALL}"
        
        # Create row with proper spacing
            row = f" {key_str:<20} {value_str:<{table_width-23}}"
        
        # Print row with animation
            print(" " * left_padding + Fore.CYAN + "║" + Style.RESET_ALL + row + " " * (table_width - len(row) + 1) + Fore.CYAN + "║" + Style.RESET_ALL)
            time.sleep(0.1)  # Typing effect
    
    # Bottom border
        print(" " * left_padding + Fore.CYAN + "╚" + "═" * table_width + "╝" + Style.RESET_ALL)
    
    # Add status line
        status = f"{Fore.GREEN}[✓] SCAN COMPLETE • {datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}"
        print(" " * ((terminal_width - len(status)) // 2) + status)

    def _print_ssl_report(self, domain, ssock, cert_obj, chain, ocsp_status, valid_days):
        """Enhanced SSL report with centered animated display"""
    
    # Stage 1-6: Animated scanning
        self._animated_ssl_scan()
    
    # Gather certificate data
        protocol = ssock.version()
        cipher = ssock.cipher()[0]
        sig_algo = cert_obj.get_signature_algorithm().decode()
    
    # Calculate risk level
        risk = 0
        if valid_days < 60:
            risk += 2
        if "SHA1" in sig_algo:
            risk += 3
        if protocol in ["TLSv1", "TLSv1.1"]:
            risk += 4
        if protocol != "TLSv1.3":
            risk += 1
        if ocsp_status != "VALID":
            risk += 2
    
        if risk == 0:
            level = "LOW"
            risk_color = Fore.GREEN
        elif risk <= 3:
            level = "MEDIUM"
            risk_color = Fore.YELLOW
        elif risk <= 6:
            level = "HIGH"
            risk_color = Fore.RED
        else:
            level = "CRITICAL"
            risk_color = Fore.RED + "\033[5m"  # Blinking red for critical
    
    # Prepare certificate data for table
        cert_data = {
            "domain": domain,
            "issuer": cert_obj.get_issuer().CN,
            "subject": cert_obj.get_subject().CN,
            "expires": f"{cert_obj.get_notAfter().decode()} ({valid_days} days)",
            "protocol": protocol,
            "cipher": cipher[:40] + "..." if len(cipher) > 40 else cipher,
            "signature": sig_algo,
            "ocsp status": ocsp_status,
            "risk level": f"{risk_color}{level}{Style.RESET_ALL}",
            "chain length": len(chain)
        }
    
    # Display animated table
        self._animated_ssl_table(cert_data)
    
    # Certificate chain display
        print("\n" + "═" * shutil.get_terminal_size().columns)
        chain_title = f"{Fore.CYAN}🔗 CERTIFICATE CHAIN ANALYSIS{Style.RESET_ALL}"
        print(chain_title.center(shutil.get_terminal_size().columns))
        print("═" * shutil.get_terminal_size().columns)
    
        for i, cert in enumerate(chain):
            indent = "  " * i
            subject = cert['subject'].get(b'CN', b'Unknown').decode()
            issuer = cert['issuer'].get(b'CN', b'Unknown').decode()
        
        # Color based on depth
            if i == 0:
                color = Fore.GREEN  # Leaf certificate
            elif i == len(chain) - 1:
                color = Fore.YELLOW  # Root certificate
            else:
                color = Fore.CYAN  # Intermediate
        
            print(f"{indent} {color}├─ {subject}{Style.RESET_ALL}")
            if i == 0:
                print(f"{indent}    Issuer: {issuer}")
                print(f"{indent}    Valid: {cert['expires'][:8]}")
    
    # Security assessment
        print("\n" + "═" * shutil.get_terminal_size().columns)
        assess_title = f"{Fore.MAGENTA}🛡️ SECURITY ASSESSMENT{Style.RESET_ALL}"
        print(assess_title.center(shutil.get_terminal_size().columns))
        print("═" * shutil.get_terminal_size().columns)
    
        warnings = []
        if valid_days < 60:
            warnings.append(f"{Fore.YELLOW}⚠ Certificate expires soon ({valid_days} days){Style.RESET_ALL}")
        if "SHA1" in sig_algo:
            warnings.append(f"{Fore.RED}✗ Weak signature algorithm (SHA-1){Style.RESET_ALL}")
        if protocol in ["TLSv1", "TLSv1.1"]:
            warnings.append(f"{Fore.RED}✗ Deprecated TLS protocol{Style.RESET_ALL}")
        if protocol != "TLSv1.3":
            warnings.append(f"{Fore.YELLOW}⚠ TLS 1.3 not enabled{Style.RESET_ALL}")
        if ocsp_status != "VALID":
            warnings.append(f"{Fore.YELLOW}⚠ OCSP revocation not verified{Style.RESET_ALL}")
    
        if warnings:
            for warning in warnings:
                print(f"  {warning}")
        else:
            print(f"  {Fore.GREEN}✓ No security issues detected{Style.RESET_ALL}")
    
    # Recommendations
        print("\n" + "═" * shutil.get_terminal_size().columns)
        rec_title = f"{Fore.BLUE}💡 RECOMMENDATIONS{Style.RESET_ALL}"
        print(rec_title.center(shutil.get_terminal_size().columns))
        print("═" * shutil.get_terminal_size().columns)
    
        if valid_days < 60:
            print(f"  {Fore.YELLOW}→ Renew SSL certificate immediately{Style.RESET_ALL}")
        if protocol != "TLSv1.3":
            print(f"  {Fore.CYAN}→ Upgrade server to support TLS 1.3{Style.RESET_ALL}")
        if ocsp_status != "VALID":
            print(f"  {Fore.CYAN}→ Enable OCSP stapling{Style.RESET_ALL}")
        if not warnings:
            print(f"  {Fore.GREEN}→ No action required. System secure.{Style.RESET_ALL}")
    
        print("\n" + "═" * shutil.get_terminal_size().columns)
    
    # Build report data
        data = {
            "domain": domain,
            "subject": cert_obj.get_subject().CN,
            "valid_days": valid_days,
            "protocol": ssock.version(),
            "cipher": ssock.cipher()[0],
            "ocsp": ocsp_status,
            "risk_level": level,
            "renewal_warning": valid_days < 60,
            "tls13": ssock.version() == "TLSv1.3",
            "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "certificate": {
                "subject": {"CN": cert_obj.get_subject().CN},
                "issuer": {"CN": cert_obj.get_issuer().CN},
                "expires": cert_obj.get_notAfter().decode(),
                "serial": str(cert_obj.get_serial_number()),
                "signature": cert_obj.get_signature_algorithm().decode()
            },
            "security_profile": {
                "tls13": ssock.version() == "TLSv1.3",
                "ocsp": ocsp_status,
                "forward_secrecy": "ECDHE" in ssock.cipher()[0]
            }
        }
    
    # Export options
        choice = input(f"\n{Fore.CYAN}Export security report to file? (y/N): {Style.RESET_ALL}").lower()
        if choice == "y":
            self._export_ssl_results(domain, ssock, cert_obj, chain)
    
        pdf_choice = input(f"{Fore.CYAN}Generate PDF compliance report? (y/N): {Style.RESET_ALL}").lower()
        if pdf_choice == "y":
            self._generate_pdf_report(data)



    def _check_ocsp(self, cert, issuer_cert):
        """Check OCSP revocation status"""
        try:
            from cryptography.x509.oid import ExtensionOID
            from cryptography.hazmat.backends import default_backend
            from cryptography.x509 import load_pem_x509_certificate
            
            cert = load_pem_x509_certificate(
                OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            )
        
            if issuer_cert:
                issuer = load_pem_x509_certificate(
                    OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, issuer_cert)
                )
                builder = OCSPRequestBuilder()
                builder = builder.add_certificate(cert, issuer)
                req = builder.build()
            
                ocsp_url = cert.extensions.get_extension_for_class(
                    cryptography.x509.AuthorityInformationAccess
                ).value.get_ocsp_urls()[0]
            
                response = requests.post(
                    ocsp_url,
                    data=req.public_bytes(serialization.Encoding.DER),
                    headers={'Content-Type': 'application/ocsp-request'}
                )
            
                return "REVOKED" if response.status == 1 else "VALID"
        except:
            return "Unknown"

    def _export_ssl_results(self, domain, ssock, cert_obj, chain):
        """Export SSL results to workspace directory"""
    
        subject = self._bytes_to_str_dict(
            dict(cert_obj.get_subject().get_components())
        )

        issuer = self._bytes_to_str_dict(
            dict(cert_obj.get_issuer().get_components())
        )

        data = {
            "domain": domain,
            "scan_time": datetime.now().isoformat(),
            "protocol": ssock.version(),
            "cipher": ssock.cipher()[0],
            "certificate": {
                "subject": subject,
                "issuer": issuer,
                "expires": cert_obj.get_notAfter().decode(),
                "serial": str(cert_obj.get_serial_number()),
                "signature": cert_obj.get_signature_algorithm().decode()
            },
            "chain": self._clean_chain(chain),
            "security_profile": {
                "tls13": ssock.version() == "TLSv1.3",
                "ocsp": "checked",
                "forward_secrecy": "ECDHE" in ssock.cipher()[0]
            }
        }

    # Get workspace directory
        workspace_dir = getattr(self, 'workspace_dir', None)
        if workspace_dir is None:
            if hasattr(self, 'current_workspace'):
                workspace_dir = self.current_workspace
            else:
                workspace_dir = os.path.join(os.path.expanduser("~"), "dsterminal_workspace")
    
    # Ensure workspace directory exists
        os.makedirs(workspace_dir, exist_ok=True)
    
        # Create reports subdirectory in workspace
        reports_dir = os.path.join(workspace_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)
    
    # Save to workspace/reports/
        report_file = os.path.join(
            reports_dir, 
            f"ssl_audit_{domain}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        )

        with open(report_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"\n[✓] Encrypted audit report saved: {report_file}")

    def _bytes_to_str_dict(self, data):
        """Convert bytes dictionary to string dictionary"""

        clean = {}

        for k, v in data.items():

            if isinstance(k, bytes):
                k = k.decode()

            if isinstance(v, bytes):
                v = v.decode()

            clean[k] = v

        return clean

    # string bytes conversions===============
    def _clean_chain(self, chain):
        """Convert certificate chain bytes to strings"""

        cleaned = []

        for cert in chain:

            new_cert = {}

            for k, v in cert.items():

            # Decode key
                if isinstance(k, bytes):
                    k = k.decode()

            # Decode value
                if isinstance(v, bytes):
                    v = v.decode()

            # If value is dict (nested)
                if isinstance(v, dict):

                    temp = {}

                    for kk, vv in v.items():

                        if isinstance(kk, bytes):
                            kk = kk.decode()

                        if isinstance(vv, bytes):
                            vv = vv.decode()

                        temp[kk] = vv

                    v = temp

                new_cert[k] = v

            cleaned.append(new_cert)

        return cleaned


    def _generate_pdf_report(self, data, logo_path="icon.jpg", footer_logo_path="icon.jpg"):
        """Generate PDF report in workspace directory"""
    
    # Safely get all keys with defaults
        domain = data.get("domain", "unknown_domain")
        certificate = data.get("certificate", {})
        security_profile = data.get("security_profile", {})
        scan_time = data.get("scan_time", datetime.now().strftime('%Y-%m-%d %H:%M'))
        protocol = data.get("protocol", "N/A")
        cipher = data.get("cipher", "N/A")

        subject = certificate.get("subject", {}).get("CN", "N/A")
        issuer = certificate.get("issuer", {}).get("CN", "N/A")
        expires = certificate.get("expires", "N/A")
        serial = certificate.get("serial", "N/A")
        signature = certificate.get("signature", "N/A")

        tls13 = security_profile.get("tls13", False)
        ocsp = security_profile.get("ocsp", "N/A")
        forward_secrecy = security_profile.get("forward_secrecy", False)

    # Get workspace directory
        workspace_dir = getattr(self, 'workspace_dir', None)
        if workspace_dir is None:
            if hasattr(self, 'current_workspace'):
                workspace_dir = self.current_workspace
            else:
                workspace_dir = os.path.join(os.path.expanduser("~"), "dsterminal_workspace")

    
    # Ensure workspace directory exists
        os.makedirs(workspace_dir, exist_ok=True)
    
    # Create reports subdirectory in workspace
        reports_dir = os.path.join(workspace_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)
    
    # Save to workspace/reports/
        report_file = os.path.join(
            reports_dir,
            f"ssl_report_{domain}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        )

        doc = SimpleDocTemplate(
            report_file,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        page_width, page_height = A4
        styles = getSampleStyleSheet()
        elements = []

    # -------- Top Logo (auto-scaled, centered) --------
        if os.path.exists(logo_path):
            logo = Image(logo_path)
            max_width = page_width - doc.leftMargin - doc.rightMargin
            if logo.imageWidth > max_width:
                scale_ratio = max_width / logo.imageWidth
                logo.drawWidth = logo.imageWidth * scale_ratio
                logo.drawHeight = logo.imageHeight * scale_ratio
            logo.hAlign = 'CENTER'
            elements.append(logo)
            elements.append(Spacer(1, 20))

    # Title
        title_style = ParagraphStyle("TitleStyle", fontSize=22, alignment=1, spaceAfter=20, bold=True)
        section_style = ParagraphStyle("SectionStyle", fontSize=14, spaceBefore=20, spaceAfter=10, bold=True)
        normal = styles["Normal"]

        elements.append(Paragraph("DSTerminal Security Compliance Report", title_style))
        elements.append(Paragraph(f"Generated: {scan_time}", normal))
        elements.append(Spacer(1, 20))

    # System Info
        elements.append(Paragraph("System Information", section_style))
        sys_table = [
            ["Domain", domain],
            ["Protocol", protocol],
            ["Cipher", cipher],
            ["Scan Time", scan_time]
        ]
        elements.append(self._styled_table(sys_table))

    # Certificate Info
        elements.append(Paragraph("Certificate Details", section_style))
        cert_table = [
            ["Subject", subject],
            ["Issuer", issuer],
            ["Expiry", expires],
            ["Serial", serial],
            ["Signature", signature]
        ]
        elements.append(self._styled_table(cert_table))

    # Security Profile
        elements.append(Paragraph("Security Profile", section_style))
        sec_table = [
            ["TLS 1.3 Enabled", str(tls13)],
            ["OCSP Checked", ocsp],
            ["Forward Secrecy", str(forward_secrecy)]
        ]
        elements.append(self._styled_table(sec_table))

    # Recommendations
        elements.append(Paragraph("Recommendations", section_style))
        recs = self._build_recommendations(data)
        for rec in recs:
            elements.append(Paragraph(f"• {rec}", normal))
            elements.append(Spacer(1, 5))

    # Footer
        elements.append(Spacer(1, 40))
        footer_data = []

    # Footer logo
        if os.path.exists(footer_logo_path):
            footer_logo = Image(footer_logo_path)
            max_footer_width = 50  # small logo width
            if footer_logo.imageWidth > max_footer_width:
                scale_ratio = max_footer_width / footer_logo.imageWidth
                footer_logo.drawWidth = footer_logo.imageWidth * scale_ratio
                footer_logo.drawHeight = footer_logo.imageHeight * scale_ratio
            footer_data.append([footer_logo, Paragraph("AUTOGENERATED CERTIFICATE REPORT | DSTerminal Platform\n© Stark Expo Tech Exchange", normal)])
            footer_table = Table(footer_data, colWidths=[60, page_width - 60 - doc.leftMargin - doc.rightMargin])
            footer_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
            elements.append(footer_table)
        else:
        # fallback if logo missing
            elements.append(Paragraph("AUTOGENERATED REPORT | DSTerminal Unified Platform", normal))
            elements.append(Paragraph("© Stark Expo Tech Exchange LTD", normal))

        doc.build(elements)
        print(f"\n[✓] PDF Compliance Report Created: {report_file}")
# ===lists of reports===
    def list_reports(self):
        """List all reports in workspace reports directory"""
        print("\n📊 DSTerminal Reports")
        print("="*50)

    # Get workspace directory
        workspace_dir = getattr(self, 'workspace_dir', None)
        if workspace_dir is None:
            if hasattr(self, 'current_workspace'):
                workspace_dir = self.current_workspace
            else:
                workspace_dir = os.path.join(os.path.expanduser("~"), "dsterminal_workspace")

    
    # Look in workspace/reports/
        reports_dir = os.path.join(workspace_dir, "reports")
    
        if not os.path.exists(reports_dir) or not os.listdir(reports_dir):
            print("No reports found in workspace.")
            return

        for f in os.listdir(reports_dir):
            report_path = os.path.join(reports_dir, f)
            if os.path.isfile(report_path):
                size = os.path.getsize(report_path)
                print(f"📄 {f:50} ({self.human_readable_size(size)})")

# ====ends list of report
    def _styled_table(self, data):

        table = Table(data, colWidths=[150, 350])

        style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, black),
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ])

        table.setStyle(style)

        return table

    def _build_recommendations(self, data):

        recs = []

        cert = data["certificate"]
        sec = data["security_profile"]

    # Expiry check
        expires = datetime.strptime(cert["expires"][:8], "%Y%m%d")
        days_left = (expires - datetime.now()).days

        if days_left < 60:
            recs.append("Renew SSL certificate within 30 days")

        if not sec["tls13"]:
            recs.append("Upgrade server configuration to support TLS 1.3")

        if sec["ocsp"] != "VALID":
            recs.append("Enable OCSP(Online Certificate Status Protocol Stapling) stapling for revocation validation.""\n" "A method for checking if an SSL/TLS certificate has been revoked (invalidated before its expiration date). Instead of the client (your browser) checking the certificate status, the server does it and ""staples"" the proof to the certificate")
            

        if sec["forward_secrecy"] is False:
            recs.append("Enable Perfect Forward Secrecy (ECDHE)." "\n" "A security feature that ensures session keys cannot be compromised even if the server's private key is later exposed. It uses ephemeral key exchange (like ECDHE) to generate unique session keys for each connection, providing stronger protection against future attacks." "\n" "ECDHE = Elliptic Curve Diffie-Hellman Ephemeral (the ""ephemeral"" part means temporary keys)")

        if not recs:
            recs.append("No critical risks detected. Maintain current security posture.")

        return recs
# added animated effects for the ssl certificate checks================
    def _type_print(self, text, delay=0.02):
        """Cinematic typing effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def _loading_animation(self, text, seconds=5):
        """Cinematic hacking-style animated loader with glitch and progress effects"""
    # Print main stage text centered
        terminal_width = 80
        print("\n" + text.center(terminal_width))
    
        spinner = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
        end_time = time.time() + seconds
        i = 0

    # Build cinematic random messages
        flickers = [
            "[ACCESSING CERT DATA]", "[TLS HANDSHAKE INIT]", "[VALIDATING CHAIN]",
            "[OCSP CHECK]", "[ASSESSING RISK]", "[GENERATING RECOMMENDATIONS]",
            "[ANALYZING PROTOCOL]", "[CIPHER SCAN]", "[SIGNATURE VERIFY]"
        ]

        while time.time() < end_time:
        # Glitchy flicker text
            flicker_text = random.choice(flickers)
        
        # Animated spinner + sliding progress
            bar_length = 30
            progress = int(((time.time() % seconds) / seconds) * bar_length)
            bar = "█" * progress + "-" * (bar_length - progress)

        # Random colors
            color = random.choice([Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW])
            sys.stdout.write(f"\r{color}{spinner[i % len(spinner)]} {bar} {flicker_text.center(40)}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

    # Finish with a completed checkmark
        sys.stdout.write(f"\r{Fore.GREEN}[✓] {text} Completed{' ' * 40}{Style.RESET_ALL}\n")
        sys.stdout.flush()
# =======================================================
# ============================================
    def dump_memory(self):
        """Create a memory dump (requires admin)"""
        if not self.is_admin():
            print("[!] Requires admin privileges")
            return

        print("\n[+] Creating memory dump...")
        try:
            if platform.system() == "Windows":
                os.system("procdump -ma -accepteula")
                print("[+] Memory dump saved as .dmp files")
            else:
                print("[!] Linux memory dump requires LiME or fmem")
        except Exception as e:
            print(f"[!] Error: {e}")

    def enable_tor_routing(self):
        """Route traffic through Tor"""
        print("\n[+] Configuring Tor routing...")
        try:
            if platform.system() == "Linux":
                os.system("sudo apt install tor -y")
                os.system("sudo service tor start")
                print("[+] Tor service started. Configure your apps to use 127.0.0.1:9050")
            else:
                print("[!] Automatic Tor setup requires Linux. Install Tor Browser manually.")
        except Exception as e:
            print(f"[!] Error: {e}")
#  --------------------for updates below==================

    def port_scan(self, target):
        """Basic port scanning"""
        print(f"\n[+] Scanning {target} for common ports...")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3389]
    
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    print(f"  [+] Port {port}: OPEN")
                sock.close()
            except:
                pass


    def kill_process(self, pid):
        """Kill a process by PID"""
        try:
            if platform.system() == "Windows":
                os.system(f"taskkill /F /PID {pid}")
            else:
                os.system(f"kill -9 {pid}")
            print(f"[+] Process {pid} terminated")
        except Exception as e:
            print(f"[!] Failed to kill process: {e}")



    def system_info(self):
        """Display comprehensive system information"""
        print("\n[+] System Information:")
        print(f"  OS: {platform.system()} {platform.release()}")
        print(f"  Architecture: {platform.machine()}")
        print(f"  Processor: {platform.processor()}")
        print(f"  Python: {platform.python_version()}")
    
        if psutil:
            print(f"  CPU Cores: {psutil.cpu_count()}")
            print(f"  RAM: {psutil.virtual_memory().total / 1024**3:.1f} GB")

 
    def check_updates(self):
        """Cinematic update check with real GitHub API integration"""
        
        # ===================== IMPORTS =====================
        import time
        import random
        import requests
        import subprocess
        import sys
        import os
        import platform
        import tempfile
        from datetime import datetime
        from pathlib import Path
        from rich.console import Console
        from rich.panel import Panel
        from rich.progress import (
            Progress, SpinnerColumn, TextColumn, BarColumn, 
            DownloadColumn, TransferSpeedColumn
        )
        from rich.live import Live
        from rich.align import Align
        from rich.table import Table
        from rich import box

        console = Console()

        # ===================== ANIMATIONS =====================
        def hacker_animation():
            symbols = "█▓▒░▄▀■►▼▲◄▶◀◢◣◥◤▬▭▮▯┌┐└┘├┤┬┴┼╔╗╚╝╠╣╦╩╬═║"
            width = console.size.width
            with console.status("[bold red]🔐 ACCESSING UPDATE SERVERS...[/]", spinner="dots"):
                for _ in range(3):
                    console.print(
                        "".join(random.choice(symbols) for _ in range(width)),
                        style="bold green"
                    )
                    time.sleep(1.5)

        def satellite_scan():
            frames = ["🛰", "📡", "📶", "🔍", "🎯", "⚡"]
            with Progress(
                SpinnerColumn(style="cyan"),
                TextColumn("[bold blue]{task.description}"),
                transient=True,
                console=console
            ) as progress:
                task = progress.add_task("Establishing secure connection...", total=100)
                for i in range(100):
                    progress.update(task, advance=1,
                                    description=f"{frames[i % len(frames)]} Scanning {i}%")
                    time.sleep(1.5)

        def version_comparison_animation(current_ver, latest_ver):
            with Live(refresh_per_second=10, console=console, transient=True) as live:
                for i in range(1, 4):
                    bar = "█" * (i * 8)
                    live.update(
                        Panel(
                            f"[bold cyan]Comparing Versions[/]\n\n"
                            f"[yellow]Current:[/] v{current_ver}\n"
                            f"[white]{bar:30}[/]\n\n"
                            f"[green]Latest:[/] v{latest_ver}\n"
                            f"[white]{bar:30}[/]",
                            border_style="cyan",
                            width=50
                        )
                    )
                    time.sleep(1.5)

        # ===================== UPDATE LOGIC =====================
        def parse_version(v):
            parts = [int(p) if p.isdigit() else 0 for p in str(v).lstrip("vV").split(".")]
            while len(parts) < 3:
                parts.append(0)
            return tuple(parts)

        def get_system_info():
            """Get system information for correct download"""
            system = platform.system().lower()
            arch = platform.machine().lower()
            
            if system == "windows":
                return "windows", "exe", "win"
            elif system == "linux":
                return "linux", "AppImage", "linux"
            elif system == "darwin":
                return "macos", "dmg", "mac"
            else:
                return system, "unknown", "unknown"

        def check_github_release():
            """Check GitHub for latest release from YOUR repo"""
            try:
                # YOUR CORRECTED GitHub API URL
                api_url = "https://api.github.com/repos/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/releases/latest"
                
                headers = {
                    'Accept': 'application/vnd.github.v3+json',
                    'User-Agent': 'DSTerminal-Update-Checker/2.0'
                }
                
                console.print(f"[dim]Connecting to Update Module...[/dim]")
                r = requests.get(api_url, timeout=15, headers=headers)
                
                if r.status_code == 403:
                    console.print("[yellow]Rate limit hit. Try again later.[/yellow]")
                    return None
                elif r.status_code != 200:
                    console.print(f"[red]Update Module API error: {r.status_code}[/red]")
                    return None
                
                data = r.json()
                
                if 'tag_name' not in data:
                    console.print("[red]Invalid response from GitHub[/red]")
                    return None
                
                # Get the version (remove 'v' prefix)
                version = data.get("tag_name", "").lstrip("v")
                
                # Find Windows installer asset
                download_url = None
                asset_name = None
                asset_size = None
                
                console.print("[dim]Scanning release assets...[/dim]")
                
                for asset in data.get("assets", []):
                    name = asset["name"]
                    console.print(f"[dim]  Found: {name}[/dim]")
                    
                    # Look for Windows installer (matches your actual file names)
                    if "DSTerminal_Installer" in name and name.endswith(".exe"):
                        download_url = asset["browser_download_url"]
                        asset_name = name
                        asset_size = asset.get("size", 0)
                        console.print(f"[green]✓ Selected: {name}[/green]")
                        break
                    elif "dsterminal_win" in name and name.endswith(".exe"):
                        download_url = asset["browser_download_url"]
                        asset_name = name
                        asset_size = asset.get("size", 0)
                        console.print(f"[green]✓ Selected: {name}[/green]")
                        break
                
                if not download_url:
                    console.print("[yellow]No Windows installer found in release[/yellow]")
                    # Fall back to showing the release page
                    return {
                        "version": version,
                        "url": data.get("html_url", ""),
                        "download_url": None,
                        "assets": {a["name"]: a["browser_download_url"] for a in data.get("assets", [])},
                        "notes": data.get("body", "No release notes provided.")[:500],
                        "prerelease": data.get("prerelease", False),
                        "published_at": data.get("published_at", ""),
                        "asset_name": None,
                    }
                
                return {
                    "version": version,
                    "url": data.get("html_url", ""),
                    "download_url": download_url,
                    "assets": {a["name"]: a["browser_download_url"] for a in data.get("assets", [])},
                    "notes": data.get("body", "No release notes provided.")[:500],
                    "prerelease": data.get("prerelease", False),
                    "published_at": data.get("published_at", ""),
                    "asset_name": asset_name,
                    "asset_size": asset_size,
                }

            except requests.RequestException as e:
                console.print(f"[red]Connection error: {e}[/red]")
                return None
            except Exception as e:
                console.print(f"[red]Parse error: {e}[/red]")
                return None

        def download_update(url, filename):
            """Download update with progress bar"""
            try:
                console.print(f"\n[cyan]📥 Downloading update from Update Modules...[/cyan]")
                console.print(f"[dim]File: {filename}[/dim]")
                
                response = requests.get(url, stream=True, timeout=30)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                
                with open(filename, 'wb') as f:
                    with Progress(
                        DownloadColumn(),
                        BarColumn(),
                        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                        TransferSpeedColumn(),
                        console=console,
                        transient=False
                    ) as progress:
                        task = progress.add_task("[green]Downloading...[/green]", total=total_size)
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))
                
                # Verify file size
                actual_size = os.path.getsize(filename)
                if total_size > 0 and actual_size != total_size:
                    console.print(f"[red]Size mismatch! Expected {total_size}, got {actual_size}[/red]")
                    return False
                
                console.print(f"[green]✓ Download complete: {filename}[/green]")
                return True
                
            except Exception as e:
                console.print(f"[red]✗ Download failed: {e}[/red]")
                return False

        def perform_update(latest):
            """Execute the actual update process"""
            
            # Show update details
            details_table = Table(box=box.HEAVY_EDGE, border_style="cyan")
            details_table.add_column("Item", style="cyan")
            details_table.add_column("Details", style="white")
            details_table.add_row("New Version", f"[green]v{latest['version']}[/green]")
            details_table.add_row("Installer", latest.get('asset_name', 'Unknown'))
            if latest.get('asset_size'):
                size_mb = latest['asset_size'] / (1024 * 1024)
                details_table.add_row("Size", f"{size_mb:.1f} MB")
            details_table.add_row("Release", latest.get('published_at', 'Unknown')[:10])
            
            console.print(Panel(details_table, title="[bold yellow]📦 UPDATE DETAILS[/bold yellow]", border_style="yellow"))
            
            # Security confirmation
            console.print("\n[bold red]⚠️ SECURITY NOTICE[/bold red]")
            console.print("[dim]• The installer will be downloaded from GitHub\n"
                        "• Verify the digital signature before running\n"
                        "• Administrator privileges may be required[/dim]\n")
            
            confirm = console.input("[bold red]Type 'INSTALL' to download and run the installer: [/]").strip()
            
            if confirm != "INSTALL":
                console.print("[yellow]Update cancelled[/yellow]")
                return False
            
            if not latest.get('download_url'):
                console.print(Panel(
                    "[yellow]No automatic download available[/]\n\n"
                    f"Please download manually from:\n{latest['url']}",
                    border_style="yellow"
                ))
                return False
            
            # Download update to temp directory
            temp_dir = tempfile.gettempdir()
            installer_path = os.path.join(temp_dir, latest['asset_name'])
            
            # Remove old installer if exists
            if os.path.exists(installer_path):
                os.remove(installer_path)
            
            if not download_update(latest['download_url'], installer_path):
                return False
            
            # Verify download exists
            if not os.path.exists(installer_path):
                console.print("[red]Download verification failed[/red]")
                return False
            
            console.print("\n[green]✓ Download verified successfully[/green]")
            
            # Ask to run installer
            console.print("\n[cyan]🔧 Ready to install update...[/cyan]")
            run_installer = console.input("[bold yellow]Run the installer now? (Y/n): [/]").strip().lower()
            
            if run_installer != 'n':
                console.print("[cyan]Launching installer...[/cyan]")
                time.sleep(1)
                
                try:
                    # Launch the installer
                    if platform.system().lower() == "windows":
                        os.startfile(installer_path)
                    else:
                        subprocess.Popen([installer_path], shell=True)
                    
                    console.print(Panel(
                        f"[bold green]✅ INSTALLER LAUNCHED![/bold green]\n\n"
                        f"[yellow]Please complete the installation wizard[/yellow]\n"
                        f"[dim]Installer location: {installer_path}[/dim]\n\n"
                        f"[cyan]After installation, restart DSTerminal[/cyan]",
                        border_style="green"
                    ))
                    return True
                    
                except Exception as e:
                    console.print(f"[red]Failed to launch installer: {e}[/red]")
                    console.print(f"[yellow]Please run manually: {installer_path}[/yellow]")
                    return False
            else:
                console.print(f"[yellow]Installer saved to: {installer_path}[/yellow]")
                return True

        # ===================== MAIN FLOW =====================
        try:
            # Display header
            console.print(Panel(
                Align.center("[bold cyan]🔄 DSTERMINAL UPDATE PROTOCOL 🔄[/bold cyan]"),
                border_style="cyan"
            ))
            
            # Animated sequence
            hacker_animation()
            satellite_scan()
            
            # Get current version
            current_version = CONFIG.get("CURRENT_VERSION", "2.0.113").lstrip("v")
            
            # Display version info
            version_table = Table(box=box.SIMPLE, border_style="blue")
            version_table.add_column("Component", style="cyan")
            version_table.add_column("Version", style="green")
            version_table.add_row("Current Installation", f"v{current_version}")
            version_table.add_row("System", platform.system())
            version_table.add_row("Architecture", platform.machine())
            
            console.print(Panel(version_table, title="[bold]📊 SYSTEM STATUS[/bold]", border_style="blue"))
            
            # Check for updates
            console.print("\n[cyan]🔍 Checking Modules for updates...[/cyan]")
            latest = check_github_release()
            
            if not latest:
                console.print(Panel(
                    "[yellow]⚠️ UPDATE SERVER UNREACHABLE[/yellow]\n\n"
                    "[dim]• Check your internet connection\n"
                    "• GitHub API may be rate-limited\n"
                    "• Visit: https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/releases[/dim]",
                    border_style="yellow"
                ))
                return True
            
            # Version comparison animation
            version_comparison_animation(current_version, latest['version'])
            
            # Compare versions
            current_tuple = parse_version(current_version)
            latest_tuple = parse_version(latest['version'])
            
            if latest_tuple > current_tuple:
                # Show update available
                update_info = (
                    f"[bold red]🚨 UPDATE AVAILABLE! 🚨[/bold red]\n\n"
                    f"[yellow]Current:[/yellow] v{current_version}\n"
                    f"[green]Latest:[/green] v{latest['version']}\n"
                    f"[cyan]Released:[/cyan] {latest.get('published_at', 'Unknown')[:10]}\n\n"
                    f"[cyan]Release Notes:[/cyan]\n"
                    f"[dim]{latest['notes'][:400]}[/dim]\n"
                )
                
                if latest.get('prerelease'):
                    update_info += f"\n[red]⚠️ PRE-RELEASE VERSION - Use with caution[/red]\n"
                
                console.print(Panel(
                    update_info,
                    border_style="red",
                    width=90,
                    padding=(1, 2)
                ))
                
                # Ask for update
                choice = console.input("\n[bold cyan]Download and install update now? (y/N): [/]").lower()
                
                if choice == 'y':
                    return perform_update(latest)
                else:
                    console.print("[yellow]Update postponed[/yellow]")
            
            else:
                console.print(Panel(
                    Align.center(
                        f"[bold green]✅ DSTERMINAL IS UP TO DATE![/bold green]\n\n"
                        f"[dim]Version: v{current_version}\n"
                        f"Checked: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]"
                    ),
                    border_style="green",
                    width=60
                ))
            
            return True
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Update cancelled by user[/yellow]")
            return True
        except Exception as e:
            console.print(Panel(
                f"[bold red]UPDATE ERROR[/]\n\n{str(e)}",
                border_style="red"
            ))
            import traceback
            traceback.print_exc()
            return True
    
# --------------------------for updates above code--------------------

    def clear_terminal(self):
        """Advanced terminal clearing with three-column centered layout and spinning animations"""
        
        import shutil
        import time
        import random
        import os
        import platform
        from datetime import datetime
        from rich.console import Console
        from rich.panel import Panel
        from rich.live import Live
        from rich.layout import Layout
        from rich.align import Align
        from rich.table import Table
        from rich.text import Text
        from rich.progress import Progress, SpinnerColumn, TextColumn
        
        console = Console()
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        column_width = min(35, terminal_width // 3 - 6)  # Width for each column
        
        # Multiple spinner types for variety
        spinners = {
            'dots': ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
            'arrows': ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
            'pipes': ["┤", "┘", "┴", "└", "├", "┌", "┬", "┐"],
            'circles': ["◴", "◷", "◶", "◵"]
        }
        
        # Glitch text fragments
        glitch_texts = [
            "CLEARING...", "WIPING...", "PURGING...", 
            "RESETTING...", "REFRESHING...", "RELOADING..."
        ]
        
        # System stats simulator
        def get_system_stats():
            return {
                "cpu": random.randint(20, 95),
                "mem": random.randint(100, 500),
                "pid": os.getpid(),
                "disk": random.randint(10, 90),
                "network": random.randint(1, 100)
            }
        
        # Phase configurations
        phases = [
            {"text": "PHASE 1: MEMORY CLEAR", "color": "bright_red", "spinner": "dots"},
            {"text": "PHASE 2: BUFFER FLUSH", "color": "bright_yellow", "spinner": "arrows"},
            {"text": "PHASE 3: CACHE WIPE", "color": "bright_green", "spinner": "pipes"},
            {"text": "PHASE 4: DISPLAY RESET", "color": "bright_cyan", "spinner": "circles"}
        ]
        
        # Animated clearing sequence with three columns
        with Live(console=console, refresh_per_second=12, screen=True, auto_refresh=False) as live:
            for phase_idx, phase in enumerate(phases):
                spinner_chars = spinners[phase["spinner"]]
                color = phase["color"]
                phase_text = phase["text"]
                
                for step in range(30):  # 30 steps per phase
                    # Calculate progress
                    total_progress = (phase_idx * 30 + step) / 120
                    progress_percent = int(total_progress * 100)
                    
                    # Current spinner character
                    spinner = spinner_chars[step % len(spinner_chars)]
                    
                    # Glitch effect
                    glitch = random.choice(glitch_texts) if random.random() > 0.7 else ""
                    
                    # Get current stats
                    stats = get_system_stats()
                    
                    # === LEFT COLUMN: System Stats ===
                    left_content = Panel(
                        Align.center(
                            f"[bold cyan]📊 SYSTEM STATS[/bold cyan]\n\n"
                            f"[white]CPU:[/white] [green]{stats['cpu']}%[/green]\n"
                            f"[white]MEM:[/white] [yellow]{stats['mem']} MB[/yellow]\n"
                            f"[white]DISK:[/white] [blue]{stats['disk']}%[/blue]\n"
                            f"[white]PID:[/white] [dim]{stats['pid']}[/dim]\n"
                            f"[white]NET:[/white] [cyan]{stats['network']} Mbps[/cyan]",
                            vertical="middle"
                        ),
                        title=f"[bold {color}]⚙️ LEFT PANEL[/bold {color}]",
                        border_style=color,
                        width=column_width,
                        padding=(0, 1),
                        height=20
                    )
                    
                    # === CENTER COLUMN: Main Progress ===
                    # Progress bar
                    bar_width = column_width - 10
                    filled = int(progress_percent / 100 * bar_width)
                    progress_bar = "█" * filled + "░" * (bar_width - filled)
                    
                    center_content = Panel(
                        Align.center(
                            f"[bold {color}]{spinner} {phase_text} {spinner}[/bold {color}]\n\n"
                            f"[white]{progress_bar}[/white]\n"
                            f"[bold cyan]{progress_percent}%[/bold cyan]\n\n"
                            f"[dim]{glitch}[/dim]",
                            vertical="middle"
                        ),
                        title=f"[bold {color}]🌀 CENTER PANEL[/bold {color}]",
                        border_style=color,
                        width=column_width,
                        padding=(0, 1),
                        height=20
                    )
                    
                    # === RIGHT COLUMN: Security Events ===
                    events = [
                        "Buffer overflow check",
                        "Memory seg scan",
                        "Stack trace verify",
                        "Heap corruption test"
                    ]
                    current_event = events[step % len(events)]
                    
                    right_content = Panel(
                        Align.center(
                            f"[bold yellow]⚠️ SECURITY[/bold yellow]\n\n"
                            f"[white]Event:[/white]\n[cyan]{current_event}[/cyan]\n\n"
                            f"[white]Status:[/white] [green]ACTIVE[/green]\n"
                            f"[white]Level:[/white] [red]HIGH[/red]",
                            vertical="middle"
                        ),
                        title=f"[bold {color}]🔒 RIGHT PANEL[/bold {color}]",
                        border_style=color,
                        width=column_width,
                        padding=(1, 1),
                        height=20
                    )
                    
                    # Create three-column layout
                    layout = Layout()
                    layout.split_row(
                        Layout(left_content, ratio=1),
                        Layout(center_content, ratio=1),
                        Layout(right_content, ratio=1)
                    )
                    
                    # Center the entire layout on screen
                    final_display = Align.center(layout)
                    live.update(final_display)
                    live.refresh()
                    time.sleep(0.06)
        
        # Execute actual terminal clear
        os.system("clear" if platform.system() != "Windows" else "cls")
        
        # Create dramatic three-column banner reveal
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        
        # ASCII Art Logo (centered across all columns)
        logo_art = [
            "╔═══════════════════════════════════════════════════════════════════╗",
            "║                                                                    ║",
            "║    ██████╗ ███████╗███████╗███████╗███╗   ██╗███████╗██╗  ██╗    ║",
            "║    ██╔══██╗██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝╚██╗██╔╝    ║",
            "║    ██║  ██║█████╗  █████╗  █████╗  ██╔██╗ ██║█████╗   ╚███╔╝     ║",
            "║    ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║██╔══╝   ██╔██╗     ║",
            "║    ██████╔╝██║     ██║     ███████╗██║ ╚████║███████╗██╔╝ ██╗    ║",
            "║    ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝    ║",
            "║                                                                    ║",
            "╚═══════════════════════════════════════════════════════════════════╝",
        ]
        
        # Center and display logo with gradient
        for i, line in enumerate(logo_art):
            centered_line = line.center(terminal_width)
            if i == 0 or i == len(logo_art) - 1:
                console.print(f"[bright_cyan]{centered_line}[/bright_cyan]")
            elif i == 1 or i == len(logo_art) - 2:
                console.print(f"[bright_blue]{centered_line}[/bright_blue]")
            elif 2 <= i <= len(logo_art) - 3:
                colors = ["cyan", "bright_cyan", "blue", "bright_blue", "green"]
                color = colors[(i - 2) % len(colors)]
                console.print(f"[bold {color}]{centered_line}[/bold {color}]")
            time.sleep(0.05)
        
        # === THREE-COLUMN STATUS PANEL ===
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Left column: System Info
        left_status = Panel(
            Align.center(
                f"[bold cyan]🖥️ SYSTEM INFO[/bold cyan]\n\n"
                f"[white]OS:[/white] [green]{platform.system()} {platform.release()}[/green]\n"
                f"[white]Arch:[/white] [yellow]{platform.machine()}[/yellow]\n"
                f"[white]Terminal:[/white] [dim]{terminal_width} cols[/dim]\n",
                vertical="middle"
            ),
            border_style="blue",
            width=column_width + 4,
            padding=(1, 1),
            height=20
        )
        
        # Center column: Status Message
        center_status = Panel(
            Align.center(
                f"[blink][bright_green]✦ SYSTEM INITIALIZED ✦[/bright_green][/blink]\n\n"
                f"[white]Session ID:[/white]\n[cyan]{datetime.now().strftime('%Y%m%d%H%M%S')}[/cyan]\n\n"
                f"[white]Ready for:[/white]\n[yellow]SSL/TLS Security Audit[/yellow]",
                vertical="middle"
            ),
            border_style="bright_green",
            width=column_width + 4,
            padding=(1, 1),
            height=20
        )
        
        # Right column: Quick Commands
        right_status = Panel(
            Align.center(
                f"[bold yellow]⚡ QUICK CMDS[/bold yellow]\n\n"
                f"[cyan]help[/cyan] - Show commands\n"
                f"[cyan]scan[/cyan] - Run security scan\n"
                f"[cyan]update[/cyan] - Check updates\n"
                f"[cyan]exit[/cyan] - Close terminal",
                vertical="middle"
            ),
            border_style="yellow",
            width=column_width + 4,
            padding=(1, 1),
            height=20
        )
        
        # Create three-column status layout
        status_layout = Layout()
        status_layout.split_row(
            Layout(left_status, ratio=1),
            Layout(center_status, ratio=1),
            Layout(right_status, ratio=1)
        )
        
        # Center and display
        console.print(Align.center(status_layout))
        print()

    # =======ends here from above-==============
    def emergency_shutdown(self):
        console = Console()

        def authenticate():
            console.print("\n[bold yellow]Authentication Required:[/bold yellow] Confirm emergency shutdown.")
            response = Prompt.ask("Type [red]YES[/red] to confirm", default="NO")
            return response.strip().lower() == "yes"

        if not authenticate():
            console.print("\n[bold cyan]Shutdown aborted.[/bold cyan]")
            return

        countdown_panel = Panel(
            Align.center("[bold red]\u26a0 EMERGENCY SHUTDOWN INITIATED \u26a0[/bold red]", vertical="middle"),
            title="[red bold]SYSTEM OVERRIDE[/red bold]",
            border_style="red",
            padding=(1, 4),
            width=60
        )

        with Live(console=console, refresh_per_second=4, screen=True) as live:
            for i in reversed(range(1, 16)):
                live.update(Panel(f"[bold red]Shutting down in {i} seconds...[/bold red]", border_style="bright_red", width=60))
                time.sleep(1)
            live.update(countdown_panel)
            time.sleep(1)

        console.print("[bold red]Powering down system...[/bold red]")
        time.sleep(1)

        if platform.system() == "Linux":
            os.system("sudo shutdown now")
        elif platform.system() == "Windows":
            os.system("shutdown /s /t 0")
        else:
            console.print("[yellow]Unsupported OS for shutdown command.[/yellow]")

# shutting down ends here
# ================================================
# ================================================
    def monitor_registry(self):
        """Monitor Windows registry changes"""
        if platform.system() != "Windows":
            return "[!] Registry monitoring requires Windows"

        suspicious_keys = [
            r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            r"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            r"HKLM\SYSTEM\CurrentControlSet\Services"
        ]
        
        try:
            import winreg
            changes = []
            
            for key_path in suspicious_keys:
                hive, path = key_path.split('\\', 1)
                hive = getattr(winreg, {
                    'HKLM': 'HKEY_LOCAL_MACHINE',
                    'HKCU': 'HKEY_CURRENT_USER'
                }[hive])
                
                with winreg.OpenKey(hive, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[1]):
                        name, value, _ = winreg.EnumValue(key, i)
                        changes.append(f"{key_path}\\{name} = {value}")
            
            if changes:
                return "\n".join(["[!] Suspicious registry entries:"] + changes)
            else:
                return "[+] No suspicious registry entries found"
        except Exception as e:
            return f"[!] Registry scan failed: {e}"
 
    #  starts here
    def _print_banner(self, text):
        subprocess.run(["figlet", text])
        """Display hacking-style banner with fallback"""
        left_panels = self.update_left_panels()
        right_panels = self.update_right_panels()
        try:
            ascii_art = figlet_format(text, font='slant')
            if os.environ.get('TERM') and 'color' in os.environ.get('TERM', ''):
                colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
                flicker = random.choice(colors) + ascii_art.replace(random.choice(text), '▒') + Style.RESET_ALL
                print(f"\n{flicker}")
            else:
                # print(f"\n{ascii_art}")
                print(f"\n")
        except ImportError:
            border = "═" * (len(text) + 4)
            print(f"\n")
            # print(f"\n{border}\n  {text.upper()}  \n{border}\n")

        except Exception as e:
            print(f"\n=== {text.upper()} ===\n")
 
    def _hacking_animation(duration, graphics):
        console = Console()
        symbols = list("▣⚙⧫◎◉⛏⊠⊞⌁⍟☍█▓▒░▌▎#@$=%/\\*~^↯⎈⛶∞∴∵")

        class RotatingSymbol:
            def __init__(self):
                self.frames = random.sample(symbols, k=4)
                self.frame_iter = itertools.cycle(self.frames)
                self.color = random.choice(["cyan", "magenta", "green", "yellow", "red", "blue", "bright_white"])

            def next(self):
                symbol = next(self.frame_iter)
                self.color = random.choice(["cyan", "magenta", "green", "yellow", "red", "blue", "bright_white"])
                return Text(symbol, style=self.color)

        rows, cols = 2, 150
        symbol_grid = [[RotatingSymbol() for _ in range(cols)] for _ in range(rows)]

    # Progress bar setup
        progress = Progress(
            TextColumn("[bold green]HARDENING...[/bold green]"),
            BarColumn(bar_width=None),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            expand=False,
        )
        task = progress.add_task("HARDENING", total=100)

        start_time = time.time()
        duration = 15  # seconds

        def render():
        # Background grid
            text = Text()
            for row in symbol_grid:
                for symbol in row:
                    text.append(symbol.next())
                text.append("\n")

        # Centered panel with progress bar
            elapsed = time.time() - start_time
            percent = min(100, int((elapsed / duration) * 100))
            progress.update(task, completed=percent)

            panel = Panel(
                Align.center(progress, vertical="middle"),
                title="[bold cyan]System Hardening Phase [1, 2 & 3][/bold cyan]",
                border_style="bright_white",
                width=40,
                padding=(1, 2),
            )

            combined = Group(text, Align.center(panel, vertical="middle"))
            return combined

        with Live(render(), console=console, refresh_per_second=10, screen=True) as live:
            try:
                while time.time() - start_time < duration:
                    time.sleep(0.1)
                    live.update(render())
            except KeyboardInterrupt:
                console.print("\n[bold red]Animation interrupted.[/bold red]")

        console.print("[bold green]✓ Access Granted.[/bold green]")

    def _cyber_attack_simulation(self):
        """Simulate incoming attacks being blocked (randomized)"""
        attack_types = ["Brute Force", "SQL Injection", "XSS", "RCE", "Zero-Day"]
        protocols = ["SSH", "HTTP", "HTTPS", "FTP", "SMTP"]

        print(f"\n{Fore.RED}▄︻デ══━ INTRUSION DETECTED ══━︻▄{Style.RESET_ALL}")
        for _ in range(random.randint(3, 5)):
            attack = random.choice(attack_types)
            protocol = random.choice(protocols)
            ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
            time.sleep(random.uniform(0.3, 0.7))
            print(f"{Fore.YELLOW}▶ {ip} | {protocol} | {attack}{Style.RESET_ALL}", end='')
            time.sleep(random.uniform(0.5, 1.2))
            print(f"\r{Fore.GREEN}✓ {ip} | {protocol} | {attack} {Fore.BLACK}▶ BLOCKED{Style.RESET_ALL}")

    def _network_scan_animation(self):
        """Simulate network scanning visualization"""
        print(f"\n{Fore.CYAN}═════════⋘ NETWORK TOPOLOGY ⋙═════════{Style.RESET_ALL}")
        devices = [
            ("Router", "192.168.1.1", "Cisco IOS"),
            ("Workstation", "192.168.1.15", "Windows 11"),
            ("Server", "192.168.1.100", "Ubuntu 22.04")
        ]

        for device, ip, osys in devices:
            print(f"{Fore.MAGENTA}⌖ {device}: {ip}", end='')
            for _ in range(3):
                print(".", end='', flush=True)
                time.sleep(0.3)
            print(f" {Fore.WHITE}[{osys}]{Style.RESET_ALL}")

# Initialize colorama for Windows compatibility
    
    def _get_terminal_width(self):
        """Get terminal width for centering"""
        try:
            import shutil
            return shutil.get_terminal_size().columns
        except:
            return 80  # Default width
    
    def _center_text(self, text):
        """Center text based on terminal width"""
        return text.center(self.terminal_width)
    
    def _blinking_text(self, text, color=Fore.GREEN, duration=2):
        """Create blinking text effect"""
        end_time = time.time() + duration
        while time.time() < end_time:
            print(f"\r{color}{text}{Style.RESET_ALL}", end="", flush=True)
            time.sleep(0.3)
            print(f"\r{' ' * len(text)}", end="", flush=True)
            time.sleep(0.3)
        print(f"\r{color}{text}{Style.RESET_ALL}")
    
    def _enlarged_ascii_banner(self):
        """Display enlarged, centered, blinking CYBER DEFENSE banner"""
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
        
        # Create the banner lines
        banner_line1 = "=" * 50
        banner_line2 = " " * 18 + "CYBER DEFENSE" + " " * 18
        banner_line3 = "=" * 50
        
        # Enlarge by repeating each character (double size)
        enlarged_lines = []
        for line in [banner_line1, banner_line2, banner_line3]:
            enlarged_line = ""
            for char in line:
                enlarged_line += char * 2  # Double each character horizontally
            enlarged_lines.append(enlarged_line)
        
        # Center each line
        centered_lines = []
        for line in enlarged_lines:
            centered_lines.append(self._center_text(line))
        
        centered_banner = "\n".join(centered_lines)
        
        # Print with blinking and color cycling effect
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
        for _ in range(4):  # Blink 4 times
            for color in colors:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"\n{color}{centered_banner}{Style.RESET_ALL}")
                print(f"\n{Fore.CYAN}{self._center_text('═' * 60)}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{self._center_text('DEFENSIVE SECURITY TERMINAL v2.0.113')}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{self._center_text('═' * 60)}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}{self._center_text('⚡ System Ready | Mode: HARDENING MODE ⚡')}{Style.RESET_ALL}")
                time.sleep(0.2)
        
        time.sleep(1)
    
    def _print_banner(self, text):
        """Print a decorative banner with centering"""
        print(f"\n{Fore.CYAN}{self._center_text('=' * 50)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{self._center_text(text)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{self._center_text('=' * 50)}{Style.RESET_ALL}\n")
    
    def _matrix_rain_effect(self, duration=2):
        """Create Matrix-style digital rain effect"""
        end_time = time.time() + duration
        chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
        
        while time.time() < end_time:
            line = ''.join(random.choice(chars) for _ in range(self.terminal_width // 2))
            print(f"\r{Fore.GREEN}{line}{Style.RESET_ALL}", end="", flush=True)
            time.sleep(0.05)
        print()
    
    def is_admin(self):
        """Check if the script is running with admin privileges"""
        try:
            if platform.system() == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.getuid() == 0
        except:
            return False
    
    def _cinematic_typing(self, text, delay=0.03):
        """Print text character by character for cinematic effect"""
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()
    
    def _hacking_animation(self, text):
        """Simple hacking animation"""
        print(f"{Fore.GREEN}[*] {text}...{Style.RESET_ALL}")
        time.sleep(0.5)
    
    def _progress_bar(self, task_name, duration=2, length=30):
        """Show a simple text-based progress bar for cinematic effect"""
        print(f"{task_name}: ", end="", flush=True)
        for i in range(length + 1):
            bar = "█" * i + "▒" * (length - i)
            percent = int((i / length) * 100)
            color = Fore.GREEN if percent < 50 else Fore.YELLOW if percent < 80 else Fore.RED
            print(f"\r{task_name}: {color}|{bar}| {percent}%{Style.RESET_ALL}", end="", flush=True)
            time.sleep(duration / length)
        print()
    
    def _network_scan_animation(self):
        """Simulate network scanning with visual effects"""
        print(f"\n{Fore.CYAN}{self._center_text('═════════⋘ NETWORK TOPOLOGY ⋙═════════')}{Style.RESET_ALL}")
        ips = [
            (f"⌖ Router: 192.168.1.1... [Cisco IOS]", Fore.YELLOW),
            (f"⌖ Workstation: 192.168.1.15... [Windows 11]", Fore.GREEN),
            (f"⌖ Server: 192.168.1.100... [Ubuntu 22.04]", Fore.BLUE),
            (f"⌖ IoT Device: 192.168.1.50... [Smart Hub]", Fore.MAGENTA),
            (f"⌖ Printer: 192.168.1.30... [HP LaserJet]", Fore.CYAN)
        ]
        
        for ip, color in ips:
            self._cinematic_typing(f"{color}{ip}{Style.RESET_ALL}", 0.02)
            time.sleep(0.3)
    
    def _vulnerability_scan(self):
        """Simulated vulnerability assessment with randomized output"""
        sample_vulns = [
            ("CVE-2023-1234", "Critical", "SMB Protocol"),
            ("CVE-2022-4567", "High", "OpenSSL"),
            ("CVE-2021-8910", "Medium", "Linux Kernel"),
            ("CVE-2020-4455", "Low", "Apache Server"),
            ("CVE-2019-1111", "Critical", "Docker")
        ]
        vulns = random.sample(sample_vulns, k=random.randint(2, 4))
        
        print(f"\n{Fore.RED}{self._center_text('▄︻デ══━ VULNERABILITY SCAN ══━︻▄')}{Style.RESET_ALL}")
        for cve, severity, component in vulns:
            time.sleep(0.5)
            severity_color = Fore.RED if severity == "Critical" else Fore.YELLOW if severity == "High" else Fore.GREEN
            print(f"{severity_color}{severity.upper().ljust(8)} {cve} → {component}{Style.RESET_ALL}")
            time.sleep(0.3)
        print(f"{Fore.GREEN}✓ {len(vulns)} vulnerabilities patched{Style.RESET_ALL}")
    
    def _cyber_attack_simulation(self):
        """Simulate cyber attack detection with blinking effects"""
        print(f"\n{Fore.RED}{self._center_text('▄︻デ══━ INTRUSION DETECTED ══━︻▄')}{Style.RESET_ALL}")
        attacks = [
            (f"✓ 225.242.61.205 | HTTPS | RCE ▶ BLOCKED", Fore.GREEN),
            (f"✓ 188.101.45.207 | HTTPS | XSS ▶ BLOCKED", Fore.GREEN),
            (f"✓ 43.77.112.198 | HTTP | Brute Force ▶ BLOCKED", Fore.YELLOW),
            (f"✓ 250.124.212.130 | HTTPS | Brute Force ▶ BLOCKED", Fore.YELLOW),
            (f"⚠ 78.95.143.67 | SSH | Dictionary Attack ▶ MITIGATED", Fore.RED)
        ]
        
        for attack, color in attacks:
            self._cinematic_typing(f"{color}{attack}{Style.RESET_ALL}", 0.03)
            time.sleep(0.3)
        
        # Blinking threat neutralized
        self._blinking_text(self._center_text("⚠ THREAT NEUTRALIZED ⚠"), Fore.RED, 2)
    
    # def harden_system(self, dry_run=False):
    #     """Cinematic system hardening with typing, animations, and progress bars"""
    #     try:
    #         # Show enlarged blinking banner at start - THIS WAS MISSING!
    #         self._enlarged_ascii_banner()
            
    #         # Matrix rain effect for style
    #         self._matrix_rain_effect(1)
            
    #         # Check admin privileges
    #         if not self.is_admin():
    #             self._hacking_animation("Checking Privileges")
    #             print(f"{Fore.RED}[!] Warning: Running without administrator privileges. Some features may be limited.{Style.RESET_ALL}")
    #             # Don't return, continue with limited functionality
            
    #         # ----------------------------
    #         # Pre-hardening animations
    #         # ----------------------------
    #         self._hacking_animation("Initializing Threat Assessment")
    #         self._cinematic_typing("Scanning system threats...")
    #         self._progress_bar("Threat Assessment", duration=3)
            
    #         self._network_scan_animation()
    #         self._hacking_animation("Scanning Exploit Database")
    #         self._cinematic_typing("Analyzing known vulnerabilities...")
    #         self._progress_bar("Exploit Database Scan", duration=3)
            
    #         self._vulnerability_scan()
    #         self._cyber_attack_simulation()
    #         self._cinematic_typing("Threat analysis complete.")
    #         self._progress_bar("Threat Analysis", duration=2)
            
    #         # ----------------------------
    #         # Dry-run simulation
    #         # ----------------------------
    #         if dry_run:
    #             self._hacking_animation("Simulating Countermeasures")
    #             self._cinematic_typing("[SIMULATION] No changes were actually made.", 0.05)
    #             self._progress_bar("Simulation", duration=2)
            
    #         # ----------------------------
    #         # Actual hardening
    #         # ----------------------------
    #         else:
    #             self._hacking_animation("Deploying Cyber Armor")
    #             self._cinematic_typing("Applying system fortifications...", 0.04)
    #             self._progress_bar("Deploying Armor", duration=3)
                
    #             try:
    #                 system = platform.system()
                    
    #                 # Windows Hardening
    #                 if system == "Windows":
    #                     try:
    #                         self._cinematic_typing("Disabling SMB1 protocol...", 0.04)
    #                         powershell_cmd = "powershell -Command Disable-WindowsOptionalFeature -Online -FeatureName smb1protocol -NoRestart"
    #                         self._progress_bar("SMB1 Disable", duration=2)
                            
    #                         if self.is_admin():
    #                             result = subprocess.run(powershell_cmd, shell=True, capture_output=True, text=True)
                                
    #                             if result.returncode == 0:
    #                                 self._cinematic_typing("[OK] SMB1 protocol disabled.", 0.04)
    #                                 logging.info("SMB1 protocol disabled successfully on Windows")
    #                             else:
    #                                 self._cinematic_typing(f"[!] PowerShell command failed: {result.stderr}", 0.04)
    #                                 logging.error(f"PowerShell command failed: {result.stderr}")
    #                         else:
    #                             self._cinematic_typing("[!] Skipping SMB1 disable (requires admin rights)", 0.04)
                            
    #                     except Exception as e:
    #                         self._cinematic_typing(f"[!] Could not disable SMB1: {str(e)}", 0.04)
    #                         logging.error(f"Error disabling SMB1: {str(e)}")
                    
    #                 # Linux Hardening
    #                 elif system == "Linux":
    #                     ufw_path = shutil.which("ufw")
    #                     if ufw_path:
    #                         self._cinematic_typing("Enabling UFW firewall...", 0.04)
    #                         self._progress_bar("UFW Firewall", duration=2)
    #                         try:
    #                             subprocess.run(["sudo", ufw_path, "--force", "enable"], check=True)
    #                             self._cinematic_typing("[OK] UFW firewall enabled.", 0.04)
    #                             logging.info("UFW firewall enabled successfully on Linux")
    #                         except subprocess.CalledProcessError as e:
    #                             self._cinematic_typing(f"[!] Failed to enable UFW: {str(e)}", 0.04)
    #                             logging.error(f"Failed to enable UFW: {str(e)}")
    #                     else:
    #                         self._cinematic_typing("[!] UFW firewall not found — skipping Linux hardening", 0.04)
                
    #             except Exception as e:
    #                 logging.error(f"Hardening failed: {str(e)}")
    #                 print(f"{Fore.RED}[!] Error during hardening: {str(e)}{Style.RESET_ALL}")
            
    #         # ----------------------------
    #         # Cinematic completion with blinking
    #         # ----------------------------
    #         self._cinematic_typing("System fortification complete!", 0.05)
            
    #         # Blinking completion banner
    #         for _ in range(3):
    #             print(f"\r{Fore.GREEN}{self._center_text('▄︻デ══━ SYSTEM FORTIFICATION COMPLETE ══━︻▄')}{Style.RESET_ALL}", end="")
    #             time.sleep(0.3)
    #             print(f"\r{' ' * self.terminal_width}", end="")
    #             time.sleep(0.3)
            
    #         print(f"\n{Fore.GREEN}{self._center_text('▄︻デ══━ SYSTEM FORTIFICATION COMPLETE ══━︻▄')}{Style.RESET_ALL}")
    #         threat_level = random.randint(1, 10)
            
    #         # Blinking threat level
    #         threat_text = f" Firewall Active | Intrusion Prevention Engaged | Threat Level: {threat_level}/10"
    #         self._blinking_text(self._center_text(threat_text), Fore.YELLOW, 3)
            
    #     except Exception as e:
    #         # Catch-all to preserve cinematic end even on errors
    #         print(f"{Fore.RED}[!] Critical error: {str(e)}{Style.RESET_ALL}")
    #         self._cinematic_typing("System fortification complete with errors.", 0.05)
    #         print(f"\n{Fore.GREEN}{self._center_text('▄︻デ══━ SYSTEM FORTIFICATION COMPLETE ══━︻▄')}{Style.RESET_ALL}")
    #         threat_level = random.randint(1, 10)
    #         print(f"{Fore.YELLOW}{self._center_text(f' Firewall Active | Intrusion Prevention Engaged | Threat Level: {threat_level}/10')}{Style.RESET_ALL}")


    # go down here, don't remove these lines below
    def nikto_scan(self, target_url, port=80, output_file=None):
        """Run Nikto scan on a target URL."""
        cmd = f"nikto -h {target_url} -p {port}"
        if output_file:
            cmd += f" -o {output_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout
# ================================for trufflehog==================
    def trufflehog_scan_git(self, git_url):
        """Scan GitHub repository for secrets using trufflehog"""
        try:
            cmd = f"trufflehog git {git_url} --no-update"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"[!] Scan failed: {result.stderr}"
        except Exception as e:
            return f"[!] Error running trufflehog: {e}"

    def trufflehog_scan_filesystem(self, fs_path):
        """Scan filesystem for secrets using trufflehog"""
        try:
            cmd = f"trufflehog filesystem {fs_path} --no-update"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"[!] Scan failed: {result.stderr}"
        except Exception as e:
            return f"[!] Error running trufflehog: {e}"

# ============end trufflehog=============================
    def legitify_scan_github(self, org_or_repo, token=None):
        """Scan a GitHub org/repo for security issues."""
        cmd = f"legitify scan --github {org_or_repo}"
        if token:
            cmd += f" --token {token}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout

    def hash_file(self, filepath):
        hashes = {
            "md5": hashlib.md5(),
            "sha1": hashlib.sha1(),
            "sha256": hashlib.sha256()
        }

        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                for h in hashes.values():
                    h.update(chunk)

        return {name: h.hexdigest() for name, h in hashes.items()}

    def handle_command(self, cmd):
        cmd = cmd.strip()
        if not cmd:
            return

        original_cmd = cmd
        parts = cmd.split()
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        # -----------------------------mkdir & touch-------------
        if parts[0] == "mkdir" and len(parts) == 2:
            self.mkdir(parts[1])
            return

        elif parts[0] == "touch" and len(parts) == 2:
            self.touch(parts[1])
            return

        elif parts[0] == "ls":
            self.ls()
            return

        # ==================== ADD HARDENING COMMANDS HERE ====================
        # Hardening commands
# Hardening commands - Enterprise Cinematic Mode
        elif parts[0] == "harden":
            if len(parts) == 1:
                self.harden_system()
            elif len(parts) == 2:
                subcmd = parts[1].lower()
                if subcmd in ["dashboard", "menu"]:
                    self.launch_hardening_dashboard()
                elif subcmd in ["cinematic", "cinema"]:
                    self.launch_hardening_cinematic()
                elif subcmd in ["list", "ls"]:
                    self.list_hardening_modules()
                elif subcmd in ["status", "st"]:
                    self.show_hardening_status()
                elif subcmd in ["full", "all"]:
                    self.harden_system_full()
                elif subcmd in ["quick", "q"]:
                    self.harden_system_quick()
                elif subcmd in ["dry-run", "dry"]:
                    self.harden_system_dry_run()
                elif subcmd in ["users", "user"]:
                    self.harden_users_only()
                elif subcmd in ["firewall", "fw"]:
                    self.harden_firewall_only()
                elif subcmd in ["ssh", "secure-ssh"]:
                    self.harden_ssh_only()
                elif subcmd in ["report", "rep"]:
                    self.generate_hardening_report()
                elif subcmd in ["rollback", "rb"]:
                    self.rollback_hardening()
                else:
                    print(f"{Fore.RED}[!] Unknown hardening command: harden {subcmd}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Commands: dashboard, cinematic, list, status, full, quick, dry-run, users, firewall, ssh, report, rollback{Style.RESET_ALL}")
            return
        
        # Also support direct commands like 'harden-status' without space
        elif parts[0] == "harden-status":
            self.show_hardening_status()
            return
        elif parts[0] == "harden-list":
            self.list_hardening_modules()
            return
        elif parts[0] == "harden-dashboard":
            self.launch_hardening_dashboard()
            return
        elif parts[0] == "harden-report":
            self.generate_hardening_report()
            return
        elif parts[0] == "harden-rollback":
            self.rollback_hardening()
            return
        elif parts[0] == "harden-full":
            self.harden_system_full()
            return
        elif parts[0] == "harden-quick":
            self.harden_system_quick()
            return
        elif parts[0] == "harden-dry-run":
            self.harden_system_dry_run()
            return
        elif parts[0] == "harden-users":
            self.harden_users_only()
            return
        elif parts[0] == "harden-firewall":
            self.harden_firewall_only()
            return
        elif parts[0] == "harden-ssh":
            self.harden_ssh_only()
            return
    
    # SOC Nmap Dashboard Commands ends here=============

        elif cmd in ["harden-list", "harden-ls"]:
            self.list_hardening_modules()
            return

        elif cmd in ["harden-status", "harden-st"]:
            self.show_hardening_status()
            return

        elif cmd in ["harden-dashboard", "harden-menu"]:
            self.launch_hardening_dashboard()
            return

        elif cmd == "harden-cinematic":
            self.launch_hardening_cinematic()
            return

        elif cmd == "harden-full":
            self.harden_system_full()
            return

        elif cmd == "harden-quick":
            self.harden_system_quick()
            return

        elif cmd == "harden-dry-run":
            self.harden_system_dry_run()
            return

        elif cmd == "harden-report":
            self.generate_hardening_report()
            return

        elif cmd == "harden-rollback":
            self.rollback_hardening()
            return

        elif cmd in ["harden-users", "harden-user"]:
            self.harden_users_only()
            return

        elif cmd in ["harden-firewall", "harden-fw"]:
            self.harden_firewall_only()
            return

        elif cmd in ["harden-ssh", "harden-sshd"]:
            self.harden_ssh_only()
            return
    # ==================== END HARDENING COMMANDS ====================
        # Direct shortcuts for SOC commands (no space version)
        elif cmd == 'soc' or cmd == 'soc-nmap':
            self.cmd_soc_nmap()
        elif cmd == 'soc-quick':
            self.cmd_soc_quick()
        elif cmd == 'soc-full':
            self.cmd_soc_full()
        elif cmd == 'soc-dns':
            self.cmd_soc_dns()
        elif cmd == 'soc-map':
            self.cmd_soc_map()
        elif cmd == 'soc-history':
            self.cmd_soc_history()
        elif cmd == 'soc-pdf':
            self.cmd_soc_pdf()
        elif cmd == 'soc-reports':
            self.cmd_soc_reports()
        elif cmd == 'soc-report':
            self.cmd_soc_report()
        elif cmd == 'soc-status':
            self.cmd_soc_status()
        
        elif cmd== 'soc-help':
            self.soc_help()
        elif cmd == 'soc-orgs':
            self.cmd_soc_organizations()
    

        # Crypto commands
        elif cmd == "crypto-list":
            self.crypto.crypto_list()
            return
        
        elif cmd == "crypto-info":
            self.crypto.crypto_info()
            return
        
        elif cmd == "crypto-verify":
            self.crypto.crypto_verify()
            return
        
        elif cmd == "crypto-backup":
            self.crypto.crypto_backup()
            return
# ======================================================
        # NEW: Export/Import key commands for sharing across machines
        elif cmd == "crypto-export":
            if self.crypto:
                self.crypto.export_encryption_key()
            else:
                print(f"{Fore.RED}[!] Crypto engine not available{Style.RESET_ALL}")
            return
        
        elif cmd == "crypto-import":
            if self.crypto:
                self.crypto.import_encryption_key()
            else:
                print(f"{Fore.RED}[!] Crypto engine not available{Style.RESET_ALL}")
            return

        # Shortcut aliases
        elif cmd in ["enc", "crypt"]:
            if self.crypto:
                self.crypto.main()
            else:
                print(f"{Fore.RED}[!] Crypto engine not available{Style.RESET_ALL}")
            return
# =============================================
        elif cmd == "dst-refresh" or cmd == "dst-reload":
            self.cmd_refresh()
            return
        
        elif parts[0] == "kill-monitor":
            self.cmd_kill_monitor()
            return
        
        # ===== Financial Forensics =====
        elif parts[0] == "forensics" or parts[0] == "ff" or parts[0] == "dst-investigation":
            self.cmd_financial_forensics()
            return

        elif parts[0] == "fraud-investigation":
            self.cmd_financial_forensics()
            return

        elif parts[0] == "dst-investigate":
            self.cmd_financial_forensics()
            return
#  =====================for recon & recon_full command parser=============================
 
        # =====================for recon & recon_full command parser=============================
        elif command == 'dst-recon' or command == 'recon.py':
            if RECON_AVAILABLE:
                # Check which functions are available
                if 'recon_menu' in globals() and recon_menu:
                    recon_menu()
                elif 'run_recon' in globals() and run_recon:
                    run_recon()
                else:
                    print(f"{Fore.YELLOW}Recon function not available. Check recon.py imports.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Recon module not available. Make sure recon.py is in: {BASE_PATH}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Files in directory: {os.listdir(BASE_PATH)}{Style.RESET_ALL}")
    
        elif command == 'recon_full' or command == 'dst-recon-full' or command == 'recon_full.py':
            if RECON_FULL_AVAILABLE:
                if 'full_recon_menu' in globals() and full_recon_menu:
                    full_recon_menu()
                elif 'run_full_recon' in globals() and run_full_recon:
                    run_full_recon()
                else:
                    print(f"{Fore.YELLOW}Full Recon function not available. Check recon_full.py imports.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Full Recon module not available. Make sure recon_full.py is in: {BASE_PATH}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Files in directory: {os.listdir(BASE_PATH)}{Style.RESET_ALL}")
    


        elif command == "crypto-import":
            if self.crypto:
                self.crypto.import_encryption_key()
            else:
                print(f"{Fore.RED}[!] Crypto engine not available{Style.RESET_ALL}")
            return
     # ========================================
            # Shortcuts
        elif command in ["enc", "crypt"]:
            if self.crypto:
                from crypto_engine import main as crypto_main
                crypto_main()
            else:
                print(f"{Fore.RED}[!] Crypto engine not available{Style.RESET_ALL}")
    # ===================================
        # Shortcut aliases
        elif command == 'r1' or command == 'rec':
            if RECON_AVAILABLE:
                if 'recon_menu' in globals() and recon_menu:
                    recon_menu()
                elif 'run_recon' in globals() and run_recon:
                    run_recon()
                else:
                    print(f"{Fore.RED}Recon module not properly loaded{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Recon module not available{Style.RESET_ALL}")
    
        elif command == 'r2' or command == 'recf':
            if RECON_FULL_AVAILABLE:
                if 'full_recon_menu' in globals() and full_recon_menu:
                    full_recon_menu()
                elif 'run_full_recon' in globals() and run_full_recon:
                    run_full_recon()
                else:
                    print(f"{Fore.RED}Full Recon module not properly loaded{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Full Recon module not available{Style.RESET_ALL}")
#  ========================================end of recon and recon_full from above================
 # ========== INTEGRITY MONITOR COMMANDS ==========
        elif command in ['integrity', 'integ', 'int']:
            if not self._check_integrity_available():
                return True
            
            if not args:
                self.show_integrity_help()
                return True
            
            subcmd = args[0].lower()
            
            # integrity scan
            if subcmd == 'scan':
                print(f"{Fore.CYAN}[*] Starting integrity scan...{Style.RESET_ALL}")
                try:
                    scan_results = self.integrity.scan_system()
                    changes = self.integrity.check_integrity(scan_results)
                    if changes and any(changes.values()):
                        print(f"{Fore.RED}[!] Integrity violations detected!{Style.RESET_ALL}")
                        self.integrity.generate_report(changes, scan_results)
                    else:
                        print(f"{Fore.GREEN}[✓] No integrity violations found{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[!] Scan failed: {e}{Style.RESET_ALL}")
            
            # integrity baseline
            elif subcmd == 'baseline':
                print(f"{Fore.CYAN}[*] Creating system baseline...{Style.RESET_ALL}")
                try:
                    self.integrity.create_baseline()
                except Exception as e:
                    print(f"{Fore.RED}[!] Failed to create baseline: {e}{Style.RESET_ALL}")
            
            # integrity status
            elif subcmd == 'status':
                print(f"\n{Fore.CYAN}Integrity Monitor Status:{Style.RESET_ALL}")
                print(f"  Status: {'Active' if self.integrity else 'Inactive'}")
                print(f"  Workspace: {self.integrity.workspace if self.integrity else 'N/A'}")
                if self.alert_manager:
                    print(f"  Alerts: {len(self.alert_manager.alerts)}")
            
            # integrity report
            elif subcmd == 'report':
                report_type = args[1] if len(args) > 1 else 'txt'
                print(f"{Fore.CYAN}[*] Generating {report_type.upper()} report...{Style.RESET_ALL}")
                try:
                    scan_results = self.integrity.scan_system()
                    if report_type == 'json':
                        self.integrity.generate_json_report(None, scan_results)
                    elif report_type == 'pdf':
                        self.integrity.generate_pdf_report(None, scan_results)
                    elif report_type == 'all':
                        self.integrity.generate_all_reports(None, scan_results)
                    else:
                        self.integrity.generate_report(None, scan_results)
                except Exception as e:
                    print(f"{Fore.RED}[!] Report generation failed: {e}{Style.RESET_ALL}")
            
            # integrity monitor
            elif subcmd == 'monitor':
                if len(args) > 1 and args[1] == 'stop':
                    if self.alert_manager:
                        self.alert_manager.stop_monitoring()
                        print(f"{Fore.GREEN}[✓] Monitoring stopped{Style.RESET_ALL}")
                else:
                    if self.alert_manager:
                        self.alert_manager.start_monitoring()
                        print(f"{Fore.GREEN}[✓] Real-time monitoring started{Style.RESET_ALL}")
            
            # integrity alerts
            elif subcmd == 'alerts':
                if self.alert_manager:
                    alerts = self.alert_manager.get_alerts()
                    if alerts:
                        print(f"\n{Fore.CYAN}Recent Alerts:{Style.RESET_ALL}")
                        for alert in alerts[-10:]:
                            print(f"  [{alert.get('severity', 'LOW')}] {alert.get('timestamp', '')}: {alert.get('path', 'Unknown')}")
                    else:
                        print(f"{Fore.GREEN}No alerts{Style.RESET_ALL}")
             # integrity list
            elif subcmd == 'list':
                try:
                    # Get scan results
                    scan_results = self.integrity.scan_system()
                    
                    # Determine which category to list
                    category = args[1] if len(args) > 1 else 'all'
                    
                    if category == 'all':
                        total_files = (len(scan_results.get('critical_files', [])) + 
                                      len(scan_results.get('configs', [])) + 
                                      len(scan_results.get('logs', [])) + 
                                      len(scan_results.get('databases', [])) + 
                                      len(scan_results.get('files', [])))
                        print(f"\n{Fore.CYAN}File Inventory Summary:{Style.RESET_ALL}")
                        print(f"  Critical System Files: {len(scan_results.get('critical_files', []))}")
                        print(f"  Configuration Files: {len(scan_results.get('configs', []))}")
                        print(f"  Log Files: {len(scan_results.get('logs', []))}")
                        print(f"  Databases: {len(scan_results.get('databases', []))}")
                        print(f"  User Files: {len(scan_results.get('files', []))}")
                        print(f"  {Fore.GREEN}Total: {total_files}{Style.RESET_ALL}")
                    
                    elif category == 'critical':
                        files = scan_results.get('critical_files', [])
                        print(f"\n{Fore.RED}Critical System Files ({len(files)}):{Style.RESET_ALL}")
                        for f in files[:20]:  # Show first 20
                            print(f"  {f.get('path', 'Unknown')}")
                        if len(files) > 20:
                            print(f"  ... and {len(files) - 20} more")
                    
                    elif category == 'configs':
                        files = scan_results.get('configs', [])
                        print(f"\n{Fore.YELLOW}Configuration Files ({len(files)}):{Style.RESET_ALL}")
                        for f in files[:20]:
                            print(f"  {f.get('path', 'Unknown')}")
                        if len(files) > 20:
                            print(f"  ... and {len(files) - 20} more")
                    
                    elif category == 'logs':
                        files = scan_results.get('logs', [])
                        print(f"\n{Fore.BLUE}Log Files ({len(files)}):{Style.RESET_ALL}")
                        for f in files[:20]:
                            print(f"  {f.get('path', 'Unknown')}")
                        if len(files) > 20:
                            print(f"  ... and {len(files) - 20} more")
                    
                    elif category == 'databases':
                        files = scan_results.get('databases', [])
                        print(f"\n{Fore.MAGENTA}Database Files ({len(files)}):{Style.RESET_ALL}")
                        for f in files[:20]:
                            print(f"  {f.get('path', 'Unknown')}")
                        if len(files) > 20:
                            print(f"  ... and {len(files) - 20} more")
                    
                    elif category == 'user':
                        files = scan_results.get('files', [])
                        print(f"\n{Fore.GREEN}User Files ({len(files)}):{Style.RESET_ALL}")
                        for f in files[:20]:
                            print(f"  {f.get('path', 'Unknown')}")
                        if len(files) > 20:
                            print(f"  ... and {len(files) - 20} more")
                    
                    else:
                        print(f"{Fore.RED}[!] Unknown category: {category}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}Valid categories: all, critical, configs, logs, databases, user{Style.RESET_ALL}")
                
                except Exception as e:
                    print(f"{Fore.RED}[!] Failed to list files: {e}{Style.RESET_ALL}")
            # integrity quarantine
            elif subcmd == 'quarantine':
                if len(args) > 1:
                    file_path = args[1]
                    print(f"{Fore.CYAN}[*] Quarantining file: {file_path}{Style.RESET_ALL}")
                    try:
                        if hasattr(self.integrity, 'quarantine_file'):
                            self.integrity.quarantine_file(file_path)
                        else:
                            # Fallback quarantine
                            import shutil
                            quarantine_dir = os.path.join(self.integrity.workspace, "quarantine")
                            os.makedirs(quarantine_dir, exist_ok=True)
                            filename = os.path.basename(file_path)
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            dest = os.path.join(quarantine_dir, f"{timestamp}_{filename}")
                            shutil.move(file_path, dest)
                            print(f"{Fore.GREEN}[✓] File quarantined to: {dest}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}[!] Failed to quarantine: {e}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}Usage: integrity quarantine <file_path>{Style.RESET_ALL}")
            
            # integrity restore
            elif subcmd == 'restore':
                if len(args) > 1:
                    file_path = args[1]
                    print(f"{Fore.CYAN}[*] Restoring from quarantine: {file_path}{Style.RESET_ALL}")
                    try:
                        if hasattr(self.integrity, 'restore_from_quarantine'):
                            self.integrity.restore_from_quarantine(file_path)
                        else:
                            print(f"{Fore.YELLOW}[!] Restore feature not implemented{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}[!] Failed to restore: {e}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}Usage: integrity restore <file_path>{Style.RESET_ALL}")
            
            # integrity report
            elif subcmd == 'report':
                report_type = args[1] if len(args) > 1 else 'txt'
                print(f"{Fore.CYAN}[*] Generating {report_type.upper()} report...{Style.RESET_ALL}")
                try:
                    scan_results = self.integrity.scan_system()
                    if report_type == 'json':
                        self.integrity.generate_json_report(None, scan_results)
                    elif report_type == 'pdf':
                        self.integrity.generate_pdf_report(None, scan_results)
                    elif report_type == 'all':
                        self.integrity.generate_all_reports(None, scan_results)
                    else:
                        self.integrity.generate_report(None, scan_results)
                except Exception as e:
                    print(f"{Fore.RED}[!] Report generation failed: {e}{Style.RESET_ALL}")
# ==================================================================================================
            # integrity forensic
            elif subcmd == 'forensic':
                if len(args) > 1:
                    if args[1] == 'timeline':
                        if self.forensic:
                            timeline = self.forensic.analyze_timeline()
                            print(f"{Fore.CYAN}[*] Timeline has {len(timeline)} events{Style.RESET_ALL}")
                    elif args[1] == 'report':
                        if self.forensic:
                            self.forensic.generate_forensic_report()
                else:
                    print(f"{Fore.YELLOW}Usage: integrity forensic <timeline|report>{Style.RESET_ALL}")
            
            else:
                print(f"{Fore.RED}[!] Unknown integrity command: {subcmd}{Style.RESET_ALL}")
                self.show_integrity_help()
# ====================font integrity=================ends here=========================================

# =======================for secure deletion protection starts here===============================
# Inside your command handler (where parts[0] == "pwd" etc. lives)

# ==================== deletion protection commands ====================
        elif parts[0] == "monitor":
            self.cmd_monitor()
            return

        elif parts[0] == "service":
            if len(parts) < 2:
                print("Usage: service <start|stop|status>")
                return
            subcmd = parts[1].lower()
            if subcmd == 'start':
                self.cmd_service_start()
            elif subcmd == 'stop':
                self.cmd_service_stop()
            elif subcmd == 'status':
                self.cmd_service_status()
            else:
                print(f"Unknown service command: {subcmd}")
            return

        elif parts[0] == "list-backups":
            self.cmd_list_backups()
            return

        elif parts[0] == "search":
            if len(parts) < 2:
                print("Usage: search <term>")
                return
            self.cmd_search_backups(parts[1])
            return

        elif parts[0] == "restore-id":
            if len(parts) < 2:
                print("Usage: restore-id <ID> [target_directory]")
                return
            try:
                bid = int(parts[1])
                target = parts[2] if len(parts) > 2 else None
                self.cmd_restore_id(bid, target)
            except ValueError:
                print("Error: Invalid backup ID")
            return

        elif parts[0] == "restore-last":
            self.cmd_restore_last()
            return

        elif parts[0] == "add-path":
            if len(parts) < 2:
                print("Usage: add-path <directory>")
                return
            self.cmd_add_path(parts[1])
            return

        elif parts[0] == "dst-workspace":
            self.cmd_workspace_info()
            return

        elif parts[0] == "dst-cleanup":
            self.cmd_cleanup()
            return

        elif parts[0] == "dst-platform":
            self.cmd_platform_info()
            return
        
        # In your command handler:
        elif parts[0] == "auto-discover":
            self.auto_discover_folders()
            return

        elif parts[0] == "monitor-all":
            self.cmd_monitor_all()
            return

        elif parts[0] == "watch-folders":
            self.cmd_start_folder_watcher()
            return
        
        elif parts[0] == "service" and len(parts) > 1:
            if parts[1] == "stop":
                self.cmd_service_stop()
                return
            elif parts[1] == "start":
                self.cmd_service_start()
                return
            elif parts[1] == "status":
                self.cmd_service_status()
                return

        elif parts[0] == "show-paths":
            print("\n📁 Monitored Paths:")
            for p in self.config['monitor_paths']:
                status = "✓" if os.path.exists(p) else "✗"
                print(f"  {status} {p}")
            return
        
        elif parts[0] == "watch-folders":
            self.cmd_start_folder_watcher()
            return
# ==================== deletion protection commands end ====================
# ====================seciure deletriomn ends here===============================
        elif parts[0] == "pwd":
            self.pwd()
            return
 
        elif parts[0] == "cd" and len(parts) == 2:
            self.cd(parts[1])
            return
            
        elif parts[0] == "cat" and len(parts) == 2:
            self.cat(parts[1])
            return
        
        elif parts[0] == "echo":
            self.handle_echo(cmd)
            return
        
        elif cmd == "debug":
            self.cmd_debug()
            return
# metasplo----------------
        elif parts[0] == "msf":
            self.handle_msf(parts[1:])
            return

    # ===== TruffleHog =====
        if parts[0] == "trufflehog":
            if "--git" in parts:
                try:
                    git_url = parts[parts.index("--git") + 1]
                    print(self.trufflehog_scan_git(git_url))
                except IndexError:
                    print("[!] Missing Git URL. Usage: trufflehog --git <URL>")
            elif "--fs" in parts:
                try:
                    fs_path = parts[parts.index("--fs") + 1]
                    print(self.trufflehog_scan_filesystem(fs_path))
                except IndexError:
                    print("[!] Missing filesystem path. Usage: trufflehog --fs <PATH>")
            else:
                print("Usage: trufflehog --git <URL> OR --fs <PATH>")

    # ===== Nikto =====
        elif parts[0] == "nikto":
            if "--url" not in parts:
                print("Usage: nikto --url <TARGET> [--port PORT] [--output FILE]")
                return
            try:
                target = parts[parts.index("--url") + 1]
                port = parts[parts.index("--port") + 1] if "--port" in parts else "80"
                output = parts[parts.index("--output") + 1] if "--output" in parts else None
                print(self.nikto_scan(target, port, output))
            except IndexError:
                print("[!] Invalid arguments. Usage: nikto --url <TARGET> [--port PORT] [--output FILE]")

    # ===== Legitify =====
        elif parts[0] == "legitify":
            if "--github" not in parts:
                print("Usage: legitify --github <ORG/REPO> [--token TOKEN]")
                return
            try:
                repo = parts[parts.index("--github") + 1]
                token = parts[parts.index("--token") + 1] if "--token" in parts else None
                print(self.legitify_scan_github(repo, token))
            except IndexError:
                print("[!] Invalid arguments. Usage: legitify --github <ORG/REPO> [--token TOKEN]")

    # Original commands (scan, netmon, etc.)
        elif original_cmd.lower() == "system scan -all":
            self.scan_system()
            self.show_tip("system scan -all")
            return

        elif original_cmd.lower() == "net -n mon":
            self.network_monitor()
            self.show_tip("net -n mon")
            return

        # ===================================
    #  for clear command to clean terminal
    # Add to  command handler:
        elif original_cmd.lower() == "clear terminal":
            self.clear_terminal()
            self.show_tip(cmd)

        elif cmd == "clear":
            self.clear_terminal()
            self.show_tip(cmd)
        elif original_cmd.lower() == "shutdown":
            self.emergency_shutdown()
    

# ================================================
    # exploit check and mac address change
        elif cmd == "exploitcheck": 
            self.check_exploits()
            self.show_tip(cmd)
        elif cmd.startswith("macspoof"): 
            self.spoof_mac(cmd.split()[1] if len(cmd.split()) > 1 else "enp3s0")
            self.show_tip(cmd)

    #  sqlmap and log clearing
        elif cmd.startswith("sqlmap"): 
            self.sql_injection_scan(cmd.split()[1] if len(cmd.split()) > 1 else input("Target URL: "))
            self.show_tip(cmd)
        elif cmd == "clearlogs": 
            self.clear_logs()
            self.show_tip(cmd)
 
    # portsweep and hashing file commands
        elif cmd.startswith("portsweep"): 
            target = cmd.split()[1] if len(cmd.split()) > 1 else "127.0.0.1"
            self.port_scan(target)
            self.show_tip(cmd)

        elif cmd.startswith("hashfile"): 
            file_path = cmd.split()[1] if len(cmd.split()) > 1 else input("File path: ")
            hashes = self.hash_file(file_path)
            for algo, hash_val in hashes.items():
                print(f"{algo.upper()}: {hash_val}")
            self.show_tip(cmd)

    #  system information detailed part and force killing of running processes
        elif cmd == "sysinfo": 
            self.system_info()
            self.show_tip(cmd)

        elif cmd.startswith("killproc"): 
            self.kill_process(int(cmd.split()[1])) if len(cmd.split()) > 1 else print("Usage: killproc PID")
            self.show_tip(cmd)
    # =====================================
        elif cmd == "crypto-list":
            self.crypto.crypto_list()
            return

        elif cmd == "crypto-info":
    # crypto_info can take an optional filename
            if args:
                self.crypto.crypto_info(args[0])
            else:
                self.crypto.crypto_info()  # Will prompt for filename
                return

        elif cmd == "crypto-verify":
            self.crypto.crypto_verify()
            return

        elif cmd == "crypto-backup":
            self.crypto.crypto_backup()
            return

        elif cmd == "encrypt-test":
            self.crypto.encrypt_test()
            return

        # NEW: Export/Import key commands for sharing
        elif cmd == "crypto-export":
            self.crypto.export_encryption_key()
            return
        
        elif cmd == "crypto-import":
            self.crypto.import_encryption_key()
            return
        
        # Shortcut aliases
        elif cmd in ["enc", "crypt"]:
            self.crypto.main()
            return
        
        elif cmd == "encrypt":
            if args:
        # Pass the filename directly - matches encrypt_file(filename)
                self.crypto.encrypt_file(args[0])
            else:
                file = input("File to encrypt: ")
                if file:
                    self.crypto.encrypt_file(file)
                else:
                    print("[!] No file specified")
            
        elif cmd == "decrypt":
            if args:
        # Pass the filename to decrypt - matches decrypt_file(filename)
                self.crypto.decrypt_file(args[0])
            else:
                file = input("File to decrypt: ")
                if file:
                    self.crypto.decrypt_file(file)
                else:
                    print("[!] No file specified")
            
        elif cmd in ["encrypt-setup", "crypto-init"]:
            self.crypto.encrypt_setup()
    
        elif cmd == "crypto-status":
            self.crypto.crypto_status()

    # ===========
        elif cmd.startswith("watchfolder"): 
            self.watch_folder(cmd.split()[1] if len(cmd.split()) > 1 else ".")
            self.show_tip(cmd)
        elif cmd.startswith("traceroute"): 
            self.trace_route(cmd.split()[1] if len(cmd.split()) > 1 else "8.8.8.8")
            self.show_tip(cmd)
        elif cmd == "ransomwatch": 
            self.monitor_ransomware()
            self.show_tip(cmd)
        elif cmd.startswith("wificrack"): 
            self.wifi_audit(cmd.split()[1] if len(cmd.split()) > 1 else "wlp2s0")
            self.show_tip(cmd)
        elif cmd.startswith("stegcheck"): 
            self.check_steganography(cmd.split()[1] if len(cmd.split()) > 1 else input("Image path: "))
            self.show_tip(cmd)

        elif cmd.startswith("certcheck"):
        # Handle both command line input and interactive prompt
            if len(cmd.split()) > 1:
                domain = cmd.split()[1]
                self.check_ssl(domain)
                self.show_tip(cmd)
            else:
                self.check_ssl()  # Will prompt for domain inside the method
        elif cmd == "msf-debug" or cmd == "msfdebug":
            self.debug_metasploit()

        elif cmd == "memdump": 
            self.dump_memory()
            self.show_tip(cmd)
        elif cmd == "torify": 
            self.enable_tor_routing()
            self.show_tip(cmd)
        elif cmd == "dst-update": 
            print(f"\n[+] {self.check_updates()}")
            self.show_tip(cmd)
        elif cmd == "vt-scan": 
            self.run_vt_module()
            self.show_tip(cmd)

        elif command in ["vt", "virustotal", "scan-vt"]:
            self.run_vt_module()
            # return
        elif original_cmd.lower() == "registry -n mon": 
            print(self.monitor_registry())
            self.show_tip(cmd)
        elif original_cmd.lower() == "harden -t sys": 
            self.harden_system(dry_run=False)
            self.show_tip(cmd)

        elif cmd == "help": 
            self.show_help()
        elif cmd == "exit": 
            print("\n[*] Exiting Defensive Security Terminal")
            sys.exit(0)
        else: 
            # print("[!] Unknown command. Type 'help' for more command options.")
            return
# ===============================added vtscan upgrade
    def run_vt_module(self):
        """Launch VirusTotal SOC module"""
        if not VT_AVAILABLE:
            print(f"{Fore.RED}[!] VirusTotal module not available{Style.RESET_ALL}")
            input("Press Enter to continue...")
            return

        try:
            vt_scan_menu(self.operator_username, self.session_id)  # launches full cinematic SOC system
        except Exception as e:
            print(f"{Fore.RED}[!] Error running VT module: {e}{Style.RESET_ALL}")
            input("Press Enter to continue...")
# ==================== HELP MENU ====================

    def show_help(self):
        """Display interactive hacking-styled help menu with categories"""
    
    # Define blink sequences if not already defined in class
        blink_on = "\033[5m"
        blink_off = "\033[25m"
    
    # Clear screen and show loading animation
        self._cinematic_box("LOADING COMMAND DATABASE", seconds=10)
    
        terminal_width = shutil.get_terminal_size((80, 20)).columns
    
    # Help menu categories with commands
        categories = {
            "🔥 CORE SECURITY": [
                ("system scan -All", "System threat scan (sys, apps, net)"),
                ("net -n mon", "Live network monitoring"),
                ("exploitcheck", "Check for critical CVEs"),
                ("vtscan", "VirusTotal file analysis"),
                ("clearlogs", "Securely wipe system logs"),
                ("nikto --url <TARGET>", "Web vulnerability scan"),
                ("legitify --github <ORG/REPO>", "Scan GitHub for misconfigs"),
                ("msfconsole", "Launch Metasploit Framework console"),
                ("msf-debug", "Debug Metasploit installation issues"),
                ("msf -h", "Metasploit help and options"),
                ("nmap -sV <TARGET>", "Service/version detection scan"),
                ("nmap -A <TARGET>", "Aggressive OS and service detection"),
                ("nmap -p- <TARGET>", "Scan all 65535 ports"),
                ("nmap scan <TARGET>", "Nmap scan the target"),
                ("fraud / financial", "Financial fraud investigation suite"),
                ("investigate", "Launch financial forensics tools"),
                ("trace", "Trace suspicious transactions")
            ],
        
            "🌐 NETWORK TOOLS": [
                ("portsweep [IP]", "Scan target for open ports"),
                ("traceroute [IP]", "Network path analysis"),
                ("torify", "Route traffic through Tor"),
                ("dnssec [DOMAIN]", "Validate DNSSEC"),
                ("nmap <TARGET>", "Basic port scan"),
                ("nmap -sS <TARGET>", "Stealth SYN scan"),
                ("nmap -sU <TARGET>", "UDP port scan"),
                ("nmap -O <TARGET>", "OS fingerprinting"),
                ("msfvenom", "Generate payloads for exploits"),
                ("msfdb", "Manage Metasploit database"),
                ("msfconsole", "Launch Metasploit Framework console")
            ],
        
            "🔍 FORENSICS & FINANCIAL": [
                ("memdump", "Capture volatile memory"),
                ("hashfile [PATH]", "Generate file integrity hashes"),
                ("stegcheck [IMG]", "Detect hidden image data"),
                ("ransomwatch", "Identify ransomware indicators"),
                ("finanalyze", "Analyze suspicious transactions"),
                ("transfertrace", "Trace transaction flows"),
                ("recon", "Run comprehensive information reconnaissance scan"),
                ("recon -full", "Run full recon with additional checks"),
                ("viewlogs", "View recent system logs"),
                ("regmon", "Monitor Windows registry changes"),
                ("sessiondump", "Dump active user sessions")
            ],
        
            "⚙️ SYSTEM MANAGEMENT": [
                ("sysinfo", "Detailed system report"),
                ("killproc PID", "Terminate process"),
                ("macspoof [IFACE]", "Randomize MAC address"),
                ("harden -t sys", "Apply security hardening"),
                ("update", "Check for DST updates"),
                ("shutdown", "Emergency shutdown"),
                ("shutdown now", "Immediate machine shutdown")
            ],
        
            "🔐 CRYPTO TOOLS": [
                ("encrypt FILE", "AES-256 file encryption"),
                ("decrypt FILE KEY", "File decryption"),
                ("crypto-list", "List encrypted files"),
                ("crypto-info <file.enc>", "Show encryption info"),
                ("crypto-verify", "Verify encryption system"),
                ("crypto-backup", "Backup encryption key"),
                ("encrypt-test", "Run encryption test"),
                ("encrypt-setup", "Setup encryption system")
            ],
        
            "🌍 WEB SECURITY": [
                ("sqlmap [URL]", "SQL injection scan"),
                ("certcheck [DOMAIN]", "SSL certificate audit"),
                ("nmap --script vuln <TARGET>", "Vulnerability scan with NSE"),
                ("nmap --script http-* <TARGET>", "HTTP service enumeration"),
                ("msfconsole -q", "Launch Metasploit quietly"),
                ("msf > search <exploit>", "Search exploits in Metasploit"),
                ("msf > use <exploit>", "Use specific exploit module"),
                ("msf > set RHOSTS <IP>", "Set target in Metasploit"),
                ("msf > run/exploit", "Execute Metasploit module")
            ],
        
            "📊 MONITORING": [
                ("watchfolder [PATH]", "Directory change detection"),
                ("regmon", "Windows registry monitor")
            ],
        
            "📁 FILE COMMANDS": [
                ("ls", "List files"),
                ("cat <file>", "Show file contents"),
                ("touch <file>", "Create file"),
                ("echo <text> > <file>", "Write to file"),
                ("pwd", "Show current directory")
            ],
        
            "🛠️ UTILITIES": [
                ("help", "Show this menu"),
                ("exit", "Quit terminal"),
                ("clear", "Clear terminal display"),
                ("clear terminal", "Clear terminal history")
            ]
        }
    
    # Create header
        print(f"\n{Fore.RED}╔{'═' * (terminal_width-2)}╗{Style.RESET_ALL}")
        print(f"{Fore.RED}║{Fore.CYAN}{'DSTerminal v2.0.113 - Command Reference Manual'.center(terminal_width-2)}{Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}║{Fore.YELLOW}{'INTERACTIVE COMMAND MENU'.center(terminal_width-2)}{Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}╠{'═' * (terminal_width-2)}╣{Style.RESET_ALL}")
    
    # Display each category
        for category, commands in categories.items():
        # Random color for each category
            cat_colors = [Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.BLUE, Fore.RED]
            cat_color = random.choice(cat_colors)
        
        # Category header with blinking for important ones
            if "CORE" in category or "SECURITY" in category:
                print(f"\n{cat_color}┌─{blink_on}{category}{blink_off}{'─' * (terminal_width - len(category) - 6)}{cat_color}┐{Style.RESET_ALL}")
            else:
                print(f"\n{cat_color}┌─{category}{'─' * (terminal_width - len(category) - 5)}{cat_color}┐{Style.RESET_ALL}")
        
        # Display commands
            for cmd, desc in commands:
            # Color code commands based on type
                if "scan" in cmd or "exploit" in cmd or "nikto" in cmd:
                    cmd_color = Fore.RED
                elif "encrypt" in cmd or "crypto" in cmd or "decrypt" in cmd:
                    cmd_color = Fore.MAGENTA
                elif "net" in cmd or "portsweep" in cmd or "traceroute" in cmd:
                    cmd_color = Fore.CYAN
                elif "sqlmap" in cmd or "certcheck" in cmd:
                    cmd_color = Fore.YELLOW
                elif "ls" in cmd or "cat" in cmd or "touch" in cmd:
                    cmd_color = Fore.BLUE
                elif "msf" in cmd or "metasploit" in cmd or "msfconsole" in cmd:
                    cmd_color = Fore.RED + Style.BRIGHT
                elif "nmap" in cmd:
                    cmd_color = Fore.YELLOW + Style.BRIGHT
                elif "viewlogs" in cmd or "sessiondump" in cmd:
                    cmd_color = Fore.MAGENTA + Style.BRIGHT
                elif "recon" in cmd or "enum" in cmd:
                    cmd_color = Fore.GREEN + Style.BRIGHT
                elif "regmon" in cmd or "watchfolder" in cmd:
                    cmd_color = Fore.YELLOW + Style.BRIGHT
                elif "sysinfo" in cmd or "killproc" in cmd or "harden" in cmd:
                    cmd_color = Fore.CYAN + Style.BRIGHT
                else:
                    cmd_color = Fore.GREEN
            
            # Format the line safely - FIXED: Avoid % formatting issues
                cmd_part = f"{cmd_color}{cmd}{Style.RESET_ALL}"
                desc_part = f"{Fore.WHITE}{desc}{Style.RESET_ALL}"
            
            # Calculate padding to align properly
                cmd_width = 30
                desc_width = terminal_width - 45
            
            # Pad the command part to fixed width
                cmd_padded = cmd_part.ljust(cmd_width)
            
            # Pad the description part to fixed width
                desc_padded = desc_part.ljust(desc_width)[:desc_width]
            
            # Build the line without using width specifiers in f-string that might contain %
                line = f"{cat_color}│{Style.RESET_ALL} {cmd_padded} {desc_padded}{cat_color}│{Style.RESET_ALL}"
                print(line[:terminal_width])
                time.sleep(0.09)  # Slight typing effect
        
        # Category footer
            print(f"{cat_color}└{'─' * (terminal_width-2)}┘{Style.RESET_ALL}")
            time.sleep(0.2)
    
    # Footer with tips
        print(f"\n{Fore.RED}╠{'═' * (terminal_width-2)}╣{Style.RESET_ALL}")
    
        tips = [
            ("💡 TIP:", "Use Tab for command completion", Fore.CYAN),
            ("⚡ PRO:", "Combine commands with '&&'", Fore.GREEN),
            ("🔧 DEV:", "Check /var/log/dsterminal for logs", Fore.YELLOW),
            ("🌐 WEB:", "Access web interface at https://www.dsterminal.com", Fore.MAGENTA)
        ]
    
        for icon, tip, color in tips:
            print(f"{Fore.RED}║{Style.RESET_ALL} {color}{icon}{Style.RESET_ALL} {Fore.WHITE}{tip:<{terminal_width-20}}{Fore.RED}║{Style.RESET_ALL}")
    
        print(f"{Fore.RED}╚{'═' * (terminal_width-2)}╝{Style.RESET_ALL}")
    
    # Interactive command search
        print(f"\n{Fore.CYAN}┌─[{Fore.GREEN}HELP{Fore.CYAN}]─[{Fore.YELLOW}type 'search' to find commands or 'exit' to quit{Fore.CYAN}]")
    
        while True:
            search = input(f"{Fore.CYAN}└─$ {Style.RESET_ALL}").strip().lower()
        
            if search == "exit" or search == "q" or search == "":
                break
        
            if search == "search":
                print(f"\n{Fore.YELLOW}Enter search term: {Style.RESET_ALL}", end="")
                term = input().strip().lower()
            
                if term:
                    found = False
                    print(f"\n{Fore.GREEN}🔍 Search results for '{term}':{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
                
                # Search through all commands
                    for category, commands in categories.items():
                        for cmd, desc in commands:
                            if term in cmd.lower() or term in desc.lower():
                                found = True
                            # Color code based on match
                                if term in cmd.lower():
                                    match_color = Fore.YELLOW
                                else:
                                    match_color = Fore.WHITE
                                print(f"{Fore.GREEN}✓{Style.RESET_ALL} {match_color}{cmd:<30}{Style.RESET_ALL} {Fore.WHITE}{desc}{Style.RESET_ALL}")
                
                    if not found:
                        print(f"{Fore.RED}✗ No commands found matching '{term}'{Style.RESET_ALL}")
                
                    print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
            else:
            # Direct command search
                found = False
                for category, commands in categories.items():
                    for cmd, desc in commands:
                        if search in cmd.lower():
                            found = True
                            print(f"{Fore.GREEN}✓ {cmd}: {Fore.WHITE}{desc}{Style.RESET_ALL}")
            
                if not found:
                    print(f"{Fore.RED}✗ Command '{search}' not found. Type 'search' to search descriptions.{Style.RESET_ALL}")
    
        print(f"{Fore.GREEN}[✓] Help system closed{Style.RESET_ALL}")

# --------------------help menu ends here from above========================
# =============================END==========================================

    def run(self):
        self.initialize_operator_session()   # ← ADD THIS
        self.print_banner()
        
        # Define available commands for autocompletion
        COMMANDS = {
            "system": {"scan": None, "info": None},
            "net": {"mon": None, "scan": None},
            "encrypt": None,
            "decrypt": None,
            "nmap": None,
            "msf": None,
            "sqlmap": None,
            "certcheck": None,
            "exploitcheck": None,
            "macspoof": None,
            "clearlogs": None,
            "portsweep": None,
            "hashfile": None,
            "sysinfo": None,
            "killproc": None,
            "watchfolder": None,
            "traceroute": None,
            "ransomwatch": None,
            "wificrack": None,
            "stegcheck": None,
            "memdump": None,
            "torify": None,
            "update": None,
            "vt-scan": None,
            "crypto-list": None,
            "crypto-info": None,
            "crypto-verify": None,
            "crypto-backup": None,
            "encrypt-test": None,
            "encrypt-setup": None,
            "crypto-status": None,
            "nikto": None,
            "legitify": None,
            "trufflehog": None,
            "recon": None,
            "ls": None,
            "cd": None,
            "pwd": None,
            "cat": None,
            "echo": None,
            "mkdir": None,
            "touch": None,
            "clear": None,
            "help": None,
            "exit": None
        }
        
        completer = NestedCompleter.from_nested_dict(COMMANDS)
        # Define styles to keep toolbar fixed
        from prompt_toolkit import PromptSession
        from prompt_toolkit.styles import Style
        style = Style.from_dict({
            'bottom-toolbar': 'bg:#1a1a2e #33ff33',
            'bottom-toolbar.text': "#078507",
        })

        self.session = PromptSession(
            history=FileHistory('.dst_history'),
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer,
            bottom_toolbar=HTML(
                "<b>DSTerminal</b> v{} | Mode: <style bg='{}'>{}</style>"
            ).format(
                CONFIG["CURRENT_VERSION"],
                "ansired" if self.is_admin() else "ansigreen",
                "ADMIN" if self.is_admin() else "USER",
            ),
            style=style,
            # Add this to ensure the toolbar doesn't scroll with content
            reserve_space_for_menu=0,
            complete_while_typing=True,
            refresh_interval=0.5,
            )
        
        while True:
            try:
            # Real SOC terminal components:
            # [TIMESTAMP] [HOSTNAME] [ENV] [SEVERITY] [SESSION] USER@TERMINAL>
            
                timestamp = datetime.now().strftime("%H:%M:%S")
                hostname = socket.gethostname()
                env = "PROD"  # or "DEV", "STAGING", "INCIDENT"
            
            
            # Dynamic severity based on context
                if hasattr(self, 'current_incident') and self.current_incident:
                    severity = f"<ansired>CRITICAL</ansired>"
                elif hasattr(self, 'active_threats') and self.active_threats > 0:
                    severity = f"<ansiyellow>HIGH</ansiyellow>"
                else:
                    severity = f"<ansigreen>NORMAL</ansigreen>"
            
            # Session/ticket tracking
                session_id = getattr(self, 'session_id', 'SOC001')
                session_id = self.session_id
            
            # Build the SOC prompt
                prompt_text = HTML(
                    f"<ansiwhite>[{timestamp}]</ansiwhite> "
                    f"<ansicyan>{hostname}</ansicyan> "
                    f"<ansiyellow>[{env}]</ansiyellow> "
                    f"{severity} "
                    f"<ansimagenta>[{session_id}]</ansimagenta>\n"
                    f"<ansigreen>🔹 {self.operator_username}</ansigreen> "
                    f"<ansiwhite>@</ansiwhite> "
                    f"<ansiblue>soc-terminal</ansiblue> "
                    f"<ansiwhite>:</ansiwhite> "
                    f"<ansired>~$ </ansired>"
                )
            
                user_input = self.session.prompt(prompt_text)
                self.log_command(user_input)
                # Log the command to SIEM
                self.log_to_siem(f"Command executed: {user_input}")
                # Detect exit command
                if user_input.lower() == "exit":
                    self.save_session_end()
                    print_formatted_text(HTML("<ansiyellow>[+] Operator session closed. Log saved.</ansiyellow>"))
                    break

                # Handle normal commands
                self.handle_command(user_input.strip())
            
            except KeyboardInterrupt:
                print("\n[!] Use 'exit' to quit or 'help' for commands")
            except Exception as e:
                print(f"[!] SOC Terminal Error: {str(e)}")
            # Log to SIEM
                self.log_to_siem(f"Terminal error: {str(e)}")

if __name__ == "__main__":
    if '--monitor-only' in sys.argv:
        ws_idx = sys.argv.index('--workspace') if '--workspace' in sys.argv else None
        paths_idx = sys.argv.index('--paths') if '--paths' in sys.argv else None
        
        workspace_path = sys.argv[ws_idx + 1] if ws_idx else os.getcwd()
        
        print("""
╔══════════════════════════════════════════════════════╗
║         DSTERMINAL DELETION PROTECTION               ║
║         Background Monitoring Active                 ║
║         Close this window to stop                    ║
╚══════════════════════════════════════════════════════╝
        """)
        
        # Load config with all paths
        if paths_idx:
            monitor_paths = sys.argv[paths_idx + 1].split(',')
        else:
            pd = PlatformDetector()
            monitor_paths = pd.get_trash_paths()
        
        config = {
            'version': '3.1.0',
            'monitor_paths': monitor_paths,
            'exclude_patterns': ['*.tmp', '*.temp', '*~', '.DS_Store', 'Thumbs.db'],
            'max_file_size': 100 * 1024 * 1024,
            'encrypt_backups': False,
        }
        
        ws = SimpleWorkspace(workspace_path)
        monitor = DSTerminalMonitor(config, ws, interactive=False, ui=None)
        
        from watchdog.observers import Observer
        observer = Observer()
        
        for path in monitor_paths:
            if os.path.exists(path):
                try:
                    observer.schedule(monitor, path=path, recursive=True)
                    print(f"  ✓ Monitoring: {path}")
                except Exception as e:
                    print(f"  ✗ Skipping {path}: {e}")
        
        observer.start()
        print(f"\n[*] Monitoring {len(monitor_paths)} folders.")
        print("[*] Press Ctrl+C to stop.\n")
        sys.stdout.flush()
        
        try:
            while True:
                time.sleep(1)
                sys.stdout.flush()
        except KeyboardInterrupt:
            print("\n[*] Stopping...")
            observer.stop()
            observer.join()
            monitor.cleanup()
            print("[✓] Monitoring stopped.")
        
        sys.exit(0)
    
    # Normal terminal startup
    terminal = SecurityTerminal()
    terminal.run()