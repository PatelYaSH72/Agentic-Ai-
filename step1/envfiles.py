from dotenv import load_dotenv
import os

load_dotenv()

db = os.getenv("STUDENT_DB")
seceret = os.getenv("OPENAI_API_KEY")

print(db)
print(seceret)