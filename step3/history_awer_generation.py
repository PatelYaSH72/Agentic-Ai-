from dotenv import load_dotenv
import os
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

persistent_directory = "db/chroma_db"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

model = ChatGroq(model="llama-3.3-70b-versatile")

db = Chroma(
  persist_directory=persistent_directory,
  embedding_function=embeddings
)

chat_message = []

def start_with_quatuion(quations):
   
   #Step 1: Make the question clear using conversation history
   if chat_message:
      #Ask Ai to make the question standalone
      message = [
         SystemMessage(content="ss")
      ] + chat_message + [
         HumanMessage(content=f"New question {quations}")
         ]
      

      result = model.invoke(message)
      serach_question = str(result.content).strip()
      print(f"Searching for: {serach_question}")
   else:
      serach_question = quations

   pass

def start_Chat():
   
   print("Ask me question: Type 'quit' to exit.")

   while True:
      quation = input("Your question: ")

      if quation.lower == "exit":
         print("Goodbay..")
         break
      
      start_with_quatuion(quation)
      
