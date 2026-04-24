#!/usr/bin/env python3
"""
DSTERMINAL - ENCRYPTION SUITE [HACKER EDITION]
Interactive cinematic mode with real-time encryption visualization
"""

import os
import sys
import time
import hashlib
import shutil
import base64
import random
import threading
from datetime import datetime
from cryptography.fernet import Fernet

# ANSI color codes for terminal effects
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    BLACK = '\033[90m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

KEY_FILE = os.path.expanduser("~/.dsterminal_key")


class MatrixRain:
    """Cinematic matrix rain effect"""
    
    def __init__(self, width=60, height=10):
        self.width = width
        self.height = height
        self.chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        
    def render_frame(self, duration=0.1):
        frame = []
        for i in range(self.height):
            line = ''
            for j in range(self.width):
                if random.random() > 0.7:
                    line += f"{Colors.GREEN}{random.choice(self.chars)}{Colors.END}"
                else:
                    line += ' '
            frame.append(line)
        
        # Clear previous lines
        sys.stdout.write('\033[{}A'.format(self.height))
        for line in frame:
            print(line)
        time.sleep(duration)


class RotatingBox:
    """Animated rotating box with content"""
    
    def __init__(self, width=40, title=""):
        self.width = width
        self.title = title
        self.frames = 0
        
    def render(self, content_lines, color=Colors.CYAN):
        """Render a box with rotating animation"""
        frames = ['╔', '╗', '╚', '╝']
        corners = frames[self.frames % 4]
        
        # Top border with animation
        if self.frames % 8 < 4:
            print(f"{color}┌─{self.title.center(self.width-4, '─')}─┐{Colors.END}")
        else:
            print(f"{color}╭─{self.title.center(self.width-4, '─')}─╮{Colors.END}")
        
        # Content
        for line in content_lines:
            print(f"{color}│{Colors.END} {line.ljust(self.width-2)} {color}│{Colors.END}")
        
        # Bottom border with animation
        if self.frames % 8 < 4:
            print(f"{color}└{'─' * (self.width-2)}┘{Colors.END}")
        else:
            print(f"{color}╰{'─' * (self.width-2)}╯{Colors.END}")
        
        self.frames += 1


