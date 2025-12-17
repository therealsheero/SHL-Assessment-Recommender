import pandas as pd
import faiss
import pickle
from sentence_transformers import SentenceTransformer

df = pd.read_csv("data/processed/shl_catalog_clean.csv")

def build_text(row):
    return (
        f"Assessment Name: {row['name']}. "
        f"Description: {row['description']}. "
        f"Test Type: {row['test_type']}. "
        f"Job Levels: {row['job_levels']}."
    )

texts = df.apply(build_text, axis=1).tolist()

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts, show_progress_bar=True)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
faiss.write_index(index, "embeddings/faiss_index/index.faiss")

with open("embeddings/faiss_index/metadata.pkl", "wb") as f:
    pickle.dump(df.to_dict(orient="records"), f)

print(f"FAISS index built with {index.ntotal} assessments")
