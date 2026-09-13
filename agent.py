from rich import print
from typing import Dict
from pathlib import Path

def generate_contributor_guide():
	content = ""
	agent_dict: Dict[str, str] = {
		"project_structure": "# Project Structure & Module Organization\n## Source Code\n## Tests\n## Assets",
		"build_test_dev_commands": "- List key commands for building, testing, and running locally (e.g., npm test, make build).\n- Briefly explain what each command does.",
		"coding_style_naming_conventions": "- Specify indentation rules, language-specific style preferences, and naming patterns.\n- Include any formatting or linting tools used.",
		"testing_guidelines": "- Identify testing frameworks and coverage requirements.\n- State test naming conventions and how to run tests.",
		"commit_pull_request_guidelines": "- Summarize commit message conventions found in the project’s Git history.\n- Outline pull request requirements (descriptions, linked issues, screenshots, etc.).",
	}

	
	for key, value in agent_dict.items():
		if key == "project_structure":
			content += value + "\n\n"
			content += f"\t## Project Structure\n\t### Source Code\n\t### Tests\n\t### Assets\n\t### Commit Messages\n\t### Pull Requests\n\n"
		elif key == "build_test_dev_commands":
			content += value + "\n\n"
			content += "\t- npm test\n\t- make build\n\n"
		elif key == "coding_style_naming_conventions":
			content += value + "\n\n"
			content += "\t# Indentation Rules\n\t# Language-Specific Style Preferences\n\t# Naming Patterns\n\n"
		elif key == "testing_guidelines":
			content += value + "\n\n"
			content += "\t## Testing Frameworks\n\t### Coverage Requirements\n\t### Test Naming Conventions\n\t### Running Tests\n\n"
		elif key == "commit_pull_request_guidelines":
			content += value + "\n\n"
			content += "\t- ## Commit Messages\n\t- ## Pull Requests\n"

	# Create a file named AGENTS.md with the generated content
	Path("AGENTS.md").write_text(content)

# Call the function to generate and save the Markdown text
generate_contributor_guide()

