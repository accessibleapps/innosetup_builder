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

## Features

This package provides a range of functionalities, including:

- Building Innosetup .iss files programmatically using a jinja2 template
- Compiling Innosetup installers with the Inno Setup compiler
- Rendering the installer with customization options
- Automatically fetching all files from a directory
- Fetching the installed location of Inno Setup from windows registry

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change. 
