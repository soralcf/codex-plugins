#!/usr/bin/env python3
"""Regression checks for preservation and removal safeguards on the real catalog."""
import contextlib
import io
from pathlib import Path
import shutil
import tempfile
import unittest

from skill_manager import Catalog, DEFAULT_ROOT, validate, remove_skill


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
        with contextlib.redirect_stdout(io.StringIO()):
            result = remove_skill(self.catalog, 'code-review', True)
        self.assertEqual(result, 1)
        self.assertTrue((self.root / self.catalog.skills['code-review']['path']).is_dir())

    def test_stage_path_mismatch_detected(self):
        self.catalog.skills['teach']['stage'] = '10-discovery'
        code, errors = self.check_validation()
        self.assertEqual(code, 1)
        self.assertIn('teach: destination does not match stage', errors)


if __name__ == '__main__':
    unittest.main()
