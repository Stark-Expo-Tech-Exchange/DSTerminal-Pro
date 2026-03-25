# #!/bin/bash
# # DSTerminal Linux Debian Package Builder
# # Version: 2.0.113
# # For: Parrot OS / Debian / Ubuntu

# set -e

# # Colors for output
# RED='\033[0;31m'
# GREEN='\033[0;32m'
# YELLOW='\033[1;33m'
# BLUE='\033[0;34m'
# NC='\033[0m' # No Color

# echo -e "${BLUE}========================================${NC}"
# echo -e "${GREEN}DSTerminal Linux Debian Package Builder${NC}"
# echo -e "${BLUE}Version: 2.0.113${NC}"
# echo -e "${BLUE}========================================${NC}"

# # Variables
# VERSION="2.0.113"
# PACKAGE_NAME="dsterminal"
# ARCH="amd64"
# BUILD_DIR="build"
# DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}_${ARCH}"
# PYINSTALLER_BIN="dist/dsterminal_linux_amd64"

# # Clean previous builds
# echo -e "${YELLOW}[1/9] Cleaning previous builds...${NC}"
# rm -rf build dist $DEB_ROOT
# mkdir -p $DEB_ROOT/DEBIAN
# mkdir -p $DEB_ROOT/usr/local/bin
# mkdir -p $DEB_ROOT/usr/share/dsterminal/{bin,lib,config,share,scripts}
# mkdir -p $DEB_ROOT/usr/share/applications
# mkdir -p $DEB_ROOT/usr/share/bash-completion/completions
# mkdir -p $DEB_ROOT/usr/share/man/man1
# mkdir -p $DEB_ROOT/usr/share/doc/dsterminal
# mkdir -p $DEB_ROOT/usr/share/icons/hicolor/{scalable,128x128,64x64,32x32}/apps
# mkdir -p $DEB_ROOT/opt/dsterminal/venv

# # Build with PyInstaller
# echo -e "${YELLOW}[2/9] Building with PyInstaller...${NC}"
# pyinstaller --onefile \
#     --collect-all rich \
#     --collect-all tqdm \
#     --collect-all pygments \
#     --add-data "integrity_monitor.py:." \
#     --add-data "crypto_engine.py:." \
#     --add-data "edu_typing_engine.py:." \
#     --add-data "recon.py:." \
#     --add-data "recon_full.py:." \
#     --add-data "VERSION:." \
#     --name dsterminal_linux_amd64 \
#     dsterminal.py

# # Check if build succeeded
# if [ ! -f "$PYINSTALLER_BIN" ]; then
#     echo -e "${RED}Error: PyInstaller build failed!${NC}"
#     exit 1
# fi

# # Copy binary
# echo -e "${YELLOW}[3/9] Copying binary files...${NC}"
# cp $PYINSTALLER_BIN $DEB_ROOT/usr/local/bin/dsterminal
# chmod 755 $DEB_ROOT/usr/local/bin/dsterminal

# # Copy Python modules
# cp integrity_monitor.py $DEB_ROOT/usr/share/dsterminal/lib/
# cp crypto_engine.py $DEB_ROOT/usr/share/dsterminal/lib/
# cp edu_typing_engine.py $DEB_ROOT/usr/share/dsterminal/lib/
# cp recon.py $DEB_ROOT/usr/share/dsterminal/lib/
# cp recon_full.py $DEB_ROOT/usr/share/dsterminal/lib/
# cp VERSION $DEB_ROOT/usr/share/dsterminal/

