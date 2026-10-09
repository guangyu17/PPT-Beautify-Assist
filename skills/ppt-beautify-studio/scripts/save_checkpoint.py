#!/usr/bin/env python3
"""Persist a small recovery checkpoint; never infer user approval or retry status.
Input is a bounded state JSON assembled from existing evidence. Output contains paths/hashes,
not images, HTML, whole-deck text or Base64. No chats/services are changed.
"""
import argparse
import hashlib
import json
from pathlib import Path
from _common import utf8_stdio


def validate(value):
    if isinstance(value,str):
        if len(value.encode('utf-8')) > 2048 or 'base64,' in value.lower() or '<html' in value.lower():
            raise ValueError('Checkpoint strings must be short plain text or paths, not media/HTML')
    elif isinstance(value,list):
        if len(value)>200:raise ValueError('Use a manifest path instead of a long list')
        for v in value:validate(v)
    elif isinstance(value,dict):
        for k,v in value.items():validate(k);validate(v)
    elif value is not None and not isinstance(value,(int,float,bool)):
        raise ValueError('Unsupported state type')


def save(workspace,state_path,output):
    workspace,state_path,output=map(lambda p:Path(p).resolve(),(workspace,state_path,output))
    if not (workspace/'logs/workspace.json').is_file():
        raise ValueError('Use an initialized workspace')
    if not state_path.is_relative_to(workspace) or not output.is_relative_to(workspace/'logs'):
        raise ValueError('State must be inside workspace; output under logs')
    if output.exists() or output==state_path:
        raise FileExistsError('Use a fresh checkpoint filename')
    if state_path.stat().st_size>16384:
        raise ValueError('State exceeds 16 KiB; replace long content with evidence paths')
    state=json.loads(state_path.read_text(encoding='utf-8-sig'))
    allowed={'mode','phase','style_approval','page_count','current_page','next_action','artifacts','unresolved'}
    if not isinstance(state,dict) or set(state)-allowed:
        raise ValueError('State keys: '+','.join(sorted(allowed)))
    for key in ('mode','phase','style_approval','next_action','artifacts'):
        if key not in state:raise ValueError('Missing '+key)
    validate(state)
    if state['style_approval'] not in ('unconfirmed','confirmed','unknown'):
        raise ValueError('Approval must be explicitly recorded, not inferred')
    if not isinstance(state['artifacts'],dict) or len(state['artifacts'])>16:
        raise ValueError('artifacts must map <=16 short labels to existing evidence paths')
    artifacts={}
    for label,relative in state['artifacts'].items():
        p=(workspace/relative).resolve()
        if not p.is_relative_to(workspace) or not p.is_file():
            raise ValueError('Evidence must be an existing file inside workspace')
        sha=hashlib.sha256()
        with p.open('rb') as handle:
            for chunk in iter(lambda:handle.read(1024*1024),b''):sha.update(chunk)
        artifacts[label]={'path':str(p),'sha256':sha.hexdigest()}
    result={'schema_version':1,'workspace':str(workspace),'state':{**state,'artifacts':artifacts},
            'approval_note':'Copied from caller; does not independently verify human consent. Unknown approval remains unknown.',
            'resume_rule':'Check hashes and preserved generation ledger. Reuse accepted files. Do not reset attempt counts or blindly repeat unknown requests.'}
    raw=json.dumps(result,ensure_ascii=False,indent=2)
    if len(raw.encode('utf-8'))>16384:raise ValueError('Final checkpoint exceeds 16 KiB')
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(raw,encoding='utf-8')
    return {'checkpoint':str(output),'bytes':len(raw.encode('utf-8')),'next_action':state['next_action']}


def main():
    utf8_stdio()
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace',type=Path,required=True);p.add_argument('--state',type=Path,required=True)
    p.add_argument('-o','--output',type=Path,required=True)
    a=p.parse_args();print(json.dumps(save(a.workspace,a.state,a.output),ensure_ascii=False))

if __name__=='__main__':main()
