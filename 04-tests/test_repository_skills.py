"""The repository checker must validate nested installable skills, not just the parent."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class NestedSkillChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for item in ROOT.iterdir():
            if item.name.startswith('.') or item.name == 'dist':
                continue
            if item.is_file():
                shutil.copy2(item, self.root / item.name)
            elif item.name in ('01-skills', '02-docs', '03-examples', '04-tests', '05-tools'):
                shutil.copytree(item, self.root / item.name,
                                ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        self.child = self.root / '01-skills/ppt-beautify-studio/subskills/fixture-design'
        self.child.mkdir(parents=True, exist_ok=True)
        for folder in (self.child, self.child.parent):
            (folder / 'README.md').write_text('# Test fixture\n', encoding='utf-8')
        self.write_skill('name: fixture-design\ndescription: A valid fixture\nmetadata:\n  version: "1.0.0"')

    def write_skill(self, metadata, body='Fixture instructions.'):
        (self.child / 'SKILL.md').write_text(f'---\n{metadata}\n---\n{body}\n', encoding='utf-8')

    def check(self):
        return subprocess.run([sys.executable, '-X', 'utf8', str(self.root/'05-tools/check_repository.py')],
                              capture_output=True, text=True, encoding='utf-8')

    def test_valid_nested_skill_passes(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_nested_name_mismatch_is_rejected(self):
        self.write_skill('name: wrong-design\ndescription: A fixture')
        self.assertNotEqual(self.check().returncode, 0)

    def test_nested_missing_description_is_rejected(self):
        self.write_skill('name: fixture-design')
        self.assertNotEqual(self.check().returncode, 0)

    def test_nested_empty_instructions_are_rejected(self):
        self.write_skill('name: fixture-design\ndescription: A fixture', body='')
        self.assertNotEqual(self.check().returncode, 0)

    def test_nested_malformed_metadata_is_rejected(self):
        self.write_skill('name: [\ndescription: A fixture')
        self.assertNotEqual(self.check().returncode, 0)


if __name__ == '__main__':
    unittest.main()
