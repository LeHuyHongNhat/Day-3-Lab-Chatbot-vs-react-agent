import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

model_name = "gemini-2.5-pro"

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "exit":
        break

    response = client.models.generate_content(model=model_name, contents=user_input)
    print("Bot:", response.text)