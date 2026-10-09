#!/usr/bin/env python3
"""Create a registered frosted-underlay patch from a text-free background composition.
Not live backdrop blur: if underlying background or panel position changes, regenerate.
Never use a finished slide with text as source; native text stays above this texture.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageColor, ImageFilter
from _common import utf8_stdio


def make_patch(source,output,box,blur_px=12,tint='#FFFFFF',tint_alpha=.38,confirmed_text_free=False):
    source,output=Path(source).resolve(),Path(output).resolve()
    report=output.with_suffix('.material.json')
    if not confirmed_text_free:raise ValueError('Verify source is a text-free backdrop, then explicitly confirm it')
    if output==source or output.exists() or report.exists() or output.suffix.lower()!='.png':raise ValueError('Choose a new PNG revision')
    if not 0<=blur_px<=64 or not 0<=tint_alpha<=1:raise ValueError('blur-px 0..64; tint-alpha 0..1')
    with Image.open(source) as im:rgba=im.convert('RGBA')
    x0,y0,x1,y1=map(int,box)
    if not 0<=x0<x1<=rgba.width or not 0<=y0<y1<=rgba.height:raise ValueError('Panel box outside source pixels')
    # Blur entire background first so crop edges do not gain artificial repeated seams.
    patch=rgba.filter(ImageFilter.GaussianBlur(blur_px)).crop((x0,y0,x1,y1))
    color=ImageColor.getrgb(tint)
    if len(color)!=3:raise ValueError('Tint must be RGB')
    veil=Image.new('RGBA',patch.size,color+(round(255*tint_alpha),))
    patch=Image.alpha_composite(patch,veil)
    output.parent.mkdir(parents=True,exist_ok=True);patch.save(output)
    data={'kind':'frozen_background_blur_patch','source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
          'source_pixels':list(rgba.size),'crop_pixels':[x0,y0,x1,y1],
          'normalized_box':[x0/rgba.width,y0/rgba.height,(x1-x0)/rgba.width,(y1-y0)/rgba.height],
          'output':str(output),'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
          'blur_px':blur_px,'tint':tint,'tint_alpha':tint_alpha,
          'caller_confirmed_text_free':True,
          'warning':'Fixed raster backdrop sample, not true live refraction or background blur; opacity of this patch is not a measurement of material transparency. Refresh when background/position changes.'}
    report.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return data


def main():
    utf8_stdio();p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path);p.add_argument('-o','--output',type=Path,required=True)
    p.add_argument('--box',type=int,nargs=4,required=True);p.add_argument('--blur-px',type=float,default=12)
    p.add_argument('--tint',default='#FFFFFF');p.add_argument('--tint-alpha',type=float,default=.38)
    p.add_argument('--confirmed-text-free',action='store_true')
    a=p.parse_args();r=make_patch(a.source,a.output,a.box,a.blur_px,a.tint,a.tint_alpha,a.confirmed_text_free)
    print(json.dumps({'output':r['output'],'box':r['normalized_box'],'report':str(a.output.with_suffix('.material.json'))},ensure_ascii=False))

if __name__=='__main__':main()
