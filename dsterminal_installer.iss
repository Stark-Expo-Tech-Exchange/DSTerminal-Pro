; DSTerminal Installer Script - Non-Admin Safe with Documentation & Auto-Update
; Version: 2.1.327
; Date: 2026

[Setup]
; Basic Setup Information
AppId={{1EFF5130-85AF-4EE9-B818-5634A06408D2}}
AppName=DSTerminal
AppVersion=2.1.327
AppVerName=DSTerminal v2.1.327
AppPublisher=Stark Expo Tech Exchange
AppPublisherURL=https://starkexpotechexchange-mw.com
AppSupportURL=https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/issues
AppUpdatesURL=https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/releases
AppContact=support@starkexpotechexchange-mw.com
AppComments=Security Operations Center Terminal
AppCopyright=Copyright © 2024 Stark Expo Tech Exchange

; Installation Paths (User AppData - No Admin Required)
DefaultDirName={userappdata}\DSTerminal
DefaultGroupName=DSTerminal
LicenseFile=license.txt
OutputDir=installer_output
OutputBaseFilename=DSTerminal_Installer_2026_v2.1.327
Compression=lzma2/ultra64
SolidCompression=yes
DisableWelcomePage=no
WizardStyle=modern
SetupIconFile=installer_assets\3486-removebg-preview.ico

WizardImageFile=installer_assets\wizard-image.bmp
WizardSmallImageFile=installer_assets\wizard-small.bmp
WizardImageStretch=No
WizardImageBackColor=clBlack

DisableProgramGroupPage=no
AllowNoIcons=yes
PrivilegesRequired=lowest
MinVersion=10.0
UninstallDisplayIcon={app}\dsterminal.exe
UninstallDisplayName=DSTerminal v2.1.327
VersionInfoVersion=2.1.327
VersionInfoCompany=Stark Expo Tech Exchange
VersionInfoDescription=DSTerminal Cyber-Ops Platform
VersionInfoTextVersion=2.1.327
VersionInfoCopyright=© 2024 Stark Expo Tech Exchange
VersionInfoProductName=DSTerminal
VersionInfoProductVersion=2.1.327

; Create uninstaller in registry
CreateUninstallRegKey=yes
UpdateUninstallLogAppName=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Types]
Name: "full"; Description: "Full Installation (Recommended)"
Name: "compact"; Description: "Compact Installation"
Name: "custom"; Description: "Custom Installation"; Flags: iscustom

[Components]
Name: "core"; Description: "Core DSTerminal Files"; Types: full compact custom; Flags: fixed
Name: "docs"; Description: "Documentation & Help Files"; Types: full custom
Name: "tools"; Description: "Additional Security Tools"; Types: full custom
Name: "templates"; Description: "Report Templates"; Types: full custom
Name: "ffmpeg"; Description: "FFmpeg (Video Analysis)"; Types: full custom
Name: "updatehelper"; Description: "Auto-Update Helper Script"; Types: full custom
; ===== Dependency Components =====
Name: "dependencies"; Description: "Install Required Dependencies (Nmap, Python packages)"; Types: full custom
Name: "dependencies\nmap"; Description: "Nmap Network Scanner"; Types: full
Name: "dependencies\sqlmap"; Description: "SQLMap (SQL Injection Tool)"; Types: full
Name: "dependencies\whois"; Description: "WHOIS Domain Lookup"; Types: full
Name: "dependencies\python"; Description: "Python 3.11+ (Required for SOC features)"; Types: full
Name: "dependencies\packages"; Description: "Python Packages (colorama, requests, folium, plotly, reportlab)"; Types: full

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Components: core; Flags: checkedonce
Name: "quicklaunchicon"; Description: "Create a &Quick Launch shortcut"; GroupDescription: "Additional icons:"; Components: core; Flags: unchecked
Name: "autoupdate"; Description: "Automatically check for updates on startup"; GroupDescription: "Update settings:"; Components: core; Flags: checkedonce
Name: "docshortcut"; Description: "Create Documentation shortcut on desktop"; GroupDescription: "Documentation:"; Components: docs; Flags: unchecked
Name: "startwithwindows"; Description: "Start DSTerminal with Windows (minimized)"; GroupDescription: "Startup options:"; Components: core; Flags: unchecked
; ===== Dependency installation tasks =====
Name: "installdeps"; Description: "Install/Update missing dependencies on completion"; GroupDescription: "Dependency management:"; Components: dependencies; Flags: checkedonce

