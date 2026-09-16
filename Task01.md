 ## 一、第一章学习心得

智能体不是按固定脚本执行的普通程序，而是给个目标它会自己想办法（有自主性）, 能感知环境并通过执行器采取行动，其核心运作机制是一个循环：感知 → 思考（规划+选工具）→ 行动 → 观察，然后再回到感知。
智能体与外部交互的输出协议为Thought和 Action；行动两种，要么调用工具要么Finish[最终答案]。


## 二、五分钟快速搭建智能体

2.1

官方库配套的 `FirstAgentTest.py` 是一个会思考、会调天气/景点工具的旅行助手。它用 ReAct 循环（Thought→Action→Observation）自主完成任务

2.2

为了智能体能够根据输入的城市自主完成任务，便在官方代码上做了些小变动

代码改动对照

①	System Prompt 加一句		   使模型输出"天气+景点+行程"

②	记忆 prompt_history      位置移到循环外实现多轮对话

③	智能补全	                 就算只输城市名也能跑

④	兜底解析		               模型漏写格式不会崩

⑤	去掉菜单 	               交互干净

<img width="379" height="65" alt="屏幕截图 2026-09-16 233728" src="https://github.com/user-attachments/assets/bfdd3a76-2dac-49fd-9c24-87208944fcae" />

 ⑥ 删 TravelAssistant 类封装 llm 和历史+ parse_action()、display_conversation() 辅助函数 	 简洁点也不用emoji  
       


① System Prompt 加"Finish 天气+景点+行程” 三个都给

官方版

python

'# AGENT_SYSTEM_PROMPT' 里只有通用的格式要求

改后版本

python

'- Finish[最终答案] 中请包含三部分：①天气概述；②推荐景点及理由；③一日行程安排建议（上午/下午/晚上分别去哪里）'


② 多轮记忆

官方版：

python

'class TravelAssistant:
    def __init__(self):
        self.prompt_history = []        # 每个实例自己一份，初始化为空

def run_assistant(user_input, ...):
    assistant = TravelAssistant()       # 每次进来要新建，上轮历史清空
    
    ...'
    
改后版本： 记忆放在所有循环之外，每轮都往里追加



python

'prompt_history = []                 # 写在 while True 外面

while True:
    raw = input("请输入城市或问题（exit 退出）: ")
    ...
    prompt_history.append(f"用户请求: {user_prompt}")   # 每轮追加用户的请求
    ...
    full_prompt = "\n".join(prompt_history)            # 把历史拼回去再发给模型
    llm_output = llm.generate(full_prompt, ...)
    prompt_history.append(llm_output)                  # 模型说的话记下来'


③ 智能补全

改后不用自己写一长串问题

python

'if not any(k in raw for k in ("天气","行程","景点","游玩","攻略","推荐","查询","查","weather","trip","plan")):
    user_prompt = f"请查询{raw}今天的天气，并根据天气推荐合适的旅游景点和一日行程安排。"
else:
    user_prompt = raw'


④ 兜底解析

官方版： 没匹配到 Action: 就直接报"未能解析"，这一轮停了

python

'action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
if not action_match:
    observation = "错误: 未能解析到 Action 字段。..."
    ...
    continue'
    
改后版本： 模型偶尔漏写 Action: 前缀时，自动兜底解析，不崩溃

python

'if action_match:
    action_str = action_match.group(1).strip()
else:
    fallback = re.search(r"(Finish\[.*?\]\s*$|\w+\([^)]*\))", llm_output, re.DOTALL | re.MULTILINE)
    if fallback:
        action_str = fallback.group(1).strip()
        print("提示：模型漏写了 'Action: ' 前缀，已自动兜底解析。\n")
    else:
        ...'


⑤ 去掉菜单 / 改交互

官方版： 

python

'if __name__ == "__main__":
    print("选择运行模式:")
    print("1. 运行测试示例 (北京)")
    print("2. 交互模式")
    print("3. 快速测试其他城市")
    choice = input("请输入选择 (1/2/3): ").strip()
    ...
    show_history = input("\n📖 是否显示完整对话历史? (y/n): ").strip().lower()'
    
改后版本： 一个循环，直接输城市名

python

'while True:
    raw = input("\n请输入城市或问题（exit 退出）: ").strip()
    if raw.lower() in ("exit", "quit", "q", "退出"):
        break
    ...'



2.3

.env 文件（密钥不直接写死在代码里，而是通过 os.environ 去读 .env 里的值）

① .env —— 纯文本配置文件，里面是 KEY=VALUE，专门放密钥

'# .env.example（模板，复制改名为 .env 后填自己的值）
DASHSCOPE_API_KEY=APIKey
TAVILY_API_KEY=avilyAPIKey


## 三、运行截图

<img width="577" height="463" alt="屏幕截图 2026-09-16 230411" src="https://github.com/user-attachments/assets/0d773721-9080-4028-bffd-30048ec99b4c" />












