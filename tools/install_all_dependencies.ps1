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
# Metasploit Installation (WSL Alternative)
# ============================================
Write-Host "[5/5] Setting up Metasploit Framework..." -ForegroundColor Yellow
Write-Host ""

if (Get-Command msfconsole -ErrorAction SilentlyContinue) {
    $msfVersion = & msfconsole --version 2>$null
    Write-Host "  [OK] Metasploit already installed" -ForegroundColor Green
    Write-Host "  Version: $msfVersion" -ForegroundColor Cyan
    $installed += "metasploit"
} else {
    Write-Host "  Metasploit not found. Checking for WSL..." -ForegroundColor Cyan
    
    # Check if WSL is installed
    $wslCheck = Get-Command wsl -ErrorAction SilentlyContinue
    if ($wslCheck) {
        Write-Host "  WSL is installed. Checking WSL for Metasploit..." -ForegroundColor Cyan
        
        # Check if Metasploit is installed in WSL
        $msfInWsl = wsl bash -c "command -v msfconsole" 2>$null
        if ($msfInWsl) {
            Write-Host "  [OK] Metasploit is already installed in WSL" -ForegroundColor Green
            $installed += "metasploit (WSL)"
        } else {
            Write-Host ""
            Write-Host "  Would you like to install Metasploit in WSL?" -ForegroundColor Yellow
            Write-Host "  (This will take 10-20 minutes and requires ~1GB of disk space)" -ForegroundColor Cyan
            Write-Host ""
            
            $installMsf = Read-Host "  Install Metasploit in WSL? (y/n)"
            if ($installMsf -eq 'y') {
                Write-Host ""
                Write-Host "  Installing Metasploit in WSL..." -ForegroundColor Yellow
                Write-Host "  This may take a while. Please be patient..." -ForegroundColor DarkYellow
                Write-Host ""
                
                # Update WSL and install Metasploit
                Write-Host "  Step 1: Updating WSL packages..." -ForegroundColor Cyan
                wsl bash -c "sudo apt update && sudo apt upgrade -y" 2>$null
                
                Write-Host ""
                Write-Host "  Step 2: Installing Metasploit Framework..." -ForegroundColor Cyan
                wsl bash -c "sudo apt install metasploit-framework -y" 2>$null
                
                Write-Host ""
                Write-Host "  Step 3: Verifying installation..." -ForegroundColor Cyan
                $msfVersion = wsl bash -c "msfconsole --version" 2>$null
                
                if ($msfVersion) {
                    Write-Host ""
                    Write-Host "  [OK] Metasploit installed successfully in WSL!" -ForegroundColor Green
                    Write-Host "  Version: $msfVersion" -ForegroundColor Cyan
                    $installed += "metasploit (WSL)"
                    
                    # Create alias function
                    $profilePath = "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
                    if (-not (Test-Path $profilePath)) {
                        New-Item -ItemType File -Path $profilePath -Force | Out-Null
                    }
                    
                    $aliasFunction = @"
# Metasploit WSL Alias for DSTERMINAL
function msfconsole { wsl msfconsole `$args }
function msfvenom { wsl msfvenom `$args }
"@
                    
                    if ((Get-Content $profilePath -Raw) -notmatch "Metasploit WSL Alias") {
                        Add-Content -Path $profilePath -Value "`n$aliasFunction"
                        Write-Host "  Added PowerShell aliases for msfconsole and msfvenom" -ForegroundColor Cyan
                    }
                } else {
                    Write-Host "  [X] Metasploit installation in WSL failed" -ForegroundColor Red
                    $failed += "metasploit (WSL failed)"
                }
            } else {
                Write-Host ""
                Write-Host "  [INFO] Skipping Metasploit installation" -ForegroundColor Yellow
                $failed += "metasploit (skipped - run install_metasploit_wsl.ps1 later)"
            }
        }
    } else {
        Write-Host ""
        Write-Host "  [INFO] Metasploit not installed. Options:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  Option 1 - Install via WSL (Recommended, no Admin required):" -ForegroundColor Cyan
        Write-Host "    - Run: wsl --install (requires Admin once)" -ForegroundColor White
        Write-Host "    - Then run: wsl sudo apt install metasploit-framework -y" -ForegroundColor White
        Write-Host ""
        Write-Host "  Option 2 - Install via Chocolatey (Requires Admin):" -ForegroundColor Cyan
        Write-Host "    - Run as Admin: choco install metasploit -y" -ForegroundColor White
        Write-Host ""
        Write-Host "  Option 3 - Download manually:" -ForegroundColor Cyan
        Write-Host "    - Visit: https://www.metasploit.com/download" -ForegroundColor White
        Write-Host ""
        
        $failed += "metasploit (manual - run install_metasploit_wsl.ps1)"
    }
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
Write-Host "  cd .." -ForegroundColor White
Write-Host "  python dsterminal.py" -ForegroundColor White

Write-Host ""
Write-Host "Note: If you installed Metasploit in WSL, restart PowerShell" -ForegroundColor Yellow
Write-Host "      to use the 'msfconsole' and 'msfvenom' commands." -ForegroundColor Yellow

Write-Host ""
pause