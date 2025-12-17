def balance_assessments(assessments, final_k=10):
    technical = []
    behavioral = []
    others = []

    for a in assessments:
        types = a.get("test_type", [])

        if "Knowledge & Skills" in types:
            technical.append(a)
        elif "Personality & Behavior" in types or "Competencies" in types:
            behavioral.append(a)
        else:
            others.append(a)

    tech_k = int(final_k * 0.6)
    beh_k = final_k - tech_k

    balanced = []
    balanced.extend(technical[:tech_k])
    balanced.extend(behavioral[:beh_k])

    if len(balanced) < final_k:
        remaining = technical[tech_k:] + behavioral[beh_k:] + others
        balanced.extend(remaining[: final_k - len(balanced)])

    return balanced
