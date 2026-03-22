# Add these imports at the top of your file
try:
    from fpdf import FPDF
    from datetime import datetime
    import textwrap
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("Warning: fpdf not installed. PDF reports will not be available.")
    print("Install with: pip install fpdf")

import os
import json
from pathlib import Path
import hashlib
import json
import time
import shutil
import platform
import threading
import sqlite3
import glob  # Added missing import
from datetime import datetime, timedelta
from pathlib import Path
import psutil  # You'll need to install: pip install psutil
import winreg  # For Windows registry (Windows only)

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
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

# Add watchdog for real-time monitoring==============
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    # Create dummy classes so the code doesn't break
    class FileSystemEventHandler:
        def on_modified(self, event): pass
        def on_created(self, event): pass
        def on_deleted(self, event): pass
        def on_moved(self, event): pass
    
    class Observer:
        def schedule(self, *args, **kwargs): pass
        def start(self): pass
        def stop(self): pass
        def join(self): pass
    
    print(f"{Fore.YELLOW}⚠ Warning: watchdog not installed. Real-time monitoring will not work.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  Install with: pip install watchdog{Style.RESET_ALL}")
# ======end watchdog here from above===========
class SystemIntegrityMonitor:
    def __init__(self):
        self.db_file = "data/system_integrity.db"
        self.report_dir = "data/integrity_reports"
        self.baseline_dir = "data/baselines"
        self.terminal_width = shutil.get_terminal_size().columns
        
        # Create necessary directories
        for dir_path in [self.report_dir, self.baseline_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        # System paths based on OS
        self.system_paths = self._get_system_paths()
        
    # ==============================
    # SYSTEM PATH DETECTION
    # ==============================
    def _get_system_paths(self):
        """Get critical system paths based on OS"""
        system = platform.system().lower()
        paths = {
            'configs': [],
            'logs': [],
            'databases': [],
            'system_files': [],
            'user_files': []
        }
        
        if system == 'windows':
            paths.update({
                'configs': [
                    os.environ.get('WINDIR', 'C:\\Windows') + '\\System32\\config',
                    os.environ.get('PROGRAMDATA', 'C:\\ProgramData'),
                    os.path.expanduser('~\\AppData\\Local'),
                    os.path.expanduser('~\\AppData\\Roaming'),
                ],
                'logs': [
                    os.environ.get('WINDIR', 'C:\\Windows') + '\\Logs',
                    os.environ.get('WINDIR', 'C:\\Windows') + '\\System32\\LogFiles',
                    os.path.expanduser('~\\AppData\\Local\\Temp'),
                ],
                'databases': [
                    os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\Caches'),
                ],
                'system_files': [
                    os.environ.get('WINDIR', 'C:\\Windows') + '\\System32\\drivers\\etc\\hosts',
                    os.environ.get('WINDIR', 'C:\\Windows') + '\\System32\\config\\SAM',
                    os.environ.get('WINDIR', 'C:\\Windows') + '\\System32\\config\\SOFTWARE',
                ]
            })
        elif system == 'linux':
            paths.update({
                'configs': [
                    '/etc',
                    '/var/lib',
                    '/home',
                ],
                'logs': [
                    '/var/log',
                    '/var/log/syslog',
                    '/var/log/auth.log',
                ],
                'databases': [
                    '/var/lib/mysql',
                    '/var/lib/postgresql',
                    '/var/lib/mongodb',
                ],
                'system_files': [
                    '/etc/passwd',
                    '/etc/shadow',
                    '/etc/hosts',
                    '/etc/fstab',
                ]
            })
        elif system == 'darwin':  # macOS
            paths.update({
                'configs': [
                    '/etc',
                    '/Library/Preferences',
                    os.path.expanduser('~/Library/Preferences'),
                ],
                'logs': [
                    '/var/log',
                    '/Library/Logs',
                    os.path.expanduser('~/Library/Logs'),
                ],
                'databases': [
                    '/usr/local/var/mysql',
                    os.path.expanduser('~/Library/Application Support'),
                ],
                'system_files': [
                    '/etc/hosts',
                    '/etc/passwd',
                    '/etc/ssh/sshd_config',
                ]
            })
        
        # Common user directories
        paths['user_files'].extend([
            os.path.expanduser('~/Documents'),
            os.path.expanduser('~/Downloads'),
            os.path.expanduser('~/Desktop'),
        ])
        
        return paths
    
    # ==============================
    # FILE/DIRECTORY SCANNING
    # ==============================
    def scan_system(self, scan_type='all'):
        """Scan system for files, configs, logs, and databases"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': {
                'hostname': platform.node(),
                'os': platform.system(),
                'os_version': platform.version(),
                'architecture': platform.machine(),
            },
            'files': [],
            'configs': [],
            'logs': [],
            'databases': [],
            'critical_files': []
        }
    
        print(f"{Fore.CYAN}{'=' * self.terminal_width}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'SYSTEM SCAN INITIALIZED'.center(self.terminal_width)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * self.terminal_width}{Style.RESET_ALL}\n")
    
    # Scan different categories
        if scan_type in ['all', 'configs']:
            self._scan_configs(results)
    
        if scan_type in ['all', 'logs']:
            self._scan_logs(results)
    
        if scan_type in ['all', 'databases']:
            self._scan_databases(results)
    
        if scan_type in ['all', 'system']:
            self._scan_system_files(results)
    
        if scan_type in ['all', 'user']:
            self._scan_user_files(results)
    
        return results

    def _scan_configs(self, results):
        """Scan configuration files with continuous spinning animation"""
        print(f"{Fore.YELLOW}Scanning configuration files...{Style.RESET_ALL}")
    
        import threading
        import itertools
        import shutil
        import time
    
        stop_spinner = threading.Event()
    
        def spin_animation():
            """Spinning wheel animation that runs until stopped"""
            spinners = [
                ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'],  # Braille spinners
                ['▉', '▊', '▋', '▌', '▍', '▎', '▏', '▎', '▍', '▌', '▋', '▊', '▉'],  # Block spinners
                ['◢', '◣', '◤', '◥']  # Triangle spinners
            ]
            colors = [Fore.CYAN, Fore.GREEN, Fore.MAGENTA]
        
            frame = 0
            while not stop_spinner.is_set():
                left = spinners[0][frame % len(spinners[0])]
                center = spinners[1][frame % len(spinners[1])]
                right = spinners[2][frame % len(spinners[2])]
            
                colored_wheels = [
                    f"{colors[0]}{left}{Style.RESET_ALL}",
                    f"{colors[1]}{center}{Style.RESET_ALL}",
                    f"{colors[2]}{right}{Style.RESET_ALL}"
                ]
            
                terminal_width = shutil.get_terminal_size().columns
                wheels_text = f"{colored_wheels[0]}  {colored_wheels[1]}  {colored_wheels[2]}  {Fore.WHITE}Scanning configuration files...{Style.RESET_ALL}"
            
            # Remove ANSI codes for width calculation
                clean_text = wheels_text.replace(Fore.CYAN, '').replace(Fore.GREEN, '').replace(Fore.MAGENTA, '').replace(Fore.WHITE, '').replace(Style.RESET_ALL, '')
                text_width = len(clean_text)
                padding = max(0, (terminal_width - text_width) // 2)
            
                print(f"\r{' ' * padding}{wheels_text}", end='', flush=True)
                frame += 1
                time.sleep(0.1)
    
    # Start spinner in background
        spinner_thread = threading.Thread(target=spin_animation)
        spinner_thread.daemon = True
        spinner_thread.start()
    
    # Perform the actual scanning
        for config_path in self.system_paths['configs']:
            if os.path.exists(config_path):
                self._scan_directory(config_path, results['configs'], 'config')
    
    # Stop the spinner
        stop_spinner.set()
        spinner_thread.join(timeout=0.5)
    
    # Clear the spinner line
        terminal_width = shutil.get_terminal_size().columns
        print(f"\r{' ' * terminal_width}", end='\r')
    
    # Show results
        print(f"{Fore.GREEN}✓ Found {len(results['configs'])} configuration items{Style.RESET_ALL}\n")

    def _scan_logs(self, results):
        """Scan log files with continuous spinning animation"""
        print(f"{Fore.YELLOW}Scanning system logs...{Style.RESET_ALL}")
    
        import threading
        import shutil
        import time
    
        stop_spinner = threading.Event()
    
        def spin_animation():
            wheels = ['◐', '◓', '◑', '◒']
            colors = [Fore.BLUE, Fore.CYAN, Fore.LIGHTBLUE_EX]
        
            frame = 0
            while not stop_spinner.is_set():
                left = f"{colors[0]}{wheels[frame % 4]}{Style.RESET_ALL}"
                center = f"{colors[1]}{wheels[(frame + 1) % 4]}{Style.RESET_ALL}"
                right = f"{colors[2]}{wheels[(frame + 2) % 4]}{Style.RESET_ALL}"
            
                terminal_width = shutil.get_terminal_size().columns
                wheels_text = f"{left}   {center}   {right}  {Fore.WHITE}Processing log files...{Style.RESET_ALL}"
            
                clean_text = wheels_text.replace(Fore.BLUE, '').replace(Fore.CYAN, '').replace(Fore.LIGHTBLUE_EX, '').replace(Fore.WHITE, '').replace(Style.RESET_ALL, '')
                text_width = len(clean_text)
                padding = max(0, (terminal_width - text_width) // 2)
            
                print(f"\r{' ' * padding}{wheels_text}", end='', flush=True)
                frame += 1
                time.sleep(0.1)
    
        spinner_thread = threading.Thread(target=spin_animation)
        spinner_thread.daemon = True
        spinner_thread.start()
    
        for log_path in self.system_paths['logs']:
            if os.path.exists(log_path):
                self._scan_directory(log_path, results['logs'], 'log')
    
        stop_spinner.set()
        spinner_thread.join(timeout=0.5)
    
        terminal_width = shutil.get_terminal_size().columns
        print(f"\r{' ' * terminal_width}", end='\r')
    
        print(f"{Fore.GREEN}✓ Found {len(results['logs'])} log files{Style.RESET_ALL}\n")

    def _scan_databases(self, results):
        """Scan database files with continuous spinning animation"""
        print(f"{Fore.YELLOW}Scanning databases...{Style.RESET_ALL}")
    
        import threading
        import shutil
        import time
    
        stop_spinner = threading.Event()
    
        def spin_animation():
            wheels = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
            colors = [Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX]
        
            frame = 0
            while not stop_spinner.is_set():
                left = f"{colors[0]}{wheels[frame % 8]}{Style.RESET_ALL}"
                center = f"{colors[1]}{wheels[(frame + 2) % 8]}{Style.RESET_ALL}"
                right = f"{colors[2]}{wheels[(frame + 4) % 8]}{Style.RESET_ALL}"
            
                terminal_width = shutil.get_terminal_size().columns
                wheels_text = f"{left}   {center}   {right}  {Fore.WHITE}Querying databases...{Style.RESET_ALL}"
            
                clean_text = wheels_text.replace(Fore.MAGENTA, '').replace(Fore.LIGHTMAGENTA_EX, '').replace(Fore.LIGHTRED_EX, '').replace(Fore.WHITE, '').replace(Style.RESET_ALL, '')
                text_width = len(clean_text)
                padding = max(0, (terminal_width - text_width) // 2)
            
                print(f"\r{' ' * padding}{wheels_text}", end='', flush=True)
                frame += 1
                time.sleep(0.1)
    
        spinner_thread = threading.Thread(target=spin_animation)
        spinner_thread.daemon = True
        spinner_thread.start()
    
        for db_path in self.system_paths['databases']:
            if os.path.exists(db_path):
                self._scan_directory(db_path, results['databases'], 'database')
    
        stop_spinner.set()
        spinner_thread.join(timeout=0.5)
    
        terminal_width = shutil.get_terminal_size().columns
        print(f"\r{' ' * terminal_width}", end='\r')
    
        print(f"{Fore.GREEN}✓ Found {len(results['databases'])} database files{Style.RESET_ALL}\n")

    def _scan_system_files(self, results):
        """Scan critical system files with continuous spinning animation"""
        print(f"{Fore.YELLOW}Scanning critical system files...{Style.RESET_ALL}")
    
        import threading
        import shutil
        import time
    
        stop_spinner = threading.Event()
    
        def spin_animation():
            wheels = ['◢', '◣', '◤', '◥']
            colors = [Fore.RED, Fore.LIGHTRED_EX, Fore.YELLOW]
        
            frame = 0
            while not stop_spinner.is_set():
                left = f"{colors[0]}{wheels[frame % 4]}{Style.RESET_ALL}"
                center = f"{colors[1]}{wheels[(frame + 1) % 4]}{Style.RESET_ALL}"
                right = f"{colors[2]}{wheels[(frame + 2) % 4]}{Style.RESET_ALL}"
            
                terminal_width = shutil.get_terminal_size().columns
                wheels_text = f"{left}   {center}   {right}  {Fore.WHITE}Checking system integrity...{Style.RESET_ALL}"
            
                clean_text = wheels_text.replace(Fore.RED, '').replace(Fore.LIGHTRED_EX, '').replace(Fore.YELLOW, '').replace(Fore.WHITE, '').replace(Style.RESET_ALL, '')
                text_width = len(clean_text)
                padding = max(0, (terminal_width - text_width) // 2)
            
                print(f"\r{' ' * padding}{wheels_text}", end='', flush=True)
                frame += 1
                time.sleep(0.1)
    
        spinner_thread = threading.Thread(target=spin_animation)
        spinner_thread.daemon = True
        spinner_thread.start()
    
        for file_path in self.system_paths['system_files']:
            if os.path.exists(file_path):
                file_info = self._get_file_info(file_path)
                file_info['category'] = 'system'
                results['critical_files'].append(file_info)
    
        stop_spinner.set()
        spinner_thread.join(timeout=0.5)
    
        terminal_width = shutil.get_terminal_size().columns
        print(f"\r{' ' * terminal_width}", end='\r')
    
        print(f"{Fore.GREEN}✓ Found {len(results['critical_files'])} critical system files{Style.RESET_ALL}\n")

    def _scan_user_files(self, results):
        """Scan user files with continuous spinning animation"""
        print(f"{Fore.YELLOW}Scanning user files...{Style.RESET_ALL}")
    
        import threading
        import shutil
        import time
    
        stop_spinner = threading.Event()
    
        def spin_animation():
            wheels = ['▉', '▊', '▋', '▌', '▍', '▎', '▏', '▎', '▍', '▌', '▋', '▊', '▉']
            colors = [Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.CYAN]
        
            frame = 0
            while not stop_spinner.is_set():
                left = f"{colors[0]}{wheels[frame % len(wheels)]}{Style.RESET_ALL}"
                center = f"{colors[1]}{wheels[(frame + 3) % len(wheels)]}{Style.RESET_ALL}"
                right = f"{colors[2]}{wheels[(frame + 6) % len(wheels)]}{Style.RESET_ALL}"
            
                terminal_width = shutil.get_terminal_size().columns
                wheels_text = f"{left}   {center}   {right}  {Fore.WHITE}Indexing user files...{Style.RESET_ALL}"
            
                clean_text = wheels_text.replace(Fore.GREEN, '').replace(Fore.LIGHTGREEN_EX, '').replace(Fore.CYAN, '').replace(Fore.WHITE, '').replace(Style.RESET_ALL, '')
                text_width = len(clean_text)
                padding = max(0, (terminal_width - text_width) // 2)
            
                print(f"\r{' ' * padding}{wheels_text}", end='', flush=True)
                frame += 1
                time.sleep(0.05)
    
        spinner_thread = threading.Thread(target=spin_animation)
        spinner_thread.daemon = True
        spinner_thread.start()
    
        for user_path in self.system_paths['user_files']:
            if os.path.exists(user_path):
                self._scan_directory(user_path, results['files'], 'user')
    
        stop_spinner.set()
        spinner_thread.join(timeout=0.5)
    
        terminal_width = shutil.get_terminal_size().columns
        print(f"\r{' ' * terminal_width}", end='\r')
    
        print(f"{Fore.GREEN}✓ Found {len(results['files'])} user files{Style.RESET_ALL}\n")

    def _scan_directory(self, directory, results_list, category, max_depth=3):
        """Recursively scan a directory with depth limit"""
        try:
            for root, dirs, files in os.walk(directory):
            # Check depth
                depth = root.replace(directory, '').count(os.sep)
                if depth > max_depth:
                    dirs[:] = []  # Don't go deeper
                    continue
            
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.exists(file_path) and os.path.isfile(file_path):
                        file_info = self._get_file_info(file_path)
                        file_info['category'] = category
                        results_list.append(file_info)


        except (PermissionError, OSError) as e:
            print(f"{Fore.RED}Permission denied: {directory}{Style.RESET_ALL}")
 # ======================================ends here==================
    def _get_file_info(self, file_path):
        """Get detailed file information"""
        try:
            stat = os.stat(file_path)
        
        # Get file hash for integrity checking
            file_hash = self._calculate_hash(file_path)
        
        # Get file permissions/attributes
            permissions = self._get_file_permissions(file_path)
        
            return {
                'path': file_path,
                'name': os.path.basename(file_path),
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'accessed': datetime.fromtimestamp(stat.st_atime).isoformat(),
                'hash': file_hash,
                'permissions': permissions,
                'owner': self._get_file_owner(file_path),
                'extension': os.path.splitext(file_path)[1],
                'is_hidden': self._is_hidden_file(file_path)
            }
        except Exception as e:
            return {
                'path': file_path,
                'name': os.path.basename(file_path),
                'error': str(e)
            }

    
    def _calculate_hash(self, file_path):
        """Calculate SHA-256 hash of file"""
        try:
            sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except:
            return None

    def _get_file_permissions(self, file_path):
        """Get file permissions (platform-specific)"""
        if platform.system().lower() == 'windows':
            try:
            # Windows: check if file is read-only
                return 'readonly' if not os.access(file_path, os.W_OK) else 'read-write'
            except:
                return 'unknown'
        else:
        # Unix-like: get octal permissions
            try:
                stat = os.stat(file_path)
                return oct(stat.st_mode)[-3:]
            except:
                return 'unknown'

    def _get_file_owner(self, file_path):
        """Get file owner"""
        try:
            import pwd
            stat = os.stat(file_path)
            return pwd.getpwuid(stat.st_uid).pw_name
        except:
            try:
                import getpass
                return getpass.getuser()
            except:
                return 'unknown'

    def _is_hidden_file(self, file_path):
        """Check if file is hidden"""
        if platform.system().lower() == 'windows':
            try:
                import ctypes
                attrs = ctypes.windll.kernel32.GetFileAttributesW(file_path)
                return attrs != -1 and bool(attrs & 2)  # FILE_ATTRIBUTE_HIDDEN
            except:
                return os.path.basename(file_path).startswith('.')
        else:
            return os.path.basename(file_path).startswith('.')
    # ==============================
    # INTEGRITY CHECKING
    # ==============================
    def check_integrity(self, scan_results=None):
        """Check system integrity against baseline"""
        if scan_results is None:
            scan_results = self.scan_system()
        
        baseline = self._load_baseline()
        
        if not baseline:
            print(f"{Fore.YELLOW}No baseline found. Creating initial baseline...{Style.RESET_ALL}")
            self.create_baseline(scan_results)
            return None
        
        print(f"{Fore.CYAN}{'=' * self.terminal_width}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'INTEGRITY CHECK IN PROGRESS'.center(self.terminal_width)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * self.terminal_width}{Style.RESET_ALL}\n")
        
        changes = {
            'new_files': [],
            'modified_files': [],
            'deleted_files': [],
            'permission_changes': [],
            'suspicious_changes': []
        }
        
        # Create lookup dictionaries
        baseline_files = {f['path']: f for f in baseline.get('files', [])}
        baseline_configs = {f['path']: f for f in baseline.get('configs', [])}
        baseline_logs = {f['path']: f for f in baseline.get('logs', [])}
        baseline_databases = {f['path']: f for f in baseline.get('databases', [])}
        baseline_critical = {f['path']: f for f in baseline.get('critical_files', [])}
        
        all_baseline = {**baseline_files, **baseline_configs, **baseline_logs, 
                       **baseline_databases, **baseline_critical}
        
        all_current = {f['path']: f for f in scan_results['files']}
        all_current.update({f['path']: f for f in scan_results['configs']})
        all_current.update({f['path']: f for f in scan_results['logs']})
        all_current.update({f['path']: f for f in scan_results['databases']})
        all_current.update({f['path']: f for f in scan_results['critical_files']})
        
        # Check for modifications and deletions
        total_items = len(all_baseline)
        current = 0
        for i, (path, baseline_info) in enumerate(all_baseline.items(), 1):
            self._print_progress(i, total_items, "Analyzing files")
            current = i
            if path not in all_current:
                changes['deleted_files'].append({
                    'path': path,
                    'baseline_info': baseline_info,
                    'severity': 'HIGH' if baseline_info.get('category') == 'system' else 'MEDIUM'
                })
                continue
            
            current_info = all_current[path]
            
            # Check hash
            if baseline_info.get('hash') != current_info.get('hash'):
                change_type = self._analyze_change(baseline_info, current_info)
                changes['modified_files'].append({
                    'path': path,
                    'baseline': baseline_info,
                    'current': current_info,
                    'change_type': change_type,
                    'severity': self._determine_severity(path, change_type)
                })
            
            # Check permissions
            if baseline_info.get('permissions') != current_info.get('permissions'):
                changes['permission_changes'].append({
                    'path': path,
                    'old_perms': baseline_info.get('permissions'),
                    'new_perms': current_info.get('permissions')
                })
        
        # Check for new files
        for path, current_info in all_current.items():
            if path not in all_baseline:
                changes['new_files'].append({
                    'path': path,
                    'current_info': current_info,
                    'severity': self._determine_severity(path, 'new')
                })
        
        return changes
    
    def _analyze_change(self, baseline, current):
        """Analyze the type of change made to a file"""
        reasons = []
        
        # Size change
        if baseline.get('size') != current.get('size'):
            size_diff = current.get('size', 0) - baseline.get('size', 0)
            if size_diff > 0:
                reasons.append(f"Size increased by {self._format_size(size_diff)}")
            else:
                reasons.append(f"Size decreased by {self._format_size(abs(size_diff))}")
        
        # Timestamp analysis
        baseline_modified = datetime.fromisoformat(baseline.get('modified', '2000-01-01'))
        current_modified = datetime.fromisoformat(current.get('modified', '2000-01-01'))
        
        if current_modified > baseline_modified:
            time_diff = current_modified - baseline_modified
            if time_diff < timedelta(minutes=5):
                reasons.append("Modified very recently (within 5 minutes)")
            elif time_diff < timedelta(hours=1):
                reasons.append("Modified within the last hour")
            else:
                reasons.append(f"Modified {time_diff.days} days ago")
        
        # Extension change (possible masquerading)
        if baseline.get('extension') != current.get('extension'):
            reasons.append(f"File extension changed from {baseline.get('extension')} to {current.get('extension')}")
        
        return reasons if reasons else ["Content modified"]
    
    def _determine_severity(self, path, change_type):
        """Determine severity of change"""
        if any(critical in path.lower() for critical in ['system32', 'etc', 'kernel', 'boot']):
            return 'CRITICAL'
        elif any(sensitive in path.lower() for sensitive in ['config', 'password', 'shadow', 'sam']):
            return 'HIGH'
        elif any(important in path.lower() for important in ['log', 'database', 'data']):
            return 'MEDIUM'
        else:
            return 'LOW'
    
    # ==============================
    # BASELINE MANAGEMENT
    # ==============================
    def create_baseline(self, scan_results=None):
        """Create a baseline of system state"""
        if scan_results is None:
            scan_results = self.scan_system()
        
        baseline = {
            'created': datetime.now().isoformat(),
            'system_info': scan_results['system_info'],
            'files': scan_results['files'],
            'configs': scan_results['configs'],
            'logs': scan_results['logs'],
            'databases': scan_results['databases'],
            'critical_files': scan_results['critical_files']
        }
        
        # Save baseline
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        baseline_file = os.path.join(self.baseline_dir, f'baseline_{timestamp}.json')
        
        with open(baseline_file, 'w') as f:
            json.dump(baseline, f, indent=2)
        
        # Also save as latest baseline
        latest_file = os.path.join(self.baseline_dir, 'latest_baseline.json')
        with open(latest_file, 'w') as f:
            json.dump(baseline, f, indent=2)
        
        print(f"\n{Fore.GREEN}✓ Baseline created successfully{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Saved to: {baseline_file}{Style.RESET_ALL}")
        
        return baseline
    
    def _load_baseline(self):
        """Load the latest baseline"""
        latest_file = os.path.join(self.baseline_dir, 'latest_baseline.json')
        if os.path.exists(latest_file):
            with open(latest_file, 'r') as f:
                return json.load(f)
        return None
    
    # ==============================
    # REPORT GENERATION
    # ==============================
    def generate_json_report(self, changes=None, scan_results=None):
        """Generate a JSON format integrity report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(self.report_dir, f'report_{timestamp}.json')
    
        if scan_results is None:
            scan_results = self.scan_system()
    
    # Prepare report data
        report_data = {
            'metadata': {
                'report_type': 'integrity_report',
                'format': 'json',  # Add format here if needed
                'generated': datetime.now().isoformat(),
                'version': '2.0.113'
            },
            'system_info': scan_results['system_info'],
            'summary': {
                'total_files_scanned': (
                    len(scan_results['files']) +
                    len(scan_results['configs']) +
                    len(scan_results['logs']) +
                    len(scan_results['databases']) +
                    len(scan_results['critical_files'])
                ),
                'categories': {
                    'critical_files': len(scan_results['critical_files']),
                    'configs': len(scan_results['configs']),
                    'logs': len(scan_results['logs']),
                    'databases': len(scan_results['databases']),
                    'user_files': len(scan_results['files'])
                }
            },
            'inventory': {
                'critical_files': scan_results['critical_files'][:100],  # Limit for readability
                'configs': scan_results['configs'][:100],
                'logs': scan_results['logs'][:100],
                'databases': scan_results['databases'][:100],
                'user_files': scan_results['files'][:100]
            }
        }
    
    # Add changes if available
        if changes:
            # Count by severity
            critical_count = 0
            high_count = 0
            medium_count = 0
            low_count = 0
        
            for change_type in ['new_files', 'modified_files', 'deleted_files']:
                for item in changes.get(change_type, []):
                    severity = item.get('severity', 'LOW')
                    if severity == 'CRITICAL':
                        critical_count += 1
                    elif severity == 'HIGH':
                        high_count += 1
                    elif severity == 'MEDIUM':
                        medium_count += 1
                    else:
                        low_count += 1
        
            report_data['changes'] = {
                'new_files': changes.get('new_files', []),
                'modified_files': changes.get('modified_files', []),
                'deleted_files': changes.get('deleted_files', []),
                'permission_changes': changes.get('permission_changes', []),
                'summary': {
                    'total_changes': (
                        len(changes.get('new_files', [])) +
                        len(changes.get('modified_files', [])) +
                        len(changes.get('deleted_files', []))
                    ),
                    'severity_breakdown': {
                        'CRITICAL': critical_count,
                        'HIGH': high_count,
                        'MEDIUM': medium_count,
                        'LOW': low_count
                    }
                }
            }
    
    # Write JSON file
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, default=str)
            print(f"{Fore.GREEN}✓ JSON report generated: {report_file}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Failed to generate JSON report: {e}{Style.RESET_ALL}")
            return None
    
        return report_file

    # ===================
    def generate_pdf_report(self, changes=None, scan_results=None):
        """Generate a formatted PDF integrity report with DSTerminal logo"""
        try:
            from fpdf import FPDF
            import textwrap
            import os
            from datetime import datetime
        except ImportError:
            print(f"{Fore.RED}✗ fpdf2 not installed. Install with: pip install fpdf2{Style.RESET_ALL}")
            return None
    
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(self.report_dir, f'report_{timestamp}.pdf')
    
        if scan_results is None:
            scan_results = self.scan_system()
    
    # Create PDF with Unicode support
        pdf = FPDF()
        pdf.add_page()
    
    # Add Unicode font support (use built-in fonts that support Unicode)
        pdf.set_font("Helvetica", size=10)
    
    # ==================== HEADER WITH ASCII LOGO ====================
    # Use ASCII art that's safe for PDF
        pdf.set_font("Courier", size=8)
    
    # Center the ASCII logo
        page_width = pdf.w - 2 * pdf.l_margin
        logo_lines = [
            "+--------------------------------------------------+",
            "|     DSTERMINAL INTEGRITY MONITOR                |",
            "|                                                  |",
            "|     ██████╗ ███████╗████████╗███████╗██████╗    |",
            "|     ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗   |",
            "|     ██║  ██║███████╗   ██║   █████╗  ██████╔╝   |",
            "|     ██║  ██║╚════██║   ██║   ██╔══╝  ██╔══██╗   |",
            "|     ██████╔╝███████║   ██║   ███████╗██║  ██║   |",
            "|     ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝   |",
            "|                                                  |",
            "+--------------------------------------------------+"
        ]
    
        for line in logo_lines:
        # Replace Unicode box characters with ASCII if needed
            safe_line = line.replace('╔', '+').replace('╗', '+').replace('╚', '+').replace('╝', '+')
            safe_line = safe_line.replace('═', '-').replace('║', '|')
        
            line_width = pdf.get_string_width(safe_line)
            x = (page_width - line_width) / 2 + pdf.l_margin
            pdf.set_x(x)
            pdf.cell(line_width, 4, safe_line, ln=True)
    
        pdf.ln(5)
    
    # ==================== TITLE ====================
        pdf.set_font("Helvetica", 'B', 16)
        title = "SYSTEM INTEGRITY REPORT"
        title_width = pdf.get_string_width(title)
        x = (page_width - title_width) / 2 + pdf.l_margin
        pdf.set_x(x)
        pdf.cell(title_width, 10, title, ln=True)
    
        pdf.set_font("Helvetica", size=10)
        pdf.ln(5)
    
    # ==================== METADATA SECTION ====================
        pdf.set_fill_color(230, 230, 250)  # Light lavender
        pdf.set_font("Helvetica", 'B', 11)
        pdf.cell(0, 8, "REPORT METADATA", 0, 1, 'L', 1)
        pdf.set_font("Helvetica", size=9)
    
    # Safe string function to avoid encoding issues
        def safe_str(text):
            if text is None:
                return ""
        # Replace any problematic characters
            return str(text).encode('ascii', errors='replace').decode('ascii')
    
    # System info
        pdf.cell(40, 6, "Generated:", 0, 0)
        pdf.cell(0, 6, safe_str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 0, 1)
    
        pdf.cell(40, 6, "Hostname:", 0, 0)
        pdf.cell(0, 6, safe_str(scan_results['system_info'].get('hostname', 'Unknown')), 0, 1)
    
    # Fix Windows display
        os_name = scan_results['system_info'].get('os', 'Unknown')
        os_version = scan_results['system_info'].get('os_version', '')
        if os_name == 'Windows' and '10.0.' in os_version:
            build = os_version.split('.')[2] if len(os_version.split('.')) > 2 else '0'
            if build.isdigit() and int(build) >= 22000:
                os_name = "Windows 11"
    
        pdf.cell(40, 6, "OS:", 0, 0)
        pdf.cell(0, 6, safe_str(f"{os_name} {os_version}"), 0, 1)
    
        pdf.cell(40, 6, "Architecture:", 0, 0)
        pdf.cell(0, 6, safe_str(scan_results['system_info'].get('architecture', 'Unknown')), 0, 1)
        pdf.ln(5)
    
    # ==================== SCAN SUMMARY ====================
        pdf.set_fill_color(173, 216, 230)  # Light blue
        pdf.set_font("Helvetica", 'B', 11)
        pdf.cell(0, 8, "SCAN SUMMARY", 0, 1, 'L', 1)
        pdf.set_font("Helvetica", size=9)
    
        total_files = (
            len(scan_results.get('critical_files', [])) +
            len(scan_results.get('configs', [])) +
            len(scan_results.get('logs', [])) +
            len(scan_results.get('databases', [])) +
            len(scan_results.get('files', []))
        )
    
        stats = [
            ("Critical System Files:", len(scan_results.get('critical_files', []))),
            ("Configuration Files:", len(scan_results.get('configs', []))),
            ("Log Files:", len(scan_results.get('logs', []))),
            ("Databases:", len(scan_results.get('databases', []))),
            ("User Files:", len(scan_results.get('files', []))),
            ("TOTAL FILES SCANNED:", total_files)
        ]
    
        for label, value in stats:
            pdf.cell(50, 6, label, 0, 0)
            pdf.cell(0, 6, str(value), 0, 1)
        pdf.ln(5)
    
    # ==================== INTEGRITY FINDINGS ====================
        if changes and any([changes.get('new_files', []), 
                            changes.get('modified_files', []), 
                            changes.get('deleted_files', [])]):
            pdf.set_fill_color(255, 228, 225)  # Misty rose
            pdf.set_font("Helvetica", 'B', 11)
            pdf.cell(0, 8, "INTEGRITY FINDINGS", 0, 1, 'L', 1)
            pdf.set_font("Helvetica", size=9)
        
        # Change summary
            change_stats = [
                ("New Files:", len(changes.get('new_files', []))),
                ("Modified Files:", len(changes.get('modified_files', []))),
                ("Deleted Files:", len(changes.get('deleted_files', []))),
            ]
        
            for label, value in change_stats:
                pdf.cell(40, 5, label, 0, 0)
                pdf.cell(0, 5, str(value), 0, 1)
        
        # Critical changes
            critical_items = []
            for change_type in ['new_files', 'modified_files', 'deleted_files']:
                for item in changes.get(change_type, []):
                    if item.get('severity') in ['CRITICAL', 'HIGH']:
                        critical_items.append((change_type, item))
        
            if critical_items:
                pdf.ln(3)
                pdf.set_text_color(255, 0, 0)  # Red
                pdf.set_font("Helvetica", 'B', 10)
                pdf.cell(0, 6, "CRITICAL/HIGH SEVERITY CHANGES:", 0, 1)
                pdf.set_text_color(0, 0, 0)  # Back to black
                pdf.set_font("Helvetica", size=8)
            
                for change_type, item in critical_items[:10]:
                    path = safe_str(item.get('path', 'Unknown'))
                    if len(path) > 70:
                        path = path[:67] + "..."
                    pdf.cell(15, 4, f"[{item.get('severity', 'UNKNOWN')}]", 0, 0)
                    pdf.multi_cell(0, 4, path)
        else:
            pdf.set_text_color(0, 128, 0)  # Green
            pdf.set_font("Helvetica", 'B', 11)
            pdf.cell(0, 8, "✓ SYSTEM INTEGRITY INTACT - No changes detected", 0, 1)
            pdf.set_text_color(0, 0, 0)
    
        pdf.ln(5)
    
    # ==================== FILE INVENTORY SAMPLES ====================
        pdf.set_fill_color(240, 248, 255)  # Alice blue
        pdf.set_font("Helvetica", 'B', 11)
        pdf.cell(0, 8, "RECENT FILES (Sample)", 0, 1, 'L', 1)
        pdf.set_font("Helvetica", size=8)
    
        categories = [
            ('Critical System Files', scan_results.get('critical_files', [])[:5]),
            ('Recent Configs', sorted(scan_results.get('configs', []), 
                                    key=lambda x: x.get('modified', ''), reverse=True)[:5]),
            ('Recent Logs', sorted(scan_results.get('logs', []), 
                                key=lambda x: x.get('modified', ''), reverse=True)[:5])
        ]
    
        for cat_name, items in categories:
            if items:
                pdf.set_font("Helvetica", 'B', 9)
                pdf.cell(0, 5, f"{cat_name}:", 0, 1)
                pdf.set_font("Helvetica", size=8)
            
                for item in items:
                    name = safe_str(item.get('name', 'Unknown'))
                    if len(name) > 40:
                        name = name[:37] + "..."
                    modified = item.get('modified', 'Unknown')[:10] if item.get('modified') else 'Unknown'
                    pdf.cell(40, 4, modified, 0, 0)
                    pdf.cell(0, 4, name, 0, 1)
                pdf.ln(2)
    
    # ==================== PROGRESS BAR SUMMARY ====================
    # Add a progress summary using ASCII instead of Unicode blocks
        pdf.set_fill_color(220, 220, 220)  # Light gray
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(0, 6, "SCAN PROGRESS SUMMARY", 0, 1, 'L', 1)
        pdf.set_font("Helvetica", size=8)
    
    # Create ASCII progress bar using = and - instead of blocks
        total = total_files
        if total > 0:
            bar_length = 40
            filled = bar_length  # 100% complete
        
        # Use ASCII characters instead of Unicode blocks
            progress_bar = "[" + "=" * filled + "]" + f" 100% ({total} files)"
        
            pdf.cell(0, 4, f"Configuration Files: {len(scan_results.get('configs', []))}", 0, 1)
            pdf.cell(0, 4, f"Log Files: {len(scan_results.get('logs', []))}", 0, 1)
            pdf.cell(0, 4, f"Database Files: {len(scan_results.get('databases', []))}", 0, 1)
            pdf.cell(0, 4, f"System Files: {len(scan_results.get('critical_files', []))}", 0, 1)
            pdf.cell(0, 4, f"User Files: {len(scan_results.get('files', []))}", 0, 1)
            pdf.ln(2)
            pdf.cell(0, 4, f"Progress: {progress_bar}", 0, 1)
    
    # ==================== FOOTER ====================
        pdf.set_y(-30)
        pdf.set_font("Helvetica", 'I', 8)
        pdf.cell(0, 5, "Generated by DSTerminal Integrity Monitor v2.0.113", 0, 1, 'C')
        pdf.cell(0, 5, f"Report: {os.path.basename(report_file)}", 0, 1, 'C')
    
    # Save PDF
        try:
            pdf.output(report_file)
            print(f"{Fore.GREEN}✓ PDF report generated: {report_file}{Style.RESET_ALL}")
            return report_file
        except Exception as e:
            print(f"{Fore.RED}✗ Failed to generate PDF: {e}{Style.RESET_ALL}")
            return None
    
        # ======================
    def generate_all_reports(self, changes, scan_results=None):
        """Generate all report formats (TXT, JSON, PDF)"""
        if scan_results is None:
            scan_results = self.scan_system()
    
        reports = {}
    
    # Generate TXT report (existing)
        reports['txt'] = self.generate_report(changes, scan_results)
    
    # Generate JSON report
        reports['json'] = self.generate_json_report(changes, scan_results)
    
    # Generate PDF report
        reports['pdf'] = self.generate_pdf_report(changes, scan_results)
    
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ ALL REPORTS GENERATED SUCCESSFULLY{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}TXT Report: {reports['txt']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}JSON Report: {reports['json']}{Style.RESET_ALL}")
        if reports['pdf']:
            print(f"{Fore.CYAN}PDF Report: {reports['pdf']}{Style.RESET_ALL}")
    
        return reports
