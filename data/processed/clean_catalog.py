import pandas as pd
df = pd.read_csv("data/raw/shl_catalog_raw.csv")

print("Raw rows:", len(df))
df = df.drop_duplicates()
df = df.drop_duplicates(subset=["url"])

print("Unique assessments after deduplication:", len(df))
df["description"] = df["description"].fillna("")
df["job_levels"] = df["job_levels"].fillna("")
df["languages"] = df["languages"].fillna("")
df["assessment_length"] = df["assessment_length"].fillna("")
df["test_type"] = df["test_type"].apply(
    lambda x: x if isinstance(x, str) else str(x)
)
assert len(df) >= 377, "Less than 377 assessments after cleaning!"

df.to_csv("data/processed/shl_catalog_clean.csv", index=False)

print("Cleaned catalog saved to data/processed/shl_catalog_clean.csv")
