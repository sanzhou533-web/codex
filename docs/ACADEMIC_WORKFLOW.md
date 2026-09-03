# Academic Research Workspace

This repository provides four project-local Codex skills for evidence-grounded research, manuscript writing, peer review, and end-to-end research-to-paper work. The repository-level [academic router](../AGENTS.md) selects one skill by intent and loads detailed resources progressively.

## Skill responsibilities

| Skill | Responsibility | Typical deliverable |
|---|---|---|
| [`ars-deep-research`](../.agents/skills/deep-research/SKILL.md) | Source discovery, literature review, evidence verification, synthesis, research-gap analysis, systematic review, and optional defensible meta-analysis | Search record, verified bibliography, evidence matrix, synthesis, gap chain |
| [`ars-academic-paper`](../.agents/skills/academic-paper/SKILL.md) | Paper planning, outlining, drafting, revision, abstract writing, citation checking, disclosure, and format conversion | Outline or manuscript artifact plus evidence/citation status |
| [`ars-academic-paper-reviewer`](../.agents/skills/academic-paper-reviewer/SKILL.md) | Read-only peer review, methodology assessment, reviewer simulation, and revision verification | Anchored review report, editorial recommendation, revision roadmap |
| [`ars-academic-pipeline`](../.agents/skills/academic-pipeline/SKILL.md) | Orchestration across research, literature, evidence, writing, review, revision, and finalization | State record and validated cross-skill handoffs |

All skills share the [evidence policy](../academic-research/shared/evidence-policy.md) and [handoff schema](../academic-research/shared/handoff-schema.md). Modes are defined in the [mode registry](../academic-research/references/mode-registry.md).

## Automatic selection

The root router applies explicit end-to-end intent first, then review intent, writing intent, and research intent:

| Request signal | Selected skill |
|---|---|
| `完整科研流程`, `research to paper`, `从研究问题到论文终稿`, `full academic workflow` | `ars-academic-pipeline` |
| `审稿`, `peer review`, `manuscript assessment`, `methodology review`, `reviewer simulation` | `ars-academic-paper-reviewer` |
| `论文规划`, `outline`, `academic writing`, `academic rewriting`, `draft`, `revision`, `citation checking`, `abstract` | `ars-academic-paper` |
| `文献检索`, `文献综述`, `研究现状`, `research gap`, `evidence verification`, `fact check`, `systematic review`, `meta-analysis` | `ars-deep-research` |

The pipeline is not selected merely because a request contains several academic words. It requires end-to-end intent. Explicit skill or mode selection overrides automatic routing when the requested artifact and supplied inputs are compatible.

### Materials-science priority

Al-Sc alloys, Al-Sc-Zr alloys, Al3Sc or Al3(Sc,Zr) precipitation, precipitation strengthening, recrystallization, grain refinement, microstructure, TEM, SEM, EBSD, and mechanical properties are priority domain signals. When they occur with research, literature, evidence, mechanism, paper, or review intent, the academic router takes precedence over a generic response.

Task intent still determines the skill:

- research status, literature, mechanism synthesis, evidence, or gaps → `ars-deep-research`;
- section or manuscript writing → `ars-academic-paper`;
- referee-style assessment → `ars-academic-paper-reviewer`;
- explicitly complete research-to-final-paper work → `ars-academic-pipeline`.

## Manual invocation

Open a Codex task at the repository root and name the skill and optional mode:

```text
$ars-deep-research mode=lit-review
Analyze ...
```

```text
$ars-academic-paper mode=revision
Revise the attached draft using this frozen reviewer concern table ...
```

If the client does not expose `$skill-name` completion, use the explicit path form:

```text
Use the `ars-academic-paper-reviewer` project skill at .agents/skills/academic-paper-reviewer/SKILL.md in methodology-focus mode.
```

Reusable examples live in [`academic-research/commands/`](../academic-research/commands/). These are prompt recipes, not Claude-style slash-command declarations.

## Literature-review workflow

