# Codex Adaptation Notes

## Upstream basis

This workspace was adapted from the following files in `Imbad0202/academic-research-skills` at commit `94436237913091d4739870159d241660527e8338`:

- `LICENSE`
- `NOTICE.md` (the upstream repository has no extensionless `NOTICE`)
- `README.md`
- `MODE_REGISTRY.md`
- `academic-paper/SKILL.md`
- `deep-research/SKILL.md`
- `academic-paper-reviewer/SKILL.md`
- `academic-pipeline/SKILL.md`

The upstream mode names, core stage relationships, human-in-the-loop boundaries, evidence verification requirements, reviewer read-only behavior, and cross-skill handoff intent were retained in a smaller project-local form.

The adapted Codex skill identities use the collision-resistant ARS namespace: `ars-deep-research`, `ars-academic-paper`, `ars-academic-paper-reviewer`, and `ars-academic-pipeline`. Directory names remain aligned with the upstream layout, but Codex discovery uses each `SKILL.md` frontmatter `name`.

## Runtime rewrites

| Upstream surface | Codex workspace treatment |
|---|---|
| `.claude/CLAUDE.md` routing | Rewritten as the repository-root `AGENTS.md` academic task router. |
| `.claude-plugin/` manifests | Not copied and not required. Project-local skills are stored under `.agents/skills/`. |
| Claude slash-command declarations | Replaced with plain prompt recipes under `academic-research/commands/`; they do not register slash commands. |
| Claude-facing skill names | Namespaced as `$ars-*`; implicit invocation remains enabled in each `agents/openai.yaml`. |
| `model: opus`, `model: sonnet`, or `model: inherit` | Removed. Skills use the active Codex model unless the user explicitly changes task settings. |
| Claude Agent/Task dispatch | Rewritten as inline staged execution. Codex subagents are optional and require explicit user request. |
| `AskUserQuestion`, `WebSearch`, `Bash`, `Write`, `Edit` names | Rewritten as capability-neutral instructions using tools available in the active Codex task. |
| Claude hooks | Not copied. No hook is required for routing, validation, or skill use. |
| Upstream cross-skill relative paths | Rebased to sibling project skills and shared files; namespaced handoff identities and physical paths are explicitly validated by the smoke test. |

## Deliberate scope

This repository contains a focused academic workspace, not a byte-for-byte vendor copy of the upstream suite. Complex upstream validators, hooks, role prompt libraries, cross-model transports, and publication-format toolchains are not silently claimed as available. The workspace retains the requested modes and evidence discipline while exposing missing capabilities honestly.
