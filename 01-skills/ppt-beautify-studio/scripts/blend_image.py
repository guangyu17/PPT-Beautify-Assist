#!/usr/bin/env python3
"""Deterministic alpha feathering; not semantic background removal or AI outpainting.
Fade range is normalized: --fade-left 0.15 0.60 means alpha 0 through x=.15,
then smooth transition to unchanged alpha at x=.60. Existing alpha is preserved.
"""
import argparse
import math
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageEnhance
from _common import utf8_stdio


def smooth_ramp(axis, start, end):
    if not 0 <= start < end <= 1:
        raise ValueError('Fade range must satisfy 0 <= start < end <= 1')
    t = np.clip((axis - start) / (end - start), 0, 1)
    return t * t * (3 - 2 * t)


def blend(source, output, fades=None, opacity=1, brightness=1, saturation=1, mask=None):
    source, output = Path(source).resolve(), Path(output).resolve()
    if output.suffix.lower() != '.png' or output == source or output.exists():
        raise ValueError('Choose a new PNG output; never overwrite source or a previous result')
    report_path = output.with_suffix('.asset.json')
    if report_path.exists():
        raise FileExistsError(report_path)
    if not 0 <= opacity <= 1 or not 0 <= brightness <= 2 or not 0 <= saturation <= 2:
        raise ValueError('opacity 0..1; brightness and saturation 0..2')
    with Image.open(source) as original:
        rgba = original.convert('RGBA')
    w, h = rgba.size
    old_alpha = np.asarray(rgba.getchannel('A'), dtype=np.float32) / 255
    weight = np.ones((h, w), dtype=np.float32)
    x = np.linspace(0, 1, w, dtype=np.float32)[None, :]
    y = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    for edge, (start, end) in (fades or {}).items():
        axis = {'left': x, 'right': 1 - x, 'top': y, 'bottom': 1 - y}[edge]
        weight *= smooth_ramp(axis, start, end)
    if mask:
        with Image.open(mask) as m:
            if m.size != (w, h):
                raise ValueError('Subject/scene mask must match source pixels exactly; no implicit resizing')
            weight *= np.asarray(m.convert('L'), dtype=np.float32) / 255
    rgb = ImageEnhance.Brightness(rgba.convert('RGB')).enhance(brightness)
    rgb = ImageEnhance.Color(rgb).enhance(saturation)
    alpha = np.round(old_alpha * weight * opacity * 255).astype('uint8')
    result = rgb.convert('RGBA'); result.putalpha(Image.fromarray(alpha))
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save(output)
    report = {'operation': 'alpha_feather', 'source': str(source), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'output': str(output), 'output_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
              'size': [w, h], 'fades': fades or {}, 'opacity': opacity, 'brightness': brightness,
              'saturation': saturation, 'mask': str(Path(mask).resolve()) if mask else None,
              'alpha_min': int(alpha.min()), 'alpha_max': int(alpha.max()),
              'registration': 'Same canvas, no crop, no scaling; semantic subject protection requires a separate intact cutout layer'}
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return report



