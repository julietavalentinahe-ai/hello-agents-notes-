# -*- coding: utf-8 -*-
"""
排查用的诊断脚本
用途：验证「三步流程里到底哪一步的回答被 token 上限截断」。
    python debug_finish_reason.py
"""

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "700"))  

llm = ChatOpenAI(
    model=os.getenv("LLM_MODEL"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    temperature=0.7,
    max_tokens=MAX_TOKENS,
)

TOPIC = os.getenv("TOPIC", "AI 编程助手会取代初级程序员吗")


def show(step: str, prompt: str) -> str:
    r = llm.invoke([HumanMessage(content=prompt)])
    meta = getattr(r, "response_metadata", {}) or {}
    usage = meta.get("token_usage") or {}
    finish = meta.get("finish_reason")
    flag = "被截断" if finish == "length" else "正常"
    print(f"[{step}] finish_reason={finish} {flag} "
          f"输出 {usage.get('completion_tokens')}/{MAX_TOKENS} token，正文 {len(r.content)} 字")
    if finish == "length":
        print("   结尾（可以看到话没说完）：", repr(r.content[-40:]))
    return r.content


write_prompt = f"请围绕主题《{TOPIC}》写一篇 200 字左右的短文，要求有清晰的小标题、具体案例和流畅的过渡。"
draft = show("写作", write_prompt)

revise_prompt = (
    "你是资深中文编辑。请根据修改意见，把下面这篇草稿改写为更完善的文章。\n"
    "要求：保留主题与核心观点；补齐缺失的案例或数据；结构更清晰；语言更流畅。\n"
    "直接输出修改后的完整文章正文，不要任何解释、前缀或评分。\n\n"
    f"修改意见：论据不足，缺少小标题\n\n原稿：\n{draft}"
)
show("修订", revise_prompt)

review_prompt = (
    "你是经验丰富的中文编辑。请审阅下面的草稿并打分(0-100)。\n"
    "严格按以下格式回复（不要多余内容）：\n评分：<整数>\n意见：<一句话修改建议>\n\n"
    f"草稿：\n{draft}"
)
show("审阅", review_prompt)

print("\n说明：看到【修订】显示 length，证明文章断了")
print("      下一轮审阅拿到的是残缺文章，分数上不去")
