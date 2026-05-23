# Complete DSTERMINAL Dependency Installer - No Admin Required
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DSTERMINAL - Complete Dependency Installer" -ForegroundColor Green
Write-Host "  (No Administrator Required)" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$failed = @()
$installed = @()

# ============================================
# Check Python
# ============================================
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
Write-Host ""

$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
    $pythonVersion = & python --version 2>$null
    Write-Host "  [OK] Python: $pythonVersion" -ForegroundColor Green
    $installed += "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
    $pythonVersion = & python3 --version 2>$null
    Write-Host "  [OK] Python3: $pythonVersion" -ForegroundColor Green
    $installed += "python"
} else {
    Write-Host "  [X] Python not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python from Microsoft Store or python.org" -ForegroundColor Yellow
    Write-Host "Then re-run this installer." -ForegroundColor Yellow
    Start-Process "https://python.org/downloads"
    pause
    exit 1
}

Write-Host ""

# ============================================
# Install Python Packages
# ============================================
Write-Host "[2/5] Installing Python Packages..." -ForegroundColor Yellow
Write-Host ""

$packages = @("colorama", "requests", "folium", "plotly", "reportlab")

foreach ($pkg in $packages) {
    Write-Host "  Installing $pkg..." -ForegroundColor Cyan
    & $pythonCmd -m pip install $pkg --user --quiet
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] $pkg" -ForegroundColor Green
        $installed += $pkg
    } else {
        Write-Host "  [X] $pkg failed" -ForegroundColor Red
        $failed += $pkg
    }
}

Write-Host ""

# ============================================
# Install SQLMap
# ============================================
Write-Host "[3/5] Installing SQLMap..." -ForegroundColor Yellow
Write-Host ""

if (Get-Command sqlmap -ErrorAction SilentlyContinue) {
    Write-Host "  [OK] SQLMap already installed" -ForegroundColor Green
    $installed += "sqlmap"
} else {
    Write-Host "  Installing SQLMap via pip..." -ForegroundColor Cyan
    & $pythonCmd -m pip install sqlmap --user --quiet
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] SQLMap installed" -ForegroundColor Green
        $installed += "sqlmap"
    } else {
        Write-Host "  [X] SQLMap installation failed" -ForegroundColor Red
        $failed += "sqlmap"
    }
}

Write-Host ""

# ============================================
# Check Nmap (Cannot install without admin)
# ============================================
Write-Host "[4/5] Checking Nmap..." -ForegroundColor Yellow
Write-Host ""

if (Get-Command nmap -ErrorAction SilentlyContinue) {
    $nmapVersion = & nmap --version 2>$null | Select-Object -First 1
    Write-Host "  [OK] Nmap: $nmapVersion" -ForegroundColor Green
    $installed += "nmap"
} else {
    Write-Host "  [WARN] Nmap not installed" -ForegroundColor Yellow
    Write-Host "  Nmap requires Administrator privileges to install." -ForegroundColor Cyan
    Write-Host "  Please install manually from: https://nmap.org/download.html" -ForegroundColor White
    $failed += "nmap (manual)"
}

Write-Host ""

# ============================================
# Summary
# ============================================
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INSTALLATION SUMMARY" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($installed.Count -gt 0) {
    Write-Host "Successfully installed/verified:" -ForegroundColor Green
    foreach ($item in $installed | Select-Object -Unique) {
        Write-Host "  [OK] $item" -ForegroundColor Green
    }
}

if ($failed.Count -gt 0) {
    Write-Host ""
    Write-Host "Manual installation needed:" -ForegroundColor Yellow
    foreach ($item in $failed) {
        Write-Host "  [!] $item" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "DSTerminal is ready to use!" -ForegroundColor Green
Write-Host ""
Write-Host "To start DSTERMINAL:" -ForegroundColor Cyan
Write-Host "  Click the installer.." -ForegroundColor White

Write-Host ""
pause