# # Create requirements file for virtual environment
# echo -e "${YELLOW}[4/9] Creating requirements file...${NC}"
# cat > $DEB_ROOT/opt/dsterminal/requirements.txt << EOF
# altgraph==0.17.4
# certifi==2025.4.26
# cffi==1.17.1
# charset-normalizer==3.4.2
# colorama==0.4.6
# cryptography==45.0.2
# docopt==0.6.2
# fpdf==1.7.2
# gitdb==4.0.12
# gitdb2==4.0.2
# GitPython==3.0.6
# idna==3.10
# markdown-it-py==3.0.0
# mdurl==0.1.2
# netifaces==0.11.0
# packaging==25.0
# pefile==2023.2.7
# pillow==12.1.0
# pipreqs==0.4.13
# prompt_toolkit==3.0.51
# psutil==7.0.0
# py-cpuinfo==9.0.0
# pyClamd==0.4.0
# pycparser==2.22
# pyfiglet==1.0.2
# Pygments==2.19.1
# pyinstaller==6.13.0
# pyinstaller-hooks-contrib==2025.4
# pyOpenSSL==25.1.0
# pywin32-ctypes==0.2.3
# qrcode==8.2
# reportlab==4.4.10
# requests==2.32.3
# rich==14.3.3
# setuptools==80.9.0
# smmap==5.0.2
# stdeb==0.11.0
# tqdm==4.67.1
# truffleHog==2.2.1
# truffleHogRegexes==0.0.7
# typing_extensions==4.13.2
# urllib3==2.4.0
# watchdog==6.0.0
# wcwidth==0.2.13
# wheel==0.45.1
# yarg==0.1.10
# EOF

# # Create virtual environment setup script
# cat > $DEB_ROOT/opt/dsterminal/setup_venv.sh << 'EOF'
# #!/bin/bash
# # Setup virtual environment for DSTerminal

# VENV_DIR="/opt/dsterminal/venv"
# REQUIREMENTS="/opt/dsterminal/requirements.txt"

# # Check if virtual environment exists
# if [ ! -d "$VENV_DIR" ]; then
#     echo "Creating virtual environment for DSTerminal..."
#     python3 -m venv "$VENV_DIR"
# fi

# # Activate and install requirements
# echo "Installing Python dependencies in virtual environment..."
# source "$VENV_DIR/bin/activate"
# pip install --upgrade pip
# pip install -r "$REQUIREMENTS"
# deactivate

# echo "Virtual environment setup complete!"
# EOF

# chmod 755 $DEB_ROOT/opt/dsterminal/setup_venv.sh

# # Create wrapper script that uses virtual environment
# cat > $DEB_ROOT/usr/local/bin/dsterminal-wrapper << 'EOF'
# #!/bin/bash
# # DSTerminal wrapper script with virtual environment

# VENV_DIR="/opt/dsterminal/venv"

# # Check if virtual environment exists, create if not
# if [ ! -d "$VENV_DIR" ]; then
#     echo "Setting up DSTerminal environment (first run only)..."
#     sudo /opt/dsterminal/setup_venv.sh
# fi

# # Run DSTerminal with virtual environment
# source "$VENV_DIR/bin/activate"
# exec /usr/local/bin/dsterminal.bin "$@"
# EOF

# chmod 755 $DEB_ROOT/usr/local/bin/dsterminal-wrapper
# mv $DEB_ROOT/usr/local/bin/dsterminal $DEB_ROOT/usr/local/bin/dsterminal.bin
# mv $DEB_ROOT/usr/local/bin/dsterminal-wrapper $DEB_ROOT/usr/local/bin/dsterminal

# # Create config directory
# echo -e "${YELLOW}[5/9] Creating configuration files...${NC}"
# mkdir -p $DEB_ROOT/etc/dsterminal
# cat > $DEB_ROOT/etc/dsterminal/config.json << EOF
# {
#     "version": "$VERSION",
#     "workspace": "/home/\$USER/.dsterminal_workspace",
#     "auto_update": true,
#     "update_channel": "stable",
#     "log_level": "INFO",
#     "monitor_dirs": ["~/Documents", "~/Downloads"]
# }
# EOF

# # Create desktop entry
# echo -e "${YELLOW}[6/9] Creating desktop entry...${NC}"
# cat > $DEB_ROOT/usr/share/applications/dsterminal.desktop << EOF
# [Desktop Entry]
# Name=DSTerminal
# Comment=Defensive Security Terminal
# Exec=/usr/local/bin/dsterminal
# Icon=dsterminal
# Terminal=true
# Type=Application
# Categories=System;Security;
# StartupNotify=true
# Keywords=security;monitoring;forensics;terminal;
# EOF

# # Create bash completion
# cat > $DEB_ROOT/usr/share/bash-completion/completions/dsterminal << 'EOF'
# _dsterminal_completion() {
#     local cur prev opts
#     COMPREPLY=()
#     cur="${COMP_WORDS[COMP_CWORD]}"
#     prev="${COMP_WORDS[COMP_CWORD-1]}"
#     opts="help exit clear system scan net integrity encrypt decrypt certcheck exploitcheck update"
    
