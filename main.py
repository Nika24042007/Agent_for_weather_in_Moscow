from agent import chat_with_agent


def main() ->None:
    client_message = input("Здравствуйте. Я ваш ИИ-агент для поиска погоды в Москве. Если моя помощь вам не нужна, напишите 'Пока'. Чем я могу помочь?\n>")
    while (client_message != "Пока"):
        print(chat_with_agent(client_message))
        print("\n---------------------------------------------------------\n")
        client_message = input("Я могу чем-нибудь еще помочь?\n>")

if __name__ == "__main__":
    main()

    