# DedupPro Build Plan

## Phase 1: Core Libraries
- [x] `sample_data.py` — Generate 200 HVAC CRM records with intentional duplicates (15 definite, 10 probable, 8 possible)
- [x] `utils.py` — String/phone/email normalization, formatting helpers
- [x] `matching_engine.py` — Levenshtein similarity with weighted scoring using rapidfuzz
- [x] `blocking.py` — Blocking strategy (company prefix, email domain, city)
- [x] Verify: run matching engine on sample data, confirm duplicate counts are reasonable

## Phase 2: UI Layer
- [x] `styles.py` — Copeland colour scheme, custom CSS
- [x] `app.py` — Main Streamlit app with:
  - [x] Demo mode loads on first visit with full analysis
  - [x] Sidebar: mode toggle, field weight sliders, threshold, blocking toggle, run button
  - [x] Summary cards (total records, dupes found, dupe rate, data quality score)
  - [x] Score distribution (histogram + donut chart)
  - [x] Duplicate Pairs tab with diff highlighting
  - [x] Cluster View tab (union-find grouping)
  - [x] Field Analysis tab (bar chart + table)
  - [x] Before/After tab
  - [x] Export tab (CSV downloads)
  - [x] Upload mode with column mapping
  - [x] Footer with attribution

## Phase 3: Data & Config
- [x] Generate `data/sample_crm.csv` from sample_data.py (200 records, 15 columns)
- [x] `requirements.txt`
- [x] `README.md`

## Phase 4: Pre-Deployment Checklist
- [x] App loads without errors in demo mode (HTTP 200, health OK)
- [x] All charts render correctly (Plotly histogram, donut, bar, gauge)
- [x] All tabs functional (Pairs, Clusters, Field Analysis, Before/After, Export)
- [x] Sample data loads on first visit
- [x] Upload mode works (with template download)
- [x] Export buttons work (3 download options)
- [x] No tracebacks visible (full integration test passed)
- [x] Currency formatting correct ($50,000,000)
- [x] Percentages display correctly (83.5%)
- [x] Custom CSS applied (Copeland colours, not default Streamlit blue)
- [x] Footer visible with LinkedIn + email
- [x] No hardcoded file paths

## Review

**Build completed successfully.**

- 200 CRM records generated with realistic HVAC industry data
- Matching engine detects 35 duplicate pairs: 14 definite, 9 probable, 12 possible
- 25 duplicate clusters identified via union-find
- Blocking reduces comparison space from 19,900 to 1,559 candidate pairs (92.2% reduction)
- All modules import cleanly and pass integration test
- Streamlit app starts cleanly and responds on port 8501