#     case "${prev}" in
#         integrity)
#             COMPREPLY=( $(compgen -W "scan baseline status monitor alerts report list forensic quarantine restore" -- ${cur}) )
#             return 0
#             ;;
#         system)
#             COMPREPLY=( $(compgen -W "scan info" -- ${cur}) )
#             return 0
#             ;;
#         net)
#             COMPREPLY=( $(compgen -W "mon scan" -- ${cur}) )
#             return 0
#             ;;
#         *)
#             ;;
#     esac
    
#     COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
#     return 0
# }
# complete -F _dsterminal_completion dsterminal
# EOF

# # Create man page
# echo -e "${YELLOW}[7/9] Creating man page...${NC}"
# cat > $DEB_ROOT/usr/share/man/man1/dsterminal.1 << EOF
# .TH DSTERMINAL 1 "March 2024" "Version $VERSION" "DSTerminal Manual"
# .SH NAME
# dsterminal \- Defensive Security Terminal
# .SH SYNOPSIS
# .B dsterminal
# [\fIOPTIONS\fR]
# .SH DESCRIPTION
# DSTerminal is a comprehensive security monitoring and analysis platform
# with features including real-time file integrity monitoring, system
# vulnerability scanning, network traffic analysis, and forensic investigation tools.
# .SH OPTIONS
# .TP
# \fBhelp\fR
# Display help information
# .TP
# \fBexit\fR
# Exit the terminal
# .TP
# \fBsystem scan\fR
# Perform system security scan
# .TP
# \fBintegrity monitor\fR
# Start real-time file integrity monitoring
# .SH FILES
# .TP
# \fB/etc/dsterminal/config.json\fR
# System-wide configuration file
# .TP
# \fB~/.dsterminal_workspace\fR
# User workspace directory
# .SH AUTHOR
# Spark Wilson Spink <spark@starkexpotechexchange-mw.com>
# .SH SEE ALSO
# Full documentation: /usr/share/doc/dsterminal/
# EOF

# gzip -9 $DEB_ROOT/usr/share/man/man1/dsterminal.1

# # Create documentation
# echo -e "${YELLOW}[8/9] Creating documentation...${NC}"
# cat > $DEB_ROOT/usr/share/doc/dsterminal/README << EOF
# DSTerminal - Defensive Security Terminal
# Version: $VERSION

# Description:
# DSTerminal is a comprehensive security monitoring and analysis platform
# designed for security professionals and system administrators.

# Features:
# - Real-time file integrity monitoring
# - System vulnerability scanning
# - Network traffic analysis
# - Forensic investigation tools
# - Encryption/decryption utilities
# - Certificate validation
# - And much more...

# Installation:
# The package is now installed. Run 'dsterminal' to start.

# First Run:
# On first run, DSTerminal will automatically set up a Python virtual environment
# and install all required dependencies. This may take a few minutes.

# Documentation:
# - Man page: man dsterminal
# - Online: https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest

# Support:
# - GitHub Issues: https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/issues
# - Email: support@starkexpotechexchange-mw.com

# Copyright © 2024 Stark Expo Tech Exchange
# EOF

# # Create changelog
# cat > $DEB_ROOT/usr/share/doc/dsterminal/changelog << EOF
# dsterminal ($VERSION) stable; urgency=medium

#   * Initial Debian package release
#   * Real-time file integrity monitoring
#   * System vulnerability scanning
#   * Network traffic analysis
#   * Forensic investigation tools
#   * Encryption/decryption utilities
#   * SSL/TLS certificate validation
#   * System hardening tools
#   * Virtual environment support for Python dependencies

#  -- Spark Wilson Spink <spark@starkexpotechexchange-mw.com>  $(date -R)
# EOF

# gzip -9 $DEB_ROOT/usr/share/doc/dsterminal/changelog

# # Copy copyright
# cp LICENSE $DEB_ROOT/usr/share/doc/dsterminal/copyright 2>/dev/null || echo "License file not found" > $DEB_ROOT/usr/share/doc/dsterminal/copyright

