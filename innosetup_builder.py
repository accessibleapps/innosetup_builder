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

{% if installer.registry_entries %}
[Registry]
{% for entry in installer.registry_entries %}
Root: {{ entry.root }}; Subkey: "{{ entry.subkey }}"{% if entry.value_type != "none" %}; ValueType: {{ entry.value_type }}{% endif %}{% if entry.value_name %}; ValueName: "{{ entry.value_name }}"{% endif %}{% if entry.value_data %}; ValueData: "{{ entry.value_data }}"{% endif %}{% if entry.permissions %}; Permissions: {{ entry.permissions }}{% endif %}{% if entry.flags %}; Flags: {{ entry.flags }}{% endif %}
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

{% if installer.run_entries %}
[Run]
{% for entry in installer.run_entries %}
Filename: "{{ entry.filename }}"{% if entry.description %}; Description: "{{ entry.description }}"{% endif %}{% if entry.parameters %}; Parameters: "{{ entry.parameters }}"{% endif %}{% if entry.working_dir %}; WorkingDir: "{{ entry.working_dir }}"{% endif %}{% if entry.status_msg %}; StatusMsg: "{{ entry.status_msg }}"{% endif %}{% if entry.verb %}; Verb: "{{ entry.verb }}"{% endif %}{% if entry.flags %}; Flags: {{ entry.flags }}{% endif %}
{% endfor %}
{% endif %}

{% if installer.uninstall_run_entries %}
[UninstallRun]
{% for entry in installer.uninstall_run_entries %}
Filename: "{{ entry.filename }}"{% if entry.parameters %}; Parameters: "{{ entry.parameters }}"{% endif %}{% if entry.working_dir %}; WorkingDir: "{{ entry.working_dir }}"{% endif %}{% if entry.runonce_id %}; RunOnceId: "{{ entry.runonce_id }}"{% endif %}{% if entry.verb %}; Verb: "{{ entry.verb }}"{% endif %}{% if entry.flags %}; Flags: {{ entry.flags }}{% endif %}
{% endfor %}
{% endif %}

{{ innosetup.extra_iss }}
"""


@define
class FileEntry:
    """This class represents a file entry in the innosetup template."""
    source: str = field(default=None)
    destination: str = field(default=None)


@define
class RegistryEntry:
    """This class represents a registry entry in the innosetup template."""
    root: str = field(default="HKLM")  # HKLM, HKCU, HKCR, HKU, HKCC, HKA
    subkey: str = field(default="")
    value_type: str = field(default="none")  # none, string, expandsz, multisz, dword, qword, binary
    value_name: str = field(default="")
    value_data: str = field(default="")
    permissions: str = field(default="")
    flags: str = field(default="")


@define
class RunEntry:
    """This class represents a run entry in the innosetup template."""
    filename: str = field(default="")
    description: str = field(default="")
    parameters: str = field(default="")
    working_dir: str = field(default="")
    status_msg: str = field(default="")
    verb: str = field(default="")
    flags: str = field(default="")


@define
class UninstallRunEntry:
    """This class represents an uninstall run entry in the innosetup template."""
    filename: str = field(default="")
    parameters: str = field(default="")
    working_dir: str = field(default="")
    runonce_id: str = field(default="")
    verb: str = field(default="")
    flags: str = field(default="")


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
    registry_entries = field(default=Factory(list))
    run_entries = field(default=Factory(list))
    uninstall_run_entries = field(default=Factory(list))
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
        if self.base_path is None or not self.languages_path.exists():
            return
        for language in self.languages_path.iterdir():
            if language.is_file() and language.suffix.lower() == '.isl':
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
