#!/usr/bin/env python3
"""
Example demonstrating advanced FileEntry functionality.

This example shows how to:
- Use file attributes and permissions
- Handle version checking and shared files  
- Install fonts and .NET assemblies
- Use exclusion patterns
- Handle external files
- Apply various file flags for different scenarios
"""

from innosetup_builder import Installer, FileEntry, InnosetupCompiler


def main():
    # Define files with various advanced options
    files = [
        # Basic application executable
        FileEntry(
            source="bin\\myapp.exe",
            destination="",
            flags="replacesameversion"
        ),
        
        # Configuration file with restricted access
        FileEntry(
            source="config\\app.ini",
            destination="config",
            attribs="readonly",
            permissions="users-readexec",
            flags="confirmoverwrite"
        ),
        
        # Shared DLL with version management
        FileEntry(
            source="lib\\shared.dll",
            destination="",
            flags="sharedfile regserver replacesameversion restartreplace"
        ),
        
        # Font installation
        FileEntry(
            source="fonts\\CustomFont.ttf",
            destination="",
            font_install="Custom Application Font",
            flags="onlyifdoesntexist uninsneveruninstall"
        ),
        
        # .NET Assembly for GAC
        FileEntry(
            source="lib\\MyLibrary.dll",
            destination="",
            strong_assembly_name="MyLibrary, Version=1.0.0.0, Culture=neutral, PublicKeyToken=1234567890abcdef, ProcessorArchitecture=MSIL",
            flags="gacinstall sharedfile"
        ),
        
        # Data files with exclusions
        FileEntry(
            source="data\\*",
            destination="data",
            excludes="*.tmp,*.log,*.debug,\\temp\\*",
            flags="recursesubdirs createallsubdirs"
        ),
        
        # Template file that gets renamed
        FileEntry(
            source="templates\\default.template",
            destination="config",
            dest_name="user.ini",
            flags="onlyifdoesntexist"
        ),
        
        # External file from source media
        FileEntry(
            source="{src}\\external\\large_data.bin",
            destination="data",
            external_size="10485760",  # 10MB
            flags="external skipifsourcedoesntexist"
        ),
        
        # Temporary file for installation only
        FileEntry(
            source="temp\\installer_helper.exe",
            destination="temp",
            flags="deleteafterinstall dontcopy"
        ),
        
        # System file with special handling
        FileEntry(
            source="system\\driver.sys",
            destination="",
            attribs="system hidden",
            permissions="administrators-full",
            flags="allowunsafefiles overwritereadonly 32bit"
        ),
        
        # Compressed data that should not be recompressed
        FileEntry(
            source="assets\\images.zip",
            destination="assets",
            flags="nocompression"
        ),
        
        # Development files only installed in debug builds
        FileEntry(
            source="debug\\*.pdb",
            destination="debug",
            flags="recursesubdirs skipifsourcedoesntexist"
        ),
        
        # README file that opens after installation
        FileEntry(
            source="docs\\readme.txt",
            destination="docs",
            flags="isreadme"
        ),
        
        # Backup of existing config (if any)
        FileEntry(
            source="{app}\\config\\user.ini",
            destination="backup",
            dest_name="user.ini.backup",
            flags="external onlyifdestfileexists"
        )
    ]
    
    # Create the installer configuration
    installer = Installer(
        app_name="Advanced Files Demo",
        app_version="1.0.0",
        author="Demo Company",
        main_executable="myapp.exe",
        desktop_icon=True,
        files=files,
        output_base_filename="AdvancedFilesDemo"
    )
    
    # Create compiler instance
    try:
        compiler = InnosetupCompiler()
        print("Inno Setup found at:", compiler.base_path)
    except (FileNotFoundError, TypeError):
        print("Inno Setup not found, creating mock compiler for demo")
        compiler = InnosetupCompiler(base_path=None)
    
    # Generate the .iss file content
    iss_content = installer.render(compiler)
    
    print("Generated Inno Setup script with advanced file handling:")
    print("=" * 70)
    print(iss_content)
    
    # Save to file
    with open("example_advanced_files.iss", "w") as f:
        f.write(iss_content)
    print("\nScript saved to: example_advanced_files.iss")
    
    # Show key features
    print("\nAdvanced File Features Demonstrated:")
    print("- File attributes and permissions")
    print("- Version checking and shared file management")
    print("- Font installation with proper flags")
    print("- .NET GAC assembly installation")
    print("- File exclusion patterns")
    print("- External file handling")
    print("- File renaming during installation")
    print("- Temporary files and cleanup")
    print("- System file handling")
    print("- Compression control")
    print("- Conditional installation")
    print("- README file integration")
    print("- Configuration backup")


if __name__ == "__main__":
    main()