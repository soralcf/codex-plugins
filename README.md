# Soralcf Codex Plugins

Private Codex plugin marketplace for personal plugins.

## Add the marketplace

```bash
codex plugin marketplace add soralcf/codex-plugins --ref main
```

## Install a plugin

```bash
codex plugin add <plugin-name>@soralcf
```

## Plugins

- `learn-anything` — Learn any topic through adaptive explanations, guided practice, and practical roadmaps.
- `vendor-mattpocock` — A pinned, unmodified subset of Matt Pocock's MIT-licensed engineering and productivity skills.
- `workflow-hub` — A personal guide for navigating and auditing the maintained skill workflows.

```bash
codex plugin add learn-anything@soralcf
codex plugin add vendor-mattpocock@soralcf
codex plugin add workflow-hub@soralcf
```

## Skill organization

- `plugins/vendor-*` contains unmodified third-party skill directories and an upstream lock file.
- Original distributable skills live in capability-oriented plugins such as `learn-anything` and `workflow-hub`.
- `registry/skills.json` records ownership, invocation mode, source, and dependencies.
- `registry/workflows.json` records the maintained workflow compositions.
- `.agents/skills/skill-maintainer` validates and synchronizes this repository; it is not distributed as a plugin.

Vendored skills are never patched locally. Update them as complete directories from the pinned upstream commit, or remove them and create a separately named original skill.
