"""Tests for advanced FileEntry functionality with flags and parameters."""

import pytest
from innosetup_builder import Installer, FileEntry


class TestAdvancedFileEntry:
    def test_file_entry_with_dest_name(self):
        entry = FileEntry(
            source="app.exe",
            destination="",
            dest_name="myapp.exe"
        )
        assert entry.dest_name == "myapp.exe"

    def test_file_entry_with_excludes(self):
        entry = FileEntry(
            source="data\\*",
            destination="data",
            excludes="*.tmp,*.log"
        )
        assert entry.excludes == "*.tmp,*.log"

    def test_file_entry_with_attributes(self):
        entry = FileEntry(
            source="config.ini",
            destination="config",
            attribs="readonly hidden"
        )
        assert entry.attribs == "readonly hidden"

    def test_file_entry_with_permissions(self):
        entry = FileEntry(
            source="data.txt",
            destination="data",
            permissions="users-modify"
        )
        assert entry.permissions == "users-modify"

    def test_file_entry_with_font_install(self):
        entry = FileEntry(
            source="myfont.ttf",
            destination="",
            font_install="My Custom Font",
            flags="onlyifdoesntexist uninsneveruninstall"
        )
        assert entry.font_install == "My Custom Font"
        assert entry.flags == "onlyifdoesntexist uninsneveruninstall"

    def test_file_entry_with_version_flags(self):
        entry = FileEntry(
            source="shared.dll",
            destination="",
            flags="sharedfile regserver replacesameversion"
        )
        assert entry.flags == "sharedfile regserver replacesameversion"

    def test_file_entry_with_compression_flags(self):
        entry = FileEntry(
            source="large_file.bin",
            destination="data",
            flags="nocompression solidbreak"
        )
        assert entry.flags == "nocompression solidbreak"

    def test_file_entry_with_external_size(self):
        entry = FileEntry(
            source="{src}\\external.dat",
            destination="data",
            external_size="1048576",
            flags="external"
        )
        assert entry.external_size == "1048576"
        assert entry.flags == "external"

    def test_file_entry_with_strong_assembly_name(self):
        entry = FileEntry(
            source="MyAssembly.dll",
            destination="",
            strong_assembly_name="MyAssembly, Version=1.0.0.0, Culture=neutral, PublicKeyToken=abcdef123456",
            flags="gacinstall"
        )
        assert "MyAssembly, Version=1.0.0.0" in entry.strong_assembly_name
        assert entry.flags == "gacinstall"

    def test_file_entry_defaults_extended(self):
        entry = FileEntry()
        assert entry.dest_name == ""
        assert entry.excludes == ""
        assert entry.external_size == ""
        assert entry.attribs == ""
        assert entry.permissions == ""
        assert entry.font_install == ""
        assert entry.strong_assembly_name == ""
        assert entry.flags == ""


class TestInstallerWithAdvancedFiles:
    def test_installer_advanced_files_template_rendering(self):
        files = [
            # Basic file
            FileEntry(
                source="app.exe",
                destination=""
            ),
            # File with destination name
            FileEntry(
                source="setup.exe",
                destination="tools",
                dest_name="installer.exe"
            ),
            # File with attributes and permissions
            FileEntry(
                source="config.ini",
                destination="config",
                attribs="readonly",
                permissions="users-readexec"
            ),
            # File with version checking flags
            FileEntry(
                source="shared.dll",
                destination="",
                flags="sharedfile regserver replacesameversion"
            ),
            # Font installation
            FileEntry(
                source="myfont.ttf",
                destination="",
                font_install="My Custom Font",
                flags="onlyifdoesntexist uninsneveruninstall"
            ),
            # File with excludes pattern
            FileEntry(
                source="data\\*",
                destination="data",
                excludes="*.tmp,*.log",
                flags="recursesubdirs"
            )
        ]
        
        installer = Installer(
            app_name="Advanced Files Test",
            files=files
        )
        
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        # Check that Files section is included with proper formatting
        assert "[Files]" in result
        
        # Check basic file
        assert 'Source: "app.exe"; DestDir: "{app}"' in result
        
        # Check file with destination name
        assert 'Source: "setup.exe"; DestDir: "{app}\\tools"; DestName: "installer.exe"' in result
        
        # Check file with attributes and permissions
        assert 'Source: "config.ini"; DestDir: "{app}\\config"' in result
        assert 'Attribs: readonly' in result
        assert 'Permissions: users-readexec' in result
        
        # Check file with flags
        assert 'Source: "shared.dll"; DestDir: "{app}"; Flags: sharedfile regserver replacesameversion' in result
        
        # Check font installation
        assert 'FontInstall: "My Custom Font"' in result
        assert 'Flags: onlyifdoesntexist uninsneveruninstall' in result
        
        # Check excludes pattern
        assert 'Excludes: "*.tmp,*.log"' in result
        assert 'Flags: recursesubdirs' in result

    def test_installer_file_with_all_parameters(self):
        """Test file entry with all possible parameters"""
        files = [
            FileEntry(
                source="complex.exe",
                destination="bin",
                dest_name="renamed.exe",
                excludes="*.debug",
                attribs="readonly system",
                permissions="everyone-readexec",
                flags="overwritereadonly confirmoverwrite replacesameversion"
            )
        ]
        
        installer = Installer(
            app_name="Complex File Test",
            files=files
        )
        
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        # Check that all parameters are included
        file_line = [line for line in result.split('\n') if 'Source: "complex.exe"' in line][0]
        assert 'DestDir: "{app}\\bin"' in file_line
        assert 'DestName: "renamed.exe"' in file_line
        assert 'Excludes: "*.debug"' in file_line
        assert 'Attribs: readonly system' in file_line
        assert 'Permissions: everyone-readexec' in file_line
        assert 'Flags: overwritereadonly confirmoverwrite replacesameversion' in file_line

    def test_installer_file_with_external_flag(self):
        """Test external file with size specification"""
        files = [
            FileEntry(
                source="{src}\\external.dat",
                destination="data",
                external_size="2097152",
                flags="external skipifsourcedoesntexist"
            )
        ]
        
        installer = Installer(
            app_name="External File Test",
            files=files
        )
        
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        assert 'ExternalSize: 2097152' in result
        assert 'Flags: external skipifsourcedoesntexist' in result

    def test_installer_gac_assembly(self):
        """Test .NET GAC assembly installation"""
        files = [
            FileEntry(
                source="MyLibrary.dll",
                destination="",
                strong_assembly_name="MyLibrary, Version=1.0.0.0, Culture=neutral, PublicKeyToken=abcdef123456, ProcessorArchitecture=MSIL",
                flags="gacinstall sharedfile"
            )
        ]
        
        installer = Installer(
            app_name="GAC Assembly Test",
            files=files
        )
        
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        assert 'StrongAssemblyName: "MyLibrary, Version=1.0.0.0, Culture=neutral, PublicKeyToken=abcdef123456, ProcessorArchitecture=MSIL"' in result
        assert 'Flags: gacinstall sharedfile' in result

    def test_installer_empty_destination_handling(self):
        """Test proper handling of empty destination"""
        files = [
            FileEntry(
                source="root.exe",
                destination=""  # Should install to app root
            ),
            FileEntry(
                source="sub.exe",
                destination="tools"  # Should install to app\tools
            )
        ]
        
        installer = Installer(
            app_name="Destination Test",
            files=files
        )
        
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        # Empty destination should result in just {app}
        assert 'Source: "root.exe"; DestDir: "{app}"' in result
        # Non-empty destination should include subdirectory
        assert 'Source: "sub.exe"; DestDir: "{app}\\tools"' in result