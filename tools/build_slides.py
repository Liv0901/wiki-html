"""由 Wiki 生成教學簡報（單一 HTML 檔）。
規則：簡報上的「內容句」只能來自 Wiki 的 ## 重點 條列、程式碼區塊或表格，
每個引用都標上 data-ref="頁面:序號"，由 check_slides.py 逐字比對。
"""
import html, re, json, pathlib
from wikilib import pages, key_points, sources, title, summary

P = pages(); S = sources()
OUT = pathlib.Path(__file__).resolve().parent.parent / "AI-Agents-是什麼.html"
esc = html.escape

def kp(page, i):
    pts = key_points(P[page])
    return pts[i - 1]

def code_block(page, n=1):
    blocks = re.findall(r"```\n(.*?)```", P[page], re.S)
    return blocks[n - 1].rstrip("\n")

def table(page, n=1):
    tables = re.findall(r"((?:^\|.*\|\n)+)", P[page], re.M)
    rows = [r.strip().strip("|").split("|") for r in tables[n - 1].strip().splitlines()]
    rows = [[c.strip() for c in r] for r in rows if not re.match(r"^[-\s|]+$", "|".join(r))]
    clean = lambda c: re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), c)
    head = "".join(f"<th>{esc(clean(c))}</th>" for c in rows[0])
    body = "".join("<tr>" + "".join(f"<td>{esc(clean(c))}</td>" for c in r) + "</tr>" for r in rows[1:])
    return f'<table class="tbl" data-table="{page}:{n}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'

def chips(cites):
    return "".join(f'<a class="chip" href="#src" data-cite="{c}" title="{esc(S[c]["name"])}">{c}</a>' for c in cites)

def point(page, i, cls="pt"):
    text, cites = kp(page, i)
    if "：" in text and text.index("：") < 28:
        head, rest = text.split("：", 1)
        inner = f"<b>{esc(head)}：</b>{esc(rest)}"
    else:
        inner = esc(text)
    return f'<li class="{cls}"><span class="txt" data-ref="{page}:{i}">{inner}</span> {chips(cites)}</li>'

def footer(refs):
    by = {}
    for p, i in refs:
        by.setdefault(p, []).append(str(i))
    s = "　".join(f"{p}.md › 重點 {'、'.join(v)}" for p, v in by.items())
    return f'<footer class="from">📖 Wiki 出處：{esc(s)}</footer>'

slides = []
def add(body, refs, cls="", wiki=None):
    slides.append((body, refs, cls))

# ---------- 1 封面 ----------
oneliner = re.search(r"## 一句話總結\n\*\*(.+?)\*\*", P["index"]).group(1)
add(f'''<div class="cover">
  <p class="kicker">第十週｜以 LLM Wiki 為知識庫的教學簡報</p>
  <h1>AI Agents 是什麼？</h1>
  <p class="lead" data-ref="index:oneliner">{esc(oneliner)}</p>
  <p class="hint">按 → 或空白鍵換頁　·　O 看全部頁面　·　F 全螢幕</p>
</div>''', [("index", "一句話總結")], "s-cover")

# ---------- 2 大綱 ----------
order = ["definition","components","agent-loop","planning","tool-use","memory","workflows-vs-agents","multi-agent","evaluation","risks"]
items = "".join(f'<li><span class="n">{k:02d}</span><span data-title="{p}">{esc(title(P[p]))}</span></li>' for k, p in enumerate(order, 1))
add(f'<p class="kicker">今天的路線</p><h2>學習大綱</h2><ol class="toc">{items}</ol>', [("index", "閱讀路線")])

# ---------- 3 定義 ----------
add(f'''<p class="kicker">01 · 定義</p><h2>{esc(title(P["definition"]))}</h2>
<ul class="pts big">{point("definition",1)}{point("definition",2)}</ul>
<div class="callout">💡 關鍵字：<b>自己決定</b>流程與工具 —— 這是 Agent 和一般程式最大的不同。</div>''',
    [("definition",1),("definition",2)])

# ---------- 4 Agent vs Chatbot vs Workflow ----------
add(f'''<p class="kicker">01 · 定義</p><h2>Agent、聊天機器人、Workflow 差在哪？</h2>
<div class="cols2">
  <ul class="pts">{point("definition",3)}{point("definition",4)}</ul>
  <div class="vs">
    <div class="vs-row"><span class="tag t1">聊天機器人</span><span>一問 → 一答</span></div>
    <div class="vs-row"><span class="tag t2">Workflow</span><span>A → B → C（路徑寫死）</span></div>
    <div class="vs-row"><span class="tag t3">Agent</span><span>想 → 做 → 看 → 再想…（模型決定）</span></div>
  </div>
</div>''', [("definition",3),("definition",4)])

