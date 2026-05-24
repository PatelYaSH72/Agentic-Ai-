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
      print("step 1 completed")
      serach_question = quations



  #step 2: Find relevent documents
   retriver = db.as_retriever(search_kwargs={"k":3})
   docs = retriver.invoke(serach_question)

   print(f"Found {len(docs)} relevent documents")
   for i, doc in enumerate(docs, 1):
      
      lines = doc.page_content.split('\n')[:2]
      preview = '\n'.join(lines)
      print(f" Doc {i}: {preview}...")


   combined_input = f"""Based on the following document, please answer this question {quations}

            Documents: {chr(10).join([f" -{doc.page_content}" for doc in docs])}

            Please provide a clear, helpful answer using only the information from these documents. If you can't find the answer in the own database 


      """
   
   message = [
      SystemMessage(content="You are a helpful assistent that answer questions based on priovided doces")
   ] + chat_message + [
      HumanMessage(content=combined_input)
   ]


   result = model.invoke(message)
   awnser = result.content

   chat_message.append(HumanMessage(content=quations))
   chat_message.append(AIMessage(content=awnser))

   print(f"Awnser: {awnser}")
   return awnser

def start_Chat():
   
   print("Ask me question: Type 'quit' to exit.")

   while True:
      quation = input("Your question: ")

      if quation.lower() == "exit":
         print("Goodbay..")
         break
      
      start_with_quatuion(quation)
      
if __name__ == "__main__":
   start_Chat()