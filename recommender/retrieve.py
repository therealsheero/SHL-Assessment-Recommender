import faiss
import pickle
from sentence_transformers import SentenceTransformer
from recommender.rank import rank_assessments
from recommender.balance import balance_assessments

_model = None
_index = None
_metadata = None


def _load_resources():
    global _model, _index, _metadata

    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    if _index is None:
        _index = faiss.read_index("embeddings/faiss_index/index.faiss")

    if _metadata is None:
        with open("embeddings/faiss_index/metadata.pkl", "rb") as f:
            _metadata = pickle.load(f)


def retrieve_assessments(query: str, top_k: int = 10):
    _load_resources()
    query_embedding = _model.encode([query])

    distances, indices = _index.search(query_embedding, 20)

    raw_results = [_metadata[idx] for idx in indices[0]]
    ranked_results = rank_assessments(raw_results, top_k=20)
    balanced_results = balance_assessments(ranked_results, final_k=top_k)

    return balanced_results
