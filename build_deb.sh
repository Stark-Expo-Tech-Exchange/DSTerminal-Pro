#!/bin/bash

set -e

APP_NAME="dsterminal"
VERSION="2.1.327"
ARCH="amd64"

BUILD_DIR="${APP_NAME}_${VERSION}"

echo "[*] Cleaning old builds..."
rm -rf "$BUILD_DIR"
rm -f "${BUILD_DIR}.deb"

echo "[*] Creating package structure..."

mkdir -p "$BUILD_DIR/DEBIAN"
mkdir -p "$BUILD_DIR/opt/dsterminal"
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

# ================= COPY MAIN FILE =================

echo "[*] Copying DSTerminal..."

cp dsterminal.py "$BUILD_DIR/opt/dsterminal/"

# ================= COPY ICON =================

if [ -f logo.png ]; then
    cp logo.png "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/dsterminal.png"
fi

# ================= LAUNCHER (TEMP PLACEHOLDER) =================

echo "[*] Creating launcher..."

cat > "$BUILD_DIR/usr/bin/dsterminal" << 'EOF'
#!/bin/bash
/opt/dsterminal/venv/bin/python /opt/dsterminal/dsterminal.py "$@"
EOF

chmod 755 "$BUILD_DIR/usr/bin/dsterminal"

# ================= DESKTOP ENTRY =================

echo "[*] Creating desktop entry..."

cat > "$BUILD_DIR/usr/share/applications/dsterminal.desktop" << EOF
[Desktop Entry]
Version=$VERSION
Name=DSTerminal
Comment=Cyber Operations Command Center
Exec=dsterminal
Icon=dsterminal
Terminal=true
Type=Application
Categories=Utility;Security;
EOF

# ================= CONTROL FILE =================

echo "[*] Creating Debian control file..."

cat > "$BUILD_DIR/DEBIAN/control" << EOF
Package: dsterminal
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Maintainer: Stark Expo Tech Exchange
Depends: python3, python3-venv, python3-pip, nmap
Description: DSTerminal Cyber Operations Platform
 Advanced Cybersecurity Operations Toolkit with SOC automation engine
EOF

# ================= POST INSTALL (FIXED PEP 668 SAFE) =================

echo "[*] Creating post-install script..."

cat > "$BUILD_DIR/DEBIAN/postinst" << 'EOF'
#!/bin/bash

set -e

echo "[*] Setting up DSTerminal virtual environment..."

APP_DIR="/opt/dsterminal"
VENV="$APP_DIR/venv"

mkdir -p "$APP_DIR"

# Create venv if missing
if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
fi

# Upgrade pip inside venv
"$VENV/bin/pip" install --upgrade pip

# Install dependencies INSIDE venv (safe)
"$VENV/bin/pip" install \
    requests \
    rich \
    psutil \
    colorama \
    pyfiglet \
    netifaces

echo "[*] Fixing launcher permissions..."
chmod +x /usr/bin/dsterminal

echo "[+] DSTerminal installed successfully"
EOF

chmod 755 "$BUILD_DIR/DEBIAN/postinst"

# ================= BUILD PACKAGE =================

echo "[*] Building .deb package..."

dpkg-deb --root-owner-group --build "$BUILD_DIR"

echo ""
echo "[+] BUILD SUCCESSFUL"
echo "[+] PACKAGE:"
echo "${BUILD_DIR}.deb"