# # Create DEBIAN control file
# echo -e "${YELLOW}[9/9] Creating Debian control file...${NC}"
# cat > $DEB_ROOT/DEBIAN/control << EOF
# Package: $PACKAGE_NAME
# Version: $VERSION
# Section: utils
# Priority: optional
# Architecture: $ARCH
# Maintainer: Spark Wilson Spink <spark@starkexpotechexchange-mw.com>
# Description: Defensive Security Terminal
#  DSTerminal is a comprehensive security monitoring and analysis platform
#  with features including:
#   * Real-time file integrity monitoring
#   * System vulnerability scanning
#   * Network traffic analysis
#   * Forensic investigation tools
#   * Encryption/decryption utilities
#   * SSL/TLS certificate validation
#   * System hardening tools
# Homepage: https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest
# Depends: python3 (>= 3.8), python3-venv, python3-full
# Recommends: python3-pip
# Suggests: nmap, sqlmap, metasploit-framework
# EOF

# # Create post-installation script (without pip install)
# cat > $DEB_ROOT/DEBIAN/postinst << 'EOF'
# #!/bin/bash
# set -e

# # Create workspace directories for each user
# for user_home in /home/*; do
#     if [ -d "$user_home" ]; then
#         username=$(basename "$user_home")
#         WORKSPACE="$user_home/.dsterminal_workspace"
        
#         if [ ! -d "$WORKSPACE" ]; then
#             mkdir -p "$WORKSPACE"/{operators,scans,reports,exploits,sandbox,quarantine,logs,config}
#             chown -R "$username":"$username" "$WORKSPACE" 2>/dev/null || true
#         fi
#     fi
# done

# # Set permissions
# chmod -R 755 /usr/share/dsterminal
# chmod 755 /usr/local/bin/dsterminal
# chmod 755 /opt/dsterminal/setup_venv.sh

# # Update icon cache
# if command -v update-icon-caches >/dev/null 2>&1; then
#     update-icon-caches /usr/share/icons/hicolor
# fi

# # Update desktop database
# if command -v update-desktop-database >/dev/null 2>&1; then
#     update-desktop-database /usr/share/applications
# fi

# echo "DSTerminal installed successfully!"
# echo ""
# echo "First run will set up the Python environment (may take a few minutes)."
# echo "Run 'dsterminal' to start the terminal"
# echo "Documentation: man dsterminal"
# EOF

# chmod 755 $DEB_ROOT/DEBIAN/postinst

# # Create post-removal script
# cat > $DEB_ROOT/DEBIAN/prerm << 'EOF'
# #!/bin/bash
# set -e

# # Ask about removing workspace for current user
# if [ -d "$HOME/.dsterminal_workspace" ]; then
#     echo "Do you want to remove your DSTerminal workspace data? (y/N)"
#     read -r response
#     if [[ "$response" =~ ^[Yy]$ ]]; then
#         rm -rf "$HOME/.dsterminal_workspace"
#         echo "Workspace data removed."
#     else
#         echo "Workspace data preserved at $HOME/.dsterminal_workspace"
#     fi
# fi

# # Ask about removing virtual environment
# if [ -d "/opt/dsterminal/venv" ]; then
#     echo "Do you want to remove the DSTerminal virtual environment? (y/N)"
#     read -r response
#     if [[ "$response" =~ ^[Yy]$ ]]; then
#         rm -rf "/opt/dsterminal/venv"
#         echo "Virtual environment removed."
#     fi
# fi
# EOF

# chmod 755 $DEB_ROOT/DEBIAN/prerm

# # Build the Debian package
# echo -e "${GREEN}Building Debian package...${NC}"
# cd $BUILD_DIR
# dpkg-deb --build ${PACKAGE_NAME}_${VERSION}_${ARCH}
# cd ..

# # Move the package to current directory
# mv $DEB_ROOT.deb .

# # Clean up build directory
# echo -e "${YELLOW}Cleaning up...${NC}"
# rm -rf build dist

# echo -e "${GREEN}========================================${NC}"
# echo -e "${GREEN}✅ Debian package created successfully!${NC}"
# echo -e "${GREEN}========================================${NC}"
# echo -e "${BLUE}Package: ${PACKAGE_NAME}_${VERSION}_${ARCH}.deb${NC}"
# echo -e "${BLUE}Size: $(du -h ${PACKAGE_NAME}_${VERSION}_${ARCH}.deb | cut -f1)${NC}"
# echo -e ""
# echo -e "${YELLOW}To install:${NC}"
# echo -e "  sudo dpkg -i ${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
# echo -e "  sudo apt-get install -f  # Install dependencies"
# echo -e ""
# echo -e "${YELLOW}To run:${NC}"
# echo -e "  dsterminal"
# echo -e ""
# echo -e "${YELLOW}To uninstall:${NC}"
# echo -e "  sudo dpkg -r dsterminal"
# echo -e "${GREEN}========================================${NC}"