# ---------- 5 自主光譜 ----------
spec = ["單次 LLM 呼叫","強化型 LLM","Workflow","自主 Agent"]
boxes = "".join(f'<g transform="translate({40+i*300},70)"><rect width="250" height="90" rx="14" class="bx b{i}"/><text x="125" y="54" class="bt">{s}</text></g>' for i, s in enumerate(spec))
arrows = "".join(f'<path d="M{290+i*300} 115 h45" class="ar" marker-end="url(#ah)"/>' for i in range(3))
add(f'''<p class="kicker">01 · 定義</p><h2>自主程度是一條光譜</h2>
<svg viewBox="0 0 1240 230" class="dia" role="img" aria-label="自主程度光譜">
<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="ahf"/></marker></defs>
{boxes}{arrows}
<path d="M40 200 H1190" class="ar thick" marker-end="url(#ah)"/>
<text x="40" y="190" class="lbl" text-anchor="start">彈性、成本 ↑　可預測性 ↓</text></svg>
<ul class="pts">{point("workflows-vs-agents",1)}{point("definition",5)}</ul>''',
    [("workflows-vs-agents",1),("definition",5)])

# ---------- 6 核心元件 ----------
comp = [("規劃","待辦清單與檢討會",160,150),("記憶","筆記本與檔案櫃",620,40),("工具","手腳：查資料、寫檔、下指令",1080,150)]
cg = "".join(f'<g><line x1="620" y1="225" x2="{x}" y2="{y+35}" class="ln"/><rect x="{x-130}" y="{y}" width="260" height="76" rx="14" class="bx b{k+1}"/><text x="{x}" y="{y+33}" class="bt">{n}</text><text x="{x}" y="{y+58}" class="bs">{d}</text></g>' for k,(n,d,x,y) in enumerate(comp))
add(f'''<p class="kicker">02 · 核心元件</p><h2>{esc(title(P["components"]))}：大腦 + 三種能力</h2>
<div class="cols2 wide-left">
<svg viewBox="0 0 1240 330" class="dia" role="img" aria-label="Agent 核心元件">
{cg}<circle cx="620" cy="245" r="70" class="core"/><text x="620" y="240" class="bt inv">LLM</text><text x="620" y="268" class="bs inv">大腦</text></svg>
</div>
<ul class="pts tight">{point("components",2)}{point("components",3)}{point("components",4)}</ul>''',
    [("components",1),("components",2),("components",3),("components",4)])

# ---------- 7 Agent loop ----------
add(f'''<p class="kicker">03 · Agent Loop</p><h2>Agent 的心跳：想 → 做 → 看</h2>
<div class="cols2">
<svg viewBox="0 0 560 470" class="dia tall" role="img" aria-label="Agent 迴圈">
<defs><marker id="ah2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="ahf"/></marker></defs>
<rect x="190" y="10" width="180" height="50" rx="25" class="bx b0"/><text x="280" y="42" class="bt">目標</text>
<path d="M280 62 V95" class="ar" marker-end="url(#ah2)"/>
<rect x="170" y="100" width="220" height="70" rx="14" class="bx b1"/><text x="280" y="132" class="bt">Thought</text><text x="280" y="156" class="bs">思考下一步</text>
<rect x="340" y="250" width="200" height="70" rx="14" class="bx b2"/><text x="440" y="282" class="bt">Action</text><text x="440" y="306" class="bs">呼叫工具</text>
<rect x="20" y="250" width="200" height="70" rx="14" class="bx b3"/><text x="120" y="282" class="bt">Observation</text><text x="120" y="306" class="bs">環境回傳結果</text>
<path d="M370 172 Q440 200 440 245" class="ar" marker-end="url(#ah2)"/>
<path d="M338 290 H226" class="ar" marker-end="url(#ah2)"/>
<path d="M120 248 Q120 200 190 172" class="ar" marker-end="url(#ah2)"/>
<path d="M120 322 V380" class="ar dash" marker-end="url(#ah2)"/>
<rect x="20" y="385" width="250" height="66" rx="14" class="bx b4"/><text x="145" y="414" class="bt sm">完成 / 達上限</text><text x="145" y="438" class="bs">→ 輸出答案</text>
</svg>
<ul class="pts tight">{point("agent-loop",1)}{point("agent-loop",4)}{point("agent-loop",5)}</ul>
</div>''', [("agent-loop",1),("agent-loop",4),("agent-loop",5)])

