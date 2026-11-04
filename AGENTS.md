# Project Structure & Module Organization
## Source Code
## Tests
## Assets

	## Project Structure
	### Source Code
	### Tests
	### Assets
	### Commit Messages
	### Pull Requests

- List key commands for building, testing, and running locally (e.g., npm test, make build).
- Briefly explain what each command does.

	- npm test
	- make build

- Specify indentation rules, language-specific style preferences, and naming patterns.
- Include any formatting or linting tools used.

	# Indentation Rules
	# Language-Specific Style Preferences
	# Naming Patterns

- Identify testing frameworks and coverage requirements.
- State test naming conventions and how to run tests.

	## Testing Frameworks
	### Coverage Requirements
	### Test Naming Conventions
	### Running Tests

- Summarize commit message conventions found in the project’s Git history.
- Outline pull request requirements (descriptions, linked issues, screenshots, etc.).

	- ## Commit Messages
	- ## Pull Requests


---

# Additional Agent Operating Rules

The rules below supplement the existing contents of this file. They are additive and do not remove or weaken existing instructions.

## 1. Evidence Over Assumption

**Do not invent facts.** If information is not confirmed by the repository, current task, tool output, documentation, test results, or explicit user input, treat it as unknown.

Do not invent file contents, command output, APIs, requirements, configuration, test results, repository state, successful execution, or security properties.

Use these distinctions when reporting:

- **Confirmed:** directly observed.
- **Verified:** tested or independently checked.
- **Inferred:** logically derived but not directly confirmed.
- **Unknown:** insufficient evidence.
- **Blocked:** required information is unavailable.

Never present an inference as a confirmed fact.

## 2. Read-Only Audit First

Before modifying anything, perform a read-only audit of the relevant project area. The initial pass must not mutate repository state.

Inspect the relevant structure, implementation, project instructions, configuration, version information, tests, scripts, entry points, and Git state when relevant.

Do not begin implementation until the existing state is sufficiently understood. If a material ambiguity is discovered, stop and identify it before proceeding.

## 3. Preserve Existing CLI Behavior

Make the smallest responsible change that fully satisfies the request.

Do not automatically refactor, rewrite, rename, reorganize, optimize, redesign, replace dependencies, remove functionality, or change behavior outside the requested scope.

The existing CLI interface, flags, output behavior, dispatch architecture, module boundaries, and platform-specific behavior are presumed intentional unless the repository or user explicitly establishes otherwise.

## 4. No Fabricated Completion

Never claim an action occurred unless it actually occurred and the result was observed.

Do not claim tests passed, a command succeeded, documentation was updated, a version changed, or a Git operation succeeded unless that result was actually verified.

If validation cannot be performed, state that explicitly.

## 5. Platform and Permission Behavior

showMeEverything may inspect platform-specific filesystems and environments. Do not assume that an existing path is accessible.

When behavior differs because of permissions, operating-system restrictions, Termux limitations, missing commands, or unavailable resources, report the observed behavior rather than inventing results or silently changing the intended behavior.

## 6. Post-Change Verification

After editing:

1. Inspect the resulting diff.
2. Check for unintended changes.
3. Run the most relevant available validation.
4. Verify the requested behavior when practical.
5. Report failures and unverified areas honestly.

## 7. Ambiguity and Intent

Do not silently reinterpret an ambiguous request. If multiple interpretations would materially change the implementation, stop and ask for clarification.

Authorization to complete a task does not authorize unrelated changes.

## 8. Git Safety

Do not reset user work, discard uncommitted changes, rewrite history, force-push, rebase, amend commits, delete branches, or delete files unless the user explicitly requests the specific operation.

Never claim a Git operation succeeded without observing its result.

## 9. Completion Report

When the task is complete, report what changed, files changed, what was verified, what was not verified, known remaining issues, and relevant Git state when inspected.

Task completion means the requested work was implemented and the available evidence supports the result. Editing files alone is not proof of completion.


## Additional AI Agent Requirements: Packaging, Help, and User Documentation

Apply the Cross-Platform Packaging and User Documentation Contract below to this repository. For software products, this contract governs every supported distribution method. For templates and packaging-tool repositories, preserve the same requirements in generated project guidance and template output.



---

# Cross-Platform Packaging and User Documentation Contract

These requirements are additive. They supplement existing project-specific instructions and do not replace, weaken, or silently reinterpret them.

## 1. One product, one installation contract

Every supported distribution format for the same software MUST deliver an equivalent, complete product installation.

This requirement applies to every format the project supports, including as applicable:

- Python source distributions, wheels, and supported Python installers;
- Termux packages and Termux YAML manifests;
- Debian packages and APT repositories;
- Arch Linux packages and PKGBUILD-based builds;
- RPM packages;
- Alpine packages;
- AppImage and other portable Linux bundles;
- Windows installers and portable distributions;
- macOS application bundles, disk images, and installers;
- source builds and other project-supported installation paths.

A project is not required to support every format. The project MUST clearly identify which formats are supported, experimental, planned, or unsupported. However, once a format is declared supported, it MUST satisfy this contract.