[Files]
; ========== CORE APPLICATION ==========
Source: "dist\dsterminal_win-2026_v2.1.327_x64-amd64.exe"; DestDir: "{app}"; DestName: "dsterminal.exe"; Flags: ignoreversion; Components: core
Source: "dist\dsterminal_console.exe"; DestDir: "{app}"; DestName: "dsterminal-console.exe"; Flags: ignoreversion skipifsourcedoesntexist; Components: core
Source: "./dsterminal.bat"; DestDir: "{app}"; Flags: ignoreversion

; Configuration files
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: core
Source: "config\settings.json"; DestDir: "{app}\config"; Flags: ignoreversion onlyifdoesntexist; Components: core
Source: "config\default.profile"; DestDir: "{app}\config"; Flags: ignoreversion; Components: core
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion; Components: core

; ========== DOCUMENTATION ==========
Source: "docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: docs
Source: "docs\index.html"; DestDir: "{app}\docs"; Flags: ignoreversion; Components: docs
Source: "docs\user_guide.pdf"; DestDir: "{app}\docs"; Flags: ignoreversion skipifsourcedoesntexist; Components: docs
Source: "docs\api_reference.md"; DestDir: "{app}\docs"; Flags: ignoreversion skipifsourcedoesntexist; Components: docs
Source: "docs\quickstart.txt"; DestDir: "{app}"; DestName: "QUICKSTART.txt"; Flags: ignoreversion; Components: docs

; ========== TOOLS & UTILITIES ==========
Source: "tools\*"; DestDir: "{app}\tools"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: tools
Source: "tools\update-helper.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: updatehelper
Source: "tools\cleanup.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion skipifsourcedoesntexist; Components: tools
Source: "tools\diagnostic.bat"; DestDir: "{app}\tools"; Flags: ignoreversion skipifsourcedoesntexist; Components: tools

; ========== TEMPLATES ==========
Source: "templates\*"; DestDir: "{app}\templates"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: templates

; ========== FFMPEG (Conditional) ==========
Source: "redist\ffmpeg\*"; DestDir: "{app}\ffmpeg"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: ffmpeg; Check: IsFFmpegRequired

; ========== LEGAL & README ==========
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion; Components: core
Source: "README.txt"; DestDir: "{app}"; Flags: ignoreversion; Components: core
Source: "CHANGELOG.txt"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist; Components: core
Source: "CREDITS.txt"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist; Components: core

; ========== UPDATE MECHANISM ==========
Source: "update\update-checker.exe"; DestDir: "{app}\update"; Flags: ignoreversion skipifsourcedoesntexist; Components: core
Source: "update\version.json"; DestDir: "{app}\update"; Flags: ignoreversion; Components: core
Source: "update\updater.ps1"; DestDir: "{app}\update"; Flags: ignoreversion; Components: updatehelper

; ========== DEPENDENCY INSTALLATION SCRIPTS ==========
Source: "tools\check_dependencies.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: dependencies
Source: "tools\install_all_dependencies.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: dependencies
Source: "tools\install_chocolatey.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: dependencies
Source: "tools\install_remaining_deps.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: dependencies
Source: "tools\install_metasploit.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: dependencies
Source: "tools\install_nmap_admin.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: dependencies
Source: "tools\install_nmap.bat"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: dependencies
Source: "tools\install_whois.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: dependencies
Source: "tools\install_sqlmap.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: dependencies\sqlmap
Source: "tools\install_python_packages.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: dependencies\packages
Source: "tools\install_python.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: dependencies
Source: "tools\install_remaining_deps.bat"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: dependencies
Source: "tools\check_deps.bat"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: dependencies
Source: "tools\install_nmap.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion; Components: dependencies\nmap

[Dirs]
; Create workspace directories
Name: "{userappdata}\DSTerminal_Workspace"; Flags: uninsalwaysuninstall
Name: "{userappdata}\DSTerminal_Workspace\operators"
Name: "{userappdata}\DSTerminal_Workspace\scans"
Name: "{userappdata}\DSTerminal_Workspace\reports"
Name: "{userappdata}\DSTerminal_Workspace\exploits"
Name: "{userappdata}\DSTerminal_Workspace\sandbox"
Name: "{userappdata}\DSTerminal_Workspace\quarantine"
Name: "{userappdata}\DSTerminal_Workspace\logs"
Name: "{userappdata}\DSTerminal_Workspace\config"

