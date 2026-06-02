from langchain_groq import ChatGroq
from dotenv import load_dotenv
import re

load_dotenv()

llm =ChatGroq(model="llama-3.3-70b-versatile")

tsla_text = """
Tesla's Q3 Results
Tesla reported record revenue of $25.2B in Q3 2024.
The company exceeded analyst expectations by 15%.
Revenue growth was driven by strong vehicle deliveries.
XL to chat, XK to generate
Model Y Performance
The Model Y became the best-selling vehicle globally, with 350,000 units sold.
Customer satisfaction ratings reached an all-time high of 96%.
Model Y now represents 60% of Tesla's total vehicle sales.

Production Challenges
Supply chain issues caused a 12% increase in production costs.
Tesla is working to diversify its supplier base.
New manufacturing techniques are being implemented to reduce costs.

"""

prompt = f"""
You are a text chunking expert. Split this text into logical chunks.

Rules:
- Each chunk should be around 200 characters or less
- Split at natural topic boundaries
- Keep related information together
- Put " <<<SPLIT>>>" between chunks

Text:
{tsla_text}

Return the text with <<<SPLIT>>> markers where you want to split:
"""

print(" Asking AI to chunk the text...")
response = llm.invoke(prompt)
marked_text= str(response.content)

chunks = marked_text.split("<<<SPLIT>>>")

clean_chunks = []
for chunk in chunks:
  cleaned = chunk.strip()
  if cleaned: # Only keep non-empty chunks
    clean_chunks.append(cleaned)

# Show results
print("\n AGENTIC CHUNKING RESULTS:")
print("=" * 50)

for i, chunk in enumerate(clean_chunks, 1):
  print(f"Chunk {i}: ({len(chunk)} chars)")
  print(f'"{chunk}"')
  print()