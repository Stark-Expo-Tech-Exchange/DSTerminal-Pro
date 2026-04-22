#!/usr/bin/env python3
"""
DSTERMINAL v3.1 - Enterprise Data Deletion Protection System
Complete implementation with cinematic progress tracking and workspace structure
"""

from email.mime import text
from fileinput import filename
from pydoc import text
import os
import time
import shutil
import hashlib
import json
import sys
import threading
import sqlite3
import zipfile
import tempfile  # ADDED: Missing import
import signal
import atexit
import fnmatch
import socket
import getpass
import platform
import logging
import re
from datetime import datetime
from collections import defaultdict
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

# Try importing optional dependencies
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: psutil not installed. Some features will be limited.")

try:
    from cryptography.fernet import Fernet
    import secrets
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("Warning: cryptography not installed. Encryption features disabled.")

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("Error: watchdog is required. Install with: pip install watchdog")
    sys.exit(1)

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("Warning: reportlab not installed. PDF generation disabled.")

# =========================
# 🎨 Terminal UI System
# =========================
# =========================
# 🌍 Cross-Platform Detection
# =========================

class PlatformDetector:
    """Cross-platform detection and path management"""
    
    def __init__(self):
        self.system = platform.system()
        self.is_windows = self.system == 'Windows'
        self.is_linux = self.system == 'Linux'
        self.is_macos = self.system == 'Darwin'
        
    def get_trash_paths(self) -> List[str]:
        """Get trash/recycle bin paths for current platform"""
        home = os.path.expanduser('~')
    
        if self.is_linux:
            return [
                os.path.join(home, '.local/share/Trash/files'),
                os.path.join(home, '.local/share/Trash/info'),
                os.path.join(home, '.Trash'),
                '/tmp'
            ]
        elif self.is_macos:
            return [
                os.path.join(home, '.Trash'),
                '/tmp',
                os.path.join(home, 'Desktop'),
                os.path.join(home, 'Downloads')
            ]
        elif self.is_windows:
        # Windows paths - EXCLUDE Recycle Bin (requires admin)
            paths = [
                os.path.join(home, 'Desktop'),
                os.path.join(home, 'Downloads'),
                os.path.join(home, 'Documents'),
                os.environ.get('TEMP', 'C:\\Windows\\Temp'),
                os.environ.get('TMP', 'C:\\Windows\\Temp')
            ]
        # Add OneDrive paths if they exist
            onedrive = os.path.join(home, 'OneDrive')
            if os.path.exists(onedrive):
                paths.extend([
                    os.path.join(onedrive, 'Desktop'),
                    os.path.join(onedrive, 'Downloads'),
                    os.path.join(onedrive, 'Documents')
                ])
        
        # Filter to only existing paths
            return [p for p in paths if os.path.exists(p)]
        else:
            return ['/tmp']
    
    def get_desktop_path(self) -> str:
        """Get desktop path for current platform"""
        home = os.path.expanduser('~')
        
        if self.is_windows:
            onedrive_desktop = os.path.join(home, 'OneDrive', 'Desktop')
            if os.path.exists(onedrive_desktop):
                return onedrive_desktop
            return os.path.join(home, 'Desktop')
        else:
            return os.path.join(home, 'Desktop')
    
    def get_downloads_path(self) -> str:
        """Get downloads path for current platform"""
        home = os.path.expanduser('~')
        return os.path.join(home, 'Downloads')
    
    def normalize_path(self, path: str) -> str:
        """Normalize path for current platform"""
        return os.path.normpath(path)
    
    def is_trash_path(self, path: str) -> bool:
        """Check if path is a trash/recycle bin location"""
        path_normalized = self.normalize_path(path).lower()
        
        trash_indicators = []
        
        if self.is_linux or self.is_macos:
            trash_indicators = [
                '.local/share/trash',
                '.trash',
                '/tmp'
            ]
        elif self.is_windows:
            trash_indicators = [
                '$recycle.bin',
                '\\temp',
                '\\windows\\temp'
            ]
        
        for indicator in trash_indicators:
            if indicator in path_normalized:
                return True
        
        return False
    
    def get_system_info(self) -> Dict[str, str]:
        """Get system information"""
        info = {
            'system': self.system,
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'hostname': socket.gethostname(),
            'user': getpass.getuser()
        }
        
        if self.is_linux:
            try:
                import distro
                info['distro'] = f"{distro.name()} {distro.version()}"
            except:
                info['distro'] = 'Linux'
        elif self.is_macos:
            info['distro'] = f"macOS {platform.mac_ver()[0]}"
        elif self.is_windows:
            info['distro'] = f"Windows {platform.win32_ver()[0]}"
        
        return info

        # ===============================
