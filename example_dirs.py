#!/usr/bin/env python3
"""Example of using DirEntry for creating directories during installation."""

import tempfile
import pathlib
from innosetup_builder import Installer, DirEntry, InnosetupCompiler, FileEntry

# Create installer with directory creation
installer = Installer(
    app_name="TestApp",
    app_version="1.0",
    app_short_description="Test application with directory creation",
    main_executable="testapp.exe",
    output_base_filename="testapp_dirs_setup"
)

# Add some basic files
installer.files = [
    FileEntry(source="README.md", destination=""),
    FileEntry(source="innosetup_builder.py", destination="", dest_name="testapp.exe")
]

# Add directory entries with various options
installer.dirs = [
    # Basic directory
    DirEntry(name="{app}\\data"),
    
    # Directory with permissions
    DirEntry(
        name="{app}\\logs",
        permissions="users-modify"
    ),
    
    # Directory with attributes
    DirEntry(
        name="{app}\\config",
        attribs="hidden"
    ),
    
    # Directory with NTFS compression flag
    DirEntry(
        name="{app}\\cache",
        flags="setntfscompression"
    ),
    
    # User-specific directory
    DirEntry(
        name="{userappdata}\\TestApp",
        flags="uninsneveruninstall"
    ),
    
    # Multiple flags and attributes
    DirEntry(
        name="{app}\\temp",
        attribs="system hidden",
        permissions="users-full",
        flags="deleteafterinstall"
    )
]

# Create output directory
output_dir = tempfile.mkdtemp()
output_path = pathlib.Path(output_dir) / "testapp_dirs.iss"

# Write the .iss file
with open(output_path, "w") as f:
    f.write(installer.render(InnosetupCompiler()))

print(f"Generated Inno Setup script: {output_path}")
print("\nScript content:")
print("-" * 80)
with open(output_path, "r") as f:
    print(f.read())