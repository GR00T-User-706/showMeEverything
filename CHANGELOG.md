# Changelog

All notable changes to **showMeEverything** are documented here.

The package version is maintained in the repository-root `VERSION` file. That file is the single source of truth for the package version; version values in release artifacts and package metadata must be derived from it.

This changelog begins with the repository state at version `3.1.0`. Earlier history is intentionally not reconstructed.

## [3.1.0] - 2026-10-24

### Added
- Independent multi-term searches across the CLI and GUI interfaces.
- Termux package build and update support.
- Termux launcher support for the Python CLI implementation.
- SemVer Forge initialization metadata, including the root `VERSION` file and `.semver-forge.toml`.

### Changed
- Updated Termux update-script executable permissions.
- Established the root `VERSION` file as the canonical package-version source.

### Notes
- This entry records the project state at the changelog's starting point. It is not intended to imply that every listed change was introduced on this date.
- Future entries should document changes introduced by their corresponding release or development increment.
