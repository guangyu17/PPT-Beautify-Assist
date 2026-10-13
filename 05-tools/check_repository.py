"""Read-only checks for the maintained source tree; works from a source ZIP too."""
import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRS = ("01-skills", "02-docs", "03-examples", "04-tests", "05-tools")
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".venv", "venv"}


def main():
    errors = []
    files = [p for p in ROOT.iterdir() if p.is_file() and not p.name.startswith(".")]
    directories = [ROOT]
    for name in SOURCE_DIRS:
        directory = ROOT / name
        if not directory.is_dir():
            errors.append(f"Missing source directory: {name}")
            continue
        directories.append(directory)
        for path in directory.rglob("*"):
            if any(part in SKIP_DIRS or part.startswith(".") for part in path.relative_to(ROOT).parts):
                continue
            if path.is_dir():
                directories.append(path)
            elif path.is_file():
                files.append(path)

    for directory in directories:
        if not (directory / "README.md").is_file():
            errors.append(f"Missing README: {directory.relative_to(ROOT)}")

    version = (ROOT / "VERSION").read_text(encoding="utf-8-sig").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append("VERSION must use major.minor.patch")
    skill_text = (ROOT / "01-skills/ppt-beautify-studio/SKILL.md").read_text(encoding="utf-8-sig")
    try:
        frontmatter = yaml.safe_load(skill_text.split("---", 2)[1])
        if frontmatter["metadata"]["version"] != version:
            errors.append("SKILL metadata.version differs from VERSION")
    except (IndexError, KeyError, TypeError, yaml.YAMLError) as exc:
        errors.append(f"Invalid skill version metadata: {exc}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8-sig")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8-sig")
    if f"**当前版本：{version}**" not in readme:
        errors.append("README current version differs from VERSION")
    if not re.search(rf"^## {re.escape(version)}(?:\s|$)", changelog, re.M):
        errors.append("CHANGELOG has no heading for VERSION")

    links = 0
    for path in sorted(files):
        relative = path.relative_to(ROOT)
        if path.suffix not in {".py", ".json", ".yaml", ".yml", ".md"}:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
            if path.suffix == ".py":
                ast.parse(text, filename=str(relative))
            elif path.suffix == ".json":
                json.loads(text)
            elif path.suffix in {".yaml", ".yml"}:
                yaml.safe_load(text)
            else:
                for block in re.findall(r"```json\s*\n(.*?)\n```", text, re.S):
                    json.loads(block)
                prose = re.sub(r"```.*?```", "", text, flags=re.S)
                for target in re.findall(r"\]\(([^)]+)\)", prose):
                    target = target.strip().strip("<>")
                    parsed = urlsplit(target)
                    if parsed.scheme or target.startswith(("#", "//")):
                        continue
                    local = unquote(parsed.path)
                    if local and not (path.parent / local).exists():
                        errors.append(f"Broken link in {relative}: {target}")
                    links += 1
        except (UnicodeError, SyntaxError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{relative}: {exc}")

    for error in errors:
        print(f"ERROR: {error}")
    print(f"Version {version}; {len(files)} source files; {len(directories)} README directories; {links} local links")
    print("PASS" if not errors else f"FAIL: {len(errors)} issue(s)")
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
