---
name: skill-maintainer
description: Maintain this marketplace repository's skill catalog. Use when inventorying skills, validating workflows and dependencies, checking or syncing vendored upstream skills, adding a source selection, or safely removing a skill.
---

# Skill Maintainer

Maintain the repository as two planes:

- The runtime plane contains installable plugins and `workflow-guide`.
- The maintenance plane contains this repository-only skill, the registries, and upstream locks.

Do not put maintenance commands into distributed third-party plugins.

## Start here

Run from the repository root:

```bash
python3 .agents/skills/skill-maintainer/scripts/skill_manager.py inventory
python3 .agents/skills/skill-maintainer/scripts/skill_manager.py validate
```

Read [references/maintenance-policy.md](references/maintenance-policy.md) before importing,
syncing, or removing anything. Read [references/registry-schema.md](references/registry-schema.md)
when changing either registry.

## Choose the operation

- **Inventory or audit:** use `inventory` and `validate`. These are read-only.
- **Check project prerequisites:** run `doctor --project <path>` with either `--skill <name>` or `--workflow <id>`. Add `--spec <path>` for a local spec. It only checks local presence and never runs configured commands or contacts a tracker.
- **Verify Codex loading:** run `python3 .agents/skills/skill-maintainer/scripts/verify_codex_plugin.py`; it installs a copy in a temporary CODEX_HOME and checks every selected name and file hash without changing the user installation.
- **Refresh the guide:** run `render-catalog`; add `--apply` only when the generated diff is intended.
- **Check upstream:** run `check-upstream --source <id>`. Add `--require-current` in scheduled automation so an available update produces a failing signal. This is read-only but needs network access.
- **Sync selected third-party skills:** first run `sync-vendor --source <id>` without `--apply`.
  Review the commit and changed skill list, then run again with `--apply` when the user requested
  the update.
- **Add a third-party skill:** verify its license, add one `ownership: vendored` registry entry with
  an exact upstream path and reviewed hard dependencies, then use `sync-vendor`. Never copy an
  unregistered directory into the plugin.
- **Remove a vendored skill:** run `remove --skill <name>` first. Use `--apply` only after the user
  chose that exact skill and the command reports no workflow or dependency blockers.
- **Create an original replacement:** use `skill-creator` and give it a new name. Never modify a
  vendored directory and relabel it as original.

After every applied change, run `validate`, validate affected plugin manifests with
`plugin-creator`, and inspect `git diff`. Installation, commits, pushes, and removal of separately
installed local copies are separate actions; perform them only when requested.
