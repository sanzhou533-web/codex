#!/usr/bin/env python3
"""Run deterministic static checks for the project-local academic workspace.

This script validates configuration fixtures. It does not test Codex runtime
discovery or implicit skill invocation.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROUTER_PATH = ROOT / "academic-research" / "shared" / "router-rules.json"
EXPECTED_SAMPLES = {
    "系统分析 Al-Sc-Zr 合金中 Al3(Sc,Zr) 析出相对再结晶抑制机制的研究现状，并识别 research gap。": "ars-deep-research",
    "根据现有 evidence matrix 帮我写 Results and Discussion。": "ars-academic-paper",
    "以材料学期刊审稿人的标准检查这一章节。": "ars-academic-paper-reviewer",
    "从研究问题开始，完成文献调研、证据矩阵、论文规划、写作、审稿和返修。": "ars-academic-pipeline",
    "Compare TEM evidence for Al3Sc coarsening kinetics.": "ars-deep-research",
}
EXPECTED_MODES = {
    "ars-deep-research": {
        "full",
        "quick",
        "review",
        "lit-review",
        "three-way-scan",
        "fact-check",
        "socratic",
        "systematic-review",
    },
    "ars-academic-paper": {
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
    "ars-academic-paper-reviewer": {
        "full",
        "re-review",
        "quick",
        "methodology-focus",
        "guided",
        "calibration",
    },
    "ars-academic-pipeline": {"full", "resume"},
}
EXPECTED_METADATA = {
    "ars-deep-research": "ARS Deep Research",
    "ars-academic-paper": "ARS Academic Paper",
    "ars-academic-paper-reviewer": "ARS Academic Paper Reviewer",
    "ars-academic-pipeline": "ARS Academic Pipeline",
}
UPSTREAM_LICENSE_SHA256 = "b3848009d12a173f549ef98d9ee486e64459e8eb5d9f895bff53782b4aa86d7c"


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
        return "ars-deep-research", "materials-science-priority"
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


def validate_openai_metadata(config: dict) -> list[str]:
    results: list[str] = []
    for skill_name, entry in config["skills"].items():
        skill_path = ROOT / entry["skill_path"]
        metadata_path = skill_path.parent / "agents" / "openai.yaml"
        if not metadata_path.is_file():
            raise AssertionError(f"missing Codex desktop metadata: {metadata_path}")
        metadata = metadata_path.read_text(encoding="utf-8")
        display_name = EXPECTED_METADATA[skill_name]
        if f'display_name: "{display_name}"' not in metadata:
            raise AssertionError(f"display_name mismatch in {metadata_path}")
        description_match = re.search(r'^  short_description: "(.+)"$', metadata, flags=re.MULTILINE)
        if not description_match or not 25 <= len(description_match.group(1)) <= 64:
            raise AssertionError(f"invalid short_description in {metadata_path}")
        if "allow_implicit_invocation: true" not in metadata:
            raise AssertionError(f"implicit invocation is not enabled in {metadata_path}")
        if re.search(r"^dependencies:", metadata, flags=re.MULTILINE):
            raise AssertionError(f"unexpected tool dependency declaration in {metadata_path}")
        results.append(f"PASS Codex metadata: {skill_name}")
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
        ("ars-deep-research", "../deep-research/SKILL.md"),
        ("ars-academic-paper", "../academic-paper/SKILL.md"),
        ("ars-academic-paper-reviewer", "../academic-paper-reviewer/SKILL.md"),
    ]
    results: list[str] = []
    for skill_name, relative in required:
        if skill_name not in text or relative not in text:
            raise AssertionError(f"pipeline does not declare dependency: {skill_name} at {relative}")
        resolved = (pipeline.parent / relative).resolve()
        if not resolved.is_file():
            raise AssertionError(f"pipeline dependency does not resolve: {resolved}")
        if parse_frontmatter(resolved).get("name") != skill_name:
            raise AssertionError(f"pipeline identity/path mismatch: {skill_name} at {resolved}")
        results.append(f"PASS pipeline dependency: {skill_name} -> {relative}")
    sequential_links = [
        (
            ROOT / ".agents" / "skills" / "deep-research" / "SKILL.md",
            "ars-academic-paper",
            "../academic-paper/SKILL.md",
        ),
        (
            ROOT / ".agents" / "skills" / "academic-paper" / "SKILL.md",
            "ars-academic-paper-reviewer",
            "../academic-paper-reviewer/SKILL.md",
        ),
        (
            ROOT / ".agents" / "skills" / "academic-paper" / "SKILL.md",
            "ars-academic-pipeline",
            "../academic-pipeline/SKILL.md",
        ),
        (
            ROOT / ".agents" / "skills" / "academic-paper-reviewer" / "SKILL.md",
            "ars-academic-paper",
            "../academic-paper/SKILL.md",
        ),
        (
            ROOT / ".agents" / "skills" / "academic-paper-reviewer" / "SKILL.md",
            "ars-academic-pipeline",
            "../academic-pipeline/SKILL.md",
        ),
    ]
    for source, target_name, relative in sequential_links:
        source_text = source.read_text(encoding="utf-8")
        if target_name not in source_text or relative not in source_text:
            raise AssertionError(f"missing sequential handoff in {source}: {target_name} at {relative}")
        if not (source.parent / relative).resolve().is_file():
            raise AssertionError(f"sequential handoff does not resolve: {source} -> {relative}")
        results.append(f"PASS sequential handoff: {source.parent.name} -> {target_name}")
    return results


def validate_agents_router() -> list[str]:
    agents_path = ROOT / "AGENTS.md"
    text = agents_path.read_text(encoding="utf-8")
    config = load_router()
    for skill_name, entry in config["skills"].items():
        if skill_name not in text or entry["skill_path"] not in text:
            raise AssertionError(f"AGENTS.md does not map {skill_name} to {entry['skill_path']}")
    for legacy_mention in ("$deep-research", "$academic-paper", "$academic-paper-reviewer", "$academic-pipeline"):
        if legacy_mention in text:
            raise AssertionError(f"legacy explicit skill invocation remains in AGENTS.md: {legacy_mention}")
    if "external literature verification is unavailable" not in text:
        raise AssertionError("AGENTS.md does not preserve the literature capability gate")
    return ["PASS AGENTS.md namespaced router and capability gate"]


def validate_handoff_schema() -> list[str]:
    schema_path = ROOT / "academic-research" / "shared" / "handoff-schema.md"
    text = schema_path.read_text(encoding="utf-8")
    transitions = [
        "ars-deep-research to ars-academic-paper",
        "ars-academic-paper to ars-academic-paper-reviewer",
        "ars-academic-paper-reviewer to ars-academic-paper",
        "ars-academic-paper to final verification",
    ]
    for transition in transitions:
        if transition not in text:
            raise AssertionError(f"missing namespaced handoff transition: {transition}")
    return ["PASS namespaced handoff schema"]


def validate_license() -> list[str]:
    license_path = ROOT / "academic-research" / "LICENSE"
    if not license_path.is_file():
        raise AssertionError(f"missing complete upstream license: {license_path}")
    normalized_text = license_path.read_text(encoding="utf-8")
    digest = hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()
    if digest != UPSTREAM_LICENSE_SHA256:
        raise AssertionError(f"upstream license hash mismatch: {digest}")
    if (ROOT / "academic-research" / "LICENSE.md").exists():
        raise AssertionError("summary LICENSE.md remains beside complete upstream LICENSE")
    notice = (ROOT / "academic-research" / "NOTICE.md").read_text(encoding="utf-8")
    notice_markers = [
        "https://github.com/Imbad0202/academic-research-skills",
        "94436237913091d4739870159d241660527e8338",
        "adaptation",
        "No endorsement",
        "CC BY-NC 4.0",
    ]
    missing = [marker for marker in notice_markers if marker not in notice]
    if missing:
        raise AssertionError(f"NOTICE.md missing required attribution markers: {missing}")
    return [f"PASS complete upstream LICENSE and NOTICE: sha256={digest}"]


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
    output.extend(validate_openai_metadata(config))
    output.extend(validate_markdown_links())
    output.extend(validate_pipeline_chain())
    output.extend(validate_agents_router())
    output.extend(validate_handoff_schema())
    output.extend(validate_codex_runtime_surface())
    output.extend(validate_license())

    for prompt, expected in EXPECTED_SAMPLES.items():
        actual, reason = route(prompt, config)
        if actual != expected:
            raise AssertionError(f"route mismatch: expected {expected}, got {actual}: {prompt}")
        output.append(f"PASS static route fixture {expected} ({reason}): {prompt}")

    print("\n".join(output))
    print("PASS Academic Research Workspace static smoke test (not a Codex runtime invocation test)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, OSError, ValueError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
