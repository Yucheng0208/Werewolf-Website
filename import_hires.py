#!/usr/bin/env python3
"""Cut high-res 1086x1448 role cards into poker-card images and face thumbnails.

Each card loses 25 px per side to reach the poker ratio 63:88 (1036x1448), then is saved 760 px wide.
The thumbnail is a 400x400 square around the face, saved at 200 px.
Add a line to CARDS for every new card, then run:  python3 import_hires.py && python3 build_web.py
"""
import pathlib, subprocess

ROOT = pathlib.Path(__file__).parent
DL = pathlib.Path.home() / "Downloads"

# role id: (source file name, thumbnail left x, thumbnail top y)
# files are looked up in ~/Downloads and ~/Downloads/卡片
CARDS = {
    "seer":        ("月下預言家的水晶啟示.png", 360, 185),
    "witch":       ("月下女巫：藥師UR卡.png", 430, 185),
    "guard":       ("月影守衛：銀狼之盾.png", 410, 185),
    "knight":      ("月下決鬥騎士 UR卡.png", 380, 170),
    "idiot":       ("白痴神職月夜幻卡.png", 330, 185),
    "gravekeeper": ("月下守墓人 UR 卡牌.png", 370, 185),
    "villager":    ("月下平民卡牌.png", 360, 185),
    "cupid":       ("月夜丘比特：神職戀人卡.png", 350, 170),
    "mixed":       ("月下混血兒狼靈卡.png", 390, 170),
    "werewolf":    ("ChatGPT 圖像 2026年11月17日 上午12_59_37.png", 500, 170),
    "hunter":      ("月下獵人：帶槍之誓.png", 410, 185),
    "hiddenwolf":  ("月下隱狼：UR狼人卡牌.png", 470, 185),
    "whitewolf":   ("白狼王：自爆反擊.png", 480, 185),
    "wolfking":    ("狼王月下卡牌插畫.png", 440, 185),
    "wolfbeauty":  ("狼美人：魅惑之夜.png", 370, 185),
}

def locate(name):
    for folder in (DL, DL / "卡片"):
        if (folder / name).exists():
            return folder / name
    raise SystemExit(f"找不到 {name}（請放在下載或下載/卡片）")

def sips(*args):
    subprocess.run(["sips", *map(str, args)], check=True, capture_output=True)

for rid, (name, tx, ty) in CARDS.items():
    src = locate(name)
    card = ROOT / "art" / f"{rid}-card.jpg"
    sips("-s", "format", "jpeg", "-s", "formatOptions", "88", "-c", 1448, 1036, "--cropOffset", 0, 25, src, "--out", card)
    sips("--resampleWidth", 760, card)
    # thumbnails now come from the dedicated square portraits (art/*-thumb.jpg); only cut one if missing
    thumb = ROOT / "art" / f"{rid}-thumb.jpg"
    if not thumb.exists():
        sips("-s", "format", "jpeg", "-s", "formatOptions", "86", "-c", 400, 400, "--cropOffset", ty, tx, src, "--out", thumb)
        sips("-Z", 200, thumb)
    print("ok", rid)
print("poker-ready roles:", ", ".join(CARDS))
