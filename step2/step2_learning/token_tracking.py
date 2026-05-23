import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

INPUT_COST = 0.0059
OUTPUT_COST = 0.0079

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

total_cost = 0

def call_with_bot(message):
  global total_cost

  response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=message
  )

  input_tokens = response.usage.prompt_tokens
  output_tokens = response.usage.completion_tokens
  total_tokens = response.usage.total_tokens

  cost = (input_tokens / 1000*INPUT_COST) + \
          (output_tokens / 1000*OUTPUT_COST)
  
  total_cost += cost

  print(f"\n--- Token Usage ---")
  print(f"Input tokens  : {input_tokens}")
  print(f"Output tokens : {output_tokens}")
  print(f"Total tokens  : {total_tokens}")
  print(f"Is request ka cost : ${cost:.6f}")
  print(f"Session total cost : ${total_cost:.6f}")
  print(f"-------------------\n")

  return response.choices[0].message.content


message = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is machine learning in one line?"}
]

result = call_with_bot(message)
print(result)