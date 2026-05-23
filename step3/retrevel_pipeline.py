import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
load_dotenv()

persistent_directory = "db/chroma_db"

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma(
    persist_directory=persistent_directory,
    embedding_function=embedding_model,
    collection_metadata={"hnsw:space":"cosine"}
)

query = "Who is founder of the Google"

retriver = db.as_retriever(search_kwargs={"k":3})


relevent_docs = retriver.invoke(query)

print(f"User Query: {query}")

print("---Context---")
for i, doc in enumerate(relevent_docs, 1):
  print(f"Document {i}:\n{doc.page_content}\n")

combined_input = f"""
                Based on the following documents, please answer this quation: {query}

Documentes: {chr(10).join([f"-{doc.page_content}" for doc in relevent_docs])}

Please provide a clear, helpful answer using only the information from these documents. If you can't find the answer in the correct, you  dont use own tranning dataset, only use this document data
"""

model = ChatGroq(model="llama-3.3-70b-versatile")

messages = [
  SystemMessage(content="You are a hepful assistent."),
  HumanMessage(content=combined_input),
]

result = model.invoke(messages)

print("\n--- Generated Response ---")


print("Content only:")
print(result.content)