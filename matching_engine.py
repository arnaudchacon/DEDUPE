"""
Core matching engine using Levenshtein distance with weighted scoring.
Uses rapidfuzz for fast string similarity computation.
"""

import pandas as pd
from rapidfuzz import distance
from utils import (
    normalize_string, normalize_phone, normalize_email_domain,
    normalize_website, classify_score,
)


# Default field weights (must sum to 100 for percentage interpretation)
DEFAULT_WEIGHTS = {
    "company_name": 30,
    "email": 20,
    "phone": 15,
    "address": 15,
    "contact_name": 10,
    "website": 10,
}


def levenshtein_similarity(a, b):
    """Calculate normalized Levenshtein similarity (0-100)."""
    if not a or not b:
        return 0.0
    max_len = max(len(a), len(b))
    if max_len == 0:
        return 100.0
    dist = distance.Levenshtein.distance(a, b)
    return round((1 - dist / max_len) * 100, 1)


def compare_records(record_a, record_b, field_weights=None):
    """
    Compare two records across all weighted fields.
    Returns (total_score, per_field_scores) where total_score is 0-100.
    """
    if field_weights is None:
        field_weights = DEFAULT_WEIGHTS

    scores = {}

    # Company name
    scores["company_name"] = levenshtein_similarity(
        normalize_string(record_a.get("company_name", "")),
        normalize_string(record_b.get("company_name", "")),
    )

    # Email domain
    domain_a = normalize_email_domain(record_a.get("email", ""))
    domain_b = normalize_email_domain(record_b.get("email", ""))
    if domain_a and domain_b:
        scores["email"] = 100.0 if domain_a == domain_b else levenshtein_similarity(domain_a, domain_b)
    else:
        scores["email"] = 0.0

    # Phone (compare last 8 digits to ignore country code variations)
    phone_a = normalize_phone(record_a.get("phone", ""))
    phone_b = normalize_phone(record_b.get("phone", ""))
    if phone_a and phone_b:
        scores["phone"] = 100.0 if phone_a[-8:] == phone_b[-8:] else levenshtein_similarity(phone_a, phone_b)
    else:
        scores["phone"] = 0.0

    # Address + City combined
    addr_a = normalize_string(
        str(record_a.get("address", "") or "") + " " + str(record_a.get("city", "") or "")
    )
    addr_b = normalize_string(
        str(record_b.get("address", "") or "") + " " + str(record_b.get("city", "") or "")
    )
    scores["address"] = levenshtein_similarity(addr_a, addr_b)

    # Contact name
    scores["contact_name"] = levenshtein_similarity(
        normalize_string(record_a.get("contact_name", "")),
        normalize_string(record_b.get("contact_name", "")),
    )

    # Website
    web_a = normalize_website(record_a.get("website", ""))
    web_b = normalize_website(record_b.get("website", ""))
    scores["website"] = levenshtein_similarity(web_a, web_b)

    # Weighted total
    weight_sum = sum(field_weights.get(f, 0) for f in scores)
    if weight_sum > 0:
        total = sum(scores[f] * field_weights.get(f, 0) for f in scores) / weight_sum
    else:
        total = 0.0
    total = round(total, 1)

    return total, scores


def find_duplicates(df, field_weights=None, threshold=60, candidate_pairs=None):
    """
    Find duplicate pairs in a DataFrame.

    Args:
        df: DataFrame with CRM records
        field_weights: dict of field -> weight
        threshold: minimum score to consider a pair (default 60)
        candidate_pairs: optional list of (idx_a, idx_b) from blocking.
                        If None, compares all pairs (N²).

    Returns:
        List of dicts with keys: idx_a, idx_b, record_id_a, record_id_b,
        company_a, company_b, total_score, field_scores, classification
    """
    if field_weights is None:
        field_weights = DEFAULT_WEIGHTS

    results = []
    records = df.to_dict("records")

    if candidate_pairs is None:
        # Brute force all pairs
        pairs = [(i, j) for i in range(len(records)) for j in range(i + 1, len(records))]
    else:
        pairs = candidate_pairs

    for idx_a, idx_b in pairs:
        total, field_scores = compare_records(records[idx_a], records[idx_b], field_weights)

        if total >= threshold:
            results.append({
                "idx_a": idx_a,
                "idx_b": idx_b,
                "record_id_a": records[idx_a].get("record_id", str(idx_a)),
                "record_id_b": records[idx_b].get("record_id", str(idx_b)),
                "company_a": records[idx_a].get("company_name", ""),
                "company_b": records[idx_b].get("company_name", ""),
                "total_score": total,
                "field_scores": field_scores,
                "classification": classify_score(total),
            })

    # Sort by score descending
    results.sort(key=lambda x: x["total_score"], reverse=True)
    return results


def build_clusters(duplicates):
    """
    Build clusters from pairwise duplicates using union-find.
    Returns list of clusters, each cluster is a list of record IDs.
    """
    parent = {}

    def find(x):
        if x not in parent:
            parent[x] = x
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path compression
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for dup in duplicates:
        union(dup["record_id_a"], dup["record_id_b"])

    # Group by root
    clusters = {}
    for dup in duplicates:
        for rid in [dup["record_id_a"], dup["record_id_b"]]:
            root = find(rid)
            if root not in clusters:
                clusters[root] = set()
            clusters[root].add(rid)

    # Only return clusters with 2+ records
    return [sorted(list(c)) for c in clusters.values() if len(c) >= 2]
