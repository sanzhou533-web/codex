# Evidence and Integrity Policy

This policy applies to all four Academic Research Workspace skills.

## Evidence states

Classify each important statement as one of:

- `VERIFIED`: supported by a located source whose relevant bibliographic identity and claim support were checked.
- `PARTIALLY_VERIFIED`: the source exists, but one or more metadata fields or the exact claim-to-source match remains uncertain.
- `UNVERIFIED`: verification was not completed or no authoritative record was found.
- `CONTRADICTED`: stronger or comparably relevant evidence conflicts with the statement.
- `INFERENCE`: a reasoned interpretation derived from cited evidence, not a direct finding.
- `HYPOTHESIS`: a testable proposal that is not established by the current evidence.

Never silently promote `PARTIALLY_VERIFIED`, `UNVERIFIED`, `INFERENCE`, or `HYPOTHESIS` to fact.

## Bibliographic verification

For each source used substantively, record as many of these fields as the source provides:

| Field | Requirement |
|---|---|
| Title | Compare against a publisher, DOI registry, or authoritative index. |
| Authors | Check order and spelling where available. |
| Year | Resolve online-first versus issue-year differences explicitly. |
| DOI or stable ID | Normalize and test the identifier; never infer one. |
| Source type | Label `primary`, `review`, `systematic-review/meta-analysis`, or `secondary/grey`. |
| Claim support | Note the exact result, section, table, figure, or abstract statement that supports the claim. |
| Verification trail | Retain the authoritative URL(s), access date when relevant, and unresolved conflicts. |

Prefer DOI registries and publisher metadata for identity, then disciplinary indexes and bibliographic databases. Use search engines for discovery, not as the sole authority when primary metadata is available. A real paper can still be an invalid citation if it does not support the associated claim.

## Evidence matrix

Literature-dependent writing should use a matrix with at least:

`source_id | source_type | full_citation | DOI_or_ID | verification_status | study_scope | method | material_or_population | key_result | limitation | supported_claims | contradictory_evidence | locator`

Keep source findings separate from the workspace's synthesis. If the user supplies a source that cannot be verified externally, retain it as user-provided and mark that provenance.

## Research-gap evidence chain

A defensible gap must include:

1. `Established knowledge`: what multiple verified sources support.
2. `Boundary or disagreement`: where evidence conflicts, is weak, or covers only a narrow condition.
3. `Missing test`: the population, alloy state, processing window, scale, method, comparator, or mechanism link not adequately tested.
4. `Why it matters`: the scientific or practical consequence of the missing test.
5. `Search boundary`: databases, query concepts, dates, languages, and source types searched.
6. `Gap strength`: `well-supported`, `provisional`, or `not established`.

Absence from a limited search is not proof that no study exists. Write `we did not identify` within a stated search boundary, not `no research exists`, unless an exhaustive and reproducible review justifies the stronger claim.

## Separation of duties

- Citation checking verifies source identity, source-to-claim support, and reference-list consistency.
- Language polishing improves clarity and style without changing evidence strength.
- Manuscript review evaluates the submitted text and produces a separate report.
- Revision changes the manuscript only after the user requests writing or revision work.

Do not let fluent prose hide missing evidence. Do not treat peer-review simulation as validation of factual accuracy.
