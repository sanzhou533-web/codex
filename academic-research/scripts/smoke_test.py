#!/usr/bin/env python3
"""Validate the project-local academic skills, paths, and routing examples."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROUTER_PATH = ROOT / "academic-research" / "shared" / "router-rules.json"
EXPECTED_SAMPLES = {
    "系统分析 Al-Sc-Zr 合金中 Al3(Sc,Zr) 析出相对再结晶抑制机制的研究现状，并识别 research gap。": "deep-research",
    "根据现有证据帮我写这一章节。": "academic-paper",
    "以材料学期刊审稿人的标准检查这一章节。": "academic-paper-reviewer",
    "Compare TEM evidence for Al3Sc coarsening kinetics.": "deep-research",
}
EXPECTED_MODES = {
    "deep-research": {
        "full",
        "quick",
        "review",
        "lit-review",
        "three-way-scan",
        "fact-check",
        "socratic",
        "systematic-review",
    },
    "academic-paper": {
        "full",
        "plan",
        "outline-only",
        "revision",
        "revision-coach",
        "abstract-only",
        "lit-review",
        "format-convert",
        "citation-check",
        "disclosure",
        "rebuttal-audit",
    },
    "academic-paper-reviewer": {
        "full",
        "re-review",
        "quick",
        "methodology-focus",
        "guided",
        "calibration",
    },
    "academic-pipeline": {"full", "resume"},
}


def load_router() -> dict:
    with ROUTER_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def route(prompt: str, config: dict) -> tuple[str | None, str]:
    normalized = prompt.casefold()
    for skill_name in config["precedence"]:
        for trigger in config["skills"][skill_name]["triggers"]:
            if trigger.casefold() in normalized:
                return skill_name, f"trigger:{trigger}"

    has_domain = any(term.casefold() in normalized for term in config["materials_science_terms"])
    has_academic_intent = any(term.casefold() in normalized for term in config["academic_intent_terms"])
    if has_domain and has_academic_intent:
        return "deep-research", "materials-science-priority"
    return None, "no-match"


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        raise AssertionError(f"missing YAML frontmatter: {path}")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line and not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    return fields


def validate_skill_paths(config: dict) -> list[str]:
    results: list[str] = []
    names: set[str] = set()
    for expected_name, entry in config["skills"].items():
        skill_path = ROOT / entry["skill_path"]
        if not skill_path.is_file():
            raise AssertionError(f"missing skill: {skill_path}")
        fields = parse_frontmatter(skill_path)
        if fields.get("name") != expected_name:
            raise AssertionError(f"frontmatter name mismatch in {skill_path}")
        if not fields.get("description"):
            raise AssertionError(f"missing description in {skill_path}")
        if fields["name"] in names:
            raise AssertionError(f"duplicate skill name: {fields['name']}")
        skill_text = skill_path.read_text(encoding="utf-8")
        missing_modes = sorted(mode for mode in EXPECTED_MODES[expected_name] if f"`{mode}`" not in skill_text)
        if missing_modes:
            raise AssertionError(f"missing modes in {skill_path}: {missing_modes}")
        names.add(fields["name"])
        results.append(
            f"PASS skill {expected_name} ({len(EXPECTED_MODES[expected_name])} modes): "
            f"{entry['skill_path']}"
        )
    return results


def validate_markdown_links() -> list[str]:
    results: list[str] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    markdown_files = [ROOT / "README.md", ROOT / "AGENTS.md"]
    markdown_files.extend(sorted((ROOT / ".agents").rglob("*.md")))
    markdown_files.extend(sorted((ROOT / "academic-research").rglob("*.md")))
    markdown_files.extend(sorted((ROOT / "docs").rglob("*.md")))
    for markdown_path in markdown_files:
        for target in link_pattern.findall(markdown_path.read_text(encoding="utf-8")):
            target_without_anchor = target.split("#", 1)[0]
            if not target_without_anchor or "://" in target_without_anchor:
                continue
            resolved = (markdown_path.parent / target_without_anchor).resolve()
            if not resolved.exists():
                raise AssertionError(f"broken link in {markdown_path}: {target}")
    results.append(f"PASS relative links: {len(markdown_files)} Markdown files")
    return results


def validate_pipeline_chain() -> list[str]:
    pipeline = ROOT / ".agents" / "skills" / "academic-pipeline" / "SKILL.md"
    text = pipeline.read_text(encoding="utf-8")
    required = [
        "../deep-research/SKILL.md",
        "../academic-paper/SKILL.md",
        "../academic-paper-reviewer/SKILL.md",
    ]
    results: list[str] = []
    for relative in required:
        if relative not in text:
            raise AssertionError(f"pipeline does not declare dependency: {relative}")
        resolved = (pipeline.parent / relative).resolve()
        if not resolved.is_file():
            raise AssertionError(f"pipeline dependency does not resolve: {resolved}")
        results.append(f"PASS pipeline dependency: {relative}")
    sequential_links = [
        (
            ROOT / ".agents" / "skills" / "deep-research" / "SKILL.md",
            "../academic-paper/SKILL.md",
        ),
        (
            ROOT / ".agents" / "skills" / "academic-paper" / "SKILL.md",
            "../academic-paper-reviewer/SKILL.md",
        ),
    ]
    for source, relative in sequential_links:
        if relative not in source.read_text(encoding="utf-8"):
            raise AssertionError(f"missing sequential handoff in {source}: {relative}")
        if not (source.parent / relative).resolve().is_file():
            raise AssertionError(f"sequential handoff does not resolve: {source} -> {relative}")
        results.append(f"PASS sequential handoff: {source.parent.name} -> {relative}")
    return results


def validate_codex_runtime_surface() -> list[str]:
    forbidden = [".claude/", ".claude-plugin/", "model: opus", "model: sonnet", "anthropic_api_key"]
    files = [ROOT / "AGENTS.md", *sorted((ROOT / ".agents" / "skills").glob("*/SKILL.md"))]
    combined = "\n".join(path.read_text(encoding="utf-8").casefold() for path in files)
    for token in forbidden:
        if token.casefold() in combined:
            # AGENTS and pipeline may name excluded paths when stating that they are not dependencies.
            if token in {".claude/", ".claude-plugin/"}:
                continue
            raise AssertionError(f"forbidden runtime declaration present: {token}")
    for excluded_directory in (ROOT / ".claude", ROOT / ".claude-plugin"):
        if excluded_directory.exists():
            raise AssertionError(f"Claude-specific runtime directory present: {excluded_directory}")
    return ["PASS active runtime has no fixed Claude model or Anthropic credential dependency"]


def main() -> int:
    config = load_router()
    output: list[str] = []
    output.extend(validate_skill_paths(config))
    output.extend(validate_markdown_links())
    output.extend(validate_pipeline_chain())
    output.extend(validate_codex_runtime_surface())

    for prompt, expected in EXPECTED_SAMPLES.items():
        actual, reason = route(prompt, config)
        if actual != expected:
            raise AssertionError(f"route mismatch: expected {expected}, got {actual}: {prompt}")
        output.append(f"PASS route {expected} ({reason}): {prompt}")

    print("\n".join(output))
    print("PASS Academic Research Workspace smoke test")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, OSError, ValueError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
