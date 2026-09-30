Task06 demo 运行截图

用 **LangGraph** 做了一个「写作-审阅-修订」反思循环助手，利用 LangGraph 的 **StateGraph + 条件边** 实现了  「草稿 → 审阅打分 → 不达标则修订再送审」的循环，直到评分 ≥80 或达到最大轮次才退出。  代码用 `TypedDict` 定义全局状态、三个 `Node` 函数对应步骤、`should_continue` 条件边控制循环。


<img width="842" height="134" alt="image" src="https://github.com/user-attachments/assets/3ada8d76-ac51-4893-9e9c-7b8719474906" />
