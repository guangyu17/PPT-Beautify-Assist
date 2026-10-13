#!/usr/bin/env python3
"""Project-local font downloads and explicit current-user Windows installation.
Only raw TTF/OTF over HTTPS; no installers/archives. Download requires reviewed license.
Installation is a dry run unless --apply is explicitly passed after user consent.
"""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import shutil
import urllib.parse
import urllib.request
from PIL import ImageFont
from _common import utf8_stdio

MAX_BYTES = 32 * 1024 * 1024


def fetch(url, limit=MAX_BYTES):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Use a reviewed public HTTPS raw-file URL without credentials')
    class SameHost(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            new = urllib.parse.urlsplit(newurl)
            if new.scheme != 'https' or new.hostname != parsed.hostname:
                raise ValueError('Redirect changed host; review the final official raw URL first')
            return super().redirect_request(req, fp, code, msg, headers, newurl)
    opener = urllib.request.build_opener(SameHost())
    with opener.open(urllib.request.Request(url, headers={'User-Agent':'ppt-beautify-studio/1.3'}), timeout=40) as response:
        raw = response.read(limit + 1)
    if len(raw) > limit:
        raise ValueError('Download exceeds local conservative size limit')
    return raw


def font_name(path):
    family, style = ImageFont.truetype(str(path), 24).getname()
    return {'family': family, 'style': style}


def workspace_path(workspace, relative):
    root = Path(workspace).resolve()
    if not (root/'logs/workspace.json').is_file():
        raise ValueError('Use init_workspace.py first')
    target = (root/relative).resolve()
    if not target.is_relative_to(root):
        raise ValueError('Unsafe workspace directory link')
    return target


def download(workspace, url, license_url, source_page, filename, reviewed=False):
    if not reviewed:
        raise ValueError('Review source and license first, then pass --license-reviewed')
    if Path(filename).name != filename or any(c in filename for c in '\\/:*?"<>|') or Path(filename).suffix.lower() not in ('.ttf','.otf'):
        raise ValueError('Use a plain .ttf/.otf filename')
    dest = workspace_path(workspace, 'fonts/downloaded') / filename
    lic = workspace_path(workspace, 'fonts/licenses') / (filename + '.license.txt')
    record = dest.with_suffix(dest.suffix + '.asset.json')
    if any(p.exists() for p in (dest, lic, record)):
        raise FileExistsError('Existing font/license/record preserved; choose a new filename or reuse verified asset')
    raw_license = fetch(license_url, 1024 * 1024)
    text = raw_license.decode('utf-8-sig')
    if not text.strip() or '<html' in text.lower() or '<!doctype html' in text.lower():
        raise ValueError('License URL did not return plain license text')
    raw = fetch(url)
    if raw[:4] not in (b'\x00\x01\x00\x00', b'OTTO', b'true'):
        raise ValueError('Not a raw TTF/OTF font (HTML, archives and installers rejected)')
    # Parse from memory before publishing a downloaded font file.
    import io
    face = ImageFont.truetype(io.BytesIO(raw), 24)
    family, style = face.getname()
    data = {'source_url':url, 'source_page':source_page, 'license_url':license_url,
            'license_reviewed_by_caller': True, 'font':str(dest), 'license':str(lic),
            'family':family,'style':style,'sha256':hashlib.sha256(raw).hexdigest(),
            'installed':False, 'note':'Caller must verify allowed use/redistribution/embedding and glyph coverage; this flag is not a legal determination.'}
    dest.parent.mkdir(parents=True, exist_ok=True); lic.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw); lic.write_text(text,encoding='utf-8')
    record.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return data


