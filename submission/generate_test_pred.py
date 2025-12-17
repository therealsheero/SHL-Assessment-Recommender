import pandas as pd
from recommender.retrieve import retrieve_assessments

DATA_PATH = "data/Gen_AI Dataset.xlsx"
SHEET_NAME = "Test-Set"
OUTPUT_PATH = "submission/test_predictions.csv"
TOP_K = 10

def main():
    test_df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME)

    test_df.columns = (
        test_df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    if "query" not in test_df.columns:
        raise ValueError(f"Expected column 'query', found: {test_df.columns.tolist()}")

    rows = []

    for query in test_df["query"]:
        results = retrieve_assessments(query, top_k=TOP_K)

        for r in results:
            rows.append({
                "Query": query,
                "Assessment_url": r["url"]
            })

    submission_df = pd.DataFrame(rows)
    submission_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved predictions to {OUTPUT_PATH}")
    print(f"Total rows: {len(submission_df)}")

if __name__ == "__main__":
    main()
