"""
Helper functions for string normalization, phone normalization,
email domain extraction, and formatting.
"""

import re
import pandas as pd


# Corporate suffixes to strip during normalization
CORPORATE_SUFFIXES = [
    " ltd", " ltd.", " limited", " inc", " inc.", " corp", " corp.",
    " corporation", " co.", " company", " plc", " pte", " gmbh",
    " s.a.", " s.a", " ag", " llc", " pte ltd", " pte. ltd.",
    " co ltd", " co. ltd", " co. ltd.",
]


def normalize_string(s):
    """Lowercase, strip whitespace, remove common corporate suffixes."""
    if pd.isna(s) or s == "":
        return ""
    s = str(s).lower().strip()
    for suffix in CORPORATE_SUFFIXES:
        if s.endswith(suffix):
            s = s[:-len(suffix)].strip()
    return s


def normalize_phone(phone):
    """Strip everything except digits."""
    if pd.isna(phone) or str(phone).strip() == "":
        return ""
    return re.sub(r'[^0-9]', '', str(phone))


def normalize_email_domain(email):
    """Extract domain from email address."""
    if pd.isna(email) or "@" not in str(email):
        return ""
    return str(email).lower().split("@")[1].strip()


def normalize_website(url):
    """Strip protocol, www, and trailing slashes from URLs."""
    if pd.isna(url) or str(url).strip() == "":
        return ""
    s = str(url).lower().strip()
    for prefix in ["https://", "http://", "www."]:
        if s.startswith(prefix):
            s = s[len(prefix):]
    return s.rstrip("/")


def format_currency(value):
    """Format number as currency string with $ and commas."""
    if pd.isna(value) or value is None:
        return "N/A"
    return f"${value:,.0f}"


def format_percentage(value):
    """Format decimal or whole number as percentage string."""
    if pd.isna(value) or value is None:
        return "N/A"
    return f"{value:.1f}%"


def classify_score(score):
    """Classify a duplicate score into a category."""
    if score >= 90:
        return "Definite Duplicate"
    elif score >= 75:
        return "Probable Duplicate"
    elif score >= 60:
        return "Possible Duplicate"
    else:
        return "Not a Duplicate"


def score_color(score):
    """Return hex color for a given similarity score (higher = greener)."""
    if score >= 80:
        return "#93C8A1"  # jade green — high similarity
    elif score >= 60:
        return "#F8B11E"  # amber — medium similarity
    else:
        return "#D31245"  # red — low similarity


def generate_diff_html(text_a, text_b):
    """
    Generate HTML showing character-level differences between two strings.
    Characters that differ are highlighted in red.
    """
    import difflib

    if not text_a and not text_b:
        return "", ""

    text_a = str(text_a) if text_a else ""
    text_b = str(text_b) if text_b else ""

    matcher = difflib.SequenceMatcher(None, text_a, text_b)
    html_a = []
    html_b = []

    for op, a_start, a_end, b_start, b_end in matcher.get_opcodes():
        if op == "equal":
            html_a.append(text_a[a_start:a_end])
            html_b.append(text_b[b_start:b_end])
        elif op == "replace":
            html_a.append(f'<span style="background-color:#FDECED;color:#D31245;font-weight:bold;padding:1px 2px;border-radius:2px">{text_a[a_start:a_end]}</span>')
            html_b.append(f'<span style="background-color:#FDECED;color:#D31245;font-weight:bold;padding:1px 2px;border-radius:2px">{text_b[b_start:b_end]}</span>')
        elif op == "delete":
            html_a.append(f'<span style="background-color:#FDECED;color:#D31245;font-weight:bold;padding:1px 2px;border-radius:2px">{text_a[a_start:a_end]}</span>')
        elif op == "insert":
            html_b.append(f'<span style="background-color:#FDECED;color:#D31245;font-weight:bold;padding:1px 2px;border-radius:2px">{text_b[b_start:b_end]}</span>')

    return "".join(html_a), "".join(html_b)
