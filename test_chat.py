# test_chat.py
from chatbot_core import get_chatbot_response

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = get_chatbot_response(user_input)
    print(f"Chatbot: {response}\n")
