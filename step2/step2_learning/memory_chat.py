import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

message = [
  {"role":"system","content":"You are a helpful assistant. Remember everything the user tells you."}
]

while True:
  user_input = input("user: ")

  if user_input.lower() == "quit":
    break

  message.append({"role":"user","content":user_input})


  stream = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=message,
    stream=True
  )

  full_response=""
  print("Bot: ", end="")

  for chunk in stream:
      content = chunk.choices[0].delta.content
      if content:
         print(content, end="",flush=True)
         full_response += content
  print()


  message.append({"role":"assistant","content":full_response})