"""Shared helpers for ppt-beautify-studio scripts (units, colors, text metrics, contrast).

Not a CLI. Imported by the sibling scripts.
"""
from __future__ import annotations

import os
import sys
from functools import lru_cache
from pathlib import Path

EMU_PER_IN = 914400
EMU_PER_PT = 12700
PT_PER_IN = 72.0


def utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


# ---------------------------------------------------------------- colors

def hex_to_rgb(value):
    if value is None:
        return None
    if isinstance(value, (list, tuple)) and len(value) == 3:
        return tuple(int(v) for v in value)
    s = str(value).strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f"bad color: {value!r}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb) -> str:
    return "#%02X%02X%02X" % tuple(max(0, min(255, int(round(c)))) for c in rgb)


def _lin(c: float) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def rel_luminance(rgb) -> float:
    r, g, b = rgb
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast_from_lum(l1: float, l2: float) -> float:
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def contrast_ratio(c1, c2) -> float:
    return contrast_from_lum(rel_luminance(c1), rel_luminance(c2))


# ---------------------------------------------------------------- geometry

def cover_crop(img_w: float, img_h: float, box_w: float, box_h: float):
    """Return (left, top, right, bottom) crop fractions that make the image cover the box."""
    if img_w <= 0 or img_h <= 0 or box_w <= 0 or box_h <= 0:
        return (0.0, 0.0, 0.0, 0.0)
    img_r, box_r = img_w / img_h, box_w / box_h
    if abs(img_r - box_r) < 1e-4:
        return (0.0, 0.0, 0.0, 0.0)
    if img_r > box_r:  # too wide: crop left/right
        keep = box_r / img_r
        side = (1 - keep) / 2
        return (side, 0.0, side, 0.0)
    keep = img_r / box_r
    side = (1 - keep) / 2
    return (0.0, side, 0.0, side)


def contain_box(img_w, img_h, x, y, w, h):
    """Return (x, y, w, h) of the image fitted inside the box, centered."""
    img_r, box_r = img_w / img_h, w / h
    if img_r > box_r:
        nh = w / img_r
        return (x, y + (h - nh) / 2, w, nh)
    nw = h * img_r
    return (x + (w - nw) / 2, y, nw, h)


def overlap_area(a, b) -> float:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    ix = max(0.0, min(ax + aw, bx + bw) - max(ax, bx))
    iy = max(0.0, min(ay + ah, by + bh) - max(ay, by))
    return ix * iy


# ---------------------------------------------------------------- fonts / measuring

