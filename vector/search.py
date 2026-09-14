"""
Semantic search over the ingested university documents.
"""
import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_data")
COLLECTION_NAME = "university_docs"

embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

_client = chromadb.PersistentClient(path=CHROMA_PATH)


def search_docs(query: str, n_results: int = 3) -> str:
    """
    Search the university policy documents for the most relevant chunks
    matching the query's meaning. Returns a formatted string of results.
    """
    collection = _client.get_collection(COLLECTION_NAME, embedding_function=embed_fn)
    results = collection.query(query_texts=[query], n_results=n_results)

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    if not docs:
        return "No relevant documents found."

    formatted = []
    for doc, meta in zip(docs, metas):
        source = meta.get("source", "unknown")
        formatted.append(f"[Source: {source}]\n{doc}")

    return "\n\n".join(formatted)


if __name__ == "__main__":
    # Quick standalone test (run vector/ingest.py first)
    print(search_docs("Can a student with low attendance write exams?"))
