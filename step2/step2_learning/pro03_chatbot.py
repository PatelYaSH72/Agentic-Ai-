import os
from dotenv import load_dotenv
from groq import Groq, RateLimitError, APIConnectionError
import time
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

messages = [
    {"role": "system", "content": "You are a helpful assistant. Remember everything the user tells you."}
]

INPUT_COST  = 0.00059
OUTPUT_COST = 0.00079
total_cost  = 0.0

# Token Budget — max kitne tokens use karne hain
TOKEN_BUDGET = 10000
total_tokens_used = 0

def project03(user_input, max_retry=3):
    global total_cost, total_tokens_used

    # Budget check karo
    if total_tokens_used >= TOKEN_BUDGET:
        print(f"Token budget khatam! {total_tokens_used}/{TOKEN_BUDGET} tokens use ho gaye.")
        return None

    messages.append({"role": "user", "content": user_input})

    wait_second = 2

    for attempt in range(max_retry):
        try:
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages
            )

            # Token tracking
            input_tokens  = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens  = response.usage.total_tokens

            cost = (input_tokens / 1000 * INPUT_COST) + \
                   (output_tokens / 1000 * OUTPUT_COST)

            total_cost        += cost
            total_tokens_used += total_tokens

            # Response nikalo
            full_response = response.choices[0].message.content

            # Memory save karo
            messages.append({
                "role": "assistant",
                "content": full_response
            })

            # Structured JSON output
            result = {
                "response": full_response,
                "tokens": {
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": total_tokens,
                    "budget_remaining": TOKEN_BUDGET - total_tokens_used
                },
                "cost": {
                    "this_request": round(cost, 6),
                    "session_total": round(total_cost, 6)
                }
            }

            return result

        except RateLimitError:
            print(f"Rate limit — {wait_second} sec wait...")
            time.sleep(wait_second)
            wait_second *= 2

        except APIConnectionError:
            print(f"Connection error — {wait_second} sec wait...")
            time.sleep(wait_second)
            wait_second *= 2

    raise Exception("Max retries exceed ho gaye")


# Main loop
print("=== AI Chatbot ===")
print(f"Token Budget: {TOKEN_BUDGET} tokens")
print("'exit' likho band karne ke liye\n")

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "exit":
        print(f"\nTotal cost: ${total_cost:.6f}")
        print(f"Total tokens used: {total_tokens_used}")
        print("Bye!")
        break

    try:
        result = project03(user_input)

        if result:
            print(f"Bot: {result['response']}")
            print(f"[Tokens: {result['tokens']['total']} | Cost: ${result['cost']['this_request']} | Budget remaining: {result['tokens']['budget_remaining']}]")
            print()

    except Exception as e:
        print(f"Error: {e}")