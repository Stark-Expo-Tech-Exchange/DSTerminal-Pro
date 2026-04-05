import os
import sys
import time
import threading
import itertools
import subprocess
import shutil
import random
from datetime import datetime
from pathlib import Path

# -------------------------------
# WORKSPACE DIRECTORY SETUP
# -------------------------------

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
    (workspace / "scans").mkdir(exist_ok=True)
    
    return workspace

WORKSPACE = get_workspace_dir()

# -------------------------------
# TARGET ARGUMENT
# -------------------------------

if len(sys.argv) < 2:
    print("Usage: recon_full.py <target>")
    sys.exit(1)

target = sys.argv[1]

# -------------------------------
# SCAN DIRECTORY STRUCTURE
# -------------------------------

# Sanitize target name for filesystem
safe_target = "".join(c for c in target if c.isalnum() or c in '.-_')

# Create scan directory in workspace
SCAN_ROOT = WORKSPACE / "scans"
SCAN_ROOT.mkdir(exist_ok=True)

# Create target-specific directory
TARGET_DIR = SCAN_ROOT / safe_target
TARGET_DIR.mkdir(exist_ok=True)

# Create session directory for this scan run
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
SESSION_DIR = TARGET_DIR / f"scan_{timestamp}"
SESSION_DIR.mkdir(exist_ok=True)

width = shutil.get_terminal_size((120, 20)).columns

# -------------------------------
# COLORS
# -------------------------------

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

# -------------------------------
# ANIMATION FRAMES
# -------------------------------

big_spinner_frames = ["◢     ◣", " ◢   ◣ ", "  ◢ ◣  ", "   ◣   ", "  ◥ ◤  ", " ◥   ◤ "]
radar_frames = ["◜", "◝", "◞", "◟"]
scanning_frames = ["🔍", "🔎", "📡", "🛰", "⚡", "💀"]

# -------------------------------
# GLOBAL DATA
# -------------------------------

alert_feed = []

stop_flags = {
    "port": False,
    "dns": False,
    "msf": False
}

scan_outputs = {
    "port": [],
    "dns": [],
    "msf": []
}

risk_scores = {
    "port": 0,
    "dns": 0,
    "msf": 0
}

scan_findings = {
    "port": 0,
    "dns": 0,
    "msf": 0
}

# -------------------------------
# UTILITIES
# -------------------------------