# ---------- 8 ReAct 實例 ----------
add(f'''<p class="kicker">03 · Agent Loop</p><h2>ReAct 實際長什麼樣子？</h2>
<div class="cols2">
<pre class="code" data-code="agent-loop:2">{esc(code_block("agent-loop",2))}</pre>
<ul class="pts tight">{point("agent-loop",2)}{point("agent-loop",3)}</ul>
</div>''', [("agent-loop",2),("agent-loop",3)])

# ---------- 9 規劃 ----------
add(f'''<p class="kicker">04 · 規劃</p><h2>規劃：把大目標拆成小步驟</h2>
<ul class="pts">{point("planning",1)}{point("planning",2)}{point("planning",3)}</ul>
{table("planning",1)}''', [("planning",1),("planning",2),("planning",3)], "dense")

# ---------- 10 反思 ----------
add(f'''<p class="kicker">04 · 規劃</p><h2>反思：從失敗中學習</h2>
<div class="flow">
 <div class="step">① 嘗試任務</div><div class="arr">→</div>
 <div class="step">② 得到回饋<br><small>（測試失敗、評估者意見）</small></div><div class="arr">→</div>
 <div class="step">③ 用文字寫下反思</div><div class="arr">→</div>
 <div class="step">④ 存入記憶，下次讀取</div>
</div>
<ul class="pts big">{point("planning",4)}{point("planning",5)}</ul>''', [("planning",4),("planning",5)])

# ---------- 11 工具 ----------
add(f'''<p class="kicker">05 · 工具使用</p><h2>工具：讓 Agent 從「會說」變成「會做」</h2>
<ul class="pts">{point("tool-use",1)}{point("tool-use",2)}{point("tool-use",4)}</ul>''',
    [("tool-use",1),("tool-use",2),("tool-use",4)])

# ---------- 12 Function calling + ACI ----------
fc = re.search(r"### Function calling 的流程\n(.*?)\n\n", P["tool-use"], re.S).group(1)
fc_items = "".join(f'<li data-fc="{k}">{esc(re.sub(r"[*（）]|見 \[\[.*?\]\]", "", re.sub(r"^\d+\.\s*", "", l)).strip())}</li>' for k, l in enumerate(fc.splitlines(), 1))
add(f'''<p class="kicker">05 · 工具使用</p><h2>Function calling 流程與好工具設計</h2>
<div class="cols2">
  <ol class="steps">{fc_items}</ol>
  <div><ul class="pts">{point("tool-use",3)}</ul>
  <div class="callout">🛡️ 能動手就可能闖禍 → 工具權限要最小化（見「風險」）</div></div>
</div>''', [("tool-use",3),("tool-use","Function calling 的流程")])

# ---------- 13 記憶 ----------
add(f'''<p class="kicker">06 · 記憶</p><h2>記憶：短期靠上下文，長期靠外部儲存</h2>
<div class="cols2">
  {table("memory",1)}
  <ul class="pts tight">{point("memory",1)}{point("memory",2)}{point("memory",3)}</ul>
</div>''', [("memory",1),("memory",2),("memory",3)], "dense")

# ---------- 14 設計模式 ----------
names = ["提示鏈","路由","平行化","協調者－工作者","評估者－最佳化者"]
cards = "".join(f'<div class="card c{k}"><div class="ct">{n}</div><ul class="pts">{point("workflows-vs-agents",k+2,"pt mini")}</ul></div>' for k, n in enumerate(names))
add(f'''<p class="kicker">07 · 設計模式</p><h2>不一定要 Agent：五種常見模式</h2>
<div class="cards">{cards}</div>''', [("workflows-vs-agents",i) for i in range(2,7)], "dense")

# ---------- 15 何時用 + graph/loop ----------
add(f'''<p class="kicker">07 · 設計模式</p><h2>什麼時候該用 Agent？</h2>
<div class="cols2">
<pre class="code" data-code="workflows-vs-agents:1">{esc(code_block("workflows-vs-agents",1))}</pre>
<div class="gl">
  <div class="glc"><b>Workflow ＝ 圖（graph）</b><span>節點與邊由開發者事先定義</span></div>
  <div class="glc"><b>Agent ＝ 迴圈（loop）</b><span>每一輪由模型決定下一個動作</span></div>
  <div class="glc"><b>實務常是混合</b><span>外層是圖，某些節點內部是 Agent 迴圈</span></div>
</div></div>''', [("workflows-vs-agents","決策指南"),("workflows-vs-agents","Graph 與 Loop")])

