"""This is a module which builds Innosetup .iss files from a Jinja2 template."""

import pathlib
import platform
import subprocess
import tempfile
from enum import StrEnum
from typing import Any, Dict, Generator, List, Optional, Union
try:
    import winreg
except ImportError:
    pass


import jinja2
from attr import Factory, define, field


class FileFlags(StrEnum):
    """Enum for Inno Setup file flags providing type safety."""
    
    # Architecture flags
    FLAG_32BIT = "32bit"
    FLAG_64BIT = "64bit"
    
    # Overwrite behavior flags
    IGNORE_VERSION = "ignoreversion"
    COMPARE_TIMESTAMP = "comparetimestamp"
    CONFIRM_OVERWRITE = "confirmoverwrite"
    OVERWRITE_READONLY = "overwritereadonly" 
    REPLACE_SAME_VERSION = "replacesameversion"
    PROMPT_IF_OLDER = "promptifolder"
    
    # Installation condition flags
    ONLY_IF_DOESNT_EXIST = "onlyifdoesntexist"
    ONLY_IF_DEST_FILE_EXISTS = "onlyifdestfileexists"
    
    # File handling flags
    DELETE_AFTER_INSTALL = "deleteafterinstall"
    DONT_COPY = "dontcopy"
    EXTERNAL = "external"
    RESTART_REPLACE = "restartreplace"
    
    # Registration flags
    REG_SERVER = "regserver"
    REG_TYPELIB = "regtypelib"
    NO_REG_ERROR = "noregerror"
    
    # Special file flags
    IS_README = "isreadme"
    SHARED_FILE = "sharedfile"
    ALLOW_UNSAFE_FILES = "allowunsafefiles"
    
    # Directory handling
    RECURSE_SUBDIRS = "recursesubdirs"
    CREATE_ALL_SUBDIRS = "createallsubdirs"
    
    # Compression and encryption
    NO_COMPRESSION = "nocompression"
    NO_ENCRYPTION = "noencryption"
    SOLID_BREAK = "solidbreak"
    SORT_FILES_BY_EXTENSION = "sortfilesbyextension"
    SORT_FILES_BY_NAME = "sortfilesbyname"
    
    # Font installation
    FONT_ISNT_TRUETYPE = "fontisnttruetype"
    
    # GAC installation
    GAC_INSTALL = "gacinstall"
    
    # NTFS compression
    SET_NTFS_COMPRESSION = "setntfscompression"
    UNSET_NTFS_COMPRESSION = "unsetntfscompression"
    
    # Security and verification
    DONT_VERIFY_CHECKSUM = "dontverifychecksum"
    SIGN = "sign"
    SIGN_CHECK = "signcheck"
    SIGN_ONCE = "signonce"
    
    # Uninstall behavior
    UNINS_NEVER_UNINSTALL = "uninsneveruninstall"
    UNINS_RESTART_DELETE = "uninsrestartdelete"
    UNINS_REMOVE_READONLY = "uninsremovereadonly"
    UNINS_NO_SHARED_FILE_PROMPT = "uninsnosharedfileprompt"
    
    # Misc flags
    TOUCH = "touch"
    SKIP_IF_SOURCE_DOESNT_EXIST = "skipifsourcedoesntexist"


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

{% if installer.component_types %}
[Types]
{% for type in installer.component_types %}
Name: "{{ type.name }}"; Description: "{{ type.description }}"{% if type.flags %}; Flags: {{ type.flags }}{% endif %}
{% endfor %}
{% endif %}

{% if installer.components %}
[Components]
{% for component in installer.components %}
Name: "{{ component.name }}"; Description: "{{ component.description }}"{% if component.types %}; Types: {{ component.types }}{% endif %}{% if component.extra_disk_space_required %}; ExtraDiskSpaceRequired: {{ component.extra_disk_space_required }}{% endif %}{% if component.flags %}; Flags: {{ component.flags }}{% endif %}
{% endfor %}
{% endif %}

{% if installer.files %}
[Files]
{% for file in installer.files %}
Source: "{{ file.source }}"; DestDir: "{app}{% if file.destination %}\\{{ file.destination }}{% endif %}"{% if file.dest_name %}; DestName: "{{ file.dest_name }}"{% endif %}{% if file.excludes %}; Excludes: "{{ file.excludes }}"{% endif %}{% if file.external_size %}; ExternalSize: {{ file.external_size }}{% endif %}{% if file.attribs %}; Attribs: {{ file.attribs }}{% endif %}{% if file.permissions %}; Permissions: {{ file.permissions }}{% endif %}{% if file.font_install %}; FontInstall: "{{ file.font_install }}"{% endif %}{% if file.strong_assembly_name %}; StrongAssemblyName: "{{ file.strong_assembly_name }}"{% endif %}{% if file.flags_string %}; Flags: {{ file.flags_string }}{% endif %}{% if file.components %}; Components: {{ file.components }}{% endif %}
{% endfor %}
{% endif %}

