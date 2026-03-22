; DSTerminal Installer Script - Non-Admin Safe with Documentation & Auto-Update
; Version: 2.0.113
; Date: 2024

[Setup]
; Basic Setup Information
AppName=DSTerminal
AppVersion=2.0.113
AppVerName=DSTerminal v2.0.113
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
OutputBaseFilename=DSTerminal_Installer_v2.0.113
Compression=lzma2/ultra64
SolidCompression=yes
DisableWelcomePage=no
WizardStyle=modern
SetupIconFile=installer_assets\icon.ico
DisableProgramGroupPage=no
AllowNoIcons=yes
PrivilegesRequired=lowest
MinVersion=10.0.10240
UninstallDisplayIcon={app}\dsterminal.exe
UninstallDisplayName=DSTerminal v2.0.113
VersionInfoVersion=2.0.113
VersionInfoCompany=Stark Expo Tech Exchange
VersionInfoDescription=DSTerminal SOC Platform
VersionInfoTextVersion=2.0.113
VersionInfoCopyright=© 2024 Stark Expo Tech Exchange
VersionInfoProductName=DSTerminal
VersionInfoProductVersion=2.0.113

; Create uninstaller in registry
CreateUninstallRegKey=yes
UpdateUninstallLogAppName=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

; Include additional language files if needed
; Name: "french"; MessagesFile: "compiler:Languages\French.isl"

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

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Components: core; Flags: checkedonce
Name: "quicklaunchicon"; Description: "Create a &Quick Launch shortcut"; GroupDescription: "Additional icons:"; Components: core; Flags: unchecked
Name: "autoupdate"; Description: "Automatically check for updates on startup"; GroupDescription: "Update settings:"; Components: core; Flags: checkedonce
Name: "docshortcut"; Description: "Create Documentation shortcut on desktop"; GroupDescription: "Documentation:"; Components: docs; Flags: unchecked
Name: "startwithwindows"; Description: "Start DSTerminal with Windows (minimized)"; GroupDescription: "Startup options:"; Components: core; Flags: unchecked

[Files]
; ========== CORE APPLICATION ==========
; Main executable (ensure this file exists in dist folder)
Source: "dist\dsterminal_win-2.0.59_x64-amd64.exe"; DestDir: "{app}"; DestName: "dsterminal.exe"; Flags: ignoreversion; Components: core
Source: "dist\dsterminal_console.exe"; DestDir: "{app}"; DestName: "dsterminal-console.exe"; Flags: ignoreversion skipifsourcedoesntexist; Components: core

; Configuration files
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: core
Source: "config\settings.json"; DestDir: "{app}\config"; Flags: ignoreversion onlyifdoesntexist; Components: core
Source: "config\default.profile"; DestDir: "{app}\config"; Flags: ignoreversion; Components: core

; Python dependencies (if needed)
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
;Source: "templates\reports\*"; DestDir: "{app}\templates\reports"; Flags: ignoreversion recursesubdirs; Components: templates
;Source: "templates\scripts\*"; DestDir: "{app}\templates\scripts"; Flags: ignoreversion; Components: templates

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

; ========== WORKSPACE INITIALIZATION FILES ==========
;Source: "workspace_defaults\*"; DestDir: "{userappdata}\DSTerminal_Workspace"; Flags: ignoreversion recursesubdirs createallsubdirs onlyifdoesntexist; AfterInstall: InitializeWorkspace

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
Name: "{group}\DSTerminal SOC"; Filename: "{app}\dsterminal.exe"; WorkingDir: "{userappdata}\DSTerminal_Workspace"; IconFilename: "{app}\dsterminal.exe"; Comment: "Launch DSTerminal Security Operations Center"
Name: "{group}\Uninstall DSTerminal"; Filename: "{uninstallexe}"; Comment: "Remove DSTerminal from your system"
Name: "{group}\DSTerminal Documentation"; Filename: "{app}\docs\index.html"; IconFilename: "{app}\dsterminal.exe"; Components: docs

; Desktop icons
Name: "{userdesktop}\DSTerminal SOC"; Filename: "{app}\dsterminal.exe"; WorkingDir: "{userappdata}\DSTerminal_Workspace"; IconFilename: "{app}\dsterminal.exe"; Tasks: desktopicon; Comment: "DSTerminal Security Terminal"
Name: "{userdesktop}\DSTerminal Documentation"; Filename: "{app}\docs\index.html"; IconFilename: "{app}\dsterminal.exe"; Tasks: docshortcut; Components: docs

