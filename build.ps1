# build.ps1
param(
    [switch]$Clean,
    [switch]$BuildPy,
    [switch]$BuildInstaller
)

$ErrorActionPreference = "Stop"

Write-Host "DSTerminal Build Script" -ForegroundColor Cyan
Write-Host "=======================" -ForegroundColor Cyan

# Clean build artifacts
if ($Clean) {
    Write-Host "Cleaning build artifacts..." -ForegroundColor Yellow
    if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" -ErrorAction SilentlyContinue }
    if (Test-Path "build") { Remove-Item -Recurse -Force "build" -ErrorAction SilentlyContinue }
    if (Test-Path "*.exe") { Remove-Item -Force "*.exe" -ErrorAction SilentlyContinue }
    Write-Host "Clean complete!" -ForegroundColor Green
}

# Build Python executable
if ($BuildPy) {
    Write-Host "Building Python executable..." -ForegroundColor Yellow

    # Check if PyInstaller is installed
    $pyinstaller = Get-Command "pyinstaller" -ErrorAction SilentlyContinue
    if (-not $pyinstaller) {
        Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
        pip install pyinstaller
    }

    # Ensure required directories exist
    if (-not (Test-Path "installer_assets")) { New-Item -ItemType Directory -Path "installer_assets" -Force }
    if (-not (Test-Path "docs")) { New-Item -ItemType Directory -Path "docs" -Force }
    if (-not (Test-Path "templates")) { New-Item -ItemType Directory -Path "templates" -Force }

    # Build with PyInstaller
    pyinstaller --onefile --name "dsterminal_win-2.0.59_x64-amd64" `
        --add-data "docs;docs" `
        --add-data "templates;templates" `
        --icon "installer_assets\icon.ico" `
        --version-file "version_info.txt" `
        --noconfirm `
        dsterminal.py

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Executable built successfully!" -ForegroundColor Green
        Write-Host "Location: dist\dsterminal_win-2.0.59_x64-amd64.exe" -ForegroundColor Green
    } else {
        Write-Host "Failed to build executable!" -ForegroundColor Red
        exit 1
    }
}

# Build Inno Setup installer
if ($BuildInstaller) {
    Write-Host "Building Inno Setup installer..." -ForegroundColor Yellow

    # Check if ISCC is in PATH
    $iscc = Get-Command "iscc" -ErrorAction SilentlyContinue
    if (-not $iscc) {
        # Try common installation paths
        $paths = @(
            "${env:ProgramFiles}\Inno Setup 6\ISCC.exe",
            "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
            "${env:ProgramFiles}\Inno Setup 5\ISCC.exe",
            "${env:ProgramFiles(x86)}\Inno Setup 5\ISCC.exe"
        )

        foreach ($path in $paths) {
            if (Test-Path $path) {
                $iscc = $path
                break
            }
        }
    }

    if (-not $iscc) {
        Write-Host "Inno Setup Compiler (ISCC.exe) not found!" -ForegroundColor Red
        Write-Host "Please install Inno Setup from: https://jrsoftware.org/isdl.php" -ForegroundColor Yellow
        exit 1
    }

    # Check if installer script exists
    if (-not (Test-Path "dsterminal_installer.iss")) {
        Write-Host "Installer script dsterminal_installer.iss not found!" -ForegroundColor Red
        exit 1
    }

    # Run ISCC
    Write-Host "Compiling installer with: $iscc" -ForegroundColor Gray
    if ($iscc -is [string]) {
        & $iscc "dsterminal_installer.iss"
    } else {
        & iscc "dsterminal_installer.iss"
    }

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Installer built successfully!" -ForegroundColor Green
        # Find the generated installer
        $installer = Get-ChildItem -Path . -Filter "DSTerminal_Setup_*.exe" | Select-Object -First 1
        if ($installer) {
            Write-Host "Location: $($installer.FullName)" -ForegroundColor Green
        }
    } else {
        Write-Host "Failed to build installer!" -ForegroundColor Red
        exit 1
    }
}

if (-not $BuildPy -and -not $BuildInstaller -and -not $Clean) {
    Write-Host "`nNo build actions specified. Available options:" -ForegroundColor Yellow
    Write-Host "  .\build.ps1 -Clean         # Clean build artifacts" -ForegroundColor White
    Write-Host "  .\build.ps1 -BuildPy       # Build Python executable" -ForegroundColor White
    Write-Host "  .\build.ps1 -BuildInstaller # Build Inno Setup installer" -ForegroundColor White
    Write-Host "  .\build.ps1 -Clean -BuildPy -BuildInstaller # Do everything" -ForegroundColor White
}

Write-Host "`nBuild complete!" -ForegroundColor Green