# 更新紀錄（Ingest Log）

> 回到 [[index|首頁]]｜來源總表見 [[sources]]
> 每次把新資料「吃進」Wiki，都記一筆：讀了什麼、改了哪幾頁、檢查結果。

## 2026-11-22｜初版建置
- 來源：S1–S14（14 筆）
- 建立 13 頁 Wiki，46 條重點；數字型重點 8 項回原文核對（見 fact-check.md）

## 2026-11-23｜Ingest 5 篇來源（S15–S19）
流程：讀原文（arXiv 摘要頁）→ 寫來源摘要卡（`raw/`）→ 找出受影響頁面 → 在各頁 `## 重點` 末尾新增條目（不改舊條目的順序，簡報引用不受影響）→ 更新 sources、glossary、index → 跑檢查。

| 來源 | 摘要卡 | 更新頁面 | 新增重點 |
|---|---|---|---|
| S15 Wang et al. 綜述 | raw/S15-llm-agent-survey.md | [[components]] | 1 條 |
| S16 AgentBench | raw/S16-agentbench.md | [[evaluation]] | 2 條 |
| S17 間接提示注入 | raw/S17-indirect-prompt-injection.md | [[risks]] | 1 條 |
| S18 SWE-agent | raw/S18-swe-agent.md | [[tool-use]] | 1 條 |
| S19 MetaGPT | raw/S19-metagpt.md | [[multi-agent]] | 1 條 |

- 另更新：[[glossary]] 新增 4 個名詞；[[sources]] 新增 5 列。
- 刻意沒寫進 Wiki 的內容：S15 的框架細節（摘要沒有列出元件名稱，需讀全文才能確認）、S16 測了幾個模型（摘要頁數字顯示不出來）、S19 的具體角色名稱（摘要未列）。原則是「摘要裡沒有的就不寫」。