class TerminalColors:
    """ANSI color codes for terminal styling"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


class CinematicProgress:
    """Cinematic progress tracking with animations"""
    
    def __init__(self, ui):
        self.ui = ui
        self.current_operation = None
        self.progress = 0
        self.lock = threading.Lock()
        self.supports_ansi = self._check_ansi_support()
        
    def _check_ansi_support(self) -> bool:
        """Check if terminal supports ANSI escape codes"""
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        
    def start_operation(self, operation_name: str, total_steps: int = 100):
        """Start a new operation with progress tracking"""
        with self.lock:
            self.current_operation = {
                'name': operation_name,
                'total': total_steps,
                'current': 0,
                'start_time': time.time(),
                'status': 'running'
            }
            self.progress = 0
            self._display_progress_header()
            
    def update_progress(self, step: int = 1, message: str = None):
        """Update progress with cinematic animation"""
        with self.lock:
            if self.current_operation:
                self.current_operation['current'] += step
                self.progress = (self.current_operation['current'] / self.current_operation['total']) * 100
                self._display_progress_bar(message)
            
    def complete_operation(self, success: bool = True, message: str = None):
        """Mark operation as complete"""
        with self.lock:
            if self.current_operation:
                duration = time.time() - self.current_operation['start_time']
                self.current_operation['status'] = 'success' if success else 'failed'
                self._display_completion(duration, success, message)
                self.current_operation = None
            
    def _display_progress_header(self):
        """Display progress header"""
        print(f"\n{self.ui.colors.CYAN}{'=' * 61}{self.ui.colors.RESET}")
        print(f"{self.ui.colors.BOLD}OPERATION: {self.current_operation['name']}{self.ui.colors.RESET}")
        print(f"{self.ui.colors.CYAN}{'-' * 61}{self.ui.colors.RESET}")
        
    def _display_progress_bar(self, message: str = None):
        """Display progress bar (ANSI or simple fallback)"""
        width = 50
        
        if self.supports_ansi:
            filled = int(width * self.progress / 100)
            bar = '█' * filled + '░' * (width - filled)
            
            if self.progress < 30:
                color = self.ui.colors.YELLOW
            elif self.progress < 70:
                color = self.ui.colors.CYAN
            else:
                color = self.ui.colors.GREEN
                
            sys.stdout.write('\033[2K\033[1A\033[2K')
            status_line = f"{color}[{bar}]{self.ui.colors.RESET} {self.progress:.1f}%"
            print(status_line)
        else:
            # Simple fallback for non-ANSI terminals
            filled = int(width * self.progress / 100)
            bar = '=' * filled + '-' * (width - filled)
            print(f"\r[{bar}] {self.progress:.1f}%", end='', flush=True)
        
        if message:
            print(f"{self.ui.colors.DIM}  -> {message}{self.ui.colors.RESET}")
            
    def _display_completion(self, duration: float, success: bool, message: str = None):
        """Display completion message"""
        if self.supports_ansi:
            sys.stdout.write('\033[2K\033[1A\033[2K')
        
        if success:
            icon = "[OK]"
            color = self.ui.colors.GREEN
            status = "COMPLETED"
        else:
            icon = "[FAIL]"
            color = self.ui.colors.RED
            status = "FAILED"
            
        print(f"{icon} {color}{status}{self.ui.colors.RESET} in {duration:.2f}s")
        
        if message:
            print(f"  {message}")
            
        print(f"{self.ui.colors.CYAN}{'=' * 61}{self.ui.colors.RESET}\n")


class TerminalUI:
    """Advanced terminal UI with animations and effects"""
    
    def __init__(self):
        self.term_width = shutil.get_terminal_size().columns
        self.colors = TerminalColors()
        self.progress = CinematicProgress(self)
    def strip_ansi(self, text: str) -> str:
        """Remove ANSI color codes from text"""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def create_box(self, content: str, title: str = "", style: str = "rounded", 
                   color: str = None, width: int = None) -> str:
        """Create styled box with content"""
        
        lines = content.split('\n')
        if width is None:
            max_len = max(len(self.strip_ansi(line)) for line in lines)
            width = min(max_len + 4, self.term_width - 4)
        
        # Box characters
        if style == "double":
            tl, tr, bl, br, h, v = '╔', '╗', '╚', '╝', '═', '║'
        elif style == "rounded":
            tl, tr, bl, br, h, v = '╭', '╮', '╰', '╯', '─', '│'
        else:
            tl, tr, bl, br, h, v = '+', '+', '+', '+', '-', '|'
        
        # Apply color
        color_code = getattr(self.colors, color.upper(), '') if color else ''
        reset = self.colors.RESET if color else ''
        
        # Build box
        result = []
        result.append(f"{color_code}{tl}{h * (width - 2)}{tr}{reset}")
        
        if title:
            title_text = f" {title} "
            title_len = len(self.strip_ansi(title_text))
            padding = width - 2 - title_len
            left_pad = padding // 2
            right_pad = padding - left_pad
            
            title_line = (f"{color_code}{v}{reset}"
                         f"{' ' * left_pad}{self.colors.BOLD}{title_text}{reset}{' ' * right_pad}"
                         f"{color_code}{v}{reset}")
            result.append(title_line)
            result.append(f"{color_code}{v}{h * (width - 2)}{v}{reset}")
        
        for line in lines:
            visible_len = len(self.strip_ansi(line))
            padding = width - 2 - visible_len
            padded_line = (f"{color_code}{v}{reset} {line}"
                          f"{' ' * padding} {color_code}{v}{reset}")
            result.append(padded_line)
        
        result.append(f"{color_code}{bl}{h * (width - 2)}{br}{reset}")
        
        return '\n'.join(result)
    
    def strip_ansi(self, text: str) -> str:
        """Remove ANSI color codes from text"""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
    
    def cinematic_print(self, text: str, delay: float = 0.02, color: str = None):
        """Print text with typewriter effect"""
        color_code = getattr(self.colors, color.upper(), '') if color else ''
        reset = self.colors.RESET if color else ''
        
        for char in text:
            print(f"{color_code}{char}{reset}", end='', flush=True)
            time.sleep(delay)
        print()
    
    def center_text(self, text: str) -> str:
        """Center text in terminal"""
        visible_len = len(self.strip_ansi(text))
        padding = max(0, (self.term_width - visible_len) // 2)
        return ' ' * padding + text
    
    def display_notification(self, title: str, message: str, level: str = "info"):
        """Display notification box"""
        level_colors = {
            'info': 'CYAN',
            'success': 'GREEN',
            'warning': 'YELLOW',
            'error': 'RED',
            'critical': 'BRIGHT_RED'
        }
        
        color = level_colors.get(level, 'WHITE')
        
        notification = self.create_box(
            message,
            title=f" {level.upper()} ",
            style='rounded',
            color=color
        )
        
        print(f"\n{notification}\n")


# =========================
# 📁 Workspace Manager
# =========================

class WorkspaceManager:
    """Manages the DSTerminal workspace directory structure"""
    
    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = os.path.join(os.getcwd(), 'dsterminal_workspace')
        
        self.base_path = base_path
        self.paths = self._create_workspace_structure()
        self._create_readme()
        
    def _create_workspace_structure(self) -> Dict[str, str]:
        """Create the complete workspace directory structure"""
        
        directories = {
            'root': self.base_path,
            'backups': os.path.join(self.base_path, 'backups'),
            'database': os.path.join(self.base_path, 'database'),
            'logs': os.path.join(self.base_path, 'logs'),
            'reports': os.path.join(self.base_path, 'reports'),
            'config': os.path.join(self.base_path, 'config'),
            'temp': os.path.join(self.base_path, 'temp'),
            'quarantine': os.path.join(self.base_path, 'quarantine'),
            
            # Backup subdirectories
            'backups_images': os.path.join(self.base_path, 'backups', 'images'),
            'backups_documents': os.path.join(self.base_path, 'backups', 'documents'),
            'backups_spreadsheets': os.path.join(self.base_path, 'backups', 'spreadsheets'),
            'backups_code': os.path.join(self.base_path, 'backups', 'code'),
            'backups_config': os.path.join(self.base_path, 'backups', 'config'),
            'backups_archives': os.path.join(self.base_path, 'backups', 'archives'),
            'backups_media': os.path.join(self.base_path, 'backups', 'media'),
            'backups_other': os.path.join(self.base_path, 'backups', 'other'),
            'backups_protected': os.path.join(self.base_path, 'backups', 'protected'),
            'backups_encrypted': os.path.join(self.base_path, 'backups', 'encrypted'),
        }
        
        # Create all directories
        for name, path in directories.items():
            os.makedirs(path, exist_ok=True)
        
        return directories
    
    def _create_readme(self):
        """Create README file"""
        readme_path = os.path.join(self.base_path, 'README.txt')
        
        content = f"""
======================================================================
                    DSTERMINAL WORKSPACE DIRECTORY                 
======================================================================

This directory contains all data and configurations for DSTerminal.

DIRECTORY STRUCTURE:
----------------------------------------------------------------------

[backups]              - All backed up files organized by category
   +-- images/         - JPG, PNG, GIF files
   +-- documents/      - PDF, DOC, TXT files
   +-- spreadsheets/   - XLS, CSV files
   +-- code/           - Source code files
   +-- config/         - Configuration files
   +-- archives/       - ZIP, TAR, RAR files
   +-- media/          - Video and audio files
   +-- other/          - Uncategorized files
   +-- protected/      - Protected files (hard links)
   +-- encrypted/      - Encrypted backups

[database]             - SQLite database files
   +-- dsterminal.db   - Main database

[logs]                 - System logs
[reports]              - Generated PDF reports
[config]               - Configuration files
[temp]                 - Temporary files
[quarantine]           - Quarantined suspicious files

----------------------------------------------------------------------

