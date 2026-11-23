# Agent Loop 與 ReAct

> 摘要：Agent 的核心是一個迴圈：思考（Thought）→ 行動（Action）→ 觀察（Observation），重複直到完成或觸發停止條件。

## 重點
- ReAct 讓 LLM 交錯產生「推理軌跡」與「任務行動」，推理幫助擬定與更新計畫，行動則從外部取得新資訊。[S2]
- ReAct 在知識問答（HotpotQA）與事實查核（FEVER）中透過 Wikipedia API 查資料，減少了純推理時的幻覺與錯誤傳遞。[S2]
- 在互動決策任務 ALFWorld 與 WebShop 上，ReAct 的成功率分別比模仿學習／強化學習方法高出 34% 與 10%（絕對值）。[S2]
- 實務上，Agent 在每一步都要從環境取得「真實狀態」（例如工具結果或程式執行結果）來判斷進度。[S1]
- 必須設定停止條件（例如最大迭代次數），避免 Agent 無限循環。[S1]

## 迴圈示意
```
目標 ─▶ [Thought] 我需要先查…
          │
          ▼
        [Action] search("…")      ← 呼叫工具
          │
          ▼
        [Observation] 回傳結果     ← 來自環境的真實回饋
          │
          ├─ 尚未完成 → 回到 Thought
          └─ 完成／達上限 → 輸出答案
```

## 範例（ReAct 格式，教學自編）
```
Thought 1: 我要找出 ReAct 論文發表在哪個會議。
Action 1: Search[ReAct Synergizing Reasoning and Acting]
Observation 1: …ICLR 2023…
Thought 2: 已找到答案。
Action 2: Finish[ICLR 2023]
```

## 相關頁面
- [[planning]]（迴圈中的「想」）、[[tool-use]]（迴圈中的「做」）、[[memory]]（迴圈中累積的「看」）
- 回到 [[index|首頁]]
