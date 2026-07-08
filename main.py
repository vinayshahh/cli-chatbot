from groq import Groq
from dotenv import load_dotenv
from datetime import date
import os
import json


today = date.today().strftime("%B %d, %Y")
load_dotenv()

client = Groq(api_key=os.getenv("API_KEY"))
print("On your service sir!!!")
messages = []

if os.path.exists("memory.json"):
    with open("memory.json", "r") as f:
        all_messages = json.load(f)
        messages.append({"role": "system", "content": all_messages["summary"]})


while True:
    user_input = input("YOU: ")

    if user_input.lower() == "quit":
        print("See u soon sir!!!")
        messages.append(
            {
                "role": "system",
                "content": "write a summary in json format strictly with keys as title,date as {today},summary of the conversation what user asked about not the summary of topic and the messages in list format and no other text or spaces outside the json the output must be one and only json format",
            }
        )

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b", messages=messages
        )
        raw_memory = response.choices[0].message.content
        parsed_memory = json.loads(raw_memory)
        with open("memory.json", "w") as file:
            json.dump(parsed_memory, file, indent=4)
        break

    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b", messages=messages
    )

    bot_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": bot_reply})
    print(f"Bot: {bot_reply}\n")