#!/bin/bash
# DSTerminal Linux Debian Package Builder
# Version: 2.0.113
# Self-contained - No external Python dependencies required!

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}DSTerminal Linux Debian Package Builder${NC}"
echo -e "${BLUE}Self-contained - No external Python deps${NC}"
echo -e "${BLUE}Version: 2.0.113${NC}"
echo -e "${BLUE}========================================${NC}"

# Variables
VERSION="2.0.113"
PACKAGE_NAME="dsterminal"
ARCH="amd64"
BUILD_DIR="build"
DEB_ROOT="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}_${ARCH}"
PYINSTALLER_BIN="dist/dsterminal_linux_amd64"

# Clean previous builds
echo -e "${YELLOW}[1/7] Cleaning previous builds...${NC}"
rm -rf build dist $DEB_ROOT
mkdir -p $DEB_ROOT/DEBIAN
mkdir -p $DEB_ROOT/usr/local/bin
mkdir -p $DEB_ROOT/usr/share/dsterminal/lib
mkdir -p $DEB_ROOT/usr/share/applications
mkdir -p $DEB_ROOT/usr/share/bash-completion/completions
mkdir -p $DEB_ROOT/usr/share/man/man1
mkdir -p $DEB_ROOT/usr/share/doc/dsterminal
mkdir -p $DEB_ROOT/usr/share/icons/hicolor/{scalable,128x128,64x64,32x32}/apps

# Build with PyInstaller (bundles ALL dependencies)
echo -e "${YELLOW}[2/7] Building self-contained executable with PyInstaller...${NC}"
pyinstaller --onefile \
    --name dsterminal_linux_amd64 \
    --add-data "integrity_monitor.py:." \
    --add-data "crypto_engine.py:." \
    --add-data "edu_typing_engine.py:." \
    --add-data "recon.py:." \
    --add-data "recon_full.py:." \
    --add-data "VERSION:." \
    --hidden-import=colorama \
    --hidden-import=prompt_toolkit \
    --hidden-import=pyfiglet \
    --hidden-import=rich \
    --hidden-import=tqdm \
    --hidden-import=psutil \
    --hidden-import=netifaces \
    --hidden-import=requests \
    --hidden-import=watchdog \
    --hidden-import=cryptography \
    --hidden-import=OpenSSL \
    --hidden-import=reportlab \
    --hidden-import=fpdf \
    --collect-all colorama \
    --collect-all prompt_toolkit \
    --collect-all pyfiglet \
    --collect-all rich \
    --collect-all tqdm \
    --collect-all psutil \
    --collect-all netifaces \
    --collect-all requests \
    --collect-all watchdog \
    --collect-all cryptography \
    --collect-all pyOpenSSL \
    --collect-all reportlab \
    --collect-all fpdf \
    dsterminal.py

# Check if build succeeded
if [ ! -f "$PYINSTALLER_BIN" ]; then
    echo -e "${RED}Error: PyInstaller build failed!${NC}"
    exit 1
fi

# Copy the standalone binary
echo -e "${YELLOW}[3/7] Copying standalone binary...${NC}"
cp $PYINSTALLER_BIN $DEB_ROOT/usr/local/bin/dsterminal
chmod 755 $DEB_ROOT/usr/local/bin/dsterminal

# Copy support files (these are needed at runtime by the binary)
echo -e "${YELLOW}[4/7] Copying support files...${NC}"
cp integrity_monitor.py $DEB_ROOT/usr/share/dsterminal/lib/ 2>/dev/null || true
cp crypto_engine.py $DEB_ROOT/usr/share/dsterminal/lib/ 2>/dev/null || true
cp edu_typing_engine.py $DEB_ROOT/usr/share/dsterminal/lib/ 2>/dev/null || true
cp recon.py $DEB_ROOT/usr/share/dsterminal/lib/ 2>/dev/null || true
cp recon_full.py $DEB_ROOT/usr/share/dsterminal/lib/ 2>/dev/null || true
cp VERSION $DEB_ROOT/usr/share/dsterminal/

