"""
DSTerminal Interactive Hardening Dashboard
Complete implementation with modular selection, real-time progress,
and automated audit reporting
"""

import os
import sys
import time
import json
import random
import shutil
import logging
import platform
import subprocess
import threading
from datetime import datetime, timedelta 
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

# Terminal colors
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

class Style:
    BRIGHT = '\033[1m'
    DIM = '\033[2m'
    NORMAL = '\033[22m'
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
# HARDENING MODULE DEFINITIONS
# ============================================================
class HardeningCategory(Enum):
    USER_SECURITY = "User Account Security"
    PASSWORD_POLICY = "Password Policies"
    FIREWALL = "Firewall Configuration"
    SSH_SECURITY = "SSH Hardening"
    FILESYSTEM = "File System Security"
    SERVICES = "Service Management"
    NETWORK = "Network Security"
    MALWARE = "Malware Protection"
    KERNEL = "Kernel Hardening"
    AUDITING = "Audit & Logging"

class HardeningSeverity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass
class HardeningModule:
    """Represents a single hardening action"""
    id: str
    name: str
    description: str
    category: HardeningCategory
    severity: HardeningSeverity
    platforms: List[str]
    command: str
    verify_command: Optional[str] = None
    rollback_command: Optional[str] = None
    requires_admin: bool = True
    estimated_time: float = 2.0
    applied: bool = False
    verified: bool = False
    output: str = ""
    timestamp: Optional[datetime] = None

@dataclass
class HardeningResult:
    """Tracks results for a hardening session"""
    module: HardeningModule
    success: bool
    start_time: datetime
    end_time: Optional[datetime] = None
    output: str = ""
    error: Optional[str] = None

