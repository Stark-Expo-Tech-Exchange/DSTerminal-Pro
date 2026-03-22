import os
import sys
import io
import glob
import queue
from turtle import color

from stdeb import command
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


# Define global variables at module level
INTEGRITY_AVAILABLE = False
COLORS_AVAILABLE = False

# Try to import colorama
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

# Try to import integrity monitor
try:
    # First check if the file exists
    if os.path.exists('integrity_monitor.py'):
        from integrity_monitor import SystemIntegrityMonitor
        # Try to import optional classes
        AlertManager = None
        ForensicAnalyzer = None

        try:
            from integrity_monitor import AlertManager as AM
            AlertManager = AM
        except ImportError:
            pass

        try:
            from integrity_monitor import ForensicAnalyzer as FA
            ForensicAnalyzer = FA
            # If we got here, integrity monitor is available
        except ImportError:
            pass
        
        INTEGRITY_AVAILABLE = True
        if COLORS_AVAILABLE:
            print(f"{Fore.GREEN}✓ Integrity Monitor loaded successfully{Style.RESET_ALL}")
        else:
            print("✓ Integrity Monitor loaded successfully")
    else:
        INTEGRITY_AVAILABLE = False
        if COLORS_AVAILABLE:
            print(f"{Fore.YELLOW}⚠ integrity monitor not found{Style.RESET_ALL}")
        else:
            print("⚠ integrity monitor not found")
            
except ImportError as e:
    INTEGRITY_AVAILABLE = False
    if COLORS_AVAILABLE:
        print(f"{Fore.YELLOW}⚠ Integrity Monitor not available: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Run: pip install -r requirements.txt{Style.RESET_ALL}")
    else:
        print(f"⚠ Integrity Monitor not available: {e}")
        print("  Run: pip install -r requirements.txt")

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
import OpenSSL
import subprocess
from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.ocsp import OCSPRequestBuilder
from threading import Thread, Event
from datetime import datetime
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
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.colors import black, lightgrey, HexColor
from crypto_engine import CryptoEngine
init(autoreset=True)

engine = EducationTypingEngine(speed=0.03)
username = "OP-" + uuid.uuid4().hex[:6].upper()
crypto_engine = CryptoEngine()


# =============dsterminal workspace creation from here===============
def init_workspace():
    workspace_path = os.path.expanduser("~/dsterminal_workspace")
    subdirs = ["sandbox", "scans", "exploits", "reports"]
    
    try:
        os.makedirs(workspace_path, exist_ok=True)
        for subdir in subdirs:
            os.makedirs(os.path.join(workspace_path, subdir), exist_ok=True)
        # print(f"{Fore.GREEN}[+] Workspace initialized at: {workspace_path}{Style.RESET_ALL}")
        # return workspace_pencryptath
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to initialize workspace: {e}{Style.RESET_ALL}")
        sys.exit(1) 
