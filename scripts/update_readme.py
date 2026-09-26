#!/usr/bin/env python3
"""Regenerate the README's contributions section from contributions.toml."""

import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOML_PATH = REPO_ROOT / "contributions.toml"
README_PATH = REPO_ROOT / "README.md"

START_MARKER = "<!-- CONTRIBUTIONS:START -->"
END_MARKER = "<!-- CONTRIBUTIONS:END -->"

CATEGORY_EMOJI = {
    "Rust": "🦀",
    "Python": "🐍",
    "TypeScript": "🟦",
    "JavaScript": "💛",
    "Go": "🐹",
    "CI": "⚙️",
    "Docker": "🐳",
}
DEFAULT_EMOJI = "✨"


def category_emoji(category: str) -> str:
    return CATEGORY_EMOJI.get(category, DEFAULT_EMOJI)


def render_entry(entry: dict) -> str:
    line = f"- **[{entry['project']}]({entry['url']})** — {entry['description']}"
    line += f" ([details]({entry['link']}))"
    line += f" · {entry['date']}"
    return line


def render_section(entries: list[dict]) -> str:
    entries_sorted = sorted(entries, key=lambda e: e["date"], reverse=True)

    categories: dict[str, list[dict]] = {}
    for entry in entries_sorted:
        categories.setdefault(entry["category"], []).append(entry)

    # Fixed category order (matches CATEGORY_EMOJI), so the section order
    # doesn't shift as new entries are added. Unlisted categories are
    # appended alphabetically at the end.
    category_rank = {cat: i for i, cat in enumerate(CATEGORY_EMOJI)}
    ordered_categories = sorted(
        categories,
        key=lambda cat: (category_rank.get(cat, len(category_rank)), cat),
    )

    groups = []
    for category in ordered_categories:
        emoji = category_emoji(category)
        bullets = "\n".join(render_entry(e) for e in categories[category])
        groups.append(f"### {emoji} {category}\n\n{bullets}")

    body = "\n\n".join(groups)
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
