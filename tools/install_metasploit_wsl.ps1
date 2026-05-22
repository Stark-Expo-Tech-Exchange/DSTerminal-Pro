# Standalone Metasploit WSL Installer
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Metasploit WSL Installer" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check WSL
if (-not (Get-Command wsl -ErrorAction SilentlyContinue)) {
    Write-Host "WSL is not installed." -ForegroundColor Red
    Write-Host "Please run: wsl --install (as Administrator)" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Installing Metasploit in WSL..." -ForegroundColor Yellow
Write-Host "This will take 10-20 minutes..." -ForegroundColor Cyan
Write-Host ""

wsl bash -c "sudo apt update && sudo apt upgrade -y && sudo apt install metasploit-framework -y"

Write-Host ""
Write-Host "Metasploit installation complete!" -ForegroundColor Green
Write-Host "Run: wsl msfconsole" -ForegroundColor Cyan
pause