!!! WARNING: Do not manually modify files in this directory !!!

Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
DSTerminal Version: 3.1.0
        """
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def get_path(self, key: str) -> str:
        """Get path by key"""
        return self.paths.get(key, self.base_path)
    
    def get_database_path(self) -> str:
        """Get database file path"""
        return os.path.join(self.paths['database'], 'dsterminal.db')
    
    def get_config_path(self) -> str:
        """Get config file path"""
        return os.path.join(self.paths['config'], 'config.json')
    
    def get_key_path(self) -> str:
        """Get encryption key path"""
        return os.path.join(self.paths['config'], 'encryption.key')
    
    def get_backup_path(self, category: str = 'other') -> str:
        """Get backup path for category"""
        category_key = f'backups_{category}'
        return self.paths.get(category_key, self.paths['backups_other'])
    
    def get_log_path(self) -> str:
        """Get log file path"""
        timestamp = datetime.now().strftime("%Y%m%d")
        return os.path.join(self.paths['logs'], f'dsterminal_{timestamp}.log')
    
    def get_report_path(self) -> str:
        """Get report file path"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.paths['reports'], f'report_{timestamp}.pdf')
    
    def get_workspace_info(self) -> Dict[str, Any]:
        """Get workspace information"""
        info = {
            'base_path': self.base_path,
            'total_size_mb': 0
        }
        
        total = 0
        for path in self.paths.values():
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for f in files:
                        fp = os.path.join(root, f)
                        if os.path.exists(fp):
                            total += os.path.getsize(fp)
        
        info['total_size_mb'] = total / (1024 * 1024)
        return info
    
    def cleanup_temp_files(self, max_age_hours: int = 24):
        """Clean up temporary files"""
        temp_dir = self.paths['temp']
        cutoff = time.time() - (max_age_hours * 3600)
        
        if not os.path.exists(temp_dir):
            return
            
        for filename in os.listdir(temp_dir):
            filepath = os.path.join(temp_dir, filename)
            if os.path.isfile(filepath):
                if os.path.getmtime(filepath) < cutoff:
                    try:
                        os.remove(filepath)
                    except:
                        pass


# =========================
# 🔐 Encryption System
# =========================

class EncryptionManager:
    """Manages file encryption and decryption"""
    
    def __init__(self, workspace: WorkspaceManager):
        self.workspace = workspace
        self.key_file = workspace.get_key_path()
        self.cipher = None
        if CRYPTO_AVAILABLE:
            self._load_or_create_key()
        
    def _load_or_create_key(self):
        """Load existing key or create new one"""
        if not CRYPTO_AVAILABLE:
            return
            
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        
        self.cipher = Fernet(key)
    
    def encrypt_file(self, filepath: str) -> str:
        """Encrypt file and return path to encrypted file"""
        if not CRYPTO_AVAILABLE or not self.cipher:
            return filepath
            
        with open(filepath, 'rb') as f:
            data = f.read()
        
        encrypted_data = self.cipher.encrypt(data)
        encrypted_path = filepath + '.encrypted'
        
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        
        return encrypted_path
    
    def decrypt_file(self, encrypted_path: str) -> str:
        """Decrypt file and return path to decrypted file"""
        if not CRYPTO_AVAILABLE or not self.cipher:
            return encrypted_path
            
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = self.cipher.decrypt(encrypted_data)
        decrypted_path = encrypted_path.replace('.encrypted', '')
        
        with open(decrypted_path, 'wb') as f:
            f.write(decrypted_data)
        
        return decrypted_path


# =========================
# 💾 Database System
# =========================

