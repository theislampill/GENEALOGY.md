"""Deterministic packaging tests only; no agent authoring or efficacy scoring."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'make-genealogy'
EXPECTED_OPERATOR = '4fe0de4c08c0d56ac73cd54e71b624a211fe6be433dfd65d04b6fea7358c7771'

class Packaging(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extraction = tempfile.TemporaryDirectory()
        with zipfile.ZipFile(ROOT/'dist/make-genealogy.skill') as archive:
            if archive.testzip() is not None:
                raise ValueError('distribution CRC failure')
            archive.extractall(cls.extraction.name)
        cls.distributed = Path(cls.extraction.name)/'make-genealogy'

    @classmethod
    def tearDownClass(cls):
        cls.extraction.cleanup()

    def test_candidate_exists(self):
        self.assertTrue((SKILL / 'SKILL.md').is_file(), 'candidate not built')

    def command(self, folder):
        return subprocess.run([sys.executable, str(folder/'scripts/check_package.py')], capture_output=True, text=True)

    def clone(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        dest = Path(tmp.name) / 'copy'; shutil.copytree(SKILL, dest)
        return dest

    def test_correct_shared_payloads(self):
        m = json.loads((SKILL/'MANIFEST.json').read_text())
        for path, entry in m['files'].items():
            with self.subTest(path=path):
                b = (SKILL/path).read_bytes()
                self.assertEqual(b, (self.distributed/path).read_bytes())
                self.assertEqual(hashlib.sha256(b).hexdigest(), entry['sha256'])
        self.assertEqual(hashlib.sha256((SKILL/'references/operator.md').read_bytes()).hexdigest(), EXPECTED_OPERATOR)

    def test_identical_source_and_packaged_instructions(self):
        self.assertEqual((SKILL/'SKILL.md').read_bytes(), (self.distributed/'SKILL.md').read_bytes())

    def test_identity_checks_both_conditions(self):
        for root in [SKILL, self.distributed]:
            with self.subTest(root=root):
                c = self.command(root); self.assertEqual(c.returncode, 0, c.stdout+c.stderr)
                d = json.loads(c.stdout)
                self.assertEqual(d['status'], 'IDENTITY_VERIFIED')
                self.assertEqual(d['procedure_sha256'], EXPECTED_OPERATOR)

    def test_missing_operator_fails(self):
        p=self.clone(); (p/'references/operator.md').unlink()
        self.assertNotEqual(self.command(p).returncode, 0)

    def test_changed_operator_fails(self):
        p=self.clone(); f=p/'references/operator.md'; f.write_bytes(f.read_bytes()+b'\n')
        self.assertNotEqual(self.command(p).returncode, 0)

    def test_missing_helper_fails(self):
        p=self.clone(); (p/'scripts/validate_public.py').unlink()
        self.assertNotEqual(self.command(p).returncode, 0)

    def test_manifest_cannot_silently_change_operator_binding(self):
        p=self.clone(); f=p/'MANIFEST.json'; d=json.loads(f.read_text()); d['procedure']['sha256']='0'*64; f.write_text(json.dumps(d))
        self.assertNotEqual(self.command(p).returncode, 0)

    def test_declared_handle_mismatch_fails(self):
        p=self.clone(); f=p/'MANIFEST.json'; d=json.loads(f.read_text()); d['name']='another-handle'; f.write_text(json.dumps(d))
        self.assertNotEqual(self.command(p).returncode, 0)

    def test_package_revision_mismatch_fails(self):
        p=self.clone(); f=p/'MANIFEST.json'; d=json.loads(f.read_text()); d['package_version']='9.9.9'; f.write_text(json.dumps(d))
        self.assertNotEqual(self.command(p).returncode, 0)

    def test_stale_standard_binding_fails(self):
        p=self.clone(); f=p/'MANIFEST.json'; d=json.loads(f.read_text()); d['standard']['version']='0.1.0-draft.1'; f.write_text(json.dumps(d))
        self.assertNotEqual(self.command(p).returncode, 0)

    def test_wrong_schema_fails(self):
        p=self.clone(); f=p/'canonical/schema/genealogy.schema.json'; d=json.loads(f.read_text()); d['properties']['genealogy-version']['const']='0.1.0-draft.1'; f.write_text(json.dumps(d))
        self.assertNotEqual(self.command(p).returncode, 0)

    def test_traversal_manifest_fails(self):
        p=self.clone(); f=p/'MANIFEST.json'; d=json.loads(f.read_text()); d['files']['../outside']={'sha256':'0'*64,'bytes':0}; f.write_text(json.dumps(d))
        self.assertNotEqual(self.command(p).returncode, 0)

    def test_symlink_resource_fails(self):
        p=self.clone(); f=p/'references/operator.md'; b=f.read_bytes(); outside=p.parent/'outside'; outside.write_bytes(b); f.unlink(); f.symlink_to(outside)
        self.assertNotEqual(self.command(p).returncode, 0)

    def test_no_mathematical_or_scoring_payload_in_skill(self):
        names=[str(p.relative_to(SKILL)) for p in SKILL.rglob('*') if p.is_file()]
        self.assertFalse(any('PROJECT-LAGRANGIAN' in p or 'scorecard' in p or 'key.json' in p for p in names))
        for p in [SKILL/'SKILL.md', SKILL/'references/operator.md']:
            text=p.read_text().lower()
            self.assertNotIn('gdopl', text); self.assertNotIn('lagrangian', text)

    def test_local_relocation_only(self):
        for name in ['alpha', 'path with spaces café']:
            with tempfile.TemporaryDirectory() as t:
                dest=Path(t)/name;shutil.copytree(SKILL,dest)
                result=self.command(dest);self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_structural_helper_equal_results(self):
        target=ROOT/'GENEALOGY.md'
        outputs=[]
        for base in [SKILL,self.distributed]:
            c=subprocess.run([sys.executable,str(base/'scripts/validate_public.py'),str(target),str(base/'canonical/schema/genealogy.schema.json')],capture_output=True,text=True)
            self.assertEqual(c.returncode,0,c.stdout+c.stderr);outputs.append(c.stdout)
        self.assertEqual(outputs[0],outputs[1]);self.assertIn('STRUCTURE=VALID',outputs[0])

    def test_quoted_date_helper_regressions(self):
        import yaml
        from jsonschema import Draft202012Validator
        spec=importlib.util.spec_from_file_location('f2_validator',SKILL/'scripts/validate_public.py')
        v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
        schema=json.loads((SKILL/'canonical/schema/genealogy.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        for seen in ['2023','2023-05','2023-05-14']:
            for quoted in [False,True]:
                value=json.dumps(seen) if quoted else seen
                text='---\ngenealogy-version: "0.1.0-draft.2"\nproject: {id: "urn:f2:probe"}\nlineage:\n  - source: "https://example.org/f2"\n    subject: "Synthetic validator lexical check, not historical evidence."\n    relationship: "inspired"\n    seen: '+value+'\n---\n\n# Probe\n'
                with self.subTest(seen=seen,quoted=quoted):
                    if quoted: self.assertEqual(v.validate_public(text,schema)['lineage'][0]['seen'],seen)
                    else:
                        with self.assertRaises(ValueError):v.validate_public(text,schema)

    def test_archive_navigation_note(self):
        import re
        self.assertEqual((self.distributed/'canonical/README.md').read_bytes(),
                         (SKILL/'canonical/README.md').read_bytes())
        spec = self.distributed/'canonical/docs/specification.md'
        self.assertIn('../README.md', spec.read_text())
        for path in self.distributed.rglob('*.md'):
            for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
                if '://' in link or link.startswith('#'):
                    continue
                with self.subTest(source=str(path), link=link):
                    self.assertTrue((path.parent/link.split('#')[0]).exists())

    def test_source_distribution_identity(self):
        identity=json.loads((ROOT/'dist/SOURCE-IDENTITY.json').read_text())
        manifest=json.loads((SKILL/'MANIFEST.json').read_text())
        self.assertEqual(manifest['package_version'],'0.1.0-f2.2')
        self.assertEqual(manifest['predecessor_package']['version'],'0.1.0-f2.1')
        self.assertFalse(identity['accepted_f2_artifact_byte_identical'])
        files={p.relative_to(self.distributed).as_posix():
               {'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
               for p in self.distributed.rglob('*') if p.is_file()}
        self.assertEqual(files,identity['distribution_files'])
        actual=hashlib.sha256((json.dumps(files,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
        self.assertEqual(actual,identity['source_file_set_sha256'])
        self.assertEqual(identity['repository_only_exclusion'],[])
        self.assertEqual(len(files),12)
        for line in (self.distributed/'CHECKSUMS.sha256').read_text().splitlines():
            digest,rel=line.split(maxsplit=1)
            self.assertEqual(files[rel]['sha256'],digest)

    def test_independent_rebuild(self):
        with tempfile.TemporaryDirectory(prefix='build path café ') as t:
            target=Path(t)/'make-genealogy.skill'
            result=subprocess.run([sys.executable,str(ROOT/'scripts/build_skill.py'),'--output',str(target)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertEqual(target.read_bytes(),(ROOT/'dist/make-genealogy.skill').read_bytes())

if __name__ == '__main__':
    unittest.main()