# =======================end report gen====
    def _generate_report_header(self, scan_results):
        """Generate report header"""
        header = []
        header.append("="*80)
        header.append("DSTERMINAL SYSTEM INTEGRITY REPORT".center(80))
        header.append("="*80)
        header.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        header.append(f"Hostname: {scan_results['system_info']['hostname']}")
        os_info = scan_results['system_info']['os']
        os_version = scan_results['system_info']['os_version']

        if os_info =='Windows' and '10.0.' in os_version:
            build = os_version.split('.')[2] if len(os_version.split('.')) > 2 else '0'
            if int(build) >= 22000:
                os_info = 'Windows 11'
        header.append(f"OS: {os_info} {os_version}")
        # header.append(f"OS: {scan_results['system_info']['os']} {scan_results['system_info']['os_version']}")
        header.append("="*80 + "\n")
        return "\n".join(header)
    
    def _generate_system_info(self, scan_results):
        """Generate system information section"""
        info = []
        info.append("\n" + "="*80)
        info.append("SYSTEM INFORMATION".center(80))
        info.append("="*80)
        
        for key, value in scan_results['system_info'].items():
            info.append(f"{key.upper()}: {value}")
        
        return "\n".join(info) + "\n"
    
    def _generate_inventory(self, scan_results):
        """Generate inventory section - without emojis"""
        inventory = []
        inventory.append("\n" + "="*80)
        inventory.append("SYSTEM INVENTORY".center(80))
        inventory.append("="*80)
        
        categories = [
            ('Critical System Files', scan_results['critical_files']),
            ('Configuration Files', scan_results['configs']),
            ('Log Files', scan_results['logs']),
            ('Databases', scan_results['databases']),
            ('User Files', scan_results['files'])
        ]
        
        for category_name, items in categories:
            inventory.append(f"\n{category_name} ({len(items)} items):")
            inventory.append("-"*40)
            
            # Show most recent items
            for item in sorted(items, key=lambda x: x.get('modified', ''), reverse=True)[:10]:
                created = datetime.fromisoformat(item['created']).strftime('%Y-%m-%d %H:%M')
                modified = datetime.fromisoformat(item['modified']).strftime('%Y-%m-%d %H:%M')
                inventory.append(f"  [FILE] {item['name']}")
                inventory.append(f"     Path: {item['path']}")
                inventory.append(f"     Created: {created}")
                inventory.append(f"     Modified: {modified}")
                inventory.append(f"     Size: {self._format_size(item['size'])}")
                inventory.append("")
        
        return "\n".join(inventory)
    
    def _generate_findings(self, changes):
        """Generate integrity findings section - without emojis"""
        findings = []
        findings.append("\n" + "="*80)
        findings.append("INTEGRITY FINDINGS".center(80))
        findings.append("="*80 + "\n")
        
        # Summary
        findings.append("SUMMARY OF CHANGES:")
        findings.append("-"*40)
        findings.append(f"New Files: {len(changes['new_files'])}")
        findings.append(f"Modified Files: {len(changes['modified_files'])}")
        findings.append(f"Deleted Files: {len(changes['deleted_files'])}")
        findings.append(f"Permission Changes: {len(changes['permission_changes'])}")
        findings.append("")
        
        # Detailed findings by severity
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        
        all_findings = []
        all_findings.extend([('new', f) for f in changes['new_files']])
        all_findings.extend([('modified', f) for f in changes['modified_files']])
        all_findings.extend([('deleted', f) for f in changes['deleted_files']])
        
        # Sort by severity
        all_findings.sort(key=lambda x: severity_order.get(x[1].get('severity', 'LOW'), 99))
        
        for change_type, finding in all_findings:
            severity = finding.get('severity', 'LOW')
            # Use text instead of emojis
            severity_text = {
                'CRITICAL': '[CRITICAL]',
                'HIGH': '[HIGH]',
                'MEDIUM': '[MEDIUM]',
                'LOW': '[LOW]'
            }.get(severity, '[UNKNOWN]')
            
            findings.append(f"\n{severity_text} {finding['path']}")
            findings.append("-"*40)
            
            if change_type == 'new':
                findings.append(f"  Type: New file detected")
                findings.append(f"  Created: {finding['current_info'].get('created', 'Unknown')}")
                findings.append(f"  Size: {self._format_size(finding['current_info'].get('size', 0))}")
            
            elif change_type == 'modified':
                findings.append(f"  Type: File modified")
                for reason in finding.get('change_type', ['Unknown change']):
                    findings.append(f"  • {reason}")
            
            elif change_type == 'deleted':
                findings.append(f"  Type: File deleted")
                findings.append(f"  Last known: {finding['baseline_info'].get('modified', 'Unknown')}")
        
        return "\n".join(findings)
    
    def _generate_mitigations(self, changes):
        """Generate mitigation recommendations - without emojis"""
        mitigations = []
        mitigations.append("\n" + "="*80)
        mitigations.append("MITIGATION RECOMMENDATIONS".center(80))
        mitigations.append("="*80 + "\n")
        
        # Group changes by severity and type
        critical_items = []
        high_items = []
        medium_items = []
        suspicious_patterns = []
        
        for change_type, items_list in [
            ('new', changes['new_files']),
            ('modified', changes['modified_files']),
            ('deleted', changes['deleted_files'])
        ]:
            for item in items_list:
                severity = item.get('severity', 'LOW')
                if severity == 'CRITICAL':
                    critical_items.append((change_type, item))
                elif severity == 'HIGH':
                    high_items.append((change_type, item))
                elif severity == 'MEDIUM':
                    medium_items.append((change_type, item))
        
        # Critical mitigations
        if critical_items:
            mitigations.append("CRITICAL ISSUES - IMMEDIATE ACTION REQUIRED:")
            mitigations.append("-"*40)
            for change_type, item in critical_items:
                mitigations.append(f"  • {item['path']}")
                mitigations.append(f"    Action: Immediate investigation required")
                mitigations.append(f"    Check: System logs, user activity, running processes")
                
                # Specific mitigations based on file type
                if 'system32' in item['path'].lower() or 'etc' in item['path'].lower():
                    mitigations.append(f"    • Verify system integrity with SFC /scannow (Windows) or package manager verification")
                    mitigations.append(f"    • Check for unauthorized administrative access")
                elif any(db in item['path'].lower() for db in ['database', 'sql', 'mysql']):
                    mitigations.append(f"    • Review database access logs")
                    mitigations.append(f"    • Check for SQL injection attacks")
            mitigations.append("")
        
        # High severity mitigations
        if high_items:
            mitigations.append("HIGH SEVERITY - Investigate Soon:")
            mitigations.append("-"*40)
            for change_type, item in high_items:
                mitigations.append(f"  • {item['path']}")
                if change_type == 'new':
                    mitigations.append(f"    Action: Verify if this file is legitimate")
                    mitigations.append(f"    Check: File signature, publisher, creation process")
                elif change_type == 'modified':
                    mitigations.append(f"    Action: Review recent backups")
                    mitigations.append(f"    Check: When and how the file was modified")
                elif change_type == 'deleted':
                    mitigations.append(f"    Action: Restore from backup if needed")
                    mitigations.append(f"    Check: Why the file was removed")
            mitigations.append("")
        
        # General mitigations
        mitigations.append("\nGENERAL SECURITY MEASURES:")
        mitigations.append("-"*40)
        mitigations.append("1. Enable File Integrity Monitoring (FIM)")
        mitigations.append("2. Implement regular backups")
        mitigations.append("3. Review user access and permissions")
        mitigations.append("4. Update antivirus/antimalware software")
        mitigations.append("5. Enable detailed logging")
        mitigations.append("6. Implement principle of least privilege")
        mitigations.append("7. Regular security audits")
        mitigations.append("8. Keep systems patched and updated")
        
        # Suspicious pattern detection
        suspicious_extensions = ['.exe', '.dll', '.vbs', '.ps1', '.sh', '.bin']
        suspicious_locations = ['temp', 'tmp', 'appdata', 'programdata']
        
        for change_type, items_list in [
            ('new', changes['new_files']),
            ('modified', changes['modified_files'])
        ]:
            for item in items_list:
                path = item.get('path', '').lower()
                file_info = item.get('current_info', {})
                ext = file_info.get('extension', '').lower()
                
                if ext in suspicious_extensions and any(loc in path for loc in suspicious_locations):
                    suspicious_patterns.append(f"  • Suspicious executable in temp location: {item['path']}")
        
        if suspicious_patterns:
            mitigations.append("\nSUSPICIOUS PATTERNS DETECTED:")
            mitigations.append("-"*40)
            mitigations.extend(suspicious_patterns)
            mitigations.append("\n  Recommended actions:")
            mitigations.append("  • Scan with antivirus")
            mitigations.append("  • Check running processes")
            mitigations.append("  • Review startup items")
            mitigations.append("  • Isolate system if necessary")
        
        return "\n".join(mitigations)
    
    # ==============================
    # UTILITY FUNCTIONS
    # ==============================
    def _format_size(self, size_bytes):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"


    
    def _print_progress(self, current, total, message, for_pdf=False):
        """Print progress bar with spinning wheels - with PDF compatibility"""
        percent = (current / total) * 100
        bar_length = 40
        filled_length = int(bar_length * current // total)
    
        if for_pdf:
        # Use ASCII characters for PDF (no Unicode)
            bar = '=' * filled_length + '-' * (bar_length - filled_length)
            progress_text = f"{message}: [{bar}] {percent:.1f}% [{current}/{total}]"
        else:
        # Use Unicode for terminal display
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            progress_text = f"{message}: |{bar}| {percent:.1f}% [{current}/{total}]"

        # Add spinning wheels based on progress
            wheels = ['◴', '◷', '◶', '◵']
            wheel_index = current % 4
        
        # Different colors for wheels
            left_wheel = f"{Fore.CYAN}{wheels[wheel_index]}{Style.RESET_ALL}"
            center_wheel = f"{Fore.GREEN}{wheels[(wheel_index + 1) % 4]}{Style.RESET_ALL}"
            right_wheel = f"{Fore.MAGENTA}{wheels[(wheel_index + 2) % 4]}{Style.RESET_ALL}"
        
            progress_text = f"{message}: |{bar}| {percent:.1f}% [{current}/{total}] {left_wheel}{center_wheel}{right_wheel}"
    
    # Center the display
        terminal_width = shutil.get_terminal_size().columns
    
    # Remove ANSI codes for width calculation if present
        if not for_pdf:
            clean_text = progress_text.replace(Fore.CYAN, '').replace(Fore.GREEN, '').replace(Fore.MAGENTA, '').replace(Style.RESET_ALL, '')
            text_width = len(clean_text)
        else:
            text_width = len(progress_text)
    
        padding = max(0, (terminal_width - text_width) // 2)
    
        print(f"\r{' ' * padding}{progress_text}", end='', flush=True)
    
        if current == total:
            print()  # New line when done

    # ==============================
    # MAIN INTERFACE FUNCTIONS
    # ==============================
    def list_all_files(self, category='all'):
        """List all files in the system by category"""
        scan_results = self.scan_system(category)
        
        print(f"\n{Fore.CYAN}{'=' * self.terminal_width}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'SYSTEM FILE INVENTORY'.center(self.terminal_width)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * self.terminal_width}{Style.RESET_ALL}\n")
        
        categories = {
            'critical': scan_results['critical_files'],
            'configs': scan_results['configs'],
            'logs': scan_results['logs'],
            'databases': scan_results['databases'],
            'user': scan_results['files']
        }
        
        if category != 'all':
            categories = {category: categories.get(category, [])}
        
        for cat_name, items in categories.items():
            if items:
                print(f"\n{Fore.YELLOW}{cat_name.upper()} FILES ({len(items)}):{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}")
                
                # Sort by modification time (most recent first)
                for item in sorted(items, key=lambda x: x.get('modified', ''), reverse=True)[:20]:
                    created = datetime.fromisoformat(item['created']).strftime('%Y-%m-%d %H:%M')
                    modified = datetime.fromisoformat(item['modified']).strftime('%Y-%m-%d %H:%M')
                    
                    print(f"{Fore.WHITE}{item['name']}{Style.RESET_ALL}")
                    print(f"  {Fore.CYAN}Path:{Style.RESET_ALL} {item['path']}")
                    print(f"  {Fore.GREEN}Created:{Style.RESET_ALL} {created}")
                    print(f"  {Fore.YELLOW}Modified:{Style.RESET_ALL} {modified}")
                    print(f"  {Fore.MAGENTA}Size:{Style.RESET_ALL} {self._format_size(item['size'])}")
                    if item.get('hash'):
                        print(f"  {Fore.BLUE}Hash:{Style.RESET_ALL} {item['hash'][:16]}...")
                    print()
    
    def full_integrity_check(self):
        """Perform full system integrity check"""
        # Scan system
        scan_results = self.scan_system()
        
        # Check integrity
        changes = self.check_integrity(scan_results)
        
        if changes:
            # Display changes in console
            self._display_changes(changes)
            
            # Generate report
            report_file = self.generate_report(changes, scan_results)
            
            # Display mitigation summary
            self._display_mitigation_summary(changes)
            
            print(f"\n{Fore.GREEN}Full report saved to: {report_file}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}System integrity is intact. No changes detected.{Style.RESET_ALL}")
    
    def _display_changes(self, changes):
        """Display changes in console - without emojis"""
        print(f"\n{Fore.CYAN}{'=' * self.terminal_width}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'INTEGRITY CHECK RESULTS'.center(self.terminal_width)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * self.terminal_width}{Style.RESET_ALL}\n")
        
        # Summary
        print(f"{Fore.YELLOW}Change Summary:{Style.RESET_ALL}")
        print(f"  New Files: {Fore.GREEN if len(changes['new_files'])==0 else Fore.RED}{len(changes['new_files'])}{Style.RESET_ALL}")
        print(f"  Modified: {Fore.GREEN if len(changes['modified_files'])==0 else Fore.RED}{len(changes['modified_files'])}{Style.RESET_ALL}")
        print(f"  Deleted: {Fore.GREEN if len(changes['deleted_files'])==0 else Fore.RED}{len(changes['deleted_files'])}{Style.RESET_ALL}")
        print(f"  Permission Changes: {Fore.GREEN if len(changes['permission_changes'])==0 else Fore.YELLOW}{len(changes['permission_changes'])}{Style.RESET_ALL}")
        
        # Show critical changes
        critical_changes = []
        for change_type in ['new_files', 'modified_files', 'deleted_files']:
            for item in changes[change_type]:
                if item.get('severity') in ['CRITICAL', 'HIGH']:
                    critical_changes.append((change_type, item))
        
        if critical_changes:
            print(f"\n{Fore.RED}{Style.BRIGHT}CRITICAL/HIGH SEVERITY CHANGES:{Style.RESET_ALL}")
            for change_type, item in critical_changes[:5]:
                severity_color = Fore.RED if item.get('severity') == 'CRITICAL' else Fore.YELLOW
                print(f"  {severity_color}[{item.get('severity')}]{Style.RESET_ALL} {item['path']}")
    
    def _display_mitigation_summary(self, changes):
        """Display mitigation summary - without emojis"""
        print(f"\n{Fore.CYAN}{'=' * self.terminal_width}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'MITIGATION SUMMARY'.center(self.terminal_width)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * self.terminal_width}{Style.RESET_ALL}\n")
        
        # Count by severity
        severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for change_type in ['new_files', 'modified_files', 'deleted_files']:
            for item in changes[change_type]:
                severity_counts[item.get('severity', 'LOW')] += 1
        
        print(f"Severity Breakdown:")
        print(f"  [CRITICAL]: {severity_counts['CRITICAL']}")
        print(f"  [HIGH]: {severity_counts['HIGH']}")
        print(f"  [MEDIUM]: {severity_counts['MEDIUM']}")
        print(f"  [LOW]: {severity_counts['LOW']}")
        
        print(f"\n{Fore.YELLOW}Recommended Immediate Actions:{Style.RESET_ALL}")
        if severity_counts['CRITICAL'] > 0:
            print(f"  • {Fore.RED}Investigate CRITICAL changes immediately{Style.RESET_ALL}")
        if severity_counts['HIGH'] > 0:
            print(f"  • {Fore.YELLOW}Review HIGH severity changes soon{Style.RESET_ALL}")


class RealTimeHandler(FileSystemEventHandler):
    """Handles real-time file system events"""
    
    def __init__(self, alert_manager):
        self.alert_manager = alert_manager
        self.suspicious_extensions = ['.exe', '.dll', '.vbs', '.ps1', '.sh', '.bin', '.scr']
        self.suspicious_locations = ['temp', 'tmp', 'appdata', 'programdata', 'downloads']
        
    def on_modified(self, event):
        if not event.is_directory:
            self._check_file(event.src_path, 'MODIFIED')
    
    def on_created(self, event):
        if not event.is_directory:
            self._check_file(event.src_path, 'CREATED')
    
    def on_deleted(self, event):
        if not event.is_directory:
            self._check_file(event.src_path, 'DELETED')
    
    def on_moved(self, event):
        if not event.is_directory:
            self._check_move(event.src_path, event.dest_path)
    
    def _check_file(self, file_path, change_type):
        """Check if file change warrants an alert"""
        severity = self._determine_severity(file_path)
    
    # Get file size if file still exists
        file_size = None
        if os.path.exists(file_path) and change_type != 'DELETED':
            try:
                file_size = os.path.getsize(file_path)
            except:
                pass
    
    # CORRECT: Pass separate arguments instead of a dictionary
        self.alert_manager.add_alert(
            alert_type=change_type,
            path=file_path,
            severity=severity,
            size=file_size
        )
    # ===================
    def _check_move(self, src_path, dest_path):
        """Check if file move is suspicious"""
        severity = self._determine_severity(dest_path)
    
    # Check if moved to/from suspicious location
        src_suspicious = any(loc in src_path.lower() for loc in self.suspicious_locations)
        dest_suspicious = any(loc in dest_path.lower() for loc in self.suspicious_locations)
    
        if src_suspicious or dest_suspicious:
            severity = 'HIGH'
    
    # CORRECT: Pass separate arguments with src_path and dest_path as kwargs
        self.alert_manager.add_alert(
            alert_type='MOVED',
            path=dest_path,
            severity=severity,
            src_path=src_path,
            dest_path=dest_path
        )

    # ===============
    def _determine_severity(self, file_path):
        """Determine alert severity based on file path"""
        file_lower = file_path.lower()
        
        # Critical system files
        critical_paths = ['system32', 'windows\\system', 'etc', 'boot', 'kernel']
        if any(critical in file_lower for critical in critical_paths):
            return 'CRITICAL'
        
        # Sensitive files
        sensitive_paths = ['config', 'password', 'shadow', 'sam', 'database', 'sql']
        if any(sensitive in file_lower for sensitive in sensitive_paths):
            return 'HIGH'
        
        # Suspicious extensions in normal locations
        ext = os.path.splitext(file_lower)[1]
        if ext in self.suspicious_extensions:
            if any(loc in file_lower for loc in self.suspicious_locations):
                return 'HIGH'
            return 'MEDIUM'
        
        # Log files
        if 'log' in file_lower or '.log' in file_lower:
            return 'MEDIUM'
        
        return 'LOW'


class AlertManager:
    """Manages real-time alerts"""
    
    def __init__(self, integrity_monitor):
        self.integrity_monitor = integrity_monitor
        self.alerts = []
        self.running = False
        self.observer = None
        self.monitored_paths = []
        
    def start_monitoring(self, paths=None):
        """Start real-time monitoring"""
        if not WATCHDOG_AVAILABLE:
            print(f"{Fore.RED}Watchdog not installed. Please install with: pip install watchdog{Style.RESET_ALL}")
            return
        
        if self.running:
            print(f"{Fore.YELLOW}Monitoring already running{Style.RESET_ALL}")
            return
        
        # Default paths to monitor
        if paths is None:
            paths = [
                os.path.expanduser('~'),  # User home
                'C:\\' if platform.system().lower() == 'windows' else '/',  # Root
            ]
        
        self.monitored_paths = paths
        self.running = True
        
        # Start observer
        self.observer = Observer()
        handler = RealTimeHandler(self)
        
        for path in paths:
            if os.path.exists(path):
                try:
                    self.observer.schedule(handler, path, recursive=True)
                    print(f"{Fore.GREEN}Monitoring: {path}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Failed to monitor {path}: {e}{Style.RESET_ALL}")
        
        if self.observer:
            self.observer.start()
            print(f"\n{Fore.GREEN}✅ Real-time monitoring started{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Press Ctrl+C in the terminal to stop monitoring{Style.RESET_ALL}\n")
            
            # Start a thread to keep monitoring active
            self._monitor_thread = threading.Thread(target=self._keep_monitoring)
            self._monitor_thread.daemon = True
            self._monitor_thread.start()
    
    def _keep_monitoring(self):
        """Keep monitoring active"""
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
        
        self.running = False
        print(f"{Fore.YELLOW}Real-time monitoring stopped{Style.RESET_ALL}")
    
    def add_alert(self, alert_type, path, severity="LOW", **kwargs):
        """Add a security alert with proper JSON serialization"""
        try:
            alert = {
                'timestamp': datetime.now().isoformat(),
                'type': alert_type,
                'path': str(path),  # Ensure path is string
                'severity': severity,
                'size': kwargs.get('size', None),
                'src_path': str(kwargs.get('src_path', '')),
                'dest_path': str(kwargs.get('dest_path', '')),
            }
    
        # Convert any non-serializable objects
            for key, value in alert.items():
                if hasattr(value, 'isoformat'):  # datetime objects
                    alert[key] = value.isoformat()
                elif isinstance(value, bytes):
                    alert[key] = value.decode('utf-8', errors='replace')
                elif not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                    alert[key] = str(value)
    
        # Add to alerts list
            self.alerts.append(alert)
    
        # Save to file
            self._save_alert(alert)
    
        # Display alert
            self._display_alert(alert)
    
        except Exception as e:
            print(f"Failed to add alert: {e}")
        # Don't raise the exception, just log it
            print(f"Alert data that failed: {alert_type}, {path}")
        # ==============
    # ====end add alerts======
    def _display_alert(self, alert):
        """Display alert in real-time"""
        severity_colors = {
            'CRITICAL': Fore.RED + Back.BLACK + Style.BRIGHT,
            'HIGH': Fore.YELLOW + Style.BRIGHT,
            'MEDIUM': Fore.CYAN,
            'LOW': Fore.GREEN
        }
        
        color = severity_colors.get(alert['severity'], Fore.WHITE)
        
        print(f"\n{color}{'!' * 60}{Style.RESET_ALL}")
        print(f"{color}🔔 SECURITY ALERT [{alert['severity']}]{Style.RESET_ALL}")
        print(f"{color}{'!' * 60}{Style.RESET_ALL}")
        print(f"Time: {alert['timestamp'][:19]}")
        print(f"Type: {alert['type']}")
        
        if alert['type'] == 'MOVED':
            print(f"From: {alert['src_path']}")
            print(f"To: {alert['dest_path']}")
        else:
            print(f"File: {alert['path']}")
        
        if alert.get('file_info'):
            size = alert['file_info'].get('size', 0)
            if size:
                print(f"Size: {self._format_size(size)}")
        
        print(f"{color}{'!' * 60}{Style.RESET_ALL}\n")
    
    def _format_size(self, size_bytes):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def _save_alert(self, alert):
        """Save alert to JSON file with proper escaping"""
        try:
        # Create alerts directory if it doesn't exist
            alerts_dir = os.path.join("data", "alerts")
            os.makedirs(alerts_dir, exist_ok=True)
        
            alerts_file = os.path.join(alerts_dir, "alerts.json")
        
        # Load existing alerts
            alerts = []
            if os.path.exists(alerts_file):
                try:
                    with open(alerts_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip():
                            alerts = json.loads(content)
                except json.JSONDecodeError as e:
                    print(f"Error reading alerts file: {e}")
                # Backup corrupted file
                    backup_file = alerts_file + ".backup"
                    shutil.copy2(alerts_file, backup_file)
                    print(f"Backed up corrupted file to {backup_file}")
                    alerts = []
                except Exception as e:
                    print(f"Error loading alerts: {e}")
                    alerts = []
        
        # Add new alert
            alerts.append(alert)
        
        # Keep only last 1000 alerts
            if len(alerts) > 1000:
                alerts = alerts[-1000:]
        
        # Write back with proper encoding and JSON formatting
            with open(alerts_file, 'w', encoding='utf-8') as f:
                json.dump(alerts, f, indent=2, ensure_ascii=False, default=str)
            
        except Exception as e:
            print(f"Failed to save alert: {e}")
        # Optionally log to a fallback file
            fallback_file = os.path.join("data", "alerts", "alerts_fallback.txt")
            with open(fallback_file, 'a', encoding='utf-8') as f:
                f.write(f"{alert}\n")

            # =======end save alerts======
    def get_alerts(self, severity=None, limit=100):
        """Get recent alerts"""
        if severity:
            return [a for a in self.alerts if a.get('severity') == severity][-limit:]
        return self.alerts[-limit:]


class ForensicAnalyzer:
    """Forensic analyzer for integrity monitoring"""
    def __init__(self, integrity_monitor):
        self.integrity_monitor = integrity_monitor
    
    def analyze_timeline(self, file_path=None, days=7):
        """Analyze timeline of changes"""
        # Load alerts
        alert_file = os.path.join(self.integrity_monitor.report_dir, 'alerts.json')
        timeline = []
        
        if os.path.exists(alert_file):
            with open(alert_file, 'r') as f:
                alerts = json.load(f)
            
            cutoff = datetime.now() - timedelta(days=days)
            
            for alert in alerts:
                alert_time = datetime.fromisoformat(alert['timestamp'])
                if alert_time > cutoff:
                    if file_path is None or file_path in alert.get('path', ''):
                        timeline.append({
                            'time': alert_time,
                            'type': 'alert',
                            'data': alert
                        })
        
        return sorted(timeline, key=lambda x: x['time'])
    
    def generate_forensic_report(self, file_path=None, days=7):
        """Generate forensic report"""
        timeline = self.analyze_timeline(file_path, days)
        
        report_file = os.path.join(self.integrity_monitor.report_dir, 
                                   f'forensic_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        
        with open(report_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write("FORENSIC ANALYSIS REPORT".center(80) + "\n")
            f.write("="*80 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Period: Last {days} days\n")
            if file_path:
                f.write(f"Target: {file_path}\n")
            f.write(f"Total Events: {len(timeline)}\n\n")
            
            if timeline:
                f.write("TIMELINE:\n")
                f.write("-"*40 + "\n")
                for event in timeline:
                    f.write(f"{event['time'].strftime('%Y-%m-%d %H:%M:%S')} - ")
                    f.write(f"[{event['data']['severity']}] {event['data']['type']}: ")
                    if 'path' in event['data']:
                        f.write(f"{event['data']['path']}\n")
                    else:
                        f.write(f"{event['data'].get('src_path', 'Unknown')}\n")
        
        return report_file


class AutoRemediation:
    """Automatically handle integrity violations"""
    
    def __init__(self, integrity_monitor):
        self.integrity_monitor = integrity_monitor
        self.remediation_log = os.path.join(integrity_monitor.report_dir, 'remediation_log.json')
        self.policies = self._load_policies()
    
    def _load_policies(self):
        """Load remediation policies"""
        policy_file = os.path.join(self.integrity_monitor.report_dir, 'remediation_policies.json')
        
        default_policies = {
            'critical_files': {
                'action': 'alert_and_restore',
                'backup_source': 'baseline',
                'notify': True
            },
            'suspicious_executables': {
                'action': 'quarantine',
                'notify': True
            },
            'config_changes': {
                'action': 'alert',
                'notify': True
            },
            'unauthorized_access': {
                'action': 'block_and_alert',
                'notify': True
            }
        }
        
        if os.path.exists(policy_file):
            with open(policy_file, 'r') as f:
                return json.load(f)
        else:
            with open(policy_file, 'w') as f:
                json.dump(default_policies, f, indent=2)
            return default_policies
    
    def handle_violation(self, violation):
        """Handle integrity violation based on policies"""
        action = self._determine_action(violation)
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'violation': violation,
            'action_taken': action,
            'success': False
        }
        
        if action == 'quarantine':
            result['success'] = self._quarantine_violation(violation)
        elif action == 'restore':
            result['success'] = self._restore_from_backup(violation)
        elif action == 'alert':
            result['success'] = True  # Alert already sent
        
        # Log remediation action
        self._log_remediation(result)
        
        return result
    
    def _determine_action(self, violation):
        """Determine appropriate action for violation"""
        path = violation.get('path', '')
        
        if any(critical in path.lower() for critical in ['system32', 'etc', 'boot']):
            return self.policies['critical_files']['action']
        elif any(suspicious in path.lower() for suspicious in ['.exe', '.dll', '.scr']):
            if 'temp' in path.lower() or 'download' in path.lower():
                return self.policies['suspicious_executables']['action']
        elif 'config' in path.lower():
            return self.policies['config_changes']['action']
        
        return 'alert'
    
    def _quarantine_violation(self, violation):
        """Quarantine violating file"""
        try:
            file_path = violation.get('path')
            if not os.path.exists(file_path):
                return False
            
            quarantine_dir = os.path.join(self.integrity_monitor.report_dir, 'auto_quarantine')
            os.makedirs(quarantine_dir, exist_ok=True)
            
            filename = os.path.basename(file_path)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            quarantine_path = os.path.join(quarantine_dir, f"{timestamp}_{filename}")
            
            shutil.move(file_path, quarantine_path)
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Auto-quarantine failed: {e}{Style.RESET_ALL}")
            return False
    
    def _restore_from_backup(self, violation):
        """Restore file from backup"""
        try:
            file_path = violation.get('path')
            
            # Check if we have a backup in baseline
            baseline = self.integrity_monitor._load_baseline()
            if not baseline:
                return False
            
            # Find file in baseline
            all_files = []
            for category in ['files', 'configs', 'critical_files']:
                all_files.extend(baseline.get(category, []))
            
            baseline_file = next((f for f in all_files if f['path'] == file_path), None)
            
            if not baseline_file:
                return False
            
            # In a real implementation, you'd restore from actual backup
            # This is a placeholder
            print(f"{Fore.YELLOW}Would restore {file_path} from backup{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Auto-restore failed: {e}{Style.RESET_ALL}")
            return False
    
    def _log_remediation(self, result):
        """Log remediation action"""
        try:
            if os.path.exists(self.remediation_log):
                with open(self.remediation_log, 'r') as f:
                    log = json.load(f)
            else:
                log = []
            
            log.append(result)
            
            # Keep last 1000 entries
            if len(log) > 1000:
                log = log[-1000:]
            
            with open(self.remediation_log, 'w') as f:
                json.dump(log, f, indent=2)
                
        except Exception as e:
            print(f"{Fore.RED}Failed to log remediation: {e}{Style.RESET_ALL}")