class BackupDatabase:
    """SQLite database for tracking all operations"""
    
    def __init__(self, workspace: WorkspaceManager):
        self.workspace = workspace
        self.db_path = workspace.get_database_path()
        self.conn = None
        self._init_database()
        
    def _init_database(self):
        """Initialize database schema"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        
        # Backups table - FIXED: Added last_restored column
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_path TEXT NOT NULL,
                backup_path TEXT NOT NULL,
                filename TEXT NOT NULL,
                file_hash TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                category TEXT NOT NULL,
                encryption_status TEXT DEFAULT 'none',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                restore_count INTEGER DEFAULT 0,
                last_restored TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        # Operations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_type TEXT NOT NULL,
                status TEXT NOT NULL,
                files_processed INTEGER DEFAULT 0,
                bytes_processed INTEGER DEFAULT 0,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                duration_seconds REAL,
                metadata TEXT
            )
        ''')
        
        # Deletion events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deletion_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                file_hash TEXT,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                backed_up BOOLEAN DEFAULT FALSE,
                backup_id INTEGER,
                FOREIGN KEY (backup_id) REFERENCES backups (id)
            )
        ''')
        
        # Check if last_restored column exists, add if missing (for existing DBs)
        cursor.execute("PRAGMA table_info(backups)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'last_restored' not in columns:
            cursor.execute('ALTER TABLE backups ADD COLUMN last_restored TIMESTAMP')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_backups_hash ON backups(file_hash)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_backups_created ON backups(created_at)')
        
        self.conn.commit()
    
    def add_backup(self, backup_data: Dict[str, Any]) -> int:
        """Add backup record"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO backups 
            (original_path, backup_path, filename, file_hash, file_size, category, encryption_status, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            backup_data['original_path'],
            backup_data['backup_path'],
            backup_data['filename'],
            backup_data['file_hash'],
            backup_data['file_size'],
            backup_data['category'],
            backup_data.get('encryption_status', 'none'),
            json.dumps(backup_data.get('metadata', {}))
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def add_deletion_event(self, file_path: str, file_hash: str, backup_id: int = None):
        """Record deletion event"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO deletion_events 
            (file_path, file_hash, backed_up, backup_id)
            VALUES (?, ?, ?, ?)
        ''', (file_path, file_hash, backup_id is not None, backup_id))
        self.conn.commit()
    
    def start_operation(self, operation_type: str, metadata: Dict[str, Any] = None) -> int:
        """Start tracking an operation"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO operations (operation_type, status, metadata)
            VALUES (?, 'running', ?)
        ''', (operation_type, json.dumps(metadata or {})))
        self.conn.commit()
        return cursor.lastrowid
    
    def complete_operation(self, operation_id: int, status: str, 
                          files_processed: int = 0, bytes_processed: int = 0):
        """Mark operation as complete"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE operations 
            SET status = ?, 
                files_processed = ?,
                bytes_processed = ?,
                completed_at = CURRENT_TIMESTAMP,
                duration_seconds = CAST((julianday(CURRENT_TIMESTAMP) - julianday(started_at)) * 86400 AS REAL)
            WHERE id = ?
        ''', (status, files_processed, bytes_processed, operation_id))
        self.conn.commit()
    
    def find_backup_by_hash(self, file_hash: str) -> Optional[Dict[str, Any]]:
        """Find backup by file hash"""
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT * FROM backups WHERE file_hash = ?',
            (file_hash,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def version_exists(self, file_hash: str) -> bool:
        """Check if file version already backed up"""
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT id FROM backups WHERE file_hash = ?',
            (file_hash,)
        )
        return cursor.fetchone() is not None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_backups,
                COALESCE(SUM(file_size), 0) as total_size
            FROM backups
        ''')
        row = cursor.fetchone()
        
        cursor.execute('''
            SELECT COUNT(*) as today_deletions
            FROM deletion_events 
            WHERE date(detected_at) = date('now')
        ''')
        del_row = cursor.fetchone()
        
        return {
            'total_backups': row['total_backups'] or 0,
            'total_size': row['total_size'] or 0,
            'deletions_today': del_row['today_deletions'] or 0
        }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


# =========================
# 📊 Advanced Monitor Handler
# =========================

class DSTerminalMonitor(FileSystemEventHandler):
    """Advanced file system monitor with proper backup-before-delete"""
    
    def __init__(self, config: Dict[str, Any], workspace: WorkspaceManager):
        self.config = config
        self.workspace = workspace
        self.ui = TerminalUI()
        self.db = BackupDatabase(workspace)
        self.encryption = EncryptionManager(workspace)
        self.platform_detector = PlatformDetector()

        self.stats = defaultdict(int)
        self.deletion_events = []
        self.honeypots = []
        self.protected_paths = set()
        
        # Setup logging
        self._setup_logging()
        
        # Create honeypots
        for path in config['monitor_paths']:
            if os.path.exists(path):
                try:
                    honeypots = self._create_honeypots(path)
                    self.honeypots.extend(honeypots)
                except Exception as e:
                    self.logger.debug(f"Skipping honeypots in {path}: {e}")
        
        # Register cleanup
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def _setup_logging(self):
        """Setup logging"""
        self.logger = logging.getLogger('DSTerminal')
        self.logger.setLevel(logging.INFO)
        
        fh = RotatingFileHandler(
            self.workspace.get_log_path(),
            maxBytes=10*1024*1024,
            backupCount=5
        )
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
    
    def _create_honeypots(self, directory: str) -> List[str]:
        """Create decoy files - skip system protected directories"""
        honeypot_files = []
    
    # Skip system protected directories
        protected_paths = [
            'C:\\$Recycle.Bin',
            'C:\\Windows',
            'C:\\Program Files',
            'C:\\Program Files (x86)',
            '/System',
            '/sys',
            '/proc',
            '/dev'
        ]
    
    # Check if directory is protected
        directory_lower = directory.lower()
        for protected in protected_paths:
            if directory_lower.startswith(protected.lower()):
                self.logger.info(f"Skipping honeypot creation in protected path: {directory}")
                return []
    
    # Skip if directory is not writable
        if not os.access(directory, os.W_OK):
            self.logger.info(f"Skipping honeypot creation in non-writable path: {directory}")
            return []
    
        bait_names = ['passwords.txt', 'credentials.json', 'backup.sql']
    
        honeypot_dir = os.path.join(directory, '.honeypot')
    
        try:
            os.makedirs(honeypot_dir, exist_ok=True)
        
            for name in bait_names:
                filepath = os.path.join(honeypot_dir, name)
                if not os.path.exists(filepath):
                    try:
                        with open(filepath, 'w') as f:
                            f.write(f"# HONEYPOT - {datetime.now()}\n")
                        honeypot_files.append(filepath)
                    except (PermissionError, OSError) as e:
                        self.logger.debug(f"Could not create honeypot {filepath}: {e}")
                        continue
        except (PermissionError, OSError) as e:
            self.logger.debug(f"Could not create honeypot directory in {directory}: {e}")
    
        return honeypot_files

    def on_created(self, event):
        """Handle file creation - proactively backup files"""
        if event.is_directory:
            return
        
        filepath = event.src_path
        
        # Only process files in monitored paths
        if not self._should_process_file(filepath):
            return
        
        # Create backup immediately when file appears in trash
        self._create_backup_with_progress(filepath, 'file_created')

    def on_deleted(self, event):
        """Handle file deletion - check if we have backup"""
        if event.is_directory:
            return
    
        filepath = event.src_path
        filename = os.path.basename(filepath)
    
    # Skip workspace and temp files
        workspace_path = os.path.normpath(self.workspace.base_path)
        if os.path.normpath(filepath).startswith(workspace_path):
            return
    
        if filename.endswith(('.tmp', '.temp', '.db-journal')):
            return
    
    # Search database for matching file (by filename and recent timestamp)
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT * FROM backups 
            WHERE filename = ? 
            ORDER BY created_at DESC 
            LIMIT 1
        ''', (filename,))
    
        backup = cursor.fetchone()
    
        if backup:
            backup_dict = dict(backup)
            self.ui.display_notification(
                "DELETION DETECTED",
                f"✓ {filename}\nBackup exists - can restore!",
                "warning"
            )
            self.db.add_deletion_event(filepath, backup_dict['file_hash'], backup_dict['id'])
            self.logger.info(f"Deletion detected, backup exists: {filename}")
        else:
            self.ui.display_notification(
                "DELETION DETECTED",
                f"⚠ {filename}\nNo backup available",
                "error"
            )
            self.db.add_deletion_event(filepath, "HASH_FAILED")
            self.logger.warning(f"File deleted without backup: {filename}")

    def on_modified(self, event):
        """Handle file modification"""
        if event.is_directory:
            return
        
        filepath = event.src_path
        
        if self._should_process_file(filepath):
            self._create_backup_with_progress(filepath, 'file_modified')
    
    def on_moved(self, event):
        """Handle file move - backup if moving to trash"""
        if event.is_directory:
            return
        
        if hasattr(event, 'dest_path') and self._is_trash_path(event.dest_path):
            self._create_backup_with_progress(event.src_path, 'moved_to_trash')
    
    def _create_backup_with_progress(self, filepath: str, trigger: str):
        """Create backup with cinematic progress tracking"""
        
        if not os.path.exists(filepath):
            return
        
        filename = os.path.basename(filepath)
        
        # Start progress tracking
        display_name = filename[:40] + '...' if len(filename) > 40 else filename
        self.ui.progress.start_operation(f"Backing up: {display_name}", 100)
        
        try:
            # Step 1: Analyze file
            self.ui.progress.update_progress(10, "Analyzing file...")
            file_size = os.path.getsize(filepath)
            
            # Step 2: Calculate hash
            self.ui.progress.update_progress(20, "Calculating hash...")
            file_hash = self._calculate_hash(filepath)
            
            # Check if already backed up
            if self.db.version_exists(file_hash):
                self.ui.progress.complete_operation(True, "Already backed up")
                return
            
            # Step 3: Categorize
            self.ui.progress.update_progress(30, "Categorizing file...")
            category = self._categorize_file(filename)
            
            # Step 4: Prepare backup location
            self.ui.progress.update_progress(40, "Preparing backup location...")
            backup_dir = os.path.join(
                self.workspace.get_backup_path(category),
                datetime.now().strftime("%Y/%m/%d")
            )
            os.makedirs(backup_dir, exist_ok=True)
            
            # Step 5: Copy file
            self.ui.progress.update_progress(50, f"Copying {filename[:30]}...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            backup_filename = f"{timestamp}_{filename}"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            shutil.copy2(filepath, backup_path)
            self.ui.progress.update_progress(80, "Verifying copy...")
            
            # Step 6: Verify
            backup_hash = self._calculate_hash(backup_path)
            if backup_hash != file_hash:
                raise Exception("Hash verification failed")
            
            # Step 7: Protect file
            self.ui.progress.update_progress(90, "Applying protection...")
            self._protect_file(backup_path)
            
            # Step 8: Save to database
            encryption_status = 'none'
            if self.config.get('encrypt_backups', False):
                encrypted_path = self.encryption.encrypt_file(backup_path)
                if encrypted_path != backup_path:
                    os.remove(backup_path)
                    backup_path = encrypted_path
                    encryption_status = 'fernet'
            
            backup_data = {
                'original_path': filepath,
                'backup_path': backup_path,
                'filename': filename,
                'file_hash': file_hash,
                'file_size': file_size,
                'category': category,
                'encryption_status': encryption_status,
                'metadata': {'trigger': trigger}
            }
            
            self.db.add_backup(backup_data)
            
            # Complete
            size_mb = file_size / (1024 * 1024)
            self.ui.progress.complete_operation(
                True,
                f"✓ {filename[:40]} ({size_mb:.2f} MB)"
            )
            
            self.stats['total_backups'] += 1
            self.stats['total_size'] += file_size
            
            self.logger.info(f"Backup created: {filename} ({size_mb:.2f} MB)")
            
        except Exception as e:
            self.ui.progress.complete_operation(False, f"Failed: {str(e)}")
            self.logger.error(f"Backup failed for {filename}: {e}")
    
    def _protect_file(self, filepath: str) -> bool:
        """Apply additional protection to file"""
        try:
            # Set read-only
            os.chmod(filepath, 0o444)
            
            # Create hard link as additional protection
            protected_path = os.path.join(
                self.workspace.get_path('backups_protected'),
                os.path.basename(filepath) + '.protected'
            )
            
            if not os.path.exists(protected_path):
                try:
                    os.link(filepath, protected_path)
                except:
                    shutil.copy2(filepath, protected_path)
            
            self.protected_paths.add(filepath)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to protect file {filepath}: {e}")
            return False
    
    def _calculate_hash(self, filepath: str) -> str:
        """Calculate SHA-256 hash of file"""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def _quick_hash(self, filepath: str) -> str:
        """Quick hash for deletion detection - matches backup identification"""
        if not os.path.exists(filepath):
            return "FILE_NOT_FOUND"
    
        try:
        # Read first 8KB and last 8KB for quick identification
        # This matches the pattern used in many deduplication systems
            size = os.path.getsize(filepath)
        
            with open(filepath, 'rb') as f:
            # Read first chunk
                start = f.read(8192)
            
            # Read last chunk if file is large enough
                if size > 8192:
                    f.seek(-8192, os.SEEK_END)
                    end = f.read(8192)
                else:
                    end = b''
        
        # Create hash from partial content + size
            hasher = hashlib.sha256()
            hasher.update(start)
            hasher.update(end)
            hasher.update(str(size).encode())
        
            return hasher.hexdigest()
        
        except (IOError, OSError, PermissionError):
        # If we can't read the file, use metadata instead
            try:
                stat = os.stat(filepath)
                hasher = hashlib.sha256()
                hasher.update(str(stat.st_size).encode())
                hasher.update(str(stat.st_mtime).encode())
                hasher.update(os.path.basename(filepath).encode())
                return hasher.hexdigest()
            except:
                return "HASH_FAILED"
         
    def _categorize_file(self, filename: str) -> str:
        """Categorize file by extension"""
        ext = os.path.splitext(filename)[1].lower()
        
        if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp']:
            return 'images'
        elif ext in ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt']:
            return 'documents'
        elif ext in ['.xls', '.xlsx', '.csv', '.ods']:
            return 'spreadsheets'
        elif ext in ['.py', '.js', '.java', '.cpp', '.c', '.h', '.go', '.rs', '.ts']:
            return 'code'
        elif ext in ['.json', '.yaml', '.yml', '.ini', '.conf', '.env', '.toml']:
            return 'config'
        elif ext in ['.zip', '.tar', '.gz', '.rar', '.7z', '.bz2']:
            return 'archives'
        elif ext in ['.mp4', '.mp3', '.avi', '.mov', '.wav', '.flac', '.m4a']:
            return 'media'
        else:
            return 'other'
    
    def _should_process_file(self, filepath: str) -> bool:
        """Determine if file should be processed"""
    
    # CRITICAL: Skip workspace directory entirely
        workspace_path = os.path.normpath(self.workspace.base_path)
        filepath_norm = os.path.normpath(filepath)
    
        if filepath_norm.startswith(workspace_path):
            return False
    
    # Skip database files and SQLite temporary files
        filename = os.path.basename(filepath)
        skip_patterns = ['*.db', '*.db-journal', '*.db-wal', '*.db-shm', '*.sqlite', '*.sqlite3']
        for pattern in skip_patterns:
            if fnmatch.fnmatch(filename, pattern):
                return False
    
    # Skip system files
        system_patterns = ['*.tmp', '*.temp', '*~', '.DS_Store', 'Thumbs.db', 'desktop.ini', '*.crdownload']
        for pattern in system_patterns:
            if fnmatch.fnmatch(filename, pattern):
                return False
    
    # Skip if in excluded patterns
        for pattern in self.config.get('exclude_patterns', []):
            if fnmatch.fnmatch(filepath, pattern):
                return False
    
    # Check file size
        max_size = self.config.get('max_file_size', 100 * 1024 * 1024)
        try:
            if os.path.getsize(filepath) > max_size:
                return False
        except (OSError, IOError):
            return False
    
        return True

    def _is_trash_path(self, path: str) -> bool:
        """Check if path is a trash/recycle bin location"""
        return self.platform_detector.is_trash_path(path) 
    def on_created(self, event):
        """Handle file creation - proactively backup files"""
        if event.is_directory:
            return
        
        filepath = event.src_path
        
        # Only process files in monitored paths
        if not self._should_process_file(filepath):
            return
        
        # Create backup for files in monitored locations
        # For Windows, also backup files in Desktop/Downloads
        if self._is_monitored_path(filepath):
            self._create_backup_with_progress(filepath, 'file_created')
    def _is_monitored_path(self, path: str) -> bool:
        """Check if path is in monitored directories"""
        path_normalized = self.platform_detector.normalize_path(path)
        
        for monitor_path in self.config['monitor_paths']:
            monitor_normalized = self.platform_detector.normalize_path(monitor_path)
            if path_normalized.startswith(monitor_normalized):
                return True
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get monitoring statistics"""
        db_stats = self.db.get_statistics()
        
        return {
            'total_backups': db_stats['total_backups'],
            'total_size': db_stats['total_size'],
            'session_backups': self.stats['total_backups'],
            'session_size': self.stats['total_size'],
            'deletions_today': db_stats['deletions_today'],
            'protected_files': len(self.protected_paths)
        }
    
    def cleanup(self):
        """Cleanup resources"""
        self.logger.info("Shutting down DSTerminal...")
        
        for honeypot in self.honeypots:
            try:
                if os.path.exists(honeypot):
                    os.remove(honeypot)
            except:
                pass
        
        self.workspace.cleanup_temp_files()
        self.db.close()
        
        self.logger.info("DSTerminal shutdown complete")
    
    def signal_handler(self, signum, frame):
        """Handle termination signals"""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.cleanup()
        sys.exit(0)


# =========================
# ⚙️ Configuration Manager
# =========================
class ConfigManager:
    """Manages system configuration"""
    
    def __init__(self, workspace: WorkspaceManager):
        self.workspace = workspace
        self.config_path = workspace.get_config_path()
        self.platform_detector = PlatformDetector()
        self.config = self.load_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get platform-specific default configuration"""
        return {
            'version': '3.1.0',
            'monitor_paths': self.platform_detector.get_trash_paths(),
            'exclude_patterns': [
                '*.tmp', '*.temp', '*~', '.DS_Store',
                'Thumbs.db', '*.swp', '*.lock', '*.pid',
                'desktop.ini', '*.crdownload'
            ],
            'max_file_size': 100 * 1024 * 1024,
            'compress_threshold': 10 * 1024 * 1024,
            'encrypt_backups': False,
            'verbose': True,
            'ui_animations': True
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load or create configuration"""
        default_config = self._get_default_config()
        
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                saved_config = json.load(f)
                
                # Check if saved config is for a different platform or old version
                saved_version = saved_config.get('version', '0.0.0')
                saved_paths = saved_config.get('monitor_paths', [])
                
                # Force update monitor_paths for current platform
                # This ensures Windows gets Windows paths, Linux gets Linux paths
                saved_config['monitor_paths'] = default_config['monitor_paths']
                saved_config['version'] = default_config['version']
                
                # Save the updated config
                self.save_config(saved_config)
                
                return saved_config
        else:
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config: Dict[str, Any] = None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self.config.copy()
# =========================
# 📊 PDF Report Generator
# =========================

class ReportGenerator:
    """Generates PDF reports"""
    
    def __init__(self, workspace: WorkspaceManager):
        self.workspace = workspace
        
    def generate_report(self, stats: Dict[str, Any]) -> Optional[str]:
        """Generate PDF report"""
        if not REPORTLAB_AVAILABLE:
            return None
            
        report_path = self.workspace.get_report_path()
        
        doc = SimpleDocTemplate(report_path, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a5276'),
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        elements.append(Paragraph("DSTERMINAL SESSION REPORT", title_style))
        elements.append(Spacer(1, 20))
        
        # Statistics table
        data = [
            ["Metric", "Value"],
            ["Total Backups", str(stats.get('total_backups', 0))],
            ["Total Data Protected", f"{stats.get('total_size', 0) / (1024**3):.2f} GB"],
            ["Session Backups", str(stats.get('session_backups', 0))],
            ["Session Data", f"{stats.get('session_size', 0) / (1024**2):.2f} MB"],
            ["Deletions Detected", str(stats.get('deletions_today', 0))],
            ["Protected Files", str(stats.get('protected_files', 0))],
            ["Report Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        ]
        
        table = Table(data, colWidths=[2.5*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        
        return report_path


# =========================
# ♻️ RESTORE MODULE
# =========================

class RestoreManager:
    """Manages file restoration from backups"""
    
    def __init__(self, workspace: WorkspaceManager):
        self.workspace = workspace
        self.db = BackupDatabase(workspace)
        self.encryption = EncryptionManager(workspace)
        self.ui = TerminalUI()
        
    def list_backups(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List all available backups"""
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT id, original_path, backup_path, filename, file_size, category, 
                   created_at, restore_count, last_restored, encryption_status
            FROM backups 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def search_backups(self, query: str) -> List[Dict[str, Any]]:
        """Search backups by filename or original path"""
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT id, original_path, backup_path, filename, file_size, category, 
                   created_at, restore_count, last_restored, encryption_status
            FROM backups 
            WHERE filename LIKE ? OR original_path LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{query}%', f'%{query}%'))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_backup_by_id(self, backup_id: int) -> Optional[Dict[str, Any]]:
        """Get backup details by ID"""
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM backups WHERE id = ?', (backup_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def restore_file(self, backup_id: int, target_path: str = None, 
                     overwrite: bool = False) -> bool:
        """Restore a file from backup"""
        
        backup = self.get_backup_by_id(backup_id)
        if not backup:
            self.ui.display_notification(
                "RESTORE FAILED",
                f"Backup ID {backup_id} not found",
                "error"
            )
            return False
        
        display_name = backup['filename'][:40] + '...' if len(backup['filename']) > 40 else backup['filename']
        self.ui.progress.start_operation(f"Restoring: {display_name}", 100)
        
        try:
            # Step 1: Locate backup file
            self.ui.progress.update_progress(10, "Locating backup...")
            backup_path = backup['backup_path']
            
            if not os.path.exists(backup_path):
                raise Exception(f"Backup file not found: {backup_path}")
            
            # Step 2: Handle encryption
            self.ui.progress.update_progress(20, "Checking encryption...")
            if backup.get('encryption_status', 'none') != 'none':
                self.ui.progress.update_progress(30, "Decrypting file...")
                backup_path = self.encryption.decrypt_file(backup_path)
            
            # Step 3: Handle compression
            self.ui.progress.update_progress(40, "Checking compression...")
            if backup_path.endswith('.zip'):
                self.ui.progress.update_progress(50, "Decompressing file...")
                temp_dir = tempfile.mkdtemp()
                with zipfile.ZipFile(backup_path, 'r') as zf:
                    zf.extractall(temp_dir)
                backup_path = os.path.join(temp_dir, backup['filename'])
            
            # Step 4: Determine target location
            self.ui.progress.update_progress(60, "Preparing target location...")
            
            if target_path is None:
                original_dir = os.path.dirname(backup['original_path'])
                if os.path.exists(original_dir) and os.access(original_dir, os.W_OK):
                    target_path = backup['original_path']
                else:
                    desktop = os.path.expanduser('~/Desktop')
                    if os.path.exists(desktop):
                        target_path = os.path.join(desktop, backup['filename'])
                    else:
                        target_path = os.path.join(os.path.expanduser('~'), backup['filename'])
            else:
                if os.path.isdir(target_path):
                    target_path = os.path.join(target_path, backup['filename'])
            
            # Step 5: Check if file exists
            self.ui.progress.update_progress(70, "Checking destination...")
            
            if os.path.exists(target_path) and not overwrite:
                base, ext = os.path.splitext(target_path)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                target_path = f"{base}_restored_{timestamp}{ext}"
            
            # Step 6: Create target directory
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # Step 7: Copy file
            self.ui.progress.update_progress(80, "Copying file...")
            shutil.copy2(backup_path, target_path)
            
            # Step 8: Verify restore
            self.ui.progress.update_progress(90, "Verifying restore...")
            
            restored_size = os.path.getsize(target_path)
            if restored_size != backup['file_size']:
                raise Exception("Restored file size mismatch")
            
            # Step 9: Update database
            cursor = self.db.conn.cursor()
            cursor.execute('''
                UPDATE backups 
                SET restore_count = restore_count + 1,
                    last_restored = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (backup_id,))
            self.db.conn.commit()
            
            # Step 10: Set permissions
            os.chmod(target_path, 0o644)
            
            size_mb = restored_size / (1024 * 1024)
            self.ui.progress.complete_operation(
                True,
                f"✓ Restored to: {target_path}\n  Size: {size_mb:.2f} MB"
            )
            
            self.ui.display_notification(
                "RESTORE SUCCESSFUL",
                f"File: {backup['filename']}\n"
                f"Location: {target_path}\n"
                f"Size: {size_mb:.2f} MB",
                "success"
            )
            
            logging.info(f"Restored backup {backup_id}: {backup['filename']} -> {target_path}")
            
            return True
            
        except Exception as e:
            self.ui.progress.complete_operation(False, f"Failed: {str(e)}")
            self.ui.display_notification(
                "RESTORE FAILED",
                f"Could not restore {backup['filename']}\nError: {str(e)}",
                "error"
            )
            logging.error(f"Restore failed for backup {backup_id}: {e}")
            return False
    
    def restore_last_deleted(self) -> bool:
        """Restore the most recently deleted file"""
        
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT * FROM deletion_events 
            WHERE backed_up = 1 
            ORDER BY detected_at DESC 
            LIMIT 1
        ''')
        
        event = cursor.fetchone()
        if not event:
            self.ui.display_notification(
                "NO DELETIONS",
                "No backed-up deletions found",
                "info"
            )
            return False
        
        return self.restore_file(event['backup_id'])


# =========================
# 🎮 Interactive Restore Menu
# =========================

def restore_menu():
    """Interactive restore interface"""
    
    workspace = WorkspaceManager()
    restore_mgr = RestoreManager(workspace)
    ui = TerminalUI()
    
    ui.clear_screen()
    
    banner = f"""
{ui.colors.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                        ♻️  RESTORE MODULE  ♻️                        ║
║                                                                  ║
║                    Recover Your Backed Up Files                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{ui.colors.RESET}
    """
    
    print(banner)
    
    while True:
        print(f"\n{ui.colors.CYAN}┌─────────────────────────────────────────────────────────────┐{ui.colors.RESET}")
        print(f"{ui.colors.CYAN}│{ui.colors.RESET} {ui.colors.BOLD}RESTORE OPTIONS{ui.colors.RESET}")
        print(f"{ui.colors.CYAN}├─────────────────────────────────────────────────────────────┤{ui.colors.RESET}")
        print(f"{ui.colors.CYAN}│{ui.colors.RESET}  1. List recent backups")
        print(f"{ui.colors.CYAN}│{ui.colors.RESET}  2. Search backups")
        print(f"{ui.colors.CYAN}│{ui.colors.RESET}  3. Restore by ID")
        print(f"{ui.colors.CYAN}│{ui.colors.RESET}  4. Restore last deleted file")
        print(f"{ui.colors.CYAN}│{ui.colors.RESET}  5. Show workspace info")
        print(f"{ui.colors.CYAN}│{ui.colors.RESET}  0. Exit")
        print(f"{ui.colors.CYAN}└─────────────────────────────────────────────────────────────┘{ui.colors.RESET}")
        
        choice = input(f"\n{ui.colors.BRIGHT_CYAN}Select option: {ui.colors.RESET}").strip()
        
        if choice == '1':
            backups = restore_mgr.list_backups(limit=20)
            if backups:
                print(f"\n{ui.colors.BOLD}Recent Backups:{ui.colors.RESET}\n")
                print(f"{'ID':<6} {'Filename':<40} {'Size':<12} {'Category':<12}")
                print("-" * 75)
                for b in backups:
                    size_kb = b['file_size'] / 1024
                    size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"
                    filename = b['filename'][:37] + '...' if len(b['filename']) > 40 else b['filename']
                    print(f"{b['id']:<6} {filename:<40} {size_str:<12} {b['category']:<12}")
            else:
                print(f"\n{ui.colors.YELLOW}No backups found.{ui.colors.RESET}")
                
        elif choice == '2':
            query = input(f"{ui.colors.CYAN}Enter search term: {ui.colors.RESET}").strip()
            if query:
                backups = restore_mgr.search_backups(query)
                if backups:
                    print(f"\n{ui.colors.BOLD}Search Results ({len(backups)} found):{ui.colors.RESET}\n")
                    for b in backups[:30]:
                        print(f"  [{b['id']}] {b['filename']} - {b['created_at']}")
                else:
                    print(f"{ui.colors.YELLOW}No matching backups found.{ui.colors.RESET}")
                    
        elif choice == '3':
            try:
                backup_id = int(input(f"{ui.colors.CYAN}Enter backup ID: {ui.colors.RESET}"))
                target = input(f"{ui.colors.CYAN}Target directory (Enter for original): {ui.colors.RESET}").strip()
                target = target if target else None
                restore_mgr.restore_file(backup_id, target)
            except ValueError:
                print(f"{ui.colors.RED}Invalid ID{ui.colors.RESET}")
                
        elif choice == '4':
            restore_mgr.restore_last_deleted()
            
        elif choice == '5':
            info = workspace.get_workspace_info()
            stats = restore_mgr.db.get_statistics()
            
            box = ui.create_box(
                f"Workspace: {workspace.base_path}\n"
                f"Total Backups: {stats['total_backups']}\n"
                f"Total Size: {stats['total_size'] / (1024**3):.2f} GB\n"
                f"Backups Directory: {workspace.get_path('backups')}",
                title=" WORKSPACE INFO ",
                style="rounded",
                color="CYAN"
            )
            print(f"\n{box}")
            
        elif choice == '0':
            print(f"\n{ui.colors.GREEN}Exiting restore module...{ui.colors.RESET}")
            break
            
        else:
            print(f"{ui.colors.RED}Invalid option{ui.colors.RESET}")
        
        input(f"\n{ui.colors.DIM}Press Enter to continue...{ui.colors.RESET}")
        ui.clear_screen()
        print(banner)


# =========================
# 🚀 Main Application
# =========================

class DSTerminal:
    """Main application controller"""
    
    def __init__(self):
        self.ui = TerminalUI()
        self.workspace = WorkspaceManager()
        self.config_manager = ConfigManager(self.workspace)
        self.config = self.config_manager.get_config()
        self.monitor = None
        self.observer = None
        self.running = False
        
    def start(self):
        """Start DSTerminal"""
        self._show_startup_banner()
        
        self.monitor = DSTerminalMonitor(self.config, self.workspace)
        self.observer = Observer()
        
        for path in self.config['monitor_paths']:
            if os.path.exists(path):
                self.observer.schedule(self.monitor, path=path, recursive=True)
                self.ui.cinematic_print(f"  ✓ Monitoring: {path}", 0.01, "GREEN")
            else:
                self.ui.cinematic_print(f"  ✗ Path not found: {path}", 0.01, "YELLOW")
        
        self.observer.start()
        self.running = True
        
        print(f"\n{self.ui.colors.BRIGHT_CYAN}✨ System Active - Protecting Your Data ✨{self.ui.colors.RESET}")
        print(f"{self.ui.colors.DIM}Press Ctrl+C to stop monitoring{self.ui.colors.RESET}\n")
        
        stats_thread = threading.Thread(target=self._display_stats, daemon=True)
        stats_thread.start()
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def _display_stats(self):
        """Display real-time statistics"""
        last_update = 0
        while self.running:
            if time.time() - last_update > 10 and self.monitor:
                stats = self.monitor.get_statistics()
                if stats['session_backups'] > 0:
                    size_mb = stats['session_size'] / (1024 * 1024)
                    print(f"\n{self.ui.colors.DIM}📊 Session: {stats['session_backups']} files ({size_mb:.2f} MB) backed up{self.ui.colors.RESET}")
                last_update = time.time()
            time.sleep(1)
    
    def stop(self):
        """Stop DSTerminal"""
        self.running = False
        
        print(f"\n{self.ui.colors.YELLOW}🛑 Shutting down...{self.ui.colors.RESET}")
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        if self.monitor:
            self.monitor.cleanup()
        
        self._show_shutdown_summary()
    
    def _show_startup_banner(self):
        """Display startup banner - terminal responsive"""
        self.ui.clear_screen()
    
        platform_detector = PlatformDetector()
        system_info = platform_detector.get_system_info()
    
    # Get terminal width
        term_width = shutil.get_terminal_size().columns
    
    # Calculate banner width (max 70, min 50 based on terminal)
        banner_width = min(70, max(50, term_width - 4))
    
    # Create responsive banner
        def center_line(text, width=banner_width):
            visible_len = len(self.ui.strip_ansi(text))
            padding = max(0, (width - visible_len) // 2)
            return ' ' * padding + text
    
    # ASCII Art Logo - scaled based on terminal width
        if banner_width >= 70:
            logo = [
                "   ██████╗ ███████╗████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     ",
                "   ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     ",
                "   ██║  ██║███████╗   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     ",
                "   ██║  ██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     ",
                "   ██████╔╝███████║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗",
                "   ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝",
            ]
        elif banner_width >= 60:
            logo = [
                "  ██████╗ ███████╗████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗  ",
                "  ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║  ",
                "  ██║  ██║███████╗   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║  ",
                "  ██║  ██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║  ",
                "  ██████╔╝███████║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗",
                "  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝",
            ]
        else:
        # Compact logo for small terminals
            logo = [
                " ██████╗ ███████╗████████╗███████╗██████╗ ███╗   ███╗██╗",
                " ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║",
                " ██║  ██║███████╗   ██║   █████╗  ██████╔╝██╔████╔██║██║",
                " ██║  ██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║",
                " ██████╔╝███████║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║",
                " ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝",
            ]
    
    # Build centered banner
        banner_lines = []
    
    # Top border
        border_top = '╔' + '═' * (banner_width - 2) + '╗'
        banner_lines.append(f"{self.ui.colors.CYAN}{border_top}{self.ui.colors.RESET}")
    
    # Empty line
        banner_lines.append(f"{self.ui.colors.CYAN}║{' ' * (banner_width - 2)}║{self.ui.colors.RESET}")
    
    # Logo lines
        for logo_line in logo:
            banner_lines.append(f"{self.ui.colors.CYAN}║ {self.ui.colors.RESET}{logo_line}{self.ui.colors.CYAN} ║{self.ui.colors.RESET}")
    
    # Empty line
        banner_lines.append(f"{self.ui.colors.CYAN}║{' ' * (banner_width - 2)}║{self.ui.colors.RESET}")
    
    # Title lines
        title1 = "Enterprise Data Deletion Protection System"
        title2 = f"Version 3.1.0 | {system_info.get('distro', system_info['system'])}"
    
    # Center title within banner
        padding1 = (banner_width - 2 - len(title1)) // 2
        padding2 = (banner_width - 2 - len(title2)) // 2
    
        banner_lines.append(f"{self.ui.colors.CYAN}║{self.ui.colors.RESET}{' ' * padding1}{title1}{' ' * (banner_width - 2 - padding1 - len(title1))}{self.ui.colors.CYAN}║{self.ui.colors.RESET}")
        banner_lines.append(f"{self.ui.colors.CYAN}║{self.ui.colors.RESET}{' ' * padding2}{title2}{' ' * (banner_width - 2 - padding2 - len(title2))}{self.ui.colors.CYAN}║{self.ui.colors.RESET}")
    
    # Empty line
        banner_lines.append(f"{self.ui.colors.CYAN}║{' ' * (banner_width - 2)}║{self.ui.colors.RESET}")
    
    # Bottom border
        border_bottom = '╚' + '═' * (banner_width - 2) + '╝'
        banner_lines.append(f"{self.ui.colors.CYAN}{border_bottom}{self.ui.colors.RESET}")
    
    # Print banner (centered in terminal)
        for line in banner_lines:
            padding = max(0, (term_width - len(self.ui.strip_ansi(line))) // 2)
            print(' ' * padding + line)
    
        print()  # Extra spacing
    
    # Platform-specific info box (also responsive)
        distro_info = system_info.get('distro', system_info['system'])
    
    # Get paths for display
        workspace_path = self.workspace.base_path
        backups_path = self.workspace.get_path('backups')
        database_path = self.workspace.get_database_path()
    
    # Truncate long paths for display
        workspace_display = workspace_path
        if len(workspace_display) > 50:
            workspace_display = "..." + workspace_display[-47:]
    
        backups_display = backups_path
        if len(backups_display) > 50:
            backups_display = "..." + backups_display[-47:]
    
        database_display = database_path
        if len(database_display) > 50:
            database_display = "..." + database_display[-47:]
    
        info_box = self.ui.create_box(
            f"Workspace: {workspace_display}\n"
            f"System: {distro_info}\n"
            f"User: {system_info['user']}@{system_info['hostname']}\n"
            f"Backups: {backups_display}\n"
            f"Database: {database_display}\n"
            f"Encryption: {'✓ Enabled' if self.config['encrypt_backups'] else '✗ Disabled'}\n"
            f"Max File Size: {self.config['max_file_size'] / (1024*1024):.0f} MB",
            title=" SYSTEM INFORMATION ",
            style="rounded",
            color="CYAN"
        )
    
        print(info_box)
        time.sleep(0.5)

    def _show_shutdown_summary(self):
        """Display shutdown summary"""
        if self.monitor:
            stats = self.monitor.get_statistics()
            
            if REPORTLAB_AVAILABLE:
                report_gen = ReportGenerator(self.workspace)
                report_path = report_gen.generate_report(stats)
            else:
                report_path = "PDF generation disabled"
            
            summary = (
                f"Session Backups: {stats['session_backups']}\n"
                f"Data Protected: {stats['session_size'] / (1024*1024):.2f} MB\n"
                f"{'─' * 40}\n"
                f"Total Backups: {stats['total_backups']}\n"
                f"Total Protected: {stats['total_size'] / (1024**3):.2f} GB\n"
                f"Deletions Today: {stats['deletions_today']}\n"
                f"Protected Files: {stats['protected_files']}\n"
                f"{'─' * 40}\n"
                f"Report: {report_path}\n"
                f"Workspace: {self.workspace.base_path}"
            )
            
            box = self.ui.create_box(
                summary,
                title=" SESSION SUMMARY ",
                style="rounded",
                color="GREEN"
            )
            
            print(f"\n{box}\n")
        
        self.ui.cinematic_print("Thank you for using DSTerminal Enterprise!", 0.02, "CYAN")


# =========================
# 🎯 Main Entry Point
# =========================

def main():
    """Main entry point"""
    platform_detector = PlatformDetector()

    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd in ['--version', '-v']:
            print("DSTERMINAL Enterprise v3.1.0")
            sys.exit(0)
        
        elif cmd in ['--help', '-h']:
            print("""
DSTERMINAL Enterprise v3.1.0


Usage:
    python dst_secure_deletion.py [command]

Commands:
    monitor         Start monitoring (default)
    restore         Open interactive restore menu
    restore-last    Restore most recently deleted file
    restore-id ID   Restore specific backup by ID
    list-backups    List recent backups
    search TERM     Search backups by filename
    --version, -v   Show version
    --help, -h      Show this help
    --workspace     Show workspace information
    --cleanup       Clean up temporary files
    --platform      Show platform information

            """)
            sys.exit(0)
        
        elif cmd == '--platform':
            info = platform_detector.get_system_info()
            print(f"\n🌍 Platform Information:")
            for key, value in info.items():
                print(f"   {key}: {value}")
            print(f"\n📁 Monitor Paths:")
            for path in platform_detector.get_trash_paths():
                print(f"   {path}")
            sys.exit(0)

        elif cmd == 'monitor':
            app = DSTerminal()
            app.start()
            
        elif cmd == 'restore':
            restore_menu()
            
        elif cmd == 'restore-last':
            workspace = WorkspaceManager()
            restore_mgr = RestoreManager(workspace)
            restore_mgr.restore_last_deleted()
            
        elif cmd == 'restore-id':
            if len(sys.argv) > 2:
                try:
                    backup_id = int(sys.argv[2])
                    workspace = WorkspaceManager()
                    restore_mgr = RestoreManager(workspace)
                    target = sys.argv[3] if len(sys.argv) > 3 else None
                    restore_mgr.restore_file(backup_id, target)
                except ValueError:
                    print("Error: Invalid backup ID")
            else:
                print("Usage: python dst_secure_deletion.py restore-id <ID> [target_directory]")
                
        elif cmd == 'list-backups':
            workspace = WorkspaceManager()
            restore_mgr = RestoreManager(workspace)
            backups = restore_mgr.list_backups(limit=30)
            print(f"\n{'ID':<6} {'Filename':<50} {'Size':<12} {'Date':<20}")
            print("-" * 95)
            for b in backups:
                size_mb = b['file_size'] / (1024 * 1024)
                size_str = f"{size_mb:.2f} MB"
                date_str = b['created_at'][:19] if b['created_at'] else 'N/A'
                filename = b['filename'][:47] + '...' if len(b['filename']) > 50 else b['filename']
                print(f"{b['id']:<6} {filename:<50} {size_str:<12} {date_str:<20}")
                
        elif cmd == 'search':
            if len(sys.argv) > 2:
                query = sys.argv[2]
                workspace = WorkspaceManager()
                restore_mgr = RestoreManager(workspace)
                backups = restore_mgr.search_backups(query)
                print(f"\nFound {len(backups)} backup(s) matching '{query}':\n")
                for b in backups:
                    print(f"  [{b['id']}] {b['filename']} - {b['created_at']}")
            else:
                print("Usage: python dst_secure_deletion.py search <term>")
                
        elif cmd == '--workspace':
            workspace = WorkspaceManager()
            info = workspace.get_workspace_info()
            stats = BackupDatabase(workspace).get_statistics()
            print(f"\n📁 Workspace: {info['base_path']}")
            print(f"📊 Total Backups: {stats['total_backups']}")
            print(f"💾 Total Size: {stats['total_size'] / (1024**3):.2f} GB\n")
            
        elif cmd == '--cleanup':
            workspace = WorkspaceManager()
            workspace.cleanup_temp_files()
            print("✅ Temporary files cleaned up")
            
        else:
            print(f"Unknown command: {cmd}")
            print("Use --help for usage information")
    
    else:
        app = DSTerminal()
        app.start()


if __name__ == "__main__":
    main()