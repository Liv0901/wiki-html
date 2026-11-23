"""Wiki 檢查器：失敗就列出問題並以非零狀態結束（回到修正步驟）。
檢查項目：
 1. 每個 [[連結]] 都指向存在的頁面（無斷鏈）；程式碼區塊與行內程式碼中的 [[範例]] 不算連結
 2. 內容頁都有 # 標題、> 摘要、## 重點、## 相關頁面
 3. ## 重點 的每一條都至少有一個 [S#]
 4. 每個 [S#] 都在 sources.md 有對應列；sources.md 的每個來源至少被用到一次
 5. 每個內容頁都能從 index 連到（無孤兒頁）
"""
import sys, re
from wikilib import pages, key_points, sources, LINK, CITE, summary

P = pages(); S = sources(); errors = []
FENCE = re.compile(r"```.*?```", re.S); INLINE = re.compile(r"`[^`\n]*`")
def prose(text):
    """去掉程式碼區塊與行內程式碼，只留下會被當成連結的正文"""
    return INLINE.sub("", FENCE.sub("", text))
SPECIAL = {"index", "sources", "glossary", "log"}
used = set()
for name, text in P.items():
    for m in LINK.finditer(prose(text)):
        if m.group(1) not in P:
            errors.append(f"{name}.md：斷鏈 [[{m.group(1)}]]")
    for c in CITE.findall(text):
        used.add(c)
        if c not in S:
            errors.append(f"{name}.md：來源 {c} 不在 sources.md")
    if name in SPECIAL:
        continue
    for need in ["\n## 重點", "\n## 相關頁面"]:
        if need not in text:
            errors.append(f"{name}.md：缺少 {need.strip()}")
    if not summary(text):
        errors.append(f"{name}.md：缺少 > 摘要")
    for i, (pt, cites) in enumerate(key_points(text), 1):
        if not cites:
            errors.append(f"{name}.md：重點 #{i} 沒有來源 → {pt[:30]}")
linked_from_index = {m.group(1) for m in LINK.finditer(P["index"])}
for name in P:
    if name != "index" and name not in linked_from_index:
        errors.append(f"{name}.md：孤兒頁（index 沒有連到）")
for s in S:
    if s not in used - {None} and s not in {c for t in P.values() if t is not P["sources"] for c in CITE.findall(t)}:
        errors.append(f"sources.md：{s} 沒有任何頁面引用")

n_points = sum(len(key_points(t)) for t in P.values())
print(f"頁面 {len(P)}｜重點 {n_points} 條｜來源 {len(S)} 筆｜連結 {sum(len(LINK.findall(t)) for t in P.values())} 個")
if errors:
    print("❌ 檢查未通過：")
    print("\n".join("  - " + e for e in errors)); sys.exit(1)
print("✅ Wiki 檢查通過")
