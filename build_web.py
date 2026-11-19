#!/usr/bin/env python3
"""Build web/index.html from werewolf-deal.html as a standalone phone web page.

- Adds a full HTML document (doctype, viewport, theme colour, home-screen app tags).
- Bundles the role card images into index.html, so the single file works anywhere.
Run again after editing werewolf-deal.html:  python3 build_web.py
"""
import json, pathlib, re, shutil

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "web"
OUT.mkdir(exist_ok=True)

src = (ROOT / "werewolf-deal.html").read_text(encoding="utf-8")

# bundle every role image into the page so index.html works on its own
# (sent to a phone, opened from a file, or hosted without the art folder)
import base64, subprocess, tempfile
CWEBP = shutil.which("cwebp")  # brew install webp; without it the JPEGs are bundled as they are

def width(f):
    out = subprocess.run(["sips", "-g", "pixelWidth", str(f)], check=True, capture_output=True, text=True).stdout
    return int(out.split()[-1])

art = {}
with tempfile.TemporaryDirectory() as tmp:
    for f in sorted([*(ROOT / "art").glob("*.jpg"), *(ROOT / "art").glob("*.png")]):
        mime, data = ("png" if f.suffix == ".png" else "jpeg"), f.read_bytes()
        if CWEBP:
            small = pathlib.Path(tmp) / (f.stem + ".webp")
            # cards show at most ~340 CSS px wide: 600 px covers a 2x phone screen; never enlarge
            resize = ["-resize", "600", "0"] if f.stem.endswith("-card") and width(f) > 600 else []
            subprocess.run([CWEBP, "-quiet", "-q", "72", *resize, str(f), "-o", str(small)], check=True)
            mime, data = "webp", small.read_bytes()
        art[f"art/{f.name}"] = f"data:image/{mime};base64," + base64.b64encode(data).decode()
src = src.replace("<script>", "<script>window.__ART__ = " + json.dumps(art) + ";</script>\n<script>", 1)

title = re.search(r"<title>(.*?)</title>", src).group(1)
src = re.sub(r"<title>.*?</title>\n?", "", src, count=1)
src = src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")

head = f"""<!doctype html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="狼人殺身份抽牌與法官工具：配置角色、輪流開牌、法官台詞與墓地。">
<meta name="theme-color" content="#0d1120">
<meta name="color-scheme" content="dark">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="{title}">
<meta name="format-detection" content="telephone=no">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="manifest" href="manifest.webmanifest">
<style>
:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
body{{margin:0}}
img{{max-width:100%}}
[hidden]{{display:none!important}}
</style>
"""
# page <link>/<style> go into <head>; the app markup + script go into <body>
split = src.index('<div class="wrap" id="app">')
doc = head + src[:split] + "</head>\n<body>\n" + src[split:] + "\n</body>\n</html>\n"
(OUT / "index.html").write_text(doc, encoding="utf-8")

manifest = {
    "name": title,
    "short_name": title,
    "description": "狼人殺身份抽牌與法官工具",
    "lang": "zh-Hant-TW",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": "#0d1120",
    "theme_color": "#0d1120",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
    ],
}
(OUT / "manifest.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print("built", OUT / "index.html", f"{(OUT / 'index.html').stat().st_size // 1024} KB")
