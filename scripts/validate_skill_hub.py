#!/usr/bin/env python3
"""Validate the Academic Skill Hub with no mandatory third-party packages."""

from __future__ import annotations

import ast
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".agents" / "skills"
REGISTRY_PATH = ROOT / "skill-registry" / "REGISTRY.md"
REQUIRED_ARS = {
    "ars-deep-research",
    "ars-academic-paper",
    "ars-academic-paper-reviewer",
    "ars-academic-pipeline",
}
REQUIRED_HUB_FILES = {
    ROOT / "skill-registry" / "REGISTRY.md",
    ROOT / "skill-sources" / "SOURCES.md",
    ROOT / "docs" / "SKILL_INTEGRATION_GUIDE.md",
    ROOT / "docs" / "CODEX_SKILL_INTAKE_PROMPT.md",
    ROOT / "scripts" / "validate_skill_hub.py",
}
REGISTRY_FIELDS = [
    "Skill Name",
    "Display Name",
    "Namespace",
    "Local Path",
    "Upstream Source",
    "Upstream Commit",
    "License",
    "Implicit Invocation",
    "Status",
    "Last Validation",
    "Notes",
]
ALLOWED_STATUSES = {"active", "testing", "deprecated", "disabled"}
BANNED_GENERIC_NAMES = {
    "research",
    "writing",
    "review",
    "analysis",
    "paper",
    "statistics",
    "plot",
}
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".py",
    ".js",
    ".ts",
    ".ps1",
    ".sh",
    ".bat",
    ".cmd",
}


class ValidationError(ValueError):
    """Raised when a structured Hub file is invalid."""


@dataclass
class Report:
    passes: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)

    def passed(self, message: str) -> None:
        self.passes.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def emit(self) -> None:
        for message in self.passes:
            print(f"PASS {message}")
        for message in self.warnings:
            print(f"WARN {message}")
        for message in self.failures:
            print(f"FAIL {message}")
        print(
            "SUMMARY "
            f"PASS={len(self.passes)} WARN={len(self.warnings)} FAIL={len(self.failures)}"
        )


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"not valid UTF-8: {path}: {exc}") from exc


def strip_inline_comment(value: str) -> str:
    in_single = False
    in_double = False
    escaped = False
    for index, char in enumerate(value):
        if escaped:
            escaped = False
            continue
        if char == "\\" and in_double:
            escaped = True
            continue
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            if index == 0 or value[index - 1].isspace():
                return value[:index].rstrip()
    if in_single or in_double:
        raise ValidationError("unterminated quoted YAML scalar")
    return value.rstrip()


def parse_scalar(value: str) -> Any:
    value = strip_inline_comment(value).strip()
    if not value:
        return None
    lowered = value.casefold()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "~"}:
        return None
    if value.startswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValidationError(f"invalid double-quoted YAML scalar: {value}") from exc
    if value.startswith("'"):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise ValidationError(f"invalid single-quoted YAML scalar: {value}") from exc
    if value.startswith(("[", "{")):
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValidationError(f"invalid flow-style YAML value: {value}") from exc
    if value in {"|", ">", "|-", ">-", "|+", ">+"}:
        raise ValidationError("block YAML scalars require PyYAML")
    if re.fullmatch(r"[-+]?\d+", value):
        return int(value)
    if re.fullmatch(r"[-+]?(?:\d+\.\d*|\d*\.\d+)", value):
        return float(value)
    return value