; Application directories
Name: "{app}\logs"; Flags: uninsalwaysuninstall
Name: "{app}\updates"; Flags: uninsalwaysuninstall
Name: "{app}\cache"; Flags: uninsalwaysuninstall
Name: "{app}\temp"; Flags: uninsalwaysuninstall

[Icons]
; Main application icons
Name: "{group}\DSTerminal SOC"; Filename: "{app}\dsterminal.exe"; WorkingDir: "{userappdata}\DSTerminal_Workspace"; IconFilename: "{app}\dsterminal.exe"; Comment: "Launch DSTerminal Cyber Ops Platform"
Name: "{group}\Uninstall DSTerminal"; Filename: "{uninstallexe}"; Comment: "Remove DSTerminal from your system"
Name: "{group}\DSTerminal Documentation"; Filename: "{app}\docs\index.html"; IconFilename: "{app}\dsterminal.exe"; Components: docs
Name: "{userdesktop}\DSTerminal SOC"; Filename: "{app}\dsterminal.exe"; WorkingDir: "{userappdata}\DSTerminal_Workspace"; IconFilename: "{app}\dsterminal.exe"; Tasks: desktopicon; Comment: "DSTerminal Security Terminal"; Parameters: "/MAX"
Name: "{userdesktop}\DSTerminal Documentation"; Filename: "{app}\docs\index.html"; IconFilename: "{app}\dsterminal.exe"; Tasks: docshortcut; Components: docs

[Run]
; Launch documentation after install (if selected)
Filename: "{app}\docs\index.html"; Description: "View DSTerminal Documentation"; Flags: postinstall shellexec skipifsilent; Components: docs

; Add to PATH
Filename: "{cmd}"; Parameters: "/c setx PATH ""%PATH%;{app}"""; Flags: runhidden

; Check and install dependencies (REMOVED THE SEMICOLON)
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\tools\check_dependencies.ps1"""; Flags: runhidden waituntilterminated; Components: dependencies; Tasks: installdeps

; Install Nmap if missing (REMOVED THE SEMICOLON)
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\tools\install_nmap.ps1"""; Flags: runhidden waituntilterminated; Components: dependencies\nmap; Tasks: installdeps; Check: IsNmapMissing

; Launch post-install script after installer closes
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -WindowStyle Hidden -File ""{app}\tools\post_install.ps1"""; Flags: nowait skipifsilent

; Install Python packages if missing (This one is already uncommented - good!)
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\tools\install_python_packages.ps1"""; Flags: runhidden waituntilterminated; Components: dependencies\packages; Tasks: installdeps; Check: ArePythonPackagesMissing

; Launch DSTerminal after install
Filename: "{app}\dsterminal.exe"; Description: "Launch DSTerminal"; Flags: nowait postinstall skipifsilent; Components: core

; Create update schedule task (if auto-update enabled)
Filename: "schtasks"; Parameters: "/create /tn ""DSTerminal Update Check"" /tr ""'{app}\update\update-checker.exe'"" /sc weekly /d SUN /st 09:00 /f"; Flags: runhidden waituntilterminated skipifsilent; Tasks: autoupdate; Check: IsAdminInstallMode

[UninstallRun]
; Clean up scheduled task
Filename: "schtasks"; Parameters: "/delete /tn ""DSTerminal Update Check"" /f"; Check: IsAdminInstallMode; RunOnceId: "RemoveScheduledTask"

[Code]
// Global variables
var
  // RemoveWorkspacePage: TInputOptionWizardPage;
  // helperUpdateChannelPage: TInputOptionWizardPage;
  DependencyCheckPage: TInputOptionWizardPage;

// ========== FFMPEG CHECK ==========
function IsFFmpegRequired: Boolean;
begin
  Result := (FileExists(ExpandConstant('{sys}\ffmpeg.exe')) = False) and
            (FileExists(ExpandConstant('{app}\ffmpeg\ffmpeg.exe')) = False);
end;

