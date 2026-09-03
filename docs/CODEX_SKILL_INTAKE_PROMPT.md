# Reusable Codex Skill Intake Prompt

Replace `SOURCE_REPOSITORY_URL` and the explicitly requested skill or suite name before using this prompt in a Codex task opened at the repository root.

```text
Integrate the explicitly specified academic skill or suite from:

SOURCE_REPOSITORY_URL

Requested skill or suite:
EXPLICIT_SKILL_OR_SUITE_NAME

Work directly in this repository. Do not install, copy, or register any other skill that I did not explicitly request. Preserve all existing skills and routing behavior. Do not modify main directly.

Follow docs/SKILL_INTEGRATION_GUIDE.md and complete this sequence:

inspect source
→ pin version/commit
→ decide license and redistribution boundaries
→ audit scripts, network, filesystem, credentials, tokens, MCP, and runtime dependencies
→ adapt to Codex project-local skill structure
→ assign a collision-resistant namespace
→ update routing without overriding more appropriate existing skills
→ update skill-registry/REGISTRY.md and skill-sources/SOURCES.md
→ run static validation
→ verify actual Codex discovery with /skills or the current selector
→ test explicit $skill-name invocation
→ run at least one positive and one negative implicit-routing test
→ run the four ARS regression cases
→ inspect the full git diff for credentials, tokens, caches, temporary files, private data, and unrelated large files
→ commit and create a dedicated pull request to main

License rules:

- Record repository owner, source URL, immutable commit, LICENSE, NOTICE, attribution, commercial restrictions, and share-alike requirements.
- If adaptation or redistribution rights are unclear, do not copy substantial source text; report the blocker.
- Preserve required full license and notice files.

Runtime rules:

- Rewrite or isolate Claude, Cursor, proprietary tool, fixed-model, hook, slash-command, unsupported agent-dispatch, and API assumptions.
- Do not declare nonexistent tools, MCP servers, credentials, or dependencies.
- Do not enable high-risk behavior by default.

Validation report:

- List actual and expected skill identity for discovery, explicit invocation, positive implicit routing, negative implicit routing, and ARS regression.
- Keep deterministic router tests clearly separate from live Codex runtime tests.
- Report every unresolved license, security, dependency, or routing concern.

Do not automatically merge the new pull request. Stop after pushing the branch and creating the PR.
```
