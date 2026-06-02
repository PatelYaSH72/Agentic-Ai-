import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# ChromaDB persistent directory
persistent_directory = "db/chroma_db"

# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load ChromaDB
db = Chroma(
    persist_directory=persistent_directory,
    embedding_function=embedding_model,
    collection_metadata={"hnsw:space": "cosine"}
)

# User query
query = "Who is founder of Google?"

# Retriever
retriever = db.as_retriever(search_kwargs={"k": 1})

# Retrieve relevant documents
relevant_docs = retriever.invoke(query)

# Print user query
print("=" * 60)
print(f"User Query: {query}")
print("=" * 60)

# Print retrieved context
print("\n--- Retrieved Context ---\n")

for i, doc in enumerate(relevant_docs, 1):
    print(f"Document {i}:")
    print(doc.page_content)
    print("-" * 60)

# Combine retrieved documents into prompt
combined_input = f"""
You are a helpful AI assistant.

Answer the following question only using the provided documents.

Question:
{query}

Documents:
{chr(10).join([doc.page_content for doc in relevant_docs])}

Instructions:
- Use only the provided document context
- Do not use external knowledge
- If the answer is not found, say:
  "Answer not found in the provided documents."
"""

# Load Groq model
model = ChatGroq(
    model="llama-3.3-70b-versatile"
)

# Messages
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content=combined_input),
]

# Generate response
result = model.invoke(messages)

# Final output
print("\n=== Generated Response ===\n")
print(result.content)
print("\n" + "=" * 60)