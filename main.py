import json

from revChatGPT.V3 import Chatbot


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

    def run(self):
        print('Welcome to ChatGPT CLI')
        while True:
            # 聊天样式
            prompt = input('> ')

            response = ""
            response = self.chatbot.ask(
                prompt
            )
            print(response)


if __name__ == '__main__':
    chat = MyChat()
    chat.run()
