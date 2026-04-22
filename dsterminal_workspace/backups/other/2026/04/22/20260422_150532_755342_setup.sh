#!/bin/bash
# COMPLETE DSTerminal Setup Script

set -e  # Exit on any error

echo "=========================================="
echo "   DSTerminal Complete Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check Python version
print_status "Checking Python version..."
python3 --version

# Remove old virtual environment if exists
if [ -d "venv" ]; then
    print_info "Removing old virtual environment..."
    rm -rf venv
fi

# Create fresh virtual environment
print_status "Creating new virtual environment..."
python3 -m venv venv --system-site-packages

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip inside venv
print_status "Upgrading pip..."
python -m pip install --upgrade pip --quiet

# Install ALL required packages
print_status "Installing dependencies..."
pip install \
    cryptography>=42.0.0 \
    requests>=2.31.0 \
    colorama>=0.4.6 \
    rich>=13.0.0 \
    prompt_toolkit>=3.0.0 \
    pyfiglet>=0.8.post1 \
    --quiet

# Verify installations
print_status "Verifying installations..."
echo ""
echo "Installed packages:"
pip list | grep -E "(cryptography|requests|colorama|rich|prompt_toolkit|pyfiglet)"

# Create easy activation script
cat > start_dsterminal.sh << 'SCRIPTEOF'
#!/bin/bash
# DSTerminal Starter Script

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
source "$DIR/venv/bin/activate"

echo "=========================================="
echo "   DSTerminal Environment Activated"
echo "=========================================="
echo ""
echo "Available commands:"
echo "  - 'deactivate' to exit this environment"
echo "  - 'pip list' to see installed packages"
echo ""
echo "Now you can run your DSTerminal application."
echo "Example: python main.py"
echo ""
SCRIPTEOF

chmod +x start_dsterminal.sh

# Create a simple test script to verify everything works
cat > test_installation.py << 'PYEOF'
#!/usr/bin/env python3
import cryptography
import requests
import colorama
import rich
import prompt_toolkit
import pyfiglet

print("✅ All imports successful!")
print(f"cryptography version: {cryptography.__version__}")
print(f"requests version: {requests.__version__}")
print(f"colorama version: {colorama.__version__}")
print(f"rich version: {rich.__version__}")
print(f"prompt_toolkit version: {prompt_toolkit.__version__}")

# Test pyfiglet
font = pyfiglet.Figlet()
print("\n" + font.renderText('DSTerminal'))
print("✅ All dependencies are working correctly!")
PYEOF

chmod +x test_installation.py

print_status "Testing the installation..."
python test_installation.py

echo ""
echo "=========================================="
echo "   SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "✅ All dependencies have been installed successfully!"
echo ""
echo "To start using DSTerminal, run:"
echo "   ./start_dsterminal.sh"
echo ""
echo "Or manually:"
echo "   source venv/bin/activate"
echo ""
echo "Your virtual environment is ready at:"
echo "   $(pwd)/venv/"
echo ""
