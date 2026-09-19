# Task03  大语言模型基础
  

## 一、本地模型部署跑通

### 1.1 部署方案

| 项目     | 内容                                                  |
| ------ | --------------------------------------------------- |
| 推理框架   | **Ollama**（本地模型运行环境，自带 OpenAI 兼容 API）               |
| 本地服务地址 | `http://localhost:11434`                            |
| 使用模型   | **qwen3:0.6b**          |
| 调用方式   | 用 `openai` 库指向 Ollama 的兼容端点 |
| 脚本位置   | `code/chapter3/local_deploy_ollama.py`              |

### 1.2
官方 `code/chapter3/Qwen.py` 走的是 `transformers` 路线，Ollama 模型已经下载在本地, 没用`Qwen.py`

### 1.3 核心代码

```python
from openai import OpenAI

# base_url 指向本机 Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",          
)

response = client.chat.completions.create(
    model="qwen3:0.6b",
    messages=[{"role": "user", "content": "你好，请用一句话介绍你自己"}],
)

print(response.choices[0].message.content)
```

### 1.4 运行步骤与结果


**方式一：脚本调用（Python 用 `openai` 库指向本机 Ollama）**

```bash
cd /d D:\hello-agents-main
venv\Scripts\activate
python code/chapter3/local_deploy_ollama.py
```

运行输出：

<img width="572" height="107" alt="屏幕截图 2026-09-19 211504" src="https://github.com/user-attachments/assets/a537e069-5822-4a97-b7e3-55cfccc02d4f" />


**方式二：命令行交互模式（`ollama run`，本地跑通截图）**

```bash
cd /d D:\hello-agents-main
ollama run qwen3:0.6b
```

<img width="562" height="346" alt="屏幕截图 2026-09-19 233839" src="https://github.com/user-attachments/assets/4b4d883c-877a-4a2d-aaf6-218cd1686eee" />

学习心得
大模型通过猜概率高的词来回答问题，会出现幻觉，需要调用工具，RAG，验证。大模型每一步都在补上一代的短板。N-gram 只会数相邻词频，没见过的组合概率直接是 0；词嵌入把"语义"变成能计算的向量；BPE 用合并字符对解决了词表爆炸又保留了新词覆盖；Transformer 的自注意力让每个词能同时看全句、还能并行算。最后 到了 GPT 只预测下一个词。本地部署可以使隐私不出本机、零 API 费用、可离线。