; Quick Launch (Windows 7/10)
;Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\DSTerminal.lnk"; Filename: "{app}\dsterminal.exe"; WorkingDir: "{userappdata}\DSTerminal_Workspace"; Tasks: quicklaunchicon

; Startup folder (optional)
;Name: "{userstartup}\DSTerminal.lnk"; Filename: "{app}\dsterminal.exe"; WorkingDir: "{userappdata}\DSTerminal_Workspace"; Tasks: startwithwindows; Parameters: "--minimized"

[Run]
; ========== POST-INSTALLATION ACTIONS ==========

; Launch documentation after install (if selected)
Filename: "{app}\docs\index.html"; Description: "View DSTerminal Documentation"; Flags: postinstall shellexec skipifsilent; Components: docs
Filename: "{cmd}"; Parameters: "/c setx PATH ""%PATH%;{app}"""; Flags: runhidden

; Launch DSTerminal after install
Filename: "{app}\dsterminal.exe"; Description: "Launch DSTerminal"; Flags: nowait postinstall skipifsilent; Components: core

; Register file associations (optional)
Filename: "{app}\tools\register-file-assoc.bat"; Parameters: "/S"; Flags: runhidden waituntilterminated skipifsilent; Check: FileExists(ExpandConstant('{app}\tools\register-file-assoc.bat'))

; Create update schedule task (if auto-update enabled)
Filename: "schtasks"; Parameters: "/create /tn ""DSTerminal Update Check"" /tr ""'{app}\update\update-checker.exe'"" /sc weekly /d SUN /st 09:00 /f"; Flags: runhidden waituntilterminated skipifsilent; Tasks: autoupdate; Check: IsAdminInstallMode

[UninstallRun]
; Clean up scheduled task
Filename: "schtasks"; Parameters: "/delete /tn ""DSTerminal Update Check"" /f"; Check: IsAdminInstallMode

; Clean up workspace (optional - user choice)
;Filename: "{cmd}"; Parameters: "/c rmdir /s /q ""{userappdata}\DSTerminal_Workspace"""; Flags: runhidden waituntilterminated; Check: RemoveWorkspaceCheck

[Code]
// Global variables
var
  RemoveWorkspacePage: TInputOptionWizardPage;
  UpdateChannelPage: TInputOptionWizardPage;
 
// ========== FFMPEG CHECK ==========
function IsFFmpegRequired: Boolean;
begin
  Result := 
    (FileExists(ExpandConstant('{sys}\ffmpeg.exe')) = False) and
    (FileExists(ExpandConstant('{app}\ffmpeg\ffmpeg.exe')) = False);
end;

// ========== WORKSPACE INITIALIZATION ==========
procedure InitializeWorkspace;
var
  WorkspacePath: string;
  ConfigFile: string;
begin
  WorkspacePath := ExpandConstant('{userappdata}\DSTerminal_Workspace');
  ConfigFile := WorkspacePath + '\config\workspace.json';
  
  // Create default config if it doesn't exist
  if not FileExists(ConfigFile) then
  begin
    SaveStringToFile(ConfigFile, 
      '{' + #13#10 +
      '  "version": "2.0.113",' + #13#10 +
      '  "created": "' + GetDateTimeString('yyyy-mm-dd hh:nn:ss', '-', ':') + '",' + #13#10 +
      '  "operator": "default",' + #13#10 +
      '  "settings": {' + #13#10 +
      '    "auto_update": true,' + #13#10 +
      '    "update_channel": "stable"' + #13#10 +
      '  }' + #13#10 +
      '}', False);
  end;
end;


// ========== HELPER FUNCTIONS ==========
function GetUninstallString: string;
var
  sUnInstPath: string;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{#emit SetupSetting("AppName")}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

// ========== CHECK FOR ADMIN RIGHTS (FOR TASKS THAT NEED IT) ==========
function IsAdminInstallMode: Boolean;
begin
  Result := IsAdminLoggedOn or IsPowerUserLoggedOn;
end;

[Registry]
; Add DSTerminal to user PATH (no admin required)
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "PATH"; \
ValueData: "{olddata};{app}"; Flags: preservestringtype

[Messages]
BeveledLabel=DSTerminal SOC Platform v2.0.113

[CustomMessages]
SetupAppTitle=DSTerminal Installer
SetupWindowTitle=DSTerminal v2.0.113 Setup