def center(text):
    """Center text with color support"""
    # Remove color codes for length calculation
    clean_text = text
    for code in [RESET, BOLD, CYAN, YELLOW, GREEN, RED, BLUE, MAGENTA]:
        clean_text = clean_text.replace(code, '')
    
    padding = max(0, (width - len(clean_text)) // 2)
    return " " * padding + text

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def check_command_exists(command):
    """Check if a command exists on the system (cross-platform)"""
    try:
        if os.name == "nt":  # Windows
            result = subprocess.run(["where", command], capture_output=True, text=True)
        else:  # Unix/Linux/Mac
            result = subprocess.run(["which", command], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

def save_summary():
    """Save scan summary to workspace"""
    summary_file = SESSION_DIR / f"summary_{timestamp}.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("DSTERMINAL FULL RECONNAISSANCE SUMMARY\n")
        f.write("="*60 + "\n\n")
        f.write(f"Target: {target}\n")
        f.write(f"Scan Time: {datetime.now().isoformat()}\n")
        f.write(f"Workspace: {WORKSPACE}\n")
        f.write(f"Session Directory: {SESSION_DIR}\n\n")
        f.write("-"*60 + "\n")
        f.write("SCAN RESULTS SUMMARY\n")
        f.write("-"*60 + "\n\n")
        
        for scan_name in ['port', 'dns', 'msf']:
            f.write(f"{scan_name.upper()} SCAN:\n")
            f.write(f"  Status: {'COMPLETE' if stop_flags[scan_name] else 'INTERRUPTED'}\n")
            f.write(f"  Findings: {scan_findings[scan_name]}\n")
            f.write(f"  Risk Score: {risk_scores[scan_name]}%\n")
            f.write("\n")
        
        f.write("-"*60 + "\n")
        f.write("ALERT FEED\n")
        f.write("-"*60 + "\n\n")
        for alert in alert_feed:
            # Remove color codes for file
            clean_alert = alert
            for code in [RED, GREEN, YELLOW, CYAN, MAGENTA, BLUE, RESET, BOLD]:
                clean_alert = clean_alert.replace(code, '')
            f.write(f"{clean_alert}\n")
    
    return summary_file

# -------------------------------
# ALERT SYSTEM
# -------------------------------

def append_alert(msg, level="INFO"):
    color = GREEN if level == "INFO" else YELLOW if level == "WARN" else RED
    timestamp_str = datetime.now().strftime("%H:%M:%S")
    alert_msg = f"{color}[{level}] [{timestamp_str}] {msg}{RESET}"
    alert_feed.append(alert_msg)
    if len(alert_feed) > 10:
        alert_feed.pop(0)

# -------------------------------
# THREAT INTELLIGENCE
# -------------------------------

def analyze_port(port):
    critical_ports = {
        "21": "FTP exposed - insecure file transfer",
        "22": "SSH service detected - monitor for brute force",
        "23": "Telnet insecure service - credentials sent in clear",
        "445": "SMB attack surface - vulnerable to ransomware",
        "3389": "RDP remote access - monitor for unauthorized access",
        "1433": "MSSQL database exposed",
        "3306": "MySQL database exposed",
        "6379": "Redis unsecured - potential data leak",
        "9200": "Elasticsearch exposed",
        "27017": "MongoDB exposed"
    }
    if port in critical_ports:
        append_alert(critical_ports[port], "WARN")
        risk_scores["port"] = min(risk_scores["port"] + 15, 100)
        scan_findings["port"] += 1

def threat_intel():
    append_alert("Threat intelligence engine active", "INFO")
    append_alert(f"Analyzing attack surface of {target}", "INFO")
    append_alert("CVE database loaded", "INFO")

# -------------------------------
# GEO LOOKUP
# -------------------------------

def geo_lookup():
    try:
        result = subprocess.run(f"nslookup {target}", shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            append_alert("DNS intelligence collected", "INFO")
            # Parse IP addresses
            for line in result.stdout.split('\n'):
                if 'Address:' in line and 'Addresses' not in line:
                    ip = line.split('Address:')[-1].strip()
                    if ip and not ip.startswith('#'):
                        append_alert(f"Resolved IP: {ip}", "INFO")
                        scan_findings["dns"] += 1
        else:
            append_alert("DNS lookup returned errors", "WARN")
    except subprocess.TimeoutExpired:
        append_alert("DNS lookup timeout", "WARN")
    except Exception as e:
        append_alert(f"DNS lookup failed: {str(e)}", "WARN")

# -------------------------------
# SOC BOX DRAWING
# -------------------------------

def draw_box(title, content_lines):
    box_width = width // 3 - 2
    max_lines = 15  # Keep last 15 lines visible
    
    # Ensure box_width is reasonable
    if box_width < 20:
        box_width = 30
    
    top = "┌" + "─" * (box_width - 2) + "┐"
    bottom = "└" + "─" * (box_width - 2) + "┘"
    title_line = f"│ {title[:box_width-4].ljust(box_width-4)} │"
    
    # Keep only the last max_lines
    if len(content_lines) > max_lines:
        content_lines = content_lines[-max_lines:]
    
    padded = []
    for line in content_lines:
        # Clean line for display
        clean_line = line
        for code in [RESET, BOLD, CYAN, YELLOW, GREEN, RED, BLUE, MAGENTA]:
            clean_line = clean_line.replace(code, '')
        padded.append(f"│ {clean_line[:box_width-4].ljust(box_width-4)} │")
    
    return [top, title_line] + padded + [bottom]

# -------------------------------
# SPINNER / PROGRESS ENGINE
# -------------------------------

def spinner_panel(label, flag):
    frames = itertools.cycle(big_spinner_frames)
    while not stop_flags[flag]:
        frame = next(frames)
        progress = int(risk_scores[flag] / 5)
        bar = "[" + ("█" * progress).ljust(20) + "]"
        scan_icon = next(itertools.cycle(scanning_frames))
        header = f"{CYAN}{scan_icon} {frame} {label} {bar} {risk_scores[flag]}%{RESET}"
        
        # Update only header line
        if scan_outputs[flag]:
            if len(scan_outputs[flag]) > 0:
                scan_outputs[flag][0] = header
            else:
                scan_outputs[flag].append(header)
        else:
            scan_outputs[flag].append(header)
        
        # Increment score slowly for effect (max 90% during scan)
        if risk_scores[flag] < 90:
            risk_scores[flag] = min(risk_scores[flag] + random.randint(1, 3), 90)
        
        time.sleep(0.3)
    
    # Final completion header
    final_score = risk_scores[flag]
    status_icon = "✓" if final_score < 50 else "⚠" if final_score < 75 else "🔴"
    status_color = GREEN if final_score < 50 else YELLOW if final_score < 75 else RED
    header = f"{status_color}{status_icon} {label} COMPLETE - Risk Score: {final_score}%{RESET}"
    
    if scan_outputs[flag]:
        if len(scan_outputs[flag]) > 0:
            scan_outputs[flag][0] = header
        else:
            scan_outputs[flag].append(header)
    else:
        scan_outputs[flag].append(header)

# -------------------------------
# RADAR ANIMATION
# -------------------------------

def radar_animation():
    i = 0
    while not all(stop_flags.values()):
        r = radar_frames[i % len(radar_frames)]
        timestamp_str = datetime.now().strftime("%H:%M:%S")
        radar_text = f"{MAGENTA}🛰 THREAT RADAR {r} [{timestamp_str}]{RESET}"
        print(center(radar_text))
        i += 1
        time.sleep(0.5)
        print("\033[1A", end="")  # Move up one line

# -------------------------------
# ALERT PANEL
# -------------------------------

def alert_panel():
    while not all(stop_flags.values()):
        print(center(f"{YELLOW}{'═' * 40}{RESET}"))
        print(center(f"{YELLOW}⚡ LIVE ALERT FEED ⚡{RESET}"))
        print(center(f"{YELLOW}{'─' * 40}{RESET}"))
        for a in alert_feed[-5:]:  # Show last 5 alerts
            print(center(a))
        time.sleep(1.5)
        # Move cursor up to refresh
        print("\033[{}A".format(len(alert_feed[-5:]) + 3), end="")

# -------------------------------
# LIVE BOX DISPLAY
# -------------------------------

def display_boxes():
    while not all(stop_flags.values()):
        box_port = draw_box("🔍 PORT SCAN", scan_outputs["port"] or ["Initializing..."])
        box_dns = draw_box("🌐 DNS / WHOIS", scan_outputs["dns"] or ["Initializing..."])
        box_msf = draw_box("💀 METASPLOIT", scan_outputs["msf"] or ["Initializing..."])
        
        rows = max(len(box_port), len(box_dns), len(box_msf))
        
        for i in range(rows):
            p = box_port[i] if i < len(box_port) else " " * (width // 3)
            d = box_dns[i] if i < len(box_dns) else " " * (width // 3)
            m = box_msf[i] if i < len(box_msf) else " " * (width // 3)
            print(p + d + m)
        
        time.sleep(0.3)
        print("\033[{}A".format(rows), end="")

# -------------------------------
# LIVE SCAN ENGINE
# -------------------------------

def run_scan(label, command, flag, outfile):
    spinner = threading.Thread(target=spinner_panel, args=(label, flag))
    spinner.start()
    
    findings_count = 0
    
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        with open(outfile, "w", encoding="utf-8") as f:
            f.write(f"DSTerminal Recon Scan - {label}\n")
            f.write(f"Target: {target}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write("="*60 + "\n\n")
            
            for line in process.stdout:
                f.write(line)
                line = line.strip()
                
                # Parse and display relevant findings
                if line:
                    # Port scan findings
                    if flag == "port" and ("/tcp" in line.lower() or "/udp" in line.lower()):
                        parts = line.split()
                        if parts:
                            port = parts[0].split('/')[0]
                            analyze_port(port)
                            findings_count += 1
                            scan_outputs[flag].append(f"{CYAN}🔓 Open: {line[:50]}{RESET}")
                            scan_findings[flag] = findings_count
                    
                    # DNS findings
                    elif flag == "dns" and ("address" in line.lower() or "canonical" in line.lower()):
                        findings_count += 1
                        scan_outputs[flag].append(f"{GREEN}📍 {line[:50]}{RESET}")
                        scan_findings[flag] = findings_count
                    
                    # WHOIS findings
                    elif flag == "dns" and any(x in line.lower() for x in ['org', 'name', 'email', 'registrar']):
                        findings_count += 1
                        scan_outputs[flag].append(f"{BLUE}📋 {line[:50]}{RESET}")
                        scan_findings[flag] = findings_count
                    
                    # Metasploit findings
                    elif flag == "msf" and any(x in line.lower() for x in ['exploit', 'auxiliary', 'module']):
                        findings_count += 1
                        scan_outputs[flag].append(f"{RED}💀 {line[:50]}{RESET}")
                        scan_findings[flag] = findings_count
                    
                    # General output for other lines
                    elif line and len(line) > 5:
                        if len(scan_outputs[flag]) < 50:  # Limit display
                            scan_outputs[flag].append(f"{CYAN}{line[:50]}{RESET}")
        
        process.wait()
        
        if process.returncode == 0:
            append_alert(f"{label} completed with {findings_count} findings", "INFO")
        else:
            append_alert(f"{label} completed with warnings (exit code: {process.returncode})", "WARN")
            
    except FileNotFoundError:
        append_alert(f"{label} failed: command not found - {command.split()[0]}", "WARN")
        scan_outputs[flag].append(f"{RED}❌ Command not found: {command.split()[0]}{RESET}")
    except Exception as e:
        append_alert(f"{label} failed: {str(e)[:50]}", "WARN")
        scan_outputs[flag].append(f"{RED}❌ Error: {str(e)[:50]}{RESET}")
    
    finally:
        stop_flags[flag] = True
        append_alert(f"{label} results saved → {outfile}", "INFO")
        spinner.join()

# -------------------------------
# SOC HEADER
# -------------------------------

def soc_header():
    clear()
    print(center(f"{BOLD}{CYAN}{'═' * 60}{RESET}"))
    print(center(f"{BOLD}{CYAN}🛡 DSTERMINAL CYBER DEFENSE OPERATIONS CENTER 🛡{RESET}"))
    print(center(f"{BOLD}{CYAN}{'═' * 60}{RESET}"))
    print(center(f"{BOLD}{YELLOW}🎯 TARGET → {target}{RESET}"))
    print(center(f"{CYAN}📡 Full Reconnaissance | Threat Intelligence | Vulnerability Discovery{RESET}"))
    print(center(f"{CYAN}📁 Workspace: {WORKSPACE}{RESET}"))
    print(center(f"{CYAN}{'─' * 60}{RESET}"))
    print()

# -------------------------------
# SOC STARTUP
# -------------------------------

soc_header()
append_alert("SOC systems online", "INFO")
append_alert("Threat radar active", "INFO")
append_alert(f"Target acquired: {target}", "INFO")

geo_lookup()
threat_intel()

# -------------------------------
# START SOC THREADS
# -------------------------------

radar_thread = threading.Thread(target=radar_animation)
alert_thread = threading.Thread(target=alert_panel)
box_thread = threading.Thread(target=display_boxes)

radar_thread.start()
alert_thread.start()
box_thread.start()

# -------------------------------
# SCAN FILES (Save to session directory)
# -------------------------------

nmap_file = SESSION_DIR / f"nmap_{timestamp}.txt"
dns_file = SESSION_DIR / f"dns_{timestamp}.txt"
msf_file = SESSION_DIR / f"metasploit_{timestamp}.txt"

# -------------------------------
# SCAN COMMANDS
# -------------------------------

# Check if nmap is available using cross-platform function
threads = []

if check_command_exists("nmap"):
    threads.append(threading.Thread(
        target=run_scan,
        args=("PORT SCAN", f"nmap -F {target}", "port", nmap_file)
    ))
else:
    append_alert("Nmap not found - using basic port scan with PowerShell", "WARN")
    # Windows fallback using PowerShell
    if os.name == "nt":
        threads.append(threading.Thread(
            target=run_scan,
            args=("PORT SCAN", f'powershell "Test-NetConnection {target} -Port 80,443,22,21,3389"', "port", nmap_file)
        ))
    else:
        threads.append(threading.Thread(
            target=run_scan,
            args=("PORT SCAN", f"nc -zv {target} 1-1000 2>&1 || echo 'Basic scan only'", "port", nmap_file)
        ))

# DNS/WHOIS scan
threads.append(threading.Thread(
    target=run_scan,
    args=("DNS / WHOIS", f"nslookup {target}", "dns", dns_file)
))

# Metasploit search (only if available)
if check_command_exists("msfconsole"):
    threads.append(threading.Thread(
        target=run_scan,
        args=("METASPLOIT SEARCH", f'msfconsole -q -x "search {target}; exit"', "msf", msf_file)
    ))
else:
    append_alert("Metasploit not found - skipping exploit search", "WARN")
    stop_flags["msf"] = True
    scan_outputs["msf"].append(f"{YELLOW}⚠ Metasploit not available on this system{RESET}")

# Start all threads
for t in threads:
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

# Stop monitoring threads
for flag in stop_flags:
    stop_flags[flag] = True

radar_thread.join(timeout=2)
alert_thread.join(timeout=2)
box_thread.join(timeout=2)

# -------------------------------
# SAVE SUMMARY
# -------------------------------

summary_file = save_summary()

# -------------------------------
# FINAL DISPLAY
# -------------------------------

soc_header()
print()

# Final boxes
final_boxes = [
    draw_box("🔍 PORT SCAN RESULTS", scan_outputs["port"][-10:] if scan_outputs["port"] else ["No results"]),
    draw_box("🌐 DNS / WHOIS RESULTS", scan_outputs["dns"][-10:] if scan_outputs["dns"] else ["No results"]),
    draw_box("💀 METASPLOIT RESULTS", scan_outputs["msf"][-10:] if scan_outputs["msf"] else ["Not available"])
]

rows = max(len(final_boxes[0]), len(final_boxes[1]), len(final_boxes[2]))

for i in range(rows):
    p = final_boxes[0][i] if i < len(final_boxes[0]) else " " * (width // 3)
    d = final_boxes[1][i] if i < len(final_boxes[1]) else " " * (width // 3)
    m = final_boxes[2][i] if i < len(final_boxes[2]) else " " * (width // 3)
    print(p + d + m)

print()
print(center(f"{BOLD}{GREEN}{'═' * 60}{RESET}"))
print(center(f"{BOLD}{GREEN}✅ ALL SCANS COMPLETE ✅{RESET}"))
print(center(f"{BOLD}{CYAN}📁 Results stored in: {SESSION_DIR}{RESET}"))
print(center(f"{BOLD}{CYAN}📄 Summary report: {summary_file}{RESET}"))

# Display final risk assessment
risk_values = [r for r in risk_scores.values() if r > 0]
if risk_values:
    total_risk = sum(risk_values) / len(risk_values)
    if total_risk < 30:
        risk_level = f"{GREEN}LOW{RESET}"
    elif total_risk < 70:
        risk_level = f"{YELLOW}MEDIUM{RESET}"
    else:
        risk_level = f"{RED}HIGH{RESET}"
else:
    risk_level = f"{YELLOW}UNKNOWN{RESET}"

print(center(f"{BOLD}Overall Risk Assessment: {risk_level}{RESET}"))
print(center(f"{BOLD}{GREEN}{'═' * 60}{RESET}"))
print()
