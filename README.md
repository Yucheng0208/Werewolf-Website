<p align="center">
  <img src="art/logo.png" alt="天黑請閉眼 logo" width="120">
</p>

<h1 align="center">天黑請閉眼 · Werewolf Role Dealer</h1>

<p align="center">
  <a href="https://werewolf.yucheng208.net">werewolf.yucheng208.net</a>
  &nbsp;·&nbsp; <a href="#english">English</a> &nbsp;·&nbsp; <a href="#繁體中文">繁體中文</a>
</p>

---

## English

A phone-first web app for running a game of Werewolf (狼人殺) with **one phone passed around the table**. It deals hidden role cards, then turns into a step-by-step script and graveyard for the moderator (上帝, "God").

### Features

- **Role setup**: choose 4–18 players and 15 roles across four camps, or press *Auto-configure* for a balanced lineup. An optional **sheriff election** rule is off by default.
- **Pass-and-reveal dealing**: each player taps the card to flip it, taps again to cover it, then presses *Next*. The next role is only loaded once the card is fully face-down, so nobody sees it mid-flip.
- **Gacha-style reveal**: charge-up shake, light burst, sparks and a foil shine on the first flip.
- **Poker-sized cards**: every role, and the card back, uses its own artwork at 63 × 88 mm proportions with rounded corners.
- **Moderator script**: the night and day lines are generated from the roles in play, with moderator tips. Navigate with buttons, swipes or arrow keys, and optionally have each line read aloud (zh-TW).
- **Graveyard**: mark players out with a cause of death. The script then suggests the death announcement, crosses out dead role holders and flags a likely win.
- **Hidden-side 混血兒**: the Mixed-blood is secretly assigned to the wolf or good side at each deal. Only the moderator sees which.
- **Responsive**: single column on phones, two columns on tablets and desktops. Font Awesome icons throughout.
- **Installable**: add it to the iPhone or Android home screen and it opens full-screen like an app.

### Roles

| Camp | Roles |
| --- | --- |
| Wolves 狼人陣營 | 狼人 Werewolf · 狼王 Wolf King · 白狼王 White Wolf King · 狼美人 Wolf Beauty · 隱狼 Hidden Wolf |
| Gods 神職 | 預言家 Seer · 女巫 Witch · 獵人 Hunter · 守衛 Guard · 白痴 Idiot · 騎士 Knight · 丘比特 Cupid |
| Villagers 平民 | 平民 Villager · 守墓人 Gravekeeper |
| Special 特殊陣營 | 混血兒 Mixed-blood (random hidden side) |

### Project structure

```text
werewolf-deal.html   Source page: all markup, styles and game logic
art/                 Card images (*-card.jpg), thumbnails (*-thumb.jpg), back.jpg, logo.png
build_web.py         Builds web/index.html with every image bundled in
import_hires.py      Cuts high-res 1086×1448 card PNGs into poker-ratio cards
web/                 Build output: index.html, manifest and app icons
deploy/              What gets uploaded to Cloudflare
wrangler.jsonc       Cloudflare Workers config (static assets + custom domain)
```

`web/index.html` is a single self-contained file (about 2.5 MB). It works opened on its own, with no `art/` folder beside it.

### Requirements

