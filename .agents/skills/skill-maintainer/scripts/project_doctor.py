"""Read-only project prerequisite checks. File presence is not semantic approval."""
import json
from pathlib import Path


TRACKER = {'triage', 'wayfinder', 'to-spec', 'to-tickets', 'code-review'}
DOMAIN = TRACKER | {'domain-modeling', 'codebase-design', 'improve-codebase-architecture'}


def inspect_project(catalog, project, skill=None, workflow=None, spec=None):
    project = Path(project).resolve()
    if not project.is_dir():
        raise ValueError(f'Project directory not found: {project}')
    if skill:
        if skill not in catalog.skills: raise ValueError(f'Unknown skill: {skill}')
        selected = {skill}
    elif workflow:
        match = next((w for w in catalog.workflows_doc['workflows'] if w['id'] == workflow), None)
        if not match: raise ValueError(f'Unknown workflow: {workflow}')
        selected = set(match['skills'])
    else:
        selected = {i['name'] for i in catalog.selected('mattpocock')}
    pending = list(selected)
    while pending:
        name = pending.pop()
        for dependency in catalog.skills[name].get('requires', []):
            if dependency not in selected:
                selected.add(dependency)
                pending.append(dependency)
    config_path = project / '.skill-project.json'
    config = json.loads(config_path.read_text()) if config_path.exists() else {}
    if not isinstance(config, dict): raise ValueError('.skill-project.json must be an object')
    checks = []

    def file_check(key, default, required=True):
        value = config.get(key, default)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'{key} must be a non-empty path')
        path = (project / value).resolve()
        if not path.is_relative_to(project):
            raise ValueError(f'{key} must resolve inside the project')
        present = path.is_file() and bool(path.read_text(encoding='utf-8').strip())
        checks.append({'check': key, 'status': 'ok' if present else ('missing' if required else 'warning'),
                       'path': str(path), 'detail': 'Non-empty file found; contents require review' if present else 'Provide a non-empty file'})
        return path

    if selected & TRACKER:
        # code-review explicitly requires this fixed path in its unchanged upstream instructions.
        if 'code-review' in selected and config.get('issueTracker', 'docs/agents/issue-tracker.md') != 'docs/agents/issue-tracker.md':
            raise ValueError('code-review requires docs/agents/issue-tracker.md; retain an adapter at that path')
        file_check('issueTracker', 'docs/agents/issue-tracker.md')
        file_check('agentInstructions', 'AGENTS.md')
    if selected & {'triage', 'to-spec', 'to-tickets'}:
        file_check('triageLabels', 'docs/agents/triage-labels.md')
    if selected & DOMAIN:
        file_check('domainGuide', 'docs/agents/domain.md', required=False)
        file_check('glossary', 'CONTEXT.md', required=False)
    if selected & {'implement', 'to-tickets', 'code-review'}:
        provided = spec or config.get('spec')
        if provided:
            if not isinstance(provided, str): raise ValueError('spec must be a path string')
            config['spec'] = provided
            file_check('spec', provided)
        else:
            checks.append({'check': 'spec', 'status': 'warning', 'detail': 'Pass --spec PATH to check a local spec/ticket. Conversation or remote inputs require manual review.'})
    if 'implement' in selected:
        commands = config.get('checks', [])
        if not isinstance(commands, list) or any(not isinstance(s, str) or not s.strip() for s in commands):
            raise ValueError('checks must be a list of non-empty command strings')
        checks.append({'check': 'projectChecks', 'status': 'ok' if commands else 'warning',
                       'detail': 'Check commands declared; not executed' if commands else 'Declare project check commands in .skill-project.json'})
    if 'teach' in selected:
        checks.append({'check': 'learningWorkspace', 'status': 'warning',
                       'detail': 'Confirm this is the intended writable workspace for learning records, lessons and assets; no files were created'})
    return {'project': str(project), 'skills': sorted(selected), 'checks': checks,
            'missing': sum(c['status'] == 'missing' for c in checks),
            'warnings': sum(c['status'] == 'warning' for c in checks),
            'scope': 'Local prerequisite presence only; no semantic, permission or remote-service verification'}


def doctor(catalog, project, skill=None, workflow=None, spec=None, as_json=False):
    report = inspect_project(catalog, project, skill, workflow, spec)
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for check in report['checks']:
            print(f"{check['status'].upper()}: {check['check']}: {check.get('path', '')} {check['detail']}")
        print(f"{report['missing']} missing; {report['warnings']} warnings. {report['scope']}")
    return 1 if report['missing'] else 0
