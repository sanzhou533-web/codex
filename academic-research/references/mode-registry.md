# Academic Research Mode Registry

This is the Codex workspace's mode source of truth. It adapts the upstream ARS mode registry without depending on its runtime configuration.

## deep-research

| Mode | Output | Typical intent |
|---|---|---|
| `full` | Comprehensive research report and evidence package | Deep or broad analysis of a clear question |
| `quick` | Bounded research brief | Rapid evidence orientation |
| `review` | Source/research-quality assessment | Evaluate supplied research before relying on it |
| `lit-review` | Search record, bibliography, matrix, thematic synthesis | Literature review or research status |
| `three-way-scan` | WHY/HOW/WHAT shortlist and cross-paper synthesis | Fast comparison of several papers |
| `fact-check` | Claim-level verification report | Fact check or evidence verification |
| `socratic` | Guided question refinement | Vague topic or uncertain research direction |
| `systematic-review` | Protocol-led systematic review; optional defensible meta-analysis | PRISMA, systematic review, meta-analysis |

## academic-paper

| Mode | Output | Typical intent |
|---|---|---|
| `full` | Complete manuscript draft | Write a paper from an adequate evidence base |
| `plan` | Guided paper plan | Decide argument and section structure interactively |
| `outline-only` | Detailed outline and evidence map | Outline without prose drafting |
| `revision` | Revised draft and response/change matrix | Revise a manuscript |
| `revision-coach` | Reviewer-comment roadmap | Interpret comments before editing |
| `abstract-only` | Abstract and keywords | Draft or revise an abstract |
| `lit-review` | Manuscript-style literature-review text | Write a literature-review section or paper |
| `format-convert` | Format-preserving conversion | Change document or citation format |
| `citation-check` | Standalone citation audit | Verify references and claim support |
| `disclosure` | Evidence-bounded disclosure statement | AI-use or contribution disclosure |
| `rebuttal-audit` | Coverage/risk audit of an existing response | Check a rebuttal draft against reviewer comments |

## academic-paper-reviewer

| Mode | Output | Typical intent |
|---|---|---|
| `full` | Multi-perspective reports, synthesis, roadmap | Comprehensive first review |
| `re-review` | Concern-by-concern revision verification | Check whether revisions resolved prior findings |
| `quick` | Journal-fit and blocking-issue brief | Rapid manuscript assessment |
| `methodology-focus` | Methods/statistics/reproducibility review | Focused methodology review |
| `guided` | Socratic issue-by-issue review | Author learning and guided diagnosis |
| `calibration` | Bounded performance comparison against an adjudicated set | Evaluate reviewer behavior without self-certification |

## academic-pipeline

| Mode | Output | Typical intent |
|---|---|---|
| `full` | End-to-end staged workflow | Research question through final manuscript |
| `resume` | Continued workflow from a supplied state/handoff record | Resume without reconstructing completed stages |

## Selection principles

- Explicit user mode wins when its inputs and requested output are compatible.
- Use `academic-pipeline` only for an explicitly end-to-end goal.
- A vague research question favors `deep-research:socratic`; a clear writing request backed by evidence favors `academic-paper`.
- `academic-paper-reviewer` remains read-only. Revision is a separate `academic-paper` action.
- Quantitative meta-analysis is conditional on compatible data, not guaranteed by selecting the mode.
