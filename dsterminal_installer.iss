; DSTerminal Debian Package Specification
; Version: 2.0.113
; Target: Debian/Ubuntu/Parrot OS (amd64/arm64)
; ============================================================

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

; Linux/DEB specific settings
DefaultDirName=/usr/share/dsterminal
DefaultGroupName=DSTerminal
LicenseFile=license.txt
OutputDir=deb_output
OutputBaseFilename=dsterminal_2025-v2.0.113_-_x64amd64
Compression=gzip
SolidCompression=yes
DisableWelcomePage=no
WizardStyle=modern
UninstallDisplayName=DSTerminal v2.0.113
VersionInfoVersion=2.0.113
VersionInfoCompany=Stark Expo Tech Exchange
VersionInfoDescription=DSTerminal SOC Platform for Linux
VersionInfoTextVersion=2.0.113
VersionInfoCopyright=© 2024 Stark Expo Tech Exchange
VersionInfoProductName=DSTerminal
VersionInfoProductVersion=2.0.113

; Linux specific: Use system-wide installation with proper permissions
PrivilegesRequired=admin
; Disable Windows-specific features
DisableProgramGroupPage=yes
DisableDirPage=no
DisableReadyPage=no
AllowNoIcons=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Types]
Name: "full"; Description: "Full Installation (Recommended)"
Name: "standard"; Description: "Standard Installation"
Name: "minimal"; Description: "Minimal Installation (CLI only)"
Name: "custom"; Description: "Custom Installation"; Flags: iscustom

[Components]
Name: "core"; Description: "Core DSTerminal Files"; Types: full standard minimal custom; Flags: fixed
Name: "gui"; Description: "GUI Components (GTK/Qt)"; Types: full standard; Check: IsDesktopEnvironment
Name: "docs"; Description: "Documentation & Help Files"; Types: full custom
Name: "tools"; Description: "Additional Security Tools"; Types: full custom
Name: "templates"; Description: "Report Templates"; Types: full custom
Name: "bash_completion"; Description: "Bash Completion Script"; Types: full standard custom
Name: "desktop_entry"; Description: "Desktop Entry (.desktop)"; Types: full standard custom; Check: IsDesktopEnvironment

[Tasks]
Name: "desktopicon"; Description: "Create desktop shortcut"; GroupDescription: "Additional icons:"; Components: core; Flags: checkedonce; Check: IsDesktopEnvironment
Name: "autoupdate"; Description: "Check for updates automatically (weekly)"; GroupDescription: "Update settings:"; Components: core; Flags: checkedonce
Name: "systemd_service"; Description: "Install systemd service (background monitoring)"; GroupDescription: "Service options:"; Components: core; Flags: unchecked; Check: IsSystemD
Name: "manpage"; Description: "Install man page documentation"; GroupDescription: "Documentation:"; Components: docs; Flags: checkedonce

[Files]
; ========== CORE APPLICATION ==========
; Main executable (Linux binary)
Source: "dist/dsterminal_linux_amd64"; DestDir: "{app}/bin"; DestName: "dsterminal"; Flags: ignoreversion; Components: core; Permissions: 755
Source: "dist/dsterminal_linux_arm64"; DestDir: "{app}/bin"; DestName: "dsterminal-arm64"; Flags: ignoreversion skipifsourcedoesntexist; Components: core; Permissions: 755

; Python modules and data files
Source: "integrity_monitor.py"; DestDir: "{app}/lib"; Flags: ignoreversion; Components: core
Source: "crypto_engine.py"; DestDir: "{app}/lib"; Flags: ignoreversion; Components: core
Source: "edu_typing_engine.py"; DestDir: "{app}/lib"; Flags: ignoreversion; Components: core
Source: "recon.py"; DestDir: "{app}/lib"; Flags: ignoreversion; Components: core
Source: "recon_full.py"; DestDir: "{app}/lib"; Flags: ignoreversion; Components: core
Source: "VERSION"; DestDir: "{app}"; Flags: ignoreversion; Components: core

; Configuration templates
Source: "config/*"; DestDir: "{app}/config"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: core

; ========== GUI COMPONENTS (Optional) ==========
Source: "gui/dsterminal-gtk"; DestDir: "{app}/bin"; DestName: "dsterminal-gtk"; Flags: ignoreversion; Components: gui; Permissions: 755
Source: "gui/dsterminal-qt"; DestDir: "{app}/bin"; DestName: "dsterminal-qt"; Flags: ignoreversion; Components: gui; Permissions: 755
Source: "gui/assets/*"; DestDir: "{app}/share/gui"; Flags: ignoreversion recursesubdirs; Components: gui

; ========== DOCUMENTATION ==========
Source: "docs/*"; DestDir: "{app}/share/doc/dsterminal"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: docs
Source: "docs/man/dsterminal.1"; DestDir: "{app}/share/man/man1"; Flags: ignoreversion; Components: docs; Tasks: manpage
Source: "README.md"; DestDir: "{app}/share/doc/dsterminal"; DestName: "README"; Flags: ignoreversion; Components: docs
Source: "CHANGELOG.md"; DestDir: "{app}/share/doc/dsterminal"; DestName: "changelog"; Flags: ignoreversion; Components: docs
Source: "LICENSE"; DestDir: "{app}/share/doc/dsterminal"; DestName: "copyright"; Flags: ignoreversion; Components: docs

