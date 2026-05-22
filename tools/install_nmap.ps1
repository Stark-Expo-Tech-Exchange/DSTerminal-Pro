# Nmap Installer
Write-Host "Installing Nmap..." -ForegroundColor Cyan
Write-Host ""

# Check if already installed
if (Get-Command nmap -ErrorAction SilentlyContinue) {
    Write-Host "Nmap is already installed" -ForegroundColor Green
    exit 0
}

# Install using Chocolatey
Write-Host "Installing Chocolatey and Nmap..." -ForegroundColor Yellow

# Create a temporary script file to avoid quote issues
$tempScript = [System.IO.Path]::GetTempFileName() + ".ps1"
$scriptContent = @'
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco install nmap -y --no-progress
'@

# Save and run the temporary script
$scriptContent | Out-File -FilePath $tempScript -Encoding ASCII
try {
    & powershell.exe -ExecutionPolicy Bypass -File $tempScript
    Write-Host "SUCCESS: Nmap installed successfully" -ForegroundColor Green
    exit 0
} catch {
    Write-Host "ERROR: Failed to install Nmap" -ForegroundColor Red
    Write-Host "Please install manually from: https://nmap.org/download.html" -ForegroundColor Yellow
    exit 1
} finally {
    Remove-Item $tempScript -ErrorAction SilentlyContinue
}