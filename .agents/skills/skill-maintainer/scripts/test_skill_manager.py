#!/usr/bin/env python3
"""Regression checks for preservation and removal safeguards on the real catalog."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

import skill_manager
from skill_manager import Catalog, DEFAULT_ROOT, validate, remove_skill
from project_doctor import inspect_project


class CatalogSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='matt-catalog-test-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for directory in ('plugins', 'registry', '.agents/skills'):
            shutil.copytree(DEFAULT_ROOT / directory, self.root / directory,
                            ignore=shutil.ignore_patterns('__pycache__'))
        self.catalog = Catalog(self.root)

    def check_validation(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = validate(self.catalog)
        return code, output.getvalue()

    def test_valid_nested_package(self):
        self.assertEqual(self.check_validation()[0], 0)

    def test_upstream_edit_detected_even_with_valid_overlay(self):
        item = self.catalog.skills['teach']
        path = self.root / item['path'] / 'SKILL.md'
        path.write_text(path.read_text() + '\nUnexpected behavioral change.\n')
        code, errors = self.check_validation()
        self.assertEqual(code, 1)
        self.assertIn('teach: vendored content differs from lock', errors)

    def test_yaml_policy_drift_detected(self):
        item = self.catalog.skills['teach']
        path = self.root / item['path'] / 'agents/openai.yaml'
        path.write_text(path.read_text().replace('allow_implicit_invocation: false', 'allow_implicit_invocation: true'))
        code, errors = self.check_validation()
        self.assertEqual(code, 1)
        self.assertIn('teach: Codex overlay differs from registry', errors)
        self.assertNotIn('teach: vendored content differs from lock', errors)

    def test_dependency_blocks_nested_removal(self):
        # Remove workflow edges to exercise skill dependency protection alone.
        self.catalog.workflows_doc['workflows'] = []
        self.catalog.workflows_path.write_text(json.dumps(self.catalog.workflows_doc))
        with contextlib.redirect_stdout(io.StringIO()):
            result = remove_skill(self.catalog, 'code-review', True)
        self.assertEqual(result, 1)
        self.assertTrue((self.root / self.catalog.skills['code-review']['path']).is_dir())

    def test_stage_path_mismatch_detected(self):
        self.catalog.skills['teach']['stage'] = '10-discovery'
        code, errors = self.check_validation()
        self.assertEqual(code, 1)
        self.assertIn('teach: destination does not match stage', errors)

    def test_removal_refreshes_owning_plugin_version(self):
        self.catalog.workflows_doc['workflows'] = []
        self.catalog.workflows_path.write_text(json.dumps(self.catalog.workflows_doc))
        manifest = self.root / 'plugins/vendor-mattpocock/.codex-plugin/plugin.json'
        before = json.loads(manifest.read_text())['version']
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(remove_skill(self.catalog, 'teach', True), 0)
        after = json.loads(manifest.read_text())['version']
        self.assertNotEqual(before, after)
        self.assertEqual(self.check_validation()[0], 0)

    def test_failed_removal_restores_all_managed_files(self):
        self.catalog.workflows_doc['workflows'] = []
        self.catalog.workflows_path.write_text(json.dumps(self.catalog.workflows_doc))
        with contextlib.redirect_stdout(io.StringIO()):
            skill_manager.write_catalog(self.catalog, True)
        before = {p.relative_to(self.root).as_posix(): p.read_bytes()
                  for base in ('plugins', 'registry')
                  for p in (self.root / base).rglob('*') if p.is_file()}
        with mock.patch.object(skill_manager, 'write_catalog', side_effect=RuntimeError('injected failure')):
            with contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(RuntimeError, 'injected failure'):
                    remove_skill(self.catalog, 'teach', True)
        after = {p.relative_to(self.root).as_posix(): p.read_bytes()
                 for base in ('plugins', 'registry')
                 for p in (self.root / base).rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(self.check_validation()[0], 0)

    def test_failed_sync_restores_all_managed_files(self):
        before = {p.relative_to(self.root).as_posix(): p.read_bytes()
                  for base in ('plugins', 'registry')
                  for p in (self.root / base).rglob('*') if p.is_file()}

        def local_checkout(source, ref, destination):
            destination.mkdir()
            lock = json.loads((self.root / source['lockPath']).read_text())
            locked = {item['name']: item for item in lock['skills']}
            for item in self.catalog.selected('mattpocock'):
                target = destination / item['origin']['path']
                shutil.copytree(self.root / item['path'], target)
                original = locked[item['name']]['upstreamOpenaiYaml']
                yaml = target / 'agents/openai.yaml'
                if original is None:
                    yaml.unlink()
                    if not any(yaml.parent.iterdir()): yaml.parent.rmdir()
                else:
                    yaml.write_text(original)
            shutil.copy2(self.root / 'plugins/vendor-mattpocock/LICENSE', destination / 'LICENSE')
            return lock['commit'], lock['committedAt']

        with mock.patch.object(skill_manager, 'checkout_source', side_effect=local_checkout), \
             mock.patch.object(skill_manager, 'write_catalog', side_effect=RuntimeError('injected sync failure')):
            with contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(RuntimeError, 'injected sync failure'):
                    skill_manager.sync_vendor(self.catalog, 'mattpocock', 'local-ref', True)
        after = {p.relative_to(self.root).as_posix(): p.read_bytes()
                 for base in ('plugins', 'registry')
                 for p in (self.root / base).rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(self.check_validation()[0], 0)

    def test_workflow_branch_without_condition_is_rejected(self):
        workflow = next(w for w in self.catalog.workflows_doc['workflows'] if w['id'] == 'matt-learning')
        workflow['relations'][0].pop('when')
        code, errors = self.check_validation()
        self.assertEqual(code, 1)
        self.assertIn('conditional relation needs when', errors)

    def test_project_doctor_expands_dependencies_without_writing(self):
        project = self.root / 'project'
        project.mkdir()
        before = list(project.iterdir())
        report = inspect_project(self.catalog, project, skill='implement')
        self.assertEqual(before, list(project.iterdir()))
        self.assertIn('code-review', report['skills'])
        self.assertIn('tdd', report['skills'])
        self.assertGreater(report['missing'], 0)

    def test_require_current_signals_an_upstream_update(self):
        lock = json.loads((self.root / 'plugins/vendor-mattpocock/UPSTREAM.lock.json').read_text())
        with mock.patch.object(skill_manager, 'remote_head', return_value='f' * 40), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(skill_manager.check_upstream(self.catalog, 'mattpocock', True), 1)
        with mock.patch.object(skill_manager, 'remote_head', return_value=lock['commit']), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(skill_manager.check_upstream(self.catalog, 'mattpocock', True), 0)


if __name__ == '__main__':
    unittest.main()
