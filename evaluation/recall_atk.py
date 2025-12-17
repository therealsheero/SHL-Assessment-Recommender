import pandas as pd
from recommender.retrieve import retrieve_assessments

K = 10

def compute_recall_at_k(retrieved_urls, relevant_urls, k=10):
    retrieved_top_k = set(retrieved_urls[:k])
    relevant_set = set(relevant_urls)

    if len(relevant_set) == 0:
        return 0.0

    hits = retrieved_top_k.intersection(relevant_set)
    return len(hits) / len(relevant_set)

def normalize_url(url: str) -> str:
    if not isinstance(url, str):
        return ""

    url = url.lower().strip()
    url = url.replace("http://", "https://")
    url = url.rstrip("/")
    url = url.replace("/solutions/products/product-catalog", "")
    url = url.replace("/products/product-catalog", "")
    url = url.replace("/products/assessments", "")

    return url


def main():
    train_df = pd.read_excel("data/Gen_AI Dataset.xlsx", sheet_name="Train-Set")

    grouped = train_df.groupby("Query")["Assessment_url"].apply(list)

    recalls = []

    print("\nEvaluating Recall@10:\n")

    for query, relevant_urls in grouped.items():
        results = retrieve_assessments(query, top_k=K)
        retrieved_urls = [normalize_url(r["url"]) for r in results]
        relevant_urls = [normalize_url(u) for u in relevant_urls]


        recall = compute_recall_at_k(retrieved_urls, relevant_urls, K)
        recalls.append(recall)

        print(f"Query: {query}")
        print(f"Recall@10: {recall:.2f}\n")

    mean_recall = sum(recalls) / len(recalls)
    print(f"Mean Recall@10: {mean_recall:.3f}")

if __name__ == "__main__":
    main()