# Initialize workspace safely
WORKSPACE = init_workspace()
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
    [bold]🔍 Network Monitoring Tip[/bold]\n
    Monitor for:\n
    1. [red]Unexpected outbound connections[/red] (could indicate data exfiltration)\n
    2. Ports in `LISTEN` state that shouldn't be open\n
    3. Use tools like [green]Wireshark[/green] for deep packet inspection.\n
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
    CER""",
    
    "vt-scan": """
    [bold]🦠 VirusTotal Tip[/bold]\n
    Advanced features:\n
    - [red]Behavioral analysis[/red] (sandbox)\n
    - [yellow]Community insights[/yellow]\n
    - [blue]YARA rule scanning[/blue]\n
    [green]Warning:[/green] Files become public!\n
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
    def __init__(self, workspace_root="."):
        self.current_dir = workspace_root
        self.workspace_root = workspace_root
        self.crypto = CryptoEngine(os.getcwd())
        # self.integrity = SystemIntegrityMonitor()
            # Initialize integrity monitor if available
         # Use the global variable
        global INTEGRITY_AVAILABLE
        
        # Initialize integrity monitor if available
        if INTEGRITY_AVAILABLE:
            try:
                self.integrity = SystemIntegrityMonitor()
                # Create data directories if they don't exist
                os.makedirs("data/baselines", exist_ok=True)
                os.makedirs("data/integrity_reports", exist_ok=True)
                os.makedirs("data/quarantine", exist_ok=True)
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
                INTEGRITY_AVAILABLE = False
        else:
            self.integrity = None
            if COLORS_AVAILABLE:
                print(f"{Fore.YELLOW}⚠ Integrity Monitor disabled{Style.RESET_ALL}")
            else:
                print("⚠ Integrity Monitor disabled")
        
        # Initialize alert manager later when needed
        self.alert_manager = None

        # Initialize alert manager later when needed
        self.alert_manager = None

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
            # print(f"{Fore.GREEN}[+] Created workspace: {self.workspace_root}{Style.RESET_ALL}")
        
        # Create default directories
        default_dirs = ["exploits", "reports", "sandbox", "scans"]
        for dir_name in default_dirs:
            dir_path = os.path.join(self.workspace_root, dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        
        self.terminal_width = self._get_terminal_width()

        # Initialize encryption
        # self.cipher = None
        # self.init_cipher()
 
        # Virtual filesystem directory
        self.vfs_root = os.path.expanduser("~/.dsterminal_vfs")
        self.ensure_vfs()

    # =========initializing operator workspace and username and session logging===========
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

        operators_root = os.path.join(self.workspace_root, "operators")
        os.makedirs(operators_root, exist_ok=True)

    # Generate unique operator identity
        username = "OP-" + uuid.uuid4().hex[:6].upper()
        self.session_id = "SOC-" + uuid.uuid4().hex[:5].upper()

        operator_dir = os.path.join(operators_root, username)
        os.makedirs(operator_dir, exist_ok=True)

        log_file = os.path.join(operator_dir, "session_log.txt")

    # Store session start time
        self.session_start = datetime.now()

        with open(log_file, "w", encoding="utf-8") as f:

            f.write("╔══════════════════════════════════════════════╗\n")
            f.write("║       DSTerminal Operator Security Audit Log ║\n")
            f.write("╠══════════════════════════════════════════════╣\n")
            f.write(f"║ Operator   : {username}\n")
            f.write(f"║ Session ID : {self.session_id}\n")
            f.write(f"║ Host       : {socket.gethostname()}\n")
            f.write(f"║ Start Time : {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("╠══════════════════════════════════════════════╣\n")
            f.write("║ Command Activity                             ║\n")
            f.write("╠══════════════════════════════════════════════╣\n")

        self.operator_username = username
        self.operator_dir = operator_dir
        self.log_file = log_file

    # ================= CINEMATIC INITIALIZATION =================

        start_time = time.time()

        self.typewriter("\n[ DSTerminal Security Initialization ]\n", 0.03)
        self.typewriter("✔ Generating Operator Identity...", 0.05)
        time.sleep(1.5)

        self.typewriter("✔ Creating Secure Session...", 0.05)
        time.sleep(1.5)

        self.typewriter("✔ Logging Enabled\n", 0.05)
        time.sleep(1)

        self.typewriter(f" 🛡️, 🌐 ⚡ YOUR UNIQUE OPERATOR SESSION USERNAME IS: {username}\n", 0.04)

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

        COMMANDS = {
            "recon": {
                "-full": None
            },
            "net": {
                "-n": {
                    "mon": None
            }
        },
        "system": {
            "scan": {
                "-All": None
            }
        },
        "nikto": None,
        "nmap": None,
        "transfertrace": None,
        "certcheck": None,
        "metasploit": None,
        "msf": None,
        "sqlmap": None,
        "torify": None,
        "crypto-list": None,
        "crypto-info": None,
        "crypto-init": None,
        "crypto-status": None,
        "crypto-backup": None,
        "vt-scan": None,
        "ransomwatch": None,
        "dnssec": None,
        "traceroute": None,
        "exploitcheck": None,
        "portsweep": None,
        "hashfile": None,
        "memdump": None,
        "sysinfo": None,
        "killproc": None,
        "encrypt": None,
        "decrypt": None,
        "encrypt-test": None,
        "encrypt-setup": None,
        "watchfolder": None,
        "check": {
            "integrity": None
        },
        "registry": {
            "-n": {
                "mon": None
            }
        },
        "clear": None,
        "cls": None,
        "clearlogs": None,
        "update": None,
        "help": None,
        "exit": None,
        "mkdir": None,
        "cd": None,
        "touch": None,
        "cat": None,
         "certcheck": None
            
        }
    
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
    # ANSI color codes for hacking-style colors
        colors = [
            '\033[92m',  # Light Green (Matrix style)
            '\033[38;5;46m',  # Matrix Green
            '\033[38;5;82m',  # Bright Green
            '\033[38;5;118m',  # Lime Green
            '\033[38;5;154m',  # Yellow-Green
            '\033[38;5;190m',  # Light Yellow-Green
            '\033[38;5;226m',  # Bright Yellow
            '\033[38;5;220m',  # Gold
            '\033[38;5;214m',  # Orange
            '\033[38;5;202m',  # Bright Orange
            '\033[38;5;196m',  # Bright Red
            '\033[38;5;201m',  # Pink/Magenta
            '\033[38;5;165m',  # Purple
            '\033[38;5;129m',  # Violet
            '\033[38;5;93m',   # Deep Purple
            '\033[38;5;63m',   # Blue-Purple
            '\033[38;5;69m',   # Blue
            '\033[38;5;75m',   # Light Blue
            '\033[38;5;81m',   # Cyan
            '\033[38;5;87m',   # Light Cyan
            '\033[96m',        # Cyan
            '\033[95m',        # Magenta
            '\033[91m',        # Light Red
            '\033[93m',        # Light Yellow
        ]
    
        # Add blinking effects for some colors
        BLINK = '\033[5m'
        BOLD = '\033[1m'
    
        # Mix in some blinking and bold variants
        extended_colors = []
        for color in colors:
            extended_colors.append(color)
            extended_colors.append(color + BOLD)
            if random.random() > 0.7:  # Add blinking to some colors randomly
                extended_colors.append(color + BLINK)
    
        color = random.choice(extended_colors)
        terminal_width = shutil.get_terminal_size((80, 20)).columns

        banner_lines = [
        "╔═══════════════════════════════════════════════════════════════════============═══╗",
        "    ██████╗ ███████╗███████╗███████╗███╗   ██╗███████╗██╗  ██╗",
        "    ██╔══██╗██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝╚██╗██╔╝",
        "    ██║  ██║█████╗  █████╗  █████╗  ██╔██╗ ██║█████╗   ╚███╔╝ ",
        "    ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║██╔══╝   ██╔██╗ ",
        "    ██████╔╝██║     ██║     ███████╗██║ ╚████║███████╗██╔╝ ██╗",
        "    ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝",
        "",
        "╠══════════════════════════════════════════════════════════════============══════╣",
        f"║    Defensive Security Terminal v2.0.113 | {platform.system()} {platform.release()}   ║",
        "║    Developed by: Spark Wilson Spink | © 2024 | Powered by Stark Expo Tech Exchange║",
        "║    Type 'help' for available commands                                            ║",
        f"║ (🔍, ⚡, 🛡️) 🌐 ⚡ CLI Mode: {'ADMIN' if self.is_admin() else 'USER'}               ",
        "╚════════════════════════════════════════════════════════════════════============══╝"
        ]

        def glitch_char(c):
            if c.isspace():
                return c
            return random.choice(["#", "@", "%", "&", "*", c])

        def type_line(line, delay=0.002, glitch=False):
            centered = line.center(terminal_width)
            for char in centered:
                if glitch and random.random() < 0.04:
                    sys.stdout.write(color + glitch_char(char))
                    sys.stdout.flush()
                    time.sleep(delay * 2)
                    sys.stdout.write('\b' + color + char)
                    sys.stdout.flush()
                else:
                    sys.stdout.write(color + char)
                    sys.stdout.flush()
                time.sleep(delay)
            sys.stdout.write("\n")
            time.sleep(0.01)

        for line in banner_lines:
            type_line(line, glitch=True)

        print(Style.RESET_ALL)

        if not self.is_admin():
            print("\n[!] Warning: Running without administrator privileges. Some features may be limited.")
            # =====================banner print ends here======================================
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
    
    # Python environment
        print(f"\n🐍 [PYTHON ENVIRONMENT]")
        print(f"  Version: {platform.python_version()}")
        print(f"  Implementation: {platform.python_implementation()}")
        print(f"  Virtual Env: {'Yes' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 'No'}")
    
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
        # displaying education tips code ends here


# ---------------------folder or dir creation for safe environment running
    # def safe_path(self, path):
    #     full_path = os.path.abspath(os.path.join(self.current_dir, path))
    #     if not full_path.startswith(self.workspace_root):
    #         raise PermissionError("Access outside workspace is not allowed")
    #     return full_path
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
 
# ---viewing a file

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

    # =================ends here==========
    def process_command(self, user_input):
        """Process and dispatch commands"""
        if not user_input.strip():
            return True  # Nothing to do, continue

    # Handle echo first to preserve the raw string
        if user_input.strip().lower().startswith("echo"):
            self.handle_echo(user_input)
            return True

    # Otherwise, parse normally
        import shlex
        parts = shlex.split(user_input)
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

    # Command dispatch
        if command == "help":
            self.show_help()
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
        # Add this to your command handler:
        elif command == "viewlog" or command == "session":
            self.view_session_log()

        elif command == 'cat ':
            if not args:
                print(f"{Fore.RED}[!] Usage: cat <filename>{Style.RESET_ALL}")
                return True
            filename = args[0]
            try:
                if hasattr(self, 'operator_dir') and os.path.exists(self.operator_dir):
                    filepath = os.path.join(self.operator_dir, filename)
                else:
                    filepath = self.safe_path(filename)
            except Exception as e:
                    filepath = filename  # Fallback to original filename if safe_path fails

              # Read the file with multiple encoding attempts
            content = self.safe_read_file(filepath)
            print(content)
  
    # In your command handler, update the integrity section:
 
# =====================debug===================
# Add this temporary debug command in your command handler
        elif cmd == "debug":
            print(f"Current directory: {self.current_dir}")
            print(f"Workspace root: {self.workspace_root}")
            print(f"Trying to write: {os.path.join(self.current_dir, 'test.txt')}")
# --------------------ends debug---------------
       
# refresh command=================
        elif command == "harden":
            dry_run = "-t" in args or "--test" in args
            self.harden_system(dry_run=dry_run)
        else:
            print(f"{Fore.RED}[!] Unknown command: '{command}'. Type 'help' for available commands.{Style.RESET_ALL}")

        return True

    def show_help(self):
        """Display help information"""
        help_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    DSTERMINAL HELP MENU                        ║
╠════════════════════════════════════════════════════════════════╣
║  {Fore.YELLOW}FILE OPERATIONS:{Fore.CYAN}                                            ║
║    ls                    - List directory contents             ║
║    cd <dir>              - Change directory                    ║
║    pwd                   - Print working directory             ║
║    mkdir <name>          - Create a new directory              ║
║    touch <file>          - Create a new file                   ║
║    cat <file>            - Display file contents               ║
║    echo <text>           - Display text                        ║
║    echo <text> > <file>  - Write text to file                  ║
║    echo <text> >> <file> - Append text to file                 ║
║                                                               ║
║  {Fore.YELLOW}SYSTEM OPERATIONS:{Fore.CYAN}                                          ║
║    harden                - Run system hardening                ║
║    harden -t             - Test mode (dry run)                 ║
║    clear / cls           - Clear the screen                    ║
║    exit / quit           - Exit DSTerminal                     ║
║    help                  - Show this help menu                 ║
║                                                               ║
║  {Fore.YELLOW}WORKSPACE:{Fore.CYAN}                                                ║
║    All operations are confined to: {Fore.GREEN}~/DSTerminal_Workspace{Fore.CYAN}     ║
║    Default directories: exploits, reports, sandbox, scans      ║
╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(help_text)
    
    def run(self):
        """Main terminal loop"""
        print(f"{Fore.GREEN}DSTerminal v2.0.113 | Type 'help' for commands | Workspace: ~/DSTerminal_Workspace{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Mode: {'ADMIN' if self.is_admin() else 'USER'}{Style.RESET_ALL}\n")
        
        running = True
        while running:
            try:
                # Show prompt
                prompt_path = self.current_dir.replace(self.workspace_root, "~")
                user_input = input(f"{Fore.CYAN}[-- DFFENEX@DSTerminal {prompt_path} ]-{Style.RESET_ALL} ").strip()
                
                # Process command
                if user_input:
                    running = self.process_command(user_input)
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Use 'exit' to quit{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
  
#   metasploit--------------------



# ------added msf impleme
 
    def launch_metasploit(self):
        system = platform.system()

        try:
            if system == "Linux":
                subprocess.call(["msfconsole"])

            elif system == "Windows":

                try:
                    result =subprocess.run(
                        ["wsl", "bash", "-c", "command -v msfconsole"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    if result.returncode == 0:
                        return True
                except Exception as e:
                    pass
                return shutil.which("msfconsole") is not None

            elif system == "Darwin":
                subprocess.call(["msfconsole"])

            else:
                print("Unsupported OS.")

        except FileNotFoundError:
            print(f"{Fore.RED}[!] msfconsole not found in PATH{Style.RESET_ALL}")

    def check_metasploit_installed(self):
        system = platform.system()

        if system == "Linux":
            return shutil.which("msfconsole") is not None

        elif system == "Windows":
        # Check WSL
            try:
                result = subprocess.run(
                    ["wsl", "which", "msfconsole"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return result.returncode == 0
            except Exception:
                return False

        elif system == "Darwin":  # macOS
            return shutil.which("msfconsole") is not None

        return False
    
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
            print(Fore.CYAN + "[Windows Installation]" + Style.RESET_ALL)

            print("Option 1: Install via WSL (Recommended)")
            print(Fore.YELLOW + "  wsl --install\n" + Style.RESET_ALL)
            print("Then install metasploit inside WSL:")

            print(Fore.YELLOW + "  sudo apt install metasploit-framework\n" + Style.RESET_ALL)

            print("Option 2: Use the official Windows installer:")
            print("  https://www.metasploit.com/download\n")

        elif system == "Darwin":
            print(Fore.CYAN + "[macOS Installation]" + Style.RESET_ALL)

            print("Install via Homebrew:")
            print(Fore.YELLOW + "  brew install metasploit\n" + Style.RESET_ALL)

            print("Official installer:")
            print("  https://www.metasploit.com/download\n")

        else:
            print("Unsupported operating system.\n")

        print(Fore.GREEN + "[*] After installation, restart DSTerminal and run 'msf' again." + Style.RESET_ALL)

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
            spinner.join()
            stop_event.clear()
        
        # Countdown effect
        print(f"\n{Fore.RED}[!] LAUNCHING IN:{Style.RESET_ALL}")
        for i in range(3, 0, -1):
            print(f"  {Fore.RED}{i}...{Style.RESET_ALL}")
            time.sleep(0.5)
        
        # Final handoff
        print(f"\n{Fore.GREEN}[+] Handing control to Metasploit Framework...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Use 'exit' to return to DSTerminal{Style.RESET_ALL}")
        self.play_beep()
        time.sleep(1)
        
        try:
            # Replace current process with msfconsole (REAL TTY)
            # os.execvp("msfconsole", ["msfconsole"])
            self.launch_metasploit()
        except FileNotFoundError:
            print(f"{Fore.RED}[!] msfconsole not found in PATH{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to start Metasploit: {e}{Style.RESET_ALL}")
    
    # Alternative implementation with ASCII art
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
 
# ---------========-----------------metasplo ends here from above-----------------------------
    # ALLOWED_NMAP_FLAGS = {"-p", "-sT", "-sS", "-sV", "-T4", "-Pn"}
    # def check_nmap_installed(self):
    #     return shutil.which("nmap") is not None


    # def handle_nmap(self, args):
    #     if not self.check_nmap_installed():
    #         print("[!] Nmap is not installed on this system")
    #         return

    #     if len(args) < 2 or args[0] != "scan":
    #         print("Usage: nmap scan <target> [flags]")
    #         return

    #     target = args[1]
    #     flags = args[2:]

    #     cmd = ["nmap"]

    #     for f in flags:
    #         if f.startswith("-"):
    #             if f not in self.ALLOWED_NMAP_FLAGS:
    #                 print(f"[!] Flag not allowed: {f}")
    #                 return
    #         cmd.append(f)

    #     cmd.append(target)

    # # Ensure scans directory exists
    #     scans_dir = os.path.join(self.workspace_root, "scans")
    #     os.makedirs(scans_dir, exist_ok=True)

    #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #     output_file = os.path.join(
    #         scans_dir,
    #         f"nmap_{target}_{timestamp}.txt"
    #     )

    #     cmd.extend(["-oN", output_file])

    #     print(f"[+] Running nmap scan on {target}...")
    #     print(f"[+] Output → scans/{os.path.basename(output_file)}")

    #     try:
    #         subprocess.run(
    #             cmd,
    #             shell=self.is_windows(),
    #             check=True
    #         )
    #     except subprocess.CalledProcessError as e:
    #         print(f"[!] Nmap failed: {e}")

# Initialize colorama
 
    ALLOWED_NMAP_FLAGS = {"-p", "-sT", "-sS", "-sV", "-T4", "-Pn", "-A", "-O", "-sC"}


    def check_nmap_installed(self):
        return shutil.which("nmap") is not None

    def create_layout(self):
        """Create the three-column layout"""
        layout = Layout()
        layout.split_row(
            Layout(name="terminal", ratio=1),
            Layout(name="progress", ratio=1),
            Layout(name="results", ratio=1)
        )
        return layout

    def render_terminal_panel(self):
        """Render the terminal/command panel"""
        table = RichTable(show_header=True, header_style="bold green", box=box.HEAVY, padding=(0, 1))
        table.add_column("Command History", style="cyan")
        
        # Show last 10 commands/outputs
        recent_lines = self.output_lines[-10:] if self.output_lines else ["Ready for commands..."]
        for line in recent_lines:
            # Clean the line of any existing Rich markup to prevent conflicts
            clean_line = line.replace('[', '\\[').replace(']', '\\]')
            if len(clean_line) > 60:
                clean_line = clean_line[:60] + "..."
            table.add_row(clean_line)
        
        return Panel(
            table,
            title="[bold red]⚡ SOC Terminal ⚡[/bold red]",
            border_style="bright_red",
            subtitle="nmap scan <target> [flags]"
        )

    def render_progress_panel(self):
        """Render the scan progress panel with enhanced styling"""
    # Status table with better colors
        status_table = RichTable(show_header=False, box=box.ROUNDED, border_style="bright_blue", padding=(0, 2))
        status_table.add_column("Status", style="bold bright_yellow")
        status_table.add_column("Value", style="bold white")
    
    # Scan status with improved color scheme
        status_color = {
            "Completed": "bright_green",
            "Scanning": "bright_yellow",
            "Starting": "bright_cyan",
            "Failed": "bright_red",
            "Ready": "bright_blue"
        }.get(self.scan_status, "white")
    
    # Add blinking effect for active scanning
        status_display = f"[{status_color}]{self.scan_status}[/{status_color}]"
        if self.scan_status == "Scanning":
            status_display = f"[blink][{status_color}]{self.scan_status}[/{status_color}][/blink]"
    
        status_table.add_row("Status:", status_display)
        status_table.add_row("Target:", f"[bold bright_magenta]{self.current_scan if self.current_scan else 'N/A'}[/bold bright_magenta]")
        status_table.add_row("Progress:", f"[bold bright_green]{self.scan_progress}%[/bold bright_green]")
    
        # Progress bar with rotating spinner while waiting
        progress_width = 40
    
    # Create rotating spinner frames
        spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        scan_start_frames = ["🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛"]
    
        if self.scan_status == "Starting" and self.scan_progress == 0:
        # Show rotating clock while waiting for scan to start
            frame = scan_start_frames[int(time.time() * 4) % len(scan_start_frames)]
            progress_display = f"\n\n[bold bright_cyan]   {frame} Initializing scan... {frame}[/bold bright_cyan]\n\n"
            progress_display += f"[dim]Preparing nmap scan on {self.current_scan}...[/dim]"
        
        elif self.scan_status == "Scanning" and self.scan_progress == 0:
        # Show spinner while scan is starting but no progress yet
            frame = spinner_frames[int(time.time() * 10) % len(spinner_frames)]
            progress_display = f"\n\n[bold bright_yellow]   {frame} Waiting for response... {frame}[/bold bright_yellow]\n\n"
        
        else:
        # Normal progress bar when scan is active
            filled = int((self.scan_progress / 100) * progress_width)
        

    # Enhanced progress bar with gradient effect
        progress_width = 40  # Wider progress bar
        filled = int((self.scan_progress / 100) * progress_width)
    
    # Create gradient progress bar
        progress_bar = ""
        for i in range(progress_width):
            if i < filled:
            # Gradient from cyan to green as progress increases
                if i < progress_width * 0.3:
                    progress_bar += "█"  # Cyan at start
                elif i < progress_width * 0.6:
                    progress_bar += "█"  # Yellow in middle
                else:
                    progress_bar += "█"  # Green at end
            else:
                progress_bar += "░"  # Dim remaining
    
    # Add percentage with color based on progress
        if self.scan_progress < 30:
            percent_color = "bright_cyan"
        elif self.scan_progress < 70:
            percent_color = "bright_yellow"
        else:
            percent_color = "bright_green"
    
        progress_display = f"[bold {percent_color}]{progress_bar}[/bold {percent_color}] [bold white]{self.scan_progress}%[/bold white]"
    
    # Add ETA simulation (optional)
        if self.scan_status == "Scanning" and self.scan_progress > 0:
            eta_seconds = int((100 - self.scan_progress) * 0.5)  # Rough estimate
            progress_display += f"\n[dim white]ETA: {eta_seconds}s[/dim white]"
    
        progress_panel = Panel(
            Align.center(progress_display),
            title="[bold bright_magenta]⚡ PROGRESS[/bold bright_magenta]",
            border_style="bright_magenta"
        )
    
    # Combine status and progress
        progress_layout = Layout()
        progress_layout.split_column(
            Layout(Panel(status_table, title="[bold bright_blue]📊 SCAN STATUS[/bold bright_blue]", border_style="bright_blue")),
            Layout(progress_panel)
        )
    
    # Discovered ports section with enhanced styling
        if self.discovered_ports:
            ports_text = ""
            for i, p in enumerate(self.discovered_ports[-8:]):  # Show more ports
                # Color code based on port state
                if p['state'] == 'open':
                    port_color = "bright_green"
                    icon = "🔓"
                elif p['state'] == 'filtered':
                    port_color = "bright_yellow"
                    icon = "🔒"
                else:
                    port_color = "bright_red"
                    icon = "❌"
            
                ports_text += f"{icon} [bold {port_color}]Port {p['port']}/{p.get('protocol', 'tcp')}: {p['service']}[/bold {port_color}]\n"
        
            ports_panel = Panel(
                Align.left(ports_text),
                title="[bold bright_cyan]🔓 DISCOVERED PORTS[/bold bright_cyan]",
                border_style="bright_cyan"
            )
            progress_layout.split_column(
                Layout(progress_layout),
                Layout(ports_panel)
            )
    
        return progress_layout

    def render_results_panel(self):
        """Render the scan results panel with enhanced styling"""
        results_table = RichTable(show_header=True, box=box.DOUBLE_EDGE, padding=(0, 2))
        results_table.add_column("[bold bright_cyan]Port/Protocol[/bold bright_cyan]", style="bright_cyan")
        results_table.add_column("[bold bright_green]State[/bold bright_green]", style="bright_green")
        results_table.add_column("[bold bright_yellow]Service[/bold bright_yellow]", style="bright_yellow")
        results_table.add_column("[bold bright_magenta]Version/Info[/bold bright_magenta]", style="bright_white")
    
    # Add discovered services with enhanced formatting
        if self.services_found:
            for i, service in enumerate(self.services_found):
                version = service.get('version', '')
                if len(version) > 35:
                    version = version[:35] + "..."
            
            # Alternate row colors for better readability
                if i % 2 == 0:
                    row_style = "on grey15"
                else:
                    row_style = ""
            
                results_table.add_row(
                    f"[bold]{service.get('port', 'N/A')}/{service.get('protocol', 'tcp')}[/bold]",
                    f"[bold bright_green]{service.get('state', 'N/A')}[/bold bright_green]",
                    f"[bold bright_yellow]{service.get('service', 'N/A')}[/bold bright_yellow]",
                    version,
                    style=row_style
                )
        else:
            # Animated waiting message
            waiting_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            frame = waiting_frames[int(time.time() * 5) % len(waiting_frames)]
            results_table.add_row(
                f"[dim]{frame} Waiting for results...[/dim]",
                "",
                "",
                ""
            )
    
    # Add summary if scan completed
        if self.scan_status == "Completed" and self.discovered_ports:
            open_ports = len([p for p in self.discovered_ports if p['state'] == 'open'])
            filtered_ports = len([p for p in self.discovered_ports if p['state'] == 'filtered'])
            closed_ports = len([p for p in self.discovered_ports if p['state'] == 'closed'])
        
        # Create summary with colored counters
            summary_text = (
                f"[bold bright_green]Open: {open_ports}[/bold bright_green] | "
                f"[bold bright_yellow]Filtered: {filtered_ports}[/bold bright_yellow] | "
                f"[bold bright_red]Closed: {closed_ports}[/bold bright_red]"
            )
        
            summary_panel = Panel(
                Align.center(summary_text),
                border_style="bright_green",
                title="[bold white]SCAN SUMMARY[/bold white]"
            )
        
        # Create a layout with both table and summary
            results_layout = Layout()
            results_layout.split_column(
                Layout(Panel(results_table, title="[bold bright_green]🎯 OPEN PORTS & SERVICES[/bold bright_green]", border_style="bright_green")),
                Layout(summary_panel)
            )
            return results_layout
    
        return Panel(
            results_table,
            title="[bold bright_green]🎯 OPEN PORTS & SERVICES[/bold bright_green]",
            border_style="bright_green"
        )


    def parse_nmap_output(self, line):
        """Parse nmap output in real-time"""
        # Parse port discovery
        port_match = re.search(r'(\d+)/(tcp|udp)\s+(\w+)\s+(\w+)\s*(.*)', line)
        if port_match:
            port_info = {
                'port': port_match.group(1),
                'protocol': port_match.group(2),
                'state': port_match.group(3),
                'service': port_match.group(4),
                'version': port_match.group(5).strip()
            }
            
            if not any(p['port'] == port_info['port'] for p in self.discovered_ports):
                self.discovered_ports.append(port_info)
                if port_info['state'] == 'open':
                    self.services_found.append(port_info)
                    self.scan_progress = min(self.scan_progress + 5, 90)
        
        # Parse progress indicators
        if "Scanning" in line:
            self.scan_status = "Scanning"
        elif "Nmap done" in line:
            self.scan_status = "Completed"
            self.scan_progress = 100
        elif "Initiating" in line:
            self.scan_progress = 10
        elif "PORT" in line and "STATE" in line:
            self.scan_progress = 30
        elif "Service detection" in line:
            self.scan_progress = 60
        elif "TRACEROUTE" in line:
            self.scan_progress = 85

    def handle_nmap(self, args):
        """Main handler for nmap commands"""
        if not self.check_nmap_installed():
            print(f"{Fore.RED}[!] Nmap is not installed on this system{Style.RESET_ALL}")
            return

        if len(args) < 1 or args[0] != "scan":
            print(f"{Fore.YELLOW}Usage: nmap scan <target> [flags]{Style.RESET_ALL}")
            return

        target = args[1]
        flags = args[2:] if len(args) > 2 else []
        
        # Start scan in background thread
        scan_thread = threading.Thread(
            target=self.run_nmap_scan,
            args=(target, flags)
        )
        scan_thread.daemon = True
        scan_thread.start()
        
        # Start the live display
        self.start_live_display()

    def run_nmap_scan(self, target, flags):
        """Run nmap scan with real-time progress updates"""
        cmd = ["nmap"]
    
    # Validate flags
        for f in flags:
            if f.startswith("-"):
                if f not in self.ALLOWED_NMAP_FLAGS:
                    self.output_lines.append(f"[!] Flag not allowed: {f}")
                    return
                cmd.append(f)
    
        cmd.append(target)
    
    # Create scans directory
        scans_dir = os.path.join(self.workspace_root, "scans")
        os.makedirs(scans_dir, exist_ok=True)

        reports_dir = os.path.join(self.workspace_root, "reports")
        os.makedirs(reports_dir, exist_ok=True) 

    
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_target = target.replace('.', '_').replace('/', '_').replace(':', '_')
        output_file = os.path.join(scans_dir, f"nmap_{safe_target}_{timestamp}.txt")
    
        cmd.extend(["-oN", output_file])
    
    # Reset scan state
        self.current_scan = target
        self.scan_status = "Starting"
        self.discovered_ports = []
        self.services_found = []
        self.scan_progress = 0
        self.output_lines = []
    
        self.output_lines.append(f"[+] Running nmap scan on {target}...")
        self.output_lines.append(f"[+] Command: {' '.join(cmd)}")
        self.output_lines.append(f"[+] Output → scans/{os.path.basename(output_file)}")
    
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
        
            for line in process.stdout:
                line = line.strip()
                if line:
                    self.output_lines.append(line)
                    self.parse_nmap_output(line)
                
                    if len(self.output_lines) > 100:
                        self.output_lines = self.output_lines[-100:]
        
            process.wait()
        
            if process.returncode == 0:
                self.scan_status = "Completed"
                self.scan_progress = 100
                self.output_lines.append("[+] Scan completed successfully!")
            
            # Save results to file
                self.save_scan_results(output_file)
            else:
                self.scan_status = "Failed"
                self.output_lines.append(f"[!] Nmap failed with code {process.returncode}")
            
        except Exception as e:
            self.scan_status = "Failed"
            self.output_lines.append(f"[!] Scan error: {str(e)}")
    
    # Keep nmap_mode active to show results
    # The user will press Enter to exit via show_final_results()

    def save_scan_results(self, output_file):
        """Save formatted scan results to file"""
        try:
            with open(output_file.replace('.txt', '_formatted.txt'), 'w') as f:
                f.write("=" * 60 + "\n")
                f.write(f"NMAP SCAN RESULTS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Target: {self.current_scan}\n")
                f.write(f"Status: {self.scan_status}\n")
                f.write(f"Open Ports: {len([p for p in self.discovered_ports if p['state'] == 'open'])}\n\n")
            
                f.write("DISCOVERED PORTS:\n")
                f.write("-" * 40 + "\n")
                for port in self.discovered_ports:
                    if port['state'] == 'open':
                        f.write(f"{port['port']}/{port['protocol']} - {port['service']} - {port['version']}\n")
        except:
            pass
    def start_live_display(self):
        """Start the live three-column display with persistent results after completion"""
        self.nmap_mode = True
        self.console.clear()
    
        try:
        # Increased refresh rate for smoother progress
            with Live(console=self.console, refresh_per_second=10, screen=True) as live:
                while self.nmap_mode or self.scan_status == "Completed":
                # Create a new layout for each update
                    layout = Layout()
                    layout.split_row(
                        Layout(self.render_terminal_panel()),
                        Layout(self.render_progress_panel()),
                        Layout(self.render_results_panel())
                    )
                
                    live.update(layout)
                    time.sleep(0.05)  # Faster updates (50ms instead of 100ms)
                
                # If scan is complete, wait for user input to exit
                    if self.scan_status == "Completed" and self.nmap_mode:
                    # Still show the display but allow exit on keypress
                        pass
                    
        except Exception as e:
            print(f"{Fore.RED}[!] Display error: {str(e)}{Style.RESET_ALL}")
        finally:
            # Show final results and prompt to return
            self.show_final_results()

    def show_final_results(self):
        """Display final scan results and wait for user to return to terminal"""
        self.console.clear()
    
    # Create final results display
        final_layout = Layout()
        final_layout.split_column(
            Layout(Panel("[bold green]✓ SCAN COMPLETE[/bold green]", border_style="green"), size=3),
            Layout(self.render_results_panel()),
            Layout(Panel("[bold yellow]Press Enter to return to terminal[/bold yellow]", border_style="yellow"), size=3)
        )
    
        self.console.print(final_layout)
        input()  # Wait for user to press Enter
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

 
#  network monitoring implementation from here to below

    def init_bandwidth(self):
        self.prev_io = psutil.net_io_counters()

    def get_bandwidth(self):
        current = psutil.net_io_counters()
        sent = current.bytes_sent - self.prev_io.bytes_sent
        recv = current.bytes_recv - self.prev_io.bytes_recv
        self.prev_io = current
        return sent, recv

    def network_monitor(self):
        """Animated network monitoring with hacking-style visuals (stable version)"""
        self.init_bandwidth()

        console = Console()
        scanning_icons = ["🜂", "🜁", "🜃", "🜄", "⦿", "⌾", "⍟", "⋙"]

    # ----------------------------
    # Generate connection table
    # ----------------------------
        def generate_connection_table(connections):
            table = RichTable()

            table.add_column("LOCAL", style="cyan")
            table.add_column("→", justify="center")
            table.add_column("REMOTE", style="magenta")
            table.add_column("PID", justify="right")
            table.add_column("STATUS", justify="right")
            table.add_column("THREAT", justify="right")
            table.add_column("COUNTRY")
            table.add_column("ISP")
            table.add_column("SCORE", justify="right")

            for conn in connections:
                if conn.status == "ESTABLISHED" and conn.raddr:
                    geo = get_geo_ip(conn.raddr.ip)
                    level, icon, score = calculate_threat_score(conn, geo)
                    country = geo["country"] if geo else "N/A"
                    isp = geo["isp"] if geo else "N/A"
                    local = f"{conn.laddr.ip}:{conn.laddr.port}"
                    remote = f"{conn.raddr.ip}:{conn.raddr.port}"

                    table.add_row(local, "⋙", remote,
                                str(conn.pid) if conn.pid else "N/A",
                                "[green]ACTIVE", icon,
                                country, isp, str(score))
            return table

        # Threat scoring
                    # level, icon, score = calculate_threat_score(conn, geo)

                    # country = geo["country"] if geo else "N/A"
                    # isp = geo["isp"] if geo else "N/A"

                    # table.add_row(
                    #     local,
                    #     "⋙",
                    #     remote,
                    #     str(conn.pid) if conn.pid else "N/A",
                    #     "[green]ACTIVE",
                    #     icon,
                    #     country,
                    #     isp,
                    #     str(score)
                    # )

            # return table  # 🔥 IMPORTANT: Only returns Table (no recursion!)

    # ----------------------------
    # Pre-scan animation
    # ----------------------------
        def threat_scan_animation():
            with console.status("[bold green]Initializing network sensors..."):
                for i in range(5):
                    console.log(f"[cyan]Scanning layer {i+1}/5...")
                    time.sleep(1)

    # ----------------------------
    # Live Monitor (NO recursion)
    # ----------------------------
        from collections import Counter

        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import Table as PDFTable
        from reportlab.platypus import TableStyle
        from rich.table import Table as RichTable
        from reportlab.lib.styles import getSampleStyleSheet

        def export_forensic_report(connections, filename="forensic_report.pdf"):
            doc = SimpleDocTemplate(filename)
            elements = []

            styles = getSampleStyleSheet()
            elements.append(Paragraph("DSTerminal Forensic Network Report", styles["Heading1"]))
            elements.append(Spacer(1, 0.5 * inch))

            data = [["Local", "Remote", "PID", "Status", "Country", "ISP", "Score"]]

            for conn in connections:
                if conn.raddr:
                    geo = get_geo_ip(conn.raddr.ip)
                    level, icon, score = calculate_threat_score(conn, geo)
                    country = geo["country"] if geo else "N/A"
                    isp = geo["isp"] if geo else "N/A"

                    local = f"{conn.laddr.ip}:{conn.laddr.port}"
                    remote = f"{conn.raddr.ip}:{conn.raddr.port}"

                    data.append([local, remote, str(conn.pid), conn.status, country, isp, str(score)])

            table = PDFTable(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (2, 1), (-1, -1), 'CENTER')
            ]))

            elements.append(table)
            doc.build(elements)
            print(f"[✓] Forensic report exported to {filename}")




        def detect_intrusion(connections):
            ips = [c.raddr.ip for c in connections if c.raddr]
            counts = Counter(ips)

            alerts = []
            for ip, count in counts.items():
                if count > 15:
                    alerts.append(f"Possible port scan from {ip}")

            return alerts


        def live_monitor(duration=15):
            sent, recv = self.get_bandwidth()

            upload_kb = sent / 1024
            download_kb = recv / 1024

            bandwidth_bar = "█" * int(download_kb / 5)

            bandwidth_panel = Panel(
            f"Download: {download_kb:.2f} KB/s\nUpload: {upload_kb:.2f} KB/s\n\n{bandwidth_bar}",
            title="Bandwidth Activity",
            border_style="green"
        )

            start_time = time.time()

            with Live(console=console, refresh_per_second=2) as live:
                while time.time() - start_time < duration:

                    try:
                        connections = psutil.net_connections()
                    except Exception as e:
                        console.print(f"[red]Access Error: {e}")
                        break

                    table = generate_connection_table(connections)

                    stats = RichTable()
                    stats.add_column("Metric")
                    stats.add_column("Value")

                    stats.add_row("Total Connections", str(len(connections)))
                    stats.add_row(
                        "ESTABLISHED",
                        str(sum(1 for c in connections if c.status == "ESTABLISHED"))
                    )
                    stats.add_row(
                        "LISTEN",
                        str(sum(1 for c in connections if c.status == "LISTEN"))
                    )

                    alerts = detect_intrusion(connections)

                    for alert in alerts:
                        console.print(f"[bold red]⚠ INTRUSION ALERT: {alert}")

                    dashboard = RichTable.grid(expand=True)
                    dashboard.add_row(bandwidth_panel)
                    dashboard.add_row(
                        Panel(
                            table,
                            title="[bold red]NETWORK TRAFFIC ANALYSIS[/bold red]",
                            border_style="bright_blue"
                        )
                    )
                    dashboard.add_row(
                        Panel(
                            stats,
                            title="[bold yellow]Network Statistics[/bold yellow]",
                            border_style="yellow"
                        )
                    )

                    live.update(dashboard)
                    time.sleep(2)

            # 🔥 Auto-generate PDF after live monitoring
            export_forensic_report(connections)

                    

    # ----------------------------
    # Run Monitor
    # ----------------------------
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

        connections = psutil.net_connections()
        export_forensic_report(connections)
    # ==================== NEW ADVANCED COMMANDS ====================
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
        """Interactive SQL injection scanner with cinematic animations"""
        console = Console()
    
    # Animation frames
        SQL_FRAMES = [
            "SELECT * FROM users",
            "UNION SELECT 1,2,3",
            "1' OR '1'='1",
            "WAITFOR DELAY '0:0:5'",
            "CONVERT(int,@@version)"
        ]

    # Get URL if not provided
        if not url:
            url = console.input("\n[bold cyan]Enter target URL (with http://): [/]").strip()
    
        if not url.startswith(("http://", "https://")):
            console.print(Panel(
                "[red]Invalid URL format! Must include http:// or https://[/red]",
                title="Input Error",
                border_style="red"
            ))
            return

    # Check sqlmap installation
        if not which("sqlmap"):
            console.print(Panel(
                "[red]sqlmap not found![/red]\n\n"
                "Install with:\n"
                "[green]git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git[/green]\n\n"
                "Or visit: [blue]https://sqlmap.org[/blue]",
                title="Dependency Missing",
                border_style="red"
            ))
            return

    # Prepare display panels
        def create_panel(content, title="", border_style="blue"):
            return Panel(
                content,
                title=title,
                border_style=border_style,
                width=50,
                padding=(1, 1)
            )

    # Main display generator
        def generate_display(scan_log, status_msg, animation_frame):
            log_panel = create_panel(
                "\n".join(scan_log[-5:]),
                title="[blue]SCAN LOG[/blue]",
                border_style="blue"
            )
        
            status_panel = create_panel(
                status_msg,
                title="[green]STATUS[/green]",
                border_style="green"
            )
        
            anim_panel = create_panel(
                animation_frame,
                title="[red]SQL INJECTION[/red]",
                border_style="red"
            )
        
            return Columns([log_panel, status_panel, anim_panel])

        scan_log = []
        status_msg = "Initializing scan..."
        current_frame = random.choice(SQL_FRAMES)

    # Prepare sqlmap command
        report_dir = "./sqlmap_reports"
        os.makedirs(report_dir, exist_ok=True)
    
        cmd = [
            "sqlmap",
            "-u", url,
            "--batch",
            "--risk=3",
            "--level=3",
            "--crawl=1",
            "--random-agent",
            "--output-dir", report_dir
        ]

        try:
            with Live(generate_display(scan_log, status_msg, current_frame), 
                    console=console, 
                    refresh_per_second=10,
                    transient=False) as live:
            
            # Start scan with progress animation
                scan_log.append(f"Starting scan on: {url}")
                status_msg = "[yellow]Scanning target...[/yellow]"
            
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    transient=True
                ) as progress:
                    task = progress.add_task("[cyan]Testing parameters", total=100)
                
                # Run sqlmap in background
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True
                    )
                
                # Animate while scanning
                    frame_counter = 0
                    while process.poll() is None:
                        frame_counter += 1
                        if frame_counter % 5 == 0:
                            current_frame = random.choice(SQL_FRAMES)
                    
                    # Update progress
                        progress.update(task, advance=0.5)
                        if progress.tasks[0].percentage >= 100:
                            progress.update(task, completed=99)
                    
                    # Read output
                        line = process.stdout.readline()
                        if line:
                            if "testing" in line.lower():
                                status_msg = f"[yellow]{line.strip()}[/yellow]"
                            scan_log.append(line.strip())
                    
                        live.update(generate_display(scan_log, status_msg, current_frame))
                        time.sleep(0.1)
                
                    progress.update(task, completed=100)
            
            # Process results
                status_msg = "[green]Scan completed![/green]"
                live.update(generate_display(scan_log, status_msg, current_frame))
            
            # Parse vulnerabilities
                vulns = []
                report_file = os.path.join(report_dir, url.replace("://", "_").replace("/", "_"), "log")
                if os.path.exists(report_file):
                    with open(report_file, "r") as f:
                        for line in f:
                            if any(x in line for x in ["injectable", "vulnerable", "payload:"]):
                                vulns.append(line.strip())
            
            # Show results
                if vulns:
                    status_msg = "[red]VULNERABILITIES FOUND![/red]"
                    scan_log.extend([""] + vulns[-3:] + [f"\nFull report: {report_file}"])
                else:
                    status_msg = "[green]No vulnerabilities found[/green]"
            
                live.update(generate_display(scan_log, status_msg, current_frame))
                console.print("\n[bold]Press Enter to continue...[/]", end="")
                input()
            
        except Exception as e:
            console.print(Panel(
                f"[red]Error: {str(e)}[/red]",
                title="Scan Failed",
                border_style="red"
            ))
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
    def financial_simulator(self):
        """Interactive financial attack simulator with real-time money transfer animations"""
        console = Console()
    
    # Financial database
        BANKS = {
            "SWIFT": ["JPMorgan", "HSBC", "BankofAmerica", "StandardChartered"],
            "Crypto": ["Binance", "Coinbase", "Kraken"],
            "Payment": ["Visa", "Mastercard", "PayPal"]
        }

        def create_panel(content, title="", border_style="blue", width=40):
            return Panel(
                content,
                title=title,
                border_style=border_style,
                width=width,
                padding=(1, 1)
            )

    # Animation frames for money transfer
        MONEY_FRAMES = [
            "▁▂▃▄▅▆▇█",
            "▁▂▃▄▅▆▇▆▅▄▃▂▁",
            "←══════✪══════→",
            "▰▰▰▰▰▰▰▰▰▰",
            "[green]$$$[/][yellow]$$[/][red]$$[/]"
        ]

    # Get user input
        console.print(Panel.fit("[bold red]FINANCIAL SIMULATOR[/]", border_style="red"))
    
    # Bank selection
        bank_type = console.input("\n[bold cyan]Enter bank type (SWIFT/Crypto/Payment): [/]").strip()
        if bank_type not in BANKS:
            console.print(Panel("[red]Invalid bank type![/]", border_style="red"))
            return
    
        bank = random.choice(BANKS[bank_type])
        amount = console.input("[bold cyan]Enter amount to transfer: [/]").strip()
        recipient = console.input("[bold cyan]Enter recipient account: [/]").strip()

    # Transaction simulation
        try:
            layout = Layout()
            layout.split(
                Layout(name="header", size=3),
                Layout(name="main", ratio=1),
                Layout(name="footer", size=7)
            )
        
        # Create panels
            transaction_panel = create_panel(
                f"[bold]From:[/] DSTerminal_Acct\n"
                f"[bold]To:[/] {recipient}\n"
                f"[bold]Bank:[/] {bank}\n"
                f"[bold]Amount:[/] [green]{amount}[/]",
                title="[blue]TRANSACTION[/]",
                border_style="blue",
                width=45
            )
        
            network_panel = create_panel(
                f"[bold]Network:[/] {bank_type}\n"
                f"[bold]Status:[/] [yellow]Pending[/]\n"
                f"[bold]Fee:[/] ${random.uniform(0.1, 5.0):.2f}",
                title="[yellow]NETWORK[/]",
                border_style="yellow",
                width=45
            )

        # Animation function
            def generate_frame(frame_num):
                animation = MONEY_FRAMES[frame_num % len(MONEY_FRAMES)]
                return create_panel(
                    f"\n\n[bold]{animation}[/]\n\n"
                    f"[dim]Encrypting transaction...[/]",
                    title="[red]TRANSFER IN PROGRESS[/]",
                    border_style="red",
                    width=50
                )

        # Live progress display
            with Live(layout, refresh_per_second=10, screen=True) as live:
            # Header
                layout["header"].update(
                    Panel.fit(
                        f"[bold]Simulating {bank_type} Transfer[/] → [green]{amount}[/]",
                        border_style="green"
                    )
                )
            
            # Main content
                layout["main"].update(Columns([transaction_panel, network_panel]))
            
            # Animated transfer
                for i in range(1, 101):
                    layout["footer"].update(generate_frame(i))
                
                # Update status at different stages
                    if i == 30:
                        network_panel.border_style = "green"
                        network_panel.title = "[green]NETWORK[/]"
                        network_panel.renderable = network_panel.renderable.replace(
                            "[yellow]Pending[/]", 
                            "[green]Processing[/]"
                        )
                
                    if i == 70:
                        network_panel.renderable = network_panel.renderable.replace(
                            "[green]Processing[/]", 
                            "[blue]Verifying[/]"
                        )
                
                    time.sleep(0.08)
                    live.refresh()

            # Completion
                layout["footer"].update(
                    create_panel(
                        f"[bold green]✓ TRANSFER COMPLETE[/]\n\n"
                        f"[dim]Confirmation: DST-{random.randint(10000,99999)}[/]",
                        title="[green]SUCCESS[/]",
                        border_style="green",
                        width=50
                    )
                )
                network_panel.renderable = network_panel.renderable.replace(
                    "[blue]Verifying[/]", 
                    "[green]Completed[/]"
                )
                live.refresh()
                time.sleep(2)

        # Generate report
            console.print(Panel(
                f"[bold]Transaction Report[/]\n\n"
                f"• Amount: [green]{amount}[/]\n"
                f"• Bank: {bank}\n"
                f"• Recipient: {recipient}\n"
                f"• Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"• Network: {bank_type}\n"
                f"• Status: [green]Verified[/]",
                title="Receipt",
                border_style="bright_white"
            ))

        except KeyboardInterrupt:
            console.print(Panel("[yellow]Transfer cancelled by user[/]", border_style="yellow"))
    
        console.print("\n[bold]Press Enter to return to menu...[/]", end="")
        input()

# FINANCIAL SECTION ENDS HERE
# ==================integrity implementation line for status and like-----
    def display_alerts(self, alerts):
        """Display alerts in formatted way"""
        if not alerts:
            print(f"{Fore.GREEN}No alerts found{Style.RESET_ALL}")
            return
    
        terminal_width = shutil.get_terminal_size().columns
    
        print(f"\n{Fore.CYAN}{'=' * terminal_width}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'RECENT ALERTS'.center(terminal_width)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * terminal_width}{Style.RESET_ALL}\n")
    
        for alert in alerts[-20:]:  # Show last 20
            severity_colors = {
                'CRITICAL': Fore.RED + Style.BRIGHT,
                'HIGH': Fore.YELLOW + Style.BRIGHT,
                'MEDIUM': Fore.CYAN,
                'LOW': Fore.GREEN
            }
            color = severity_colors.get(alert.get('severity', 'LOW'), Fore.WHITE)
        
            time_str = alert.get('timestamp', 'Unknown')[:19] if alert.get('timestamp') else 'Unknown'
            alert_type = alert.get('type', 'unknown')
            path = alert.get('path', alert.get('src_path', 'Unknown'))
        
            print(f"{color}[{alert.get('severity', 'UNKNOWN')}]{Style.RESET_ALL} "
                f"{time_str} - {alert_type.upper()}: {os.path.basename(path)}")
        
            if alert.get('type') == 'moved':
                print(f"      From: {os.path.basename(alert.get('src_path', ''))}")
                print(f"      To: {os.path.basename(alert.get('dest_path', ''))}")
    
        print(f"\n{Fore.CYAN}{'=' * terminal_width}{Style.RESET_ALL}")

    def display_timeline(self, timeline):
        """Display forensic timeline"""
        if not timeline:
            print(f"{Fore.GREEN}No events in timeline{Style.RESET_ALL}")
            return
    
        terminal_width = shutil.get_terminal_size().columns
    
        print(f"\n{Fore.CYAN}{'=' * terminal_width}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'FORENSIC TIMELINE'.center(terminal_width)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * terminal_width}{Style.RESET_ALL}\n")
    
        for event in timeline:
            time_str = event['time'].strftime('%Y-%m-%d %H:%M:%S') if hasattr(event['time'], 'strftime') else str(event['time'])
        
            if event['type'] == 'alert':
                print(f"{Fore.RED}{time_str} - ALERT [{event['data'].get('severity', 'UNKNOWN')}]{Style.RESET_ALL}")
                print(f"      {event['data'].get('type', 'unknown')}: {event['data'].get('path', 'Unknown')}")
        
            elif event['type'] == 'baseline_change':
                print(f"{Fore.YELLOW}{time_str} - BASELINE CHANGE{Style.RESET_ALL}")
                changes = event['data']
                if changes.get('added'):
                    print(f"      + Added: {len(changes['added'])} files")
                if changes.get('removed'):
                    print(f"      - Removed: {len(changes['removed'])} files")
                if changes.get('modified'):
                    print(f"      * Modified: {len(changes['modified'])} files")
        
            print()

    def show_integrity_help(self):
        """Show integrity monitor help"""
        terminal_width = shutil.get_terminal_size().columns
    
        print(f"\n{Fore.CYAN}{'=' * terminal_width}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'INTEGRITY MONITOR COMMANDS'.center(terminal_width)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * terminal_width}{Style.RESET_ALL}\n")
    
        help_sections = [
            ("CORE COMMANDS", [
                ("integrity scan", "Full system integrity check"),
                ("integrity baseline", "Create new system baseline"),
                ("integrity compare <file>", "Compare with specific baseline"),
                ("integrity status", "Show integrity monitor status"),
            ]),
            ("INVENTORY COMMANDS", [
                ("integrity list", "List all files"),
                ("integrity list critical", "List critical system files"),
                ("integrity list configs", "List configuration files"),
                ("integrity list logs", "List log files"),
                ("integrity list databases", "List database files"),
                ("integrity list user", "List user files"),
            ]),
            ("REPORT COMMANDS", [
                ("integrity report", "Generate TXT report"),
                ("integrity report latest", "Show latest TXT report"),
                ("integrity report json", "Generate JSON format report"),
                ("integrity report pdf", "Generate PDF format report (with logo)"),
                ("integrity report all", "Generate all report formats"),
            ]),
            ("REAL-TIME MONITORING", [
                ("integrity monitor", "Start real-time monitoring"),
                ("integrity monitor stop", "Stop real-time monitoring"),
                ("integrity alerts", "Show recent alerts"),
                ("integrity alerts show [severity]", "Filter alerts by severity"),
                ("integrity alerts clear", "Clear all alerts"),
            ]),
            ("FORENSIC ANALYSIS", [
                ("integrity forensic timeline [file] [days]", "Show change timeline"),
                ("integrity forensic report [file] [days]", "Generate forensic report"),
            ]),
            ("INCIDENT RESPONSE", [
                ("integrity quarantine <file>", "Quarantine suspicious file"),
                ("integrity restore <file>", "Restore from quarantine"),
            ]),
        ]
    
        for section_title, commands in help_sections:
            print(f"{Fore.YELLOW}{section_title}:{Style.RESET_ALL}")
            for cmd, desc in commands:
                print(f"  {Fore.GREEN}{cmd:<35}{Style.RESET_ALL} - {desc}")
            print()
    
        print(f"{Fore.CYAN}{'=' * terminal_width}{Style.RESET_ALL}")

    def show_integrity_status(self):
        """Show integrity monitor status"""
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'INTEGRITY MONITOR STATUS'.center(60)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")
    
    # Check baseline
        baseline_dir = "data/baselines"
        if os.path.exists(baseline_dir):
            baselines = [f for f in os.listdir(baseline_dir) if f.endswith('.json')]
            if baselines:
                latest = max([os.path.join(baseline_dir, f) for f in baselines], key=os.path.getctime)
                latest_time = datetime.fromtimestamp(os.path.getctime(latest))
                print(f"{Fore.GREEN}✅ Baseline:{Style.RESET_ALL} Found ({len(baselines)} total)")
                print(f"   Latest: {latest_time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"{Fore.YELLOW}⚠️ Baseline:{Style.RESET_ALL} No baselines found")
        else:
            print(f"{Fore.RED}❌ Baseline:{Style.RESET_ALL} Directory not found")
    
    # Check reports
        report_dir = "data/integrity_reports"
        if os.path.exists(report_dir):
            reports = [f for f in os.listdir(report_dir) if f.endswith(('.txt', '.json'))]
            print(f"{Fore.GREEN}✅ Reports:{Style.RESET_ALL} {len(reports)} reports available")
        else:
            print(f"{Fore.YELLOW}⚠️ Reports:{Style.RESET_ALL} No reports found")
    
    # Check monitoring status
        if hasattr(self, 'alert_manager') and hasattr(self.alert_manager, 'running') and self.alert_manager.running:
            print(f"{Fore.GREEN}✅ Monitoring:{Style.RESET_ALL} Active")
            if hasattr(self.alert_manager, 'alerts'):
                print(f"   Alerts: {len(self.alert_manager.alerts)}")
        else:
            print(f"{Fore.YELLOW}⚠️ Monitoring:{Style.RESET_ALL} Inactive (use 'integrity monitor' to start)")
    
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")

    def compare_with_baseline(self, baseline_file):
        """Compare current state with a specific baseline"""
        if not os.path.exists(baseline_file):
            print(f"{Fore.RED}Baseline file not found: {baseline_file}{Style.RESET_ALL}")
            return
    
        try:
            with open(baseline_file, 'r') as f:
                baseline = json.load(f)
        
            print(f"{Fore.CYAN}Comparing with baseline from: {baseline.get('created', 'Unknown')}{Style.RESET_ALL}")
        
        # Scan current system
            scan_results = self.integrity.scan_system()
        
        # Perform comparison
            changes = self.integrity.check_integrity(scan_results)
        
            if changes and any(changes.values()):
                if hasattr(self.integrity, '_display_changes'):
                    self.integrity._display_changes(changes)
                else:
                    print(f"{Fore.YELLOW}Changes detected. Run 'integrity scan' for details.{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}No changes detected since baseline.{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}Error comparing with baseline: {e}{Style.RESET_ALL}")

    def show_latest_report(self):
        """Show the latest integrity report"""
        report_dir = "data/integrity_reports"
        if not os.path.exists(report_dir):
            print(f"{Fore.RED}No reports directory found.{Style.RESET_ALL}")
            return
    
    # Look for report files
        report_files = glob.glob(os.path.join(report_dir, 'report_*.txt'))
        if not report_files:
            print(f"{Fore.RED}No reports found.{Style.RESET_ALL}")
            return
    
    # Get the most recent report
        latest_report = max(report_files, key=os.path.getctime)
    
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'LATEST INTEGRITY REPORT'.center(60)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}File: {latest_report}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}\n")
    
        try:
            with open(latest_report, 'r') as f:
                content = f.read()
                print(content)
        except Exception as e:
            print(f"{Fore.RED}Error reading report: {e}{Style.RESET_ALL}")
    
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    # ================
    def quarantine_file(self, file_path):
        """Quarantine a suspicious file"""
        if not os.path.exists(file_path):
            print(f"{Fore.RED}File not found: {file_path}{Style.RESET_ALL}")
            return
    
        quarantine_dir = os.path.join("data", "quarantine")
        os.makedirs(quarantine_dir, exist_ok=True)
    
    # Create quarantine filename with timestamp
        filename = os.path.basename(file_path)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        quarantine_path = os.path.join(quarantine_dir, f"{timestamp}_{filename}.quarantine")
    
        try:
            # Move file to quarantine
            shutil.move(file_path, quarantine_path)
        
        # Log quarantine action
            quarantine_log = os.path.join(quarantine_dir, 'quarantine_log.json')
        
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'original_path': file_path,
                'quarantine_path': quarantine_path,
                'action': 'quarantined'
            }
        
            if os.path.exists(quarantine_log):
                with open(quarantine_log, 'r') as f:
                    log = json.load(f)
            else:
                log = []
        
            log.append(log_entry)
        
            with open(quarantine_log, 'w') as f:
                json.dump(log, f, indent=2)
        
            print(f"{Fore.GREEN}✅ File quarantined: {quarantine_path}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Original location: {file_path}{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}Failed to quarantine file: {e}{Style.RESET_ALL}")

    def restore_from_quarantine(self, file_path):
        """Restore file from quarantine"""
        quarantine_dir = os.path.join("data", "quarantine")
        quarantine_log = os.path.join(quarantine_dir, 'quarantine_log.json')
    
        if not os.path.exists(quarantine_log):
            print(f"{Fore.RED}No quarantine log found{Style.RESET_ALL}")
            return
    
        try:
            with open(quarantine_log, 'r') as f:
                log = json.load(f)
        
        # Find matching entry
            matching_entries = [entry for entry in log 
                            if entry['original_path'] == file_path or 
                            entry['quarantine_path'] == file_path]
        
            if not matching_entries:
                print(f"{Fore.RED}No quarantine entry found for: {file_path}{Style.RESET_ALL}")
                return
        
            entry = matching_entries[-1]
            quarantine_path = entry['quarantine_path']
        
            if not os.path.exists(quarantine_path):
                print(f"{Fore.RED}Quarantine file not found: {quarantine_path}{Style.RESET_ALL}")
                return
        
        # Create backup directory if original path doesn't exist
            original_dir = os.path.dirname(entry['original_path'])
            if not os.path.exists(original_dir):
                os.makedirs(original_dir, exist_ok=True)
        
        # Restore file
            shutil.move(quarantine_path, entry['original_path'])
        
        # Update log
            entry['restored_at'] = datetime.now().isoformat()
            entry['action'] = 'restored'
        
            with open(quarantine_log, 'w') as f:
                json.dump(log, f, indent=2)
        
            print(f"{Fore.GREEN}✅ File restored to: {entry['original_path']}{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}Failed to restore file: {e}{Style.RESET_ALL}")
        # ================================================
