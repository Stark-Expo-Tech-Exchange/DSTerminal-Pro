# Install SQLMap via pip (No admin required)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Installing SQLMap" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if already installed
if (Get-Command sqlmap -ErrorAction SilentlyContinue) {
    $sqlmapVersion = & sqlmap --version 2>$null | Select-Object -First 1
    Write-Host "SQLMap is already installed" -ForegroundColor Green
    Write-Host "Version: $sqlmapVersion" -ForegroundColor Cyan
    pause
    exit 0
}

# Check if Python is available
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-Host "ERROR: Python is not installed" -ForegroundColor Red
    Write-Host "Please install Python first (Microsoft Store or python.org)" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Using Python: $pythonCmd" -ForegroundColor Cyan
Write-Host ""

# Install SQLMap via pip (user install to avoid admin)
Write-Host "Installing SQLMap via pip..." -ForegroundColor Yellow

try {
    # Upgrade pip (user level)
    Write-Host "Upgrading pip..." -ForegroundColor Cyan
    & $pythonCmd -m pip install --upgrade pip --user --quiet
    
    # Install SQLMap (user level)
    Write-Host "Installing SQLMap..." -ForegroundColor Cyan
    & $pythonCmd -m pip install sqlmap --user
    
    if ($LASTEXITCODE -eq 0) {
        # Add user site-packages to PATH if needed
        $userSite = & $pythonCmd -c "import site; print(site.USER_BASE)" 2>$null
        if ($userSite) {
            $userBin = Join-Path $userSite "Scripts"
            if (Test-Path $userBin) {
                $env:Path = "$userBin;$env:Path"
                [System.Environment]::SetEnvironmentVariable("Path", "$userBin;$([System.Environment]::GetEnvironmentVariable('Path', 'User'))", "User")
            }
        }
        
        # Verify installation
        $sqlmapVersion = & sqlmap --version 2>$null | Select-Object -First 1
        Write-Host ""
        Write-Host "SUCCESS: SQLMap installed successfully!" -ForegroundColor Green
        Write-Host "Version: $sqlmapVersion" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Test with: sqlmap --version" -ForegroundColor Yellow
    } else {
        Write-Host ""
        Write-Host "ERROR: Failed to install SQLMap via pip" -ForegroundColor Red
        Write-Host ""
        Write-Host "Try installing manually:" -ForegroundColor Yellow
        Write-Host "  $pythonCmd -m pip install sqlmap --user" -ForegroundColor White
        exit 1
    }
} catch {
    Write-Host ""
    Write-Host "ERROR: Failed to install SQLMap" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
pause