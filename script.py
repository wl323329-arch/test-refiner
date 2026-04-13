# 这几行是在给自己列流程，不参与程序运行。
# Python 里以 # 开头的内容叫“单行注释”，解释给人看，解释器会直接忽略。
#接收用户信息
#拼接提示词
#唤醒claude code
#获取claude code的回复
#唤醒codex
#输入到codex
#codex理解，自动执行

# 三引号字符串可以写多行文本。
# 这一段现在相当于写在文件最外层的说明文字，可以理解为文件级注释。
"""Step 1: receive one-line user query from command line."""

# 导入 Python 标准库 subprocess。
# 标准库 = Python 自带的库，不需要额外安装。
# subprocess 的作用：让 Python 程序去启动并控制外部命令，
# 比如这里要在 Python 里执行终端命令 claude。
import subprocess

# 导入 Python 标准库 textwrap。
# 这里主要用其中的 dedent 函数去掉多行字符串前面统一的缩进，
# 让我们写在代码里的 prompt 看起来整齐，发出去的内容也不会多一层空格。
import textwrap


def get_user_query() -> str:
    """
    接收用户在命令行输入的原始问题。
    设计说明：先给用户一个输入提示，去除前后空格，避免空输入导致后续流程报错。
    """

    # while True 表示“无限循环”。
    # 只要函数内部没有 return 或 break，它就会一直重复执行。
    while True:
        # input(...) 会暂停程序，等待用户在终端输入内容。
        # .strip() 是字符串方法，用来去掉首尾空格和换行。
        user_input = input("请用一句话描述你的问题（例如：帮我整理今天的日报）：").strip()

        # if user_input 的意思是：
        # 如果这个字符串不是空字符串，就当作 True。
        if user_input:
            # return 表示“把结果返回出去，并立刻结束函数”。
            return user_input

        # 如果用户什么都没输入，就打印提示，然后循环继续执行。
        print("输入不能为空，请重新输入。")


def build_prompt(user_query: str) -> str:
    """
    根据用户输入的问题，构建给Claude Code的提示词。
    设计说明：提示词需要清晰地告诉Claude Code我们需要它做什么，以及我们期望的输出格式。
    """

    # f"""...""" 叫 f-string，多行版本。
    # 作用：在多行字符串里直接插入变量。
    # 下面的 {user_query} 会在运行时替换成真实的用户输入。
    prompt = textwrap.dedent(f"""
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
    """).strip()
    # .strip() 用来去掉这段多行字符串最前面和最后面的空白字符，
    # 这样发给模型的文本会更干净。

    # 把拼好的 prompt 返回给调用者。
    return prompt


def run_claude_code(prompt: str) -> str:
    """
    第三步 + 第四步：
    调用 Claude Code，并获取它返回的指令文本。

    设计说明：
    - 使用 `claude -p` 以非交互方式调用，便于 Python 程序接收输出。
    - 通过 stdin 把 prompt 传给 Claude，避免命令行参数解析把 prompt 吃掉。
    """

    # try / except 是 Python 的异常处理语法。
    # try 里放“可能出错”的代码；
    # except 里放“出错后怎么处理”。
    try:
        # subprocess.run(...) 是 subprocess 库里最常用的函数之一。
        # 它的作用是：运行一条外部命令，等命令执行完，再把结果返回给 Python。
        result = subprocess.run(
            # 这里传入的是“命令 + 参数”的列表。
            # 列表里的每一项都是一个独立参数。
            # 这样写比直接拼接一整条字符串更清晰，也更安全。
            #
            # 这几项合起来，等价于在终端里输入：
            # claude -p
            [
                # 第 1 项是命令本身：执行 claude。
                "claude",
                # 第 2 项是命令参数。
                # -p 表示 print mode：非交互模式，直接输出答案然后退出。
                "-p",
            ],
            # input=prompt 表示把 prompt 通过标准输入 stdin 传给 claude。
            # stdin 可以理解成“程序运行时喂进去的输入内容”。
            # 这样做比把超长 prompt 直接塞进命令行参数更稳。
            input=prompt,
            # capture_output=True 表示把命令执行后的输出“抓回来”。
            # 不然内容只会显示在终端，Python 代码里拿不到。
            # 抓回来的主要有两部分：
            # 1. stdout：正常输出
            # 2. stderr：报错输出
            capture_output=True,
            # text=True 表示把输出当成字符串处理。
            # 如果不写，拿到的通常是 bytes（字节），初学时不方便使用。
            encoding="utf-8",
            # check=True 表示：
            # 如果命令返回的退出状态不是 0，就自动抛出异常。
            # 一般退出状态 0 代表成功，非 0 代表失败。
            check=True,
        )
    # FileNotFoundError 表示：系统里根本找不到这个命令。
    # 例如 claude 没安装，或者没有加到 PATH 里。
    except FileNotFoundError as exc:
        # raise 表示主动抛出一个异常。
        # RuntimeError 是一个通用运行时错误类型。
        # from exc 表示“把原始错误挂在后面”，方便排查。
        raise RuntimeError("未找到 claude 命令，请先确认 Claude Code 已正确安装。") from exc
    # subprocess.CalledProcessError 表示：
    # 命令确实执行了，但执行失败了，比如参数错误、权限问题、认证失败等。
    except subprocess.CalledProcessError as exc:
        # exc.stderr 是报错信息，exc.stdout 是普通输出。
        # or 的作用是“取第一个有值的内容”。
        # 所以这行代码的意思是：
        # 先用 stderr；没有就用 stdout；再没有就用默认文案。
        error_message = exc.stderr.strip() or exc.stdout.strip() or "Claude Code 调用失败。"
        # f"..." 也是 f-string。
        # 这里把 error_message 插进报错字符串里，方便直接看到原因。
        raise RuntimeError(f"Claude Code 调用失败：{error_message}") from exc

    # result 是 subprocess.run(...) 的返回结果对象。
    # result.stdout 表示命令的标准输出，也就是 Claude 正常返回的文字。
    reply = result.stdout.strip()
    # not reply 表示“reply 是空的”。
    # 比如空字符串 "" 会被当作 False。
    if not reply:
        # 如果没拿到内容，就主动报错，避免后面的流程继续用空数据。
        raise RuntimeError("Claude Code 没有返回任何内容。")

    # 把 Claude 的回复返回给主程序。
    return reply


def main() -> None:
    """程序入口：先完成第一步：接收用户问题。"""

    # 第一步：接收用户信息
    raw_query = get_user_query()

    # 先打印一次，方便你看到输入是否正确被读取
    print(f"你输入的问题是：{raw_query}")

    # 第二步：拼接提示词
    prompt = build_prompt(raw_query)
    print("\n发给 Claude Code 的 prompt：")
    print(prompt)

    # 第三步 + 第四步：唤醒 Claude Code，并获取回复
    claude_reply = run_claude_code(prompt)
    print("\nClaude Code 返回的指令：")
    print(claude_reply)


# __name__ 是 Python 的内置变量。
# 当你“直接运行这个文件”时，__name__ 的值就是 "__main__"。
# 当你“把这个文件当模块导入”时，__name__ 就不是 "__main__"。
# 所以这句 if 的作用是：
# 只有在直接运行 script.py 时，才执行 main()。
if __name__ == "__main__":
    main()
