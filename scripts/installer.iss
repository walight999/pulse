; Pulse Windows installer — Inno Setup script
;
; Build:
;   1. Build the .exe first:    pyinstaller pulse.spec
;   2. Install Inno Setup:      https://jrsoftware.org/isinfo.php  (free)
;   3. Compile:                  ISCC.exe scripts\installer.iss
;   Output: scripts\Output\pulse-setup-1.5.0.exe
;
; Signed installer (when you have a code signing cert):
;   Pass /S "<certificate-path>" to ISCC, or set SignTool in the Inno Setup IDE.

#define MyAppName "pulse"
#define MyAppVersion "1.5.0"
#define MyAppPublisher "White"
#define MyAppURL "https://pulse.app"
#define MyAppExeName "pulse.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-4789-A1B2-PULSE0000001}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/support
AppUpdatesURL={#MyAppURL}/changelog
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=..\LICENSE
OutputBaseFilename=pulse-setup-{#MyAppVersion}
SetupIconFile=..\static\brand\app-icon.png
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName} {#MyAppVersion}

; Brand colors for installer
WindowVisible=no
DisableWelcomePage=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &Desktop shortcut"; \
    GroupDescription: "Additional shortcuts:"; Flags: unchecked
Name: "autostart"; Description: "&Launch pulse at Windows startup"; \
    GroupDescription: "Startup:"

[Files]
; Main executable (built by pyinstaller pulse.spec)
Source: "..\dist\pulse.exe"; DestDir: "{app}"; Flags: ignoreversion

; Brand assets (in case the .exe needs them on first run)
Source: "..\static\brand\*"; DestDir: "{app}\static\brand"; Flags: ignoreversion recursesubdirs

; Docs
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\PRIVACY.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\SECURITY.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; \
    Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; \
    Flags: nowait postinstall skipifsilent

[Registry]
; Auto-launch at startup (optional, user can untick)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
    ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"""; \
    Flags: uninsdeletevalue; Tasks: autostart

[UninstallDelete]
; Clean up user data prompt is shown in [Code] section
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\backups"

[Code]
function InitializeUninstall(): Boolean;
var
  Choice: Integer;
begin
  Choice := MsgBox(
    'Do you want to keep your Pulse data?' + #13#10#13#10 +
    'YES — keeps your subscription data, usage history, and backups.' + #13#10 +
    'NO — deletes everything (this cannot be undone).',
    mbConfirmation, MB_YESNO);
  if Choice = IDNO then begin
    DelTree(ExpandConstant('{userappdata}\pulse'), True, True, True);
    DelTree(ExpandConstant('{localappdata}\pulse'), True, True, True);
  end;
  Result := True;
end;

[Messages]
WelcomeLabel1=Welcome to pulse
WelcomeLabel2=This will install pulse {#MyAppVersion} on your computer.%n%nLocal-first personal finance dashboard for the AI era. No account, no cloud, no telemetry by default.%n%nClick Next to continue.
FinishedHeadingLabel=pulse is ready
FinishedLabelNoIcons=pulse is now installed and will appear in your system tray (lower-right corner).