def gradient_field(width, height, config):
    """Pixel-space projection, normalized across all four corners. 0=right,90=down.
    This is gradient direction, not rotation of the source artwork.
    """
    angle = float(config.get('angle', 0))
    gamma = float(config.get('gamma', 1))
    if not math.isfinite(angle) or not math.isfinite(gamma) or not 0.05 <= gamma <= 20:
        raise ValueError('Finite angle and gamma in 0.05..20 required')
    theta = math.radians(angle % 360)
    dx, dy = math.cos(theta), math.sin(theta)
    xx = np.arange(width, dtype=np.float64)[None, :]
    yy = np.arange(height, dtype=np.float64)[:, None]
    corners = [0, (width - 1) * dx, (height - 1) * dy,
               (width - 1) * dx + (height - 1) * dy]
    lo, hi = min(corners), max(corners)
    t = (xx * dx + yy * dy - lo) / max(hi - lo, 1e-12)
    stops = config.get('stops', [[0, 0], [1, 1]])
    if not isinstance(stops, list) or len(stops) < 2:
        raise ValueError('Gradient needs at least two [position, alpha] stops')
    data = np.asarray(stops, dtype=np.float64)
    if data.shape != (len(stops), 2) or not np.isfinite(data).all():
        raise ValueError('Stops must be finite [position, alpha] pairs')
    positions, alphas = data[:, 0], data[:, 1]
    if (data < 0).any() or (data > 1).any() or (np.diff(positions) <= 0).any():
        raise ValueError('Stops must be in 0..1 with strictly increasing positions')
    idx = np.clip(np.searchsorted(positions, t, side='right') - 1, 0, len(stops) - 2)
    u = np.clip((t - positions[idx]) / (positions[idx + 1] - positions[idx]), 0, 1)
    curve = config.get('curve', 'smoothstep')
    if curve == 'smoothstep':
        u = u * u * (3 - 2 * u)
    elif curve == 'smootherstep':
        u = u * u * u * (u * (u * 6 - 15) + 10)
    elif curve != 'linear':
        raise ValueError('curve must be linear, smoothstep, or smootherstep')
    u = u ** gamma
    return np.clip(alphas[idx] + u * (alphas[idx + 1] - alphas[idx]), 0, 1)


