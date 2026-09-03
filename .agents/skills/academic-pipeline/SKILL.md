---
name: academic-pipeline
description: Orchestrate an explicit end-to-end academic workflow from research question through literature, evidence, planning, writing, review, revision, verification, and finalization. Use only for 完整科研流程, research to paper, 从研究问题到论文终稿, full academic workflow, or equivalent end-to-end requests.
metadata:
  version: "0.1.0"
  upstream: "Imbad0202/academic-research-skills@94436237913091d4739870159d241660527e8338"
  upstream_skill_version: "3.21.1"
  depends_on: "deep-research, academic-paper, academic-paper-reviewer"
---

# Academic Pipeline

Coordinate the workflow; do not replace the substantive skills. Read [the shared evidence policy](../../../academic-research/shared/evidence-policy.md) and [the handoff schema](../../../academic-research/shared/handoff-schema.md) before starting. Use [workflow protocols](../../../academic-research/references/workflow-protocols.md) for gate details.

Modes are `full` for a new end-to-end run and `resume` when the user supplies a prior state record and handoff artifacts. Resume from the recorded stage without reconstructing completed work or upgrading unverified artifacts.

## Dependency resolution

Resolve project-local skills relative to this file:

1. Research and evidence: `../deep-research/SKILL.md`
2. Planning, writing, and revision: `../academic-paper/SKILL.md`
3. Review and re-review: `../academic-paper-reviewer/SKILL.md`

Load each dependency only when its stage begins. These paths are the runtime contract; `.claude/`, `.claude-plugin/`, external slash-command registries, fixed model declarations, and Anthropic credentials are not dependencies.

## Workflow

The canonical progression is:

`research question → literature → evidence → planning → writing → review → revision → finalization`

| Stage | Skill and mode | Required artifact or gate |
|---|---|---|
| 0. Intake | pipeline | Goal, available materials, scope, deliverable, constraints |
| 1. Research question | deep-research `socratic`, `quick`, or `full` | Answerable question and scope |
| 2. Literature | deep-research `lit-review`, `three-way-scan`, or `systematic-review` | Search record and screened corpus |
| 3. Evidence | deep-research `fact-check` plus synthesis | Verified evidence matrix and research-gap chain |
| 4. Planning | academic-paper `plan` or `outline-only` | Approved claim architecture and evidence map |
| 5. Writing | academic-paper `full` | Draft plus independent citation audit status |
| 6. Review | academic-paper-reviewer `full` or focused mode | Immutable reports and revision roadmap |
| 7. Revision | academic-paper `revision`, then reviewer `re-review` as needed | Response matrix, revised draft, residual issues |
| 8. Finalization | academic-paper `citation-check` and `format-convert` | Final verification record and requested output |

## Stage behavior

1. Detect the earliest stage supported by the user's materials. Do not rerun completed work when a valid handoff artifact exists.
2. Before each stage, state the selected skill and mode, required inputs, and expected output.
3. Execute the named skill, then validate the handoff envelope.
4. Require explicit user confirmation for scope/RQ, manuscript outline, unresolved integrity failures, review disposition, and final acceptance. Routine internal transitions can proceed when the user has explicitly asked for a continuous workflow, but integrity failures may not be hidden or silently bypassed.
5. Track source counts and evidence states rather than claiming blanket verification.
6. After any revision, recheck changed claims, citations, figures/tables, and cross-section consistency from the revised artifact.

## Integrity gates

At minimum, run these gates:

- `Evidence gate`: before manuscript drafting, ensure the evidence matrix exists and unsupported claims are visibly marked.
- `Pre-review citation gate`: before reviewer simulation, audit source identity, in-text/reference consistency, and claim support.
- `Reviewer gate`: preserve every major concern and the author's disposition.
- `Final gate`: after revision, independently recheck changed evidence-bearing text and unresolved citations.

A gate report must expose its denominator and limits. `All checked rows passed` does not mean `the entire manuscript is correct` unless completeness was established.

## State record

Maintain a compact state table:

`stage | status | skill | mode | input artifact | output artifact | unresolved issues | user decision`

Allowed statuses are `not_started`, `in_progress`, `blocked`, `awaiting_user`, `complete`, and `skipped_by_scope`. Integrity checks cannot be labeled `skipped_by_scope` when evidence-bearing manuscript text is being finalized.

## Failure handling

- If sources are insufficient, return to literature discovery or narrow the claim; do not draft certainty.
- If the research gap is provisional, preserve that label in planning and writing.
- If the reviewer identifies a conclusion-threatening flaw, pause finalization until the user chooses revision, limitation, or withdrawal of the claim.
- If a required dependency or artifact is missing, report the exact path or field and stop that transition rather than inventing a substitute.
- The user may pause or end the pipeline at any point; return the current state and reusable artifacts.

## Materials-science route

For Al-Sc, Al-Sc-Zr, Al3Sc or Al3(Sc,Zr), precipitation strengthening, recrystallization, grain refinement, microstructure, TEM, SEM, EBSD, or mechanical properties, ensure every substantive skill reads [the materials-science guide](../../../academic-research/references/materials-science-guide.md). Preserve composition, processing, microstructure, and property context through every handoff.
