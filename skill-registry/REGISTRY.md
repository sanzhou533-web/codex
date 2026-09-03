# Academic Skill Hub Registry

This registry is the authoritative inventory of skills formally included in this repository. A skill is installed only when its entry exists here and its local `SKILL.md` is present. Planned namespaces are not installed skills.

## Registered skills

| Skill Name | Display Name | Namespace | Local Path | Upstream Source | Upstream Commit | License | Implicit Invocation | Status | Last Validation | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| `ars-deep-research` | ARS Deep Research | `ars` | `.agents/skills/deep-research` | https://github.com/Imbad0202/academic-research-skills | `94436237913091d4739870159d241660527e8338` | `CC-BY-NC-4.0` (CC BY-NC 4.0); full text: `academic-research/LICENSE` | `true` | `active` | `2026-09-03` | Codex adaptation; external literature capability gate required |
| `ars-academic-paper` | ARS Academic Paper | `ars` | `.agents/skills/academic-paper` | https://github.com/Imbad0202/academic-research-skills | `94436237913091d4739870159d241660527e8338` | `CC-BY-NC-4.0` (CC BY-NC 4.0); full text: `academic-research/LICENSE` | `true` | `active` | `2026-09-03` | Evidence-matrix writing gate; citation checking is independent |
| `ars-academic-paper-reviewer` | ARS Academic Paper Reviewer | `ars` | `.agents/skills/academic-paper-reviewer` | https://github.com/Imbad0202/academic-research-skills | `94436237913091d4739870159d241660527e8338` | `CC-BY-NC-4.0` (CC BY-NC 4.0); full text: `academic-research/LICENSE` | `true` | `active` | `2026-09-03` | Read-only reviewer workflow by default |
| `ars-academic-pipeline` | ARS Academic Pipeline | `ars` | `.agents/skills/academic-pipeline` | https://github.com/Imbad0202/academic-research-skills | `94436237913091d4739870159d241660527e8338` | `CC-BY-NC-4.0` (CC BY-NC 4.0); full text: `academic-research/LICENSE` | `true` | `active` | `2026-09-03` | Orchestrates the three substantive ARS skills |

Allowed status values are `active`, `testing`, `deprecated`, and `disabled`. Only `active` skills participate in normal routing. Every physical project skill must have exactly one registry row, including skills in testing or disabled states.

## Planned namespaces

| Namespace | Intended scope | State |
|---|---|---|
| `nature` | Nature and journal-specific workflows | Reserved; no skill installed |
| `stats` | Statistics and quantitative analysis | Reserved; no skill installed |
| `materials` | Materials-science domain workflows | Reserved; no skill installed |
| `figures` | Scientific figures and visualization | Reserved; no skill installed |
| `data` | Research-data processing | Reserved; no skill installed |
| `review` | Independent review suites not belonging to ARS | Conditional reservation; no skill installed |

Register a new skill only after completing the intake process in [`docs/SKILL_INTEGRATION_GUIDE.md`](../docs/SKILL_INTEGRATION_GUIDE.md). Never pre-register a hypothetical skill as active.