def blend_recipe(recipe_path, output):
    """Rebuild a reversible visual-only stack from source assets, never previous composites.
    Every processed layer is retained as its own registered RGBA PNG for native PPTX pictures.
    """
    from PIL import ImageColor
    recipe_path, output = Path(recipe_path).resolve(), Path(output).resolve()
    spec = json.loads(recipe_path.read_text(encoding='utf-8-sig'))
    size = spec.get('canvas', {})
    w, h = size.get('width'), size.get('height')
    if not isinstance(w, int) or not isinstance(h, int) or isinstance(w, bool) or isinstance(h, bool) or min(w, h) < 2 or w * h > 16000000:
        raise ValueError('Canvas integer width/height >=2 and <=16 million pixels required')
    layers = spec.get('layers')
    if not isinstance(layers, list) or not 1 <= len(layers) <= 16:
        raise ValueError('Recipe requires 1..16 layers')
    report_path = output.with_suffix('.asset.json')
    layer_dir = output.parent / (output.stem + '-layers')
    if output.suffix.lower() != '.png' or any(p.exists() for p in (output, report_path, layer_dir)):
        raise ValueError('Choose a new PNG revision; output/report/layer directory must not exist')
    records, prepared, ids = [], [], set()
    composite = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for i, layer in enumerate(layers, 1):
        layer_id = str(layer.get('id', f'layer-{i:02}'))
        if layer_id in ids:
            raise ValueError('Layer IDs must be unique')
        ids.add(layer_id)
        opacity = float(layer.get('opacity', 1))
        brightness = float(layer.get('brightness', 1))
        saturation = float(layer.get('saturation', 1))
        if not all(math.isfinite(v) for v in (opacity, brightness, saturation)) or not 0 <= opacity <= 1 or not 0 <= brightness <= 2 or not 0 <= saturation <= 2:
            raise ValueError('opacity 0..1; brightness/saturation 0..2, finite')
        record = {'id': layer_id, 'parameters': layer}
        kind = layer.get('type', 'image')
        if kind == 'image':
            source = (recipe_path.parent / layer['path']).resolve()
            if source in (output, report_path):
                raise ValueError('Cannot overwrite input')
            with Image.open(source) as image:
                if image.size != (w, h):
                    raise ValueError(f'{source}: all layers must match canvas; no implicit resize/crop')
                image = image.convert('RGBA')
            record.update(source=str(source), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
        elif kind == 'color':
            image = Image.new('RGBA', (w, h), ImageColor.getcolor(layer['color'], 'RGBA'))
        else:
            raise ValueError('Layer type must be image or color; no text layers in raster recipe')
        alpha = np.asarray(image.getchannel('A'), dtype=np.float64) / 255
        rgb = ImageEnhance.Brightness(image.convert('RGB')).enhance(brightness)
        rgb = ImageEnhance.Color(rgb).enhance(saturation)
        gradients = layer.get('gradients', [])
        if len(gradients) > 8:
            raise ValueError('At most 8 gradient masks per layer')
        for gradient in gradients:
            alpha *= gradient_field(w, h, gradient)
        if layer.get('mask'):
            mask_path = (recipe_path.parent / layer['mask']).resolve()
            with Image.open(mask_path) as mask:
                if mask.size != (w, h):
                    raise ValueError('Mask must match canvas')
                alpha *= np.asarray(mask.convert('L'), dtype=np.float64) / 255
            record.update(mask_source=str(mask_path), mask_sha256=hashlib.sha256(mask_path.read_bytes()).hexdigest())
        alpha = np.round(np.clip(alpha * opacity, 0, 1) * 255).astype('uint8')
        rgba = rgb.convert('RGBA'); rgba.putalpha(Image.fromarray(alpha))
        composite = Image.alpha_composite(composite, rgba)
        prepared.append(rgba)
        record.update(alpha_min=int(alpha.min()), alpha_max=int(alpha.max()))
        records.append(record)
    output.parent.mkdir(parents=True, exist_ok=True)
    layer_dir.mkdir()
    for i, (image, record) in enumerate(zip(prepared, records), 1):
        path = layer_dir / f'layer-{i:02}.png'
        image.save(path)
        record.update(output=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    composite.save(output)
    report = {'operation':'registered_alpha_stack', 'recipe':str(recipe_path),
              'recipe_sha256':hashlib.sha256(recipe_path.read_bytes()).hexdigest(),
              'canvas':{'width':w,'height':h}, 'output':str(output),
              'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(), 'layers':records,
              'blend_mode':'source-over, layers listed bottom to top; gradient masks multiply within each layer',
              'text_policy':'No text rendered by this tool. Native text belongs in compose_slide layout.',
              'editable_delivery':'Use exported layers as separate registered PPTX images, or the merged visual background only with user-approved editability tradeoff.'}
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report


def main():
    utf8_stdio()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path, nargs='?')
    p.add_argument('--recipe', type=Path, help='Registered multilayer JSON; mutually exclusive with source')
    p.add_argument('-o', '--output', type=Path, required=True)
    for edge in ('left', 'right', 'top', 'bottom'):
        p.add_argument('--fade-' + edge, type=float, nargs=2, metavar=('START','END'))
    p.add_argument('--opacity', type=float, default=1)
    p.add_argument('--brightness', type=float, default=1)
    p.add_argument('--saturation', type=float, default=1)
    p.add_argument('--mask', type=Path, help='Verified mask: black removes, white keeps; not automatic segmentation')
    a = p.parse_args()
    if a.recipe:
        if a.source:
            p.error('Use source OR --recipe, not both')
        if a.mask or any(getattr(a, 'fade_' + edge) for edge in ('left','right','top','bottom')) or (a.opacity, a.brightness, a.saturation) != (1, 1, 1):
            p.error('With --recipe, set image adjustments in JSON, not single-source CLI flags')
        result = blend_recipe(a.recipe, a.output)
        print(json.dumps({'output':result['output'], 'layer_count':len(result['layers']), 'report':str(a.output.with_suffix('.asset.json'))}, ensure_ascii=False))
        return
    if not a.source:
        p.error('source or --recipe is required')
    fades = {edge: getattr(a, 'fade_' + edge) for edge in ('left', 'right', 'top', 'bottom') if getattr(a, 'fade_' + edge)}
    print(json.dumps(blend(a.source, a.output, fades, a.opacity, a.brightness, a.saturation, a.mask), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