The installation format is a delivery mechanism, not a separate product definition. Users MUST NOT receive materially different application capabilities, command interfaces, configuration behavior, or required resources merely because they selected a different package format.

## 2. Canonical release payload

Each product MUST define one canonical release payload or an equivalent machine-verifiable payload specification. Every supported packaging backend MUST derive its installed file set from that specification or from a demonstrably equivalent source of truth.

The specification MUST identify, as applicable:

- executable binaries and application entry points;
- Python modules, libraries, plugins, and runtime resources;
- GUI assets, icons, desktop entries, MIME definitions, and application metadata;
- default configuration files and configuration schema;
- templates, migrations, schemas, certificates, and other required data files;
- shell completion files and command aliases;
- man pages and other user manuals;
- usage examples and reference documentation;
- license, copyright, and third-party notices;
- changelog and release information;
- service definitions, integration files, and platform-specific support resources;
- uninstall metadata or other information required for safe removal.

Every packaging backend MUST install all files required for the software to function as documented. It MUST NOT omit a required resource merely because a packaging format or build script has a separate implementation.

Documentation may be installed in platform-appropriate locations, and platform-specific executable artifacts may differ. The logical documentation set and user-visible product capabilities MUST remain equivalent. A format-specific omission MUST be explicitly justified and documented.

## 3. Installation behavior parity

Every supported installer MUST implement the same product-level lifecycle contract:

- install the product and its required runtime resources;
- expose the documented commands, launchers, APIs, and interfaces;
- install or generate the same documented default configuration;
- preserve user configuration and user data during upgrades unless a documented migration explicitly requires otherwise;
- perform required configuration or data migrations safely and transparently;
- establish required permissions and platform integrations;
- report actionable errors when prerequisites or permissions are missing;
- support the documented upgrade and repair behavior;
- remove product-owned files during uninstall without deleting user data or unrelated files;
- provide an accurate installed-version and installation-location result where the platform supports it.

Package managers may own their native transaction, dependency, and uninstall mechanics. Product-specific scripts MUST NOT fight those mechanisms or perform surprising side effects.

Installing through a Python installer, Termux, APT/DEB, Arch, RPM, AppImage, Windows, macOS, or source installation MUST NOT result in different required application files, documentation, default behavior, command capabilities, or configuration semantics.

## 4. Platform-specific differences

Platform differences are allowed only when required by the operating system, runtime, package ecosystem, filesystem layout, security model, or user interaction conventions.

Examples include executable formats, filesystem destinations, service managers, desktop integration, permissions, signing, application bundle layout, dependency declarations, and platform-native launchers.

Every such difference MUST be:

1. identified in the packaging documentation;
2. limited to the platform-specific implementation detail;
3. tested or validated on the relevant platform when practical; and
4. prevented from changing the product-level contract without an explicit product decision.

Do not claim that two package formats are equivalent merely because both build successfully.

## 5. Packaging metadata, build scripts, and installers

All package metadata, manifests, build scripts, installer scripts, release workflows, and backend adapters MUST describe or produce the same canonical product payload.

Contributors and agents MUST inspect every supported packaging path when changing:

- application entry points or command names;
- modules, resources, plugins, assets, or runtime dependencies;
- default or user configuration;
- documentation or man pages;
- permissions, services, desktop integration, or filesystem paths;
- version metadata or release contents;
- installation, upgrade, repair, or uninstall behavior.

Do not independently add a file to one package format while omitting it from another supported format. Do not maintain conflicting versions of product metadata when a canonical source or generated manifest can be used.

Build scripts MUST distinguish building from installing. Building a package MUST NOT silently install it on the host, modify active system prefixes, publish a release, or perform unrelated destructive operations.

Generated metadata and package artifacts MUST be reproducible to the extent supported by the toolchain. Validation MUST distinguish metadata validation, mocked backend tests, native package builds, payload inspection, and actual installation tests. Passing one category MUST NOT be reported as proof of another.

## 6. Required packaging parity validation

For each supported format, maintain an auditable mapping between the canonical release payload and the package's installed filesystem contents.

Where practical, automate checks that compare:

- required paths and file presence;
- executable names and entry points;
- application version metadata;
- configuration defaults and schema;
- man pages and user documentation;
- icons, desktop entries, plugins, templates, and runtime data;
- dependency declarations and runtime requirements;
- uninstall ownership and preservation of user data.

A parity check MUST fail when a required payload item is missing from a supported package. Differences that are intentionally platform-specific MUST be enumerated as explicit exceptions rather than hidden through broad exclusions.

At least one clean installation test SHOULD be maintained for each supported package family and platform. Tests MUST verify actual installed behavior where feasible, not only inspect package metadata.

## 7. User manuals and man pages are required deliverables

Every user-facing software product MUST provide useful operating documentation appropriate to its interfaces. Documentation is part of the product, not an optional development extra.

For command-line applications, provide:

