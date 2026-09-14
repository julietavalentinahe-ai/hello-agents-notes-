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

微软商店版 Python 一律用 python main.py   认不了 py main.py

三、运行显示如下
C:\Users\13706>cd /d D:\hello-agents-main

D:\hello-agents-main>python -m venv venv

D:\hello-agents-main>venv\Scripts\activate

(venv) D:\hello-agents-main>pip install requests tavily-python openai python-dotenv
Collecting requests

  Downloading requests-2.34.2-py3-none-any.whl.metadata (4.8 kB)
Collecting tavily-python

  Downloading tavily_python-0.8.1-py3-none-any.whl.metadata (12 kB)
Collecting openai

  Downloading openai-3.11.0-py3-none-any.whl.metadata (41 kB)
Collecting python-dotenv

  Downloading python_dotenv-1.2.3-py3-none-any.whl.metadata (29 kB)
Collecting charset_normalizer<4,>=2 (from requests)

  Downloading charset_normalizer-3.5.1-cp313-cp313-win_amd64.whl.metadata (46 kB)
Collecting idna<4,>=2.5 (from requests)

  Downloading idna-3.19-py3-none-any.whl.metadata (9.2 kB)
Collecting urllib3<3,>=1.26 (from requests)

  Downloading urllib3-2.7.0-py3-none-any.whl.metadata (6.9 kB)
Collecting certifi>=2023.5.7 (from requests)

  Downloading certifi-2026.7.22-py3-none-any.whl.metadata (2.5 kB)
Collecting tiktoken>=0.5.1 (from tavily-python)

  Downloading tiktoken-0.14.0-cp313-cp313-win_amd64.whl.metadata (6.8 kB)
Collecting httpx (from tavily-python)

  Downloading httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting anyio<5,>=4.10.0 (from openai)

  Downloading anyio-4.15.1-py3-none-any.whl.metadata (4.7 kB)
Collecting httpx2<3,>=2.7.0 (from openai)

  Downloading httpx2-2.12.0-py3-none-any.whl.metadata (9.5 kB)
Collecting jiter<1,>=0.16.0 (from openai)

  Downloading jiter-0.16.0-cp313-cp313-win_amd64.whl.metadata (5.3 kB)
  
Collecting pydantic!=2.0.,!=2.1.,!=2.2.,!=2.3.,<3,>=1.10.13 (from openai)

  Downloading pydantic-2.13.5-py3-none-any.whl.metadata (110 kB)
  
Collecting sniffio (from openai)

  Downloading sniffio-1.3.1-py3-none-any.whl.metadata (3.9 kB)
  
Collecting typing-extensions<5,>=4.14 (from openai)

  Downloading typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
  
Collecting httpcore2==2.12.0 (from httpx2<3,>=2.7.0->openai)

  Downloading httpcore2-2.12.0-py3-none-any.whl.metadata (25 kB)
  
Collecting truststore>=0.10 (from httpx2<3,>=2.7.0->openai)

  Downloading truststore-0.10.4-py3-none-any.whl.metadata (4.4 kB)
  
Collecting h11>=0.16 (from httpcore2==2.12.0->httpx2<3,>=2.7.0->openai)

  Downloading h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
  
Collecting annotated-types>=0.6.0 (from pydantic!=2.0.,!=2.1.,!=2.2.,!=2.3.,<3,>=1.10.13->openai)

  Downloading annotated_types-0.8.0-py3-none-any.whl.metadata (15 kB)
  
Collecting pydantic-core==2.46.5 (from pydantic!=2.0.,!=2.1.,!=2.2.,!=2.3.,<3,>=1.10.13->openai)

  Downloading pydantic_core-2.46.5-cp313-cp313-win_amd64.whl.metadata (6.7 kB)
  
Collecting typing-inspection>=0.4.2 (from pydantic!=2.0.,!=2.1.,!=2.2.,!=2.3.,<3,>=1.10.13->openai)

  Downloading typing_inspection-0.4.4-py3-none-any.whl.metadata (2.6 kB)
  
Collecting regex (from tiktoken>=0.5.1->tavily-python)

  Downloading regex-2026.9.10-cp313-cp313-win_amd64.whl.metadata (41 kB)
  
Collecting httpcore==1.* (from httpx->tavily-python)

  Downloading httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
  
Downloading requests-2.34.2-py3-none-any.whl (73 kB)

Downloading charset_normalizer-3.5.1-cp313-cp313-win_amd64.whl (199 kB)

Downloading idna-3.19-py3-none-any.whl (68 kB)

Downloading urllib3-2.7.0-py3-none-any.whl (131 kB)

Downloading tavily_python-0.8.1-py3-none-any.whl (22 kB)

Downloading openai-3.11.0-py3-none-any.whl (1.7 MB)

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.7/1.7 MB 2.7 MB/s  0:00:00
   
Downloading anyio-4.15.1-py3-none-any.whl (132 kB)

Downloading httpx2-2.12.0-py3-none-any.whl (95 kB)

Downloading httpcore2-2.12.0-py3-none-any.whl (83 kB)

Downloading jiter-0.16.0-cp313-cp313-win_amd64.whl (196 kB)

Downloading pydantic-2.13.5-py3-none-any.whl (472 kB)

Downloading pydantic_core-2.46.5-cp313-cp313-win_amd64.whl (2.0 MB)

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.0/2.0 MB 4.9 MB/s  0:00:00
   
Downloading typing_extensions-4.16.0-py3-none-any.whl (45 kB)

Downloading python_dotenv-1.2.3-py3-none-any.whl (22 kB)

Downloading annotated_types-0.8.0-py3-none-any.whl (13 kB)

Downloading certifi-2026.7.22-py3-none-any.whl (136 kB)

Downloading h11-0.16.0-py3-none-any.whl (37 kB)

Downloading tiktoken-0.14.0-cp313-cp313-win_amd64.whl (940 kB)

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 940.9/940.9 kB 5.6 MB/s  0:00:00
   
Downloading truststore-0.10.4-py3-none-any.whl (18 kB)

Downloading typing_inspection-0.4.4-py3-none-any.whl (14 kB)

Downloading httpx-0.28.1-py3-none-any.whl (73 kB)

Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)

Downloading regex-2026.9.10-cp313-cp313-win_amd64.whl (277 kB)

Downloading sniffio-1.3.1-py3-none-any.whl (10 kB)

Installing collected packages: urllib3, typing-extensions, truststore, sniffio, regex, python-dotenv, jiter, idna, h11, charset_normalizer, certifi, annotated-types, typing-inspection, requests, pydantic-core, httpcore2, httpcore, anyio, tiktoken, pydantic, httpx2, httpx, tavily-python, openai

Successfully installed annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 charset_normalizer-3.5.1 h11-0.16.0 httpcore-1.0.9 httpcore2-2.12.0 httpx-0.28.1 httpx2-2.12.0 idna-3.19 jiter-0.16.0 openai-3.11.0 pydantic-2.13.5 pydantic-core-2.46.5 python-dotenv-1.2.3 regex-2026.9.10 requests-2.34.2 sniffio-1.3.1 tavily-python-0.8.1 tiktoken-0.14.0 truststore-0.10.4 typing-extensions-4.16.0 typing-inspection-0.4.4 urllib3-2.7.0

[notice] A new release of pip is available: 26.1.2 -> 26.2.1

[notice] To update, run: python.exe -m pip install --upgrade pip

(venv) D:\hello-agents-main>notepad code/chapter1/FirstAgentTest.py

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
