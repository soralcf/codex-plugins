# Codex compatibility evidence

Verified during this migration with Codex Desktop / CLI runtime 0.153.4 on macOS.

## Runtime checks

An isolated local marketplace and temporary CODEX_HOME were used; the user's plugin registration and installation were not changed.

- plugin/read discovered all 23 names under the nine numbered stage directories.
- plugin/install succeeded.
- skills/list returned all 23 selected names, enabled, with no plugin-specific errors.
- Installed skill trees matched the repository trees, including Codex YAML metadata.
- All 41 selected upstream files other than agents/openai.yaml were byte-identical to commit 3cca18b368ae95cdbdebbff572ccafa662551015.
- A second pinned sync dry run reported no changes.

This proves discovery, packaging and installed content parity. It does not claim that all interactive workflows, external tracker writes, commits or learning sessions were executed. Explicit-only policies are present in the adapted YAML; automatic trigger behavior was not tested with model turns.

## Bundled static validator limitations

The bundled plugin-creator validator is not fully aligned with this runtime:

1. On the real stage layout it reports the nine stage directories as missing SKILL.md because it inspects only immediate children.
2. On a temporary flattened copy of all 23 skills, it reports only the original disable-model-invocation: true field for 12 skills: grill-me, grill-with-docs, handoff, implement, improve-codebase-architecture, teach, to-questionnaire, to-spec, to-tickets, triage, wait-what, wayfinder.
3. It reports no other manifest or YAML errors in the flattened check. The workflow-hub plugin passes its normal validation.

These failures are recorded, not suppressed. No upstream frontmatter or installed validator was changed to produce a pass. The runtime checks inspect the exact selected set and hashes, so a missing nested skill cannot count as success.

## Maintenance

The repository-only skill-maintainer includes verify_codex_plugin.py to repeat isolated runtime verification and test_skill_manager.py to check preservation and removal safeguards. The main registry validator checks the reconstructed upstream tree, the adapted package, generated indexes and dependencies.
