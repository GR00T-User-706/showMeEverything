# showMeEverything Project Standards

These standards describe the current project as a personal Linux system-probing and search tool that is being productized gradually. They supplement `AGENTS.md`, the README, the technical documentation, and the actual installer and CLI behavior.

## Product identity and maturity

The original CLI is the primary product and must remain intact. Treat this repository as an actively developed personal project and playground, not as an already mature, universally supported distribution.

Do not imply that every Linux distribution, package manager, desktop environment, shell, or installation method is supported merely because related code, metadata, or examples exist. State only support demonstrated by the current implementation and verified installation/testing records.

The current installer has a limited supported system scope. Do not broaden that claim or describe it as a universal Linux installer. If the exact supported OS release or host configuration is not recorded in verified project documentation, mark it as needing maintainer confirmation rather than inventing a value.

## Interfaces and components

- Treat the original CLI as the core interface.
- Document the Zsh implementation and Python implementation separately wherever their behavior differs.
- Treat GUI frontends as optional interfaces with their own prerequisites and limitations.
- Do not imply a GUI can replace, bundle, or independently operate without its documented CLI/backend dependency.
- Keep shell compatibility claims tied to actual sourcing and execution behavior.

## CLI reference

Document every implemented flag, argument, combination rule, output mode, exit status, and example against the actual CLI. Explain which flags stack, which modes conflict, and how `--pipe` affects stdout/stderr. Distinguish machine-readable output from human-oriented output. Include safe examples and explicit warnings for operations that can expose large system inventories or produce dangerous command pipelines.

## Installation and distribution

Document the existing installer exactly as it behaves today: prerequisites, supported host scope, privileges, files installed, destinations, symlinks, desktop integration, build attempts, failure handling, rerun behavior, and uninstall behavior. Do not silently change its behavior through documentation assumptions.

Keep any package format marked as supported only when its build and install path is actually maintained and tested. A packaging directory, recipe, archived artifact, or manifest is not proof of a supported release channel.

## Search and privacy behavior

Describe which filesystem locations and system interfaces are inspected, what user scope is used, what privileges are needed, and where diagnostics are written. Document data written to disk, log contents, and output-stream guarantees. Avoid absolute privacy or safety claims unless the implementation proves them.

## Productization discipline

Move toward external usability through accurate documentation and explicit support boundaries. Do not force a premature multi-platform architecture, replace the original CLI, or make unrelated design changes. Future productization should be incremental and evidence-led.

## Documentation-only changes

Documentation changes do not alter the CLI's version or installer behavior. Record documentation additions in the changelog without implying that support, compatibility, or functionality has expanded.
