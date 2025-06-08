"""Tests for Run and UninstallRun section functionality."""

import pytest
from innosetup_builder import Installer, RunEntry, UninstallRunEntry


class TestRunEntry:
    def test_run_entry_creation(self):
        entry = RunEntry(
            filename="{app}\\setup.exe",
            description="Complete installation",
            parameters="/silent",
            working_dir="{app}",
            status_msg="Configuring application...",
            flags="postinstall skipifsilent"
        )
        assert entry.filename == "{app}\\setup.exe"
        assert entry.description == "Complete installation"
        assert entry.parameters == "/silent"
        assert entry.working_dir == "{app}"
        assert entry.status_msg == "Configuring application..."
        assert entry.flags == "postinstall skipifsilent"

    def test_run_entry_defaults(self):
        entry = RunEntry()
        assert entry.filename == ""
        assert entry.description == ""
        assert entry.parameters == ""
        assert entry.working_dir == ""
        assert entry.status_msg == ""
        assert entry.verb == ""
        assert entry.flags == ""

    def test_run_entry_with_verb(self):
        entry = RunEntry(
            filename="readme.txt",
            verb="open",
            flags="shellexec postinstall"
        )
        assert entry.verb == "open"
        assert entry.flags == "shellexec postinstall"


class TestUninstallRunEntry:
    def test_uninstall_run_entry_creation(self):
        entry = UninstallRunEntry(
            filename="{app}\\cleanup.exe",
            parameters="/removedata",
            working_dir="{app}",
            runonce_id="cleanup_data",
            flags="waituntilterminated"
        )
        assert entry.filename == "{app}\\cleanup.exe"
        assert entry.parameters == "/removedata"
        assert entry.working_dir == "{app}"
        assert entry.runonce_id == "cleanup_data"
        assert entry.flags == "waituntilterminated"

    def test_uninstall_run_entry_defaults(self):
        entry = UninstallRunEntry()
        assert entry.filename == ""
        assert entry.parameters == ""
        assert entry.working_dir == ""
        assert entry.runonce_id == ""
        assert entry.verb == ""
        assert entry.flags == ""


class TestInstallerWithRun:
    def test_installer_with_run_entries(self):
        run_entries = [
            RunEntry(
                filename="{app}\\init.exe",
                parameters="/setup",
                flags="waituntilterminated"
            ),
            RunEntry(
                filename="readme.txt",
                description="View README",
                flags="postinstall shellexec skipifsilent"
            )
        ]
        
        installer = Installer(
            app_name="Test App",
            run_entries=run_entries
        )
        
        assert len(installer.run_entries) == 2
        assert installer.run_entries[0].filename == "{app}\\init.exe"
        assert installer.run_entries[1].description == "View README"

    def test_installer_with_uninstall_run_entries(self):
        uninstall_entries = [
            UninstallRunEntry(
                filename="{app}\\cleanup.exe",
                runonce_id="cleanup",
                flags="waituntilterminated"
            )
        ]
        
        installer = Installer(
            app_name="Test App",
            uninstall_run_entries=uninstall_entries
        )
        
        assert len(installer.uninstall_run_entries) == 1
        assert installer.uninstall_run_entries[0].runonce_id == "cleanup"

    def test_installer_run_template_rendering(self):
        run_entries = [
            RunEntry(
                filename="{app}\\setup.exe",
                description="Initialize application",
                parameters="/config",
                working_dir="{app}",
                status_msg="Configuring...",
                flags="waituntilterminated"
            ),
            RunEntry(
                filename="readme.txt",
                description="View README file",
                flags="postinstall shellexec skipifsilent unchecked"
            )
        ]
        
        installer = Installer(
            app_name="Test App",
            run_entries=run_entries
        )
        
        # Create a mock InnosetupCompiler for testing
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        # Check that Run section is included
        assert "[Run]" in result
        assert 'Filename: "{app}\\setup.exe"' in result
        assert 'Description: "Initialize application"' in result
        assert 'Parameters: "/config"' in result
        assert 'WorkingDir: "{app}"' in result
        assert 'StatusMsg: "Configuring..."' in result
        assert 'Flags: waituntilterminated' in result
        assert 'Filename: "readme.txt"' in result
        assert 'Flags: postinstall shellexec skipifsilent unchecked' in result

    def test_installer_uninstall_run_template_rendering(self):
        uninstall_entries = [
            UninstallRunEntry(
                filename="{app}\\cleanup.exe",
                parameters="/removeall",
                runonce_id="cleanup_all",
                flags="waituntilterminated"
            )
        ]
        
        installer = Installer(
            app_name="Test App",
            uninstall_run_entries=uninstall_entries
        )
        
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        # Check that UninstallRun section is included
        assert "[UninstallRun]" in result
        assert 'Filename: "{app}\\cleanup.exe"' in result
        assert 'Parameters: "/removeall"' in result
        assert 'RunOnceId: "cleanup_all"' in result
        assert 'Flags: waituntilterminated' in result

    def test_installer_no_run_entries(self):
        installer = Installer(app_name="Test App")
        
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        # Should not include Run sections when no entries
        assert "[Run]" not in result
        assert "[UninstallRun]" not in result

    def test_installer_mixed_run_entries(self):
        """Test installer with both Run and UninstallRun entries"""
        run_entries = [
            RunEntry(
                filename="{app}\\init.exe",
                flags="waituntilterminated"
            )
        ]
        
        uninstall_entries = [
            UninstallRunEntry(
                filename="{app}\\cleanup.exe",
                runonce_id="cleanup"
            )
        ]
        
        installer = Installer(
            app_name="Test App",
            run_entries=run_entries,
            uninstall_run_entries=uninstall_entries
        )
        
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        # Both sections should be present
        assert "[Run]" in result
        assert "[UninstallRun]" in result
        assert 'Filename: "{app}\\init.exe"' in result
        assert 'Filename: "{app}\\cleanup.exe"' in result

    def test_run_entry_minimal_parameters(self):
        """Test run entry with only filename"""
        run_entries = [
            RunEntry(filename="{app}\\simple.exe")
        ]
        
        installer = Installer(
            app_name="Test App",
            run_entries=run_entries
        )
        
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        # Should only include filename, no other parameters
        lines = result.split('\n')
        run_line = [line for line in lines if 'Filename: "{app}\\simple.exe"' in line][0]
        
        # Should not contain empty parameter clauses
        assert '; Description: ""' not in run_line
        assert '; Parameters: ""' not in run_line
        assert '; WorkingDir: ""' not in run_line