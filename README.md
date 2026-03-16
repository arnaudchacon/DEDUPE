# DedupPro — Probabilistic Record Deduplication Tool

An interactive CRM data deduplication tool that uses Levenshtein distance scoring
with configurable field weights to detect and score duplicate records.

## How It Works
1. **Field Matching:** Compares records across company name, email, phone, address,
   contact name, and website using normalized Levenshtein distance
2. **Weighted Scoring:** Each field contributes to an overall duplicate probability
   score (0-100) based on configurable weights
3. **Classification:** Pairs are classified as Definite (90+), Probable (75-89),
   Possible (60-74), or Clean (<60)
4. **Blocking:** Performance optimization that only compares records within the
   same block (first 3 chars of company name, email domain, or city)

## Features
- **Demo mode** with pre-loaded B2B CRM data (200 records, HVAC industry)
- **Upload mode** for your own CSV files
- **Configurable weights** — adjust field importance via sidebar sliders
- **Diff highlighting** — see exactly which characters differ between duplicate pairs
- **Cluster detection** — groups related duplicates together
- **Before/After analysis** — shows dedup impact on data quality
- **Export** — download duplicate pairs report and cleaned dataset

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Why I Built This
At Payplug (French payments fintech), I designed and executed a deduplication
project on a 100,000+ record CRM database using Levenshtein distance scoring
with weighted fields. This tool is a productized version of that methodology,
built to demonstrate the approach interactively.

## Tech Stack
Python, Streamlit, Pandas, rapidfuzz, Plotly

## About Me
Arnaud Chacon — RevOps & Data Operations Analyst
- LinkedIn: [linkedin.com/in/arnaudchacon](https://www.linkedin.com/in/arnaudchacon/)
- Email: arnaudchacon@gmail.com
