import json

from src.revChatGPT.V3 import Chatbot


class MyChat:
    def __init__(self):
        self.chatbot = None
        self.config = None

        self.load_config()
        self.init_chatbot()

    def load_config(self):
        fd = open("./config.json")
        data = json.loads(fd.read())
        self.config = data

    def init_chatbot(self):
        self.chatbot = Chatbot(api_key=self.config.get("apikey"), proxy=self.config.get("proxy"))

    def chat_loop(self):
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
            response = self.chatbot.ask_stream(
                prompt
            )
            for r in response:
                print(r, end="")
            print("")

    def run(self):
        print('Welcome to ChatGPT CLI')
        while True:
            try:
                self.chat_loop()
            except KeyboardInterrupt as e:
                print("C-c 断开连接")

            r = input("$ 输入 run 或者 exit\n")
            if r.strip().upper() == "RUN":
                continue
            elif r.strip().upper() == "EXIT":
                print("chat 结束")
                break
            else:
                continue


if __name__ == '__main__':
    chat = MyChat()
    chat.run()
