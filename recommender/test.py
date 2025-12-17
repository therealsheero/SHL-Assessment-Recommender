from recommender.retrieve import retrieve_assessments
#from recommender.retrieve import retrieve_assessments

results = retrieve_assessments(
    "Looking for a Java developer with good collaboration skills",
    top_k=5
)
for r in results:
    print(r["name"], " | ", r["test_type"])
