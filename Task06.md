Task06 demo 运行截图

用 **LangGraph** 做了一个「写作-审阅-修订」反思循环助手，利用 LangGraph 的 **StateGraph + 条件边** 实现了  「草稿 → 审阅打分 → 不达标则修订再送审」的循环，直到评分 ≥80 或达到最大轮次才退出。  代码用 `TypedDict` 定义全局状态、三个 `Node` 函数对应步骤、`should_continue` 条件边控制循环。


<img width="842" height="134" alt="image" src="https://github.com/user-attachments/assets/3ada8d76-ac51-4893-9e9c-7b8719474906" />


#### 接下来是这个反思循环助手 agent 的用法

它只有一个输入：主题（topic）

给一个主题 → 自动写草稿 → 自动打分 → 不到 80 分就自动修订再送审 → 达标退出 → 存成 article.md

换文章 = 把 topic 覆盖掉
```bash
$env:TOPIC="你想写的题目"; python main.py
```

（`$env:TOPIC` 设一次，终端窗口会有记忆，想恢复默认题目要输 `$env:TOPIC=$null`，或者直接关掉终端重开）

> 补充：输出文件名也能改 —— `$env:OUT_FILE="auto"; python main.py` 会按主题自动命名（如 `article_AI时代的钓鱼邮件.md`），换主题不会覆盖。不设就还是 `article.md`。另外每次运行前，旧稿会自动备份到 `history/` 文件夹（main.py 所在目录下）


下面为 换了个标题运行的截图

<img width="668" height="293" alt="image" src="https://github.com/user-attachments/assets/c9d4a29a-35e4-410e-b8a4-4b5b00728f8e" />



调试日志

问题：写的旧代码跑的时候初稿 78 分，修订后反而降到 75，再改还是 75，一直耗到最大轮次被迫结束

<img width="350" height="218" alt="屏幕截图 2026-10-07 220650" src="https://github.com/user-attachments/assets/8a7a7cd3-2ba5-4752-a8db-440341322cef" />


解决：写个小脚本把 API 每次返回的 finish_reason 打印出来，看看是否为Groq token限制，最后结果写作是 stop（只用 170 token）、审阅也是 stop，只有修订是 length，于是按三个环节的需要分别设额度（审阅 400、写作1200、修订 2000），并加了检测到截断就加倍重试

原因：旧代码的token额度都是700,但修订(revise)token不够，就是说文章没写完，下一轮审阅拿到的是残缺的，所以越改分越低改完实测：78 分 → 修订 → 86 分达标，两轮正常结束，成稿完整保存

📄 代码入口
- 主程序：[main.py](main.py)
- 排查脚本：[debug_finish_reason.py](debug_finish_reason.py)
- 成稿示例：[article.md](article.md)

🔧 关键位置
- 按环节分配额度：[main.py L46–L50](main.py#L46-L50)
- 截断加倍重试：[main.py L73–L80](main.py#L73-L80)
- 80 分及格线：[main.py L214](main.py#L214)
