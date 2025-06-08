#!/usr/bin/env python3
"""Example of using Components and Types for modular installation."""

import tempfile
import pathlib
from innosetup_builder import (
    Installer, FileEntry, DirEntry, RegistryEntry, RunEntry, 
    Component, ComponentType, InnosetupCompiler
)

# Create installer with components
installer = Installer(
    app_name="ComponentsApp",
    app_version="2.0",
    app_short_description="Application with selectable components",
    main_executable="app.exe",
    output_base_filename="componentsapp_setup"
)

# Define setup types
installer.component_types = [
    ComponentType(
        name="full",
        description="Full installation"
    ),
    ComponentType(
        name="compact", 
        description="Compact installation"
    ),
    ComponentType(
        name="custom",
        description="Custom installation",
        flags="iscustom"
    )
]

# Define components
installer.components = [
    # Main component (always installed)
    Component(
        name="main",
        description="Main Program Files", 
        types="full compact custom",
        flags="fixed"
    ),
    
    # Optional components
    Component(
        name="help",
        description="Help Files",
        types="full custom"
    ),
    
    # Nested components
    Component(
        name="help\\english",
        description="English Help",
        types="full custom"
    ),
    Component(
        name="help\\spanish",
        description="Spanish Help",
        types="full"
    ),
    
    # Development tools
    Component(
        name="dev",
        description="Development Tools",
        types="full",
        extra_disk_space_required="1048576"  # 1MB extra
    ),
    
    # Exclusive components (only one can be selected)
    Component(
        name="database\\sqlite",
        description="SQLite Database",
        types="full compact custom",
        flags="exclusive"
    ),
    Component(
        name="database\\mysql",
        description="MySQL Database", 
        types="full custom",
        flags="exclusive"
    )
]

# Add files with component associations
installer.files = [
    # Main files (always installed)
    FileEntry(
        source="README.md",
        destination="",
        components="main"
    ),
    FileEntry(
        source="innosetup_builder.py",
        destination="",
        dest_name="app.exe",
        components="main"
    ),
    
    # Help files
    FileEntry(
        source="TODO.md",
        destination="help",
        dest_name="help_en.txt",
        components="help\\english"
    ),
    FileEntry(
        source="CLAUDE.md",
        destination="help", 
        dest_name="help_es.txt",
        components="help\\spanish"
    ),
    
    # Development tools
    FileEntry(
        source="pyproject.toml",
        destination="dev",
        components="dev"
    ),
    
    # Database files
    FileEntry(
        source=".gitignore",
        destination="db",
        dest_name="sqlite.db",
        components="database\\sqlite"
    ),
    FileEntry(
        source=".gitignore",
        destination="db",
        dest_name="mysql.cfg",
        components="database\\mysql"
    )
]

# Add directories with component associations
installer.dirs = [
    DirEntry(
        name="{app}\\data",
        components="main"
    ),
    DirEntry(
        name="{app}\\help",
        components="help"
    ),
    DirEntry(
        name="{app}\\dev\\tools",
        components="dev"
    ),
    DirEntry(
        name="{app}\\db",
        components="database\\sqlite or database\\mysql"
    )
]

# Add registry entries with component associations
installer.registry_entries = [
    RegistryEntry(
        root="HKLM",
        subkey="Software\\ComponentsApp",
        value_type="string",
        value_name="InstallPath",
        value_data="{app}",
        components="main"
    ),
    RegistryEntry(
        root="HKLM",
        subkey="Software\\ComponentsApp",
        value_type="string", 
        value_name="DatabaseType",
        value_data="SQLite",
        components="database\\sqlite"
    ),
    RegistryEntry(
        root="HKLM",
        subkey="Software\\ComponentsApp",
        value_type="string",
        value_name="DatabaseType", 
        value_data="MySQL",
        components="database\\mysql"
    )
]

# Add run entries with component associations  
installer.run_entries = [
    RunEntry(
        filename="{app}\\app.exe",
        description="Launch ComponentsApp",
        flags="postinstall skipifsilent",
        components="main"
    ),
    RunEntry(
        filename="{app}\\dev\\setup_dev.bat",
        description="Configure development environment",
        components="dev"
    )
]

# Create output directory
output_dir = tempfile.mkdtemp()
output_path = pathlib.Path(output_dir) / "componentsapp.iss"

# Write the .iss file
with open(output_path, "w") as f:
    f.write(installer.render(InnosetupCompiler()))

print(f"Generated Inno Setup script: {output_path}")
print("\nScript content:")
print("-" * 80)
with open(output_path, "r") as f:
    print(f.read())