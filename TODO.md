# Inno Setup Builder - Feature Roadmap

This document outlines the planned features and improvements for the Inno Setup Builder library, prioritized by importance and complexity.

## Current Implementation Status

The library currently supports:
- ✅ Basic Setup section configuration (app name, version, directories)
- ✅ Files section with source/destination mapping
- ✅ Simple Icons section for Start Menu shortcuts
- ✅ Multi-language support
- ✅ Desktop icon and startup options
- ✅ Registry-based Inno Setup installation detection
- ✅ Template-based .iss file generation
- ✅ Registry Section Support (full implementation)
- ✅ Run Section Support (Run and UninstallRun)
- ✅ Advanced File Flags (all parameters and flags)
- ✅ Dirs Section Support (directory creation with attributes)

## High Priority Features (Completed)

### 1. Registry Section Support ✅
**Priority: High** | **Complexity: Medium** | **Status: COMPLETED**

Implemented comprehensive registry manipulation capabilities:
- Registry key creation/modification/deletion
- Support for all data types (string, dword, qword, binary, multisz, expandsz)
- Uninstall cleanup flags (uninsdeletekey, uninsdeletevalue, uninsdeletekeyifempty)
- Permissions and access control
- 32-bit/64-bit registry view support

### 2. Run Section Support ✅
**Priority: High** | **Complexity: Medium** | **Status: COMPLETED**

Implemented post-installation program execution:
- Execute programs after installation completes
- Support for parameters, working directories, status messages
- Execution flags (postinstall, nowait, shellexec, runhidden, etc.)
- UninstallRun section for uninstallation tasks
- Conditional execution based on user choices

### 3. Advanced File Flags ✅
**Priority: High** | **Complexity: High** | **Status: COMPLETED**

Implemented expanded file handling capabilities:
- Version checking and comparison (ignoreversion, replacesameversion)
- File permissions and attributes
- Compression options (nocompression, solidbreak)
- Shared file management (sharedfile, regserver, regtypelib)
- Font installation support
- Digital signing flags
- Conditional file installation

## Medium Priority Features

### 4. Dirs Section Support ✅
**Priority: Medium** | **Complexity: Low** | **Status: COMPLETED**

Implemented directory creation with advanced options:
- Directory creation with permissions
- Attributes (hidden, system, readonly)
- NTFS compression support
- Uninstall behavior control

**Implementation Details:**
- Created `DirEntry` class with name, permissions, attribs, and flags fields
- Added dirs list to `Installer` class
- Extended template with `[Dirs]` section
- Full test coverage in test_dirs.py

### 5. Components Support ✅
**Priority: Medium** | **Complexity: High** | **Status: COMPLETED**

Implemented modular installation options:
- Selectable installation components
- Component hierarchies (parent/child relationships)
- Installation types (full, compact, custom)
- Component-specific file/registry/run entries
- Mutual exclusion and dependencies

**Implementation Details:**
- Created `Component` and `ComponentType` classes
- Added components parameter to all entry types (FileEntry, DirEntry, RegistryEntry, RunEntry, UninstallRunEntry)
- Added Types and Components sections to template
- Full support for boolean expressions in components
- Complete test coverage in test_components.py

### 6. Setup Section Expansion
**Priority: Medium** | **Complexity: Medium**

Add comprehensive installer configuration:
- Licensing (LicenseFile, InfoBeforeFile, InfoAfterFile)
- Compression settings (Compression, SolidCompression, InternalCompressLevel)
- Version information fields
- Digital signing configuration
- Wizard appearance customization
- Administrative privileges control

**Implementation Notes:**
- Extend `Installer` class with additional setup fields
- Update template with conditional setup directives

### 7. Icons Section Enhancement
**Priority: Medium** | **Complexity: Low**

Improve shortcut creation capabilities:
- Command line parameters for shortcuts
- Working directory specification
- Hot key assignments
- Icon file and index selection
- Advanced shortcut flags (runmaximized, preventpinning)
- Internet shortcuts (URL support)

**Implementation Notes:**
- Extend existing icon functionality in template
- Add IconEntry class with full parameter support

## Lower Priority Features

### 8. Conditional Installation
**Priority: Low** | **Complexity: Medium**

Add platform and condition-based installation:
- Check parameter for all sections
- Platform detection (IsWin64, processor architecture)
- Custom condition functions
- Version-based installation logic

### 9. Code Section Support  
**Priority: Low** | **Complexity: High**

Enable Pascal scripting for advanced scenarios:
- Custom installation logic
- User input validation
- Dynamic configuration
- Event handling (InitializeSetup, NextButtonClick, etc.)

### 10. Digital Signing Support
**Priority: Low** | **Complexity: Medium**

Add code signing capabilities:
- SignTool configuration
- File signing during compilation
- Installer signing
- Certificate management

## Implementation Guidelines

### Development Approach
1. **Incremental Development**: Implement features one at a time with full testing
2. **Backward Compatibility**: Ensure existing code continues to work
3. **Template Extension**: Extend Jinja2 template systematically
4. **Class Design**: Use attrs dataclasses for consistent API
5. **Documentation**: Update README and examples for each feature

### Testing Strategy
- Unit tests for each new class and method
- Integration tests with actual Inno Setup compilation
- Example scripts demonstrating new features
- Cross-platform testing (Windows focus, graceful degradation elsewhere)

### API Design Principles
- Follow existing patterns (attrs classes, Factory defaults)
- Use descriptive parameter names matching Inno Setup documentation
- Provide sensible defaults for optional parameters
- Include comprehensive docstrings with examples

## Future Considerations

### Advanced Features for Later Versions
- MSI product code integration
- Patch/update installation support
- Multi-disk spanning
- Custom wizard pages
- Plugin system for extensions
- GUI builder interface

### Performance Optimizations
- Template compilation caching
- Large file handling improvements
- Compression optimization
- Build time reduction

---

**Last Updated:** January 2025
**Next Review:** After completing high-priority features