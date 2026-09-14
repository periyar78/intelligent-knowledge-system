"""
Reads all .txt files from /documents, splits into chunks,
generates embeddings, and stores them in a persistent ChromaDB collection.

Run this once (or whenever documents change):
    python vector/ingest.py
"""
import os
import glob
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_data")
DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "..", "documents")
COLLECTION_NAME = "university_docs"

embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50):
    """Simple word-based chunking with overlap."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks


def ingest_documents():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    # Fresh start each time this script is run
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(COLLECTION_NAME, embedding_function=embed_fn)

    all_chunks = []
    all_ids = []
    all_metadatas = []

    txt_files = glob.glob(os.path.join(DOCUMENTS_DIR, "*.txt"))
    print(f"Found {len(txt_files)} documents to ingest.")

    for filepath in txt_files:
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            chunk_id = f"{filename}::chunk{i}"
            all_chunks.append(chunk)
            all_ids.append(chunk_id)
            all_metadatas.append({"source": filename})

    collection.add(documents=all_chunks, ids=all_ids, metadatas=all_metadatas)
    print(f"Ingested {len(all_chunks)} chunks into ChromaDB at '{CHROMA_PATH}'.")


if __name__ == "__main__":
    ingest_documents()
