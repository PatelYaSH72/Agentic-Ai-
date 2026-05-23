import os
import time
from groq import Groq, RateLimitError, APIConnectionError
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_with_retry(messages, max_retries=3):
    wait_time = 2  # pehli baar 2 second wait

    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}...")
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages
            )
            
            print("Success!")
            return response.choices[0].message.content

        except RateLimitError:
            print(f"Rate limit hit — {wait_time} second ruk raha hoon...")
            time.sleep(wait_time)
            wait_time *= 2  # 2 → 4 → 8

        except APIConnectionError:
            print(f"Connection error — {wait_time} second ruk raha hoon...")
            time.sleep(wait_time)
            wait_time *= 2

    # Teen baar bhi fail hua
    raise Exception("Max retries exceed ho gaye — API unreachable hai")


# Test karo
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is machine learning in one line?"}
]

try:
    result = call_with_retry(messages)
    print("\nResponse:", result)
except Exception as e:
    print("Error:", e)