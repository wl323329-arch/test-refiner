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


def main() -> None:
    """程序入口：先完成第一步：接收用户问题。"""

    # 第一步：接收用户信息
    raw_query = get_user_query()

    # 先打印一次，方便你看到输入是否正确被读取
    print(f"你输入的问题是：{raw_query}")


if __name__ == "__main__":
    main()
