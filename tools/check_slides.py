"""簡報檢查器（用 Playwright 開啟真實瀏覽器）：
 1. 每一頁都有 data-wiki 出處
 2. 每個 data-ref 的文字與 Wiki ## 重點 逐字相同；data-code / data-sum / data-title 也比對
 3. 換頁功能：→ 鍵、按鈕、#網址可跳頁，頁碼正確
 4. 每頁內容不超出 1280×720 畫面（無溢出）
 5. 主控台沒有錯誤
 6. 可見文字不得殘留 Wiki 語法 [[ 或 ]]
 8. 截圖當下頁面不透明度必須為 1（確認動畫已結束）
 7. 圖表（SVG）尺寸：寬 ≥ 300px、高 ≥ 150px，且圖中最小文字的實際字級 ≥ 14px
固定規則：每次換頁後等 ANIM_WAIT 毫秒（淡入動畫 350ms 結束）才檢查與截圖。
並把每頁截圖存到 screenshots/ 供人工檢視。
"""
import sys, re, pathlib
from playwright.sync_api import sync_playwright
from wikilib import pages, key_points, summary, title

ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML = ROOT / "AI-Agents-是什麼.html"; SHOTS = ROOT / "screenshots"; SHOTS.mkdir(exist_ok=True)
P = pages(); errors = []
ANIM_WAIT = 450      # 毫秒；必須大於 CSS 淡入動畫 .35s，否則截圖會偏淡
MIN_FONT = 14; MIN_W = 300; MIN_H = 150
code = lambda p, n: re.findall(r"```\n(.*?)```", P[p], re.S)[n-1].rstrip("\n")
oneliner = re.search(r"## 一句話總結\n\*\*(.+?)\*\*", P["index"]).group(1)

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium") if pathlib.Path("/opt/pw-browsers/chromium").is_file() else pw.chromium.launch(); pg = b.new_page(viewport={"width":1300,"height":740})
    logs = []; pg.on("console", lambda m: m.type == "error" and logs.append(m.text)); pg.on("pageerror", lambda e: logs.append(str(e)))
    pg.route("**/fonts.g*/**", lambda r: r.abort())  # 離線也要能正常顯示
    pg.goto(HTML.as_uri()); pg.wait_for_timeout(ANIM_WAIT)
    n = pg.locator(".slide").count()
    refs = pg.eval_on_selector_all("[data-ref]", "els=>els.map(e=>[e.dataset.ref,e.textContent])")
    for ref, txt in refs:
        p, i = ref.split(":")
        want = oneliner if i == "oneliner" else key_points(P[p])[int(i)-1][0]
        if txt.strip() != want: errors.append(f"data-ref {ref} 與 Wiki 不一致：{txt[:25]}… ≠ {want[:25]}…")
    for ref, txt in pg.eval_on_selector_all("[data-code]", "els=>els.map(e=>[e.dataset.code,e.textContent])"):
        p, k = ref.split(":")
        if txt != code(p, int(k)): errors.append(f"data-code {ref} 與 Wiki 不一致")
    for p, txt in pg.eval_on_selector_all("[data-sum]", "els=>els.map(e=>[e.dataset.sum,e.textContent])"):
        if txt != summary(P[p]): errors.append(f"data-sum {p} 與 Wiki 不一致")
    for p, txt in pg.eval_on_selector_all("[data-title]", "els=>els.map(e=>[e.dataset.title,e.textContent])"):
        if txt != title(P[p]): errors.append(f"data-title {p} 與 Wiki 不一致")
    missing = pg.eval_on_selector_all(".slide", "els=>els.map((e,i)=>e.dataset.wiki?null:i+1).filter(Boolean)")
    if missing: errors.append(f"缺少 Wiki 出處的頁面：{missing}")
    for k in range(n):
        cnt = pg.text_content("#count").strip()
        if cnt != f"{k+1} / {n}": errors.append(f"第 {k+1} 頁頁碼錯誤：{cnt}")
        over = pg.evaluate("""()=>{const s=document.querySelector('.slide.active');const r=s.getBoundingClientRect();
          const f=s.querySelector('.from').getBoundingClientRect();let bad=[];
          s.querySelectorAll('h2,li,pre,table,svg,.card,.stat,.callout,.flow,.vs,.gl,.quiz,p').forEach(el=>{const b=el.getBoundingClientRect();
            if(b.height && (b.bottom>f.top+1 || b.right>r.right+1)) bad.push(el.tagName+':'+(el.textContent||'').trim().slice(0,12));});return bad;}""")
        if over: errors.append(f"第 {k+1} 頁內容溢出／壓到頁尾：{over[:3]}")
        op = float(pg.evaluate("()=>getComputedStyle(document.querySelector('.slide.active')).opacity"))
        if op < 0.99: errors.append(f"第 {k+1} 頁截圖時動畫尚未結束（opacity={op:.2f}）")
        vis = pg.evaluate("()=>document.querySelector('.slide.active').innerText")
        if "[[" in vis or "]]" in vis:
            bad = [l.strip()[:40] for l in vis.splitlines() if "[[" in l or "]]" in l]
            errors.append(f"第 {k+1} 頁殘留 Wiki 語法：{bad[:2]}")
        for d in pg.evaluate("""()=>{const s=document.querySelector('.slide.active');const k=s.getBoundingClientRect().width/1280;
            return [...s.querySelectorAll('svg')].map(svg=>{const r=svg.getBoundingClientRect();
              const ts=[...svg.querySelectorAll('text')].map(t=>parseFloat(getComputedStyle(t).fontSize)*svg.getScreenCTM().a/k);
              return {label:svg.getAttribute('aria-label')||'svg',w:r.width/k,h:r.height/k,font:ts.length?Math.min(...ts):99};});}"""):
            if d["w"] < MIN_W or d["h"] < MIN_H:
                errors.append(f"第 {k+1} 頁圖表「{d['label']}」太小：{d['w']:.0f}×{d['h']:.0f}px")
            if d["font"] < MIN_FONT:
                errors.append(f"第 {k+1} 頁圖表「{d['label']}」文字太小：實際 {d['font']:.1f}px < {MIN_FONT}px")
        pg.screenshot(path=str(SHOTS / f"slide-{k+1:02d}.png"))
        pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(ANIM_WAIT)
    pg.click("#prev"); 
    if pg.text_content("#count").strip() != f"{n-1} / {n}": errors.append("上一頁按鈕失效")
    pg.goto(HTML.as_uri() + "#7"); pg.reload(); pg.wait_for_timeout(200)
    if pg.text_content("#count").strip() != f"7 / {n}": errors.append("網址 #7 跳頁失效")
    logs = [l for l in logs if "ERR_FAILED" not in l]  # 排除刻意封鎖的網路字型請求
    if logs: errors.append(f"主控台錯誤：{logs[:3]}")
    b.close()

print(f"簡報 {n} 頁｜逐字比對 {len(refs)} 個 Wiki 重點引用")
if errors:
    print("❌ 簡報檢查未通過："); print("\n".join("  - " + e for e in errors)); sys.exit(1)
print("✅ 簡報檢查通過（截圖已存到 screenshots/）")
