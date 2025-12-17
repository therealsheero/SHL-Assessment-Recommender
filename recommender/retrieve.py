import faiss
import pickle
from sentence_transformers import SentenceTransformer

from recommender.rank import rank_assessments
from recommender.balance import balance_assessments

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("embeddings/faiss_index/index.faiss")

with open("embeddings/faiss_index/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)


def retrieve_assessments(query: str, top_k: int = 10):
    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, 20)

    raw_results = [metadata[idx] for idx in indices[0]]
    ranked_results = rank_assessments(raw_results, top_k=20)
    balanced_results = balance_assessments(ranked_results, final_k=top_k)

    return balanced_results
