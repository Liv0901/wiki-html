# AI Agents Wiki（首頁）

> 主題：AI Agents（AI 代理人）｜語言：繁體中文｜建立日期：2026-11-22
> 這是一個「給大型語言模型與人類都好讀」的 LLM Wiki：每頁一個概念、頁面之間用雙中括號的 wiki 連結互相連結、每個重點都標註來源 `[S#]`（見 [[sources]]）。

## 閱讀路線（建議順序）
1. [[definition|什麼是 AI Agent？]] — 定義、與聊天機器人的差別、自主程度光譜
2. [[components|核心元件]] — LLM 大腦 + 規劃 + 記憶 + 工具
3. [[agent-loop|Agent Loop 與 ReAct]] — 想 → 做 → 看 的循環
4. [[planning|規劃與反思]] — CoT、ToT、任務拆解、Reflexion
5. [[tool-use|工具使用]] — Function calling、Toolformer、MCP
6. [[memory|記憶]] — 短期／長期記憶、Generative Agents、MemGPT
7. [[workflows-vs-agents|Workflow 與 Agent 的設計模式]] — 何時不該用 Agent
8. [[multi-agent|多代理人系統]] — 分工、對話、協調者
9. [[evaluation|評估]] — 怎麼知道 Agent 做得好不好
10. [[risks|風險與防護]] — 提示注入、過度授權、成本失控

## 一句話總結
**AI Agent ＝ 以 LLM 為大腦，在一個「思考 → 行動 → 觀察」的迴圈中，自己決定要用哪些工具、記住什麼、下一步做什麼，直到完成目標的系統。** [S1][S2][S3]

## 其他頁面
- [[glossary|名詞表]]
- [[sources|來源清單]]
- [[log|更新紀錄（ingest log）]]

## 頁面規格（給維護者與 LLM）
- 每頁結構固定：`# 標題` → `> 摘要` → `## 重點`（可被簡報引用的條列，每條附來源）→ 其他說明段落 → `## 相關頁面`。
- 簡報只能引用各頁 `## 重點` 區塊中的句子（由 `tools/build_slides.py` 檢查）。
