# install_sqlmap.ps1 - Updated for virtual environments
Write-Host "Installing SQLMap..." -ForegroundColor Cyan

# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Find Python
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
}

if (-not $pythonCmd) {
    Write-Host "Python not found!" -ForegroundColor Red
    exit 1
}

Write-Host "Using Python: $pythonCmd" -ForegroundColor Green

# Check if in virtual environment
$inVenv = ($pythonCmd -eq "python" -and (Get-Command python).Source -like "*venv*")
if ($inVenv) {
    Write-Host "Detected virtual environment. Installing without --user flag..." -ForegroundColor Yellow
    & $pythonCmd -m pip install sqlmap
} else {
    Write-Host "Installing SQLMap via pip..." -ForegroundColor Yellow
    & $pythonCmd -m pip install sqlmap --user
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "SQLMap installed successfully!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "SQLMap installation failed!" -ForegroundColor Red
    exit 1
}