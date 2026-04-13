#接收用户信息
#拼接提示词
#唤醒claude code
#获取claude code的回复
#唤醒codex
#输入到codex
#codex理解，自动执行
"""Step 1: receive one-line user query from command line."""


def get_user_query() -> str:
    """
    接收用户在命令行输入的原始问题。
    设计说明：先给用户一个输入提示，去除前后空格，避免空输入导致后续流程报错。
    """

    while True:
        user_input = input("请用一句话描述你的问题（例如：帮我整理今天的日报）：").strip()

        if user_input:
            return user_input

        print("输入不能为空，请重新输入。")

def build_prompt(user_query:str) ->str:
    """
    根据用户输入的问题，构建给Claude Code的提示词。
    设计说明：提示词需要清晰地告诉Claude Code我们需要它做什么，以及我们期望的输出格式。
    """

    prompt = f"""
    你是一位善解人意的需求分析专家，擅长把用户模糊的想法改写成可直接交给编码 Agent 执行的清晰指令。

    【用户原始问题】
    {user_query}

    【你的任务】
    1. 推断用户的真实意图与关键约束（输入、输出、边界条件）。
    2. 将其改写为一条目标明确、动词开头、可独立执行的指令。
    3. 如有必要，补全用户省略但执行所必需的信息；不要引入用户未提及的额外需求。

    【输出要求】
    - 只输出改写后的指令本身，不要解释、前言、引号或 Markdown 标记。
    - 指令须简洁、具体、无歧义，控制在两句话以内。
    - 使用祈使句，直接描述要做的事。

    【严格禁止】
    - 禁止在本轮对话中修改任何代码或文件，你的唯一职责是产出指令文本。
    """.strip()


    return prompt


def main() -> None:
    """程序入口：先完成第一步：接收用户问题。"""

    # 第一步：接收用户信息
    raw_query = get_user_query()

    # 先打印一次，方便你看到输入是否正确被读取
    print(f"你输入的问题是：{raw_query}")


if __name__ == "__main__":
    main()