{% if installer.dirs %}
[Dirs]
{% for dir in installer.dirs %}
Name: "{{ dir.name }}"{% if dir.permissions %}; Permissions: {{ dir.permissions }}{% endif %}{% if dir.attribs %}; Attribs: {{ dir.attribs }}{% endif %}{% if dir.flags %}; Flags: {{ dir.flags }}{% endif %}{% if dir.components %}; Components: {{ dir.components }}{% endif %}
{% endfor %}
{% endif %}

{% if installer.registry_entries %}
[Registry]
{% for entry in installer.registry_entries %}
Root: {{ entry.root }}; Subkey: "{{ entry.subkey }}"{% if entry.value_type != "none" %}; ValueType: {{ entry.value_type }}{% endif %}{% if entry.value_name %}; ValueName: "{{ entry.value_name }}"{% endif %}{% if entry.value_data %}; ValueData: "{{ entry.value_data }}"{% endif %}{% if entry.permissions %}; Permissions: {{ entry.permissions }}{% endif %}{% if entry.flags %}; Flags: {{ entry.flags }}{% endif %}{% if entry.components %}; Components: {{ entry.components }}{% endif %}
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
Filename: "{{ entry.filename }}"{% if entry.description %}; Description: "{{ entry.description }}"{% endif %}{% if entry.parameters %}; Parameters: "{{ entry.parameters }}"{% endif %}{% if entry.working_dir %}; WorkingDir: "{{ entry.working_dir }}"{% endif %}{% if entry.status_msg %}; StatusMsg: "{{ entry.status_msg }}"{% endif %}{% if entry.verb %}; Verb: "{{ entry.verb }}"{% endif %}{% if entry.flags %}; Flags: {{ entry.flags }}{% endif %}{% if entry.components %}; Components: {{ entry.components }}{% endif %}
{% endfor %}
{% endif %}

{% if installer.uninstall_run_entries %}
[UninstallRun]
{% for entry in installer.uninstall_run_entries %}
Filename: "{{ entry.filename }}"{% if entry.parameters %}; Parameters: "{{ entry.parameters }}"{% endif %}{% if entry.working_dir %}; WorkingDir: "{{ entry.working_dir }}"{% endif %}{% if entry.runonce_id %}; RunOnceId: "{{ entry.runonce_id }}"{% endif %}{% if entry.verb %}; Verb: "{{ entry.verb }}"{% endif %}{% if entry.flags %}; Flags: {{ entry.flags }}{% endif %}{% if entry.components %}; Components: {{ entry.components }}{% endif %}
{% endfor %}
{% endif %}