# Create config directory
echo -e "${YELLOW}[5/7] Creating configuration files...${NC}"
mkdir -p $DEB_ROOT/etc/dsterminal
cat > $DEB_ROOT/etc/dsterminal/config.json << EOF
{
    "version": "$VERSION",
    "workspace": "\$HOME/.dsterminal_workspace",
    "auto_update": true,
    "update_channel": "stable",
    "log_level": "INFO"
}
EOF

# Create desktop entry
cat > $DEB_ROOT/usr/share/applications/dsterminal.desktop << EOF
[Desktop Entry]
Name=DSTerminal
Comment=Defensive Security Terminal
Exec=/usr/local/bin/dsterminal
Icon=dsterminal
Terminal=true
Type=Application
Categories=System;Security;
StartupNotify=true
Keywords=security;monitoring;forensics;
EOF

# Create bash completion
cat > $DEB_ROOT/usr/share/bash-completion/completions/dsterminal << 'EOF'
_dsterminal_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="help exit clear system scan net integrity encrypt decrypt certcheck exploitcheck update"
    
    case "${prev}" in
        integrity)
            COMPREPLY=( $(compgen -W "scan baseline status monitor alerts report list forensic quarantine restore" -- ${cur}) )
            return 0
            ;;
        system)
            COMPREPLY=( $(compgen -W "scan info" -- ${cur}) )
            return 0
            ;;
        net)
            COMPREPLY=( $(compgen -W "mon scan" -- ${cur}) )
            return 0
            ;;
        *)
            ;;
    esac
    
    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    return 0
}
complete -F _dsterminal_completion dsterminal
EOF

# Create man page
cat > $DEB_ROOT/usr/share/man/man1/dsterminal.1 << EOF
.TH DSTERMINAL 1 "March 2024" "Version $VERSION" "DSTerminal Manual"
.SH NAME
dsterminal \- Defensive Security Terminal
.SH SYNOPSIS
.B dsterminal
[\fIOPTIONS\fR]
.SH DESCRIPTION
DSTerminal is a comprehensive security monitoring and analysis platform
with features including real-time file integrity monitoring, system
vulnerability scanning, network traffic analysis, and forensic investigation tools.
.SH OPTIONS
.TP
\fBhelp\fR
Display help information
.TP
\fBexit\fR
Exit the terminal
.TP
\fBsystem scan\fR
Perform system security scan
.TP
\fBintegrity monitor\fR
Start real-time file integrity monitoring
.SH FILES
.TP
\fB/etc/dsterminal/config.json\fR
System-wide configuration file
.TP
\fB~/.dsterminal_workspace\fR
User workspace directory
.SH AUTHOR
Spark Wilson Spink <spark@starkexpotechexchange-mw.com>
.SH SEE ALSO
Full documentation: /usr/share/doc/dsterminal/
EOF

gzip -9 $DEB_ROOT/usr/share/man/man1/dsterminal.1

# Create documentation
echo -e "${YELLOW}[6/7] Creating documentation...${NC}"
cat > $DEB_ROOT/usr/share/doc/dsterminal/README << EOF
DSTerminal - Defensive Security Terminal
Version: $VERSION

Description:
DSTerminal is a comprehensive security monitoring and analysis platform
designed for security professionals and system administrators.

Features:
- Real-time file integrity monitoring
- System vulnerability scanning
- Network traffic analysis
- Forensic investigation tools
- Encryption/decryption utilities
- Certificate validation
- System hardening tools

Installation:
The package is now installed. Run 'dsterminal' to start.

Requirements:
- No additional Python packages needed!
- Everything is bundled in the executable.

Documentation:
- Man page: man dsterminal
- Online: https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest

Support:
- GitHub Issues: https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/issues
- Email: support@starkexpotechexchange-mw.com

Copyright © 2024 Stark Expo Tech Exchange
EOF

