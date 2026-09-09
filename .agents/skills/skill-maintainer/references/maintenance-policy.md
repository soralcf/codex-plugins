# Skill maintenance policy

## Ownership classes

- `vendored`: a directory from a pinned upstream source. Preserve every upstream file except the explicitly authorized `agents/openai.yaml` Codex adaptation. Updates replace the directory, then regenerate that adaptation. Retain original YAML and upstream/packaged hashes in the lock.
- `original`: maintained in this repository. It may learn from general ideas elsewhere, but must
  not silently preserve copied third-party text or assets.

If a vendored skill needs behavioral changes, remove it from the selection and design a new,
separately named original skill.

## Import requirements

Before selecting a third-party skill:

1. Verify the current upstream repository and exact source path.
2. Read the governing license and preserve every required notice.
3. Classify it as user-invoked or model-invoked from its unchanged metadata.
4. Record hard dependencies in `registry/skills.json` and select their transitive closure.
5. Check for overlap with original skills and platform-native behavior.
6. Pin one upstream commit in the plugin lock.

Do not import draft, deprecated, personal, or repository-specific routing/setup skills by default.
For the Matt package, retain original frontmatter even when the bundled static validator rejects it. Report static-validator incompatibilities and verify every selected skill through an isolated Codex plugin install and skills/list scan. Never use nested-directory omissions as validation evidence. Runtime failures remain blockers; YAML does not replace project prerequisites.

## Sync requirements

- Fetch into a temporary checkout.
- Copy only registered upstream paths.
- Derive numbered destination paths from the registry. Adapt only agents/openai.yaml; keep its original contents in the lock and validate reconstructed upstream and final packaged trees separately.
- Replace the complete vendored `skills/` tree, not individual files.
- Refresh content hashes, the upstream commit, preserved license, plugin cachebuster, and generated
  workflow catalog in the same operation.
- Derive cachebusters from both the upstream commit and selected-content hash, so changing the
  selection at the same commit cannot reuse a stale installed cache.
- Review the upstream diff before applying a new commit.

## Removal requirements

- Resolve the exact registry name.
- Refuse removal while another skill declares it in `requires` or a workflow references it.
- Remove the whole skill directory and its registry/lock entry together.
- Do not claim a skill is unused without usage evidence. Static analysis can prove only that it is
  unreferenced or has overlapping responsibilities.

Tracked files remain recoverable from Git. The manager does not delete separately installed user
copies or caches.
