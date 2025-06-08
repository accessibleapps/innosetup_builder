#!/usr/bin/env python3
"""Tests for Components and Types functionality."""

import pytest
from innosetup_builder import (
    Installer, Component, ComponentType, FileEntry, DirEntry, 
    RegistryEntry, RunEntry, InnosetupCompiler
)


class TestComponentType:
    """Test ComponentType class functionality."""
    
    def test_component_type_defaults(self):
        """Test ComponentType with default values."""
        comp_type = ComponentType()
        assert comp_type.name == ""
        assert comp_type.description == ""
        assert comp_type.flags == ""
    
    def test_component_type_with_values(self):
        """Test ComponentType with custom values."""
        comp_type = ComponentType(
            name="full",
            description="Full installation",
            flags="iscustom"
        )
        assert comp_type.name == "full"
        assert comp_type.description == "Full installation"
        assert comp_type.flags == "iscustom"


class TestComponent:
    """Test Component class functionality."""
    
    def test_component_defaults(self):
        """Test Component with default values."""
        component = Component()
        assert component.name == ""
        assert component.description == ""
        assert component.types == ""
        assert component.extra_disk_space_required == ""
        assert component.flags == ""
    
    def test_component_with_values(self):
        """Test Component with custom values."""
        component = Component(
            name="main",
            description="Main Files",
            types="full compact",
            extra_disk_space_required="1024",
            flags="fixed"
        )
        assert component.name == "main"
        assert component.description == "Main Files"
        assert component.types == "full compact"
        assert component.extra_disk_space_required == "1024"
        assert component.flags == "fixed"
    
    def test_nested_component(self):
        """Test nested component naming."""
        component = Component(
            name="help\\english",
            description="English Help Files",
            types="full"
        )
        assert component.name == "help\\english"


class TestComponentsInEntries:
    """Test components parameter in various entry types."""
    
    def test_file_entry_with_components(self):
        """Test FileEntry with components parameter."""
        file_entry = FileEntry(
            source="test.exe",
            destination="",
            components="main"
        )
        assert file_entry.components == "main"
    
    def test_dir_entry_with_components(self):
        """Test DirEntry with components parameter."""
        dir_entry = DirEntry(
            name="{app}\\data",
            components="main"
        )
        assert dir_entry.components == "main"
    
    def test_registry_entry_with_components(self):
        """Test RegistryEntry with components parameter."""
        reg_entry = RegistryEntry(
            root="HKLM",
            subkey="Software\\Test",
            components="main"
        )
        assert reg_entry.components == "main"
    
    def test_run_entry_with_components(self):
        """Test RunEntry with components parameter."""
        run_entry = RunEntry(
            filename="{app}\\test.exe",
            components="main"
        )
        assert run_entry.components == "main"
    
    def test_boolean_expression_components(self):
        """Test components with boolean expressions."""
        file_entry = FileEntry(
            source="test.dll",
            components="main or help"
        )
        assert file_entry.components == "main or help"
        
        dir_entry = DirEntry(
            name="{app}\\optional",
            components="not main and (help or dev)"
        )
        assert dir_entry.components == "not main and (help or dev)"


