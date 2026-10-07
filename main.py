# -*- coding: utf-8 -*-

import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv

# 加载同目录下的 .env（把 key 写进 .env 后无需每次 set 环境变量）
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage


# ============================================================================
# 1) 全局状态 State —— 贯穿整张图的共享数据结构
# ============================================================================
class WritingState(TypedDict):
    messages: Annotated[list, add_messages]   # 对话/过程记录
    topic: str                                # 写作主题
    draft: str                                # 当前草稿
    score: int                                # 审阅评分 0-100
    comments: str                             # 审阅意见
    round: int                                # 当前循环轮次
    max_rounds: int                           # 最大修订轮次（安全阀）
    final_doc: str                            # 最终成稿
    step: str                                 # 当前所处步骤（便于观测）
    fact_check: str                           # 文中需要人工核实的事实点清单


# ============================================================================
# 2) LLM 客户端：真实 / Mock 双模式
# ============================================================================
REAL_LLM = bool(os.getenv("LLM_API_KEY"))

if REAL_LLM:
    from langchain_openai import ChatOpenAI
    _llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
        temperature=0.7,
    )

    # ---- 按用途分配输出预算----
    BASE_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    BUDGET = {
        "review": 400,                              # 只回评分/意见
        "write": max(800, int(BASE_TOKENS * 0.6)),  # 初稿
        "revise": BASE_TOKENS,                      # 修订稿 
    }
    _bound = {}

    def _get_llm(max_tokens: int):
        if max_tokens not in _bound:
            _bound[max_tokens] = _llm.bind(max_tokens=max_tokens)
        return _bound[max_tokens]

    def _invoke(prompt: str, max_tokens: int):
        r = _get_llm(max_tokens).invoke([HumanMessage(content=prompt)])
        meta = getattr(r, "response_metadata", {}) or {}
        return r.content, meta.get("finish_reason")

    def call_llm(prompt: str, kind: str = "write") -> str:
        # 用 HumanMessage 发送，兼容 Groq 上要求 user 角色的模型（像 gpt-oss / qwen3）
        import time
        budget = BUDGET.get(kind, BASE_TOKENS)
        last_err = None
        for attempt in range(4):
            try:
                content, finish = _invoke(prompt, budget)
                # 截断保护：被 token 上限砍断时，预算翻倍再要一次
                if finish == "length":
                    print(f"   ⚠️ 输出被截断（{budget} token 不够），自动加倍重试…")
                    content2, finish2 = _invoke(prompt, budget * 2)
                    if finish2 != "length" or len(content2) > len(content):
                        content, finish = content2, finish2
                    if finish == "length":
                        print("   ⚠️ 仍被截断，本轮内容可能不完整。")
                return content
            except Exception as e:  # noqa: BLE001
                last_err = e
                msg = str(e)
                if "429" in msg or "rate_limit" in msg.lower():
                    wait = 20 * (attempt + 1)
                    print(f"   ⏳ 触发限流，等待 {wait}s 后重试（第 {attempt+1} 次）…")
                    time.sleep(wait)
                else:
                    raise
        raise last_err
else:
    # ---- Mock 模式：无需联网可演示完整循环 ----
    class _Mock:
        def __init__(self):
            self.review_calls = 0
            self.write_calls = 0

        def respond(self, prompt: str, kind: str) -> str:
            if kind == "write":
                self.write_calls += 1
                return (
                    f"【关于《{TOPIC}》的初稿（第{self.write_calls}版）】\n"
                    "这是一段结构尚不完整、缺乏案例支撑的示例草稿，"
                    "用于演示 LangGraph 的循环能力。"
                )
            if kind == "review":
                self.review_calls += 1
                # 评分逐轮提升，演示「反思-修订」最终达标退出
                score = min(60 + self.review_calls * 15, 92)
                return (
                    f"评分：{score}\n"
                    f"意见：第{self.review_calls}次审阅。文章整体方向正确，"
                    f"但{'论据不足、缺少小标题' if score < 80 else '已较为完整，可交付'}。"
                )
            if kind == "revise":
                return (
                    "【修订稿】在上一版基础上补充了小标题、数据案例与过渡句，"
                    "逻辑更清晰，可读性提升。"
                )
            return "（mock 无内容）"

    _mock = _Mock()

    def call_llm(prompt: str, kind: str = "write") -> str:
        return _mock.respond(prompt, kind)


TOPIC = "远程办公时代的团队协作"  # 默认主题，可用环境变量 TOPIC 覆盖


