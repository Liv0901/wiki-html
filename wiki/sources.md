# 來源清單（Sources）

> 本 Wiki 每一個重點句後面的 `[S#]` 都對應到下表。S1–S14 於 2026-11-22、S15–S19 於 2026-11-23 確認標題、作者與網址；S15–S19 為第二批 ingest，內容只取自 arXiv 摘要原文（見 [[log]]）。
> 回到 [[index|首頁]]

| 編號 | 來源 | 類型 | 網址 | 用於頁面 |
|---|---|---|---|---|
| S1 | Anthropic（Schluntz & Zhang），〈Building effective agents〉，2024-12 | 業界工程文章 | https://www.anthropic.com/engineering/building-effective-agents | [[definition]]、[[components]]、[[workflows-vs-agents]]、[[tool-use]]、[[evaluation]]、[[risks]] |
| S2 | Yao et al.，〈ReAct: Synergizing Reasoning and Acting in Language Models〉，ICLR 2023 | 論文 | https://arxiv.org/abs/2210.03629 | [[agent-loop]] |
| S3 | Lilian Weng，〈LLM Powered Autonomous Agents〉，2023-06 | 綜述部落格 | https://lilianweng.github.io/posts/2023-06-23-agent/ | [[components]]、[[planning]]、[[memory]]、[[tool-use]] |
| S4 | Shinn et al.，〈Reflexion: Language Agents with Verbal Reinforcement Learning〉，NeurIPS 2023 | 論文 | https://arxiv.org/abs/2303.11366 | [[planning]]、[[memory]] |
| S5 | Park et al.，〈Generative Agents: Interactive Simulacra of Human Behavior〉，UIST 2023 | 論文 | https://arxiv.org/abs/2304.03442 | [[memory]]、[[multi-agent]] |
| S6 | Schick et al.，〈Toolformer: Language Models Can Teach Themselves to Use Tools〉，NeurIPS 2023 | 論文 | https://arxiv.org/abs/2302.04761 | [[tool-use]] |
| S7 | Packer et al.，〈MemGPT: Towards LLMs as Operating Systems〉，2023 | 論文 | https://arxiv.org/abs/2310.08560 | [[memory]] |
| S8 | Wei et al.，〈Chain-of-Thought Prompting Elicits Reasoning in Large Language Models〉，NeurIPS 2022 | 論文 | https://arxiv.org/abs/2201.11903 | [[planning]] |
| S9 | Yao et al.，〈Tree of Thoughts: Deliberate Problem Solving with Large Language Models〉，NeurIPS 2023 | 論文 | https://arxiv.org/abs/2305.10601 | [[planning]] |
| S10 | Wu et al.，〈AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation〉，2023 | 論文 | https://arxiv.org/abs/2308.08155 | [[multi-agent]] |
| S11 | Jimenez et al.，〈SWE-bench: Can Language Models Resolve Real-World GitHub Issues?〉，ICLR 2024 | 論文 | https://arxiv.org/abs/2310.06770 | [[evaluation]] |
| S12 | Anthropic，〈Introducing the Model Context Protocol〉，2024-11 | 官方公告 | https://www.anthropic.com/news/model-context-protocol | [[tool-use]] |
| S13 | OWASP，〈Top 10 for LLM Applications 2025〉 | 安全標準 | https://genai.owasp.org/llm-top-10/ （交叉查證：https://www.hackerone.com/blog/owasp-top-10-llms-2025-how-genai-risks-are-evolving ） | [[risks]] |
| S14 | Russell & Norvig，《Artificial Intelligence: A Modern Approach》第 4 版，2020 | 教科書 | （紙本／出版社） | [[definition]] |
| S15 | Wang et al.，〈A Survey on Large Language Model based Autonomous Agents〉，Frontiers of Computer Science，2024 | 綜述論文 | https://arxiv.org/abs/2308.11432 | [[components]] |
| S16 | Liu et al.，〈AgentBench: Evaluating LLMs as Agents〉，ICLR 2024 | 論文（基準） | https://arxiv.org/abs/2308.03688 | [[evaluation]] |
| S17 | Greshake et al.，〈Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection〉，2023 | 論文（資安） | https://arxiv.org/abs/2302.12173 | [[risks]] |
| S18 | Yang et al.，〈SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering〉，2024 | 論文 | https://arxiv.org/abs/2405.15793 | [[tool-use]] |
| S19 | Hong et al.，〈MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework〉，2023 | 論文 | https://arxiv.org/abs/2308.00352 | [[multi-agent]] |

## 來源選擇原則
1. **一手優先**：提出概念的原始論文（ReAct、Reflexion、Toolformer…）優先於二手轉述。
2. **一個重點至少一個來源**：沒有來源能支持的句子不寫進 Wiki。
3. **新舊平衡**：經典定義（S14）＋ 2022–2024 的 LLM Agent 研究 ＋ 業界實務（S1、S12）＋ 安全標準（S13）。
4. **數字只引原文**：例如 SWE-bench 題數、ReAct 的提升幅度，皆取自論文摘要。