def parse_yaml_subset(text: str) -> dict[str, Any]:
    """Parse the mapping/list subset used by SKILL.md and openai.yaml."""

    tokens: list[tuple[int, str, int]] = []
    for number, raw_line in enumerate(text.splitlines(), start=1):
        if "\t" in raw_line:
            raise ValidationError(f"tabs are not allowed in YAML indentation at line {number}")
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent % 2:
            raise ValidationError(f"YAML indentation must use two-space levels at line {number}")
        tokens.append((indent, raw_line[indent:], number))

    if not tokens:
        return {}

    key_pattern = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(.*)$")

    def parse_block(index: int, indent: int) -> tuple[Any, int]:
        if index >= len(tokens) or tokens[index][0] != indent:
            raise ValidationError("invalid YAML block indentation")
        is_list = tokens[index][1].startswith("-")
        container: Any = [] if is_list else {}

        while index < len(tokens):
            current_indent, content, line_number = tokens[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                raise ValidationError(f"unexpected YAML indentation at line {line_number}")

            if is_list:
                if not content.startswith("-"):
                    break
                rest = content[1:].strip()
                index += 1
                if not rest:
                    if index >= len(tokens) or tokens[index][0] <= indent:
                        container.append(None)
                        continue
                    item, index = parse_block(index, tokens[index][0])
                    container.append(item)
                    continue
                match = key_pattern.match(rest)
                if not match:
                    container.append(parse_scalar(rest))
                    continue
                key, raw_value = match.groups()
                item: dict[str, Any] = {}
                if raw_value.strip():
                    item[key] = parse_scalar(raw_value)
                elif index < len(tokens) and tokens[index][0] > indent:
                    item[key], index = parse_block(index, tokens[index][0])
                else:
                    item[key] = None
                if index < len(tokens) and tokens[index][0] > indent:
                    continuation, index = parse_block(index, tokens[index][0])
                    if not isinstance(continuation, dict):
                        raise ValidationError(
                            f"YAML list mapping continuation must be a mapping at line {line_number}"
                        )
                    for continuation_key, continuation_value in continuation.items():
                        if continuation_key in item:
                            raise ValidationError(
                                f"duplicate YAML key {continuation_key!r} at line {line_number}"
                            )
                        item[continuation_key] = continuation_value
                container.append(item)
                continue

            if content.startswith("-"):
                break
            match = key_pattern.match(content)
            if not match:
                raise ValidationError(f"invalid YAML mapping at line {line_number}: {content}")
            key, raw_value = match.groups()
            if key in container:
                raise ValidationError(f"duplicate YAML key {key!r} at line {line_number}")
            index += 1
            if raw_value.strip():
                container[key] = parse_scalar(raw_value)
            elif index < len(tokens) and tokens[index][0] > indent:
                container[key], index = parse_block(index, tokens[index][0])
            else:
                container[key] = None

        return container, index

    document, final_index = parse_block(0, tokens[0][0])
    if final_index != len(tokens):
        raise ValidationError(f"unparsed YAML content at line {tokens[final_index][2]}")
    if not isinstance(document, dict):
        raise ValidationError("YAML document must be a mapping")
    return document


def parse_yaml(text: str) -> dict[str, Any]:
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        return parse_yaml_subset(text)

    try:
        document = yaml.safe_load(text)
    except yaml.YAMLError as exc:  # type: ignore[attr-defined]
        raise ValidationError(f"invalid YAML: {exc}") from exc
    if not isinstance(document, dict):
        raise ValidationError("YAML document must be a mapping")
    return document


def parse_skill_frontmatter(path: Path) -> dict[str, Any]:
    text = read_text(path)
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, flags=re.DOTALL)
    if not match:
        raise ValidationError("missing YAML frontmatter")
    return parse_yaml(match.group(1))


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def unquote_markdown(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == "`" and value[-1] == "`":
        return value[1:-1]
    link = re.fullmatch(r"\[[^]]+\]\(([^)]+)\)", value)
    return link.group(1) if link else value


def load_registry(report: Report) -> dict[str, dict[str, str]]:
    if not REGISTRY_PATH.is_file():
        report.fail(f"missing registry: {REGISTRY_PATH.relative_to(ROOT)}")
        return {}
    lines = read_text(REGISTRY_PATH).splitlines()
    header_index = next(
        (index for index, line in enumerate(lines) if table_cells(line) == REGISTRY_FIELDS),
        None,
    )
    if header_index is None:
        report.fail("REGISTRY.md is missing the required registered-skills table")
        return {}
    if header_index + 1 >= len(lines):
        report.fail("REGISTRY.md table has no separator row")
        return {}

    rows: dict[str, dict[str, str]] = {}
    for line in lines[header_index + 2 :]:
        if not line.strip().startswith("|"):
            break
        cells = table_cells(line)
        if len(cells) != len(REGISTRY_FIELDS):
            report.fail(f"registry row has {len(cells)} fields instead of {len(REGISTRY_FIELDS)}")
            continue
        row = dict(zip(REGISTRY_FIELDS, cells))
        name = unquote_markdown(row["Skill Name"])
        if name in rows:
            report.fail(f"duplicate registry entry: {name}")
            continue
        rows[name] = row
    report.passed(f"registry parsed with {len(rows)} skill entries")
    return rows


def discover_skills(report: Report) -> dict[str, dict[str, Any]]:
    discovered: dict[str, dict[str, Any]] = {}
    if not SKILLS_ROOT.is_dir():
        report.fail("missing .agents/skills directory")
        return discovered

    directories = sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir())
    report.passed(f"discovered {len(directories)} project skill directories")
    for directory in directories:
        skill_path = directory / "SKILL.md"
        if not skill_path.is_file():
            report.fail(f"missing SKILL.md: {directory.relative_to(ROOT)}")
            continue
        try:
            frontmatter = parse_skill_frontmatter(skill_path)
        except (OSError, ValidationError) as exc:
            report.fail(f"invalid frontmatter in {skill_path.relative_to(ROOT)}: {exc}")
            continue
        name = frontmatter.get("name")
        description = frontmatter.get("description")
        if not isinstance(name, str) or not name.strip():
            report.fail(f"missing name in {skill_path.relative_to(ROOT)}")
            continue
        if not isinstance(description, str) or not description.strip():
            report.fail(f"missing description in {skill_path.relative_to(ROOT)}")
        if name in discovered:
            report.fail(
                f"duplicate skill name {name}: {discovered[name]['path']} and {skill_path.relative_to(ROOT)}"
            )
            continue
        if name in BANNED_GENERIC_NAMES:
            report.fail(f"collision-prone generic skill name is forbidden: {name}")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            report.fail(f"invalid skill name syntax: {name}")

        metadata_path = directory / "agents" / "openai.yaml"
        metadata: dict[str, Any] | None = None
        implicit = True
        display_name: str | None = None
        if not metadata_path.is_file():
            report.warn(f"optional metadata missing: {metadata_path.relative_to(ROOT)}")
        else:
            try:
                metadata = parse_yaml(read_text(metadata_path))
            except (OSError, ValidationError) as exc:
                report.fail(f"invalid YAML in {metadata_path.relative_to(ROOT)}: {exc}")
            if metadata is not None:
                interface = metadata.get("interface", {})
                if interface is not None and not isinstance(interface, dict):
                    report.fail(f"interface must be a mapping in {metadata_path.relative_to(ROOT)}")
                elif isinstance(interface, dict):
                    raw_display = interface.get("display_name")
                    if raw_display is not None and not isinstance(raw_display, str):
                        report.fail(
                            f"interface.display_name must be a string in {metadata_path.relative_to(ROOT)}"
                        )
                    else:
                        display_name = raw_display
                policy = metadata.get("policy", {})
                if policy is None:
                    policy = {}
                if not isinstance(policy, dict):
                    report.fail(f"policy must be a mapping in {metadata_path.relative_to(ROOT)}")
                else:
                    raw_implicit = policy.get("allow_implicit_invocation", True)
                    if not isinstance(raw_implicit, bool):
                        report.fail(
                            "policy.allow_implicit_invocation must be true or false in "
                            f"{metadata_path.relative_to(ROOT)}"
                        )
                    else:
                        implicit = raw_implicit
                    if "allow_implicit_invocation" not in policy:
                        report.warn(
                            "implicit invocation uses the default true value in "
                            f"{metadata_path.relative_to(ROOT)}"
                        )
                report.passed(f"parsed Codex metadata YAML: {name}")

        discovered[name] = {
            "path": skill_path.relative_to(ROOT).as_posix(),
            "directory": directory.relative_to(ROOT).as_posix(),
            "description": description,
            "display_name": display_name,
            "implicit": implicit,
        }
        report.passed(f"valid skill entrypoint: {name}")
    return discovered


