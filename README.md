# Soralcf Codex Plugins

Public Codex plugin marketplace for reusable skills and personal workflows.

## Clone the repository

```bash
git clone https://github.com/soralcf/codex-plugins.git
```

## Add the marketplace

```bash
codex plugin marketplace add https://github.com/soralcf/codex-plugins.git --ref main
```

## Install a plugin

```bash
codex plugin add <plugin-name>@soralcf
```

## Plugins

- `learn-anything` — Learn any topic through adaptive explanations, guided practice, and practical roadmaps.
- `vendor-mattpocock` — 23 pinned Matt Pocock skills organized into nine work stages, with original content and separate Codex metadata adaptation. [Stage guide](plugins/vendor-mattpocock/README.md).
- `workflow-hub` — A personal guide for navigating and auditing the maintained skill workflows.

```bash
codex plugin add learn-anything@soralcf
codex plugin add vendor-mattpocock@soralcf
codex plugin add workflow-hub@soralcf
```

## Skill organization

- `plugins/vendor-*` contains third-party skill content and an upstream lock file. Matt skills use numbered stage folders and separately tracked Codex YAML adaptations.
- Original distributable skills live in capability-oriented plugins such as `learn-anything` and `workflow-hub`.
- `registry/skills.json` records ownership, invocation mode, source, and dependencies.
- `registry/workflows.json` records the maintained workflow compositions.
- `.agents/skills/skill-maintainer` validates and synchronizes this repository; it is not distributed as a plugin.

Vendored SKILL.md files and supporting content are never patched locally. The Matt plugin permits only agents/openai.yaml adaptation, retaining the upstream YAML snapshot and original tree hash in the lock. Update from the pinned upstream commit with the maintenance script; behavioral rewrites belong in separately named original skills.
