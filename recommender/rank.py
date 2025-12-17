from typing import List, Dict

def rank_assessments(
    retrieved: List[Dict],
    top_k: int = 10
) -> List[Dict]:

    if not retrieved:
        return []

    return retrieved[:top_k]
