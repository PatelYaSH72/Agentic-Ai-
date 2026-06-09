from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

persistent_directory = "db/chroma_db"
embedding_model = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma(
  persist_directory=persistent_directory,
  embedding_function=embedding_model,
  collection_metadata={"hnsw:space":"cosine"}
)

query = "How much did Microsoft pay to acquire Github?"

print(f"Query: {query}")


# Method 1
# print("=== METHOD 1: Similarity Search {k=3} ===")
# retriever = db.as_retriever(search_kwargs={"k":3})

# docs = retriever.invoke(query)
# print(f"Retrieved {len(docs)} documents:\n")

# for i, doc in enumerate(docs, 1):
#   print(f"Document {i}):")
#   print(f"{doc.page_content}\n")

#   print("-" * 60)


#Method 2
# print("\n === METHOD 2: Similarity with Score Threshold === ")
# retriever = db.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs={
#       "k": 3,
#       "score_threshold": 0.3
#       } # Only return docs with similarity >= 0.3
# )


#Method 3
print("\n=== METHOD 3: Maximum Marginal Relevance (MMR) ===")
retriever = db.as_retriever(
  search_type="mmr",
  search_kwargs = {
    "k":3,
    "fetch_k":10,
    "lambda_mult": 0.5
  }
)


docs = retriever.invoke(query)
print(f"Retrieved {len(docs)} documents (threshold: 0.3):\n")

for i, doc in enumerate(docs, 1):
  print(f"Document {i}):")
  print(f"{doc.page_content}\n")

print("-" * 60)