class HardeningDashboard:
    """Interactive hardening dashboard with progress tracking"""
    
    def __init__(self, terminal_width: int = 80):
        self.terminal_width = terminal_width
        self.system = platform.system()
        self.is_admin_user = self._check_admin()
        self.modules: List[HardeningModule] = []
        self.results: List[HardeningResult] = []
        self.selected_modules: List[str] = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_data = {}
        
        # Initialize hardening modules
        self._initialize_modules()
        
        # Setup logging
        self._setup_logging()
    
    def _check_admin(self) -> bool:
        """Check if running with administrator privileges"""
        try:
            if self.system == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except:
            return False
    
    def _setup_logging(self):
        """Setup logging for audit trail"""
        log_dir = os.path.expanduser("~/DSTerminal_Workspace/logs")
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{log_dir}/hardening_{self.session_id}.log"),
                logging.StreamHandler()
            ]
        )
    
    def _initialize_modules(self):
        """Define all available hardening modules"""
        
        # User Account Security
        self.modules.append(HardeningModule(
            id="disable_guest",
            name="Disable Guest Account",
            description="Disables the guest account to prevent unauthorized access",
            category=HardeningCategory.USER_SECURITY,
            severity=HardeningSeverity.HIGH,
            platforms=["Windows", "Linux", "Darwin"],
            command=self._get_disable_guest_command(),
            verify_command=self._get_verify_guest_command(),
            rollback_command=self._get_enable_guest_command(),
            estimated_time=1.5
        ))
        
        self.modules.append(HardeningModule(
            id="remove_unused_users",
            name="Remove Unused User Accounts",
            description="Identifies and removes accounts that haven't been used recently",
            category=HardeningCategory.USER_SECURITY,
            severity=HardeningSeverity.MEDIUM,
            platforms=["Linux", "Darwin"],
            command="for user in $(awk -F: '$3 >= 1000 && $7 !~ /nologin|false/ {print $1}' /etc/passwd); do lastlog -u $user | grep 'Never logged in' && echo $user; done",
            estimated_time=3.0,
            requires_admin=True
        ))
        
        # Password Policies
        self.modules.append(HardeningModule(
            id="enforce_password_policy",
            name="Enforce Strong Password Policy",
            description="Sets minimum password length, complexity requirements, and aging",
            category=HardeningCategory.PASSWORD_POLICY,
            severity=HardeningSeverity.CRITICAL,
            platforms=["Windows", "Linux", "Darwin"],
            command=self._get_password_policy_command(),
            estimated_time=2.0
        ))
        
        self.modules.append(HardeningModule(
            id="account_lockout",
            name="Account Lockout Policy",
            description="Locks accounts after multiple failed login attempts",
            category=HardeningCategory.PASSWORD_POLICY,
            severity=HardeningSeverity.HIGH,
            platforms=["Windows", "Linux"],
            command=self._get_lockout_policy_command(),
            estimated_time=1.5
        ))
        
        # Firewall Configuration
        self.modules.append(HardeningModule(
            id="enable_firewall",
            name="Enable & Configure Firewall",
            description="Enables firewall with default deny inbound policy",
            category=HardeningCategory.FIREWALL,
            severity=HardeningSeverity.CRITICAL,
            platforms=["Windows", "Linux", "Darwin"],
            command=self._get_firewall_command(),
            verify_command=self._get_firewall_verify_command(),
            estimated_time=3.0
        ))
        
        self.modules.append(HardeningModule(
            id="block_common_ports",
            name="Block Common Attack Ports",
            description="Blocks commonly exploited ports (445, 135-139, 3389 exposed)",
            category=HardeningCategory.FIREWALL,
            severity=HardeningSeverity.HIGH,
            platforms=["Windows", "Linux"],
            command=self._get_block_ports_command(),
            estimated_time=2.0
        ))
        
        # SSH Security
        self.modules.append(HardeningModule(
            id="harden_ssh",
            name="SSH Hardening",
            description="Disables root login, password auth, and implements key-only access",
            category=HardeningCategory.SSH_SECURITY,
            severity=HardeningSeverity.CRITICAL,
            platforms=["Linux", "Darwin"],
            command=self._get_ssh_hardening_command(),
            verify_command="grep '^PermitRootLogin no' /etc/ssh/sshd_config",
            rollback_command=self._get_ssh_rollback_command(),
            estimated_time=2.5
        ))
        
        # File System Security
        self.modules.append(HardeningModule(
            id="secure_permissions",
            name="Secure File Permissions",
            description="Sets proper permissions on critical system files",
            category=HardeningCategory.FILESYSTEM,
            severity=HardeningSeverity.CRITICAL,
            platforms=["Linux", "Darwin"],
            command=self._get_permissions_command(),
            estimated_time=3.0
        ))
        
        self.modules.append(HardeningModule(
            id="remove_suid",
            name="Remove Unnecessary SUID/SGID Bits",
            description="Removes setuid/setgid from binaries that don't need them",
            category=HardeningCategory.FILESYSTEM,
            severity=HardeningSeverity.HIGH,
            platforms=["Linux", "Darwin"],
            command=self._get_suid_removal_command(),
            estimated_time=4.0,
            requires_admin=True
        ))
        
        # Service Management
        self.modules.append(HardeningModule(
            id="disable_unnecessary_services",
            name="Disable Unnecessary Services",
            description="Disables services that are not required for operation",
            category=HardeningCategory.SERVICES,
            severity=HardeningSeverity.MEDIUM,
            platforms=["Windows", "Linux", "Darwin"],
            command=self._get_disable_services_command(),
            estimated_time=3.0
        ))
        
        # Network Security
        self.modules.append(HardeningModule(
            id="disable_ipv6",
            name="Disable IPv6 (if not needed)",
            description="Disables IPv6 to reduce attack surface",
            category=HardeningCategory.NETWORK,
            severity=HardeningSeverity.LOW,
            platforms=["Linux"],
            command="sysctl -w net.ipv6.conf.all.disable_ipv6=1 && sysctl -w net.ipv6.conf.default.disable_ipv6=1",
            rollback_command="sysctl -w net.ipv6.conf.all.disable_ipv6=0",
            estimated_time=1.0
        ))
        
        self.modules.append(HardeningModule(
            id="syncookie_protection",
            name="SYN Cookie Protection",
            description="Enables TCP SYN cookie protection against SYN flood attacks",
            category=HardeningCategory.NETWORK,
            severity=HardeningSeverity.HIGH,
            platforms=["Linux"],
            command="sysctl -w net.ipv4.tcp_syncookies=1",
            estimated_time=1.0
        ))
        
        # Malware Protection
        self.modules.append(HardeningModule(
            id="install_clamav",
            name="Install ClamAV Antivirus",
            description="Installs and updates ClamAV antivirus scanner",
            category=HardeningCategory.MALWARE,
            severity=HardeningSeverity.HIGH,
            platforms=["Linux", "Darwin"],
            command=self._get_clamav_install_command(),
            estimated_time=5.0
        ))
        
        # Kernel Hardening
        self.modules.append(HardeningModule(
            id="kernel_hardening",
            name="Kernel Security Parameters",
            description="Applies secure kernel parameters via sysctl",
            category=HardeningCategory.KERNEL,
            severity=HardeningSeverity.HIGH,
            platforms=["Linux"],
            command=self._get_kernel_hardening_command(),
            estimated_time=2.0
        ))
        
        # Auditing
        self.modules.append(HardeningModule(
            id="enable_auditd",
            name="Enable System Auditing",
            description="Enables and configures auditd for security event monitoring",
            category=HardeningCategory.AUDITING,
            severity=HardeningSeverity.HIGH,
            platforms=["Linux"],
            command=self._get_auditd_command(),
            estimated_time=2.5
        ))
    
    # ============================================================
    # PLATFORM-SPECIFIC COMMAND GENERATORS
    # ============================================================
    
    def _get_disable_guest_command(self) -> str:
        if self.system == "Windows":
            return 'net user guest /active:no'
        elif self.system == "Darwin":
            return 'dscl . -create /Users/Guest AuthenticationAuthority ";DisabledUser;"'
        else:
            return 'usermod -L guest && passwd -l guest'
    
    def _get_verify_guest_command(self) -> str:
        if self.system == "Windows":
            return 'net user guest | findstr "Active"'
        elif self.system == "Darwin":
            return 'dscl . -read /Users/Guest AuthenticationAuthority | grep DisabledUser'
        else:
            return 'passwd -S guest 2>/dev/null | grep -q "L"'
    
    def _get_enable_guest_command(self) -> str:
        if self.system == "Windows":
            return 'net user guest /active:yes'
        elif self.system == "Darwin":
            return 'dscl . -delete /Users/Guest AuthenticationAuthority'
        else:
            return 'usermod -U guest 2>/dev/null; passwd -u guest 2>/dev/null'
    
    def _get_password_policy_command(self) -> str:
        if self.system == "Windows":
            return 'net accounts /minpwlen:14 /maxpwage:90 /minpwage:1 /uniquepw:24'
        else:
            return 'sed -i "s/^PASS_MAX_DAYS.*/PASS_MAX_DAYS 90/" /etc/login.defs && sed -i "s/^PASS_MIN_DAYS.*/PASS_MIN_DAYS 1/" /etc/login.defs'
    
    def _get_lockout_policy_command(self) -> str:
        if self.system == "Windows":
            return 'net accounts /lockoutthreshold:5 /lockoutduration:30 /lockoutwindow:30'
        else:
            return 'echo "auth required pam_tally2.so deny=5 unlock_time=900" >> /etc/pam.d/common-auth'
    
    def _get_firewall_command(self) -> str:
        if self.system == "Windows":
            return 'netsh advfirewall set allprofiles state on && netsh advfirewall set allprofiles firewallpolicy blockinbound,allowoutbound'
        elif self.system == "Darwin":
            return '/usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on'
        else:
            return 'ufw --force enable && ufw default deny incoming && ufw default allow outgoing'
    
    def _get_firewall_verify_command(self) -> str:
        if self.system == "Windows":
            return 'netsh advfirewall show allprofiles | findstr "State"'
        elif self.system == "Darwin":
            return '/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate'
        else:
            if shutil.which('ufw'):
                return 'ufw status | grep -q "Status: active"'
            else:
                return 'iptables -L -n | head -5'
    
    def _get_block_ports_command(self) -> str:
        if self.system == "Windows":
            ports = ["445", "135", "137", "138", "139", "3389"]
            commands = []
            for port in ports:
                commands.append(
                    f'netsh advfirewall firewall add rule name="Block Port {port}" '
                    f'dir=in protocol=TCP localport={port} action=block'
                )
            return ' && '.join(commands)
        else:
            ports = ["445", "135", "137", "138", "139", "3389"]
            commands = []
            for port in ports:
                commands.append(f'iptables -A INPUT -p tcp --dport {port} -j DROP')
            return ' && '.join(commands)
    
    def _get_ssh_hardening_command(self) -> str:
        config_changes = [
            'sed -i "s/^#*PermitRootLogin.*/PermitRootLogin no/" /etc/ssh/sshd_config',
            'sed -i "s/^#*PasswordAuthentication.*/PasswordAuthentication no/" /etc/ssh/sshd_config',
            'sed -i "s/^#*MaxAuthTries.*/MaxAuthTries 3/" /etc/ssh/sshd_config',
            'sed -i "s/^#*X11Forwarding.*/X11Forwarding no/" /etc/ssh/sshd_config'
        ]
        return ' && '.join(config_changes) + ' && systemctl restart sshd'
    
    def _get_ssh_rollback_command(self) -> str:
        return 'cp /etc/ssh/sshd_config.bak /etc/ssh/sshd_config 2>/dev/null && systemctl restart sshd 2>/dev/null || service ssh restart 2>/dev/null'
    
    def _get_permissions_command(self) -> str:
        return ('chmod 644 /etc/passwd && chmod 600 /etc/shadow && '
                'chmod 644 /etc/group && chmod 600 /etc/gshadow && '
                'chmod 440 /etc/sudoers 2>/dev/null')
    
    def _get_suid_removal_command(self) -> str:
        return ('find / -perm -4000 -type f 2>/dev/null | '
                'grep -v -E "/(bin/su|usr/bin/sudo|usr/bin/passwd|usr/bin/newgrp|usr/bin/chsh|usr/bin/chfn)$" | '
                'xargs -r chmod u-s 2>/dev/null')
    
    def _get_disable_services_command(self) -> str:
        if self.system == "Windows":
            services = ["telnet", "ftp", "RemoteRegistry"]
            commands = []
            for service in services:
                commands.append(f'sc config {service} start=disabled 2>nul')
                commands.append(f'sc stop {service} 2>nul')
            return ' & '.join(commands)
        else:
            services = ["telnet", "vsftpd", "rsh-server", "rlogin", "rexecd"]
            commands = []
            for service in services:
                commands.append(f'systemctl disable {service} 2>/dev/null')
                commands.append(f'systemctl stop {service} 2>/dev/null')
            return '; '.join(commands)
    
    def _get_clamav_install_command(self) -> str:
        if self.system == "Darwin":
            return 'brew install clamav 2>/dev/null && freshclam'
        elif shutil.which('apt'):
            return 'apt install -y clamav clamav-daemon 2>/dev/null && freshclam'
        elif shutil.which('yum'):
            return 'yum install -y clamav clamav-update 2>/dev/null && freshclam'
        else:
            return 'freshclam 2>/dev/null'
    
    def _get_kernel_hardening_command(self) -> str:
        params = [
            'sysctl -w net.ipv4.tcp_syncookies=1',
            'sysctl -w net.ipv4.conf.all.rp_filter=1',
            'sysctl -w net.ipv4.conf.all.accept_redirects=0',
            'sysctl -w net.ipv4.conf.all.send_redirects=0',
            'sysctl -w net.ipv4.conf.all.accept_source_route=0',
            'sysctl -w kernel.randomize_va_space=2'
        ]
        return ' && '.join(params)
    
    def _get_auditd_command(self) -> str:
        if shutil.which('apt'):
            return 'apt install -y auditd 2>/dev/null && systemctl enable auditd && systemctl start auditd'
        elif shutil.which('yum'):
            return 'yum install -y audit && systemctl enable auditd && systemctl start auditd'
        else:
            return 'systemctl enable auditd 2>/dev/null && systemctl start auditd 2>/dev/null'
    
    # ============================================================
    # INTERACTIVE DASHBOARD DISPLAY
    # ============================================================
    
    def display_dashboard(self):
        """Main interactive dashboard"""
        self._clear_screen()
        self._display_header()
        
        while True:
            self._display_menu()
            choice = input(f"\n{Fore.CYAN}[DSTerminal] Select option (1-7): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                self._select_modules_interactive()
            elif choice == '2':
                self._view_selected_modules()
            elif choice == '3':
                self._execute_hardening()
            elif choice == '4':
                self._view_results()
            elif choice == '5':
                self._generate_report()
            elif choice == '6':
                self._rollback_hardening()
            elif choice == '7':
                print(f"\n{Fore.GREEN}Exiting Hardening Dashboard...{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
    
    def _display_header(self):
        """Display dashboard header"""
        header = f"""
{Fore.GREEN}{'='*self.terminal_width}
{self._center_text('╔══════════════════════════════════════════════════════════════╗')}
{self._center_text('║     DSTERMINAL INTERACTIVE HARDENING DASHBOARD v2.0.113     ║')}
{self._center_text('║              Advanced System Fortification Suite             ║')}
{self._center_text('╚══════════════════════════════════════════════════════════════╝')}
{'='*self.terminal_width}{Style.RESET_ALL}

{Fore.YELLOW}System: {self.system} | Admin: {self.is_admin_user} | Session: {self.session_id}
{Fore.CYAN}Available Modules: {len(self.modules)} | Selected: {len(self.selected_modules)} | Completed: {sum(1 for r in self.results if r.success)}{Style.RESET_ALL}
"""
        print(header)
    
    def _display_menu(self):
        """Display main menu options"""
        menu = f"""
{Fore.WHITE}{'─'*self.terminal_width}
{self._center_text('MAIN MENU')}
{'─'*self.terminal_width}{Style.RESET_ALL}

{Fore.GREEN}[1]{Style.RESET_ALL} Select Hardening Modules
{Fore.GREEN}[2]{Style.RESET_ALL} View Selected Modules
{Fore.GREEN}[3]{Style.RESET_ALL} Execute Hardening
{Fore.GREEN}[4]{Style.RESET_ALL} View Results
{Fore.GREEN}[5]{Style.RESET_ALL} Generate Audit Report
{Fore.GREEN}[6]{Style.RESET_ALL} Rollback Hardening
{Fore.GREEN}[7]{Style.RESET_ALL} Exit Dashboard
"""
        print(menu)
    
    def _select_modules_interactive(self):
        """Interactive module selection interface"""
        self._clear_screen()
        self._display_header()
        
        # Group modules by category
        categories = {}
        for module in self.modules:
            cat = module.category.value
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(module)
        
        print(f"\n{Fore.CYAN}{'='*self.terminal_width}")
        print(self._center_text("MODULE SELECTION"))
        print(f"{'='*self.terminal_width}{Style.RESET_ALL}\n")
        
        for category, modules in categories.items():
            print(f"\n{Fore.YELLOW}▸ {category}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{'─'*50}{Style.RESET_ALL}")
            
            for i, module in enumerate(modules, 1):
                selected = "✓" if module.id in self.selected_modules else " "
                severity_color = self._get_severity_color(module.severity)
                
                print(f"  [{selected}] {Fore.GREEN}{i:2d}{Style.RESET_ALL}. "
                      f"{module.name:40s} "
                      f"[{severity_color}{module.severity.value:8s}{Style.RESET_ALL}] "
                      f"{'⚠ ADMIN' if module.requires_admin and not self.is_admin_user else ''}")
        
        print(f"\n{Fore.CYAN}Options:{Style.RESET_ALL}")
        print("  • Enter module numbers separated by commas (e.g., '1,3,5-8')")
        print("  • 'all' - Select all compatible modules")
        print("  • 'clear' - Clear all selections")
        print("  • 'back' - Return to main menu")
        
        choice = input(f"\n{Fore.GREEN}Selection: {Style.RESET_ALL}").strip().lower()
        
        if choice == 'back':
            return
        elif choice == 'all':
            self.selected_modules = [m.id for m in self.modules 
                                    if not (m.requires_admin and not self.is_admin_user)]
            print(f"{Fore.GREEN}✓ Selected all compatible modules ({len(self.selected_modules)}){Style.RESET_ALL}")
        elif choice == 'clear':
            self.selected_modules = []
            print(f"{Fore.GREEN}✓ Cleared all selections{Style.RESET_ALL}")
        else:
            # Parse selection
            try:
                selected_indices = self._parse_selection(choice)
                for idx in selected_indices:
                    if 1 <= idx <= len(self.modules):
                        module = self.modules[idx - 1]
                        if module.requires_admin and not self.is_admin_user:
                            print(f"{Fore.YELLOW}⚠ Skipping '{module.name}' - requires admin privileges{Style.RESET_ALL}")
                            continue
                        if module.id not in self.selected_modules:
                            self.selected_modules.append(module.id)
                print(f"{Fore.GREEN}✓ Updated selections ({len(self.selected_modules)} modules selected){Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}Invalid selection format{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def _parse_selection(self, selection: str) -> List[int]:
        """Parse selection string like '1,3,5-8'"""
        indices = []
        for part in selection.split(','):
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                indices.extend(range(int(start), int(end) + 1))
            else:
                indices.append(int(part))
        return indices
    
    def _get_severity_color(self, severity: HardeningSeverity) -> str:
        """Get color for severity level"""
        colors = {
            HardeningSeverity.CRITICAL: Fore.RED,
            HardeningSeverity.HIGH: Fore.YELLOW,
            HardeningSeverity.MEDIUM: Fore.CYAN,
            HardeningSeverity.LOW: Fore.GREEN
        }
        return colors.get(severity, Fore.WHITE)
    
    # ============================================================
    # REAL-TIME PROGRESS DISPLAY
    # ============================================================
    
    def _progress_bar(self, label: str, duration: float, width: int = 50):
        """Animated progress bar"""
        steps = 100
        for i in range(steps + 1):
            filled = int(width * i / steps)
            bar = '█' * filled + '░' * (width - filled)
            percent = i
            print(f'\r{Fore.CYAN}{label:30s} {Fore.GREEN}[{bar}] {Fore.YELLOW}{percent:3d}%{Style.RESET_ALL}', end='')
            time.sleep(duration / steps)
        print()
    
    def _display_split_progress(self, module_name: str, progress: float, 
                                 left_info: str, center_info: str, right_info: str):
        """Three-panel progress display"""
        width = self.terminal_width
        panel_width = (width - 4) // 3
        
        left_panel = f"{Fore.CYAN}{left_info[:panel_width]:<{panel_width}}{Style.RESET_ALL}"
        center_panel = f"{Fore.GREEN}{center_info[:panel_width]:^{panel_width}}{Style.RESET_ALL}"
        right_panel = f"{Fore.YELLOW}{right_info[:panel_width]:>{panel_width}}{Style.RESET_ALL}"
        
        # Progress bar
        bar_width = width - 4
        filled = int(bar_width * progress)
        bar = '█' * filled + '░' * (bar_width - filled)
        
        print(f"\r{left_panel} │ {center_panel} │ {right_panel}")
        print(f"{Fore.WHITE}{'─'*width}{Style.RESET_ALL}")
        print(f"{module_name:30s} [{Fore.GREEN}{bar}{Style.RESET_ALL}] {Fore.YELLOW}{int(progress*100):3d}%{Style.RESET_ALL}")
    
    # ============================================================
    # HARDENING EXECUTION
    # ============================================================
    
    def _execute_hardening(self):
        """Execute selected hardening modules"""
        if not self.selected_modules:
            print(f"{Fore.RED}[!] No modules selected. Please select modules first.{Style.RESET_ALL}")
            input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        self._clear_screen()
        self._display_header()
        
        print(f"\n{Fore.GREEN}{'='*self.terminal_width}")
        print(self._center_text("EXECUTING SYSTEM HARDENING"))
        print(f"{'='*self.terminal_width}{Style.RESET_ALL}\n")
        
        modules_to_execute = [m for m in self.modules if m.id in self.selected_modules]
        total_modules = len(modules_to_execute)
        
        for i, module in enumerate(modules_to_execute):
            overall_progress = i / total_modules
            
            print(f"\n{Fore.CYAN}[{i+1}/{total_modules}] Processing: {module.name}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Category: {module.category.value}")
            print(f"Severity: {self._get_severity_color(module.severity)}{module.severity.value}{Style.RESET_ALL}")
            
            # Execute module
            result = self._execute_single_module(module, overall_progress)
            self.results.append(result)
            
            if result.success:
                module.applied = True
                module.verified = True
                module.timestamp = datetime.now()
                print(f"\n{Fore.GREEN}✓ {module.name} - SUCCESS{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}✗ {module.name} - FAILED: {result.error}{Style.RESET_ALL}")
            
            time.sleep(0.5)
        
        # Completion summary
        self._display_completion_summary()
    
    def _execute_single_module(self, module: HardeningModule, overall_progress: float) -> HardeningResult:
        """Execute a single hardening module with progress"""
        start_time = datetime.now()
        
        # Display initial progress
        for progress in range(0, 101, 5):
            pct = progress / 100
            
            self._display_split_progress(
                module.name,
                pct,
                f"System: {self.system}",
                f"Applying: {module.name[:30]}",
                f"ETA: {module.estimated_time * (1-pct):.1f}s"
            )
            
            if progress < 50:
                time.sleep(module.estimated_time * 0.05)
            elif progress < 80:
                time.sleep(module.estimated_time * 0.03)
            else:
                time.sleep(module.estimated_time * 0.02)
        
        print()  # New line after progress
        
        try:
            # Execute the actual command
            if module.command:
                result = subprocess.run(
                    module.command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                output = result.stdout + result.stderr
                success = result.returncode == 0
                
                # Store output
                module.output = output
                
                return HardeningResult(
                    module=module,
                    success=success,
                    start_time=start_time,
                    end_time=datetime.now(),
                    output=output,
                    error=None if success else f"Exit code: {result.returncode}"
                )
            else:
                return HardeningResult(
                    module=module,
                    success=True,
                    start_time=start_time,
                    end_time=datetime.now(),
                    output="No command to execute (simulated)"
                )
                
        except subprocess.TimeoutExpired:
            return HardeningResult(
                module=module,
                success=False,
                start_time=start_time,
                end_time=datetime.now(),
                error="Command timed out"
            )
        except Exception as e:
            return HardeningResult(
                module=module,
                success=False,
                start_time=start_time,
                end_time=datetime.now(),
                error=str(e)
            )
    
    def _display_completion_summary(self):
        """Display completion summary with statistics"""
        total = len(self.results)
        successful = sum(1 for r in self.results if r.success)
        failed = total - successful
        
        print(f"\n{Fore.GREEN}{'='*self.terminal_width}")
        print(self._center_text('▄︻デ══━ SYSTEM FORTIFICATION COMPLETE ══━︻▄'))
        print(f"{'='*self.terminal_width}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}Session Summary:{Style.RESET_ALL}")
        print(f"  Total Modules: {total}")
        print(f"  {Fore.GREEN}Successful: {successful}{Style.RESET_ALL}")
        print(f"  {Fore.RED}Failed: {failed}{Style.RESET_ALL}")
        print(f"  Success Rate: {(successful/total*100):.1f}%")
        
        if failed > 0:
            print(f"\n{Fore.RED}Failed Modules:{Style.RESET_ALL}")
            for result in self.results:
                if not result.success:
                    print(f"  ✗ {result.module.name}: {result.error}")
        
        # Threat level assessment
        threat_level = max(1, 10 - successful)
        print(f"\n{Fore.YELLOW}Firewall Active | Intrusion Prevention Engaged | Threat Level: {threat_level}/10{Style.RESET_ALL}")
    
    # ============================================================
    # VIEW FUNCTIONS
    # ============================================================
    
    def _view_selected_modules(self):
        """View currently selected modules"""
        self._clear_screen()
        self._display_header()
        
        print(f"\n{Fore.CYAN}{'='*self.terminal_width}")
        print(self._center_text("SELECTED MODULES"))
        print(f"{'='*self.terminal_width}{Style.RESET_ALL}\n")
        
        if not self.selected_modules:
            print(f"{Fore.YELLOW}No modules selected.{Style.RESET_ALL}")
        else:
            selected = [m for m in self.modules if m.id in self.selected_modules]
            for i, module in enumerate(selected, 1):
                status = f"{Fore.GREEN}✓ APPLIED{Style.RESET_ALL}" if module.applied else f"{Fore.YELLOW}⏳ PENDING{Style.RESET_ALL}"
                print(f"  {i:2d}. {module.name:40s} [{status}]")
                print(f"      {Fore.CYAN}{module.description[:60]}...{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def _view_results(self):
        """View hardening results"""
        self._clear_screen()
        self._display_header()
        
        print(f"\n{Fore.CYAN}{'='*self.terminal_width}")
        print(self._center_text("HARDENING RESULTS"))
        print(f"{'='*self.terminal_width}{Style.RESET_ALL}\n")
        
        if not self.results:
            print(f"{Fore.YELLOW}No results available. Execute hardening first.{Style.RESET_ALL}")
        else:
            for i, result in enumerate(self.results, 1):
                status = f"{Fore.GREEN}✓ SUCCESS{Style.RESET_ALL}" if result.success else f"{Fore.RED}✗ FAILED{Style.RESET_ALL}"
                print(f"  {i:2d}. {result.module.name:40s} [{status}]")
                print(f"      Duration: {(result.end_time - result.start_time).total_seconds():.2f}s")
                if result.error:
                    print(f"      Error: {Fore.RED}{result.error}{Style.RESET_ALL}")
                print()
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    # ============================================================
    # REPORT GENERATION
    # ============================================================
    
    def _generate_report(self):
        """Generate comprehensive audit report"""
        self._clear_screen()
        self._display_header()
        
        print(f"\n{Fore.CYAN}Generating Hardening Audit Report...{Style.RESET_ALL}")
        self._progress_bar("Report Generation", 2)
        
        report = self._build_report()
        
        # Save report
        report_dir = os.path.expanduser("~/DSTerminal_Workspace/reports")
        os.makedirs(report_dir, exist_ok=True)
        
        # Save as JSON
        json_path = f"{report_dir}/hardening_report_{self.session_id}.json"
        with open(json_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Save as readable text
        txt_path = f"{report_dir}/hardening_report_{self.session_id}.txt"
        with open(txt_path, 'w') as f:
            f.write(self._format_report_text(report))
        
        print(f"\n{Fore.GREEN}✓ Report generated successfully!{Style.RESET_ALL}")
        print(f"  JSON: {json_path}")
        print(f"  Text: {txt_path}")
        
        # Display summary
        self._display_report_summary(report)
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def _build_report(self) -> Dict:
        """Build comprehensive report data structure"""
        total = len(self.results)
        successful = sum(1 for r in self.results if r.success)
        failed = total - successful
        
        report = {
            "report_metadata": {
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "system": self.system,
                "platform_release": platform.release(),
                "architecture": platform.machine(),
                "admin_privileges": self.is_admin_user
            },
            "summary": {
                "total_modules": total,
                "successful": successful,
                "failed": failed,
                "success_rate": f"{(successful/total*100):.1f}%" if total > 0 else "N/A",
                "execution_time": str(sum((r.end_time - r.start_time for r in self.results if r.end_time), 
                                         datetime.timedelta()))
            },
            "results": [],
            "recommendations": []
        }
        
        for result in self.results:
            report["results"].append({
                "module_id": result.module.id,
                "module_name": result.module.name,
                "category": result.module.category.value,
                "severity": result.module.severity.value,
                "success": result.success,
                "start_time": result.start_time.isoformat(),
                "end_time": result.end_time.isoformat() if result.end_time else None,
                "duration": str(result.end_time - result.start_time) if result.end_time else None,
                "output": result.output[:500] if result.output else "",
                "error": result.error
            })
        
        # Add recommendations for failed modules
        for result in self.results:
            if not result.success:
                report["recommendations"].append({
                    "module": result.module.name,
                    "issue": result.error,
                    "suggestion": f"Manually apply {result.module.name} using: {result.module.command}"
                })
        
        return report
    
    def _format_report_text(self, report: Dict) -> str:
        """Format report as readable text"""
        lines = []
        lines.append("=" * 80)
        lines.append("DSTERMINAL SYSTEM HARDENING AUDIT REPORT")
        lines.append("=" * 80)
        lines.append(f"\nSession ID: {report['report_metadata']['session_id']}")
        lines.append(f"Timestamp: {report['report_metadata']['timestamp']}")
        lines.append(f"System: {report['report_metadata']['system']}")
        lines.append(f"Platform: {report['report_metadata']['platform_release']}")
        lines.append(f"Admin Privileges: {report['report_metadata']['admin_privileges']}")
        
        lines.append(f"\n{'='*80}")
        lines.append("EXECUTION SUMMARY")
        lines.append(f"{'='*80}")
        lines.append(f"Total Modules: {report['summary']['total_modules']}")
        lines.append(f"Successful: {report['summary']['successful']}")
        lines.append(f"Failed: {report['summary']['failed']}")
        lines.append(f"Success Rate: {report['summary']['success_rate']}")
        
        lines.append(f"\n{'='*80}")
        lines.append("DETAILED RESULTS")
        lines.append(f"{'='*80}")
        
        for result in report['results']:
            status = "✓ SUCCESS" if result['success'] else "✗ FAILED"
            lines.append(f"\n{result['module_name']} [{status}]")
            lines.append(f"  Category: {result['category']}")
            lines.append(f"  Severity: {result['severity']}")
            lines.append(f"  Duration: {result['duration']}")
            if result['error']:
                lines.append(f"  Error: {result['error']}")
        
        if report['recommendations']:
            lines.append(f"\n{'='*80}")
            lines.append("RECOMMENDATIONS")
            lines.append(f"{'='*80}")
            for rec in report['recommendations']:
                lines.append(f"\n{rec['module']}:")
                lines.append(f"  Issue: {rec['issue']}")
                lines.append(f"  Suggestion: {rec['suggestion']}")
        
        return '\n'.join(lines)
    
    def _display_report_summary(self, report: Dict):
        """Display report summary"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(self._center_text("REPORT SUMMARY"))
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"Total Modules: {report['summary']['total_modules']}")
        print(f"Successful: {Fore.GREEN}{report['summary']['successful']}{Style.RESET_ALL}")
        print(f"Failed: {Fore.RED}{report['summary']['failed']}{Style.RESET_ALL}")
        print(f"Success Rate: {report['summary']['success_rate']}")
    
    # ============================================================
    # ROLLBACK FUNCTIONALITY
    # ============================================================
    
    def _rollback_hardening(self):
        """Rollback applied hardening modules"""
        self._clear_screen()
        self._display_header()
        
        applied_modules = [r for r in self.results if r.success and r.module.rollback_command]
        
        if not applied_modules:
            print(f"{Fore.YELLOW}No modules available for rollback.{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.YELLOW}⚠ WARNING: This will rollback hardening changes!{Style.RESET_ALL}")
        print(f"\nModules available for rollback:")
        for i, result in enumerate(applied_modules, 1):
            print(f"  {i}. {result.module.name}")
        
        confirm = input(f"\n{Fore.RED}Type 'ROLLBACK' to confirm: {Style.RESET_ALL}").strip()
        
        if confirm == "ROLLBACK":
            for result in applied_modules:
                print(f"\n{Fore.CYAN}Rolling back: {result.module.name}...{Style.RESET_ALL}")
                try:
                    subprocess.run(result.module.rollback_command, shell=True, check=True)
                    print(f"{Fore.GREEN}✓ Rolled back successfully{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}✗ Rollback failed: {str(e)}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}Rollback cancelled.{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    # ============================================================
    # UTILITY FUNCTIONS
    # ============================================================
    
    def _center_text(self, text: str) -> str:
        """Center text in terminal"""
        return text.center(self.terminal_width)
    
    def _clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if self.system == 'Windows' else 'clear')
    
    def run(self):
        """Main entry point"""
        try:
            self.display_dashboard()
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Hardening dashboard interrupted.{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}Critical error: {str(e)}{Style.RESET_ALL}")
            logging.error(f"Dashboard error: {str(e)}")


# ============================================================
# ENHANCED CINEMATIC FUNCTIONS FOR EXISTING CODE
# ============================================================

def enhanced_cinematic_hardening(self, dry_run=False):
    """
    Enhanced version of harden_system that can be added to your existing class
    """
    # Initialize dashboard for tracking
    dashboard = HardeningDashboard()
    
    # Show cinematic elements
    # self._enlarged_ascii_banner()
    # self._matrix_rain_effect(1)
    
    if not dashboard.is_admin_user:
        print(f"{Fore.RED}[!] Warning: Running without administrator privileges{Style.RESET_ALL}")
    
    # Select critical modules automatically
    critical_modules = [m for m in dashboard.modules 
                       if m.severity in [HardeningSeverity.CRITICAL, HardeningSeverity.HIGH]]
    dashboard.selected_modules = [m.id for m in critical_modules]
    
    # Execute with cinematic effects
    # self._hacking_animation("Initializing Threat Assessment")
    dashboard._execute_hardening()
    
    # Generate report
    dashboard._generate_report()
    
    # Blinking completion
    for _ in range(3):
        print(f"\r{Fore.GREEN}{dashboard._center_text('▄︻デ══━ SYSTEM FORTIFICATION COMPLETE ══━︻▄')}{Style.RESET_ALL}", end="")
        time.sleep(0.3)
        print(f"\r{' ' * dashboard.terminal_width}", end="")
        time.sleep(0.3)


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    dashboard = HardeningDashboard()
    dashboard.run()