class TestInstallerWithComponents:
    """Test Installer with Components and Types."""
    
    def test_installer_with_types(self):
        """Test installer with component types."""
        installer = Installer(
            app_name="TestApp",
            app_version="1.0",
            main_executable="test.exe"
        )
        
        installer.component_types = [
            ComponentType(name="full", description="Full installation"),
            ComponentType(name="custom", description="Custom", flags="iscustom")
        ]
        
        rendered = installer.render(InnosetupCompiler())
        
        assert "[Types]" in rendered
        assert 'Name: "full"; Description: "Full installation"' in rendered
        assert 'Name: "custom"; Description: "Custom"; Flags: iscustom' in rendered
    
    def test_installer_with_components(self):
        """Test installer with components."""
        installer = Installer(
            app_name="TestApp",
            app_version="1.0",
            main_executable="test.exe"
        )
        
        installer.components = [
            Component(
                name="main",
                description="Main Files",
                types="full compact",
                flags="fixed"
            ),
            Component(
                name="help",
                description="Help Files",
                types="full",
                extra_disk_space_required="1024"
            )
        ]
        
        rendered = installer.render(InnosetupCompiler())
        
        assert "[Components]" in rendered
        assert 'Name: "main"; Description: "Main Files"; Types: full compact; Flags: fixed' in rendered
        assert 'Name: "help"; Description: "Help Files"; Types: full; ExtraDiskSpaceRequired: 1024' in rendered
    
    def test_files_with_components(self):
        """Test files section with components."""
        installer = Installer(
            app_name="TestApp",
            app_version="1.0",
            main_executable="test.exe"
        )
        
        installer.files = [
            FileEntry(source="main.exe", components="main"),
            FileEntry(source="help.chm", components="help")
        ]
        
        rendered = installer.render(InnosetupCompiler())
        
        assert 'Source: "main.exe"; DestDir: "{app}"; Components: main' in rendered
        assert 'Source: "help.chm"; DestDir: "{app}"; Components: help' in rendered
    
    def test_complete_components_setup(self):
        """Test complete setup with types, components, and entries."""
        installer = Installer(
            app_name="CompleteApp",
            app_version="1.0",
            main_executable="app.exe"
        )
        
        # Add types
        installer.component_types = [
            ComponentType(name="full", description="Full installation"),
            ComponentType(name="compact", description="Compact installation"),
            ComponentType(name="custom", description="Custom", flags="iscustom")
        ]
        
        # Add components
        installer.components = [
            Component(name="main", description="Main Program", types="full compact custom", flags="fixed"),
            Component(name="help", description="Help Files", types="full custom"),
            Component(name="dev", description="Development Tools", types="full")
        ]
        
        # Add files with components
        installer.files = [
            FileEntry(source="app.exe", components="main"),
            FileEntry(source="help.pdf", destination="docs", components="help"),
            FileEntry(source="sdk.zip", destination="dev", components="dev")
        ]
        
        # Add dirs with components
        installer.dirs = [
            DirEntry(name="{app}\\docs", components="help"),
            DirEntry(name="{app}\\dev", components="dev")
        ]
        
        # Add registry with components
        installer.registry_entries = [
            RegistryEntry(
                root="HKLM",
                subkey="Software\\CompleteApp",
                value_type="string",
                value_name="Version",
                value_data="1.0",
                components="main"
            )
        ]
        
        # Add run entries with components
        installer.run_entries = [
            RunEntry(
                filename="{app}\\app.exe",
                description="Launch CompleteApp",
                flags="postinstall",
                components="main"
            )
        ]
        
        rendered = installer.render(InnosetupCompiler())
        
        # Verify all sections are present
        assert "[Types]" in rendered
        assert "[Components]" in rendered
        assert "[Files]" in rendered
        assert "[Dirs]" in rendered
        assert "[Registry]" in rendered
        assert "[Run]" in rendered
        
        # Verify components are properly referenced
        assert "Components: main" in rendered
        assert "Components: help" in rendered
        assert "Components: dev" in rendered
    
    def test_exclusive_components(self):
        """Test mutually exclusive components."""
        installer = Installer(
            app_name="TestApp",
            app_version="1.0"
        )
        
        installer.components = [
            Component(name="db\\sqlite", description="SQLite", flags="exclusive"),
            Component(name="db\\mysql", description="MySQL", flags="exclusive"),
            Component(name="db\\postgres", description="PostgreSQL", flags="exclusive")
        ]
        
        rendered = installer.render(InnosetupCompiler())
        
        assert 'Name: "db\\sqlite"; Description: "SQLite"; Flags: exclusive' in rendered
        assert 'Name: "db\\mysql"; Description: "MySQL"; Flags: exclusive' in rendered
        assert 'Name: "db\\postgres"; Description: "PostgreSQL"; Flags: exclusive' in rendered
    
    def test_components_not_rendered_when_empty(self):
        """Test that Types and Components sections are not rendered when empty."""
        installer = Installer(
            app_name="TestApp",
            app_version="1.0",
            main_executable="test.exe"
        )
        
        rendered = installer.render(InnosetupCompiler())
        
        assert "[Types]" not in rendered
        assert "[Components]" not in rendered