# Create changelog
cat > $DEB_ROOT/usr/share/doc/dsterminal/changelog << EOF
dsterminal ($VERSION) stable; urgency=medium

  * Initial Debian package release
  * Self-contained executable - No Python dependencies required!
  * Real-time file integrity monitoring
  * System vulnerability scanning
  * Network traffic analysis
  * Forensic investigation tools
  * Encryption/decryption utilities
  * SSL/TLS certificate validation
  * System hardening tools

 -- Spark Wilson Spink <spark@starkexpotechexchange-mw.com>  $(date -R)
EOF

gzip -9 $DEB_ROOT/usr/share/doc/dsterminal/changelog

# Copy license
cp LICENSE $DEB_ROOT/usr/share/doc/dsterminal/copyright 2>/dev/null || echo "License file not found" > $DEB_ROOT/usr/share/doc/dsterminal/copyright

# Create DEBIAN control file (minimal dependencies)
echo -e "${YELLOW}[7/7] Creating Debian control file...${NC}"
cat > $DEB_ROOT/DEBIAN/control << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Maintainer: Spark Wilson Spink <spark@starkexpotechexchange-mw.com>
Description: Defensive Security Terminal
 DSTerminal is a comprehensive security monitoring and analysis platform
 with features including:
  * Real-time file integrity monitoring
  * System vulnerability scanning
  * Network traffic analysis
  * Forensic investigation tools
  * Encryption/decryption utilities
  * SSL/TLS certificate validation
  * System hardening tools
 .
 This package is self-contained and requires NO additional Python packages.
 Everything needed is bundled in the executable.
Homepage: https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest
Depends: libc6 (>= 2.28)
Recommends: nmap, sqlmap
Suggests: metasploit-framework, wireshark
EOF

# Create simple post-installation script
cat > $DEB_ROOT/DEBIAN/postinst << 'EOF'
#!/bin/bash
set -e

echo "DSTerminal v2.0.113 installed successfully!"

# Create workspace directories for current user
WORKSPACE="$HOME/.dsterminal_workspace"
if [ ! -d "$WORKSPACE" ]; then
    mkdir -p "$WORKSPACE"/{operators,scans,reports,exploits,sandbox,quarantine,logs,config}
    echo "Workspace created at: $WORKSPACE"
fi

# Update icon cache (don't fail if command doesn't exist)
if command -v update-icon-caches >/dev/null 2>&1; then
    update-icon-caches /usr/share/icons/hicolor 2>/dev/null || true
fi

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications 2>/dev/null || true
fi

echo ""
echo "✅ DSTerminal is ready to use!"
echo ""
echo "To start: dsterminal"
echo "For help: dsterminal help"
echo "Documentation: man dsterminal"
echo ""

exit 0
EOF

chmod 755 $DEB_ROOT/DEBIAN/postinst

# Create post-removal script
cat > $DEB_ROOT/DEBIAN/prerm << 'EOF'
#!/bin/bash
set -e

# Ask about removing workspace
if [ -d "$HOME/.dsterminal_workspace" ]; then
    echo ""
    echo "Do you want to remove your DSTerminal workspace data? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        rm -rf "$HOME/.dsterminal_workspace"
        echo "Workspace data removed."
    else
        echo "Workspace data preserved at $HOME/.dsterminal_workspace"
    fi
fi

exit 0
EOF

chmod 755 $DEB_ROOT/DEBIAN/prerm

# Build the Debian package
echo -e "${GREEN}Building Debian package...${NC}"
cd $BUILD_DIR
dpkg-deb --build ${PACKAGE_NAME}_${VERSION}_${ARCH}
cd ..

# Move the package to current directory
mv $DEB_ROOT.deb .

# Clean up build directory
echo -e "${YELLOW}Cleaning up...${NC}"
rm -rf build

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Debian package created successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${BLUE}Package: ${PACKAGE_NAME}_${VERSION}_${ARCH}.deb${NC}"
echo -e "${BLUE}Size: $(du -h ${PACKAGE_NAME}_${VERSION}_${ARCH}.deb | cut -f1)${NC}"
echo -e ""
echo -e "${YELLOW}To install:${NC}"
echo -e "  sudo dpkg -i ${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
echo -e ""
echo -e "${YELLOW}To run:${NC}"
echo -e "  dsterminal"
echo -e ""
echo -e "${YELLOW}To uninstall:${NC}"
echo -e "  sudo dpkg -r dsterminal"
echo -e "${GREEN}========================================${NC}"