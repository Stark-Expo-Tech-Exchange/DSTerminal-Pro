; DSTerminal Installer Script - Non-Admin Safe

[Setup]
AppName=DSTerminal
AppVersion=v2.1.0
AppPublisher=Stark Expo Tech Exchange
AppPublisherURL=https://starkexpotechexchange-mw.com
; Install to AppData to avoid admin rights
DefaultDirName={userappdata}\DSTerminal
DefaultGroupName=DSTerminal
LicenseFile=license.txt
OutputDir=.
OutputBaseFilename=DSTerminal_Installer_v2.1.0
Compression=lzma
SolidCompression=yes
DisableWelcomePage=no
WizardStyle=modern
SetupIconFile=installer_assets/icon.ico
DisableProgramGroupPage=no
AllowNoIcons=yes
PrivilegesRequired=lowest
MinVersion=10.0.10240

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\dsterminal_win-2.0.59_x64-amd64.exe"; DestDir: "{app}"; DestName: "dsterminal.exe"; Flags: ignoreversion
Source: "tools\*"; DestDir: "{app}\tools"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs
Source: "templates\*"; DestDir: "{app}\templates"; Flags: ignoreversion recursesubdirs
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "redist\ffmpeg\*"; DestDir: "{app}\ffmpeg"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: IsFFmpegRequired
Source: "tools\update-helper.ps1"; DestDir: "{app}\tools"; Flags: ignoreversion

[Icons]
Name: "{group}\DSTerminal"; Filename: "{app}\dsterminal.exe"; WorkingDir: "{userappdata}\DSTerminal_Workspace"
Name: "{group}\Uninstall DSTerminal"; Filename: "{uninstallexe}"
Name: "{userdesktop}\DSTerminal"; Filename: "{app}\dsterminal.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: checkedonce

[Dirs]
Name: "{userappdata}\DSTerminal_Workspace"
Name: "{userappdata}\DSTerminal_Workspace\scans"
Name: "{userappdata}\DSTerminal_Workspace\reports"
Name: "{userappdata}\DSTerminal_Workspace\exploits"
Name: "{userappdata}\DSTerminal_Workspace\sandbox"
Name: "{userappdata}\DSTerminal_Workspace\quarantine"
Name: "{app}\logs"
Name: "{app}\updates"

[Run]
Filename: "{app}\dsterminal.exe"; Description: "Launch DSTerminal"; Flags: nowait postinstall skipifsilent

[Code]
function IsFFmpegRequired: Boolean;
begin
  Result := 
    (FileExists(ExpandConstant('{sys}\ffmpeg.exe')) = False) and
    (FileExists(ExpandConstant('{app}\ffmpeg\ffmpeg.exe')) = False);
end;