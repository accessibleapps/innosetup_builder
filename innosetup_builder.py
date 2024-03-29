"""This is a module which builds Innosetup .iss files from a Jinja2 template."""

import pathlib
import platform
import subprocess
import tempfile
try:
    import winreg
except ImportError:
    pass


import jinja2
from attr import Factory, define, field

innosetup_template = """\
[Setup]
AppName={{ installer.app_name }}
WizardStyle=modern
DefaultDirName={autopf}\\{{ installer.app_name }}
DefaultGroupName={{ installer.app_name }}
AppVersion  ={{ installer.app_version }}
Compression=lzma2/ultra
VersionInfoProductName={{ installer.app_name }}
{%- if installer.license_file -%}
LicenseFile={{ installer.license_file }}
{%- endif -%}
{% if installer.output_base_filename %}
OutputBaseFilename={{ installer.output_base_filename }}
{% endif %}
{% if installer.files %}
[files]
{% for file in installer.files %}
Source:     "{{ file.source }}";                 DestDir: "{app}\\{{ file.destination }}";
{% endfor %}    
{% endif %}

{% if installer.multilingual %}
[Languages]
MessagesFile: "compiler:Default.isl"; Name: "Default"
{% for language in innosetup.available_languages() %}
MessagesFile: "{{ language.messages_file }}"; Name: "{{ language.name }}"
{% endfor %}
{% endif %}

[Icons]
Name: "{group}\\{{ installer.app_name }}"; Filename: "{app}\\{{ installer.main_executable }}"
Name: "{group}\\Uninstall {{ installer.app_name }}"; Filename: "{uninstallexe}"
{% if installer.desktop_icon %}
tasks: "desktopicon"; WorkingDir: "{app}"; Name: "{commondesktop}\\{{ installer.app_name }}"; filename: "{app}\\{{ installer.main_executable }}"
{% endif %}

{% if installer.desktop_icon or installer.run_at_startup %}
[tasks]
{% if installer.desktop_icon %}
GroupDescription: "{cm:AdditionalIcons}"; Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"
{% endif %}
{% if installer.run_at_startup %}
Name: "startup"; Description: "Run at startup"

[registry]
Tasks: "startup"; ValueType: "string"; ValueData: "{app}\\{{ installer.main_executable }}"; Flags: uninsdeletevalue; Subkey: "Software\\Microsoft\\Windows\\CurrentVersion\\Run"; ValueName: "{{ installer.app_name }}"; Root: "HKCU"
{% endif %}
{% endif %}

{{ innosetup.extra_iss }}
"""


@define
class FileEntry:
    """This class represents a file entry in the innosetup template."""
    source: str = field(default=None)
    destination: str = field(default=None)


@define
class Installer:
    """This class represents an installer."""
    author: str = field(default="")
    author_email: str = field(default="")
    app_name: str = field(default="")
    app_version: str = field(default="")
    app_short_description: str = field(default="")
    desktop_icon = field(default=False)
    run_at_startup: bool = field(default=False)
    multilingual: bool = field(default=True)
    main_executable: str = field(default="")
    files = field(default=Factory(list))
    license_file = field(default=None)
    output_base_filename: str = field(default="")
    extra_iss = field(default="")

    def render(self, innosetup_installation):
        """This method renders the installer."""
        env = jinja2.Environment()
        # load the template from the string
        template = env.from_string(innosetup_template)
        # render the template
        return template.render(installer=self, innosetup=innosetup_installation)


def get_path_from_registry():
    """This function gets the path to the innosetup installation from the registry"""
    if platform.system() != "Windows":
        return None
    try:
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion   \\Uninstall\\Inno Setup 6_is1")
        except FileNotFoundError:
            # WOW64
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Inno Setup 6_is1")
    except FileNotFoundError:
        raise FileNotFoundError("Inno Setup 6 is not installed")
    path = winreg.QueryValueEx(key, "InstallLocation")[0]
    winreg.CloseKey(key)
    return path


def all_files(path):
    """A generator which produces all files as FileEntry objects relative to a directory recursively"""
    path = pathlib.Path(path)

    def _all_files(_path):
        for entry in _path.iterdir():
            if entry.is_dir():
                yield from _all_files(entry)
            else:
                yield FileEntry(source=str(entry.absolute()), destination=str(entry.relative_to(path).parent))
    yield from _all_files(path)


@define
class InnosetupCompiler:
    """Represents the local innosetup installation"""
    base_path = field(default=Factory(get_path_from_registry))

    @property
    def languages_path(self):
        """This property returns the path to the languages folder."""
        return pathlib.Path(self.base_path) / "Languages"

    @property
    def compiler_path(self):
        """This property returns the path to the compiler executable."""
        return pathlib.Path(self.base_path) / "ISCC.exe"

    def available_languages(self):
        for language in self.languages_path.iterdir():
            yield {'name': language.stem,
                   'messages_file': 'compiler:' + str(language.relative_to(self.base_path))
                   }

    def build(self, installer, output_path=pathlib.Path       .cwd() / "installer.exe"):
        """This method compiles the given installer"""
        with tempfile.TemporaryDirectory() as tmpdir:
            installer_path = pathlib.Path(tmpdir) / "installer.iss"
            installer_text = installer.render(self)
            installer_path.write_text(installer_text)
            subprocess.check_call(
                [str(self.compiler_path), '/Qp', '/O' + str(output_path), str(installer_path)])
