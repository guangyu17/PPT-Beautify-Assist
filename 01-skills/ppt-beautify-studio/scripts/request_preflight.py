#!/usr/bin/env python3
"""Byte preflight, NOT an HTTP client/interceptor. Never replays a request.
A complete serialized body may be measured exactly. Tool arguments/partial manifests
cannot certify a hidden Desktop /responses body: they return needs_capture (exit 2).
"""
import argparse
import hashlib
import json
from pathlib import Path
from studio_settings import load, BACKENDS
from _common import utf8_stdio


def fingerprint(path):
    digest=hashlib.sha256();total=0
    with Path(path).open('rb') as handle:
        for block in iter(lambda:handle.read(1024*1024),b''):
            total+=len(block);digest.update(block)
    return total,digest.hexdigest()


def inspect_request(backend=None, body=None, complete=False, manifest=None, preferences=None, transport='default'):
    settings=load(preferences);backend=backend or settings['backend']
    if backend not in BACKENDS:raise ValueError('Unknown backend')
    if transport not in ('default','ifapi-desktop'):raise ValueError('Unknown transport')
    if body and manifest:raise ValueError('Use raw body OR estimate manifest')
    if complete and not body:raise ValueError('--complete-body requires --body; assertions cannot make a manifest complete')
    guarded=(backend=='ifapi' or transport=='ifapi-desktop') and settings['ifapi_guard']['enabled']
    report={'backend':backend,'transport':transport,'guard_applies':guarded,
            'budget_bytes':settings['ifapi_guard']['budget_bytes'] if guarded else None,
            'budget_basis':settings['ifapi_guard']['basis'] if guarded else 'No IF API temporary byte gate on this backend by default',
            'network_requests_sent':0}
    if body:
        path=Path(body).resolve()
        if not path.is_file():raise FileNotFoundError(path)
        count,sha=fingerprint(path)
        report.update(measurement='complete_body_as_asserted_by_caller' if complete else 'partial_body',
                      measured_bytes=count,body_sha256=sha,body_path=str(path),
                      coverage_note='Caller must obtain the FINAL serialized body including history, images and wrappers. This tool cannot independently verify completeness or bind a hidden transport to these bytes.')
        if guarded and count>report['budget_bytes']:report['status']='oversize'
        elif guarded and not complete:report['status']='needs_capture'
        else:report['status']='pass' if guarded else 'exempt'
    elif manifest:
        path=Path(manifest).resolve()
        if path.stat().st_size>65536:raise ValueError('Estimate manifest must be <=64KiB; do not embed image bytes')
        data=json.loads(path.read_text(encoding='utf-8-sig'))
        if set(data)-{'text_bytes','known_overhead_bytes','unknown_history','assets'}:raise ValueError('Unknown estimate fields')
        total=0
        for name in ('text_bytes','known_overhead_bytes'):
            value=data.get(name,0)
            if type(value) is not int or value<0:raise ValueError('Byte counts must be nonnegative integer')
            total+=value
        assets=data.get('assets',[])
        if not isinstance(assets,list) or len(assets)>1000:raise ValueError('Invalid asset list')
        for asset in assets:
            if set(asset)-{'path','encoding','occurrences'}:raise ValueError('Unknown asset fields')
            actual=(path.parent/asset['path']).resolve();count=actual.stat().st_size
            copies=asset.get('occurrences',1)
            if type(copies) is not int or copies<1:raise ValueError('occurrences must be positive integer')
            encoding=asset.get('encoding','base64')
            if encoding not in ('base64','binary'):raise ValueError('encoding: base64 or binary')
            total+=(4*((count+2)//3) if encoding=='base64' else count)*copies
        report.update(measurement='known_parts_estimate_only',estimated_known_bytes=total,asset_count=len(assets),
                      unknown_history=data.get('unknown_history',True),
                      coverage_note='Always an estimate, even if unknown_history=false. Does not certify wire body.')
        report['status']='oversize' if guarded and total>report['budget_bytes'] else ('needs_capture' if guarded else 'exempt')
    else:
        report.update(measurement='not_observable',status='needs_capture' if guarded else 'exempt',
                      coverage_note='No final request body is exposed. Do not claim checked or send IF API automatically while this temporary guard applies.')
    report['send_allowed_by_this_gate']=report['status'] in ('pass','exempt')
    report['next_action']={'oversize':'Rebuild a smaller independent request / reduce encoded references and unnecessary history, then recheck. Do not split serialized JSON into arbitrary chunks.',
      'needs_capture':'Obtain the actual final body through a supported caller/transport interface, or stop IF API and explain that completeness is unobservable. Do not silently switch providers.',
      'pass':'Send only these same measured bytes through a supported caller; recheck after any prompt/history/asset/wrapper change. This tool sends nothing.',
      'exempt':'No IF API-specific gate here; backend capability, normal errors, cost and provider limits still apply.'}[report['status']]
    return report


def main():
    utf8_stdio();p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--backend',choices=BACKENDS);p.add_argument('--transport',choices=('default','ifapi-desktop'),default='default')
    p.add_argument('--body',type=Path);p.add_argument('--complete-body',action='store_true')
    p.add_argument('--manifest',type=Path);p.add_argument('--preferences',type=Path)
    p.add_argument('-o','--output',type=Path)
    a=p.parse_args();r=inspect_request(a.backend,a.body,a.complete_body,a.manifest,a.preferences,a.transport)
    if a.output:
        if a.output.resolve() in {p.resolve() for p in (a.body,a.manifest,a.preferences) if p}:raise ValueError('Report cannot overwrite input')
        if a.output.exists():raise FileExistsError('Choose a new preflight report')
        a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(r,ensure_ascii=False))
    raise SystemExit({'pass':0,'exempt':0,'oversize':1,'needs_capture':2}[r['status']])

if __name__=='__main__':main()