// ========== METASPLOIT CHECK ==========
function IsMetasploitMissing: Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  if Exec(ExpandConstant('{cmd}'), '/c msfconsole --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    if ResultCode = 0 then
      Result := False;
  end;
end;

// ========== NMAP CHECK ==========
function IsNmapMissing: Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  if Exec(ExpandConstant('{cmd}'), '/c nmap --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    if ResultCode = 0 then
      Result := False;
  end;
end;

// ========== SQLMAP CHECK ==========
function IsSQLMapMissing: Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  if Exec(ExpandConstant('{cmd}'), '/c sqlmap --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    if ResultCode = 0 then
      Result := False;
  end;
end;

// ========== PYTHON PACKAGES CHECK ==========
function ArePythonPackagesMissing: Boolean;
var
  ResultCode: Integer;
  TempFile: string;
begin
  Result := True;
  TempFile := ExpandConstant('{tmp}\check_packages.vbs');
  
  SaveStringToFile(TempFile, 
    'Set objShell = CreateObject("WScript.Shell")' + #13#10 +
    'packages = Array("colorama", "requests", "folium", "plotly", "reportlab")' + #13#10 +
    'missing = 0' + #13#10 +
    'For Each pkg In packages' + #13#10 +
    '    Set objExec = objShell.Exec("python -c ""import " & pkg & """")' + #13#10 +
    '    Do While objExec.Status = 0' + #13#10 +
    '        WScript.Sleep 100' + #13#10 +
    '    Loop' + #13#10 +
    '    If objExec.ExitCode <> 0 Then missing = missing + 1' + #13#10 +
    'Next' + #13#10 +
    'If missing > 0 Then WScript.Quit 1 Else WScript.Quit 0', False);
  
  if Exec(ExpandConstant('{cmd}'), '/c cscript //nologo "' + TempFile + '"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    if ResultCode = 0 then
      Result := False;
  end;
  
  DeleteFile(TempFile);
end;

// ========== WORKSPACE INITIALIZATION ==========
procedure InitializeWorkspace;
var
  WorkspacePath: string;
  ConfigFile: string;
begin
  WorkspacePath := ExpandConstant('{userappdata}\DSTerminal_Workspace');
  ConfigFile := WorkspacePath + '\config\workspace.json';
  
  if not FileExists(ConfigFile) then
  begin
    SaveStringToFile(ConfigFile, 
      '{' + #13#10 +
      '  "version": "2.1.327",' + #13#10 +
      '  "created": "' + GetDateTimeString('yyyy-mm-dd hh:nn:ss', '-', ':') + '",' + #13#10 +
      '  "operator": "default",' + #13#10 +
      '  "settings": {' + #13#10 +
      '    "auto_update": true,' + #13#10 +
      '    "update_channel": "stable"' + #13#10 +
      '  }' + #13#10 +
      '}', False);
  end;
end;

// ========== CUSTOM WIZARD PAGE FOR DEPENDENCIES =====
procedure InitializeWizard;
begin
  DependencyCheckPage := CreateInputOptionPage(wpSelectTasks,
    'Dependency Installation', 'Install required dependencies',
    'DSTerminal requires certain dependencies for full functionality.' + #13#10#13#10 +
    'Select your preferred installation method:' + #13#10#13#10 +
    'Note: You can skip this and install dependencies manually later.',
    True, False);
    
  DependencyCheckPage.Add('Automatically install all missing dependencies (Recommended)');
  DependencyCheckPage.Add('Only check for missing dependencies (Show report)');
  DependencyCheckPage.Add('Skip dependency installation (I will install manually)');
  DependencyCheckPage.Values[0] := True;
end;

// ========== HELPER FUNCTIONS ==========
function IsAdminInstallMode: Boolean;
begin
  Result := IsAdmin or IsPowerUserLoggedOn;
end;

function RemoveWorkspaceCheck: Boolean;
begin
  Result := False;
end;

// ========== DEPENDENCY HANDLING =====
procedure CurStepChanged(CurStep: TSetupStep);
var
  DependencyChoice: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    DependencyChoice := DependencyCheckPage.SelectedValueIndex;
    
    if DependencyChoice = 0 then
    begin
      MsgBox('DSTerminal will now check and install missing dependencies. This may take a few minutes.', mbInformation, MB_OK);
    end
    else if DependencyChoice = 1 then
    begin
      MsgBox('DSTerminal will check for missing dependencies and show a report.', mbInformation, MB_OK);
    end
    else
    begin
      MsgBox('Dependency installation skipped. You can install them manually later.' + #13#10#13#10 +
             'Required: nmap, sqlmap' + #13#10 +
             'Optional: whois, Metasploit, Python packages', mbInformation, MB_OK);
    end;
  end;
end;

[Registry]
; Add DSTerminal to user PATH (no admin required)
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "PATH"; \
ValueData: "{olddata};{app}"; Flags: preservestringtype

[Messages]
BeveledLabel=DSTerminal Cyber-Ops Platform v2.1.327

[CustomMessages]
SetupAppTitle=DSTerminal Installer
SetupWindowTitle=DSTerminal v2.1.327 Setup