[Setup]
AppName=TestApp
WizardStyle=modern
DefaultDirName={autopf}\TestApp
DefaultGroupName=TestApp
AppVersion  =1.0
Compression=lzma2/ultra
VersionInfoProductName=TestApp
OutputBaseFilename=testapp_dirs_setup


[Files]

Source: "README.md"; DestDir: "{app}"

Source: "innosetup_builder.py"; DestDir: "{app}"; DestName: "testapp.exe"




[Dirs]

Name: "{app}\data"

Name: "{app}\logs"; Permissions: users-modify

Name: "{app}\config"; Attribs: hidden

Name: "{app}\cache"; Flags: setntfscompression

Name: "{userappdata}\TestApp"; Flags: uninsneveruninstall

Name: "{app}\temp"; Permissions: users-full; Attribs: system hidden; Flags: deleteafterinstall






[Languages]
MessagesFile: "compiler:Default.isl"; Name: "Default"



[Icons]
Name: "{group}\TestApp"; Filename: "{app}\testapp.exe"
Name: "{group}\Uninstall TestApp"; Filename: "{uninstallexe}"