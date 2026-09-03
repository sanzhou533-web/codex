# Cross-Skill Handoff Schema

Use this schema whenever an output moves between academic skills. A handoff may be Markdown, YAML, or JSON, but it must preserve the same fields and must point to actual artifacts rather than reconstructing them from memory.

## Handoff envelope

```yaml
handoff_version: "1.0"
from_skill: ars-deep-research
from_mode: lit-review
to_skill: ars-academic-paper
requested_next_mode: full
topic: "..."
research_question: "..."
scope:
  included: []
  excluded: []
artifacts:
  evidence_matrix: "path or inline artifact id"
  search_record: "path or inline artifact id"
  synthesis: "path or inline artifact id"
  manuscript: null
  review_report: null
verification_summary:
  verified_sources: 0
  partially_verified_sources: 0
  unverified_sources: 0
  unresolved_conflicts: []
epistemic_limits: []
user_decisions: []
next_gate: "user approval or named integrity check"
```

## Required transitions

### ars-deep-research to ars-academic-paper

Pass the research question, scope, reproducible search record, deduplicated bibliography, evidence matrix, synthesis, research-gap chain, and unresolved evidence conflicts. The paper skill must not present unverified rows as established evidence.

### ars-academic-paper to ars-academic-paper-reviewer

Pass the immutable review copy, target journal or review standard if known, manuscript version/hash, evidence matrix, citation-audit status, author-declared limitations, and any questions the author wants reviewers to examine. Reviewers return reports separately and do not edit this copy.

### ars-academic-paper-reviewer to ars-academic-paper

Pass every concern with `id`, `severity`, `location`, `evidence`, `rationale`, and `minimum_remedy`. Preserve disagreements and user decisions. Revision must account for each concern as `addressed`, `partially_addressed`, `declined_with_reason`, or `not_applicable`.

### ars-academic-paper to final verification

Pass the revised manuscript, change log, response matrix, evidence matrix, and citation audit. Recheck changed claims and references; do not assume a prior check still applies after revision.

## Integrity conditions

- Do not omit unresolved issues during handoff.
- Do not infer user approval.
- Keep source identifiers and paths stable.
- Mark missing artifacts explicitly rather than fabricating substitutes.
- Record whether each artifact is user-supplied, tool-generated, or externally verified.