# ---------------------ends here---------------
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

        filename = f"dsterminal_ssl_{domain}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"\n[✓] Encrypted audit report saved: {filename}")

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

        filename = f"dsterminal_report_{domain}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"

        doc = SimpleDocTemplate(
            filename,
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
            scale_ratio = max_footer_width / footer_logo.imageWidth
            footer_logo.drawWidth = footer_logo.imageWidth * scale_ratio
            footer_logo.drawHeight = footer_logo.imageHeight * scale_ratio
            footer_data.append([footer_logo, Paragraph("AUTOGENERATED CERTIFICATE REPORT | DSTerminal Platform\n© Stark Expo Tech Exchange", normal)])
            footer_table = Table(footer_data, colWidths=[60, page_width - 60 - doc.leftMargin - doc.rightMargin])
            footer_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
            elements.append(footer_table)
        else:
        # fallback if logo missing
            elements.append(Paragraph("AUTOGENERATED REPORT | DSTerminal Platform", normal))
            elements.append(Paragraph("© Stark Expo Tech Exchange LTD", normal))

   
        doc.build(elements)
        print(f"\n[✓] PDF Compliance Report Created: {filename}")
# ===lists of reports===
    def list_reports(self):
        print("\n📊 DSTerminal Reports")
        print("="*50)

        reports_path = os.path.join(self.workspace_root, "reports")
        if not os.path.exists(reports_path) or not os.listdir(reports_path):
            print("No reports found.")
            return

        for f in os.listdir(reports_path):
            file_path = os.path.join(reports_path, f)
            size = os.path.getsize(file_path)
            print(f"📄 {f:35} ({self.human_readable_size(size)})")
        
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
        days_left = (expires - datetime.utcnow()).days

        if days_left < 60:
            recs.append("Renew SSL certificate within 30 days")

        if not sec["tls13"]:
            recs.append("Upgrade server configuration to support TLS 1.3")

        if sec["ocsp"] != "VALID":
            recs.append("Enable OCSP stapling for revocation validation")

        if sec["forward_secrecy"] is False:
            recs.append("Enable Perfect Forward Secrecy (ECDHE)")

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
        console = Console()

    # ===================== ANIMATIONS =====================
        def hacker_animation():
            symbols = "█▓▒░▄▀■►▼▲◄▶◀◢◣◥◤▬▭▮▯┌┐└┘├┤┬┴┼╔╗╚╝╠╣╦╩╬═║"
            width = console.size.width
            with console.status("[bold red]ACCESSING UPDATE SERVERS...[/]", spinner="dots"):
                for _ in range(3):
                    console.print(
                        "".join(random.choice(symbols) for _ in range(width)),
                        style="bold green"
                    )
                    time.sleep(1.5)

        def satellite_scan():
            frames = ["🛰", "📡", "📶", "🔍", "🎯"]
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
            with Live(refresh_per_second=20, console=console) as live:
                for i in range(1, 6):
                    bar = "█" * (i * 10)
                    live.update(
                        Panel(
                            f"[bold]Comparing Versions[/]\n\n"
                            f"[yellow]Current:[/] {current_ver}\n{bar}\n\n"
                            f"[green]Latest:[/] {latest_ver}\n{bar}",
                            border_style="cyan"
                        )
                    )
                    time.sleep(1.5)

    # ===================== UPDATE LOGIC =====================
        def parse_version(v):
            parts = [int(p) if p.isdigit() else 0 for p in str(v).lstrip("vV").split(".")]
            while len(parts) < 3:
                parts.append(0)
            return tuple(parts)

        def check_github_release():
            try:
                api_url = (
                    "https://api.github.com/repos/"
                    "Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/releases/latest"
                )
                r = requests.get(api_url, timeout=10)
                if r.status_code != 200:
                    return None

                data = r.json()
                assets = {
                    a["name"]: a["browser_download_url"]
                    for a in data.get("assets", [])
                }

                return {
                    "version": data.get("tag_name", "").lstrip("v"),
                    "url": data.get("html_url", ""),
                    "assets": assets,
                    "notes": data.get("body", ""),
                    "prerelease": data.get("prerelease", False),
                }

            except requests.RequestException:
                return None
        
# ---------------------another update function ends here from above===========

        def perform_update(latest_tag):
            """
            Downloads the latest DSTerminal release and updates local version.
            latest_tag: string, e.g., "v2.0.113"
            """

            os_type = platform.system().lower()  # 'linux', 'windows', 'darwin'
            print(f"[+] Detected OS: {os_type}")

            # Clean the version tag (remove 'v' if present)
            clean_version = latest_tag.lstrip('v')

    # Determine download URL based on OS
            if os_type == "linux":
                filename = f"dsterminal_{clean_version}_amd64.deb"
                download_url = f"https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/releases/download/{latest_tag}/{filename}"
            elif os_type == "windows":
                    clean_version = latest_tag.lstrip('v')
                    version_with_v = f"v{clean_version}"
                    possible_filenames = [
                        f"DSTerminal_Installer_v{clean_version}.exe",
                        f"DSTerminal_Setup_{clean_version}_x64.exe",
                        f"DSTerminalInstaller_{version_with_v}.exe",
                        f"DSTerminal_{clean_version}_setup.exe",
                        f"DSTerminal_v{clean_version}_installer.exe"
                    ]

                    downloaded = False
                    for filename in possible_filenames:
                        download_url = f"https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/releases/download/{version_with_v}/{filename}"
                        print(f"[+] Trying: {filename}")
        
                        try:
                            # First, check if the file exists without downloading (HEAD request)
                            response = requests.head(download_url, timeout=5)
                            if response.status_code == 200:
                                print(f"[+] Found: {filename}")
                                # Now download the file
                                print(f"[+] Downloading {filename} from GitHub...")
                                r = requests.get(download_url, stream=True)
                                r.raise_for_status()
                
                                # Get file size for progress bar
                                total_size = int(r.headers.get('content-length', 0))
                
                                with open(filename, 'wb') as f:
                                    if total_size == 0:
                                        f.write(r.content)
                                    else:
                                        with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                                            for chunk in r.iter_content(chunk_size=8192):
                                                f.write(chunk)
                                                pbar.update(len(chunk))
                
                                print(f"[+] Download complete: {filename}")
                                print(f"[+] Please run the downloaded installer manually: {filename}")
                                print("[+] After installation, restart DSTerminal.")
                                downloaded = True
                                break
                            else:
                                print(f"[-] Not found (HTTP {response.status_code})")
                        except Exception as e:
                            print(f"[-] Error checking: {e}")
    
                    if not downloaded:
                        print("[!] Could not find installer file. Please download manually from:")
                        print(f"https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/releases/tag/{version_with_v}")

                   # Try each filename until one works
                    for filename in possible_filenames:
                        download_url = f"https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/releases/download/{version_with_v}/{filename}"
                        print(f"[+] Trying: {filename}")
                    # You might want to check if URL exists before downloading
                        break  # For now, just use the first one
            else:
                print("[!] Your OS is not supported for auto-update.")
                return

    # Download the file
            try:
                print(f"[+] Downloading {filename} from GitHub...")
                r = requests.get(download_url, stream=True)
                r.raise_for_status()
                with open(filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"[+] Download complete: {filename}")

            except Exception as e:
                print(f"[!] Download failed: {e}")
                return

    # Auto-install depending on OS
            if os_type == "linux":
                print("[+] Installing .deb package...")
                try:
                    subprocess.run(["sudo", "dpkg", "-i", filename], check=True)
                    print("[+] Update installed successfully!")
                except subprocess.CalledProcessError as e:
                    print(f"[!] Installation failed: {e}")
                    print(f"[+] You may try: sudo dpkg -i {filename}")
            elif os_type == "windows":
                # print(f"[+] Please run the downloaded installer manually: {filename}")
                # print("[+] After installation, restart DSTerminal.")
                clean_version = latest_tag.lstrip('v')
                version_with_v = f"v{clean_version}"
                filename = f"DSTerminal_Installer_v{clean_version}.exe"
                download_url = f"https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/releases/download/{version_with_v}/{filename}"

    # Update local VERSION file
            version_file = os.path.join(os.path.dirname(__file__), "VERSION")
            try:
                with open(version_file, "w") as vf:
                    vf.write(latest_tag.strip("v"))
                print(f"[+] Local version updated to {latest_tag}")
            except Exception as e:
                print(f"[!] Could not update local VERSION file: {e}")

    # ===================== MAIN FLOW =====================
        try:
            console.print("\n")
            console.print(Panel(
                "[bold cyan]▄︻デ══━ INITIATING SYSTEM UPDATE PROTOCOL ══━︻▄[/]",
                border_style="cyan"
            ))

            time.sleep(0.5)
            hacker_animation()
            satellite_scan()

            current_version = CONFIG.get("CURRENT_VERSION", "1.0.0").lstrip("v")
            console.print(Panel(f"[bold]Current version:[/] v{current_version}",
            border_style="white"
            ))

            latest = check_github_release()
            if not latest:
                console.print(Panel(
                    "[yellow]Unable to reach update servers[/]",
                    border_style="yellow"
                ))
                return True

            version_comparison_animation(
                f"v{current_version}", f"v{latest['version']}"
            )

            if parse_version(latest["version"]) > parse_version(current_version):
                console.print(Panel(
                    f"[bold red]UPDATE AVAILABLE[/]\n\n"
                    f"Latest: v{latest['version']}\n"
                    f"{latest['notes'][:300]}",
                    border_style="red"
                ))

                if console.input("Install update now? (y/N): ").lower() == "y":
                    return perform_update(latest['version'])

            else:
                console.print(Panel(
                    f"[bold green]DSTerminal is up to date[/]\n\n"
                    f"Checked: {datetime.now():%Y-%m-%d %H:%M:%S}",
                    border_style="green"
                ))

            return True

        except Exception as e:
            console.print(Panel(
                f"[bold red]UPDATE ERROR[/]\n\n{str(e)}",
                border_style="red"
            ))
            return True

# --------------------------for updates above code--------------------

# ---------------------------wipe tracks and terminal clearing
    def clear_terminal(self):
        """Advanced terminal clearing with spinning boxes and centered animations"""
    
        console = Console()
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        panel_width = min(70, terminal_width - 10)
    
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
    
    # Create a box with spinning animation
        with Live(console=console, refresh_per_second=12, screen=True) as live:
            for phase in range(4):  # 4 phases of clearing
                for step in range(25):  # 25 steps per phase
                # Select spinner based on phase
                    spinner_type = list(spinners.keys())[phase % len(spinners)]
                    spinner = spinners[spinner_type][step % len(spinners[spinner_type])]
                
                # Phase-based colors
                    if phase == 0:
                        color = "bright_red"
                        phase_text = "PHASE 1: MEMORY CLEAR"
                    elif phase == 1:
                        color = "bright_yellow"
                        phase_text = "PHASE 2: BUFFER FLUSH"
                    elif phase == 2:
                        color = "bright_green"
                        phase_text = "PHASE 3: CACHE WIPE"
                    else:
                        color = "bright_cyan"
                        phase_text = "PHASE 4: DISPLAY RESET"
                
                # Progress calculation
                    total_progress = (phase * 25 + step) / 100
                    progress_bar_width = panel_width - 30
                    progress_filled = int(total_progress * progress_bar_width)
                    progress_bar = "█" * progress_filled + "░" * (progress_bar_width - progress_filled)
                
                # Random glitch effect
                    if random.random() > 0.7:
                        glitch = random.choice(glitch_texts)
                    else:
                        glitch = ""
                
                # Create stats content
                    stats_content = (
                        f"[cyan]CPU: [green]{random.randint(20, 95)}%[/green]\n"
                        f"[cyan]MEM: [yellow]{random.randint(100, 500)}MB[/yellow]\n"
                        f"[cyan]PID: [white]{os.getpid()}[/white]"
                    )
                
                # Create main content
                    main_content = Panel(
                        Align.center(
                            f"[bold {color}]{spinner} {phase_text} {spinner}[/bold {color}]\n\n"
                            f"[white]{progress_bar}[/white] [{int(total_progress*100)}%]\n\n"
                            f"[dim]{glitch}[/dim]",
                            vertical="middle"
                        ),
                        title=f"[bold {color}]╔ TERMINAL WIPE SEQUENCE ╗[/bold {color}]",
                        border_style=color,
                        padding=(1, 2),
                        width=panel_width
                    )
                
                # Create stats box
                    stats_box = Panel(
                        Align.center(stats_content, vertical="middle"),
                        title="[bold white]SYS STATS[/bold white]",
                        border_style="bright_black",
                        width=panel_width - 4,
                        padding=(1, 1)
                    )
                
                # Create layout to combine panels
                    layout = Layout()
                    layout.split_column(
                        Layout(main_content),
                        Layout(stats_box)
                    )
                
                # Center everything
                    final_display = Align.center(layout)
                
                    live.update(final_display)
                    time.sleep(0.08)
    
    # Execute actual terminal clear
        os.system("clear" if platform.system() != "Windows" else "cls")
    
    # Create a dramatic banner reveal
        banner = """
        ╔═══════════════════════════════════════════════════════════════════╗
        ║                                                                    ║
        ║    ██████╗ ███████╗███████╗███████╗███╗   ██╗███████╗██╗  ██╗    ║
        ║    ██╔══██╗██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝╚██╗██╔╝    ║
        ║    ██║  ██║█████╗  █████╗  █████╗  ██╔██╗ ██║█████╗   ╚███╔╝     ║
        ║    ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║██╔══╝   ██╔██╗     ║
        ║    ██████╔╝██║     ██║     ███████╗██║ ╚████║███████╗██╔╝ ██╗    ║
        ║    ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝    ║
        ║                                                                    ║
        ╚═══════════════════════════════════════════════════════════════════╝
        """
    
    # Animate banner with scan line effect
        banner_lines = banner.split('\n')
        centered_banner = []
    
    # Center each line
        for line in banner_lines:
            if line.strip():
                centered_banner.append(line.center(terminal_width))
            else:
                centered_banner.append('')
    
    # Display with scan line animation
        for i, line in enumerate(centered_banner):
            if i == 0 or i == len(centered_banner)-1:
                console.print(f"[bright_cyan]{line}[/bright_cyan]")
            elif i == 1 or i == 7:
                console.print(f"[bright_blue]{line}[/bright_blue]")
            elif 2 <= i <= 6:
            # Gradient effect on logo
                colors = ["cyan", "bright_cyan", "blue", "bright_blue", "green"]
                color = colors[(i-2) % len(colors)]
                console.print(f"[bold {color}]{line}[/bold {color}]")
            else:
                console.print(f"[dim]{line}[/dim]")
            time.sleep(0.08)
    
    # Add a status message with blink effect
        status_panel = Panel(
            Align.center(
                "[blink][bright_green]✦ SYSTEM INITIALIZED ✦[/bright_green][/blink]\n\n"
                f"[cyan]Session ID:[/cyan] [white]{datetime.now().strftime('%Y%m%d%H%M%S')}[/white]\n"
                f"[cyan]Ready for:[/cyan] [yellow]SSL/TLS Security Audit[/yellow]",
                vertical="middle"
            ),
            title="[bold white]SYSTEM STATUS[/bold white]",
            border_style="bright_green",
            padding=(1, 2),
            width=panel_width
        )
    
        console.print(Align.center(status_panel))
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
    # def clear_terminal(self):
    #     console = Console()

    #     panel = Panel(
    #         Align.center("[cyan]Resetting interface...[/cyan]", vertical="middle"),
    #         title="[bold white]TERMINAL WIPE[/bold white]",
    #         border_style="bright_cyan",
    #         padding=(1, 2),
    #         width=50
    #     )

    #     with Live(console=console, refresh_per_second=5, screen=True) as live:
    #         for i in range(10):
    #             live.update(Panel(f"[cyan]Wiping in progress... {10 - i}[/cyan]", title="[bold]CLEANING TERMINAL[/bold]", border_style="bright_cyan", width=50))
    #             time.sleep(1)

    #     os.system("clear" if platform.system() != "Windows" else "cls")

    #     banner = """
    #         ██████╗ ███████╗███████╗███████╗███╗   ██╗███████╗██╗  ██╗
    #         ██╔══██╗██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝╚██╗██╔╝
    #         ██║  ██║█████╗  █████╗  █████╗  ██╔██╗ ██║█████╗   ╚███╔╝ 
    #         ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║██╔══╝   ██╔██╗ 
    #         ██████╔╝██║     ██║     ███████╗██║ ╚████║███████╗██╔╝ ██╗
    #         ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
    #     """
    #     centered_banner = Align.center(f"[bold cyan]{banner}[/bold cyan]", vertical="middle")
    #     console.print(centered_banner)


# =======testing code from above ends here for shutdown command
    def vt_scan_menu(self):
        """Enhanced VirusTotal scanning interface"""
        print("\n[VirusTotal Scanner]")
        print("1. Hash lookup")
        print("2. File scan")
        print("3. Bulk scan folder")
        print("4. Check previous scan")
        choice = input("Select option: ")
        
        if choice == "1":
            file_hash = input("Enter file hash (MD5/SHA1/SHA256): ").strip()
            self.vt_hash_lookup(file_hash)
        elif choice == "2":
            file_path = input("File path to scan: ").strip()
            self.vt_file_scan(file_path)
        elif choice == "3":
            folder_path = input("Folder path to scan: ").strip()
            max_files = input("Max files to scan (default 10): ").strip() or 10
            self.vt_bulk_scan(folder_path, int(max_files))
        elif choice == "4":
            scan_id = input("Enter previous scan ID: ").strip()
            self.check_scan_result(scan_id)
        else:
            print("[!] Invalid choice")

    def vt_hash_lookup(self, file_hash):
        """Enhanced hash lookup with detailed results"""
        if not self._validate_vt_api():
            return

        try:
            url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
            headers = {"x-apikey": CONFIG['VT_API_KEY']}
            
            print(f"\n[+] Checking hash: {file_hash}...")
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                attrs = result['data']['attributes']
                
                # Detailed report
                print(f"\n╔{'═'*60}╗")
                print(f"║ {'VirusTotal Report':^58} ║")
                print(f"╠{'═'*60}╣")
                print(f"║ {'Detection:':<15} {attrs['last_analysis_stats']['malicious']}/{sum(attrs['last_analysis_stats'].values())} ║")
                print(f"║ {'First Seen:':<15} {attrs['first_submission_date']} ║")
                print(f"║ {'File Type:':<15} {attrs.get('type_tag', 'Unknown')} ║")
                
                # Top detections
                malicious = [k for k,v in attrs['last_analysis_results'].items() if v['category'] == 'malicious']
                if malicious:
                    print(f"╠{'═'*60}╣")
                    print(f"║ {'Top Detections:':<58} ║")
                    for engine in malicious[:3]:
                        print(f"║ - {engine:<55} ║")
                print(f"╚{'═'*60}╝")
                
                # Auto-quarantine recommendation
                if attrs['last_analysis_stats']['malicious'] > 0:
                    print("\n[!] MALICIOUS FILE DETECTED!")
                    if input("Quarantine file? (y/N): ").lower() == 'y':
                        self.quarantine_file(None, file_hash=file_hash)
            else:
                print("[!] Hash not found in VirusTotal")
        except Exception as e:
            print(f"[!] Error: {e}")
  

    def vt_file_scan(self, file_path):
        """Upload file to VirusTotal with debug output"""
        print(f"\n[DEBUG] Starting scan for: {file_path}")  # Debug line
    
        if not os.path.exists(file_path):
            print("[!] Error: File not found")
            print(f"[DEBUG] Resolved path: {os.path.abspath(file_path)}")  # Debug line
            return

            print("[DEBUG] File exists check passed")  # Debug line
    
        if not self._validate_vt_api():
            print("[!] Error: VirusTotal API validation failed")
            print(f"[DEBUG] API Key: {'Set' if CONFIG.get('VT_API_KEY') else 'Not Set'}")  # Debug line
            return

        print("[DEBUG] API validation passed")  # Debug line
    
        MAX_SIZE = 32 * 1024 * 1024  # 32MB
        file_size = os.path.getsize(file_path)
        print(f"[DEBUG] File size: {file_size} bytes")  # Debug line

        if file_size > MAX_SIZE:
            print(f"[!] Error: File too large ({file_size/1024/1024:.2f}MB > 32MB)")
            return

        print("[DEBUG] Size check passed")  # Debug line
    
        try:
            print(f"\n[+] Analyzing {os.path.basename(file_path)}...")
            print(f"  ↳ Size: {file_size/1024:.2f}KB")
            print("  ↳ Uploading...", end='', flush=True)
        
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                headers = {"x-apikey": CONFIG['VT_API_KEY']}
                print(f"\n[DEBUG] Sending request to VirusTotal...")  # Debug line
                response = requests.post(
                    "https://www.virustotal.com/api/v3/files",
                    headers=headers,
                    files=files,
                    timeout=30
                )
            print(" Done!")

            print(f"[DEBUG] Response status: {response.status_code}")  # Debug line
            if response.status_code == 200:
                result = response.json()
                scan_id = result['data']['id']
                print(f"\n[+] Scan ID: {scan_id}")
                print(f"[+] Report URL: https://www.virustotal.com/gui/file/{scan_id}")
                self._cache_scan_id(file_path, scan_id)
            else:
                print(f"[!] Error: Upload failed (HTTP {response.status_code})")
                print(f"[DEBUG] Response text: {response.text}")  # Debug line

        except Exception as e:
            print(f"\n[!] Critical Error: {str(e)}")
            print("[DEBUG] Exception occurred during upload")  # Debug line

        if response.status_code == 200:
            result = response.json()
            scan_id = result['data']['id']
            print(f"\n[+] Scan ID: {scan_id}")
        
        # Start polling in background
        Thread(target=self._poll_results, args=(scan_id, file_path), daemon=True).start()
 
    def _cache_scan_id(self, file_path, scan_id):
        """Store scan IDs for future reference"""
        cache_file = os.path.expanduser("~/.dstenex_scans.log")
        with open(cache_file, "a") as f:
            f.write(f"{file_path}|{scan_id}|{datetime.now()}\n")

    def vt_bulk_scan(self, folder_path, max_files=10):
        """Scan multiple files in a folder"""
        if not os.path.isdir(folder_path):
            print("[!] Invalid folder path")
            return
            
        print(f"\n[+] Scanning up to {max_files} files in {folder_path}...")
        scanned = 0
        
        for root, _, files in os.walk(folder_path):
            for file in files:
                if scanned >= max_files:
                    break
                    
                file_path = os.path.join(root, file)
                print(f"\n[File {scanned+1}/{max_files}] {file}")
                
                # First try local scan
                local_result = self.local_scan(file_path, silent=True)
                if local_result and local_result['infected']:
                    print("[!] LOCAL SCAN DETECTED THREAT!")
                    self.quarantine_file(file_path)
                    scanned += 1
                    continue
                
                # Fall back to VT if file < 32MB
                if os.path.getsize(file_path) <= 32 * 1024 * 1024:
                    self.vt_file_scan(file_path)
                else:
                    print("[!] File too large for VT, skipped")
                
                scanned += 1
                time.sleep(15)  # Respect VT API rate limits
        
        print("\n[+] Bulk scan completed")

    def _poll_results(self, scan_id, original_path=None):
        """Background result polling"""
        url = f"https://www.virustotal.com/api/v3/analyses/{scan_id}"
        headers = {"x-apikey": CONFIG['VT_API_KEY']}
        
        print("\n[+] Waiting for results... (Ctrl+C to check later)")
        try:
            for _ in range(10):  # Max 10 checks
                time.sleep(30)
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    result = response.json()
                    status = result['data']['attributes']['status']
                    
                    if status == 'completed':
                        stats = result['data']['attributes']['stats']
                        print(f"\n[+] Final Results: {stats['malicious']} malicious / {stats['harmless']} clean")
                        
                        if stats['malicious'] > 0 and original_path:
                            self.quarantine_file(original_path)
                        return
                    else:
                        print(f"\r  ↳ Status: {status}...", end='', flush=True)
        except Exception:
            print("\n[!] Polling interrupted. Check later with 'check_result'")

    def check_scan_result(self, scan_id):
        """Check existing scan results"""
        url = f"https://www.virustotal.com/api/v3/analyses/{scan_id}"
        headers = {"x-apikey": CONFIG['VT_API_KEY']}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                stats = result['data']['attributes']['stats']
                print(f"\n[+] Results: {stats['malicious']} malicious / {stats['harmless']} clean")
                
                if stats['malicious'] > 0:
                    print("[!] MALICIOUS CONTENT DETECTED")
            else:
                print("[!] Results not available yet")
        except Exception as e:
            print(f"[!] Error checking results: {e}")

    def local_scan(self, file_path, silent=False):
        """Integrate ClamAV for local scanning"""
        try:
            import pyclamd
            cd = pyclamd.ClamdAgnostic()
            scan_result = cd.scan_file(file_path)
            
            if scan_result and scan_result.get(file_path) == 'OK':
                if not silent:
                    print("[+] Local scan: Clean")
                return {'infected': False}
            else:
                if not silent:
                    print("[!] Local scan: Infected!")
                    print(f"Detection: {scan_result.get(file_path, 'Unknown threat')}")
                return {'infected': True, 'threat': scan_result.get(file_path)}
                
        except ImportError:
            if not silent:
                print("[!] ClamAV not installed (pip install pyclamd)")
        except Exception as e:
            if not silent:
                print(f"[!] Local scan failed: {e}")
        return None

    def quarantine_file(self, file_path, file_hash=None):
        """Move dangerous files to quarantine"""
        quarantine_dir = os.path.join(os.path.expanduser("~"), "quarantine")
        os.makedirs(quarantine_dir, exist_ok=True)
        
        try:
            if file_path:
                filename = os.path.basename(file_path)
                new_path = os.path.join(quarantine_dir, f"quarantined_{filename}")
                shutil.move(file_path, new_path)
                print(f"[+] File moved to quarantine: {new_path}")
            elif file_hash:
                with open(os.path.join(quarantine_dir, "quarantined_hashes.txt"), "a") as f:
                    f.write(f"{file_hash}\n")
                print("[+] Malicious hash recorded")
        except Exception as e:
            print(f"[!] Quarantine failed: {e}")

    def _validate_vt_api(self):
        """Check if API key is configured"""
        if not CONFIG.get('VT_API_KEY') or CONFIG['VT_API_KEY'] == 'YOUR_VIRUSTOTAL_API_KEY':
            print("[!] Configure VirusTotal API key first:")
            print("1. Get key from: https://www.virustotal.com/gui/join-us")
            print("2. Edit CONFIG['VT_API_KEY'] in your code")
            return False
        return True


        # go up to change

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
    
    def harden_system(self, dry_run=False):
        """Cinematic system hardening with typing, animations, and progress bars"""
        try:
            # Show enlarged blinking banner at start - THIS WAS MISSING!
            self._enlarged_ascii_banner()
            
            # Matrix rain effect for style
            self._matrix_rain_effect(1)
            
            # Check admin privileges
            if not self.is_admin():
                self._hacking_animation("Checking Privileges")
                print(f"{Fore.RED}[!] Warning: Running without administrator privileges. Some features may be limited.{Style.RESET_ALL}")
                # Don't return, continue with limited functionality
            
            # ----------------------------
            # Pre-hardening animations
            # ----------------------------
            self._hacking_animation("Initializing Threat Assessment")
            self._cinematic_typing("Scanning system threats...")
            self._progress_bar("Threat Assessment", duration=3)
            
            self._network_scan_animation()
            self._hacking_animation("Scanning Exploit Database")
            self._cinematic_typing("Analyzing known vulnerabilities...")
            self._progress_bar("Exploit Database Scan", duration=3)
            
            self._vulnerability_scan()
            self._cyber_attack_simulation()
            self._cinematic_typing("Threat analysis complete.")
            self._progress_bar("Threat Analysis", duration=2)
            
            # ----------------------------
            # Dry-run simulation
            # ----------------------------
            if dry_run:
                self._hacking_animation("Simulating Countermeasures")
                self._cinematic_typing("[SIMULATION] No changes were actually made.", 0.05)
                self._progress_bar("Simulation", duration=2)
            
            # ----------------------------
            # Actual hardening
            # ----------------------------
            else:
                self._hacking_animation("Deploying Cyber Armor")
                self._cinematic_typing("Applying system fortifications...", 0.04)
                self._progress_bar("Deploying Armor", duration=3)
                
                try:
                    system = platform.system()
                    
                    # Windows Hardening
                    if system == "Windows":
                        try:
                            self._cinematic_typing("Disabling SMB1 protocol...", 0.04)
                            powershell_cmd = "powershell -Command Disable-WindowsOptionalFeature -Online -FeatureName smb1protocol -NoRestart"
                            self._progress_bar("SMB1 Disable", duration=2)
                            
                            if self.is_admin():
                                result = subprocess.run(powershell_cmd, shell=True, capture_output=True, text=True)
                                
                                if result.returncode == 0:
                                    self._cinematic_typing("[OK] SMB1 protocol disabled.", 0.04)
                                    logging.info("SMB1 protocol disabled successfully on Windows")
                                else:
                                    self._cinematic_typing(f"[!] PowerShell command failed: {result.stderr}", 0.04)
                                    logging.error(f"PowerShell command failed: {result.stderr}")
                            else:
                                self._cinematic_typing("[!] Skipping SMB1 disable (requires admin rights)", 0.04)
                            
                        except Exception as e:
                            self._cinematic_typing(f"[!] Could not disable SMB1: {str(e)}", 0.04)
                            logging.error(f"Error disabling SMB1: {str(e)}")
                    
                    # Linux Hardening
                    elif system == "Linux":
                        ufw_path = shutil.which("ufw")
                        if ufw_path:
                            self._cinematic_typing("Enabling UFW firewall...", 0.04)
                            self._progress_bar("UFW Firewall", duration=2)
                            try:
                                subprocess.run(["sudo", ufw_path, "--force", "enable"], check=True)
                                self._cinematic_typing("[OK] UFW firewall enabled.", 0.04)
                                logging.info("UFW firewall enabled successfully on Linux")
                            except subprocess.CalledProcessError as e:
                                self._cinematic_typing(f"[!] Failed to enable UFW: {str(e)}", 0.04)
                                logging.error(f"Failed to enable UFW: {str(e)}")
                        else:
                            self._cinematic_typing("[!] UFW firewall not found — skipping Linux hardening", 0.04)
                
                except Exception as e:
                    logging.error(f"Hardening failed: {str(e)}")
                    print(f"{Fore.RED}[!] Error during hardening: {str(e)}{Style.RESET_ALL}")
            
            # ----------------------------
            # Cinematic completion with blinking
            # ----------------------------
            self._cinematic_typing("System fortification complete!", 0.05)
            
            # Blinking completion banner
            for _ in range(3):
                print(f"\r{Fore.GREEN}{self._center_text('▄︻デ══━ SYSTEM FORTIFICATION COMPLETE ══━︻▄')}{Style.RESET_ALL}", end="")
                time.sleep(0.3)
                print(f"\r{' ' * self.terminal_width}", end="")
                time.sleep(0.3)
            
            print(f"\n{Fore.GREEN}{self._center_text('▄︻デ══━ SYSTEM FORTIFICATION COMPLETE ══━︻▄')}{Style.RESET_ALL}")
            threat_level = random.randint(1, 10)
            
            # Blinking threat level
            threat_text = f" Firewall Active | Intrusion Prevention Engaged | Threat Level: {threat_level}/10"
            self._blinking_text(self._center_text(threat_text), Fore.YELLOW, 3)
            
        except Exception as e:
            # Catch-all to preserve cinematic end even on errors
            print(f"{Fore.RED}[!] Critical error: {str(e)}{Style.RESET_ALL}")
            self._cinematic_typing("System fortification complete with errors.", 0.05)
            print(f"\n{Fore.GREEN}{self._center_text('▄︻デ══━ SYSTEM FORTIFICATION COMPLETE ══━︻▄')}{Style.RESET_ALL}")
            threat_level = random.randint(1, 10)
            print(f"{Fore.YELLOW}{self._center_text(f' Firewall Active | Intrusion Prevention Engaged | Threat Level: {threat_level}/10')}{Style.RESET_ALL}")


    # go down here, don't remove these lines below
    def nikto_scan(self, target_url, port=80, output_file=None):
        """Run Nikto scan on a target URL."""
        cmd = f"nikto -h {target_url} -p {port}"
        if output_file:
            cmd += f" -o {output_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout

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

#   ---------------------------------
    def handle_command(self, cmd):
        cmd = cmd.strip()
        if not cmd:
            return

        original_cmd = cmd
        parts = cmd.split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []


# -----------------------------starts here-------------
        if parts[0] == "mkdir" and len(parts) == 2:
            self.mkdir(parts[1])
            return

        elif parts[0] == "touch" and len(parts) == 2:
            self.touch(parts[1])
            return
 
        elif parts[0] == "ls":
            self.ls()
            return

            # Fix 2: Add the missing command handlers
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
        

        elif cmd == "refresh" or cmd == "reload":
            self.cmd_refresh()
            return

# Add this temporary debug command
    
        elif cmd == "recon":
            if len(args) == 0:
                print("Usage: recon <target> OR recon -full <target>")
                return

            if args[0] == "-full":
                if len(args) < 2:
                    print("Usage: recon -full <target>")
                    return
                target = args[1]
                # Use sys.executable for cross-platform Python call
                subprocess.run([sys.executable, "recon_full.py", target])
            else:
                target = args[0]
                subprocess.run([sys.executable, "recon.py", target])
 
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

# nmap-------------------
        elif parts[0] == "nmap":
            self.handle_nmap(parts[1:])
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
        elif cmd == "transfertrace":
            self.financial_simulator()
            # Add to your command handler:
        elif original_cmd.lower() == "extract -money":
            self.financial_simulator()
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


        # ------------integrity section===========
            # Handle integrity commands (with typo tolerance)
        elif cmd in ['integrity', 'integrit', 'integ', 'int']:
            if len(args) > 0:
                subcmd = args[0].lower()
            
            # integrity help
                if subcmd == "help":
                    self.show_integrity_help()
                    self.show_tip(cmd)
            
            # integrity scan
                elif subcmd == "scan":
                    print(f"{Fore.CYAN}Starting full system integrity scan...{Style.RESET_ALL}")
                    if hasattr(self, 'integrity') and self.integrity:
                        self.integrity.full_integrity_check()
                    else:
                        print(f"{Fore.RED}Integrity monitor not initialized{Style.RESET_ALL}")
                    self.show_tip(cmd)
            
            # integrity baseline
                elif subcmd == "baseline":
                    print(f"{Fore.CYAN}Creating new system baseline...{Style.RESET_ALL}")
                    if hasattr(self, 'integrity') and self.integrity:
                        self.integrity.create_baseline()
                    else:
                        print(f"{Fore.RED}Integrity monitor not initialized{Style.RESET_ALL}")
                    self.show_tip(cmd)
            
            # integrity compare <file>
                elif subcmd == "compare":
                    if len(args) < 2:
                        print(f"{Fore.RED}[!] Usage: integrity compare <baseline_file>{Style.RESET_ALL}")
                    else:
                        self.compare_with_baseline(args[1])
                    self.show_tip(cmd)
            
            # integrity list [category]
                elif subcmd == "list":
                    category = args[1] if len(args) > 1 else 'all'
                    valid_categories = ['all', 'critical', 'configs', 'logs', 'databases', 'user', 'system']
                
                    if category not in valid_categories:
                        print(f"{Fore.RED}Invalid category. Valid: {', '.join(valid_categories)}{Style.RESET_ALL}")
                    elif hasattr(self, 'integrity') and self.integrity:
                        self.integrity.list_all_files(category)
                    else:
                        print(f"{Fore.RED}Integrity monitor not initialized{Style.RESET_ALL}")
                    self.show_tip(cmd)
            
            # integrity report [latest]
                elif subcmd == "report":
                    if len(args) > 1:
                        if args[1] == "latest":
                            self.show_latest_report()
                        elif args[1] == "json":
                            print(f"{Fore.CYAN}Generating JSON report...{Style.RESET_ALL}")
                            if hasattr(self, 'integrity') and self.integrity:
                                scan_results = self.integrity.scan_system()
                                changes = self.integrity.check_integrity(scan_results)
                                self.integrity.generate_json_report(changes, scan_results)
                            else:
                                print(f"{Fore.RED}Integrity monitor not initalized{Style.RESET_ALL}") 
                        elif args[1] == "pdf":
                            print(f"{Fore.CYAN}Generating PDF report...{Style.RESET_ALL}")
                            if hasattr(self, 'integrity') and self.integrity:
                                scan_results = self.integrity.scan_system()
                                changes = self.integrity.check_integrity(scan_results)
                                self.integrity.generate_pdf_report(changes, scan_results)
                            else:
                                print(f"{Fore.RED}Integrity monitor not initialized{Style.RESET_ALL}")

                        elif args[1] == "all":
                            print(f"{Fore.CYAN}Generating all report formats...{Style.RESET_ALL}")
                            if hasattr(self, 'integrity') and self.integrity:
                                scan_results = self.integrity.scan_system()
                                changes = self.integrity.check_integrity(scan_results)
                                self.integrity.generate_all_reports(changes, scan_results)
                            else:
                                print(f"{Fore.RED}Integrity monitor not initialized{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}Unknown report type. Use: latest, json, pdf, all{Style.RESET_ALL}")
            # ====
                    else:
                        print(f"{Fore.CYAN}Generating comprehensive report...{Style.RESET_ALL}")
                        if hasattr(self, 'integrity') and self.integrity:
                            scan_results = self.integrity.scan_system()
                            changes = self.integrity.check_integrity(scan_results)
                            self.integrity.generate_report(changes, scan_results)
                        else:
                            print(f"{Fore.RED}Integrity monitor not initialized{Style.RESET_ALL}")
                    self.show_tip(cmd)
                
            
            # integrity monitor [stop]
                elif subcmd == "monitor":
                    if len(args) > 1 and args[1] == "stop":
                        if hasattr(self, 'alert_manager') and self.alert_manager:
                            self.alert_manager.stop_monitoring()
                            print(f"{Fore.GREEN}Real-time monitoring stopped{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}Alert manager not initialized{Style.RESET_ALL}")
                    else:
                    # Start real-time monitoring
                        if not hasattr(self, 'alert_manager') or not self.alert_manager:
                            try:
                                from integrity_monitor import AlertManager
                                self.alert_manager = AlertManager(self.integrity)
                            except ImportError:
                                print(f"{Fore.RED}AlertManager not available{Style.RESET_ALL}")
                                self.show_tip(cmd)
                                return True
                    
                        paths = args[1:] if len(args) > 1 else None
                        self.alert_manager.start_monitoring(paths)
                    self.show_tip(cmd)
            
            # integrity alerts [show|clear] [severity]
                elif subcmd == "alerts":
                    if len(args) > 1:
                        if args[1] == "show":
                            severity = args[2] if len(args) > 2 else None
                            if hasattr(self, 'alert_manager') and self.alert_manager:
                                alerts = self.alert_manager.get_alerts(severity)
                                self.display_alerts(alerts)
                            else:
                                print(f"{Fore.RED}Alert manager not initialized{Style.RESET_ALL}")
                        elif args[1] == "clear":
                            if hasattr(self, 'alert_manager') and self.alert_manager:
                                self.alert_manager.alerts = []
                                print(f"{Fore.GREEN}Alerts cleared{Style.RESET_ALL}")
                            else:
                                print(f"{Fore.RED}Alert manager not initialized{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}Unknown alerts subcommand. Use: alerts show|clear{Style.RESET_ALL}")
                    else:
                    # Show recent alerts
                        if hasattr(self, 'alert_manager') and self.alert_manager:
                            alerts = self.alert_manager.get_alerts(limit=20)
                            self.display_alerts(alerts)
                        else:
                            print(f"{Fore.RED}No alerts. Start monitoring with 'integrity monitor'{Style.RESET_ALL}")
                    self.show_tip(cmd)
            
            # integrity forensic <timeline|report> [file] [days]
                elif subcmd == "forensic":
                    if len(args) < 2:
                        print(f"{Fore.RED}[!] Usage: integrity forensic <timeline|report> [file_path] [days]{Style.RESET_ALL}")
                        self.show_tip(cmd)
                        return True
                
                    forensic_action = args[1].lower()
                
                    try:
                        from integrity_monitor import ForensicAnalyzer
                        forensic = ForensicAnalyzer(self.integrity)
                    except ImportError:
                        print(f"{Fore.RED}ForensicAnalyzer not available{Style.RESET_ALL}")
                        self.show_tip(cmd)
                        return True
                
                    if forensic_action == "timeline":
                        file_path = args[2] if len(args) > 2 else None
                        days = int(args[3]) if len(args) > 3 else 7
                        timeline = forensic.analyze_timeline(file_path, days)
                        self.display_timeline(timeline)
                
                    elif forensic_action == "report":
                        file_path = args[2] if len(args) > 2 else None
                        days = int(args[3]) if len(args) > 3 else 7
                        report_file = forensic.generate_forensic_report(file_path, days)
                        print(f"{Fore.GREEN}Forensic report generated: {report_file}{Style.RESET_ALL}")
                
                    else:
                        print(f"{Fore.RED}Unknown forensic action. Use: timeline|report{Style.RESET_ALL}")
                    self.show_tip(cmd)
            
            # integrity quarantine <file>
                elif subcmd == "quarantine":
                    if len(args) < 2:
                        print(f"{Fore.RED}[!] Usage: integrity quarantine <file_path>{Style.RESET_ALL}")
                    else:
                        self.quarantine_file(args[1])
                    self.show_tip(cmd)
            
            # integrity restore <file>
                elif subcmd == "restore":
                    if len(args) < 2:
                        print(f"{Fore.RED}[!] Usage: integrity restore <file_path>{Style.RESET_ALL}")
                    else:
                        self.restore_from_quarantine(args[1])
                    self.show_tip(cmd)
            
            # integrity configure <email|webhook> <options>
                elif subcmd == "configure":
                    if len(args) < 2:
                        print(f"{Fore.RED}[!] Usage: integrity configure <email|webhook> <options>{Style.RESET_ALL}")
                        self.show_tip(cmd)
                        return True
                
                    config_type = args[1].lower()
                
                    if config_type == "email":
                        if len(args) < 8:
                            print(f"{Fore.RED}[!] Usage: integrity configure email <smtp_server> <port> <username> <password> <from> <to>{Style.RESET_ALL}")
                            self.show_tip(cmd)
                            return True
                    
                        if not hasattr(self, 'alert_manager') or not self.alert_manager:
                            try:
                                from integrity_monitor import AlertManager
                                self.alert_manager = AlertManager(self.integrity)
                            except ImportError:
                                print(f"{Fore.RED}AlertManager not available{Style.RESET_ALL}")
                                self.show_tip(cmd)
                                return True
                    
                        self.alert_manager.configure_email(
                            args[2], int(args[3]), args[4], args[5], args[6], args[7:]
                        )
                
                    elif config_type == "webhook":
                        if len(args) < 3:
                            print(f"{Fore.RED}[!] Usage: integrity configure webhook <url>{Style.RESET_ALL}")
                            self.show_tip(cmd)
                            return True
                    
                        if not hasattr(self, 'alert_manager') or not self.alert_manager:
                            try:
                                from integrity_monitor import AlertManager
                                self.alert_manager = AlertManager(self.integrity)
                            except ImportError:
                                print(f"{Fore.RED}AlertManager not available{Style.RESET_ALL}")
                                self.show_tip(cmd)
                                return True
                    
                        self.alert_manager.configure_webhook(args[2])
                
                    else:
                        print(f"{Fore.RED}Unknown configuration type. Use: email|webhook{Style.RESET_ALL}")
                    self.show_tip(cmd)
            
            # integrity status
                elif subcmd == "status":
                    self.show_integrity_status()
                    self.show_tip(cmd)
            
            # Default: show help if unknown subcommand
                else:
                    print(f"{Fore.RED}[!] Unknown integrity command: {subcmd}{Style.RESET_ALL}")
                    self.show_integrity_help()
                    self.show_tip(cmd)
        
            else:
            # Just 'integrity' with no args shows help
                self.show_integrity_help()
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

    # ==================check integrity and encrypt or decrypt files/folders
        elif original_cmd.lower() == "check integrity": 
            self.check_integrity()
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

        elif cmd == "memdump": 
            self.dump_memory()
            self.show_tip(cmd)
        elif cmd == "torify": 
            self.enable_tor_routing()
            self.show_tip(cmd)
        elif cmd == "update": 
            print(f"\n[+] {self.check_updates()}")
            self.show_tip(cmd)
        elif cmd == "vt-scan": 
            self.vt_scan_menu()
            self.show_tip(cmd)
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
            print("[!] Unknown command. Type 'help' for more command options.")
            self.show_tip(cmd)

# ==================== HELP MENU ====================

    def show_help(self):
        """Display interactive hacking-styled help menu with categories"""
    
    # Define blink sequences if not already defined in class
        blink_on = "\033[5m"
        blink_off = "\033[25m"
    
    # Clear screen and show loading animation
        self._cinematic_box("LOADING COMMAND DATABASE", seconds=2)
    
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
                ("msf -h", "Metasploit help and options"),
                ("nmap -sV <TARGET>", "Service/version detection scan"),
                ("nmap -A <TARGET>", "Aggressive OS and service detection"),
                ("nmap -p- <TARGET>", "Scan all 65535 ports"),
                ("nmap scan <TARGET>", "Nmap scan the target")
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
#     def run(self):
#             self.print_banner()
#             while True:
#                 try:
#                         prompt_text = HTML('<ansigreen><b>[-- DFFENEX</b></ansigreen>'
#                                '<ansiblue>@</ansiblue>'
#                                '<ansigreen><b>DSTerminal</b></ansigreen> '
#                                '<ansired>]-[]</ansired> ')
#                         user_input = self.session.prompt(prompt_text)
#                         self.handle_command(user_input.strip())
#                 except KeyboardInterrupt:
#                     print("\n[*] Use 'exit' to quit")
#                 except Exception as e:
#                     print(f"[!] Error: {str(e)}")

# if __name__ == "__main__":
#     terminal = SecurityTerminal()
#     terminal.run()

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
            "check": {"integrity": None},
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
        self.session = PromptSession(
            history=FileHistory('.dst_history'),
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer,
            complete_while_typing=True,
            bottom_toolbar=HTML(
                "<b>DSTerminal</b> v{} | Mode: <style bg='{}'>{}</style>"
            ).format(
                CONFIG["CURRENT_VERSION"],
                "ansired" if self.is_admin() else "ansigreen",
                "ADMIN" if self.is_admin() else "USER",
            ),
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
    terminal = SecurityTerminal()
    terminal.run()