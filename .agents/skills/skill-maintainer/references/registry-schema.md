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
explicit entry Skill, ordered `skills`, and desired `outcome`. Every referenced Skill must exist.

The generated `workflow-guide/references/catalog.md` is a distribution artifact, not a source of
truth. Regenerate it from both JSON registries.
