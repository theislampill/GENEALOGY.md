# `GENEALOGY.md`

A draft, human- and machine-readable convention for **feature-level provenance** and **implementation lineage** in open-source repositories.

## Draft status

The current convention version is `0.1.0-draft.2`. It is ready for trial use, not presented as an adopted industry standard.

The [experimental authoring skill](skills/README.md) is optional and is not part of conformance. The [methodology/research note](docs/research/README.md) is non-normative; neither addition changes the convention.

The format has two independently optional functions:

- **Self-citation:** publish a narrow, feature-scoped answer to “when should descendants acknowledge this project, and what does not count?”
- **Lineage:** record affirmative statements about particular antecedents, including inspiration, translation, reimplementation, or behavioural reproduction where no artifact-level copy may exist.

A lineage list is **not an exhaustive inventory**. Missing entries carry no negative meaning. They do not assert independent invention, deny a relationship, or prove that an antecedent search occurred.

## Why this exists

Licence notices, SPDX, REUSE, SBOMs, package manifests, Git history, credits, and `CITATION.cff` each solve important problems. They do not provide one lightweight repository interface for saying:

> This particular feature or method came from, was translated from, was behaviourally reproduced from, or was materially inspired by this particular source.

Coding agents make that middle layer easier to lose because they can translate code, reconstruct distinctive structures, and reproduce behaviour without preserving an obvious textual trail. `GENEALOGY.md` standardises how a maintainer may publish known relationships; it does not compel honesty or independently verify them.

## Five-minute adoption

There are two ways to author a `GENEALOGY.md`. Both produce the same convention document; using the skill is **not** required for conformance.

### Assisted authoring with `make-genealogy`

If your coding-agent host supports Agent Skills, the experimental [`make-genealogy`](skills/README.md) skill is the convenient assisted route for creating or updating a repository's `GENEALOGY.md`.

It packages the bounded authoring procedure, the pinned draft.2 resources, and a fail-closed structural validator. The procedure is designed to preserve an existing file, distinguish supported public lineage from unresolved candidates, avoid invented precision, and ask only when a material authoring decision cannot responsibly be made from the available evidence.

1. Import [`dist/make-genealogy.skill`](dist/make-genealogy.skill) using your host's supported skill mechanism, or expose the editable [`skills/make-genealogy/`](skills/make-genealogy/) directory where your host can load skills.
2. Invoke `make-genealogy` for the repository you want to document.
3. Review the proposed `GENEALOGY.md`; the skill does not establish historical truth or publication authority.
4. Run the bundled structural validator before publishing.

Native installation, discovery and invocation have not yet been comparatively qualified across hosts. If your runtime does not recognise the package, see the [experimental status, boundaries and direct validation instructions](skills/README.md).

### Manual authoring

If you are not using the skill:

1. Copy [`templates/GENEALOGY.md`](templates/GENEALOGY.md) to the root of your repository as `GENEALOGY.md`.
2. Copy [`schema/genealogy.schema.json`](schema/genealogy.schema.json) to the same relative path in your repository.
3. Replace the template placeholders and keep at least one non-empty `self-citation` or `lineage` block.
4. Quote every `seen` value, for example `seen: "2026-09-02"`.
5. Run one of the fail-closed validation commands below.

`seen` may be quoted as a year (`"2023"`), month (`"2023-05"`), or full date (`"2023-05-14"`). Missing components are not defaults. Use optional `seen-qualifier: approximate|uncertain|approximate-and-uncertain` when the reported period itself is qualified. Do not append EDTF-style `?` or `~`, and do not invent January 1 for an unknown month or day.

Minimal self-citation-only example:

```yaml
---
genealogy-version: "0.1.0-draft.2"
project:
  id: "https://github.com/example/project"
  name: "Example Project"
self-citation:
  - id: "retry-state-transition"
    subject: "The retry-state transition pattern used by the task governor."
    cite-when:
      - "Substantially reimplementing this transition structure."
    do-not-cite-when:
      - "Using the same public retry API without adopting this structure."
---

# Genealogy
```

`lineage` is optional. Add an entry only when the project has a reasonable basis to publish the affirmative statement. See the root [`GENEALOGY.md`](GENEALOGY.md) for a dogfooded example containing both blocks.

## Self-service validation