- macOS (the scripts use the built-in `sips`)
- Python 3
- [`cwebp`](https://developers.google.com/speed/webp) (optional, recommended): `brew install webp`. It shrinks the bundled images to WebP. Without it, the JPEGs are bundled as they are.
- [Wrangler](https://developers.cloudflare.com/workers/wrangler/) for deploying: `npm i -g wrangler`

### Build

```bash
python3 build_web.py
```

To preview it locally:

```bash
python3 -m http.server 8000 --directory web
```

Then open <http://localhost:8000>.

### Deploy to Cloudflare

The site is a static-assets Worker named `werewolf-night`, served on the custom domain `werewolf.yucheng208.net`.

```bash
python3 build_web.py
cp web/index.html web/manifest.webmanifest deploy/
wrangler login        # first time only
wrangler deploy
```

### Updating card art

1. Put the new 1086 × 1448 card PNG in `~/Downloads` or `~/Downloads/卡片`.
2. Add or update its entry in `CARDS` in `import_hires.py`.
3. Run `python3 import_hires.py`, then build and deploy as above.

To replace a thumbnail, overwrite `art/<role>-thumb.jpg` (square, about 200 px). `import_hires.py` never overwrites an existing thumbnail.

### Add to the home screen

- **iPhone**: open the site in Safari, then tap Share → *Add to Home Screen*.
- **Android**: open the site in Chrome, then tap ⋮ → *Add to Home screen*.

### License

[MIT](LICENSE) © 2026 Yu-Cheng Chang（張育丞）

---

## 繁體中文

一款以手機為主的狼人殺網頁工具，設計成**一支手機在桌上輪流傳**。它會發出隱藏的角色卡，發完後變成給上帝用的逐句台詞和墓地紀錄。

### 功能

- **角色配置**：選擇 4–18 位玩家，從四個陣營、15 種角色中挑選，或按「依人數自動配置」直接配好。可選擇是否開啟「警長競選」，預設關閉。
- **輪流開牌**：玩家點卡牌翻開，再點一次蓋牌，看好後按「下一位」。卡片完全蓋回去後才會換成下一位的身份，翻牌過程中不會被看到。
- **抽卡特效**：第一次翻牌時有蓄力震動、閃光、火花和卡面掃光。
- **撲克牌尺寸卡片**：每個角色和卡背都使用專屬卡圖，比例為 63 × 88 mm，並有圓角。
- **上帝台詞**：依本局角色自動產生夜晚與白天的台詞，附上帝提示。可用按鈕、左右滑動或方向鍵切換，也能開啟語音朗讀。
- **墓地**：標記玩家出局與死因。台詞會依紀錄給出公布死訊的句子、劃掉已出局的角色，並提示可能的勝負。
- **混血兒隨機陣營**：每次發牌時偷偷幫混血兒抽一個陣營，只有上帝看得到。
- **RWD 響應式版面**：手機單欄，平板和電腦雙欄，整個介面使用 Font Awesome 圖示。
- **可加入主畫面**：在 iPhone 或 Android 加入主畫面後，會像 App 一樣全螢幕開啟。

### 角色

| 陣營 | 角色 |
| --- | --- |
| 狼人陣營 | 狼人 · 狼王 · 白狼王 · 狼美人 · 隱狼 |
| 神職 | 預言家 · 女巫 · 獵人 · 守衛 · 白痴 · 騎士 · 丘比特 |
| 平民 | 平民 · 守墓人 |
| 特殊陣營 | 混血兒（隨機隱藏陣營） |

### 專案結構

```text
werewolf-deal.html   原始網頁：所有版面、樣式與遊戲邏輯
art/                 卡片圖（*-card.jpg）、縮圖（*-thumb.jpg）、卡背 back.jpg、LOGO logo.png
build_web.py         產生 web/index.html，並把所有圖片包進去
import_hires.py      把 1086×1448 的高解析卡片 PNG 裁成撲克牌比例
web/                 建置結果：index.html、manifest 與 App 圖示
deploy/              上傳到 Cloudflare 的檔案
wrangler.jsonc       Cloudflare Workers 設定（靜態網站 + 自訂網域）
```

`web/index.html` 是單一檔案（約 2.5 MB），所有圖片都包在裡面，不需要旁邊有 `art/` 資料夾也能打開。

### 需求

- macOS（腳本使用內建的 `sips`）
- Python 3
- [`cwebp`](https://developers.google.com/speed/webp)（選用，建議安裝）：`brew install webp`。可以把包進網頁的圖片轉成 WebP 縮小檔案；沒有安裝時會直接包入 JPEG。
- 部署需要 [Wrangler](https://developers.cloudflare.com/workers/wrangler/)：`npm i -g wrangler`

### 建置

```bash
python3 build_web.py
```

本機預覽：

```bash
python3 -m http.server 8000 --directory web
```

然後打開 <http://localhost:8000>。

### 部署到 Cloudflare

網站是名為 `werewolf-night` 的靜態 Worker，使用自訂網域 `werewolf.yucheng208.net`。

```bash
python3 build_web.py
cp web/index.html web/manifest.webmanifest deploy/
wrangler login        # 只有第一次需要
wrangler deploy
```

### 更新卡片圖

1. 把新的 1086 × 1448 卡片 PNG 放到 `~/Downloads` 或 `~/Downloads/卡片`。
2. 在 `import_hires.py` 的 `CARDS` 裡新增或修改那張卡的檔名。
3. 執行 `python3 import_hires.py`，再照上面的步驟建置和部署。

要換縮圖，直接覆蓋 `art/<角色>-thumb.jpg`（正方形，約 200 px）。`import_hires.py` 不會覆蓋已經存在的縮圖。

### 加入主畫面

- **iPhone**：用 Safari 打開網站，點分享 →「加入主畫面」。
- **Android**：用 Chrome 打開網站，點 ⋮ →「加到主畫面」。

### 授權

[MIT](LICENSE) © 2026 Yu-Cheng Chang（張育丞）
