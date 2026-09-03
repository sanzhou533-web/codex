---
name: ars-academic-paper
description: Plan, outline, draft, revise, rewrite, format, or audit academic manuscripts and abstracts from supplied results or a verified evidence base. Use for 论文规划, outline, academic writing, academic rewriting, draft, revision, citation checking, abstract, or requests to write a section from existing evidence. Do not use for source discovery as the primary goal or for referee-style manuscript assessment.
metadata:
  version: "0.1.0"
  upstream: "Imbad0202/academic-research-skills@94436237913091d4739870159d241660527e8338"
  upstream_skill_version: "3.3.1"
---

# Academic Paper

Create manuscript-ready academic prose without exceeding the evidence. Read [the shared evidence policy](../../../academic-research/shared/evidence-policy.md) first. When research artifacts are supplied, validate and consume [the handoff schema](../../../academic-research/shared/handoff-schema.md). For materials-science manuscripts, read [the materials-science guide](../../../academic-research/references/materials-science-guide.md).

## Modes

Select one mode from [the mode registry](../../../academic-research/references/mode-registry.md):

| Mode | Primary output |
|---|---|
| `full` | Complete manuscript draft in the appropriate scholarly structure |
| `plan` | User-guided paper plan, decisions, and evidence needs |
| `outline-only` | Detailed outline with claim-to-evidence mapping |
| `revision` | Revised text plus a change/response matrix |
| `revision-coach` | Non-ranking revision roadmap from reviewer comments |
| `abstract-only` | Evidence-faithful abstract and keywords |
| `lit-review` | Manuscript-style literature-review section or paper from an evidence matrix |
| `format-convert` | Content-preserving structure or citation-style conversion |
| `citation-check` | Independent citation and reference audit; no language polishing |
| `disclosure` | Venue-aware AI-use or contribution disclosure with policy status stated |
| `rebuttal-audit` | Coverage and risk audit of an existing response draft; no new rebuttal generation |

If reviewer comments are present without a response draft, use `revision-coach`. If both comments and an existing response are present and the user asks to check it, use `rebuttal-audit`. If the user primarily asks for a referee assessment, route to `ars-academic-paper-reviewer` at `../academic-paper-reviewer/SKILL.md`.

## Evidence gate

Before drafting literature-dependent claims:

1. Locate the evidence matrix or build a minimal one from supplied verified sources.
2. Separate the paper's own results from external literature.
3. Mark every planned claim as `supported`, `partially_supported`, `unsupported`, or `author_interpretation`.
4. Do not fill evidence gaps with plausible citations, invented numbers, generic mechanism language, or assumptions about unseen figures.
5. If verification is incomplete, preserve placeholders such as `[citation verification required]` and state what is missing.

Citation checking is an independent task. Do not claim that a citation is valid merely because the prose is polished or the reference is formatted correctly.

## Workflow

1. Confirm or infer only low-risk configuration: deliverable, audience, article type, language, citation style, target length, target venue if supplied, and available materials.
2. Build a claim architecture: contribution, section purposes, claim-evidence links, counter-evidence, and limitations.
3. For `plan` or `outline-only`, stop after the requested planning artifact. Identify evidence still needed instead of drafting around it.
4. Draft from the evidence matrix and author-provided results. Distinguish observed result, literature-supported mechanism, inference, and hypothesis.
5. Check internal consistency among title, abstract, methods, results, figures/tables, discussion, conclusions, and declarations.
6. Run a language-quality pass without changing numeric values, citation meaning, epistemic strength, or author intent.
7. Run `citation-check` separately when requested or before a pipeline handoff to review.

Use [workflow protocols](../../../academic-research/references/workflow-protocols.md) for detailed literature-review, evidence-verification, and revision flows.

## Revision rules

- Preserve the original manuscript and produce a separate revised artifact or explicit patch unless the user requests in-place editing.
- Account for every reviewer concern as `addressed`, `partially_addressed`, `declined_with_reason`, or `not_applicable`.
- Do not accept reviewer suggestions automatically; preserve scientifically justified disagreement.
- Do not introduce new experiments, results, methods, or citations as though they already exist.
- Recheck any citation or claim affected by revision.

## Citation-check output

Report independently:

- in-text/reference-list mismatches;
- metadata conflicts in title, authors, year, venue, DOI, volume, issue, or pages;
- source existence status;
- source-to-claim support;
- primary/review/secondary source class;
- retraction, correction, or version concerns when found;
- required fixes and items that remain unverified.

## Deliverables

Include the requested manuscript artifact plus a compact evidence note describing the matrix used, unresolved claims, and whether citation verification was run. Full manuscripts should include limitations and the declarations appropriate to the venue and study type; do not invent ethics approval, funding, data availability, author contributions, or conflicts of interest.

## Handoff

For assessment, hand off from `ars-academic-paper` to `ars-academic-paper-reviewer` at `../academic-paper-reviewer/SKILL.md`, passing an immutable review copy, manuscript version, evidence matrix, and citation-audit status through [the handoff schema](../../../academic-research/shared/handoff-schema.md). In a full workflow, return control to `ars-academic-pipeline` at `../academic-pipeline/SKILL.md` after the stage artifact is complete.