; ========== TOOLS & UTILITIES ==========
Source: "tools/*"; DestDir: "{app}/share/tools"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: tools; Permissions: 755
Source: "scripts/update-helper.sh"; DestDir: "{app}/bin"; DestName: "dsterminal-update"; Flags: ignoreversion; Components: core; Permissions: 755
Source: "scripts/diagnostic.sh"; DestDir: "{app}/bin"; DestName: "dsterminal-diagnostic"; Flags: ignoreversion; Components: tools; Permissions: 755

; ========== TEMPLATES ==========
Source: "templates/*"; DestDir: "{app}/share/templates"; Flags: ignoreversion recursesubdirs createallsubdirs; Components: templates

; ========== BASH COMPLETION ==========
Source: "completion/dsterminal-completion.bash"; DestDir: "{app}/share/bash-completion/completions"; DestName: "dsterminal"; Flags: ignoreversion; Components: bash_completion

; ========== DESKTOP ENTRY ==========
Source: "desktop/dsterminal.desktop"; DestDir: "{app}/share/applications"; Flags: ignoreversion; Components: desktop_entry

; ========== SYSTEMD SERVICE ==========
Source: "systemd/dsterminal-monitor.service"; DestDir: "{app}/lib/systemd/system"; Flags: ignoreversion; Components: core; Tasks: systemd_service

; ========== ICON ==========
Source: "icons/dsterminal.svg"; DestDir: "{app}/share/icons/hicolor/scalable/apps"; Flags: ignoreversion; Components: core
Source: "icons/dsterminal-128.png"; DestDir: "{app}/share/icons/hicolor/128x128/apps"; DestName: "dsterminal.png"; Flags: ignoreversion; Components: core
Source: "icons/dsterminal-64.png"; DestDir: "{app}/share/icons/hicolor/64x64/apps"; DestName: "dsterminal.png"; Flags: ignoreversion; Components: core
Source: "icons/dsterminal-32.png"; DestDir: "{app}/share/icons/hicolor/32x32/apps"; DestName: "dsterminal.png"; Flags: ignoreversion; Components: core

[Dirs]
; Create necessary directories
Name: "{app}/bin"; Permissions: 755
Name: "{app}/lib"; Permissions: 755
Name: "{app}/config"; Permissions: 755
Name: "{app}/logs"; Permissions: 755
Name: "{app}/cache"; Permissions: 755
Name: "{app}/updates"; Permissions: 755
Name: "{userappdata}/DSTerminal_Workspace"; Permissions: 755
Name: "{userappdata}/DSTerminal_Workspace/operators"
Name: "{userappdata}/DSTerminal_Workspace/scans"
Name: "{userappdata}/DSTerminal_Workspace/reports"
Name: "{userappdata}/DSTerminal_Workspace/exploits"
Name: "{userappdata}/DSTerminal_Workspace/sandbox"
Name: "{userappdata}/DSTerminal_Workspace/quarantine"
Name: "{userappdata}/DSTerminal_Workspace/logs"

[Icons]
; Desktop icons
Name: "{userdesktop}/DSTerminal"; Filename: "/usr/bin/dsterminal"; WorkingDir: "{userappdata}/DSTerminal_Workspace"; IconFilename: "{app}/share/icons/hicolor/128x128/apps/dsterminal.png"; Comment: "DSTerminal Security Terminal"; Tasks: desktopicon
Name: "{group}/DSTerminal"; Filename: "/usr/bin/dsterminal"; WorkingDir: "{userappdata}/DSTerminal_Workspace"; IconFilename: "{app}/share/icons/hicolor/128x128/apps/dsterminal.png"; Comment: "Launch DSTerminal"
Name: "{group}/DSTerminal Documentation"; Filename: "{app}/share/doc/dsterminal/README"; IconFilename: "text"; Components: docs

[Run]
; ========== POST-INSTALLATION ACTIONS ==========
; Update icon cache
Filename: "update-icon-caches"; Parameters: "{app}/share/icons/hicolor"; Flags: runhidden waituntilterminated skipifsilent; Check: FileExists('/usr/bin/update-icon-caches')
; Update desktop database
Filename: "update-desktop-database"; Parameters: "{app}/share/applications"; Flags: runhidden waituntilterminated skipifsilent; Check: FileExists('/usr/bin/update-desktop-database')
; Update man database
Filename: "mandb"; Parameters: "--quiet"; Flags: runhidden waituntilterminated skipifsilent; Tasks: manpage; Check: FileExists('/usr/bin/mandb')

[UninstallRun]
; Remove symlink from /usr/local/bin
Filename: "/bin/rm"; Parameters: "-f /usr/local/bin/dsterminal"; Flags: runhidden waituntilterminated
; Remove systemd service if installed
Filename: "/bin/systemctl"; Parameters: "disable --now dsterminal-monitor.service"; Flags: runhidden waituntilterminated; Tasks: systemd_service
; Remove systemd service file
Filename: "/bin/rm"; Parameters: "-f /etc/systemd/system/dsterminal-monitor.service"; Flags: runhidden waituntilterminated; Tasks: systemd_service

