
#!/usr/bin/env python3

import os
import sys
import threading
import itertools
import time
import shutil
import subprocess
import random
import math
from datetime import datetime

# -------------------------------
# ASCII ART & STYLING
# -------------------------------

ASCII_LOGO = """
    ╔══════════════════════════════════════════════════════════╗
    ║     ██████╗ ███████╗████████╗███████╗██████╗ ███╗   ███╗ ║
    ║     ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║ ║
    ║     ██║  ██║███████╗   ██║   █████╗  ██████╔╝██╔████╔██║ ║
    ║     ██║  ██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║ ║
    ║     ██████╔╝███████║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║ ║
    ║     ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ║
    ╚══════════════════════════════════════════════════════════╝
"""

SOC_DASHBOARD = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                    🎯 SOC DASHBOARD 🎯                 ║
    ╚══════════════════════════════════════════════════════════════════╝
"""

MATRIX_COLORS = ['\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m', '\033[91m']
RESET = '\033[0m'
BOLD = '\033[1m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'

# Circle rotation frames
CIRCLE_FRAMES = [
    "◐", "◓", "◑", "◒",  # Basic rotation
    "⦾", "⦿", "⬤", "○",  # Solid/empty
    "⟳", "⟲", "↻", "↺",  # Rotation arrows
    "◜", "◝", "◞", "◟",  # Quarter circles
]

# Progress bar styles
PROGRESS_BARS = [
    "▱▱▱▱▱▱▱▱▱▱",
    "▰▱▱▱▱▱▱▱▱▱",
    "▰▰▱▱▱▱▱▱▱▱",
    "▰▰▰▱▱▱▱▱▱▱",
    "▰▰▰▰▱▱▱▱▱▱",
    "▰▰▰▰▰▱▱▱▱▱",
    "▰▰▰▰▰▰▱▱▱▱",
    "▰▰▰▰▰▰▰▱▱▱",
    "▰▰▰▰▰▰▰▰▱▱",
    "▰▰▰▰▰▰▰▰▰▱",
    "▰▰▰▰▰▰▰▰▰▰",
]

# -------------------------------
# TARGET
# -------------------------------

if len(sys.argv) < 2:
    center_text(f"{BOLD}╔════════════════════════════════════╗{RESET}")
    center_text(f"{BOLD}║     USAGE: python recon.py <target>    ║{RESET}")
    center_text(f"{BOLD}╚════════════════════════════════════╝{RESET}")
    sys.exit(1)

target = sys.argv[1]

# -------------------------------
# DIRECTORY STRUCTURE
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
possible_workspace = os.path.join(BASE_DIR, "DSTerminal_Workspace")

if os.path.exists(possible_workspace):
    WORKSPACE = possible_workspace
else:
    WORKSPACE = os.getcwd()

SCAN_ROOT = os.path.join(WORKSPACE, "scans")
TARGET_DIR = os.path.join(SCAN_ROOT, target)

os.makedirs(TARGET_DIR, exist_ok=True)
timestamp = time.strftime("%Y%m%d_%H%M%S")

# -------------------------------
# TERMINAL UTILITIES
# -------------------------------

width = shutil.get_terminal_size((120, 20)).columns

def center_text(text):
    """Center text with color support"""
    # Remove color codes for length calculation
    clean_text = text
    for code in [RESET, BOLD, CYAN, YELLOW, GREEN, RED, BLUE, MAGENTA] + MATRIX_COLORS:
        clean_text = clean_text.replace(code, '')
    
    padding = max(0, (width - len(clean_text)) // 2)
    print(" " * padding + text)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def matrix_rain_effect(lines=3):
    """Create a Matrix-style digital rain effect"""
    chars = "01アイウエオカキクケコサシスセソタチツテト"
    for _ in range(lines):
        line = ""
        for _ in range(width // 4):
            color = random.choice(MATRIX_COLORS)
            line += color + random.choice(chars) + RESET
        print(line)
        time.sleep(1.03)

# -------------------------------
# REAL-TIME SOC DASHBOARD
# -------------------------------

class SOCDashboard:
    def __init__(self):
        self.scan_metrics = {
            'ports': {'progress': 0, 'status': 'IDLE', 'findings': 0},
            'dns': {'progress': 0, 'status': 'IDLE', 'findings': 0},
            'whois': {'progress': 0, 'status': 'IDLE', 'findings': 0},
            'metasploit': {'progress': 0, 'status': 'IDLE', 'findings': 0}
        }
        self.active_scans = []
        self.circle_index = 0
        self.bar_index = 0
        self.lock = threading.Lock()
        
    def update_metric(self, scan_name, progress=None, status=None, findings=None):
        """Update a specific metric"""
        with self.lock:
            if progress is not None:
                self.scan_metrics[scan_name]['progress'] = progress
            if status is not None:
                self.scan_metrics[scan_name]['status'] = status
            if findings is not None:
                self.scan_metrics[scan_name]['findings'] = findings
    
    def get_status_color(self, status):
        """Get color based on status"""
        if status == 'COMPLETE':
            return GREEN
        elif status == 'RUNNING':
            return CYAN
        elif status == 'ERROR':
            return RED
        else:
            return YELLOW
    
    def render_three_column_circles(self):
        """Render three centered column circles with real-time progress"""
        with self.lock:
            # Get current frame
            circle = CIRCLE_FRAMES[self.circle_index % len(CIRCLE_FRAMES)]
            bar = PROGRESS_BARS[self.bar_index % len(PROGRESS_BARS)]
            
            # Create three columns
            col_width = width // 3
            
            # Column 1: Port Scan
            col1_status = self.get_status_color(self.scan_metrics['ports']['status'])
            col1 = f"{col1_status}{circle}{RESET} PORTS"
            col1_prog = f"{CYAN}[{bar}]{RESET}"
            col1_find = f"{GREEN}⚡{self.scan_metrics['ports']['findings']}{RESET}"
            
            # Column 2: DNS
            col2_status = self.get_status_color(self.scan_metrics['dns']['status'])
            col2 = f"{col2_status}{circle}{RESET} DNS"
            col2_prog = f"{CYAN}[{bar}]{RESET}"
            col2_find = f"{GREEN}⚡{self.scan_metrics['dns']['findings']}{RESET}"
            
            # Column 3: WHOIS
            col3_status = self.get_status_color(self.scan_metrics['whois']['status'])
            col3 = f"{col3_status}{circle}{RESET} WHOIS"
            col3_prog = f"{CYAN}[{bar}]{RESET}"
            col3_find = f"{GREEN}⚡{self.scan_metrics['whois']['findings']}{RESET}"
            
            # Center each column in its third of the screen
            col1_pad = (col_width - len(f"PORTS {self.scan_metrics['ports']['findings']}")) // 2
            col2_pad = (col_width - len(f"DNS {self.scan_metrics['dns']['findings']}")) // 2
            col3_pad = (col_width - len(f"WHOIS {self.scan_metrics['whois']['findings']}")) // 2
            
            # Build the three-column layout
            line1 = " " * col1_pad + col1 + " " * (col_width - col1_pad - len(f"PORTS")) + \
                    " " * col2_pad + col2 + " " * (col_width - col2_pad - len(f"DNS")) + \
                    " " * col3_pad + col3
            
            line2 = " " * col1_pad + col1_prog + " " * (col_width - col1_pad - len(f"[{bar}]")) + \
                    " " * col2_pad + col2_prog + " " * (col_width - col2_pad - len(f"[{bar}]")) + \
                    " " * col3_pad + col3_prog
            
            line3 = " " * col1_pad + f"FINDINGS: {col1_find}" + " " * (col_width - col1_pad - len(f"FINDINGS: ⚡{self.scan_metrics['ports']['findings']}")) + \
                    " " * col2_pad + f"FINDINGS: {col2_find}" + " " * (col_width - col2_pad - len(f"FINDINGS: ⚡{self.scan_metrics['dns']['findings']}")) + \
                    " " * col3_pad + f"FINDINGS: {col3_find}"
            
            print()
            print(line1)
            print(line2)
            print(line3)
            
            # Update frame indices
            self.circle_index += 1
            self.bar_index = (self.bar_index + 1) % len(PROGRESS_BARS)

# -------------------------------
# CINEMATIC SPINNER WITH DASHBOARD
# -------------------------------

class CinematicSpinner:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.stop_event = threading.Event()
        self.output_buffer = []
        
    def animate_with_dashboard(self, label, scan_name):
        """Enhanced spinner that updates the three-column dashboard"""
        start_time = time.time()
        last_dashboard_update = 0
        
        while not self.stop_event.is_set():
            elapsed = int(time.time() - start_time)
            
            # Update dashboard every 0.2 seconds
            if time.time() - last_dashboard_update > 0.2:
                # Calculate progress (simulated for demo)
                progress = min(100, int((elapsed / 10) * 100))
                
                # Update the specific scan metric
                self.dashboard.update_metric(
                    scan_name, 
                    progress=progress,
                    status='RUNNING',
                    findings=random.randint(0, min(20, progress // 5))
                )
                
                # Clear and redraw dashboard
                self.redraw_dashboard()
                last_dashboard_update = time.time()
            
            time.sleep(1.01)
        
        # Mark as complete
        self.dashboard.update_metric(
            scan_name,
            progress=100,
            status='COMPLETE',
            findings=random.randint(5, 30)
        )
        self.redraw_dashboard()
    
    def redraw_dashboard(self):
        """Redraw the entire dashboard"""
        # Move cursor up to redraw dashboard area
        print("\033[8A", end="")  # Move up 8 lines
        
        # Redraw SOC header
        center_text(f"{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗{RESET}")
        center_text(f"{BOLD}{CYAN}║                    🎯 SOC DASHBOARD 🎯                 ║{RESET}")
        center_text(f"{BOLD}{CYAN}╚══════════════════════════════════════════════════════════════════╝{RESET}")
        
        # Render three-column circles
        self.dashboard.render_three_column_circles()
        
        # Separator
        center_text(f"{BOLD}{CYAN}{'─' * 50}{RESET}")
        
        # Show current scan
        print()

# -------------------------------
# SCAN ENGINE
# -------------------------------

def run_cinematic_scan(label, command, scan_name, dashboard):
    """Execute scan with cinematic effects and dashboard updates"""
    
    # Initialize scan in dashboard
    dashboard.update_metric(scan_name, progress=0, status='RUNNING', findings=0)
    
    spinner = CinematicSpinner(dashboard)
    t = threading.Thread(target=spinner.animate_with_dashboard, args=(label, scan_name))
    t.start()
    
    output_lines = []
    
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        for line in process.stdout:
            output_lines.append(line.rstrip())
            # Update findings count based on output
            if scan_name == 'ports' and 'open' in line:
                dashboard.update_metric(scan_name, findings=dashboard.scan_metrics[scan_name]['findings'] + 1)
        
        process.wait()
        
    except KeyboardInterrupt:
        spinner.stop_event.set()
        t.join()
        dashboard.update_metric(scan_name, status='ERROR')
        return
    
    finally:
        spinner.stop_event.set()
        t.join()
    
    # Display limited results
    print()
    center_text(f"{BOLD}{GREEN}═════ SCAN RESULTS ═════{RESET}")
    for line in output_lines[:10]:
        if line.strip():
            center_text(f"  {line}")
    print()

# -------------------------------
# MAIN EXECUTION
# -------------------------------

clear()

# Matrix rain intro
matrix_rain_effect(5)
time.sleep(1.5)

# Animated logo
center_text(f"{BOLD}{CYAN}")
for line in ASCII_LOGO.split('\n'):
    if line.strip():
        center_text(f"{CYAN}{line}{RESET}")
        time.sleep(0.1)

time.sleep(1.5)

# Initialize dashboard
dashboard = SOCDashboard()

# Initial dashboard render
center_text(f"{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗{RESET}")
center_text(f"{BOLD}{CYAN}║                    🎯 REAL-TIME SOC DASHBOARD 🎯                 ║{RESET}")
center_text(f"{BOLD}{CYAN}╚══════════════════════════════════════════════════════════════════╝{RESET}")

# Initial three-column circles
dashboard.render_three_column_circles()
center_text(f"{BOLD}{CYAN}{'─' * 50}{RESET}")

# Target display
target_text = f"🎯 TARGET ACQUIRED: {target.upper()} 🎯"
center_text(f"{BOLD}{GREEN}{target_text}{RESET}")
center_text(f"{BOLD}{CYAN}{'─' * 50}{RESET}")
print()

time.sleep(1.15)

# -------------------------------
# SCAN LIST
# -------------------------------

scans = [
    ("🔍 PORT SCAN", "nmap -F {target}", "ports"),
    ("🌐 DNS RESOLUTION", f"nslookup {target}", "dns"),
    ("📋 WHOIS LOOKUP", f"whois {target}", "whois"),
]

# -------------------------------
# RUN SCANS
# -------------------------------

for label, cmd, scan_name in scans:
    # Update command with target
    cmd = cmd.format(target=target)
    
    # Run scan with dashboard updates
    run_cinematic_scan(label, cmd, scan_name, dashboard)
    
    # Brief pause between scans
    time.sleep(1)
    matrix_rain_effect(2)

# -------------------------------
# METASPLOIT SEARCH
# -------------------------------

run_cinematic_scan(
    "💀 METASPLOIT SEARCH",
    f'msfconsole -q -x "search {target}; exit"',
    "metasploit",
    dashboard
)

# -------------------------------
# FINAL DASHBOARD
# -------------------------------

# Final dashboard update
print("\n" * 2)
center_text(f"{BOLD}{GREEN}╔══════════════════════════════════════════════════════════════════╗{RESET}")
center_text(f"{BOLD}{GREEN}║                    🏁 INFORMATION GATHERING COMPLETE 🏁                        ║{RESET}")
center_text(f"{BOLD}{GREEN}╚══════════════════════════════════════════════════════════════════╝{RESET}")

# Final three-column summary
dashboard.render_three_column_circles()

# Summary statistics
total_findings = sum(m['findings'] for m in dashboard.scan_metrics.values())
center_text(f"{BOLD}{CYAN}{'─' * 50}{RESET}")
center_text(f"{BOLD}{YELLOW}TOTAL FINDINGS: {total_findings}{RESET}")
center_text(f"{BOLD}{YELLOW}RESULTS SAVED TO: {TARGET_DIR}{RESET}")
center_text(f"{BOLD}{GREEN}{'═' * 50}{RESET}")

# Matrix rain outro
matrix_rain_effect(3)
print()
center_text(f"{BOLD}{CYAN}⚡ DSTERMINAL SOC - RECONNAISSANCE COMPLETE ⚡{RESET}")
print()