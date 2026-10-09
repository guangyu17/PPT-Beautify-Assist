#!/usr/bin/env python3
"""Render PDF with bundled PDFium, read positioned text with pdfplumber and originals with pypdf.
No OCR is fabricated: image-only pages are explicitly marked needs_ocr.
"""
import argparse
import json
from pathlib import Path
import pdfplumber
import pypdfium2 as pdfium
from pypdf import PdfReader
from _common import utf8_stdio


def extract(source, output, pages, media, dpi=200):
    source, output, pages, media = map(lambda x: Path(x).resolve(), (source, output, pages, media))
    if source == output or not 36 <= dpi <= 600:
        raise ValueError('Unsafe output or DPI outside 36..600')
    for path in (output.parent, pages, media):
        path.mkdir(parents=True, exist_ok=True)
    result = {'schema_version': 1, 'source': str(source), 'dpi': dpi,
              'coordinates': 'points, top-left; page rotation applied by pdfplumber/PDFium; verify cropped/rotated pages', 'pages': []}
    reader = PdfReader(source)
    with pdfium.PdfDocument(str(source)) as render_doc, pdfplumber.open(source) as text_doc:
        for i, (rp, tp) in enumerate(zip(reader.pages, text_doc.pages)):
            page = render_doc[i]
            bitmap = page.render(scale=dpi / 72)
            pil = bitmap.to_pil()
            png = pages / f'page-{i + 1:03}.png'
            pil.save(png)
            chars = [{k: ch.get(k) for k in ('text', 'x0', 'x1', 'top', 'bottom', 'fontname', 'size', 'non_stroking_color', 'upright', 'matrix')} for ch in tp.chars]
            images = []
            for j, img in enumerate(rp.images):
                suffix = Path(img.name).suffix or '.bin'
                path = media / f'p{i + 1:03}-img{j + 1:03}{suffix}'
                path.write_bytes(img.data)
                images.append({'path': str(path), 'source_name': img.name, 'pixel_size': list(img.image.size)})
            result['pages'].append({'index': i + 1, 'width_pt': tp.width, 'height_pt': tp.height,
                                    'rotation': rp.rotation, 'image': str(png), 'pixel_size': list(pil.size),
                                    'text': tp.extract_text() or '', 'characters': chars,
                                    'words': tp.extract_words(), 'needs_ocr': not bool(chars),
                                    'embedded_images': images,
                                    'image_placements': [{k: im.get(k) for k in ('name', 'x0', 'x1', 'top', 'bottom', 'width', 'height', 'srcsize')} for im in tp.images],
                                    'image_mapping_note': 'Placements and embedded assets must be visually matched; resource names may differ inside Form XObjects.'})
            pil.close()
            bitmap.close()
            page.close()
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    return result


def main():
    utf8_stdio()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path)
    p.add_argument('-o', '--output', required=True, type=Path)
    p.add_argument('--pages', type=Path)
    p.add_argument('--media', type=Path)
    p.add_argument('--dpi', type=int, default=200)
    a = p.parse_args()
    r = extract(a.source, a.output, a.pages or a.output.parent / 'pages', a.media or a.output.parent / 'media', a.dpi)
    print(json.dumps({'pages': len(r['pages']), 'needs_ocr': [p['index'] for p in r['pages'] if p['needs_ocr']], 'output': str(a.output)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