_FONT_DIRS = [Path(os.environ.get("WINDIR", r"C:\\Windows")) / "Fonts"]
if os.environ.get("LOCALAPPDATA"):
    _FONT_DIRS.append(Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts")
_FONT_DIRS += [Path("/usr/share/fonts"), Path("/Library/Fonts"), Path("/System/Library/Fonts")]

# family (lowercase) -> (regular candidates, bold candidates)
_FONT_TABLE = {
    "microsoft yahei": (["msyh.ttc", "msyh.ttf"], ["msyhbd.ttc", "msyhbd.ttf"]),
    "microsoft yahei ui": (["msyh.ttc"], ["msyhbd.ttc"]),
    "微软雅黑": (["msyh.ttc", "msyh.ttf"], ["msyhbd.ttc", "msyhbd.ttf"]),
    "dengxian": (["Deng.ttf"], ["Dengb.ttf"]),
    "等线": (["Deng.ttf"], ["Dengb.ttf"]),
    "simhei": (["simhei.ttf"], ["simhei.ttf"]),
    "黑体": (["simhei.ttf"], ["simhei.ttf"]),
    "simsun": (["simsun.ttc"], ["simsun.ttc"]),
    "宋体": (["simsun.ttc"], ["simsun.ttc"]),
    "kaiti": (["simkai.ttf"], ["simkai.ttf"]),
    "楷体": (["simkai.ttf"], ["simkai.ttf"]),
    "fangsong": (["simfang.ttf"], ["simfang.ttf"]),
    "source han sans sc": (["SourceHanSansSC-Regular.otf", "SourceHanSansCN-Regular.otf"], ["SourceHanSansSC-Bold.otf", "SourceHanSansCN-Bold.otf"]),
    "思源黑体": (["SourceHanSansSC-Regular.otf", "SourceHanSansCN-Regular.otf"], ["SourceHanSansSC-Bold.otf", "SourceHanSansCN-Bold.otf"]),
    "noto sans sc": (["NotoSansSC-Regular.otf", "NotoSansSC-VF.ttf"], ["NotoSansSC-Bold.otf", "NotoSansSC-VF.ttf"]),
    "arial": (["arial.ttf"], ["arialbd.ttf"]),
    "calibri": (["calibri.ttf"], ["calibrib.ttf"]),
    "segoe ui": (["segoeui.ttf"], ["segoeuib.ttf"]),
    "times new roman": (["times.ttf"], ["timesbd.ttf"]),
    "georgia": (["georgia.ttf"], ["georgiab.ttf"]),
    "verdana": (["verdana.ttf"], ["verdanab.ttf"]),
    "tahoma": (["tahoma.ttf"], ["tahomabd.ttf"]),
    "consolas": (["consola.ttf"], ["consolab.ttf"]),
}
_CJK_FALLBACK = (["msyh.ttc", "Deng.ttf", "simhei.ttf", "simsun.ttc", "NotoSansCJK-Regular.ttc", "PingFang.ttc"],
                 ["msyhbd.ttc", "Dengb.ttf", "simhei.ttf"])
_LATIN_FALLBACK = (["arial.ttf", "segoeui.ttf", "DejaVuSans.ttf", "Helvetica.ttc"], ["arialbd.ttf", "segoeuib.ttf", "DejaVuSans-Bold.ttf"])


@lru_cache(maxsize=None)
def _find_file(name: str):
    for d in _FONT_DIRS:
        p = d / name
        if p.exists():
            return str(p)
    return None


@lru_cache(maxsize=None)
def _font_path(family: str | None, bold: bool, cjk: bool):
    cands = []
    if family:
        entry = _FONT_TABLE.get(family.strip().lower())
        if entry:
            cands += entry[1] if bold else entry[0]
            cands += entry[0]
    fb = _CJK_FALLBACK if cjk else _LATIN_FALLBACK
    cands += (fb[1] if bold else []) + fb[0]
    for c in cands:
        p = _find_file(c)
        if p:
            return p
    return None


def is_cjk(ch: str) -> bool:
    o = ord(ch)
    return (0x2E80 <= o <= 0x9FFF or 0xAC00 <= o <= 0xD7AF or 0xF900 <= o <= 0xFAFF
            or 0xFE30 <= o <= 0xFE4F or 0xFF00 <= o <= 0xFFEF or 0x20000 <= o <= 0x2FA1F)


class TextMeasurer:
    """Approximate PowerPoint text metrics using local font files (falls back to heuristics)."""

    REF = 100  # reference px size for measurement

    def __init__(self):
        try:
            from PIL import ImageFont  # noqa
            self._pil = True
        except Exception:
            self._pil = False
        self._fonts = {}
        self._widths = {}

    def _font(self, family, bold, cjk):
        key = (family, bold, cjk)
        if key not in self._fonts:
            font = None
            if self._pil:
                path = _font_path(family, bold, cjk)
                if path:
                    try:
                        from PIL import ImageFont
                        font = ImageFont.truetype(path, self.REF)
                    except Exception:
                        font = None
            self._fonts[key] = font
        return self._fonts[key]

    def char_width(self, ch, size, bold=False, font=None, latin_font=None):
        cjk = is_cjk(ch)
        family = font if cjk else (latin_font or font)
        key = (ch, family, bold, cjk)
        w = self._widths.get(key)
        if w is None:
            f = self._font(family, bold, cjk)
            if f is not None:
                try:
                    w = f.getlength(ch) / self.REF
                except Exception:
                    w = None
            if w is None:
                w = 1.0 if cjk else (0.3 if ch == " " else 0.55)
            if bold and f is None:
                w *= 1.05
            self._widths[key] = w
        return w * size

    def line_height_factor(self, font=None, bold=False):
        f = self._font(font, bold, True)
        if f is not None:
            try:
                asc, desc = f.getmetrics()
                return max(1.1, min(1.6, (asc + desc) / self.REF))
            except Exception:
                pass
        return 1.2

    def layout_paragraph(self, runs, width_pt, wrap=True):
        """runs: list of dicts with text,size,bold,font,latin_font. Return (lines, max_width_pt, max_size)."""
        chars = []
        for r in runs:
            for ch in r.get("text", ""):
                chars.append((ch, r))
        max_size = max([float(r.get("size") or 18) for r in runs] or [18.0])
        if not chars:
            return 1, 0.0, max_size
        lines, cur, max_w = 1, 0.0, 0.0
        i = 0
        n = len(chars)
        while i < n:
            ch, r = chars[i]
            if ch in "\n\v\x0b":
                max_w = max(max_w, cur)
                lines += 1
                cur = 0.0
                i += 1
                continue
            # take a token: a latin word (with trailing space) or a single CJK/other char
            j = i
            if not is_cjk(ch) and not ch.isspace():
                while j < n and not is_cjk(chars[j][0]) and not chars[j][0].isspace() and chars[j][0] not in "\n\v\x0b":
                    j += 1
                while j < n and chars[j][0] == " ":
                    j += 1
            else:
                j = i + 1
            tok_w = 0.0
            for k in range(i, j):
                c, rr = chars[k]
                tok_w += self.char_width(c, float(rr.get("size") or 18), bool(rr.get("bold")), rr.get("font"), rr.get("latin_font"))
            if wrap and cur > 0 and cur + tok_w > width_pt + 0.5:
                max_w = max(max_w, cur)
                lines += 1
                cur = 0.0
                # leading spaces on a wrapped line are dropped
                while i < j and chars[i][0] == " ":
                    i += 1
                tok_w = sum(self.char_width(c, float(rr.get("size") or 18), bool(rr.get("bold")), rr.get("font"), rr.get("latin_font")) for c, rr in chars[i:j])
            if wrap and tok_w > width_pt and j - i > 1:
                # very long word: break by characters
                for c, rr in chars[i:j]:
                    cw = self.char_width(c, float(rr.get("size") or 18), bool(rr.get("bold")), rr.get("font"), rr.get("latin_font"))
                    if cur > 0 and cur + cw > width_pt + 0.5:
                        max_w = max(max_w, cur)
                        lines += 1
                        cur = 0.0
                    cur += cw
            else:
                cur += tok_w
            i = j
        max_w = max(max_w, cur)
        return lines, max_w, max_size


BULLET_INDENT_PT = 18.0
LEVEL_INDENT_PT = 27.0


def estimate_text_block(paragraphs, width_pt, wrap=True, measurer=None):
    """Return dict(height_pt, max_line_width_pt, lines) for normalized paragraphs."""
    m = measurer or TextMeasurer()
    total_h, max_w, total_lines = 0.0, 0.0, 0
    for idx, p in enumerate(paragraphs):
        runs = p.get("runs") or []
        indent = float(p.get("level") or 0) * LEVEL_INDENT_PT + (BULLET_INDENT_PT if p.get("bullet") else 0.0)
        avail = max(10.0, width_pt - indent)
        lines, w, size = m.layout_paragraph(runs, avail, wrap)
        font = None
        bold = False
        for r in runs:
            font = font or r.get("font")
            bold = bold or bool(r.get("bold"))
        ls = float(p.get("line_spacing") or 1.0)
        lh = size * m.line_height_factor(font, bold) * ls
        total_h += lines * lh
        if idx > 0:
            total_h += float(p.get("space_before") or 0)
        if idx < len(paragraphs) - 1:
            total_h += float(p.get("space_after") or 0)
        max_w = max(max_w, w + indent)
        total_lines += lines
    return {"height_pt": total_h, "max_line_width_pt": max_w, "lines": total_lines}


# ---------------------------------------------------------------- layout JSON normalisation

TEXT_KEYS = ("font", "latin_font", "size", "bold", "italic", "underline", "color")


def normalize_paragraphs(el: dict, defaults: dict):
    """Turn a layout-JSON text element into a list of paragraphs with fully-resolved runs."""
    base = {k: defaults.get(k) for k in TEXT_KEYS}
    base.update({k: el[k] for k in TEXT_KEYS if k in el})
    para_defaults = {k: el.get(k) for k in ("align", "line_spacing", "space_before", "space_after", "bullet")}
    raw = el.get("paragraphs")
    if raw is None:
        text = str(el.get("text", ""))
        raw = [{"text": t} for t in text.split("\n")]
    out = []
    for p in raw:
        if isinstance(p, str):
            p = {"text": p}
        pstyle = dict(base)
        pstyle.update({k: p[k] for k in TEXT_KEYS if k in p})
        runs = p.get("runs")
        if runs is None:
            runs = [{"text": str(p.get("text", ""))}]
        nruns = []
        for r in runs:
            if isinstance(r, str):
                r = {"text": r}
            rs = dict(pstyle)
            rs.update({k: r[k] for k in TEXT_KEYS if k in r})
            rs["text"] = str(r.get("text", ""))
            if rs.get("size") is None:
                rs["size"] = 18
            nruns.append(rs)
        para = {k: p.get(k, para_defaults.get(k)) for k in ("align", "line_spacing", "space_before", "space_after", "bullet")}
        para["level"] = int(p.get("level", 0) or 0)
        para["runs"] = nruns
        out.append(para)
    return out


class Units:
    """Convert layout JSON coordinates to inches."""

    def __init__(self, spec: dict):
        size = spec.get("slide_size") or {}
        aspect = spec.get("aspect") or size.get("aspect")
        if size.get("width") and size.get("height"):
            self.sw, self.sh = float(size["width"]), float(size["height"])
        elif aspect in ("4:3", "4x3"):
            self.sw, self.sh = 10.0, 7.5
        elif aspect in ("16:10",):
            self.sw, self.sh = 12.0, 7.5
        else:
            self.sw, self.sh = 13.333, 7.5
        self.units = (spec.get("units") or "in").lower()
        if self.sw <= 0 or self.sh <= 0 or self.units not in ('in', 'pt', 'px', 'pct', '%'):
            raise ValueError('Invalid slide size or coordinate units')
        if self.units == 'px' and not spec.get('canvas'):
            raise ValueError('Pixel coordinates require an explicit canvas')
        canvas = spec.get("canvas") or {}
        self.cw = float(canvas.get("width") or 1920)
        self.ch = float(canvas.get("height") or self.cw * self.sh / self.sw)
        if self.cw <= 0 or self.ch <= 0:
            raise ValueError('Canvas dimensions must be positive')

    def x(self, v):
        v = float(v)
        if self.units == "px":
            return v / self.cw * self.sw
        if self.units == "pt":
            return v / PT_PER_IN
        if self.units in ("pct", "%"):
            return v / 100.0 * self.sw
        return v

    def y(self, v):
        v = float(v)
        if self.units == "px":
            return v / self.ch * self.sh
        if self.units == "pt":
            return v / PT_PER_IN
        if self.units in ("pct", "%"):
            return v / 100.0 * self.sh
        return v

    def box(self, el):
        return (self.x(el.get("x", 0)), self.y(el.get("y", 0)), self.x(el.get("w", 0)), self.y(el.get("h", 0)))


def resolve_path(p, base_dir: Path):
    if not p:
        return None
    q = Path(p)
    if not q.is_absolute():
        q = (base_dir / q)
    return q.resolve()
