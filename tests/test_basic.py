"""Basic tests for innosetup_builder functionality."""

import pytest
import tempfile
import pathlib
from types import SimpleNamespace
from unittest.mock import Mock

import innosetup_builder
from innosetup_builder import Installer, FileEntry, InnosetupCompiler, all_files


class TestFileEntry:
    def test_file_entry_creation(self):
        entry = FileEntry(source="test.exe", destination="bin")
        assert entry.source == "test.exe"
        assert entry.destination == "bin"

    def test_file_entry_defaults(self):
        entry = FileEntry()
        assert entry.source is None
        assert entry.destination is None


class TestInstaller:
    def test_installer_creation(self):
        installer = Installer(
            app_name="Test App",
            app_version="1.0.0",
            main_executable="test.exe"
        )
        assert installer.app_name == "Test App"
        assert installer.app_version == "1.0.0"
        assert installer.main_executable == "test.exe"

    def test_installer_defaults(self):
        installer = Installer()
        assert installer.author == ""
        assert installer.app_name == ""
        assert installer.desktop_icon is False
        assert installer.multilingual is True
        assert len(installer.files) == 0

    def test_installer_render_basic(self):
        installer = Installer(
            app_name="Test App",
            app_version="1.0.0",
            main_executable="test.exe"
        )
        
        # Create a mock InnosetupCompiler for testing
        class MockInnosetupCompiler:
            extra_iss = ""
            def available_languages(self):
                return []
        
        mock_compiler = MockInnosetupCompiler()
        result = installer.render(mock_compiler)
        
        assert "AppName=Test App" in result
        assert "AppVersion  =1.0.0" in result
        assert "test.exe" in result

    def test_installer_with_files(self):
        files = [
            FileEntry(source="app.exe", destination=""),
            FileEntry(source="config.ini", destination="config")
        ]
        installer = Installer(
            app_name="Test App",
            files=files
        )
        assert len(installer.files) == 2
        assert installer.files[0].source == "app.exe"


class TestAllFiles:
    def test_all_files_generator(self):
        # Create a temporary directory structure for testing
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = pathlib.Path(tmpdir)
            
            # Create test files
            (tmppath / "test1.txt").write_text("content1")
            (tmppath / "subdir").mkdir()
            (tmppath / "subdir" / "test2.txt").write_text("content2")
            
            # Test the generator
            files = list(all_files(tmppath))
            assert len(files) == 2
            
            # Check that we get FileEntry objects
            for file_entry in files:
                assert isinstance(file_entry, FileEntry)
                assert file_entry.source is not None
                assert file_entry.destination is not None


class TestInnosetupCompiler:
    def test_default_compiler_finds_standard_registry_install(self, monkeypatch):
        standard_key = (
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1"
        )
        handle = object()

        def open_key(root, subkey):
            if subkey != standard_key:
                raise FileNotFoundError(subkey)
            return handle

        registry = SimpleNamespace(
            HKEY_LOCAL_MACHINE=object(),
            OpenKey=Mock(side_effect=open_key),
            QueryValueEx=Mock(return_value=(r"C:\Inno Setup 6", 1)),
            CloseKey=Mock(),
        )
        monkeypatch.setattr(innosetup_builder.platform, "system", lambda: "Windows")
        monkeypatch.setattr(innosetup_builder, "winreg", registry, raising=False)

        compiler = InnosetupCompiler()

        assert compiler.base_path == r"C:\Inno Setup 6"
        registry.OpenKey.assert_called_once_with(registry.HKEY_LOCAL_MACHINE, standard_key)
        registry.CloseKey.assert_called_once_with(handle)

    def test_compiler_creation(self):
        # Test with None base_path (non-Windows environment)
        compiler = InnosetupCompiler(base_path=None)
        assert compiler.base_path is None

    def test_compiler_paths_with_base(self):
        compiler = InnosetupCompiler(base_path="/test/path")
        assert compiler.languages_path == pathlib.Path("/test/path/Languages")
        assert compiler.compiler_path == pathlib.Path("/test/path/ISCC.exe")

    def test_available_languages_with_base(self):
        # Test available_languages when base_path is set but path doesn't exist
        compiler = InnosetupCompiler(base_path="/test/path")
        languages = list(compiler.available_languages())
        assert isinstance(languages, list)
        assert len(languages) == 0  # Should be empty when path doesn't exist

    def test_available_languages_none_base(self):
        # Test available_languages when base_path is None
        compiler = InnosetupCompiler(base_path=None)
        languages = list(compiler.available_languages())
        assert isinstance(languages, list)
        assert len(languages) == 0
