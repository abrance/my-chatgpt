from revChatGPT.V3 import Chatbot


MYAPIKEY = ""
MYPROXY = ""


chatbot = Chatbot(api_key=MYAPIKEY, proxy=MYPROXY)


def start_chat():
    print('Welcome to ChatGPT CLI')
    while True:
        prompt = input('> ')

        response = ""

        response = chatbot.ask(
            prompt
        )

        print(response)


if __name__ == '__main__':
    start_chat()
