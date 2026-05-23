import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader 
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

def load_documents(docs_path="docs"):
  """Load all text files from the docs diretory"""
  print(f"Loading documens from {docs_path}")

  if not os.path.exists(docs_path):
    raise FileNotFoundError(f"The directory {docs_path} does not exist. Please create it and add your company")
  
  loader = DirectoryLoader(
    path=docs_path,
    glob="*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding":"utf:8"}
  )

  document = loader.load()

  if len(document) == 0:
    raise FileNotFoundError(f"No .txt files found in {docs_path}. Please add your company documents.")
  
  for i,doc in enumerate(document[:2]):
    print(f"\nDocument {i+1}:")
    print(f" Source: {doc.metadata['source']}")
    print(f" Content length: {len(doc.page_content)} characters")
    print(f" Content preview: {doc.page_content[:100]}...")
    print(f" metadata: {doc.metadata}")

  return document

def split_document(document,chunk_size=800, chunk_overlap=0):

  """Split documents into smaller chunks with overlap"""
  print("Splitting documents into chunks...")

  text_splitter = CharacterTextSplitter(
      chunk_size=chunk_size,
      chunk_overlap=chunk_overlap
  )

  chunks = text_splitter.split_documents(document)

  # if chunks:

  #   for i, chunk in enumerate(chunks[:5]):
  #     print(f"\n--- Chunk {i+1} ---")
  #     print(f"Source: {chunk.metadata['source']}")
  #     print(f"Length: {len(chunk.page_content)} characters")
  #     print(f"Content:")
  #     print(chunk.page_content)
  #     print("-" * 50)

  #   if len(chunks) > 5:
  #     print(f"\n... and {len(chunks) - 5} more chunks")

  return chunks
 
def create_vectore_db(chunks, persist_directory="db/chroma_db"):
  """Create and persist ChromaDB vector store"""
  print("Creating embedding and storing in ChromaDB...")

  embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

  print("--- Creating vector store ---")
  vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=persist_directory,
    collection_metadata={"hnsw:space":"cosine"}
  )

  print("--- Finished creating vector store ---")

  print(f"Vector store created and saved to {persist_directory}")
  return vectorstore

def main():
  print("Main Function")

  #1. Loading the files
  documents = load_documents(docs_path="docs")

  #2 Chunking
  chunks = split_document(documents,chunk_size=800, chunk_overlap=0)

  store_chunks = create_vectore_db(chunks,persist_directory="db/chroma_db")


if __name__ == "__main__":
  main()