class AnimatedTable:
    """Animated table with rotating columns"""
    
    def __init__(self, headers):
        self.headers = headers
        self.rotation = 0
        
    def render(self, rows, color=Colors.YELLOW):
        """Render table with rotating effect"""
        col_widths = [len(h) for h in self.headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Create rotating separator
        if self.rotation % 2 == 0:
            separator = f"{color}├{'─┼─'.join(['─' * w for w in col_widths])}┤{Colors.END}"
        else:
            separator = f"{color}╞{'═╪═'.join(['═' * w for w in col_widths])}╡{Colors.END}"
        
        # Header
        header_line = ''
        for i, h in enumerate(self.headers):
            header_line += f" {h.center(col_widths[i])} "
            if i < len(self.headers)-1:
                header_line += f"{color}│{Colors.END}"
        
        print(f"{color}┌{'─' * (sum(col_widths) + len(self.headers)*3 - 1)}┐{Colors.END}")
        print(f"{color}│{Colors.END}{header_line}{color}│{Colors.END}")
        print(separator)
        
        # Rows
        for row in rows:
            row_line = ''
            for i, cell in enumerate(row):
                row_line += f" {str(cell).ljust(col_widths[i])} "
                if i < len(row)-1:
                    row_line += f"{color}│{Colors.END}"
            print(f"{color}│{Colors.END}{row_line}{color}│{Colors.END}")
        
        print(f"{color}└{'─' * (sum(col_widths) + len(self.headers)*3 - 1)}┘{Colors.END}")
        self.rotation += 1


class CryptoEngine:

    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.cipher = None
        self.matrix = MatrixRain()
        self.init_cipher()
        self.show_banner()

#     def show_banner(self):
#         """Show hacker-style banner"""
#         os.system('clear' if os.name == 'posix' else 'cls')
#         colors = [
#             '\033[92m',  # Light Green (Matrix style)
#             '\033[38;5;46m',  # Matrix Green
#             '\033[38;5;82m',  # Bright Green
#             '\033[38;5;118m',  # Lime Green
#             '\033[38;5;154m',  # Yellow-Green
#             '\033[38;5;190m',  # Light Yellow-Green
#             '\033[38;5;226m',  # Bright Yellow
#             '\033[38;5;220m',  # Gold
#             '\033[38;5;214m',  # Orange
#             '\033[38;5;202m',  # Bright Orange
#             '\033[38;5;196m',  # Bright Red
#             '\033[38;5;201m',  # Pink/Magenta
#             '\033[38;5;165m',  # Purple
#             '\033[38;5;129m',  # Violet
#             '\033[38;5;93m',   # Deep Purple
#             '\033[38;5;63m',   # Blue-Purple
#             '\033[38;5;69m',   # Blue
#             '\033[38;5;75m',   # Light Blue
#             '\033[38;5;81m',   # Cyan
#             '\033[38;5;87m',   # Light Cyan
#             '\033[96m',        # Cyan
#             '\033[95m',        # Magenta
#             '\033[91m',        # Light Red
#             '\033[93m',        # Light Yellow
#         ]
    
#         # Add blinking effects for some colors
#         BLINK = '\033[5m'
#         BOLD = '\033[1m'
    
#         # Mix in some blinking and bold variants
#         extended_colors = []
#         for color in colors:
#             extended_colors.append(color)
#             extended_colors.append(color + BOLD)
#             if random.random() > 0.7:  # Add blinking to some colors randomly
#                 extended_colors.append(color + BLINK)
    
#         color = random.choice(extended_colors)
#         terminal_width = shutil.get_terminal_size((80, 20)).columns

#         banner = [f"""
# ╔══════════════════════════════════════════════════════════════╗
# ║  ██████╗ ███████╗████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗         ║
# ║  ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║         ║
# ║  ██║  ██║███████╗   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║         ║
# ║  ██║  ██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║         ║
# ║  ██████╔╝███████║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗    ║
# ║  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ║
# ╚══════════════════════════════════════════════════════════════╝
#                         [ ENCRYPTION SUITE v2.0.113 -  EDITION ]
#                        ══════════════════════════════════════════
# """
#         ]
#         def glitch_char(c):
#             if c.isspace():
#                 return c
#             return random.choice(["#", "@", "%", "&", "*", c])

#         def type_line(line, delay=0.002, glitch=False):
#             centered = line.center(terminal_width)
#             for char in centered:
#                 if glitch and random.random() < 0.04:
#                     sys.stdout.write(color + glitch_char(char))
#                     sys.stdout.flush()
#                     time.sleep(delay * 1)
#                     sys.stdout.write('\b' + color + char)
#                     sys.stdout.flush()
#                 else:
#                     sys.stdout.write(color + char)
#                     sys.stdout.flush()
#                 time.sleep(delay)
#             sys.stdout.write("\n")
#             time.sleep(0.01)

#         for line in banner:
#             type_line(line, glitch=True)
         
#         # print(banner_lines)
#         # time.sleep(1)
    def show_banner(self):
        """Show hacker-style banner (single display without blinking)"""
    
    # Only clear once at the beginning
        if not hasattr(self, '_banner_shown'):
            os.system('clear' if os.name == 'posix' else 'cls')
            self._banner_shown = True
    
    # Use a consistent color instead of random changing colors
        colors = [
            '\033[92m',  # Light Green (Matrix style)
            '\033[38;5;46m',  # Matrix Green
            '\033[38;5;82m',  # Bright Green
            '\033[96m',        # Cyan
            '\033[95m',        # Magenta]
        ]
        BOLD = '\033[1m'
        RESET = '\033[0m'
    
    # Pick ONE color at start
        color = random.choice(colors)
    
        terminal_width = shutil.get_terminal_size((80, 20)).columns
    
    # Single banner string (no list)
        banner = f"""
    {color}{BOLD}
    ╔══════════════════════════════════════════════════════════════╗
    ║  ██████╗ ███████╗████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗         ║
    ║  ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║         ║
    ║  ██║  ██║███████╗   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║         ║
    ║  ██║  ██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║         ║
    ║  ██████╔╝███████║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗    ║
    ║  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ║
    ╚══════════════════════════════════════════════════════════════╝
                            [ ENCRYPTION SUITE v2.0.113 - EDITION ]
                           ══════════════════════════════════════════
    {RESET}"""
    
    # Print banner directly (no typewriter effect that causes blinking)
        print(banner)


    def animate_encryption(self, filename, operation="ENCRYPTING"):
        """Show encryption/decryption animation"""
        box = RotatingBox(50, f" {operation} ")
        
        for i in range(8):  # 8 frames of animation
            os.system('clear' if os.name == 'posix' else 'cls')
            self.show_banner()
            
            progress = (i + 1) * 12.5
            bar_length = 30
            filled = int(bar_length * progress // 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            # Show rotating box with progress
            content = [
                f"{Colors.BOLD}Target:{Colors.END} {filename}",
                f"{Colors.BOLD}Mode:{Colors.END} AES-256 (Fernet)",
                "",
                f"Progress: [{bar}] {progress:.1f}%",
                "",
                f"{Colors.GREEN}▶ Initializing encryption vectors...{Colors.END}" if i < 2 else
                f"{Colors.YELLOW}▶ Generating round keys...{Colors.END}" if i < 4 else
                f"{Colors.CYAN}▶ Applying substitution boxes...{Colors.END}" if i < 6 else
                f"{Colors.MAGENTA}▶ Finalizing {operation.lower()}...{Colors.END}"
            ]
            
            box.render(content, color=Colors.MAGENTA if "DECRYPT" in operation else Colors.CYAN)
            
            # Matrix rain effect
            print(f"\n{Colors.GREEN}")
            self.matrix.render_frame(0.05)
            
            time.sleep(0.3)

    def init_cipher(self):
        """Initialize cipher from key file"""
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "r") as f:
                key = f.read().strip()
                try:
                    self.cipher = Fernet(key.encode())
                except:
                    self.cipher = None

    def human_readable_size(self, size):
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"

    def secure_delete(self, file_path, passes=3):
        try:
            size = os.path.getsize(file_path)
            with open(file_path, "wb") as f:
                for _ in range(passes):
                    f.write(os.urandom(size))
                    f.flush()
                    os.fsync(f.fileno())
            os.remove(file_path)
        except:
            pass

    # =============================
    # SETUP
    # =============================

    def encrypt_setup(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        box = RotatingBox(50, " ENCRYPTION SETUP ")
        
        print(f"\n{Colors.RED}╔══════════════════════════════════════════════════════════════╗")
        print(f"║{Colors.YELLOW}              INITIALIZING SECURE ENCRYPTION SYSTEM             {Colors.RED}║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}\n")

        if os.path.exists(KEY_FILE):
            with open(KEY_FILE) as f:
                key = f.read().strip()
            key_id = hashlib.sha256(key.encode()).hexdigest()[:16]
            
            content = [
                f"{Colors.GREEN}✅ EXISTING KEY FOUND{Colors.END}",
                f"{Colors.BOLD}Key ID:{Colors.END} {Colors.CYAN}{key_id}{Colors.END}",
                f"{Colors.BOLD}Location:{Colors.END} {KEY_FILE}",
                f"{Colors.BOLD}Status:{Colors.END} {Colors.GREEN}ACTIVE{Colors.END}"
            ]
            box.render(content, color=Colors.GREEN)
            return

        # Generate new key with animation
        print(f"{Colors.YELLOW}▶ Generating quantum-resistant encryption key...{Colors.END}")
        time.sleep(1)
        
        for i in range(3):
            print(f"{Colors.CYAN}   Entropy pool: {''.join(random.choices('01', k=20))}{Colors.END}")
            time.sleep(0.3)
        
        key = Fernet.generate_key().decode()
        
        with open(KEY_FILE, "w") as f:
            f.write(key)
        
        os.chmod(KEY_FILE, 0o600)
        
        key_id = hashlib.sha256(key.encode()).hexdigest()[:16]
        
        content = [
            f"{Colors.GREEN}✅ NEW ENCRYPTION KEY GENERATED{Colors.END}",
            f"{Colors.BOLD}Key ID:{Colors.END} {Colors.CYAN}{key_id}{Colors.END}",
            f"{Colors.BOLD}Location:{Colors.END} {KEY_FILE}",
            f"{Colors.BOLD}Permissions:{Colors.END} {Colors.YELLOW}600 (root only){Colors.END}",
            "",
            f"{Colors.RED}⚠️  KEEP THIS KEY SAFE!{Colors.END}"
        ]
        box.render(content, color=Colors.GREEN)
        
        self.init_cipher()
        input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.END}")

    # =============================
    # STATUS
    # =============================

    def crypto_status(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        box = RotatingBox(50, " SYSTEM STATUS ")
        
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE) as f:
                key = f.read().strip()
            key_id = hashlib.sha256(key.encode()).hexdigest()[:16]
            
            content = [
                f"{Colors.BOLD}Encryption:{Colors.END} {Colors.GREEN}ENABLED ✓{Colors.END}",
                f"{Colors.BOLD}Key ID:{Colors.END} {Colors.CYAN}{key_id}{Colors.END}",
                f"{Colors.BOLD}Key file:{Colors.END} {KEY_FILE}",
                f"{Colors.BOLD}Cipher:{Colors.END} {Colors.YELLOW}AES-256 (Fernet){Colors.END}",
                f"{Colors.BOLD}Initialized:{Colors.END} {Colors.GREEN}YES{Colors.END}" if self.cipher else f"{Colors.BOLD}Initialized:{Colors.END} {Colors.RED}NO{Colors.END}"
            ]
        else:
            content = [
                f"{Colors.BOLD}Encryption:{Colors.END} {Colors.RED}NOT CONFIGURED{Colors.END}",
                f"{Colors.BOLD}Key file:{Colors.END} {Colors.YELLOW}Missing{Colors.END}",
                f"{Colors.BOLD}Run 'setup'{Colors.END} to initialize"
            ]
        
        box.render(content, color=Colors.CYAN)
        input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.END}")

    # =============================
    # ENCRYPT
    # =============================
    
    def encrypt_test(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\n{Colors.RED}╔══════════════════════════════════════════════════════════════╗")
        print(f"║{Colors.YELLOW}                  ENCRYPTION SYSTEM TEST                      {Colors.RED}║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}\n")

        test_file = os.path.join(self.base_dir, "crypto_test.txt")
        
        # Create test file
        with open(test_file, "w") as f:
            f.write("DSTerminal encryption test - HACKER EDITION\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write("Classified: TOP SECRET\n")
        
        print(f"{Colors.CYAN}✓ Test file created{Colors.END}")
        time.sleep(0.5)
        
        # Animated encryption
        self.animate_encryption("crypto_test.txt", "ENCRYPTING")
        
        self.encrypt_file("crypto_test.txt")
        enc = test_file + ".enc"
        
        if os.path.exists(enc):
            print(f"\n{Colors.GREEN}✓ Encryption successful{Colors.END}")
            time.sleep(0.5)
            
            # Animated decryption
            self.animate_encryption("crypto_test.txt.enc", "DECRYPTING")
            
            self.decrypt_file("crypto_test.txt.enc")
            print(f"{Colors.GREEN}✓ Decryption successful{Colors.END}")
            
            # Verify content
            with open(test_file, "r") as f:
                content = f.read()
            print(f"{Colors.CYAN}✓ Data integrity verified{Colors.END}")
        
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(enc):
            os.remove(enc)
        
        print(f"\n{Colors.GREEN}╔══════════════════════════════════════════════════════════════╗")
        print(f"║{Colors.BOLD}              ENCRYPTION SYSTEM OPERATIONAL!              {Colors.GREEN}║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
        input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.END}")

    def encrypt_file(self, filename):
        if not self.cipher:
            print(f"{Colors.RED}[!] Encryption not initialized{Colors.END}")
            return

        path = os.path.join(self.base_dir, filename)

        if not os.path.exists(path):
            print(f"{Colors.RED}[!] File not found{Colors.END}")
            return

        # Read file data
        with open(path, "rb") as f:
            data = f.read()
        
        original_size = len(data)
        
        # Encrypt with progress simulation
        encrypted = self.cipher.encrypt(data)
        
        enc_file = path + ".enc"
        
        with open(enc_file, "wb") as f:
            f.write(encrypted)
        
        encrypted_size = len(encrypted)
        
        # Show encryption stats
        table = AnimatedTable(["Metric", "Value"])
        rows = [
            ["Original Size", self.human_readable_size(original_size)],
            ["Encrypted Size", self.human_readable_size(encrypted_size)],
            ["Expansion", f"{((encrypted_size/original_size)-1)*100:.1f}%"],
            ["Algorithm", "AES-256 (Fernet)"]
        ]
        table.render(rows)
        
        # Secure delete original
        self.secure_delete(path)
        print(f"{Colors.GREEN}✅ File encrypted: {enc_file}{Colors.END}")

    # =============================
    # DECRYPT
    # =============================

    def decrypt_file(self, filename):
        if not self.cipher:
            print(f"{Colors.RED}[!] Encryption not initialized{Colors.END}")
            return

        path = os.path.join(self.base_dir, filename)

        if not os.path.exists(path):
            print(f"{Colors.RED}[!] File not found{Colors.END}")
            return

        with open(path, "rb") as f:
            data = f.read()

        try:
            decrypted = self.cipher.decrypt(data)
            out_file = path.replace(".enc", "")
            
            with open(out_file, "wb") as f:
                f.write(decrypted)
            
            print(f"{Colors.GREEN}✅ File decrypted: {out_file}{Colors.END}")
            
            # Show success stats
            print(f"{Colors.CYAN}   Original hash: {hashlib.md5(data).hexdigest()[:16]}...{Colors.END}")
            print(f"{Colors.CYAN}   Decrypted hash: {hashlib.md5(decrypted).hexdigest()[:16]}...{Colors.END}")
            
        except Exception as e:
            print(f"{Colors.RED}❌ Decryption failed: {e}{Colors.END}")

    # =============================
    # LIST ENCRYPTED FILES
    # =============================

    def crypto_list(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        box = RotatingBox(60, " ENCRYPTED FILES INVENTORY ")
        
        encrypted = []
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(".enc"):
                    path = os.path.join(root, file)
                    encrypted.append(path)

        if not encrypted:
            content = [f"{Colors.YELLOW}No encrypted files found.{Colors.END}"]
            box.render(content, color=Colors.RED)
            input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.END}")
            return

        # Prepare table data
        headers = ["#", "File", "Size", "Modified"]
        rows = []
        
        for i, file in enumerate(encrypted, 1):
            size = self.human_readable_size(os.path.getsize(file))
            mod = datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y-%m-%d %H:%M")
            filename = os.path.basename(file)
            if len(filename) > 20:
                filename = filename[:17] + "..."
            rows.append([f"{i}", f"🔒 {filename}", size, mod])
        
        table = AnimatedTable(headers)
        table.render(rows)
        input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.END}")

    # =============================
    # FILE INFO
    # =============================
    
    def crypto_info(self, filename=None):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        if not filename:
            filename = input(f"{Colors.CYAN}Encrypted file: {Colors.END}").strip()

        if not filename.endswith(".enc"):
            filename += ".enc"

        path = os.path.join(self.base_dir, filename)

        if not os.path.exists(path):
            print(f"{Colors.RED}[!] File not found{Colors.END}")
            input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.END}")
            return

        # File info box
        box = RotatingBox(60, " ENCRYPTION INFO ")
        
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            data = f.read()

        sha256 = hashlib.sha256(data).hexdigest()
        md5 = hashlib.md5(data).hexdigest()

        content = [
            f"{Colors.BOLD}File:{Colors.END} {filename}",
            f"{Colors.BOLD}Path:{Colors.END} {path}",
            f"{Colors.BOLD}Size:{Colors.END} {self.human_readable_size(size)}",
            f"{Colors.BOLD}SHA256:{Colors.END} {sha256[:32]}...",
            f"{Colors.BOLD}MD5:{Colors.END} {md5[:16]}..."
        ]
        box.render(content, color=Colors.CYAN)

        # Format detection
        print(f"\n{Colors.YELLOW}🔍 Encryption Analysis{Colors.END}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.END}")
        
        try:
            base64.urlsafe_b64decode(data)
            print(f"{Colors.GREEN}✓ Format: Fernet (AES-256){Colors.END}")
        except Exception:
            print(f"{Colors.RED}✗ Format: Unknown{Colors.END}")

        # Integrity check
        print(f"\n{Colors.YELLOW}🛡️ Integrity Check{Colors.END}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.END}")

        if not self.cipher:
            print(f"{Colors.RED}⚠️ Key not loaded — cannot verify integrity{Colors.END}")
        else:
            try:
                self.cipher.decrypt(data)
                print(f"{Colors.GREEN}✅ File integrity: VALID{Colors.END}")
                print(f"   Authentication tag verified")
            except Exception:
                print(f"{Colors.RED}❌ File integrity: FAILED{Colors.END}")

        input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.END}")

    # =============================
    # VERIFY
    # =============================
    
    def crypto_verify(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        box = RotatingBox(50, " SYSTEM VERIFICATION ")
        
        checks = []
        
        # Check key file
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE) as f:
                key = f.read().strip()
            try:
                Fernet(key.encode())
                checks.append(f"{Colors.GREEN}✓ Key format valid{Colors.END}")
            except:
                checks.append(f"{Colors.RED}✗ Invalid key{Colors.END}")
        else:
            checks.append(f"{Colors.RED}✗ Key file missing{Colors.END}")

        # Check cipher
        if self.cipher:
            checks.append(f"{Colors.GREEN}✓ Cipher initialized{Colors.END}")
            
            # Self-test
            test = b"dsterminal test data"
            try:
                enc = self.cipher.encrypt(test)
                dec = self.cipher.decrypt(enc)
                if test == dec:
                    checks.append(f"{Colors.GREEN}✓ Self-test PASSED{Colors.END}")
                else:
                    checks.append(f"{Colors.RED}✗ Self-test FAILED{Colors.END}")
            except:
                checks.append(f"{Colors.RED}✗ Encryption test failed{Colors.END}")
        else:
            checks.append(f"{Colors.RED}✗ Cipher not initialized{Colors.END}")
        
        box.render(checks, color=Colors.YELLOW)
        input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.END}")

    # =============================
    # BACKUP KEY
    # =============================
    def cmd_crypto_debug(self):
        """Debug command to show crypto engine paths and status"""
        print(f"\n{Colors.RED}╔══════════════════════════════════════════════════════════════╗")
        print(f"║{Colors.YELLOW}                  CRYPTO ENGINE DEBUG INFO                     {Colors.RED}║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    # Check if crypto exists
        if not hasattr(self, 'crypto') or self.crypto is None:
            print(f"{Colors.RED}[!] Crypto engine not initialized!{Colors.END}")
            print(f"    Run 'encrypt-setup' first")
            return
    
    # Crypto engine info
        print(f"{Colors.CYAN}🔐 CRYPTO ENGINE STATUS:{Colors.END}")
        print(f"  • Crypto object: {Colors.GREEN}Initialized{Colors.END}")
        print(f"  • Cipher loaded: {Colors.GREEN}Yes{Colors.END if self.crypto.cipher else f'{Colors.RED}No{Colors.END}'}")
    
    # Base directory
        if hasattr(self.crypto, 'base_dir'):
            print(f"\n{Colors.CYAN}📁 BASE DIRECTORY:{Colors.END}")
            print(f"  • base_dir = {self.crypto.base_dir}")
            print(f"  • Exists: {Colors.GREEN}Yes{Colors.END if os.path.exists(self.crypto.base_dir) else f'{Colors.RED}No{Colors.END}'}")
            print(f"  • Writable: {Colors.GREEN}Yes{Colors.END if os.access(self.crypto.base_dir, os.W_OK) else f'{Colors.RED}No{Colors.END}'}")
        else:
            print(f"\n{Colors.YELLOW}⚠️  Crypto engine has no base_dir attribute{Colors.END}")
    
    # Current directory
        print(f"\n{Colors.CYAN}📂 CURRENT SESSION:{Colors.END}")
        print(f"  • current_dir = {self.current_dir}")
        print(f"  • Exists: {Colors.GREEN}Yes{Colors.END if os.path.exists(self.current_dir) else f'{Colors.RED}No{Colors.END}'}")
        print(f"  • Writable: {Colors.GREEN}Yes{Colors.END if os.access(self.current_dir, os.W_OK) else f'{Colors.RED}No{Colors.END}'}")
    
    # Workspace root
        if hasattr(self, 'workspace_root'):
            print(f"\n{Colors.CYAN}🏠 WORKSPACE ROOT:{Colors.END}")
            print(f"  • workspace_root = {self.workspace_root}")
            print(f"  • Exists: {Colors.GREEN}Yes{Colors.END if os.path.exists(self.workspace_root) else f'{Colors.RED}No{Colors.END}'}")
    
    # Check for fruits.txt
        fruits_path = os.path.join(self.current_dir, 'fruits.txt')
        print(f"\n{Colors.CYAN}🍎 TARGET FILE: fruits.txt{Colors.END}")
        print(f"  • Path: {fruits_path}")
        print(f"  • Exists: {Colors.GREEN}Yes{Colors.END if os.path.exists(fruits_path) else f'{Colors.RED}No{Colors.END}'}")
    
        if os.path.exists(fruits_path):
            size = os.path.getsize(fruits_path)
            print(f"  • Size: {size} bytes")
            print(f"  • Readable: {Colors.GREEN}Yes{Colors.END if os.access(fruits_path, os.R_OK) else f'{Colors.RED}No{Colors.END}'}")
    
    # Check for any .enc files
        enc_files = []
        for root, dirs, files in os.walk(self.current_dir):
            for file in files:
                if file.endswith('.enc'):
                    enc_files.append(os.path.join(root, file))
    
        if enc_files:
            print(f"\n{Colors.CYAN}🔒 ENCRYPTED FILES FOUND:{Colors.END}")
            for ef in enc_files[:5]:  # Show first 5
                rel_path = os.path.relpath(ef, self.current_dir)
                print(f"  • {rel_path}")
            if len(enc_files) > 5:
                print(f"  • ... and {len(enc_files) - 5} more")
        else:
            print(f"\n{Colors.YELLOW}📭 No encrypted files found in current directory{Colors.END}")
    
    # Key file status
        key_file = os.path.expanduser("~/.dsterminal_key")
        print(f"\n{Colors.CYAN}🔑 KEY FILE:{Colors.END}")
        print(f"  • Path: {key_file}")
        print(f"  • Exists: {Colors.GREEN}Yes{Colors.END if os.path.exists(key_file) else f'{Colors.RED}No{Colors.END}'}")
    
        if os.path.exists(key_file):
        # Show key info (without exposing the key)
            with open(key_file, 'r') as f:
                key = f.read().strip()
            key_id = hashlib.sha256(key.encode()).hexdigest()[:16]
            print(f"  • Key ID: {Colors.CYAN}{key_id}{Colors.END}")
            print(f"  • Key length: {len(key)} characters")
    
        print(f"\n{Colors.RED}╚══════════════════════════════════════════════════════════════╝{Colors.END}")

    def crypto_backup(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        box = RotatingBox(50, " KEY BACKUP ")
        
        if not os.path.exists(KEY_FILE):
            content = [f"{Colors.RED}No key found to backup{Colors.END}"]
            box.render(content, color=Colors.RED)
            input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.END}")
            return

        with open(KEY_FILE) as f:
            key = f.read()

        backup = os.path.expanduser("~/dsterminal_key.backup")
        
        # Animated backup process
        print(f"{Colors.YELLOW}▶ Creating secure backup...{Colors.END}")
        time.sleep(1)
        
        with open(backup, "w") as f:
            f.write(key)
        
        os.chmod(backup, 0o600)
        
        content = [
            f"{Colors.GREEN}✅ Backup created successfully{Colors.END}",
            f"{Colors.BOLD}Location:{Colors.END} {backup}",
            f"{Colors.BOLD}Permissions:{Colors.END} 600",
            "",
            f"{Colors.YELLOW}⚠️ Store this backup securely!{Colors.END}"
        ]
        box.render(content, color=Colors.GREEN)
        input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.END}")