def validate_registry(
    report: Report,
    registry: dict[str, dict[str, str]],
    discovered: dict[str, dict[str, Any]],
) -> None:
    for name, skill in discovered.items():
        if name not in registry:
            report.fail(f"physical skill is not registered: {name}")
            continue
        row = registry[name]
        namespace = unquote_markdown(row["Namespace"])
        local_path = unquote_markdown(row["Local Path"]).replace("\\", "/").rstrip("/")
        status = unquote_markdown(row["Status"]).casefold()
        implicit_text = unquote_markdown(row["Implicit Invocation"]).casefold()
        display_name = unquote_markdown(row["Display Name"])

        if not namespace or not name.startswith(f"{namespace}-"):
            report.fail(f"namespace mismatch for {name}: {namespace}")
        if local_path != skill["directory"]:
            report.fail(
                f"registry path mismatch for {name}: {local_path} != {skill['directory']}"
            )
        if status not in ALLOWED_STATUSES:
            report.fail(f"invalid registry status for {name}: {status}")
        if implicit_text not in {"true", "false"}:
            report.fail(f"invalid registry implicit-invocation value for {name}: {implicit_text}")
        elif (implicit_text == "true") != skill["implicit"]:
            report.fail(f"registry/openai.yaml implicit-invocation mismatch for {name}")
        if skill["display_name"] and display_name != skill["display_name"]:
            report.fail(f"registry/openai.yaml display-name mismatch for {name}")

        upstream = unquote_markdown(row["Upstream Source"])
        commit = unquote_markdown(row["Upstream Commit"])
        if upstream.startswith("http") and not re.fullmatch(r"[0-9a-f]{40}", commit):
            report.fail(f"third-party registry commit is not a pinned SHA for {name}: {commit}")
        try:
            dt.date.fromisoformat(unquote_markdown(row["Last Validation"]))
        except ValueError:
            report.fail(f"invalid Last Validation date for {name}")
        if not row["License"].strip():
            report.fail(f"missing license record for {name}")
        for license_path in re.findall(r"`([^`]*(?:LICENSE|NOTICE)[^`]*)`", row["License"]):
            resolved = (ROOT / license_path).resolve()
            if not resolved.is_file():
                report.fail(f"missing registered license file for {name}: {license_path}")

    for name, row in registry.items():
        status = unquote_markdown(row["Status"]).casefold()
        if status == "active" and name not in discovered:
            report.fail(f"active registry skill does not exist: {name}")
        elif name not in discovered:
            report.warn(f"non-active registry skill has no local directory: {name}")

    missing_ars = sorted(REQUIRED_ARS - set(discovered))
    if missing_ars:
        report.fail(f"required ARS skills missing: {', '.join(missing_ars)}")
    inactive_ars = sorted(
        name
        for name in REQUIRED_ARS
        if name not in registry
        or unquote_markdown(registry[name]["Status"]).casefold() != "active"
    )
    if inactive_ars:
        report.fail(f"required ARS skills not registered active: {', '.join(inactive_ars)}")
    if not missing_ars and not inactive_ars:
        report.passed("four required ARS skills exist and are registered active")


