# Python Packages Installer
Write-Host "Installing Python packages..." -ForegroundColor Cyan
Write-Host ""

# Find Python executable
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-Host "ERROR: Python is not installed" -ForegroundColor Red
    Write-Host "Please install Python from: https://python.org/downloads" -ForegroundColor Yellow
    exit 1
}

Write-Host "Using: $pythonCmd" -ForegroundColor Cyan
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
& $pythonCmd -m pip install --upgrade pip --quiet

# Install packages
$packages = @("colorama", "requests", "folium", "plotly", "reportlab")
$failed = @()

foreach ($pkg in $packages) {
    Write-Host "Installing $pkg..." -ForegroundColor Yellow
    & $pythonCmd -m pip install $pkg --quiet
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] $pkg installed" -ForegroundColor Green
    } else {
        Write-Host "  [X] $pkg failed" -ForegroundColor Red
        $failed += $pkg
    }
}

Write-Host ""
if ($failed.Count -eq 0) {
    Write-Host "SUCCESS: All packages installed" -ForegroundColor Green
    exit 0
} else {
    Write-Host "WARNING: Failed to install: $($failed -join ', ')" -ForegroundColor Yellow
    exit 1
}