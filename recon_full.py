import os
import sys
import time
import threading
import itertools
import subprocess
import shutil
from datetime import datetime

# -------------------------------
# TARGET ARGUMENT
# -------------------------------

if len(sys.argv) < 2:
    print("Usage: recon_full.py <target>")
    sys.exit(1)

target = sys.argv[1]

# -------------------------------
# DIRECTORY STRUCTURE
# -------------------------------

# -------------------------------
# DIRECTORY STRUCTURE (WORKSPACE)
# -------------------------------

# -------------------------------
# DIRECTORY STRUCTURE (DSTerminal Workspace)
# -------------------------------

# -------------------------------
# DIRECTORY STRUCTURE
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# look for workspace folder
possible_workspace = os.path.join(BASE_DIR, "DSTerminal_Workspace")

if os.path.exists(possible_workspace):
    WORKSPACE = possible_workspace
else:
    WORKSPACE = os.getcwd()

SCAN_ROOT = os.path.join(WORKSPACE, "scans")
TARGET_DIR = os.path.join(SCAN_ROOT, target)

os.makedirs(TARGET_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
width = shutil.get_terminal_size((120, 20)).columns

# -------------------------------
# COLORS
# -------------------------------

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# -------------------------------
# ANIMATION FRAMES
# -------------------------------

big_spinner_frames = ["◢     ◣", " ◢   ◣ ", "  ◢ ◣  ", "   ◣   ", "  ◥ ◤  ", " ◥   ◤ "]
radar_frames = ["◜", "◝", "◞", "◟"]

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

# -------------------------------
# UTILITIES
# -------------------------------

def center(text):
    return text.center(width)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# -------------------------------
# ALERT SYSTEM
# -------------------------------

def append_alert(msg, level="INFO"):
    color = GREEN if level=="INFO" else YELLOW if level=="WARN" else RED
    alert_feed.append(f"{color}[{level}] {msg}")
    if len(alert_feed) > 10:
        alert_feed.pop(0)

# -------------------------------
# THREAT INTELLIGENCE
# -------------------------------

def analyze_port(port):
    critical_ports = {
        "21": "FTP exposed",
        "22": "SSH service detected",
        "23": "Telnet insecure service",
        "445": "SMB attack surface",
        "3389": "RDP remote access"
    }
    if port in critical_ports:
        append_alert(critical_ports[port], "WARN")
        risk_scores["port"] = min(risk_scores["port"] + 20, 100)

def threat_intel():
    append_alert("Threat intelligence engine active", "INFO")
    append_alert(f"Analyzing attack surface of {target}", "INFO")

# -------------------------------
# GEO LOOKUP
# -------------------------------

def geo_lookup():
    try:
        subprocess.run(f"nslookup {target}", shell=True, stdout=subprocess.DEVNULL)
        append_alert("DNS intelligence collected", "INFO")
    except:
        append_alert("DNS lookup failed", "WARN")

# -------------------------------
# SOC BOX DRAWING
# -------------------------------

def draw_box(title, content_lines):
    box_width = width // 3 - 2
    max_lines = 20  # Keep last 20 lines visible
    top = "┌" + "─"*(box_width-2) + "┐"
    bottom = "└" + "─"*(box_width-2) + "┘"
    title_line = f"│ {title[:box_width-4].ljust(box_width-4)} │"
    # Keep only the last max_lines
    content_lines = content_lines[-max_lines:]
    padded = [f"│ {line[:box_width-4].ljust(box_width-4)} │" for line in content_lines]
    return [top, title_line] + padded + [bottom]

# -------------------------------
# SPINNER / PROGRESS ENGINE
# -------------------------------

def spinner_panel(label, flag):
    frames = itertools.cycle(big_spinner_frames)
    while not stop_flags[flag]:
        frame = next(frames)
        progress = int(risk_scores[flag] / 5)
        bar = "[" + ("█"*progress).ljust(20) + "]"
        header = f"{CYAN}{frame} Threat Index {bar} {risk_scores[flag]}%"
        # Update only header line
        if scan_outputs[flag]:
            scan_outputs[flag][0] = header
        else:
            scan_outputs[flag].append(header)
        # Increment score slowly for effect
        risk_scores[flag] = min(risk_scores[flag] + 1, 100)
        time.sleep(0.4)
    # Final completion header
    header = f"{GREEN}{label} ✔ COMPLETE"
    if scan_outputs[flag]:
        scan_outputs[flag][0] = header
    else:
        scan_outputs[flag].append(header)

# -------------------------------
# RADAR ANIMATION
# -------------------------------

def radar_animation():
    i = 0
    while not all(stop_flags.values()):
        r = radar_frames[i % len(radar_frames)]
        print(center(f"{MAGENTA}🛰 Threat Radar {r}"))
        i += 1
        time.sleep(0.6)
        print("\033[1A", end="")

# -------------------------------
# ALERT PANEL
# -------------------------------

def alert_panel():
    while not all(stop_flags.values()):
        print(center(f"{YELLOW}=== LIVE ALERT FEED ==="))
        for a in alert_feed:
            print(center(a))
        time.sleep(1)
        print("\033[{}A".format(len(alert_feed)+1), end="")

# -------------------------------
# LIVE BOX DISPLAY
# -------------------------------

def display_boxes():
    while not all(stop_flags.values()):
        box_port = draw_box("PORT SCAN", scan_outputs["port"] or ["Initializing..."])
        box_dns = draw_box("DNS / WHOIS", scan_outputs["dns"] or ["Initializing..."])
        box_msf = draw_box("METASPLOIT", scan_outputs["msf"] or ["Initializing..."])
        rows = max(len(box_port), len(box_dns), len(box_msf))
        for i in range(rows):
            p = box_port[i] if i < len(box_port) else " "*(width//3)
            d = box_dns[i] if i < len(box_dns) else " "*(width//3)
            m = box_msf[i] if i < len(box_msf) else " "*(width//3)
            print(p + d + m)
        time.sleep(0.4)
        print("\033[{}A".format(rows), end="")

# -------------------------------
# LIVE SCAN ENGINE
# -------------------------------

def run_scan(label, command, flag, outfile):
    spinner = threading.Thread(target=spinner_panel, args=(label, flag))
    spinner.start()
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        with open(outfile, "w", encoding="utf-8") as f:
            for line in process.stdout:
                f.write(line)
                line = line.strip()
                # Append discovered ports or lines to live output
                if line and "/tcp" in line:
                    port = line.split("/")[0]
                    analyze_port(port)
                    scan_outputs[flag].append(line[:width//3-4])
    except Exception as e:
        append_alert(f"{label} failed: {str(e)}", "WARN")
    stop_flags[flag] = True
    append_alert(f"{label} results saved → {outfile}", "INFO")
    spinner.join()

# -------------------------------
# SOC HEADER
# -------------------------------

def soc_header():
    clear()
    print(center("🛡 DSTerminal Cyber Defense Operations Center 🛡"))
    print(center("="*width))
    print(center(f"{CYAN}TARGET → {target}"))
    print(center("Network Recon | Threat Intelligence | Exploit Discovery"))
    print(center("-"*width))

# -------------------------------
# SOC STARTUP
# -------------------------------

soc_header()
append_alert("SOC systems online", "INFO")
append_alert("Threat radar active", "INFO")

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
# SCAN FILES
# -------------------------------

nmap_file = os.path.join(TARGET_DIR, f"nmap_{timestamp}.txt")
dns_file = os.path.join(TARGET_DIR, f"dns_{timestamp}.txt")
msf_file = os.path.join(TARGET_DIR, f"metasploit_{timestamp}.txt")

# -------------------------------
# SCAN COMMANDS
# -------------------------------

threads = [
    threading.Thread(
        target=run_scan,
        args=("PORT SCAN", f"nmap -sS -sV -T4 {target}", "port", nmap_file)
    ),
    threading.Thread(
        target=run_scan,
        args=("DNS / WHOIS", f"nslookup {target} && whois {target}", "dns", dns_file)
    ),
    threading.Thread(
        target=run_scan,
        args=("METASPLOIT SEARCH", f'msfconsole -q -x "search {target}; exit"', "msf", msf_file)
    )
]

for t in threads:
    t.start()
for t in threads:
    t.join()

radar_thread.join()
alert_thread.join()
box_thread.join()

# -------------------------------
# FINAL DISPLAY
# -------------------------------

soc_header()
print()

final_boxes = [
    draw_box("PORT SCAN", scan_outputs["port"]),
    draw_box("DNS / WHOIS", scan_outputs["dns"]),
    draw_box("METASPLOIT", scan_outputs["msf"])
]

rows = max(len(final_boxes[0]), len(final_boxes[1]), len(final_boxes[2]))

for i in range(rows):
    p = final_boxes[0][i] if i < len(final_boxes[0]) else " "*(width//3)
    d = final_boxes[1][i] if i < len(final_boxes[1]) else " "*(width//3)
    m = final_boxes[2][i] if i < len(final_boxes[2]) else " "*(width//3)
    print(p + d + m)

print(center(f"{GREEN}ALL SCANS COMPLETE ✔"))
print(center(f"Results stored in workspace → scans/{target}"))
print()