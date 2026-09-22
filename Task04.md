# Task04 

## 一、三种范式运行截图

### ReAct（边想边干）
![ReAct 1](Task04_screenshots/react_1.png)
![ReAct 2](Task04_screenshots/react_2.png)
![ReAct 3](Task04_screenshots/react_3.png)
![ReAct 收尾](Task04_screenshots/react_4.png)

每步 `Thought → Action → Observation`，模型说 `Finish[答案]` 才停。本次走到 Finish 给出答案（华为最新手机 = 2024-03-28 发布的 Pura 90 Pro Max），并自己发现"2025.11.25 发布会"是未来日期、判定不合理 → 体现 ReAct 会**自我校验**搜索结果。

### Plan-and-Solve（先计划再执行）
![Plan](Task04_screenshots/plan_1.png)

"正在生成计划"只出现**一次**，然后"执行 1/4 → 4/4"按顺序一口气跑完，中途不回头。苹果题答案 = **70**（15+30+25）。计划质量决定成败。

### Reflection（写完再校对）
![Reflection 1](Task04_screenshots/reflection_1.png)
![Reflection 2](Task04_screenshots/reflection_2.png)
![Reflection 3](Task04_screenshots/reflection_3.png)

机制：生成 → 评审 →（可能）优化，多轮迭代。本次初版直接上埃拉托色尼筛法，第 1 轮反思即判"无需改进" → 只跑 1 轮收敛。质量高，但每轮多调一次模型、费 token。

### 三者对比
| 范式 | 风格 | 适合 |
|---|---|---|
| ReAct | 边想边干，循环到 Finish | 需外部工具、动态决策 |
| Plan-and-Solve | 先计划再执行，一遍成型 | 步骤清晰、结构化任务 |
| Reflection | 写→审→改，多轮 | 重质量、可打磨 |

---

## 二、思考与练习

### Q1　三种范式在"思考/行动"组织上的本质区别？
react 第一步都思考然后行动观察不行再来一轮，plan_and_solve 开始的计划就想好了蓝图接着再行动，reflection 会打磨一段产出且有任务约束

### Q2　智能家居控制助手选哪种范式？
ReAct 为主（每步决定调哪个设备、传什么参数）+ Reflection 润色话术 + Plan-and-Solve 管固定场景（晚安模式）

### Q3　三种范式能否组合？
三者迭代化调用工具，温度自动调节 / 情绪音乐 / 复杂数学解题
**Plan（高层规划）→ ReAct（每步执行+工具）→ Reflection（关键输出质检）**。
温度自动调节偏 **ReAct**（感知→决策→执行）；情绪音乐可加 Reflection 打磨理由；数学解题用 Plan-and-Solve 拆步 + Reflection 验算

### Q4　ReAct 正则解析的脆弱性？更鲁棒方案？
脆弱：①模型不按 `Thought:/Action:` 格式；②工具名写中文（`计算[...]` 非 `Calculator[...]`）正则匹配不到；③输入含 `]` 截断；④直接给答案不写 Action；⑤思考泄露到 Action 行
更稳：JSON 结构化输出（`json.loads`）、Function Calling / Tool Calling API（SDK 直接解析）、约束解码、Pydantic 校验。生产首选函数调用；正则轻量但易碎。

### Q5　计算器工具 + 失败处理
`calculator`：支持 `+-*/` 和括号，中文 `×÷` 转英文，`eval` 计算，除零优雅报错。注册 `Calculator`。
 失败处理：`fail_count` 计数，Action 格式非法或工具名不存在时 +1，成功归零；连续 ≥3 次往历史追加强提示"可用工具只有 Search、Calculator，请严格用 Tool[输入]"，让模型自己纠正。
 工具涨到 50–100 个：不能全塞 prompt（挑花眼、token 爆）。工程做法：**工具检索/RAG** 先语义筛 5–10 个，或分组/分层。

### Q6　Plan-and-Solve 深入分析
动态重规划：每步执行后验证，失败则从当前状态重生成剩余计划（不从头）。
北京→上海商务旅行：ReAct 更合适，需查实时库存、步骤间有依赖反馈（航班满换班），Plan-and-Solve 列死计划不会灵活改。
分层规划：先高层抽象计划（订机票→酒店→租车），再对每步生成子计划。优势：降复杂度、易重规划、可并行复用。

### Q7　Reflection 深入分析
双模型（强模型反思/快模型执行）：质量↑成本↓，但延迟↑、critic 过严会反复改。
终止条件："无需改进/达上限"基本合理但粗糙；可加置信度阈值、可执行验证（测试通过才停）、LLM-as-judge 分数。
论文助手多维 Reflection：逻辑性 / 创新性 / 语言 / 引用规范 四个维度并行评审，引用维度接真实文献库防幻觉。

### Q8　提示词工程
ReAct 提示词强调循环格式（`Thought/Action/Observation`+`Finish`）逼逐步；Plan-and-Solve 分两段（先只出计划、再只执行）用阶段隔离防提前行动。差异服务各自核心逻辑。
角色设定塑造批判视角："严格评审专家"挑错重规范；"可读性维护者"重命名注释。同一代码不同角色不同优化方向。
few-shot：加 1–2 个标准格式样例，小模型遵循率显著提升，代价占 token。

### Q9　电商客服智能体
范式：ReAct 为主（理解意图+调工具：查订单/物流/判退款/发邮件）+ Reflection 兜底（置信度低时自我反思给审慎建议）。
工具：`query_order`（订单信息）、`query_logistics`（物流状态）、`check_refund_policy`（政策判定）、`send_email`（发回复）。
提示词：立场锚定"合法合规、控损失且让用户被尊重"；政策红线写死、语气共情不过度承诺、决定留痕可审计。
风险：误退款（金额阈值+人工复核）、隐私泄露（脱敏+最小权限）、幻觉（只基于工具真实返回作答）、提示注入（输入清洗）、情绪冲突（升级人工）。

---
### 错误点回顾
1. Q2 把 Reflection 当多设备调度方案（错，它只打磨输出）→ 应选 ReAct。
2. Q1 把 Reflection 说成"筛选工具"（错，是生成→评审→优化）。
3. Q3 举例混淆：温度调节偏 ReAct。
