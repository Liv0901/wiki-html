"""共用：讀取 Wiki 頁面、解析 [[連結]]、## 重點 條列與 [S#] 來源。"""
import re, pathlib

WIKI = pathlib.Path(__file__).resolve().parent.parent / "wiki"
LINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
CITE = re.compile(r"\[(S\d+)\]")

def pages():
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted(WIKI.glob("*.md"))}

def title(text):
    m = re.search(r"^# (.+)$", text, re.M)
    return m.group(1).strip() if m else ""

def summary(text):
    m = re.search(r"^> 摘要：(.+)$", text, re.M)
    return m.group(1).strip() if m else ""

def key_points(text):
    """回傳 ## 重點 區塊中的條列：[(純文字, [S#...])]"""
    m = re.search(r"^## 重點\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m:
        return []
    out = []
    for line in m.group(1).splitlines():
        if line.startswith("- "):
            body = line[2:].strip()
            cites = CITE.findall(body)
            plain = CITE.sub("", body).strip()
            out.append((plain, cites))
    return out

def sources():
    text = (WIKI / "sources.md").read_text(encoding="utf-8")
    rows = {}
    for line in text.splitlines():
        m = re.match(r"\| (S\d+) \| (.+?) \| (.+?) \| (.+?) \|", line)
        if m:
            rows[m.group(1)] = {"name": m.group(2), "type": m.group(3), "url": m.group(4)}
    return rows