def inventory():
    dirs = [Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts']
    if os.environ.get('LOCALAPPDATA'):
        dirs.append(Path(os.environ['LOCALAPPDATA'])/'Microsoft/Windows/Fonts')
    return {'directories':[str(d) for d in dirs], 'files':[str(p) for d in dirs if d.is_dir() for p in sorted(d.iterdir()) if p.suffix.lower() in ('.ttf','.otf','.ttc')]}


def install_user(workspace, source, apply=False):
    source = Path(source).resolve()
    downloads = workspace_path(workspace, 'fonts/downloaded')
    if not source.is_relative_to(downloads) or source.suffix.lower() not in ('.ttf','.otf'):
        raise ValueError('Install only reviewed raw font files archived under this project fonts/downloaded')
    meta = json.loads(source.with_suffix(source.suffix+'.asset.json').read_text(encoding='utf-8'))
    if not meta.get('license_reviewed_by_caller') or hashlib.sha256(source.read_bytes()).hexdigest() != meta['sha256']:
        raise ValueError('Font provenance missing or font changed')
    license_path=Path(meta['license']).resolve()
    if not license_path.is_relative_to(workspace_path(workspace,'fonts/licenses')) or not license_path.is_file():
        raise ValueError('Missing project-local license')
    if os.name != 'nt':
        raise RuntimeError('Current helper supports Windows per-user install only')
    import winreg
    info = font_name(source)
    # Hash filename avoids overwriting another font file with the same download filename.
    destination = Path(os.environ['LOCALAPPDATA'])/'Microsoft/Windows/Fonts'/('pbs-'+meta['sha256'][:16]+source.suffix.lower())
    key_path = r'Software\Microsoft\Windows NT\CurrentVersion\Fonts'
    registry_name = f'{info["family"]} {info["style"]} (TrueType)'
    result = {'action':'install-user' if apply else 'dry-run','source':str(source),'destination':str(destination),
              'registry_hive':'HKCU','registry_key':key_path,'registry_value':registry_name,
              'requires_explicit_user_consent':True, 'family':info['family']}
    if not apply:
        return result
    if destination.exists() and hashlib.sha256(destination.read_bytes()).hexdigest() != meta['sha256']:
        raise FileExistsError('Destination differs; will not replace')
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER,key_path) as key:
        try:
            old, _ = winreg.QueryValueEx(key,registry_name)
        except FileNotFoundError:
            old = None
        if old and Path(old).resolve() != destination.resolve():
            raise FileExistsError('Same family/style already registered elsewhere; do not replace it')
        destination.parent.mkdir(parents=True,exist_ok=True)
        if not destination.exists():
            shutil.copyfile(source,destination)
        winreg.SetValueEx(key,registry_name,0,winreg.REG_SZ,str(destination))
    count = ctypes.windll.gdi32.AddFontResourceExW(str(destination),0,0)
    out = ctypes.c_size_t()
    ctypes.windll.user32.SendMessageTimeoutW(0xFFFF,0x001D,0,0,2,1000,ctypes.byref(out))
    result['font_resource_count'] = int(count)
    result['status'] = 'registered_verify_in_office' if count else 'registered_restart_or_repair_required'
    record = workspace_path(workspace,'logs')/('font-install-'+meta['sha256'][:16]+'.json')
    record.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result


def main():
    utf8_stdio()
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command',required=True)
    subs.add_parser('inventory')
    inspect = subs.add_parser('inspect'); inspect.add_argument('font',type=Path)
    dl = subs.add_parser('download')
    for flag in ('workspace','url','license-url','source-page','filename'):
        dl.add_argument('--'+flag,required=True)
    dl.add_argument('--license-reviewed',action='store_true')
    install = subs.add_parser('install-user'); install.add_argument('font',type=Path)
    install.add_argument('--workspace',required=True); install.add_argument('--apply',action='store_true')
    a=parser.parse_args()
    if a.command=='inventory': r=inventory()
    elif a.command=='inspect': r=font_name(a.font)
    elif a.command=='download': r=download(a.workspace,a.url,a.license_url,a.source_page,a.filename,a.license_reviewed)
    else: r=install_user(a.workspace,a.font,a.apply)
    print(json.dumps(r,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
