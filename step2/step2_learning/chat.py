import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv(""))

stream = client.chat.completions.create(
  model="llama-3.3-70b-versatile",
  messages=[
    {"role":"system","content":"You are a helpful assistant."},
    {"role":"user","content":"What is  Python in one line?"}
  ],
  stream=True
)

for chunk in stream:
  content = chunk.choices[0].delta.content
  if content:
    print(content,end="",flush=True)


print()