1. Define an answerable scope: material/population, process or exposure, comparator, outcomes, methods, time range, languages, and exclusions.
2. Build database-specific queries with synonyms and notation variants.
3. Record databases, complete search concepts, dates, filters, and access limits.
4. Deduplicate and screen. For systematic work, preserve counts and exclusion reasons.
5. Verify source identity using DOI/publisher records and authoritative indexes.
6. Classify sources as primary research, review/systematic review, or secondary/grey literature.
7. Extract findings, conditions, methods, limitations, and locators into the evidence matrix.
8. Synthesize themes, mechanisms, disagreements, and method-dependent differences.
9. Report search limits, inaccessible full text, unresolved metadata, and evidence gaps.

Use `ars-deep-research:three-way-scan` for a rapid WHY/HOW/WHAT shortlist, `lit-review` for thematic synthesis, and `systematic-review` for a protocol-led PRISMA-style process. Before any literature discovery, current-status analysis, or systematic review, the skill checks for web/search access or a user-supplied searchable paper/PDF/source corpus. Without either, it reports `external literature verification is unavailable` and requests an evidence source instead of claiming a current review from model memory. A meta-analysis is performed only when compatible data justify it.

## Research-gap workflow

A research gap is not a rhetorical sentence at the end of a review. The workspace builds an evidence chain:

1. verified established knowledge;
2. the precise boundary, contradiction, or weakly tested condition;
3. the missing experiment, comparator, material state, scale, or mechanism link;
4. why resolving it matters;
5. the databases, queries, dates, languages, and source classes searched;
6. a strength label: `well-supported`, `provisional`, or `not established`.

Author claims that a field is unexplored are treated as claims to verify. The preferred wording for a bounded search is “we did not identify studies meeting these criteria,” not an unqualified “no research exists.”

## Evidence-verification workflow

Evidence verification is separate from writing quality and citation formatting:

1. Split prose into atomic claims.
2. Verify that each cited item exists and that title, authors, year, and DOI/stable ID agree across authoritative records where reasonably possible.
3. Locate the exact passage, table, figure, or result relevant to the claim.
4. Compare direction, magnitude, material/population, processing conditions, and uncertainty.
5. Assign `VERIFIED`, `PARTIALLY_VERIFIED`, `UNVERIFIED`, or `CONTRADICTED`.
6. Label inference and hypothesis separately from reported findings.
7. Record correction, retraction, version, and contradictory-evidence concerns.
8. Return an audit trail and required fixes without polishing the prose during the audit.

## Manuscript-review workflow

The reviewer skill keeps the submitted manuscript immutable:

1. establish review scope, paper type, target venue/standard if supplied, and manuscript version;
2. evaluate fit and contribution separately from scientific validity;
3. review methodology, evidence, statistics, reproducibility, citations, figures/tables, interpretation, and reporting;
4. anchor each concern to manuscript evidence;
5. test alternative explanations and whether the conclusions respect limitations;
6. for full review, freeze role-separated perspectives before editorial synthesis;
7. provide categorical concerns, minimum remedies, and a reasoned recommendation;
8. hand the frozen concern table to `ars-academic-paper:revision` only when the user requests revision.

For re-review, compare the original concern, claimed author action, original text, revised text, and observed evidence. A response letter is not proof that the manuscript changed.

## Full academic pipeline

The full workflow is:

```text
research question
  → literature
  → verified evidence matrix
  → research-gap chain
  → manuscript plan
  → evidence-grounded draft
  → independent citation audit
  → read-only peer review
  → author-directed revision
  → re-review and final verification
  → requested final format
```

The pipeline resolves dependencies in this order:

`ars-academic-pipeline → ars-deep-research → ars-academic-paper → ars-academic-paper-reviewer`

After review, control returns to `ars-academic-paper:revision`; `ars-academic-paper-reviewer` may then run `re-review`. Each transition uses the shared handoff envelope so unresolved evidence and reviewer concerns are not lost. The pipeline maintains a state table with stage, status, skill, mode, input/output artifacts, unresolved issues, and user decisions.

