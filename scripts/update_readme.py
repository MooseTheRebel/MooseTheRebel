#!/usr/bin/env python3
"""Regenerate the README's contributions section from contributions.toml."""

import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOML_PATH = REPO_ROOT / "contributions.toml"
README_PATH = REPO_ROOT / "README.md"

START_MARKER = "<!-- CONTRIBUTIONS:START -->"
END_MARKER = "<!-- CONTRIBUTIONS:END -->"


def render_entry(entry: dict) -> str:
    tags = " ".join(f"`{tag}`" for tag in entry.get("tags", []))
    line = f"- **[{entry['project']}]({entry['url']})** — {entry['description']}"
    line += f" ([details]({entry['link']}))"
    line += f" · {entry['date']}"
    if tags:
        line += f" · {tags}"
    return line


def render_section(entries: list[dict]) -> str:
    entries_sorted = sorted(entries, key=lambda e: e["date"], reverse=True)
    body = "\n".join(render_entry(e) for e in entries_sorted)
    return f"{START_MARKER}\n## 🌟 Recent Contributions\n\n{body}\n{END_MARKER}"


def update_readme(readme_text: str, section: str) -> str:
    if START_MARKER in readme_text and END_MARKER in readme_text:
        start = readme_text.index(START_MARKER)
        end = readme_text.index(END_MARKER) + len(END_MARKER)
        return readme_text[:start] + section + readme_text[end:]
    separator = "\n\n" if readme_text and not readme_text.endswith("\n\n") else ""
    return readme_text.rstrip("\n") + "\n" + separator + section + "\n"


def main() -> None:
    with TOML_PATH.open("rb") as f:
        data = tomllib.load(f)

    section = render_section(data.get("contribution", []))
    readme_text = README_PATH.read_text()
    README_PATH.write_text(update_readme(readme_text, section))


if __name__ == "__main__":
    main()