{{ innosetup.extra_iss }}
"""


@define
class FileEntry:
    """This class represents a file entry in the innosetup template."""
    source: Optional[str] = field(default=None)
    destination: Optional[str] = field(default=None)
    dest_name: str = field(default="")
    excludes: str = field(default="")
    external_size: str = field(default="")
    attribs: str = field(default="")
    permissions: str = field(default="")
    font_install: str = field(default="")
    strong_assembly_name: str = field(default="")
    flags: Union[str, List[FileFlags], FileFlags] = field(default="")
    components: str = field(default="")
    
    @property
    def flags_string(self) -> str:
        """Convert flags to space-separated string for Inno Setup template."""
        if isinstance(self.flags, str):
            return self.flags
        elif isinstance(self.flags, FileFlags):
            return str(self.flags)
        elif isinstance(self.flags, list):
            return " ".join(str(flag) for flag in self.flags)
        return ""


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
    components: str = field(default="")


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
    components: str = field(default="")


@define
class UninstallRunEntry:
    """This class represents an uninstall run entry in the innosetup template."""
    filename: str = field(default="")
    parameters: str = field(default="")
    working_dir: str = field(default="")
    runonce_id: str = field(default="")
    verb: str = field(default="")
    flags: str = field(default="")
    components: str = field(default="")


@define
class DirEntry:
    """This class represents a directory entry in the innosetup template."""
    name: str = field(default="")
    permissions: str = field(default="")
    attribs: str = field(default="")
    flags: str = field(default="")
    components: str = field(default="")


@define
class ComponentType:
    """This class represents a setup type in the innosetup template."""
    name: str = field(default="")
    description: str = field(default="")
    flags: str = field(default="")


@define
class Component:
    """This class represents a component in the innosetup template."""
    name: str = field(default="")
    description: str = field(default="")
    types: str = field(default="")
    extra_disk_space_required: str = field(default="")
    flags: str = field(default="")


@define
class Installer:
    """This class represents an installer."""
    author: str = field(default="")
    author_email: str = field(default="")
    app_name: str = field(default="")
    app_version: str = field(default="")
    app_short_description: str = field(default="")
    desktop_icon: bool = field(default=False)
    run_at_startup: bool = field(default=False)
    multilingual: bool = field(default=True)
    main_executable: str = field(default="")
    files: List[FileEntry] = field(default=Factory(list))
    registry_entries: List[RegistryEntry] = field(default=Factory(list))
    run_entries: List[RunEntry] = field(default=Factory(list))
    uninstall_run_entries: List[UninstallRunEntry] = field(default=Factory(list))
    dirs: List[DirEntry] = field(default=Factory(list))
    component_types: List[ComponentType] = field(default=Factory(list))
    components: List[Component] = field(default=Factory(list))
    license_file: Optional[str] = field(default=None)
    output_base_filename: str = field(default="")
    extra_iss: str = field(default="")

    def render(self, innosetup_installation: 'InnosetupCompiler') -> str:
        """This method renders the installer."""
        env = jinja2.Environment()
        # load the template from the string
        template = env.from_string(innosetup_template)
        # render the template
        return template.render(installer=self, innosetup=innosetup_installation)


def get_path_from_registry() -> Optional[str]:
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


def get_default_flags_for_file(file_path: pathlib.Path, main_executable: Optional[str] = None) -> List[FileFlags]:
    """Determine appropriate default flags for a file based on its type and purpose."""
    flags = []
    
    # Get file extension
    suffix = file_path.suffix.lower()
    filename = file_path.name
    
    # Check if this is the main executable
    if main_executable and filename == main_executable:
        flags.append(FileFlags.IGNORE_VERSION)
        flags.append(FileFlags.OVERWRITE_READONLY)
    
    # Executable files (not main executable)
    elif suffix in {'.exe', '.com', '.bat', '.cmd'}:
        flags.append(FileFlags.IGNORE_VERSION)
    
    # Dynamic libraries and components
    elif suffix in {'.dll'}:
        flags.append(FileFlags.SHARED_FILE)
    elif suffix in {'.ocx', '.bpl', '.dpl'}:
        flags.append(FileFlags.SHARED_FILE)
        flags.append(FileFlags.REG_SERVER)
    
    # Configuration files - don't overwrite if they exist
    elif suffix in {'.ini', '.cfg', '.config', '.json', '.xml', '.yaml', '.yml'} or filename.lower() in {'settings.txt', 'config.txt'}:
        flags.append(FileFlags.ONLY_IF_DOESNT_EXIST)
    
    # README files
    elif filename.lower() in {'readme.txt', 'readme.md', 'read me.txt'} or 'readme' in filename.lower():
        flags.append(FileFlags.IS_README)
    
    # Font files
    elif suffix in {'.ttf', '.otf', '.fon'}:
        flags.append(FileFlags.ONLY_IF_DOESNT_EXIST)
        flags.append(FileFlags.UNINS_NEVER_UNINSTALL)
    
    # Help files
    elif suffix in {'.chm', '.hlp'}:
        flags.append(FileFlags.IGNORE_VERSION)
    
    # Type libraries
    elif suffix in {'.tlb'}:
        flags.append(FileFlags.REG_TYPELIB)
        flags.append(FileFlags.SHARED_FILE)
    
    # Compressed files - don't compress again
    elif suffix in {'.zip', '.7z', '.rar', '.gz', '.jpg', '.jpeg', '.png', '.gif', '.mp3', '.mp4', '.avi'}:
        flags.append(FileFlags.NO_COMPRESSION)
    
    return flags


def all_files(path: Union[str, pathlib.Path], main_executable: Optional[str] = None, auto_flags: bool = True) -> Generator[FileEntry, None, None]:
    """A generator which produces all files as FileEntry objects relative to a directory recursively
    
    Args:
        path: Directory to scan for files
        main_executable: Name of the main executable to give special treatment
        auto_flags: Whether to automatically assign appropriate flags based on file type
    """
    path = pathlib.Path(path)

    def _all_files(_path: pathlib.Path) -> Generator[FileEntry, None, None]:
        for entry in _path.iterdir():
            if entry.is_dir():
                yield from _all_files(entry)
            else:
                flags = get_default_flags_for_file(entry, main_executable) if auto_flags else []
                yield FileEntry(
                    source=str(entry.absolute()), 
                    destination=str(entry.relative_to(path).parent),
                    flags=flags
                )
    yield from _all_files(path)


@define
class InnosetupCompiler:
    """Represents the local innosetup installation"""
    base_path: Optional[str] = field(default=Factory(get_path_from_registry))

    @property
    def languages_path(self) -> pathlib.Path:
        """This property returns the path to the languages folder."""
        return pathlib.Path(self.base_path) / "Languages"

    @property
    def compiler_path(self) -> pathlib.Path:
        """This property returns the path to the compiler executable."""
        return pathlib.Path(self.base_path) / "ISCC.exe"

    def available_languages(self) -> Generator[Dict[str, str], None, None]:
        if self.base_path is None or not self.languages_path.exists():
            return
        for language in self.languages_path.iterdir():
            if language.is_file() and language.suffix.lower() == '.isl':
                yield {'name': language.stem,
                       'messages_file': 'compiler:' + str(language.relative_to(self.base_path))
                       }

    def build(self, installer: Installer, output_path: Union[str, pathlib.Path] = pathlib.Path.cwd() / "installer.exe") -> None:
        """This method compiles the given installer"""
        with tempfile.TemporaryDirectory() as tmpdir:
            installer_path = pathlib.Path(tmpdir) / "installer.iss"
            installer_text = installer.render(self)
            installer_path.write_text(installer_text)
            subprocess.check_call(
                [str(self.compiler_path), '/Qp', '/O' + str(output_path), str(installer_path)])
