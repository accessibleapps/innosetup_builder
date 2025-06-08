"""Tests for Registry section functionality."""

import pytest
from innosetup_builder import Installer, RegistryEntry


class TestRegistryEntry:
    def test_registry_entry_creation(self):
        entry = RegistryEntry(
            root="HKLM",
            subkey="Software\\MyCompany\\MyApp",
            value_type="string",
            value_name="InstallPath",
            value_data="{app}"
        )
        assert entry.root == "HKLM"
        assert entry.subkey == "Software\\MyCompany\\MyApp"
        assert entry.value_type == "string"
        assert entry.value_name == "InstallPath"
        assert entry.value_data == "{app}"

    def test_registry_entry_defaults(self):
        entry = RegistryEntry()
        assert entry.root == "HKLM"
        assert entry.subkey == ""
        assert entry.value_type == "none"
        assert entry.value_name == ""
        assert entry.value_data == ""
        assert entry.permissions == ""
        assert entry.flags == ""

    def test_registry_entry_with_flags(self):
        entry = RegistryEntry(
            root="HKCU",
            subkey="Software\\MyApp",
            flags="uninsdeletekey"
        )
        assert entry.flags == "uninsdeletekey"

    def test_registry_entry_dword_type(self):
        entry = RegistryEntry(
            root="HKLM",
            subkey="Software\\MyApp",
            value_type="dword",
            value_name="Version",
            value_data="1"
        )
        assert entry.value_type == "dword"
        assert entry.value_data == "1"


class TestInstallerWithRegistry:
    def test_installer_with_registry_entries(self):
        registry_entries = [
            RegistryEntry(
                root="HKLM",
                subkey="Software\\MyCompany",
                flags="uninsdeletekeyifempty"
            ),
            RegistryEntry(
                root="HKLM",
                subkey="Software\\MyCompany\\MyApp",
                value_type="string",
                value_name="InstallPath",
                value_data="{app}",
                flags="uninsdeletekey"
            )
        ]
        
        installer = Installer(
            app_name="Test App",
            app_version="1.0.0",
            registry_entries=registry_entries
        )
        
        assert len(installer.registry_entries) == 2
        assert installer.registry_entries[0].subkey == "Software\\MyCompany"
        assert installer.registry_entries[1].value_name == "InstallPath"

    def test_installer_registry_template_rendering(self):
        registry_entries = [
            RegistryEntry(
                root="HKLM",
                subkey="Software\\MyApp",
                value_type="string",
                value_name="Version",
                value_data="1.0.0"
            ),
            RegistryEntry(
                root="HKCU",
                subkey="Software\\MyApp\\Settings",
                value_type="dword",
                value_name="FirstRun",
                value_data="1",
                flags="createvalueifdoesntexist"
            )
        ]
        
        installer = Installer(
            app_name="Test App",
            registry_entries=registry_entries
        )
        
        # Create a mock InnosetupCompiler for testing
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        # Check that Registry section is included
        assert "[Registry]" in result
        assert "Root: HKLM; Subkey: \"Software\\MyApp\"" in result
        assert "ValueType: string" in result
        assert "ValueName: \"Version\"" in result
        assert "ValueData: \"1.0.0\"" in result
        assert "Root: HKCU; Subkey: \"Software\\MyApp\\Settings\"" in result
        assert "ValueType: dword" in result
        assert "Flags: createvalueifdoesntexist" in result

    def test_installer_no_registry_entries(self):
        installer = Installer(app_name="Test App")
        
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        # Should not include Registry section when no entries
        assert "[Registry]" not in result

    def test_registry_entry_none_value_type(self):
        """Test registry entry with value_type='none' (key only)"""
        entry = RegistryEntry(
            root="HKLM",
            subkey="Software\\MyApp",
            value_type="none",
            flags="uninsdeletekey"
        )
        
        installer = Installer(
            app_name="Test App",
            registry_entries=[entry]
        )
        
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        # Should not include ValueType when it's 'none'
        assert "ValueType: none" not in result
        assert "Root: HKLM; Subkey: \"Software\\MyApp\"" in result
        assert "Flags: uninsdeletekey" in result

    def test_registry_entry_with_permissions(self):
        """Test registry entry with permissions"""
        entry = RegistryEntry(
            root="HKLM",
            subkey="Software\\MyApp",
            value_type="string",
            value_name="SharedData",
            value_data="test",
            permissions="users-modify"
        )
        
        installer = Installer(
            app_name="Test App",
            registry_entries=[entry]
        )
        
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        assert "Permissions: users-modify" in result