#!/usr/bin/env python3
"""Tests for DirEntry functionality."""

import pytest
from innosetup_builder import Installer, DirEntry, InnosetupCompiler


def test_dir_entry_defaults():
    """Test DirEntry class with default values."""
    dir_entry = DirEntry()
    assert dir_entry.name == ""
    assert dir_entry.permissions == ""
    assert dir_entry.attribs == ""
    assert dir_entry.flags == ""


def test_dir_entry_with_values():
    """Test DirEntry class with custom values."""
    dir_entry = DirEntry(
        name="{app}\\data",
        permissions="users-modify",
        attribs="hidden",
        flags="setntfscompression"
    )
    assert dir_entry.name == "{app}\\data"
    assert dir_entry.permissions == "users-modify"
    assert dir_entry.attribs == "hidden"
    assert dir_entry.flags == "setntfscompression"


def test_installer_with_dirs():
    """Test Installer with directory entries."""
    installer = Installer(
        app_name="TestApp",
        app_version="1.0",
        main_executable="test.exe"
    )
    
    # Add directory entries
    installer.dirs = [
        DirEntry(name="{app}\\data"),
        DirEntry(
            name="{app}\\logs",
            permissions="users-full",
            flags="uninsneveruninstall"
        )
    ]
    
    # Render the installer
    rendered = installer.render(InnosetupCompiler())
    
    # Check that Dirs section is present
    assert "[Dirs]" in rendered
    assert 'Name: "{app}\\data"' in rendered
    assert 'Name: "{app}\\logs"; Permissions: users-full; Flags: uninsneveruninstall' in rendered


def test_dirs_section_conditional():
    """Test that Dirs section only appears when dirs are defined."""
    installer = Installer(
        app_name="TestApp",
        app_version="1.0",
        main_executable="test.exe"
    )
    
    # Render without dirs
    rendered = installer.render(InnosetupCompiler())
    assert "[Dirs]" not in rendered
    
    # Add a dir and render again
    installer.dirs = [DirEntry(name="{app}\\data")]
    rendered = installer.render(InnosetupCompiler())
    assert "[Dirs]" in rendered


def test_dir_with_all_attributes():
    """Test directory entry with all possible attributes."""
    dir_entry = DirEntry(
        name="{commonappdata}\\TestApp\\Config",
        permissions="admins-full users-readexec",
        attribs="readonly hidden system",
        flags="setntfscompression uninsalwaysuninstall"
    )
    
    installer = Installer(
        app_name="TestApp",
        app_version="1.0",
        main_executable="test.exe",
        dirs=[dir_entry]
    )
    
    rendered = installer.render(InnosetupCompiler())
    expected_line = 'Name: "{commonappdata}\\TestApp\\Config"; Permissions: admins-full users-readexec; Attribs: readonly hidden system; Flags: setntfscompression uninsalwaysuninstall'
    assert expected_line in rendered


def test_multiple_dirs_order():
    """Test that multiple directories are rendered in order."""
    installer = Installer(
        app_name="TestApp",
        app_version="1.0",
        main_executable="test.exe",
        dirs=[
            DirEntry(name="{app}\\first"),
            DirEntry(name="{app}\\second"),
            DirEntry(name="{app}\\third")
        ]
    )
    
    rendered = installer.render(InnosetupCompiler())
    
    # Check order is preserved
    first_pos = rendered.find('Name: "{app}\\first"')
    second_pos = rendered.find('Name: "{app}\\second"')
    third_pos = rendered.find('Name: "{app}\\third"')
    
    assert first_pos < second_pos < third_pos