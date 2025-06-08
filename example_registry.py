#!/usr/bin/env python3
"""
Example demonstrating Registry section functionality in innosetup_builder.

This example shows how to create registry entries for:
- Application installation path
- Version information  
- User settings with proper cleanup
"""

from innosetup_builder import Installer, FileEntry, RegistryEntry, InnosetupCompiler


def main():
    # Define some files to install
    files = [
        FileEntry(source="bin\\myapp.exe", destination=""),
        FileEntry(source="config\\default.ini", destination="config"),
        FileEntry(source="readme.txt", destination="")
    ]
    
    # Define registry entries
    registry_entries = [
        # Create company key (will be cleaned up if empty during uninstall)
        RegistryEntry(
            root="HKLM",
            subkey="Software\\MyCompany",
            flags="uninsdeletekeyifempty"
        ),
        
        # Application key with installation path
        RegistryEntry(
            root="HKLM", 
            subkey="Software\\MyCompany\\MyApp",
            value_type="string",
            value_name="InstallPath",
            value_data="{app}",
            flags="uninsdeletekey"
        ),
        
        # Version information
        RegistryEntry(
            root="HKLM",
            subkey="Software\\MyCompany\\MyApp",
            value_type="string", 
            value_name="Version",
            value_data="1.0.0"
        ),
        
        # User-specific settings in HKCU
        RegistryEntry(
            root="HKCU",
            subkey="Software\\MyCompany\\MyApp\\Settings",
            value_type="dword",
            value_name="FirstRun", 
            value_data="1",
            flags="createvalueifdoesntexist uninsdeletevalue"
        ),
        
        # File association (example)
        RegistryEntry(
            root="HKCR",
            subkey=".myext",
            value_type="string",
            value_data="MyApp.Document",
            flags="uninsdeletevalue"
        ),
        
        # File association description
        RegistryEntry(
            root="HKCR", 
            subkey="MyApp.Document",
            value_type="string",
            value_data="MyApp Document",
            flags="uninsdeletekey"
        ),
        
        # Shell command for opening files
        RegistryEntry(
            root="HKCR",
            subkey="MyApp.Document\\shell\\open\\command",
            value_type="string", 
            value_data='"{app}\\myapp.exe" "%1"'
        )
    ]
    
    # Create the installer configuration
    installer = Installer(
        app_name="My Application",
        app_version="1.0.0",
        author="My Company",
        author_email="support@mycompany.com", 
        main_executable="myapp.exe",
        desktop_icon=True,
        files=files,
        registry_entries=registry_entries,
        output_base_filename="MyAppSetup"
    )
    
    # Create compiler instance (will work on Windows with Inno Setup installed)
    try:
        compiler = InnosetupCompiler()
        print("Inno Setup found at:", compiler.base_path)
    except (FileNotFoundError, TypeError):
        print("Inno Setup not found, creating mock compiler for demo")
        compiler = InnosetupCompiler(base_path=None)
    
    # Generate the .iss file content
    iss_content = installer.render(compiler)
    
    print("Generated Inno Setup script:")
    print("=" * 50)
    print(iss_content)
    
    # Optionally save to file
    with open("example_with_registry.iss", "w") as f:
        f.write(iss_content)
    print("\nScript saved to: example_with_registry.iss")


if __name__ == "__main__":
    main()