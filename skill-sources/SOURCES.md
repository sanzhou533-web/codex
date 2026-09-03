# Third-Party Skill Source Ledger

This ledger preserves provenance and adaptation decisions for every third-party suite represented in the Skill Hub. Update it whenever a pinned commit, license decision, or local adaptation changes.

## Academic Research Skills

| Field | Value |
|---|---|
| Upstream | `Imbad0202/academic-research-skills` |
| Repository | https://github.com/Imbad0202/academic-research-skills |
| Pinned commit | `94436237913091d4739870159d241660527e8338` |
| License | `CC-BY-NC-4.0`; Creative Commons Attribution-NonCommercial 4.0 International; CC BY-NC 4.0 |
| Local namespace | `ars-` |
| Local license | [`academic-research/LICENSE`](../academic-research/LICENSE) |
| Local notice | [`academic-research/NOTICE.md`](../academic-research/NOTICE.md) |
| Adaptation | Claude-oriented packaging adapted to Codex project-local skills. |

### Adaptation record

- Replaced Claude routing with the repository-level `AGENTS.md` router.
- Replaced Claude slash-command declarations with prompt recipes.
- Removed fixed Claude model, hook, Anthropic credential, and Claude agent-dispatch dependencies.
- Rebased shared references and cross-skill handoffs to project-relative Codex paths.
- Added `ars-` identities, Codex desktop metadata, implicit-invocation policy, static validation, and real runtime discovery checks.

### Security notes

The integrated ARS workspace is instruction-led. No upstream install hooks, credential readers, MCP requirements, or automatic external command dependencies are enabled. Literature discovery remains capability-gated and must not claim external verification when search or a supplied corpus is unavailable.
