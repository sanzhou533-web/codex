# codex

This is my first GitHub repository.

## Academic Research Workspace

This repository includes a Codex-friendly academic research workspace with four project-local skills:

- `deep-research` for literature discovery, research status, evidence verification, research-gap analysis, systematic review, and meta-analysis;
- `academic-paper` for planning, outlining, evidence-grounded writing, revision, abstracts, citation audits, disclosure, and format conversion;
- `academic-paper-reviewer` for read-only peer review, methodology assessment, reviewer simulation, and re-review;
- `academic-pipeline` for the full research → literature → evidence → planning → writing → review → revision → finalization workflow.

Start with [the Academic Research Workspace guide](docs/ACADEMIC_WORKFLOW.md). The repository-level [AGENTS.md](AGENTS.md) automatically routes academic requests, including priority routing for Al-Sc, Al-Sc-Zr, Al3Sc/Al3(Sc,Zr), precipitation strengthening, recrystallization, grain refinement, TEM, SEM, EBSD, microstructure, and mechanical-properties research.

Example:

```text
系统分析 Al-Sc-Zr 合金中 Al3(Sc,Zr) 析出相对再结晶抑制机制的研究现状，并识别 research gap。
```

Run the local validation with:

```text
python academic-research/scripts/smoke_test.py
```

The adapted academic workflow is attributed and licensed separately under [`academic-research/`](academic-research/NOTICE.md); see the [CC BY-NC 4.0 notice](academic-research/LICENSE.md).
