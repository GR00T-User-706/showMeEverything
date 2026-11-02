# Changelog

All notable changes to **showMeEverything** are documented here.

The repository-root VERSION file is the single source of truth for package versions.
Release manifests and package metadata must stay synchronized with it.

## [3.3.0] - 2026-11-02

### Added
- Multi-package-manager detection and search across every detected supported backend: Pacman, APT/dpkg, DNF, Zypper/RPM, and APK.
- Persistent package-manager diagnostics containing manager, operation, search term, command, exit status, and captured stderr.
- SME_ERROR_LOG override and XDG state-directory default for the diagnostic log.
- Normal-mode diagnostic log-path notification while keeping --pipe stdout and stderr free of backend diagnostics.

### Changed
- Replaced first-match package-manager selection with multi-manager dispatch in the Zsh and Python CLI implementations.
- Implemented the previously empty Python DNF, Zypper, and APK search adapters.
- Synchronized Termux and Arch package metadata with VERSION 3.3.0.

## [3.2.0]

### Features
- finalized the multisearch engine (f7e2851c)

### Documentation
- add changelog starting at version 3.1.0 (ab44f571)
- added the semver-forge init generated VERSION and .semver-forge.toml (9aa2482e)
- strengthen agent operating rules (d062269b)

### Maintenance
- housekeepih deleted old package version 3.0.3 (115aade5)

## [3.1.0] - 2026-10-24

### Added
- Independent multi-term searches across the CLI and GUI interfaces.
- Termux package build and update support.
- Termux launcher support for the Python CLI implementation.
- SemVer Forge initialization metadata, including the root VERSION file and .semver-forge.toml.

### Changed
- Updated Termux update-script executable permissions.
- Established the root VERSION file as the canonical package-version source.

### Notes
- This entry records the project state at the changelog's starting point. It is not intended to imply that every listed change was introduced on this date.
- Future entries should document changes introduced by their corresponding release or development increment.