# ---------- 16 多代理人 ----------
add(f'''<p class="kicker">08 · 多代理人</p><h2>多代理人：分工、對話、互相檢查</h2>
<ul class="pts">{point("multi-agent",1)}{point("multi-agent",2)}{point("multi-agent",3)}</ul>
{table("multi-agent",1)}''', [("multi-agent",1),("multi-agent",2),("multi-agent",3)], "dense")

# ---------- 17 評估 ----------
add(f'''<p class="kicker">09 · 評估</p><h2>評估：不只看答案，要看有沒有真的做完</h2>
<div class="cols2">
  <div class="stat"><div class="num">2,294</div><div class="cap">SWE-bench 題目數</div><div class="num">1.96%</div><div class="cap">發表時最佳模型解題率</div></div>
  <ul class="pts tight">{point("evaluation",1)}{point("evaluation",2)}{point("evaluation",3)}{point("evaluation",4)}</ul>
</div>''', [("evaluation",i) for i in range(1,5)])

# ---------- 18 風險 ----------
add(f'''<p class="kicker">10 · 風險與防護</p><h2>風險：能自主行動，代價也更高</h2>
<div class="cols2">
  <ul class="pts tight">{point("risks",1)}{point("risks",2)}{point("risks",3)}</ul>
  <ul class="pts tight">{point("risks",4)}{point("risks",5)}</ul>
</div>''', [("risks",i) for i in range(1,6)])

# ---------- 19 小測驗 ----------
quiz = [("Agent 與 Workflow 最大的差別是什麼？","definition",3),
        ("ReAct 迴圈的三個步驟是？","agent-loop",1),
        ("為什麼 Agent 一定要設定停止條件？","agent-loop",5),
        ("OWASP 把哪一種風險列為 LLM 應用第一名？","risks",1)]
qz = "".join(f'<details class="q"><summary>Q{k}. {esc(q)}</summary><ul class="pts">{point(p,i)}</ul></details>' for k,(q,p,i) in enumerate(quiz,1))
add(f'<p class="kicker">複習</p><h2>小測驗（點題目看答案）</h2><div class="quiz">{qz}</div>', [(p,i) for _,p,i in quiz])

# ---------- 20 總結 ----------
add(f'''<div class="cover">
<p class="kicker">總結</p><h2>帶走三件事</h2>
<ol class="takeaway">
<li><span data-sum="definition">{esc(summary(P["definition"]))}</span></li>
<li><span data-sum="agent-loop">{esc(summary(P["agent-loop"]))}</span></li>
<li><span data-sum="workflows-vs-agents">{esc(summary(P["workflows-vs-agents"]))}</span></li>
</ol></div>''', [("definition","摘要"),("agent-loop","摘要"),("workflows-vs-agents","摘要")], "s-cover")

# ---------- 21 來源 ----------
srows = "".join(f'<li id="src-{k}"><b>{k}</b> {esc(v["name"])}' + (f' <a href="{esc(v["url"].split()[0])}" target="_blank" rel="noopener">連結</a>' if v["url"].startswith("http") else "") + "</li>" for k, v in S.items())
add(f'<p class="kicker">參考</p><h2 id="src">參考來源</h2><ol class="srcs">{srows}</ol>', [("sources","全部")], "dense")

# ---------- 組裝 ----------
sections = []
for n, (body, refs, cls) in enumerate(slides, 1):
    wiki = ",".join(f"{p}:{i}" for p, i in refs)
    sections.append(f'<section class="slide {cls}" data-wiki="{esc(wiki)}" aria-label="第 {n} 頁">{body}{footer(refs)}</section>')

CSS = pathlib.Path(__file__).with_name("slides.css").read_text(encoding="utf-8")
JS = pathlib.Path(__file__).with_name("slides.js").read_text(encoding="utf-8")
doc = f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Agents 是什麼？</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>
<div id="viewport"><div id="stage">
{chr(10).join(sections)}
</div></div>
<nav id="bar"><button id="prev" aria-label="上一頁">‹</button><span id="count"></span><button id="next" aria-label="下一頁">›</button><button id="ov" aria-label="總覽">▦</button></nav>
<div id="progress"><i></i></div>
<script>{JS}</script>
</body></html>'''
OUT.write_text(doc, encoding="utf-8")
print(f"已生成 {OUT.name}：{len(slides)} 頁")