The experimental skill carries the maintained validator at [`skills/make-genealogy/scripts/validate_public.py`](skills/make-genealogy/scripts/validate_public.py). The standalone commands below mirror its core draft.2 checks for manual adopters: they install [PyYAML](https://pyyaml.org/) plus `jsonschema` with non-GPL format support, verify that URI checking is actually registered and working, extract the first qualifying YAML front-matter block, require every `lineage[].seen` scalar to be explicitly quoted, validate the decoded data against the local schema, reject duplicate local subject IDs, and print `GENEALOGY.md: valid` on success.

If URI-format capability is unavailable or inert, these commands fail rather than reporting the document valid. They use explicit runtime checks rather than Python `assert`, so optimisation mode cannot erase the guards.

### Bash

```bash
python -m pip install --quiet PyYAML 'jsonschema[format-nongpl]' && python -c 'import json,pathlib,yaml; from jsonschema import Draft202012Validator,FormatChecker; req=lambda c,m: c or (_ for _ in ()).throw(ValueError(m)); p=pathlib.Path("GENEALOGY.md"); l=p.read_text(encoding="utf-8").splitlines(); req(l and l[0]=="---", "first line must be ---"); i=next(i for i in range(1,len(l)-1) if l[i]=="---" and l[i+1]==""); f="\n".join(l[1:i]); n=yaml.compose(f,Loader=yaml.SafeLoader); d=yaml.safe_load(f); lns=[] if not isinstance(n,yaml.nodes.MappingNode) else [v for k,v in n.value if isinstance(k,yaml.nodes.ScalarNode) and k.value=="lineage"]; ln=lns[-1] if lns else None; sn=[] if not isinstance(ln,yaml.nodes.SequenceNode) else [(k,v) for e in ln.value if isinstance(e,yaml.nodes.MappingNode) for k,v in e.value if isinstance(k,yaml.nodes.ScalarNode) and k.value=="seen"]; dl=d.get("lineage") if isinstance(d,dict) else None; ec=sum(1 for e in dl if isinstance(e,dict) and "seen" in e) if isinstance(dl,list) else 0; req(len(sn)==ec and all(isinstance(v,yaml.nodes.ScalarNode) and v.style in (chr(39),chr(34)) and v.start_mark.index>=k.end_mark.index for k,v in sn), "every lineage[].seen value must be explicitly single- or double-quoted"); s=json.loads(pathlib.Path("schema/genealogy.schema.json").read_text(encoding="utf-8")); Draft202012Validator.check_schema(s); fc=FormatChecker(); req("uri" in fc.checkers and fc.conforms("https://example.org/validation-control","uri") and fc.conforms("urn:example:validation-control","uri") and not fc.conforms("not a uri","uri"), "required uri format validation unavailable or inert"); Draft202012Validator(s,format_checker=fc).validate(d); ids=[e["id"] for e in d.get("self-citation",[]) if "id" in e]; dup=sorted({x for x in ids if ids.count(x)>1}); req(not dup, "duplicate self-citation id(s): "+", ".join(dup)); print("GENEALOGY.md: valid")'
```

### PowerShell

```powershell
py -m pip install --quiet PyYAML "jsonschema[format-nongpl]"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
py -c "import json,pathlib,yaml; from jsonschema import Draft202012Validator,FormatChecker; req=lambda c,m: c or (_ for _ in ()).throw(ValueError(m)); p=pathlib.Path('GENEALOGY.md'); l=p.read_text(encoding='utf-8').splitlines(); req(l and l[0]=='---', 'first line must be ---'); i=next(i for i in range(1,len(l)-1) if l[i]=='---' and l[i+1]==''); f='\n'.join(l[1:i]); n=yaml.compose(f,Loader=yaml.SafeLoader); d=yaml.safe_load(f); lns=[] if not isinstance(n,yaml.nodes.MappingNode) else [v for k,v in n.value if isinstance(k,yaml.nodes.ScalarNode) and k.value=='lineage']; ln=lns[-1] if lns else None; sn=[] if not isinstance(ln,yaml.nodes.SequenceNode) else [(k,v) for e in ln.value if isinstance(e,yaml.nodes.MappingNode) for k,v in e.value if isinstance(k,yaml.nodes.ScalarNode) and k.value=='seen']; dl=d.get('lineage') if isinstance(d,dict) else None; ec=sum(1 for e in dl if isinstance(e,dict) and 'seen' in e) if isinstance(dl,list) else 0; req(len(sn)==ec and all(isinstance(v,yaml.nodes.ScalarNode) and v.style in (chr(39),chr(34)) and v.start_mark.index>=k.end_mark.index for k,v in sn), 'every lineage[].seen value must be explicitly single- or double-quoted'); s=json.loads(pathlib.Path('schema/genealogy.schema.json').read_text(encoding='utf-8')); Draft202012Validator.check_schema(s); fc=FormatChecker(); req('uri' in fc.checkers and fc.conforms('https://example.org/validation-control','uri') and fc.conforms('urn:example:validation-control','uri') and not fc.conforms('not a uri','uri'), 'required uri format validation unavailable or inert'); Draft202012Validator(s,format_checker=fc).validate(d); ids=[e['id'] for e in d.get('self-citation',[]) if 'id' in e]; dup=sorted({x for x in ids if ids.count(x)>1}); req(not dup, 'duplicate self-citation id(s): '+', '.join(dup)); print('GENEALOGY.md: valid')"
```

The closing delimiter is the first later standalone `---` followed immediately by a blank line. A Markdown horizontal rule written as `---` after that close is ordinary body content and does not affect extraction.

## What the format does not do

`GENEALOGY.md` does not:

- establish copying, derivation, infringement, priority, ownership, or entitlement to credit;
- claim that omitted sources do not exist;
- replace licence notices, REUSE, SPDX, an SBOM, `CITATION.cff`, or Git history;
- make a published provenance statement legally neutral; or
- resolve uncertain or disputed licensing questions.

Before publishing a strong lineage characterisation involving restrictively licensed material, review the upstream licence and seek qualified legal advice where ownership, permission, compatibility, or obligations are unclear.

## Files

### Normative draft standard and repository

- [Draft specification](docs/specification.md)
- [Copyable template](templates/GENEALOGY.md)
- [JSON Schema](schema/genealogy.schema.json)
- [This repository's genealogy](GENEALOGY.md)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [MIT licence](LICENSE)

### Experimental authoring skill

- [Status and usage boundaries](skills/README.md)
- [Skill source](skills/make-genealogy/SKILL.md)
- [Generated experimental archive and build identity](dist/README.md)

### Non-normative methodology and design

- [The Cost of a Decisive Revision: Evidence, Reuse, and Self-Application](docs/research/README.md)
- [Inner authoring and outer project-evolution models](docs/design/authoring-model.md)

## Licence

This repository is licensed under the [MIT License](LICENSE).
