#!/usr/bin/env python3
"""Offline canonical structural checks. No fact repair or historical judgment."""
from __future__ import annotations
import json,sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator,FormatChecker

def validate_public(text: str,schema:dict) -> dict:
    l=text.splitlines()
    if not l or l[0]!='---':raise ValueError('first line must be ---')
    i=next((i for i in range(1,len(l)-1) if l[i]=='---' and l[i+1]==''),None)
    if i is None:raise ValueError('qualifying front-matter close missing')
    f='\n'.join(l[1:i]);n=yaml.compose(f,Loader=yaml.SafeLoader);d=yaml.safe_load(f)
    # Same source-style check as the reviewed draft.2 README; not inferred from JSON types.
    lns=[] if not isinstance(n,yaml.nodes.MappingNode) else [v for k,v in n.value if isinstance(k,yaml.nodes.ScalarNode) and k.value=='lineage']
    ln=lns[-1] if lns else None
    sn=[] if not isinstance(ln,yaml.nodes.SequenceNode) else [(k,v) for e in ln.value if isinstance(e,yaml.nodes.MappingNode) for k,v in e.value if isinstance(k,yaml.nodes.ScalarNode) and k.value=='seen']
    dl=d.get('lineage') if isinstance(d,dict) else None
    ec=sum(1 for e in dl if isinstance(e,dict) and 'seen' in e) if isinstance(dl,list) else 0
    if not(len(sn)==ec and all(isinstance(v,yaml.nodes.ScalarNode) and v.style in (chr(39),chr(34)) and v.start_mark.index>=k.end_mark.index for k,v in sn)):
        raise ValueError('every lineage[].seen value must be explicitly single- or double-quoted')
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema,format_checker=FormatChecker()).validate(d)
    ids=[e['id'] for e in d.get('self-citation',[]) if 'id' in e]
    if len(ids)!=len(set(ids)):raise ValueError('duplicate self-citation id(s)')
    return d

def main():
    if len(sys.argv)!=3:
        print('Usage: python validate_public.py PROPOSAL_FILE SCHEMA_FILE',file=sys.stderr);return 2
    try:
        d=validate_public(Path(sys.argv[1]).read_text(encoding='utf-8'),json.loads(Path(sys.argv[2]).read_text(encoding='utf-8')))
        print('STRUCTURE=VALID\nHISTORICAL_TRUTH_VERIFIED=NO');return 0
    except Exception as exc:
        print('STRUCTURE=INVALID_OR_UNAVAILABLE\nDETAIL='+str(exc));return 1
if __name__=='__main__':raise SystemExit(main())
