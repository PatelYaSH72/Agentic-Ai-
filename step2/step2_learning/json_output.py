import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def sturcture_josn(message):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"system",
                "content":""" You are a helpful assistant.
                Always respond in valid JSON format only.
                No extra text, no markdown, only JSON.

                Format: {
                        "answer":"main jawab yahan",
                        "confidence":"high/medium/low",
                        "follow_up":"ek related sawaal"
                } """             
             },
             {
                 "role":"user",
                 "content":message
             }

        ]   
    )

    raw = response.choices[0].message.content


    try:
        data = json.loads(raw)
        return data
    except:
        return {"error":"Invalid JSON aaya", "raw":raw}
    
result = sturcture_josn("What is Python programming language?")

print("Raw JOSN:")
print(json.dumps(result, indent=2))

print("\nSirf answer:")
print(result["answer"])

print("\nConfidence:")
print(result["confidence"])

print("\nFollow up question:")
print(result["follow_up"])