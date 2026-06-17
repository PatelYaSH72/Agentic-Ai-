from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from pydantic import BaseModel
from typing import List
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

persistent_directry = "db/chroma_db"
embedding_model=  HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
llm = ChatGroq(model="llama-3.3-70b-versatile")

db = Chroma(
  persist_directory=persistent_directry,
  embedding_function=embedding_model,
  collection_metadata={"hnsw:space":"cosine"}
)


class QueryVariations(BaseModel):
  queries: List[str]


original_query = "How does Tesla make money?"
print(f"Original Query: {original_query}\n")

llm_with_tools = llm.with_structured_output(QueryVariations)

prompt = f"""Generate 3 different variations of this query that would help retrieve relevant documents:
{original_query}

Return 3 alternative queries that rephrase or approach the same question from different angles."""

response = llm_with_tools.invoke(prompt)
query_variations = response.queries

print("Generated Query Variations:", response)
for i, variation in enumerate(query_variations, 1):
   print(f"{i}. {variation}")

print("\n" + "="*60)

retirever = db.as_retriever(search_kwargs={"k":5 })
all_retrievl_results = []
 
for i, query in enumerate(query_variations, 1):
   print(f"\n === RESULTS FOR QUERY {i}: {query} === ")

   docs = retirever.invoke(query)
   all_retrievl_results.append(docs)

   print(f"Retrieved {len(docs)} documents:\n")

   for j, doc in enumerate(docs, 1):
    print(f"Document {j}:")
    print(f"{doc.page_content [:150]} ... \n")

   print("-" * 50)



def reciprocal_rank_fusion(chunk_lists, k=60):

    rrf_scores = defaultdict(float)
    all_unique_chunks = {}

    for chunks in chunk_lists:

        for position, chunk in enumerate(chunks, 1):

            chunk_content = chunk.page_content

            all_unique_chunks[chunk_content] = chunk

            position_score = 1 / (k + position)

            rrf_scores[chunk_content] += position_score

    sorted_chunks = sorted(
        [
            (all_unique_chunks[chunk_content], score)
            for chunk_content, score in rrf_scores.items()
        ],
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_chunks

fused_results = reciprocal_rank_fusion(all_retrievl_results, k=60)          


# ──────────────────────────────────────────────────────────────────
# Step 4: Display Final Fused Results
# ──────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("FINAL RRF RANKING")
print("="*60)

print(f"\nTop {min(10, len(fused_results))} documents after RRF fusion:\n")

for rank, (doc, rrf_score) in enumerate(fused_results[:10], 1):
    print(f"🏆 RANK {rank} (RRF Score: {rrf_score:.4f})")
    print(f"{doc.page_content[:200]}...")
    print("-" * 50)

print(f"\n✅ RRF Complete! Fused {len(fused_results)} unique documents from {len(query_variations)} query variations.")
print("\n💡 Key benefits:")
print("   • Documents appearing in multiple queries get boosted scores")
print("   • Higher positions contribute more to the final score") 
print("   • Balanced fusion using k=60 for gentle position penalties")

# ──────────────────────────────────────────────────────────────────
# Optional: Quick Usage Examples
# ──────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("USAGE EXAMPLES")
print("="*60)