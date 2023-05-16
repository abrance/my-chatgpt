import pathlib

from src.revChatGPT.V3 import Chatbot
from src.revChatGPT.typing import APIConnectionError
from util import load_config


class MyChat:
    def __init__(self):
        self.chatbot = None
        self.config = load_config()
        self.history_filename = "history"
        self.init_chatbot()
        # sessions 就是 conv 的概念
        self.sessions = []

    def init_chatbot(self):
        self.chatbot = Chatbot(api_key=self.config.get("apikey"), proxy=self.config.get("proxy"))

    def ask_continue(self, conv="default") -> str:
        response = None
        # response = self.chatbot.ask_stream(
        #     "continue"
        # )
        try:
            response = self.chatbot.ask_stream(
                "continue",
                convo_id=conv
            )
        except APIConnectionError as e:
            print(e)
        answer = ""
        for r in response:
            print(r, end="")
            answer += r

        return answer

    def chat_loop(self, conv="default"):
        while True:
            # 聊天样式
            try:
                prompt = input('> ')
            except UnicodeDecodeError as e:
                print("error: {}, 重新输入".format(e))
                continue
            # 如果输入字符低于 2 个字,认为是输入错误
            # 因为 chatgpt 经常不说完, 所以补全
            if prompt in ("g", "go", "go ", "go o", "go on"):
                print("asking continue ...")
                prompt = "continue"

            if len(prompt.strip()) < 2:
                print("输入字符必须超过 2 个")
                continue

            response = None
            try:
                response = self.chatbot.ask_stream(
                    prompt,
                    convo_id=conv
                )
            except APIConnectionError as e:
                print(e)

            answer = ""
            for r in response:
                print(r, end="")
                answer += r

            while True:
                if answer[-1] not in ["!", "?", ".", "。", "？", "！"]:
                    answer = self.ask_continue(conv=conv)
                else:
                    break

            print("")

    def run(self, conv="default"):
        print('Welcome to ChatGPT CLI')
        print("conv: ", conv)
        while True:
            try:
                self.chat_loop(conv=conv)
            except KeyboardInterrupt as e:
                print("C-c 断开连接")
            except BaseException as be:
                print(be)

            r = input("$ 输入 run 或者 exit 或者 reset\n")
            if r.strip().upper() == "RUN":
                continue
            elif r.strip().upper() == "EXIT":
                print("chat 结束")
                break
            elif r.strip().upper() == "RESET":
                # self.chatbot.reset(convo_id=conv)
                del self.chatbot.conversation[conv]
                print("reset")
                break
            else:
                continue
        self.save_session()

    def save_session(self):
        self.chatbot.save(self.history_filename)

    def select_session(self):
        r = input("$ 输入 session 编号或 session name 或者 exit\n")
        if r.strip().upper() == "EXIT":
            return None
        elif len(r) > 10:
            print("session name 不允许超过 10 个")
            return None
        elif r.isdigit():
            index = int(r)
            if len(self.sessions) < index:
                print("index no found: ", r)
                return None
            else:
                return self.sessions[index]
        elif len(r) < 2:
            print("session name 不允许少于 2 个")
            return None
        else:
            return r

    def list_sessions(self):
        if pathlib.Path(self.history_filename).exists():
            print("session list: ")
            self.chatbot.load(self.history_filename)
            for i, conv in enumerate(self.chatbot.conversation.keys()):
                print(i, ": ", conv)
                self.sessions.append(conv)
        else:
            pass


if __name__ == '__main__':
    chat = MyChat()
    chat.list_sessions()
    session_name = chat.select_session()
    print(session_name)
    if not session_name:
        pass
    else:
        chat.run(conv=session_name)