[Code]
// Global variables
var
  RemoveWorkspacePage: TInputOptionWizardPage;
  UpdateChannelPage: TInputOptionWizardPage;

// ========== SYSTEM CHECKS ==========
function IsDesktopEnvironment: Boolean;
begin
  // Check if running in GUI environment
  Result := (GetEnv('DISPLAY') <> '') or (FileExists('/usr/bin/startx'));
end;

function IsSystemD: Boolean;
begin
  // Check if systemd is running
  Result := FileExists('/run/systemd/system');
end;

function IsAdminInstallMode: Boolean;
begin
  // Check if running with sudo/root
  Result := (GetEnv('SUDO_USER') <> '') or (GetEnv('USER') = 'root');
end;

// ========== WORKSPACE INITIALIZATION ==========
procedure InitializeWorkspace;
var
  WorkspacePath: string;
  ConfigFile: string;
begin
  WorkspacePath := ExpandConstant('{userappdata}/DSTerminal_Workspace');
  ConfigFile := WorkspacePath + '/config/workspace.json';
  
  // Create default config if it doesn't exist
  if not FileExists(ConfigFile) then
  begin
    SaveStringToFile(ConfigFile, 
      '{' + #10 +
      '  "version": "2.0.113",' + #10 +
      '  "created": "' + GetDateTimeString('yyyy-mm-dd hh:nn:ss', '-', ':') + '",' + #10 +
      '  "operator": "default",' + #10 +
      '  "settings": {' + #10 +
      '    "auto_update": true,' + #10 +
      '    "update_channel": "stable",' + #10 +
      '    "monitor_dirs": ["~/Documents", "~/Downloads"]' + #10 +
      '  }' + #10 +
      '}', False);
  end;
end;

// ========== CREATE SYMLINK TO /USR/LOCAL/BIN ==========
procedure CreateSymlink;
var
  SymlinkPath: string;
begin
  SymlinkPath := '/usr/local/bin/dsterminal';
  if not FileExists(SymlinkPath) then
  begin
    if Exec('/bin/ln', '-s ' + ExpandConstant('{app}/bin/dsterminal') + ' ' + SymlinkPath, '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
    begin
      Log('Symlink created: ' + SymlinkPath);
    end;
  end;
end;

// ========== ENABLE SYSTEMD SERVICE ==========
procedure EnableSystemdService;
var
  ServicePath: string;
begin
  if IsSystemD and WizardIsTaskSelected('systemd_service') then
  begin
    ServicePath := ExpandConstant('{app}/lib/systemd/system/dsterminal-monitor.service');
    if FileExists(ServicePath) then
    begin
      Exec('/bin/systemctl', 'enable --now dsterminal-monitor.service', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
      Log('Systemd service enabled');
    end;
  end;
end;

// ========== POST-INSTALLATION HOOK ==========
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    CreateSymlink;
    InitializeWorkspace;
    EnableSystemdService;
  end;
end;

// ========== CUSTOM PAGES ==========
procedure InitializeWizard;
begin
  // Custom page for workspace cleanup option
  RemoveWorkspacePage := CreateInputOptionPage(
    wpSelectTasks,
    'Workspace Cleanup',
    'Would you like to keep your workspace data?',
    'Select whether to keep or remove your DSTerminal workspace data when uninstalling.',
    True, False);
  RemoveWorkspacePage.Add('&Keep workspace data (recommended)');
  RemoveWorkspacePage.Add('&Remove workspace data');
  RemoveWorkspacePage.Values[0] := True;
  
  // Custom page for update channel selection
  UpdateChannelPage := CreateInputOptionPage(
    wpSelectTasks,
    'Update Settings',
    'Select your preferred update channel',
    'Choose between stable releases or development builds.',
    True, False);
  UpdateChannelPage.Add('&Stable (recommended for production)');
  UpdateChannelPage.Add('&Beta (for testing new features)');
  UpdateChannelPage.Add('&Development (nightly builds)');
  UpdateChannelPage.Values[0] := True;
end;

// ========== UNINSTALL CLEANUP ==========
function ShouldRemoveWorkspace: Boolean;
begin
  Result := not RemoveWorkspacePage.Values[0];
end;

function InitializeUninstall: Boolean;
begin
  Result := True;
  if ShouldRemoveWorkspace and DirExists(ExpandConstant('{userappdata}/DSTerminal_Workspace')) then
  begin
    if MsgBox('Do you want to remove your DSTerminal workspace data?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      DelTree(ExpandConstant('{userappdata}/DSTerminal_Workspace'), True, True, True);
    end;
  end;
end;

[Messages]
BeveledLabel=DSTerminal SOC Platform v2.0.113

[CustomMessages]
SetupAppTitle=DSTerminal Installer
SetupWindowTitle=DSTerminal v2.0.113 Setup for Linux
WelcomeLabel2=This will install DSTerminal v2.0.113 on your system.%n%nDSTerminal is a comprehensive security monitoring and analysis platform for Linux.