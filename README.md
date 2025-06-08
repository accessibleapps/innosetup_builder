# Innosetup Builder

[![Python](https://img.shields.io/badge/python-3.9-blue.svg)]() 

This is a Python package for creating Innosetup installers from a Jinja2 template and compiling them using the Inno Setup compiler. This makes it easier to create complex installer files programmatically, tailoring them to specific needs.

## Usage

```python
import pathlib
from innosetup_builder import Installer, FileEntry, InnosetupCompiler

installer = Installer(
    app_name="MyApp",
    app_version="1.0.0",
    main_executable="bin\\my_app.exe",
    files=list(all_files('src\\my_app')),
)

innosetup = InnosetupCompiler()
innosetup.build(installer)
```

In this example, "MyApp" is the name of the application for which you want to create the installer, "1.0.0" is the version of your application, "bin\\my_app.exe" is your main executable file, and "src\\my_app" is the directory for which you want to create an installer.

### Advanced Examples

#### Directory Creation
```python
from innosetup_builder import Installer, DirEntry

installer = Installer(
    app_name="MyApp",
    app_version="1.0.0",
    dirs=[
        DirEntry(name="{app}\\data"),
        DirEntry(name="{app}\\logs", permissions="users-modify"),
        DirEntry(name="{app}\\config", attribs="hidden", flags="setntfscompression")
    ]
)
```

#### Registry Entries
```python
from innosetup_builder import Installer, RegistryEntry

installer = Installer(
    app_name="MyApp",
    app_version="1.0.0",
    registry_entries=[
        RegistryEntry(
            root="HKLM",
            subkey="Software\\MyCompany\\MyApp",
            value_type="string",
            value_name="InstallPath",
            value_data="{app}"
        )
    ]
)
```

#### Run Commands
```python
from innosetup_builder import Installer, RunEntry

installer = Installer(
    app_name="MyApp",
    app_version="1.0.0",
    run_entries=[
        RunEntry(
            filename="{app}\\install_service.bat",
            description="Install Windows Service",
            flags="postinstall skipifsilent"
        )
    ]
)
```

## Features

This package provides a range of functionalities, including:

- Building Innosetup .iss files programmatically using a jinja2 template
- Compiling Innosetup installers with the Inno Setup compiler
- Rendering the installer with customization options
- Automatically fetching all files from a directory
- Fetching the installed location of Inno Setup from windows registry
- Registry manipulation with full data type support
- Post-installation and uninstallation run commands
- Advanced file handling with permissions, attributes, and flags
- Directory creation with permissions and attributes

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change. 
