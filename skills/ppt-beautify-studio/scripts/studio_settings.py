#!/usr/bin/env python3
"""Persistent non-secret preferences. Default native; explicit changes only.
Never stores keys or changes another skill's configuration. User preferences live outside repo.
"""
import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
from _common import utf8_stdio

DEFAULTS = Path(__file__).resolve().parents[1] / 'config/defaults.json'
BACKENDS = ('native', 'ifapi', 'relay')
TIERS = ('ultra', 'high', 'medium', 'low')


def preference_path():
    home = Path(os.environ.get('CODEX_HOME', Path.home() / '.codex'))
    return home / 'ppt-beautify-studio/preferences.json'


def validate(settings):
    allowed={'schema_version','backend','tier','relay_config_path','ifapi_model','ifapi_guard'}
    if not isinstance(settings,dict) or set(settings)!=allowed:raise ValueError('Unknown/missing preference fields; never store credentials here')
    if settings['schema_version']!=1 or settings['backend'] not in BACKENDS:raise ValueError('Invalid backend or schema')
    if settings['tier'] is not None and settings['tier'] not in TIERS:raise ValueError('Invalid tier')
    if settings['ifapi_model']!='gpt-image-2.5-sunburst':raise ValueError('IF API model is preserved unless a later explicit model-support change is implemented')
    relay=settings['relay_config_path']
    if relay is not None and (not isinstance(relay,str) or not Path(relay).is_absolute()):raise ValueError('Relay config must be an absolute local path, not a URL or credential')
    guard=settings['ifapi_guard']
    if not isinstance(guard,dict) or set(guard)!={'enabled','reported_rejected_bytes','budget_bytes','basis','fix_evidence'}:raise ValueError('Invalid guard configuration')
    if type(guard['enabled']) is not bool:raise ValueError('enabled must be boolean')
    for key in ('reported_rejected_bytes','budget_bytes'):
        if type(guard[key]) is not int or guard[key]<=0:raise ValueError('Byte counts must be positive integers')
    if not isinstance(guard['basis'],str) or len(guard['basis'])>1000:raise ValueError('Invalid guard basis')
    if guard['fix_evidence'] is not None and (not isinstance(guard['fix_evidence'],str) or len(guard['fix_evidence'])>1000):raise ValueError('Evidence must be a short non-secret note')
    if not guard['enabled'] and not guard['fix_evidence']:raise ValueError('Disabled guard requires recorded verified-fix evidence')
    return settings


def load(path=None):
    default=json.loads(DEFAULTS.read_text(encoding='utf-8-sig'))
    target=Path(path) if path else preference_path()
    return validate(json.loads(target.read_text(encoding='utf-8-sig'))) if target.exists() else validate(default)


def update(path=None, backend=None, tier=None, clear_tier=False, relay_config=None,
           budget=None, guard=None, evidence=None, confirmed=False):
    if not confirmed:raise ValueError('Changing persistent preferences requires explicit user instruction (--confirmed)')
    target=(Path(path) if path else preference_path()).resolve()
    result=deepcopy(load(target))
    if backend is not None:result['backend']=backend
    if tier is not None:result['tier']=tier
    if clear_tier:result['tier']=None
    if relay_config is not None:
        resolved=Path(relay_config).expanduser().resolve()
        if not resolved.is_file():raise FileNotFoundError('Relay configuration path not found; its contents are never printed')
        result['relay_config_path']=str(resolved)
    if budget is not None:result['ifapi_guard']['budget_bytes']=budget
    if guard is not None:
        if guard=='off' and not evidence:raise ValueError('Do not auto-disable by version; need confirmed fix evidence')
        result['ifapi_guard']['enabled']=guard=='on'
        result['ifapi_guard']['fix_evidence']=evidence if guard=='off' else None
    validate(result)
    target.parent.mkdir(parents=True,exist_ok=True)
    fd,temporary=tempfile.mkstemp(dir=target.parent,suffix='.tmp')
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as handle:json.dump(result,handle,ensure_ascii=False,indent=2)
        os.replace(temporary,target)
    finally:
        if Path(temporary).exists():Path(temporary).unlink()
    return result


def main():
    utf8_stdio();p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--file',type=Path,help='Test/explicit preference file; otherwise outside skill/repo under CODEX_HOME')
    subs=p.add_subparsers(dest='command',required=True);subs.add_parser('show')
    change=subs.add_parser('set');change.add_argument('--backend',choices=BACKENDS);change.add_argument('--tier',choices=TIERS)
    change.add_argument('--clear-tier',action='store_true');change.add_argument('--relay-config',type=Path)
    change.add_argument('--budget-bytes',type=int);change.add_argument('--ifapi-guard',choices=('on','off'))
    change.add_argument('--fix-evidence');change.add_argument('--confirmed',action='store_true')
    a=p.parse_args()
    if a.command=='show':result=load(a.file)
    else:
        result=update(a.file,a.backend,a.tier,a.clear_tier,a.relay_config,a.budget_bytes,a.ifapi_guard,a.fix_evidence,a.confirmed)
    print(json.dumps({'settings':result,'preferences_file':str((a.file or preference_path()).resolve())},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