Important gates are:

- evidence matrix before drafting;
- citation and claim-support audit before review;
- explicit disposition of every major reviewer concern before revision;
- fresh verification of changed claims and citations after revision;
- visible unresolved integrity limits before finalization.

## Al-Sc example prompts

Research status and gap:

```text
系统分析 Al-Sc-Zr 合金中 Al3(Sc,Zr) 析出相对再结晶抑制机制的研究现状，并识别 research gap。要求区分原始研究和综述，交叉核验 DOI、题名、作者与年份，并给出 gap evidence chain。
```

Mechanism-focused literature review:

```text
$ars-deep-research mode=lit-review
比较不同热机械路径下 Al3Sc 与 Al3(Sc,Zr) 析出、粗化、Zener pinning 和再结晶行为；将合金成分、处理制度、TEM/EBSD 证据与力学性能放入 evidence matrix。
```

Systematic review:

```text
$ars-deep-research mode=systematic-review
设计并执行 Al-Sc-Zr 合金微合金化对再结晶温度和晶粒稳定性影响的系统综述。先冻结纳入标准；若数据不可比，不要强行 meta-analysis。
```

Writing from evidence:

```text
$ars-academic-paper mode=full
根据所附 evidence matrix 帮我写“Al3(Sc,Zr) 析出相对再结晶抑制机制”章节。把直接证据、推断和待验证假设分开，缺失证据保留占位符。
```

Reviewer simulation:

```text
$ars-academic-paper-reviewer mode=methodology-focus
以材料学期刊审稿人的标准检查这一章节，重点审查 TEM/EBSD 证据是否足以支持析出相钉扎晶界并抑制再结晶的因果表述。保持原稿只读。
```

Full workflow:

```text
$ars-academic-pipeline mode=full
从 Al-Sc-Zr 合金再结晶抑制机理的研究问题开始，完成文献检索、证据矩阵、research gap、章节规划、论文写作、审稿、修订和终稿验证。
```

## Validation

Run the project smoke test from the repository root:

```text
python academic-research/scripts/smoke_test.py
```

This script performs deterministic static validation only: it checks the four skill entrypoints, frontmatter, desktop metadata, relative links, the pipeline dependency chain, the full upstream license, Claude-runtime exclusions, and routing-rule fixtures. It is not a Codex implicit-invocation test. Real discovery and routing must be checked in a fresh Codex runtime with `/skills`, `$` completion, or equivalent runtime evidence.

### Codex runtime verification record

On 2026-09-03, a fresh Codex CLI 0.153.0-alpha.5 session was opened at the repository root. `/skills` displayed `ARS Deep Research`, `ARS Academic Paper`, `ARS Academic Paper Reviewer`, and `ARS Academic Pipeline`. Four separate read-only, ephemeral Codex runs then applied implicit routing without executing the substantive research, writing, or review task:

| Test | Prompt intent | Actual selected skill | Expected skill | Result |
|---|---|---|---|---|
| A | Al-Sc-Zr research status and research gap | `ars-deep-research` | `ars-deep-research` | PASS |
| B | Write Results and Discussion from an existing evidence matrix | `ars-academic-paper` | `ars-academic-paper` | PASS |
| C | Materials-journal review of a section | `ars-academic-paper-reviewer` | `ars-academic-paper-reviewer` | PASS |
| D | Research question through literature, evidence, writing, review, and revision | `ars-academic-pipeline` | `ars-academic-pipeline` | PASS |

This is a runtime selection record, not output from `smoke_test.py`. Each run also returned a distinctive loaded-skill instruction: the external-literature capability gate, evidence-matrix drafting gate, read-only review boundary, or end-to-end-only pipeline rule, respectively.

## Attribution

This workspace is a Codex-focused adaptation of Academic Research Skills by Cheng-I Wu. See the [notice](../academic-research/NOTICE.md), [complete license](../academic-research/LICENSE), and [adaptation notes](../academic-research/references/codex-adaptation.md).
