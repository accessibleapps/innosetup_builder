# Inno Setup Builder - Missing Features

This document provides a comprehensive list of all missing features based on analysis of the Inno Setup documentation versus current implementation.

## Current Implementation Status

The library currently supports:
- ✅ **[Setup]** - Basic configuration (app name, version, compression, etc.)
- ✅ **[Types]** - Installation types with ComponentType class
- ✅ **[Components]** - Installation components with Component class
- ✅ **[Files]** - File installation with FileEntry class (comprehensive)
- ✅ **[Dirs]** - Directory creation with DirEntry class
- ✅ **[Registry]** - Registry management with RegistryEntry class
- ✅ **[Languages]** - Multi-language support (basic)
- ✅ **[Icons]** - Basic icon creation (hardcoded)
- ✅ **[Tasks]** - Basic task support (hardcoded for desktop icon/startup)
- ✅ **[Run]** - Post-installation execution with RunEntry class
- ✅ **[UninstallRun]** - Pre-uninstall execution with UninstallRunEntry class

## Missing Features

### **Missing Core Sections**

#### **[INI] Section**
- Create/modify INI file entries
- Support for all INI value types
- Section and key management
- Uninstallation cleanup of INI entries
- Encoding support for INI files

#### **[Messages] Section**
- Override default installer messages
- Custom error messages
- Localized message overrides
- Message parameters and formatting
- Context-sensitive help text

#### **[CustomMessages] Section**
- User-defined messages for templates
- Parameterized message support
- Multi-language custom messages
- Message inheritance and overrides
- Dynamic message generation

#### **[InstallDelete] Section**
- Delete files/directories before installation
- Wildcard pattern support
- Recursive directory deletion
- Conditional deletion based on flags
- Version-based file cleanup

#### **[UninstallDelete] Section**
- Delete additional files during uninstallation
- Clean up user-generated content
- Log file cleanup
- Configuration file removal
- Temporary file cleanup

#### **[LangOptions] Section**
- Language-specific font settings
- Text direction (RTL/LTR) support
- Language-specific UI options
- Custom language configurations
- Font fallback options

#### **[Code] Section**
- Pascal scripting support
- Event function definitions
- Custom installation logic
- User input validation
- Dynamic configuration generation
- Custom wizard pages
- Runtime condition checking

### **Missing Advanced Features**

#### **Enhanced [Setup] Section Parameters**

**Digital Signing Configuration:**
- SignTool configuration
- SignedUninstaller support
- SignToolMinimumTimeBetween
- SignToolRetryCount
- SignToolRetryDelay
- SignToolRunMinimized

**Advanced Compression Settings:**
- LZMAAlgorithm options
- LZMABlockSize configuration
- LZMADictionarySize settings
- LZMAMatchFinder options
- LZMANumBlockThreads
- LZMANumFastBytes
- LZMAUseSeparateProcess
- CompressionThreads

**Security and Privileges:**
- PrivilegesRequired configuration
- PrivilegesRequiredOverridesAllowed
- ArchitecturesAllowed
- ArchitecturesInstallIn64BitMode
- MinVersion requirements
- OnlyBelowVersion restrictions

**UI Customization:**
- WizardImageFile support
- WizardSmallImageFile
- WizardImageBackColor
- WizardImageAlphaFormat
- WizardImageStretch
- WizardSizePercent
- WizardResizable
- WindowShowCaption
- WindowStartMaximized
- WindowResizable
- WindowVisible

**Installation Behavior:**
- SetupLogging configuration
- UninstallLogging
- UninstallLogMode
- RestartIfNeededByRun
- RestartApplications
- CloseApplications
- CloseApplicationsFilter
- AlwaysRestart
- SetupMutex
- AppMutex

**Version Information:**
- VersionInfoCompany
- VersionInfoCopyright
- VersionInfoDescription
- VersionInfoOriginalFileName
- VersionInfoProductName
- VersionInfoProductTextVersion
- VersionInfoProductVersion
- VersionInfoTextVersion
- VersionInfoVersion

**Advanced Installation Control:**
- DisableStartupPrompt
- DisableWelcomePage
- DisableReadyPage
- DisableFinishedPage
- DisableDirPage
- DisableProgramGroupPage
- DisableReadyMemo
- FlatComponentsList
- ShowComponentSizes
- AlwaysShowComponentsList
- AlwaysShowDirOnReadyPage
- AlwaysShowGroupOnReadyPage

#### **Flexible [Icons] Section**
- IconEntry class for custom icon definitions
- Command line parameters for shortcuts
- Working directory specification
- Hot key assignments
- Icon file and index selection
- Shortcut flags (runmaximized, runminimized, preventpinning)
- Internet shortcuts (URL support)
- Conditional icon creation
- Icon permissions and attributes

#### **Flexible [Tasks] Section**
- TaskEntry class for custom task definitions
- Hierarchical task structure support
- Task groups and descriptions
- Mutually exclusive tasks
- Task dependencies
- Conditional task availability
- Custom task flags
- Task-specific UI elements

#### **Advanced File Features**
Missing FileEntry parameters:
- CopyMode specification
- OnlyBelowVersion checking
- MinVersion requirements
- Check conditions
- BeforeInstall/AfterInstall events
- SourceDir overrides
- Languages parameter
- Tasks parameter

#### **Service Installation Support**
- Windows service installation
- Service configuration parameters
- Service dependencies
- Service startup types
- Service accounts and permissions
- Service description and display names
- Service failure actions
- Service recovery options

#### **Architecture and Platform Support**
- Enhanced 32/64-bit handling
- ARM architecture support
- Platform-specific installations
- Processor architecture detection
- Compatibility checking
- Cross-platform file selection

### **Missing Utility Features**

#### **Disk Spanning Support**
- Multi-disk installation creation
- DiskSpanning configuration
- SlicesPerDisk settings
- DiskSliceSize specification
- DiskClusterSize optimization

#### **Encryption Support**
- File encryption during installation
- Password protection
- Encryption algorithm selection
- Key management

#### **Network Installation Features**
- UNC path support improvements
- Network drive handling
- Remote installation capabilities
- Download functionality integration

#### **Validation and Checking**
- Input validation functions
- File integrity checking
- Digital signature verification
- Checksum validation
- Version compatibility checking

#### **Advanced Registry Features**
Missing registry capabilities:
- Registry key permissions (detailed ACL)
- Registry key backup/restore
- Registry key linking
- Registry virtualization control

#### **Custom Installation Types**
- Installation type customization beyond basic types
- Type-specific component selection
- Dynamic type creation
- Type inheritance and overrides

#### **Advanced Language Support**
- Language detection methods
- Fallback language handling
- Mixed-language installations
- Dynamic language switching
- Custom language files

#### **Development and Debugging Features**
- Debug logging capabilities
- Installation progress callbacks
- Error handling customization
- Rollback functionality
- Installation state tracking

#### **Integration Features**
- MSI product code integration
- Windows Installer interoperability
- Package management integration
- Update/patch installation support
- Dependency management

### **Missing Documentation Features**
- Comprehensive parameter documentation
- Best practices guide
- Migration guides
- Performance optimization guide
- Troubleshooting documentation
- Example gallery expansion

---

**Note:** This list represents a comprehensive analysis of Inno Setup capabilities versus current implementation. Features are listed without prioritization to provide a complete overview of potential enhancements.