# ============================================================================
# 3) 节点 Nodes —— 每个节点是一个 (state -> dict) 的函数
# ============================================================================
def write_node(state: WritingState) -> dict:
    """步骤1：根据主题生成/修订草稿。"""
    # 事实性约束：LLM 为了满足「要有案例/数据」最容易编造细节（幻觉），
    # 所以明确禁止虚构机构名、金额、时间；不确定时改用模糊表述。
    FACT_RULE = (
        "【事实性要求】严禁编造具体的机构名、人物名、金额、时间、报告名称。"
        "举例时优先使用公开报道过的真实事件；"
        "若无法确定，请用「某跨国企业」「公开报道的一起案件」等模糊表述，"
        "不要为了显得具体而杜撰细节。\n"
    )
    topic = state.get("topic") or TOPIC
    prompt = (
        f"请围绕主题《{topic}》写一篇 200 字左右的短文，"
        "要求有清晰的小标题、具体案例和流畅的过渡。\n"
        + FACT_RULE
    )
    draft = call_llm(prompt, kind="write")
    return {
        "draft": draft,
        "step": "written",
        "round": state.get("round", 0) + 1,
        "messages": [AIMessage(content=f"✍️ 第 {state.get('round',0)+1} 轮写作完成。")],
    }


def review_node(state: WritingState) -> dict:
    """步骤2：审阅打分，给出修改意见。"""
    draft = state["draft"]
    prompt = (
        "你是经验丰富的中文编辑。请审阅下面的草稿并打分(0-100)。\n"
        "请从「结构是否清晰、案例是否具体、语言是否流畅」三方面如实评价，\n"
        "并给出 2 条最关键的修改建议。评分保持客观：一般初稿在 70-80 分，\n"
        "润色完善后可到 85 分以上。\n"
        "另外注意：若文中出现疑似杜撰的机构名、金额、时间等具体细节，"
        "应视为硬伤并扣分，同时在意见里点名要求删除或改成模糊表述。\n\n"
        f"草稿：\n{draft}\n\n"
        "严格按以下格式回复（不要多余内容）：\n"
        "评分：<整数>\n"
        "意见：<一句话修改建议>\n"
        "待核实：<文中出现的机构名/金额/时间/报告名等需要人工核实的细节，"
        "用分号分隔；若文中没有这类细节就写 无>"
    )
    result = call_llm(prompt, kind="review")
    # 解析评分
    import re
    score = 0
    comments = result
    fact_check = ""
    for line in result.splitlines():
        if line.startswith("评分"):
            try:
                score = int("".join(ch for ch in line if ch.isdigit()))
            except ValueError:
                score = 0
        if line.startswith("意见"):
            comments = line.split("：", 1)[-1].strip()
        if line.startswith("待核实"):
            # 兼容中文冒号「：」和英文冒号「:」两种写法
            fact_check = line.replace("：", ":", 1).split(":", 1)[-1].strip()
    # 兜底：模型未严格按「评分：」输出时，从全文取第一个 0-100 的整数
    if score == 0:
        for m in re.findall(r"\b(\d{1,3})\b", result):
            v = int(m)
            if 0 <= v <= 100:
                score = v
                break
    # 每轮审阅都立刻把待核实清单打出来，避免只在最后才出现、容易被漏看
    if fact_check and fact_check != "无":
        print("   🔎 待核实：", "；".join(x.strip() for x in fact_check.replace(";", "；").split("；") if x.strip()))
    return {
        "score": score,
        "comments": comments,
        "fact_check": fact_check,
        "step": "reviewed",
        "messages": [AIMessage(content=f"🔍 审阅评分：{score} / 100 —— {comments}")],
    }


def revise_node(state: WritingState) -> dict:
    """步骤3：根据审阅意见修订草稿。"""
    draft = state["draft"]
    comments = state["comments"]
    prompt = (
        "你是资深中文编辑。请根据修改意见，把下面这篇草稿改写为更完善的文章。\n"
        "要求：保留主题与核心观点；补齐缺失的案例或数据；结构更清晰；语言更流畅。\n"
        "篇幅控制在 700-900 字，务必写完整并以句号结尾，不要中途停止。\n"
        "【事实性要求】严禁编造具体的机构名、人物名、金额、时间、报告名称；"
        "若原稿中有无法核实的细节，请改为模糊表述或直接删掉，不要保留杜撰内容。\n"
        "直接输出修改后的完整文章正文，不要任何解释、前缀或评分。\n\n"
        f"修改意见：{comments}\n\n原稿：\n{draft}"
    )
    revised = call_llm(prompt, kind="revise")
    return {
        "draft": revised,
        "step": "revised",
        "round": state.get("round", 0) + 1,   # 每修订一轮计数+1，作为安全阀依据
        "messages": [AIMessage(content="🔧 已根据审阅意见完成修订，重新送审。")],
    }


# ============================================================================
# 4) 条件边 Conditional Edge —— 实现 循环 / 退出 判断
# ============================================================================
def should_continue(state: WritingState) -> str:
    """根据评分与轮次决定下一步路由。"""
    if state["score"] >= 80:
        return "accept"                      # 达标 -> 结束
    if state["round"] >= state["max_rounds"]:
        return "accept"                      # 达安全阀 -> 强制结束
    return "revise"                          # 不达标 -> 回到修订节点


# ============================================================================
# 5) 构建并编译图 Graph
# ============================================================================
def build_graph():
    workflow = StateGraph(WritingState)
    workflow.add_node("write", write_node)
    workflow.add_node("review", review_node)
    workflow.add_node("revise", revise_node)

    workflow.add_edge(START, "write")
    workflow.add_edge("write", "review")
    # 条件边：review 之后根据 should_continue 决定走向
    workflow.add_conditional_edges(
        "review",
        should_continue,
        {
            "accept": END,        # 评分达标或轮次用尽 -> 结束
            "revise": "revise",    # 不达标 -> 回到修订
        },
    )
    workflow.add_edge("revise", "review")   # 修订完再次送审（形成循环）

    return workflow.compile()


