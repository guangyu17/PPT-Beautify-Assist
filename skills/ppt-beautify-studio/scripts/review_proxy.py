#!/usr/bin/env python3
"""Create optional size-adaptive inspection proxies (not a mandatory request cap); does NOT measure Codex's serialized request.
Never lowers output PPTX/source image quality. JPEG proxies flatten alpha on an explicit matte.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
from PIL import Image, ImageColor, ImageOps
from _common import utf8_stdio


def prepare(source, output, max_edge=1600, max_kib=512, crop=None, matte='#FFFFFF'):
    source, output = Path(source).resolve(), Path(output).resolve()
    sidecar = output.with_suffix('.review.json')
    if output.suffix.lower() not in ('.jpg','.jpeg') or output == source:
        raise ValueError('Output must be a new JPEG inspection copy, never the source')
    if output.exists() or sidecar.exists():
        raise FileExistsError('Choose a fresh revision; no overwrite')
    if max_edge < 64 or max_kib < 1:
        raise ValueError('max-edge >=64 and max-kib >=1 required; select these according to readability and measured request size')
    color = ImageColor.getrgb(matte)
    if len(color) != 3:
        raise ValueError('Matte must be an opaque RGB color')
    with Image.open(source) as original:
        oriented = ImageOps.exif_transpose(original).convert('RGBA')
    original_size = oriented.size
    if crop is not None:
        if len(crop) != 4:
            raise ValueError('Crop requires left top right bottom pixels')
        left, top, right, bottom = crop
        if not 0 <= left < right <= oriented.width or not 0 <= top < bottom <= oriented.height:
            raise ValueError('Crop out of bounds; coordinates refer to EXIF-oriented pixels')
        oriented = oriented.crop(tuple(crop))
    backing = Image.new('RGBA', oriented.size, color + (255,))
    rgb = Image.alpha_composite(backing, oriented).convert('RGB')
    initial = min(max_edge, max(rgb.size))
    edge = initial
    chosen = None
    # Bounded deterministic search. Do not make text arbitrarily tiny to pass a byte cap.
    floor = min(512, initial)
    while True:
        proxy = rgb.copy(); proxy.thumbnail((edge,edge),Image.Resampling.LANCZOS)
        for quality in (84,76,68,60):
            buffer = io.BytesIO()
            proxy.save(buffer,format='JPEG',quality=quality,optimize=True,subsampling=0)
            raw = buffer.getvalue()
            if len(raw) <= max_kib * 1024:
                chosen = raw, proxy.size, quality
                break
        if chosen or edge <= floor:
            break
        edge = max(floor,int(edge*.8))
    if not chosen:
        raise ValueError('Cannot fit this view within cap without excessive loss; request a smaller region/crop instead')
    raw, dimensions, quality = chosen
    report = {'kind':'inspection_proxy_not_generation_reference', 'source':str(source),
              'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_pixels':list(original_size),
              'crop':list(crop) if crop else None,'matte':matte, 'output':str(output), 'pixels':list(dimensions),
              'jpeg_quality':quality,'bytes':len(raw),'estimated_base64_bytes':4*((len(raw)+2)//3),
              'output_sha256':hashlib.sha256(raw).hexdigest(),
              'limits':{'max_edge':max_edge,'max_kib':max_kib},
              'review_status':'unreviewed',
              'warning':'Local file cap only; tool serialization, all chat history, images and tool definitions are outside this measurement. Inspect proxy; use a bounded source crop if text is unreadable. Do not certify visual QA from compression success.'}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(raw)
    sidecar.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report


def audit(paths, budget_kib=4096):
    """Byte-only preflight for a small candidate image/HTML group; no contents printed."""
    if budget_kib < 1:
        raise ValueError('budget-kib must be positive')
    if not 1 <= len(paths) <= 12:
        raise ValueError('Audit 1..12 candidate files, not the whole project')
    total = 0
    records = []
    seen = set()
    for item in paths:
        p = Path(item).resolve()
        if p in seen:
            continue
        seen.add(p)
        size = p.stat().st_size
        extension = p.suffix.lower()
        if extension not in ('.jpg','.jpeg','.png','.webp','.html'):
            raise ValueError('Audit accepts inspection images or HTML only')
        # Raw image may be encoded for transport; HTML size already includes embedded data.
        estimate = size if extension == '.html' else 4*((size+2)//3)
        total += estimate
        records.append({'path':str(p),'file_bytes':size,'estimated_transfer_bytes':estimate})
    return {'status':'within_local_budget' if total <= budget_kib*1024 else 'over_local_budget',
            'estimated_group_bytes':total,'budget_bytes':budget_kib*1024,'files':records,
            'warning':'This is not the actual /responses payload or server limit; history and automatic tool media remain unmeasured.'}


def main():
    utf8_stdio()
    p=argparse.ArgumentParser(description=__doc__)
    commands=p.add_subparsers(dest='command',required=True)
    view=commands.add_parser('image')
    view.add_argument('source',type=Path); view.add_argument('-o','--output',type=Path,required=True)
    view.add_argument('--max-edge',type=int,default=1600); view.add_argument('--max-kib',type=int,default=512)
    view.add_argument('--crop',type=int,nargs=4);view.add_argument('--matte',default='#FFFFFF')
    check=commands.add_parser('audit');check.add_argument('files',type=Path,nargs='+')
    check.add_argument('--budget-kib',type=int,default=4096)
    a=p.parse_args()
    if a.command=='image':
        r=prepare(a.source,a.output,a.max_edge,a.max_kib,a.crop,a.matte)
        # Deliberately compact output: never dump image bytes, Base64, HTML or full manifest.
        print(json.dumps({k:r[k] for k in ('output','pixels','bytes','estimated_base64_bytes','review_status')},ensure_ascii=False))
    else:
        r=audit(a.files,a.budget_kib)
        print(json.dumps(r,ensure_ascii=False))
        raise SystemExit(1 if r['status']=='over_local_budget' else 0)

if __name__=='__main__':main()
