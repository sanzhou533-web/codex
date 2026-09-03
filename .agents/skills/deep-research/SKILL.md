---
name: ars-deep-research
description: Conduct evidence-grounded academic research, literature reviews, research-gap analysis, fact checking, systematic reviews, and meta-analysis. Use for 文献检索, 文献综述, 研究现状, research gap, evidence verification, fact check, systematic review, meta-analysis, or research/mechanism questions about Al-Sc and related materials science topics. Do not use when the primary deliverable is manuscript prose or a referee report.
metadata:
  version: "0.1.0"
  upstream: "Imbad0202/academic-research-skills@94436237913091d4739870159d241660527e8338"
  upstream_skill_version: "2.12.1"
---

# Deep Research

Produce a source-grounded research artifact with a reproducible evidence trail. Read [the shared evidence policy](../../../academic-research/shared/evidence-policy.md) before research. For Al-Sc, Al-Sc-Zr, precipitation, recrystallization, grain refinement, microscopy, or mechanical-property work, also read [the materials-science guide](../../../academic-research/references/materials-science-guide.md).

## Runtime capability gate

Before starting literature discovery, a current-research-status analysis, or a systematic review, verify that the current Codex task has at least one of these evidence inputs:

- working web or literature-search capability; or
- a user-supplied, searchable corpus of papers, PDFs, or source records.

If neither is available, do not pretend to have searched the literature and do not use model memory to claim a current or latest research status. Tell the user exactly: `external literature verification is unavailable`. Ask the user to enable web/search or supply papers/PDFs. A pre-existing evidence matrix may still be used for writing or review, provided its verification status and limits remain visible.

## Modes

Select one mode from [the mode registry](../../../academic-research/references/mode-registry.md):

| Mode | Use when | Minimum output |
|---|---|---|
| `full` | A clear question needs comprehensive analysis | Scope, search record, evidence matrix, synthesis, gaps, limitations |
| `quick` | A bounded rapid brief is requested | Compact source set, verified core claims, uncertainties |
| `review` | The user supplies a paper or research text for source-quality evaluation | Evidence-quality review; do not turn it into a journal referee report |
| `lit-review` | Literature discovery and thematic synthesis are primary | Search strategy, screened bibliography, matrix, themes, disagreements |
| `three-way-scan` | A rapid WHY/HOW/WHAT comparison is sufficient | Deduplicated shortlist, per-paper WHY/HOW/WHAT, cross-paper gaps |
| `fact-check` | Specific claims need verification | Claim-by-claim verdicts and verification trail |
| `socratic` | The research question is vague and the user wants guidance | Questions, user-stated assumptions, scope options; no invented user position |
| `systematic-review` | PRISMA-style review or meta-analysis is explicitly requested | Protocol, reproducible search/screening, risk-of-bias assessment, synthesis |

If the user asks for `meta-analysis`, use `systematic-review`. Perform a quantitative meta-analysis only when compatible effect estimates and sufficient data exist; otherwise explain why narrative synthesis is more defensible.

## Workflow

1. Define the question, population/material state, intervention or processing route, comparator, outcomes, time range, and exclusions. In `socratic`, ask focused narrowing questions and keep candidate questions labeled as system-proposed if the user explicitly requests them.
2. Design database-appropriate queries and record databases, dates, full query concepts, filters, language limits, and deduplication method.
3. Discover candidate sources. Prefer primary research for mechanism and measured effects; use reviews to map the field and secondary sources only for orientation or context.
4. Verify source identity. Cross-check title, authors, year, DOI or stable identifier, publication venue, and retraction/correction status where relevant.
5. Screen sources against the stated scope. Preserve excluded-source reasons for systematic work.
6. Populate the evidence matrix. Extract the actual alloy composition or study population, processing state, methods, quantitative or qualitative result, limitations, and claim locator.
7. Synthesize convergent evidence, contradictory evidence, method-dependent differences, and plausible alternative explanations. Mark inference separately.
8. Build every research-gap claim through the six-part chain in the evidence policy. State the search boundary and gap strength.
9. Report limitations, unresolved metadata, inaccessible full text, and claims that could not be verified.

For detailed procedures, use only the relevant section of [workflow protocols](../../../academic-research/references/workflow-protocols.md).

## Mode-specific constraints

### Literature review

Do not equate a list of papers with a review. Group evidence by mechanism, processing route, measurement method, or competing explanation. Show how source type and method affect confidence.

### Three-way scan

For each paper capture:

- `WHY`: problem and significance.
- `HOW`: material/system, method, and analytical route.
- `WHAT`: result, limitation, and unresolved question.

End with shared motivations, divergent methods, strongest evidence, and a provisional gap.

### Fact check

Decompose compound claims. Return `VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED`, or `CONTRADICTED` per claim, with the exact source trail. A source's existence does not prove claim support.

### Systematic review

Define the protocol before screening. Preserve the search log, inclusion/exclusion rules, deduplication, screening counts, data extraction, risk-of-bias method, and synthesis rationale. Never fabricate PRISMA counts, effect sizes, confidence intervals, heterogeneity statistics, or missing study data.

## Deliverables

Unless the user requests a narrower format, provide:

1. Research question and scope.
2. Search and verification record.
3. Evidence matrix.
4. Thematic or mechanistic synthesis.
5. Contradictions and alternative explanations.
6. Research-gap evidence chains.
7. Limitations and unverified items.
8. Verified reference list with stable links.

## Handoff

When the user next asks for writing, hand off from `ars-deep-research` to `ars-academic-paper` at `../academic-paper/SKILL.md` using [the handoff schema](../../../academic-research/shared/handoff-schema.md). Do not make the writing skill rediscover sources already verified, and do not hide unresolved rows.
