#!/usr/bin/env python3
"""
Example demonstrating Run and UninstallRun section functionality.

This example shows how to:
- Execute programs after installation
- Run configuration scripts
- Open documentation 
- Clean up during uninstallation
- Handle various execution flags
"""

from innosetup_builder import Installer, FileEntry, RunEntry, UninstallRunEntry, InnosetupCompiler


def main():
    # Define some files to install
    files = [
        FileEntry(source="bin\\myapp.exe", destination=""),
        FileEntry(source="bin\\config.exe", destination=""),
        FileEntry(source="bin\\cleanup.exe", destination=""),
        FileEntry(source="docs\\readme.txt", destination="docs"),
        FileEntry(source="config\\default.ini", destination="config")
    ]
    
    # Define run entries (executed after installation)
    run_entries = [
        # Run configuration tool automatically (silent)
        RunEntry(
            filename="{app}\\config.exe",
            description="Configure application settings",
            parameters="/autoconfig /silent",
            working_dir="{app}",
            status_msg="Configuring application...",
            flags="waituntilterminated"
        ),
        
        # Offer to show README file (user choice)
        RunEntry(
            filename="{app}\\docs\\readme.txt",
            description="View the README file",
            flags="postinstall shellexec skipifsilent unchecked"
        ),
        
        # Launch application (optional, unchecked by default)
        RunEntry(
            filename="{app}\\myapp.exe",
            description="Launch MyApp",
            working_dir="{app}",
            flags="postinstall nowait skipifsilent unchecked"
        ),
        
        # Hidden initialization (always runs)
        RunEntry(
            filename="{app}\\config.exe",
            parameters="/init",
            flags="runhidden waituntilterminated"
        ),
        
        # Example of shellexec with verb
        RunEntry(
            filename="https://mycompany.com/support",
            description="Visit support website",
            verb="open",
            flags="postinstall shellexec skipifsilent unchecked"
        )
    ]
    
    # Define uninstall run entries (executed during uninstallation)
    uninstall_run_entries = [
        # Clean up user data (with confirmation)
        UninstallRunEntry(
            filename="{app}\\cleanup.exe",
            parameters="/userdata /confirm",
            working_dir="{app}",
            runonce_id="cleanup_userdata",
            flags="waituntilterminated"
        ),
        
        # Remove temporary files (silent)
        UninstallRunEntry(
            filename="{app}\\cleanup.exe", 
            parameters="/temp /silent",
            runonce_id="cleanup_temp",
            flags="waituntilterminated"
        ),
        
        # Stop any running services
        UninstallRunEntry(
            filename="{sys}\\sc.exe",
            parameters="stop MyAppService",
            runonce_id="stop_service",
            flags="runhidden"
        )
    ]
    
    # Create the installer configuration
    installer = Installer(
        app_name="MyApp with Run Examples",
        app_version="1.0.0",
        author="My Company",
        main_executable="myapp.exe",
        desktop_icon=True,
        files=files,
        run_entries=run_entries,
        uninstall_run_entries=uninstall_run_entries,
        output_base_filename="MyAppWithRunSetup"
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
    
    print("Generated Inno Setup script with Run sections:")
    print("=" * 60)
    print(iss_content)
    
    # Save to file
    with open("example_with_run.iss", "w") as f:
        f.write(iss_content)
    print("\nScript saved to: example_with_run.iss")
    
    # Show key features
    print("\nKey Run Section Features Demonstrated:")
    print("- Post-install configuration tool")
    print("- Optional README viewing")
    print("- Optional application launch")
    print("- Hidden initialization")
    print("- Website opening with shellexec")
    print("- Uninstall cleanup with RunOnceId")
    print("- Service management during uninstall")


if __name__ == "__main__":
    main()