"""
Blocking strategy to avoid N² comparisons.
Groups records into blocks and only compares within blocks.
"""

import pandas as pd
from utils import normalize_string, normalize_email_domain


def generate_blocks(df, use_company_prefix=True, use_email_domain=True, use_city=True):
    """
    Generate candidate pairs using blocking.

    Blocking keys:
    - First 3 characters of normalized company name
    - Email domain
    - City (normalized)

    Records sharing any block key are candidate pairs.

    Returns:
        Set of (idx_a, idx_b) tuples where idx_a < idx_b
    """
    blocks = {}  # block_key -> set of row indices

    for idx, row in df.iterrows():
        keys = set()

        if use_company_prefix:
            company = normalize_string(row.get("company_name", ""))
            if len(company) >= 3:
                keys.add(("company", company[:3]))
            elif len(company) >= 1:
                keys.add(("company", company))

        if use_email_domain:
            domain = normalize_email_domain(row.get("email", ""))
            if domain:
                keys.add(("email", domain))

        if use_city:
            city = normalize_string(row.get("city", ""))
            if city:
                keys.add(("city", city))

        for key in keys:
            if key not in blocks:
                blocks[key] = set()
            blocks[key].add(idx)

    # Build candidate pairs from blocks
    candidate_pairs = set()
    for block_members in blocks.values():
        members = sorted(block_members)
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                candidate_pairs.add((members[i], members[j]))

    return candidate_pairs


def get_blocking_stats(df, candidate_pairs):
    """Return stats about the blocking efficiency."""
    n = len(df)
    total_pairs = n * (n - 1) // 2
    blocked_pairs = len(candidate_pairs)
    reduction = (1 - blocked_pairs / total_pairs) * 100 if total_pairs > 0 else 0

    return {
        "total_records": n,
        "total_possible_pairs": total_pairs,
        "candidate_pairs": blocked_pairs,
        "reduction_percent": round(reduction, 1),
    }
