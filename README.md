# codex

This is my first GitHub repository.

## Academic Research Workspace

This repository includes a Codex-friendly academic research workspace with four project-local skills:

- `$ars-deep-research` for literature discovery, research status, evidence verification, research-gap analysis, systematic review, and meta-analysis;
- `$ars-academic-paper` for planning, outlining, evidence-grounded writing, revision, abstracts, citation audits, disclosure, and format conversion;
- `$ars-academic-paper-reviewer` for read-only peer review, methodology assessment, reviewer simulation, and re-review;
- `$ars-academic-pipeline` for the full research → literature → evidence → planning → writing → review → revision → finalization workflow.

Start with [the Academic Research Workspace guide](docs/ACADEMIC_WORKFLOW.md). The repository-level [AGENTS.md](AGENTS.md) automatically routes academic requests, including priority routing for Al-Sc, Al-Sc-Zr, Al3Sc/Al3(Sc,Zr), precipitation strengthening, recrystallization, grain refinement, TEM, SEM, EBSD, microstructure, and mechanical-properties research.

Example:

```text
系统分析 Al-Sc-Zr 合金中 Al3(Sc,Zr) 析出相对再结晶抑制机制的研究现状，并识别 research gap。
```

Run the local validation with:

```text
python academic-research/scripts/smoke_test.py
```

The adapted academic workflow is attributed and licensed separately under [`academic-research/`](academic-research/NOTICE.md); see the [complete upstream CC BY-NC 4.0 license](academic-research/LICENSE).

## Academic Skill Hub

This repository includes a governance layer for safely maintaining project-local academic skills over time.

Active suite: **ARS Academic Research Suite**

Active skills:

- `ars-deep-research`
- `ars-academic-paper`
- `ars-academic-paper-reviewer`
- `ars-academic-pipeline`

Use the [Skill Registry](skill-registry/REGISTRY.md) for the authoritative active inventory, the [Source Ledger](skill-sources/SOURCES.md) for provenance and licensing, and the [Skill Integration Guide](docs/SKILL_INTEGRATION_GUIDE.md) before adding a third-party skill. Run both validators from the repository root:

```text
python academic-research/scripts/smoke_test.py
python scripts/validate_skill_hub.py
```

Reserved future namespace architecture:

- `nature-*` — Nature or journal-specific workflows
- `stats-*` — statistics and quantitative analysis
- `materials-*` — materials-science domain workflows
- `figures-*` — scientific figures and visualization
- `data-*` — research-data processing

These future namespaces are governance reservations only. They do not mean that any corresponding skills are installed or active.
