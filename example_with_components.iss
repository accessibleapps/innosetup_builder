[Setup]
AppName=ComponentsApp
WizardStyle=modern
DefaultDirName={autopf}\ComponentsApp
DefaultGroupName=ComponentsApp
AppVersion  =2.0
Compression=lzma2/ultra
VersionInfoProductName=ComponentsApp
OutputBaseFilename=componentsapp_setup



[Types]

Name: "full"; Description: "Full installation"

Name: "compact"; Description: "Compact installation"

Name: "custom"; Description: "Custom installation"; Flags: iscustom




[Components]

Name: "main"; Description: "Main Program Files"; Types: full compact custom; Flags: fixed

Name: "help"; Description: "Help Files"; Types: full custom

Name: "help\english"; Description: "English Help"; Types: full custom

Name: "help\spanish"; Description: "Spanish Help"; Types: full

Name: "dev"; Description: "Development Tools"; Types: full; ExtraDiskSpaceRequired: 1048576

Name: "database\sqlite"; Description: "SQLite Database"; Types: full compact custom; Flags: exclusive

Name: "database\mysql"; Description: "MySQL Database"; Types: full custom; Flags: exclusive




[Files]

Source: "README.md"; DestDir: "{app}"; Components: main

Source: "innosetup_builder.py"; DestDir: "{app}"; DestName: "app.exe"; Components: main

Source: "TODO.md"; DestDir: "{app}\help"; DestName: "help_en.txt"; Components: help\english

Source: "CLAUDE.md"; DestDir: "{app}\help"; DestName: "help_es.txt"; Components: help\spanish

Source: "pyproject.toml"; DestDir: "{app}\dev"; Components: dev

Source: ".gitignore"; DestDir: "{app}\db"; DestName: "sqlite.db"; Components: database\sqlite

Source: ".gitignore"; DestDir: "{app}\db"; DestName: "mysql.cfg"; Components: database\mysql




[Dirs]

Name: "{app}\data"; Components: main

Name: "{app}\help"; Components: help

Name: "{app}\dev\tools"; Components: dev

Name: "{app}\db"; Components: database\sqlite or database\mysql




[Registry]

Root: HKLM; Subkey: "Software\ComponentsApp"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Components: main

Root: HKLM; Subkey: "Software\ComponentsApp"; ValueType: string; ValueName: "DatabaseType"; ValueData: "SQLite"; Components: database\sqlite

Root: HKLM; Subkey: "Software\ComponentsApp"; ValueType: string; ValueName: "DatabaseType"; ValueData: "MySQL"; Components: database\mysql




[Languages]
MessagesFile: "compiler:Default.isl"; Name: "Default"



[Icons]
Name: "{group}\ComponentsApp"; Filename: "{app}\app.exe"
Name: "{group}\Uninstall ComponentsApp"; Filename: "{uninstallexe}"





[Run]

Filename: "{app}\app.exe"; Description: "Launch ComponentsApp"; Flags: postinstall skipifsilent; Components: main

Filename: "{app}\dev\setup_dev.bat"; Description: "Configure development environment"; Components: dev