def markdown_link_targets(text: str) -> list[str]:
    targets = re.findall(r"!?\[[^]]*\]\(([^)]+)\)", text)
    return [target.strip() for target in targets]


def resolve_relative_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    elif " " in target:
        target = target.split(" ", 1)[0]
    target = unquote(target.split("#", 1)[0])
    if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, flags=re.IGNORECASE):
        return None
    return (source.parent / target).resolve()


def validate_relative_links(report: Report) -> None:
    markdown_files = sorted(
        path for path in ROOT.rglob("*.md") if ".git" not in path.relative_to(ROOT).parts
    )
    checked = 0
    for source in markdown_files:
        try:
            text = read_text(source)
        except ValidationError as exc:
            report.fail(str(exc))
            continue
        for raw_target in markdown_link_targets(text):
            resolved = resolve_relative_target(source, raw_target)
            if resolved is None:
                continue
            checked += 1
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                report.fail(f"relative link escapes repository in {source.relative_to(ROOT)}: {raw_target}")
                continue
            if not resolved.exists():
                report.fail(f"broken relative link in {source.relative_to(ROOT)}: {raw_target}")

    dependency_pattern = re.compile(r"`((?:\.\.?/)[^`\n]+\.md(?:#[^`\n]+)?)`")
    for source in sorted(SKILLS_ROOT.rglob("*.md")):
        for raw_target in dependency_pattern.findall(read_text(source)):
            resolved = resolve_relative_target(source, raw_target)
            if resolved is not None and not resolved.is_file():
                report.fail(
                    f"broken required dependency in {source.relative_to(ROOT)}: {raw_target}"
                )
            else:
                checked += 1
    report.passed(f"checked {checked} relative Markdown links and dependency paths")