- a man page for the primary command;
- man pages for additional major commands when their interfaces warrant separate references;
- complete command and option reference documentation;
- examples of common and advanced workflows;
- help for applicable subcommands;
- installation, configuration, troubleshooting, and uninstall instructions.

For GUI applications, provide a user manual covering the interface, workflows, settings, dialogs, menus, shortcuts, supported file formats, error recovery, and relevant integration behavior.

For APIs, libraries, services, and automation tools, provide API or function references, configuration documentation, request/response or function examples, lifecycle information, and operational guidance appropriate to the actual public interface.

The manuals MUST be written for users and operators who did not develop the software. Use professional, neutral product documentation language. Do not address an individual maintainer, refer to private conversations, narrate how an AI agent wrote the code, or assume that the reader already knows the implementation.

Documentation MUST describe observed, implemented behavior. Clearly identify unsupported, experimental, optional, or platform-limited behavior.

## 8. Configuration documentation requirements

Every user-editable configuration file, environment variable, command-line setting, or remotely configurable option MUST be documented.

For each setting, document:

- exact key or option name;
- purpose and effect;
- data type;
- default value, or explicitly state that no default exists;
- accepted values, ranges, and format;
- whether the setting is required or optional;
- where the setting is read and how it is applied;
- precedence when multiple configuration sources exist;
- interactions or dependencies with other settings;
- validation rules and behavior for invalid values;
- a working example;
- whether a restart, reload, regeneration, or migration is required.

For structured configuration systems such as TOML, YAML, JSON, INI, or project-specific manifests, include a complete annotated example and explain every section and field. Do not document only the obvious settings while leaving nested or less common sections unexplained.

When configuration behavior is non-obvious, document the exact syntax and operational sequence. For example, a synchronization section must explain its supported targets, source and destination semantics, mapping rules, direction, conflict behavior, validation, and how a user can verify that synchronization occurred, but only to the extent those behaviors are confirmed by the implementation.

## 9. CLI and command help requirements

Every CLI MUST expose a discoverable general help interface, conventionally through `--help` and, where appropriate, `-h` or a `help` command.

Every command MUST communicate its purpose, syntax, arguments, options, defaults, accepted values, and relevant examples. Nested command systems MUST provide help for applicable subcommands, including a way to discover available subcommands without executing them.

Help output MUST:

- be accurate and generated from, or validated against, the actual command parser and implementation;
- include common usage examples;
- identify required and optional arguments;
- explain defaults and environment/configuration interactions;
- avoid exposing secrets or private implementation details;
- return useful output without performing the requested operation;
- use clear, user-facing language and actionable error messages.

If a command genuinely has no meaningful subcommands or no applicable secondary help surface, document why. Do not omit help merely for implementation convenience.

GUI applications and APIs MUST provide equivalent discoverability through their user manual, built-in help/about surfaces, API reference, or other appropriate interface documentation.

## 10. Documentation validation and release inclusion

Documentation must be checked as part of release validation.

For each supported package, verify that the applicable manuals, man pages, configuration references, examples, licenses, and notices are present in the installed payload and accessible at documented locations.

Man pages MUST use the correct section and platform installation conventions. Their source files MUST remain maintained alongside the implementation. Package build scripts MUST include them in the resulting artifact.

When a command, option, configuration key, API, UI action, installer, package format, or lifecycle behavior changes, update every affected user-facing reference in the same change set.

Do not leave examples, help output, or manuals describing removed or nonexistent behavior.

## 11. Contribution requirements for packaging changes

Any contribution that changes packaging, build metadata, release payloads, installers, installation paths, runtime dependencies, or uninstall behavior MUST:

1. inspect the canonical release payload specification;
2. inspect all supported package formats and their build/install scripts;
3. explain the intended behavior and any platform exceptions;
4. update all affected metadata and package definitions;
5. update user and maintainer documentation;
6. update or add payload parity and lifecycle tests where practical;
7. validate each affected package backend;
8. report which package formats were actually built and which were actually installed and tested.

A pull request MUST NOT be marked complete based solely on one successful package build when other supported formats may be affected.

## 12. AI agent enforcement

AI agents MUST treat this contract as a release requirement.

Before changing packaging, they MUST perform a read-only audit of all relevant package formats, metadata, build scripts, installer/uninstaller scripts, documentation payloads, and tests.

Agents MUST preserve existing files and behavior outside the explicit task scope. They MUST NOT delete, rewrite, reorganize, rename, or replace unrelated files or sections.

When a requested change cannot be applied consistently across supported formats, agents MUST identify the exact mismatch and either complete the consistent change or report the specific blocker. They MUST NOT silently update only the easiest backend.

Agents MUST NOT invent supported package formats, installation behavior, configuration semantics, commands, manual content, or validation results.

## Project-specific documentation standards

Before changing project behavior, packaging, interfaces, configuration, or release documentation, read [docs/PROJECT_STANDARDS.md](docs/PROJECT_STANDARDS.md) and keep it aligned with the actual implementation. These standards supplement this file and do not authorize unrelated changes.
