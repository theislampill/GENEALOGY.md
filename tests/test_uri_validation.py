"""B1 regressions. Run using an isolated environment installed from skill requirements."""
import importlib.metadata
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/make-genealogy'
HELPER = SKILL / 'scripts/validate_public.py'
SCHEMA_PATH = SKILL / 'canonical/schema/genealogy.schema.json'
spec = importlib.util.spec_from_file_location('uri_validator_under_test', HELPER)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
SCHEMA = json.loads(SCHEMA_PATH.read_text())


def document(project='https://example.org/project', source='https://example.org/source',
             seen='"2023-05"', qualifier=None):
    extra = '' if qualifier is None else '    seen-qualifier: ' + json.dumps(qualifier) + '\n'
    return ('---\ngenealogy-version: "0.1.0-draft.2"\nproject:\n  id: '
            + json.dumps(project) + '\nlineage:\n  - source: ' + json.dumps(source)
            + '\n    subject: "Synthetic validation check."\n    relationship: "inspired"\n'
            + '    seen: ' + seen + '\n' + extra + '---\n\n# Validation check\n')


class UriValidation(unittest.TestCase):
    def cli(self, text, modification='', flags=('-I',), before_import=''):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'GENEALOGY.md'
            target.write_text(text, encoding='utf-8')
            code = ('import importlib.util,sys; ' + before_import +
                    f's=importlib.util.spec_from_file_location("test_helper",{str(HELPER)!r}); '
                    'm=importlib.util.module_from_spec(s); s.loader.exec_module(m); '
                    + modification + f'sys.argv=[{str(HELPER)!r},{str(target)!r},{str(SCHEMA_PATH)!r}]; '
                    'raise SystemExit(m.main())')
            return subprocess.run([sys.executable, '-B', *flags, '-c', code],
                                  capture_output=True, text=True, timeout=30)

    def assert_terminal(self, result, code, structure, status):
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        self.assertIn('STRUCTURE=' + structure + '\n', result.stdout)
        self.assertIn('VALIDATION_STATUS=' + status + '\n', result.stdout)
        if code:
            self.assertNotIn('STRUCTURE=VALID\n', result.stdout)

    def test_declared_dependency_contract(self):
        self.assertEqual((SKILL/'requirements.txt').read_text().splitlines(),
                         ['PyYAML==6.0.3', 'jsonschema[format-nongpl]==4.26.0'])

    def test_provisioned_checker_rejects_invalid_control(self):
        self.assertEqual(importlib.metadata.version('jsonschema'), '4.26.0')
        self.assertEqual(importlib.metadata.version('PyYAML'), '6.0.3')
        from jsonschema import FormatChecker
        from jsonschema.exceptions import FormatError
        checker = FormatChecker()
        self.assertIn('uri', checker.checkers)
        checker.check('https://example.org/control', 'uri')
        with self.assertRaises(FormatError):
            checker.check('not a uri', 'uri')

    def test_invalid_project_uri(self):
        self.assert_terminal(self.cli(document(project='not a uri')), 1, 'INVALID', 'INVALID_DOCUMENT')

    def test_invalid_lineage_source_uri(self):
        self.assert_terminal(self.cli(document(source='not a uri')), 1, 'INVALID', 'INVALID_DOCUMENT')

    def test_valid_uris(self):
        for uri in ['https://example.org/a_b?x=1&y=2', 'urn:example:control', 'mailto:test@example.org']:
            with self.subTest(uri=uri):
                self.assert_terminal(self.cli(document(uri, uri)), 0, 'VALID', 'VALID_DOCUMENT')

    def test_missing_registry_entry_fails_closed(self):
        for text in [document(), document(project='not a uri'), document(source='not a uri')]:
            with self.subTest(text=text):
                self.assert_terminal(self.cli(text, 'm.FormatChecker.checkers.pop("uri",None); '),
                                     2, 'UNAVAILABLE', 'VALIDATION_CAPABILITY_UNAVAILABLE')

    def test_registered_noop_checker_fails_closed(self):
        self.assert_terminal(self.cli(document(), 'm.FormatChecker.checkers["uri"]=(lambda x:True,()); '),
                             2, 'UNAVAILABLE', 'VALIDATION_CAPABILITY_UNAVAILABLE')

    def test_registered_reject_all_checker_is_unavailable(self):
        self.assert_terminal(self.cli(document(), 'm.FormatChecker.checkers["uri"]=(lambda x:False,()); '),
                             2, 'UNAVAILABLE', 'VALIDATION_CAPABILITY_UNAVAILABLE')

    def test_checker_runtime_error_is_unavailable(self):
        self.assert_terminal(self.cli(document(), 'm.FormatChecker.checkers["uri"]=(lambda x:1/0,()); '),
                             2, 'UNAVAILABLE', 'VALIDATION_CAPABILITY_UNAVAILABLE')

    def test_missing_checker_guard_survives_optimized_python(self):
        self.assert_terminal(self.cli(document(), 'm.FormatChecker.checkers.pop("uri",None); ', ('-I','-O')),
                             2, 'UNAVAILABLE', 'VALIDATION_CAPABILITY_UNAVAILABLE')

    def test_all_third_party_dependencies_unavailable(self):
        self.assert_terminal(self.cli(document(), flags=('-I','-S')),
                             2, 'UNAVAILABLE', 'VALIDATION_CAPABILITY_UNAVAILABLE')

    def test_uri_backends_hidden_before_jsonschema_import(self):
        # A fresh interpreter prevents already imported backends masking absence.
        blocker = ("import importlib.abc\n"
                   "class HideUri(importlib.abc.MetaPathFinder):\n"
                   "    def find_spec(self, fullname, path=None, target=None):\n"
                   "        if fullname.split('.')[0] in {'rfc3987','rfc3986_validator'}:\n"
                   "            raise ModuleNotFoundError('URI backend deliberately hidden')\n"
                   "sys.meta_path.insert(0, HideUri())\n")
        for text in [document(), document(project='not a uri'), document(source='not a uri')]:
            result=self.cli(text, 'assert "uri" not in m.FormatChecker.checkers; ',
                            before_import='exec('+repr(blocker)+'); ')
            self.assert_terminal(result,2,'UNAVAILABLE','VALIDATION_CAPABILITY_UNAVAILABLE')

    def test_schema_and_precision_matrix_unchanged(self):
        from jsonschema import Draft202012Validator
        Draft202012Validator.check_schema(SCHEMA)
        for period in ['2023', '2023-05', '2023-05-14']:
            for quote in ['"', "'"]:
                for qualifier in [None, 'approximate', 'uncertain', 'approximate-and-uncertain']:
                    with self.subTest(period=period, quote=quote, qualifier=qualifier):
                        data = helper.validate_public(document(seen=quote+period+quote, qualifier=qualifier), SCHEMA)
                        self.assertEqual(data['lineage'][0]['seen'], period)

    def test_unquoted_forms_rejected(self):
        for period in ['2023','2023-05','2023-05-14']:
            with self.subTest(period=period):
                with self.assertRaisesRegex(ValueError, 'explicitly single- or double-quoted'):
                    helper.validate_public(document(seen=period), SCHEMA)

    def test_full_date_calendar_and_qualifier_behaviour_unchanged(self):
        from jsonschema.exceptions import ValidationError
        for period in ['0000', '2023-00', '2023-13', '2023-02-29', '2023-04-31', '1900-02-29', '2023?', '2023~']:
            with self.subTest(period=period):
                with self.assertRaises(ValidationError):
                    helper.validate_public(document(seen=json.dumps(period)), SCHEMA)
        for period in ['2000-02-29','2024-02-29','2023-04-30']:
            self.assertEqual(helper.validate_public(document(seen=json.dumps(period)), SCHEMA)['lineage'][0]['seen'],period)
        with self.assertRaises(ValidationError):
            helper.validate_public(document(qualifier='roughly'), SCHEMA)

    def test_quotation_failure_cli_is_invalid_not_unavailable(self):
        self.assert_terminal(self.cli(document(seen='2023-05')), 1, 'INVALID', 'INVALID_DOCUMENT')

    def test_root_and_template_remain_valid(self):
        for path in [ROOT/'GENEALOGY.md', ROOT/'templates/GENEALOGY.md']:
            with self.subTest(path=path):
                helper.validate_public(path.read_text(), SCHEMA)

    def test_flow_mapping_quote_styles(self):
        for q in ['"', "'"]:
            text=('---\ngenealogy-version: "0.1.0-draft.2"\nproject: {id: "urn:example:test"}\n'
                  'lineage: [{source: "https://example.org/source", subject: "Test", relationship: "inspired", '
                  'seen: '+q+'2023-05'+q+'}]\n---\n\n')
            self.assertEqual(helper.validate_public(text, SCHEMA)['lineage'][0]['seen'],'2023-05')

    def test_bad_schema_is_validation_unavailable(self):
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'GENEALOGY.md'; target.write_text(document())
            schema=Path(temp)/'bad.json'; schema.write_text('{"type":42}')
            c=subprocess.run([sys.executable,'-I',str(HELPER),str(target),str(schema)],capture_output=True,text=True)
            self.assert_terminal(c,2,'UNAVAILABLE','VALIDATION_CAPABILITY_UNAVAILABLE')


if __name__ == '__main__':
    unittest.main()
