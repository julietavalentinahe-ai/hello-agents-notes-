Hello-Agents 入门篇 Task00 打卡笔记：环境配置与跑通第一个智能体
资料来源：Datawhale《Hello-Agents 入门篇》官方仓库 https://github.com/datawhalechina/hello-agents   本笔记为个人学习记录，转载请标注来源

一、我的环境配置步骤（Windows）
下载代码：浏览器打开仓库 → 绿色 Code → Download ZIP → 解压到 D:\hello-agents-main
进目录：cmd 里先 D: 切盘，再 cd hello-agents-main
建虚拟环境：python -m venv venv
激活：venv\Scripts\activate（命令行前面出现 (venv) 才算成功）
装依赖：pip install requests tavily-python openai python-dotenv
申请两个免费 Key：Tavily（tavily.com 注册拿 tvly-xxx）、AIHubmix（aihubmix.com，模型中心选「免费」标签下的模型）
改代码：记事本打开 code/chapter1/FirstAgentTest.py，替换下面四行
API_KEY = "sk-xxx"                             # 替换 YOUR_API_KEY
BASE_URL = "https://aihubmix.com/v1"           # 不要漏了结尾的 /v1
MODEL_ID = "免费标签下的模型名"           
os.environ['TAVILY_API_KEY'] = "tvly-xxx"      # 替换 YOUR_TAVILY_API_KEY
跑：python code/chapter1/FirstAgentTest.py
二、操作小要点总结
教程 4.3 的 .env / 系统环境部分在这一章可以直接在下载的 D:\hello-agents-main\code\chapter1\FirstAgentTest.py 里替换那四行
FirstAgentTest.py 是把 Key 写死成占位符（API_KEY = "YOUR_API_KEY"），不读 .env。直接改那 4 行代码，建 .env 是白费劲。

微软商店版 Python 一律用 python main.py   认不了 py main.py，

三、运行显示如下
(venv) D:\hello-agents-main>python code/chapter1/FirstAgentTest.py
用户输入: 你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。
========================================
--- 循环 1 ---

正在调用大语言模型...
大语言模型响应成功。
模型输出:
Thought: 用户想了解北京今天的天气，然后根据天气情况获得旅游景点推荐。我需要先查询北京的实时天气，这是后续推荐景点的必要前提。
Action: get_weather(city="北京")

Observation: 北京当前天气：Sunny，气温27摄氏度
========================================
--- 循环 2 ---

正在调用大语言模型...
大语言模型响应成功。
已截断多余的 Thought-Action 对
模型输出:
Thought: 已经获取到北京今天的天气信息：晴朗（Sunny），气温27摄氏度，天气很好。接下来需要根据这个天气情况搜索合适的旅游景点推荐。
Action: get_attraction(city="北京", weather="Sunny")

Observation: Under sunny weather, visit the Temple of Heaven, the Forbidden City, and the Olympic Park. These spots offer clear views and are less crowded.
========================================
--- 循环 3 ---

正在调用大语言模型...
大语言模型响应成功。
模型输出:
Thought: 我已经获取到北京今天的天气信息（晴朗，27摄氏度），并根据晴天天气获得了旅游景点推荐（天坛、故宫、奥林匹克公园）。现在信息已经足够，可以给用户一个完整的答案了。
Action: Finish[北京今天的天气为晴朗（Sunny），气温27摄氏度，非常适合出游。根据这样的好天气，为您推荐以下旅游景点：天坛、故宫和奥林匹克公园。这些景点在晴天游览视野开阔、景色优美，而且游客相对较少，可以更好地享受游览体验。祝您旅途愉快！]

任务完成，最终答案: 北京今天的天气为晴朗（Sunny），气温27摄氏度，非常适合出游。根据这样的好天气，为您推荐以下旅游景点：天坛、故宫和奥林匹克公园。这些景点在晴天游览视野开阔、景色优美，而且游客相对较少，可以更好地享受游览体验。祝您旅途愉快！

(venv) D:\hello-agents-main>

四、心得思考
跟着仓库步骤一步步完成环境配置并跑通，在这过程中巩固了 Python 函数、类与异常处理（try/except），更重要的是理清了 venv/依赖/Key 的配置流程，把一个项目跑起来的通用流程基本上是 搭环境、装依赖、填凭证最后跑通。配环境像跟单纯写代码逻辑比起来更立体
