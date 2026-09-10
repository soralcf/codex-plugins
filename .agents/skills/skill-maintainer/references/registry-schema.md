# Registry schema

`registry/skills.json` is the source of truth for availability and provenance.

Each skill entry contains:

- `name`: unique Skill frontmatter name.
- `plugin`: owning plugin name, or `null` for a repository-only Skill.
- `ownership`: `original` or `vendored`.
- `scope`: `plugin` or `repository`.
- `invocation`: `user` or `model`.
- `status`: lifecycle state; currently `active`.
- `path`: repository-relative directory containing `SKILL.md`.
- `origin`: required for vendored entries; contains a source id and upstream directory path.
- `requires`: hard Skill dependencies that must be present. Optional or contextual relationships do
  not belong here.

Top-level `sources` defines the upstream repository, branch, license, plugin, and lock path.
Its `exclusions` array records stable upstream Skill paths that were deliberately not selected and
the current reason. Move or remove an exclusion when the decision changes; never leave one name in
both the selected Skill list and exclusions.

`registry/workflows.json` contains named compositions. Each workflow has an `id`, human title,
primary `entry`, optional `entries`, member `skills`, typed `relations`, and desired `outcome`.
Relations use `sequence`, `optional`, `calls`, `choice`, or `alongside`; conditional choices and
optional edges include `when`. Every member is an entry or participates in a relation. Sequence
edges must be acyclic. The member list records coverage and does not imply an execution order.

The generated `workflow-guide/references/catalog.md` is a distribution artifact, not a source of
truth. Regenerate it from both JSON registries.

## Stage organization and Codex adaptation

- Top-level `stages` lists ordered ids and titles. Numbers aid navigation, not mandatory execution.
- `stage` selects a stage; `path` is `plugins/<plugin>/skills/<stage>/<name>`.
- `codex` contains `displayName` and `shortDescription`; the adapter generates a namespaced default prompt and preserves registry invocation mode. Only agents/openai.yaml may change.
- `requires` includes skills invoked by supported branches so the package is complete; it is not a sequence for the human to execute.
- `prerequisites` records project configuration and input artifacts, not installable dependencies.
- The lock retains `treeSha256` for the original upstream tree, `upstreamOpenaiYaml` for its original YAML, `packagedTreeSha256` for the adapted tree, and `path` for placement.

`render-catalog --apply` also generates the Matt README stage/dependency index. WORKFLOWS.md and PROJECT-SETUP.md are maintained packaging documentation.
