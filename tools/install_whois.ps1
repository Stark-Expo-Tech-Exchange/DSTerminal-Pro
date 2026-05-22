# Install WHOIS - User-level installation (no admin required)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Installing WHOIS Domain Lookup Tool" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if already installed
$whoisCheck = Get-Command whois -ErrorAction SilentlyContinue
if ($whoisCheck) {
    Write-Host "WHOIS is already installed" -ForegroundColor Green
    $whoisPath = (Get-Command whois).Source
    Write-Host "Location: $whoisPath" -ForegroundColor Cyan
    pause
    exit 0
}

Write-Host "NOTE: WHOIS installation may require Administrator privileges." -ForegroundColor Yellow
Write-Host ""

Write-Host "Options for WHOIS:" -ForegroundColor Cyan
Write-Host "  1. Skip WHOIS (DSTerminal works fine without it)" -ForegroundColor White
Write-Host "  2. Use online WHOIS via web browser" -ForegroundColor White
Write-Host "  3. Install manually (download and extract)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Choose option (1/2/3)"
Write-Host ""

if ($choice -eq "1") {
    Write-Host "Skipping WHOIS installation." -ForegroundColor Yellow
    Write-Host "You can use web-based WHOIS at: https://whois.domaintools.com" -ForegroundColor Cyan
    exit 0
} elseif ($choice -eq "2") {
    Write-Host "Opening online WHOIS service..." -ForegroundColor Cyan
    Start-Process "https://whois.domaintools.com"
    exit 0
} else {
    Write-Host "Manual installation instructions:" -ForegroundColor Green
    Write-Host ""
    Write-Host "1. Download WhoIs.zip from:" -ForegroundColor White
    Write-Host "   https://docs.microsoft.com/en-us/sysinternals/downloads/whois" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "2. Extract the zip file" -ForegroundColor White
    Write-Host ""
    Write-Host "3. Create a folder: %USERPROFILE%\tools\" -ForegroundColor White
    Write-Host "   mkdir %USERPROFILE%\tools" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "4. Copy whois.exe to that folder" -ForegroundColor White
    Write-Host ""
    Write-Host "5. Add to PATH (no admin required):" -ForegroundColor White
    Write-Host "   [Environment]::SetEnvironmentVariable('Path', " -ForegroundColor Cyan
    Write-Host "     '$env:Path;%USERPROFILE%\tools', 'User')" -ForegroundColor Cyan
    Write-Host ""
    
    $openBrowser = Read-Host "Open download page? (y/n)"
    if ($openBrowser -eq 'y') {
        Start-Process "https://docs.microsoft.com/en-us/sysinternals/downloads/whois"
    }
    exit 0
}