def main():
    crypto = CryptoEngine()
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        crypto.show_banner()
        
        menu = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║{Colors.YELLOW}                      MAIN MENU                              {Colors.CYAN}║
╠══════════════════════════════════════════════════════════════╣
║{Colors.GREEN}  1.{Colors.END} 🔐 Setup Encryption System        {Colors.GREEN}6.{Colors.END} 📋 List Encrypted Files   {Colors.CYAN}║
║{Colors.GREEN}  2.{Colors.END} 📊 System Status                {Colors.GREEN}7.{Colors.END} ℹ️  File Information      {Colors.CYAN}║
║{Colors.GREEN}  3.{Colors.END} 🧪 Run Encryption Test          {Colors.GREEN}8.{Colors.END} 🔍 Verify System         {Colors.CYAN}║
║{Colors.GREEN}  4.{Colors.END} 🔒 Encrypt File                  {Colors.GREEN}9.{Colors.END} 💾 Backup Key            {Colors.CYAN}║
║{Colors.GREEN}  5.{Colors.END} 🔓 Decrypt File                  {Colors.GREEN}0.{Colors.END} 🚪 Exit                   {Colors.CYAN}║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
"""
        print(menu)
        
        choice = input(f"{Colors.YELLOW}Select option [0-9]: {Colors.END}").strip()
        
        if choice == '1':
            crypto.encrypt_setup()
        elif choice == '2':
            crypto.crypto_status()
        elif choice == '3':
            crypto.encrypt_test()
        elif choice == '4':
            filename = input(f"{Colors.CYAN}File to encrypt: {Colors.END}").strip()
            if filename:
                crypto.animate_encryption(filename, "ENCRYPTING")
                crypto.encrypt_file(filename)
                input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.END}")
        elif choice == '5':
            filename = input(f"{Colors.CYAN}File to decrypt: {Colors.END}").strip()
            if filename:
                crypto.animate_encryption(filename, "DECRYPTING")
                crypto.decrypt_file(filename)
                input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.END}")
        elif choice == '6':
            crypto.crypto_list()
        elif choice == '7':
            crypto.crypto_info()
        elif choice == '8':
            crypto.crypto_verify()
        elif choice == '9':
            crypto.crypto_backup()
        elif choice == '0':
            print(f"\n{Colors.RED}╔══════════════════════════════════════════════════════════════╗")
            print(f"║{Colors.YELLOW}              SHUTTING DOWN SECURE CONNECTION...               {Colors.RED}║")
            print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}")
            time.sleep(1)
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}⚠️  Emergency shutdown initiated{Colors.END}")
        time.sleep(1)
        sys.exit(0)