def secret_patterns() -> list[tuple[str, re.Pattern[str]]]:
    return [
        ("GitHub classic token", re.compile("gh" + r"[pousr]_[A-Za-z0-9]{30,}")),
        ("GitHub fine-grained token", re.compile("github" + r"_pat_[A-Za-z0-9_]{20,}")),
        ("OpenAI-style key", re.compile("s" + r"k-[A-Za-z0-9_-]{20,}")),
        ("AWS access key", re.compile("AK" + r"IA[0-9A-Z]{16}")),
        (
            "private key",
            re.compile("-" * 5 + r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY" + "-" * 5),
        ),
        (
            "assigned credential",
            re.compile(
                r"(?i)\b(?:api[_-]?key|access[_-]?token|password|client[_-]?secret)\b"
                r"\s*[:=]\s*[\"']([^\"'\r\n]{8,})[\"']"
            ),
        ),
    ]


def looks_like_placeholder(match: re.Match[str]) -> bool:
    candidate = match.group(1) if match.lastindex else match.group(0)
    lowered = candidate.casefold()
    return any(
        marker in lowered
        for marker in ("placeholder", "example", "redacted", "replace_me", "your_", "<", "...")
    )


def validate_credentials(report: Report) -> None:
    suspicious_names = {".env", "id_rsa", "id_ed25519", "credentials.json", "secrets.json"}
    patterns = secret_patterns()
    scanned = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.relative_to(ROOT).parts:
            continue
        lowered_name = path.name.casefold()
        if lowered_name in suspicious_names and not lowered_name.endswith(".example"):
            report.fail(f"credential-sensitive filename committed: {path.relative_to(ROOT)}")
        if path.suffix.casefold() not in TEXT_SUFFIXES and lowered_name not in {"license", "notice"}:
            continue
        if path.stat().st_size > 2_000_000:
            report.warn(f"large text file skipped during credential scan: {path.relative_to(ROOT)}")
            continue
        try:
            text = read_text(path)
        except ValidationError as exc:
            report.fail(str(exc))
            continue
        scanned += 1
        for label, pattern in patterns:
            for match in pattern.finditer(text):
                if not looks_like_placeholder(match):
                    line = text.count("\n", 0, match.start()) + 1
                    report.fail(f"possible {label} in {path.relative_to(ROOT)}:{line}")
    report.passed(f"credential scan completed across {scanned} text files")


def validate_hub_records(report: Report) -> None:
    for path in sorted(REQUIRED_HUB_FILES):
        if not path.is_file():
            report.fail(f"missing required Hub file: {path.relative_to(ROOT)}")
    if all(path.is_file() for path in REQUIRED_HUB_FILES):
        report.passed("required Hub governance files exist")

    agents_text = read_text(ROOT / "AGENTS.md")
    for name in sorted(REQUIRED_ARS):
        if name not in agents_text:
            report.fail(f"AGENTS.md is missing active ARS route: {name}")
    future_claim_pattern = re.compile(
        r"(?:nature|stats|materials|figures|data)-[a-z0-9-]+\s*:\s*\.agents/skills/"
    )
    if future_claim_pattern.search(agents_text):
        report.fail("AGENTS.md claims an uninstalled future namespace skill")
    report.passed("AGENTS.md preserves active ARS routing without future-skill claims")

    source_text = read_text(ROOT / "skill-sources" / "SOURCES.md")
    source_markers = [
        "Imbad0202/academic-research-skills",
        "94436237913091d4739870159d241660527e8338",
        "CC BY-NC 4.0",
        "academic-research/LICENSE",
        "academic-research/NOTICE.md",
        "Security notes",
    ]
    missing_markers = [marker for marker in source_markers if marker not in source_text]
    if missing_markers:
        report.fail(f"source ledger missing required ARS markers: {missing_markers}")
    else:
        report.passed("source ledger preserves ARS provenance, license, and security notes")


def main() -> int:
    report = Report()
    validate_hub_records(report)
    registry = load_registry(report)
    discovered = discover_skills(report)
    validate_registry(report, registry, discovered)
    validate_relative_links(report)
    validate_credentials(report)
    report.emit()
    return 1 if report.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
