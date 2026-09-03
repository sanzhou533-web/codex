# Academic Skill Hub Integration Guide

Use this guide for every new or updated third-party academic skill. Each skill or suite receives its own branch and pull request. The current active suite is ARS; reserved namespaces do not represent installed capabilities.

## Namespace governance

| Namespace | Intended scope |
|---|---|
| `ars-*` | Academic Research Suite workflows |
| `nature-*` | Nature or other journal-specific workflows |
| `stats-*` | Statistics and quantitative analysis |
| `materials-*` | Materials-science domain workflows |
| `figures-*` | Scientific figure and visualization workflows |
| `data-*` | Research-data processing workflows |
| `review-*` | A future independent review suite that does not belong to ARS |

Before accepting a name, compare it with OpenAI official skills, user-level skills, project skills, and all third-party candidates under review. Do not introduce collision-prone generic names such as `research`, `writing`, `review`, `analysis`, `paper`, `statistics`, or `plot`. Assign a stable namespace when the upstream name could collide. Record both the upstream identity and adapted identity in the source ledger.

## Two-level routing and collision policy

Level 1 chooses an installed suite or domain. Level 2 chooses a specific skill and mode. A namespace reservation alone never participates in routing.

1. A compatible explicit `$skill-name` selection overrides implicit selection.
2. Among implicit candidates, choose the most specific skill for the requested outcome.
3. Do not give a newly installed skill highest priority merely because it exists.
4. Domain specialization does not override an explicit compatible user selection.
5. Preserve a general fallback. For example, “帮我写论文” belongs to a general academic writer; “按 Nature 风格重构投稿稿件” may use a future Nature-specific skill only after that skill is actually installed and registered.
6. When no installed specialization matches, use the compatible active general skill or disclose that the specialization is unavailable.

Currently, only the ARS suite is active:

- research, literature, and evidence → `ars-deep-research`
- writing and manuscripts → `ars-academic-paper`
- peer review and manuscript assessment → `ars-academic-paper-reviewer`
- explicit end-to-end research-to-paper work → `ars-academic-pipeline`

## Standard intake workflow

### Stage 1 — Source inspection

Record the GitHub URL, repository owner, LICENSE, NOTICE, version/tag/commit, project activity, security-relevant scripts, and external dependencies. Pin an immutable commit. Do not rely only on a moving branch or release label.

### Stage 2 — Runtime inspection

Classify the source as a native Codex skill, Claude skill, Cursor rules, generic prompt, MCP-dependent skill, CLI-dependent workflow, Python/Node tool, or mixed runtime. Identify every assumption that is unavailable in the target Codex environment.

### Stage 3 — License decision

Record whether adaptation and redistribution are permitted, commercial restrictions, attribution duties, and share-alike conditions. If the license is absent, conflicting, or unclear, do not copy substantial source text. Prefer a clean-room interoperability note or stop for legal clarification.

### Stage 4 — Codex adaptation

Create `.agents/skills/<folder>/SKILL.md` and, when useful, `.agents/skills/<folder>/agents/openai.yaml`. Rewrite or isolate Claude-specific model declarations, hooks, slash commands, proprietary tool names, unsupported agent dispatch, install assumptions, and API assumptions. Do not declare a dependency that is not genuinely required and available.

### Stage 5 — Namespace assignment

Check all discovery scopes for frontmatter `name` collisions. Assign the approved namespace, keep it under 64 lowercase letters/digits/hyphens, and align UI metadata and examples with the adapted identity.

### Stage 6 — Routing integration

Update `AGENTS.md` according to task intent and specificity. Preserve explicit-selection priority and existing fallback routes. Do not elevate a skill merely because it was added.

### Stage 7 — Static validation

Check `SKILL.md`, YAML frontmatter, name, description, relative paths, required dependencies, license, attribution, and `agents/openai.yaml`. Update the registry and source ledger in the same change.

### Stage 8 — Codex discovery validation

Open a fresh Codex task at the repository root and inspect `/skills` or the current skill selector. Record the actual discovered identity and display name. A filesystem scan alone is not discovery proof.

### Stage 9 — Explicit invocation

Run a bounded prompt using `$skill-name`. Confirm the named skill is loaded and its distinctive safety or workflow constraints are applied.

### Stage 10 — Implicit invocation

Run at least two natural-language cases:

- Positive test: the new skill should be selected.
- Negative test: the new skill should not be selected.

Record prompt, actual skill, expected skill, and pass/fail. A deterministic Python router fixture is not a live implicit-invocation test.

### Stage 11 — Regression

Confirm the integration has not broken `ars-deep-research`, `ars-academic-paper`, `ars-academic-paper-reviewer`, or `ars-academic-pipeline`. Run the ARS smoke test, Hub validator, `/skills`, and the four established ARS runtime prompts.

### Stage 12 — Pull request

Use a separate PR for each third-party skill or suite. Include provenance, pinned commit, license decision, namespace, adaptation notes, security notes, static validation, discovery evidence, positive/negative runtime tests, and regression results. Do not merge automatically.

## Third-party safety review

Before enabling a third-party skill, inspect all shell scripts, PowerShell, Python, Node, install commands, `curl`/`wget`, network calls, filesystem writes, environment-variable access, token requirements, and MCP server requirements.

Pay special attention to attempts to access or modify:

- SSH keys;
- GitHub tokens;
- browser credentials;
- API keys;
- system-wide configuration;
- files outside the declared workspace;
- persistent startup hooks or background services.

Record findings under a `Security Notes` section in the source ledger and PR. High-risk behavior must not be enabled by default. Remove it, isolate it behind explicit authorization, or leave the integration disabled until the risk is resolved.

## Required records

Every integrated skill must have:

- one row in [`skill-registry/REGISTRY.md`](../skill-registry/REGISTRY.md);
- a source-suite entry in [`skill-sources/SOURCES.md`](../skill-sources/SOURCES.md);
- a pinned immutable upstream reference;
- an explicit license and attribution decision;
- security notes;
- static, discovery, explicit, implicit, and regression evidence appropriate to the change.
