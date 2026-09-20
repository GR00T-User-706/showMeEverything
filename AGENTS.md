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