# ============================================================================
# 6) 运行入口
# ============================================================================
def main():
    global TOPIC
    topic_env = os.getenv("TOPIC")
    TOPIC = topic_env or TOPIC
    out_file_env = os.getenv("OUT_FILE", "")
    max_rounds = int(os.getenv("MAX_ROUNDS", "4"))

    print("=" * 60)
    print("📝 LangGraph 写作-审阅-修订 反思循环助手")
    print(f"   主题：{TOPIC}")
    # 防呆提醒：没设 TOPIC 时明确告知用的是默认题目，避免"换题失败还以为换了"
    if topic_env is None:
        print("   ⚠️ 本次未设置 TOPIC，使用的是默认题目！")
        print("      换题目请先运行： $env:TOPIC=\"你的题目\"; python main.py")
    # 防呆提醒：手动设了 OUT_FILE 但没设 TOPIC，最容易把题目错填进文件名
    if topic_env is None and out_file_env and out_file_env.lower() != "auto":
        print("   ⚠️ 你设置了 OUT_FILE 却没设置 TOPIC——OUT_FILE 只管\"存成什么文件名\"，")
        print("      管不了\"写什么题目\"。想换题+按题存稿，一条命令：")
        print('      $env:TOPIC="你的题目"; $env:OUT_FILE="auto"; python main.py')
    print(f"   模式：{'真实 LLM' if REAL_LLM else 'Mock（无 Key 演示）'}")
    print(f"   最大轮次：{max_rounds}")
    print("=" * 60)

    app = build_graph()
    init_state = {
        "topic": TOPIC,
        "draft": "",
        "score": 0,
        "comments": "",
        "round": 0,
        "max_rounds": max_rounds,
        "final_doc": "",
        "step": "start",
        "messages": [],
    }

    final = None
    for event in app.stream(init_state, stream_mode="values"):
        # 打印每一步的关键状态，方便观测图的执行轨迹
        s = event
        if s.get("step") in ("written", "reviewed", "revised"):
            print(f"[{s['step']:<8}] 轮次={s.get('round')} 评分={s.get('score')}")
        final = s

    print("=" * 60)
    print("✅ 流程结束")
    print(f"   最终轮次：{final['round']}  最终评分：{final['score']}")
    if final["score"] >= 80:
        print("   状态：✅ 质量达标，成稿如下：")
        print("-" * 60)
        print(final["draft"])
    else:
        print("   状态：⚠️ 达到最大轮次仍未达标，以上为当前最优稿。")

    # ---- 事实核查清单：把文中需要人工核实的细节单独列出来 ----
    fact = final.get("fact_check", "").strip()
    if fact and fact != "无":
        print("=" * 60)
        print("🔎 需要人工核实的事实点（AI 可能记错，用前请搜一遍）：")
        for item in fact.replace(";", "；").split("；"):
            item = item.strip()
            if item:
                print(f"   · {item}")
    else:
        print("=" * 60)
        print("🔎 待核实清单：本轮审阅未列出需核实的细节")
        print("   （可能是文章里本来就没有具体数据，也可能是小模型没按要求输出这行）")
    print("=" * 60)

    # ---- 把成稿保存成 Markdown 文件，方便直接拿去交作业 ----
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 输出文件名：默认 article.md；
    # 可用环境变量 OUT_FILE 指定（如 OUT_FILE="我的文章.md"）；
    # 设为 auto 则按主题自动命名，换主题不会再互相覆盖。
    out_name = os.getenv("OUT_FILE", "article.md").strip() or "article.md"
    if out_name.lower() == "auto":
        safe = "".join(ch for ch in TOPIC if ch not in '\\/:*?"<>|').strip()[:40]
        out_name = f"article_{safe}.md"
    if not out_name.endswith(".md"):
        out_name += ".md"
    out_path = os.path.join(base_dir, out_name)

    # 保存前先备份上一版旧稿到 history/，避免直接被覆盖后找不回来
    import shutil
    import datetime
    if os.path.exists(out_path):
        history_dir = os.path.join(base_dir, "history")
        os.makedirs(history_dir, exist_ok=True)
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(history_dir, f"article_{stamp}.md")
        shutil.copyfile(out_path, backup_path)
        print(f"📦 上一版旧稿已备份到：{backup_path}")

    mode_txt = "真实 LLM" if REAL_LLM else "Mock（无 Key 演示）"
    content = (
        f"# {TOPIC}\n\n"
        f"> 由 LangGraph「写作-审阅-修订」反思循环自动生成 ｜ "
        f"最终评分：{final['score']}/100 ｜ 轮次：{final['round']} ｜ 模式：{mode_txt}\n\n"
        f"{final['draft']}\n"
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"💾 成稿已保存到：{out_path}")


if __name__ == "__main__":
    main()
