# CLAUDE.md — DedupPro: Probabilistic Record Deduplication Tool

---

## WORKFLOW ORCHESTRATION (READ THIS FIRST)

### 1. Plan Node Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately — don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Task Management
1. **Plan First**: Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

### 3. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness
- **TEST THE APP LOCALLY BEFORE SAYING IT'S DONE**

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes — don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user
- Go fix failing tests without being told how

### 7. Core Principles
- **Simplicity First**: Make every change as simple as possible. Minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.

---

## PRE-DEPLOYMENT CHECKLIST

Before telling the user the app is done, verify ALL of these:

```
[ ] App loads without errors in demo mode
[ ] All charts render correctly (no blank spaces, no JS errors)
[ ] All tabs/sections are functional and navigable
[ ] Sample data loads on first visit — no upload required
[ ] Upload mode works with a test CSV
[ ] Export/download button works
[ ] No Python tracebacks visible anywhere in the UI
[ ] No raw code or error messages displayed to the user
[ ] Currency formatting is correct (commas, decimal places)
[ ] Percentages display correctly (not 0.78 but 78%)
[ ] All colours render as specified (not default Streamlit blue)
[ ] Custom CSS is applied and visible
[ ] App loads in under 5 seconds
[ ] Mobile-responsive (doesn't break on smaller screens)
[ ] Footer with attribution is visible
[ ] README.md is complete and accurate
[ ] requirements.txt includes all dependencies
[ ] No hardcoded file paths that only work locally
```

**If ANY of these fail, fix them before declaring done.**

---

## CONTEXT

This project is a **portfolio piece** being built by Arnaud Chacon as part of a job application for the **Senior RevOps Analyst** role at **Copeland** (global climate technologies company, formerly Emerson Climate Technologies). The role involves CRM data governance, deduplication, systems integration, and establishing a single source of truth.

Arnaud's key differentiator: at Payplug (French payments fintech), he personally designed and executed a deduplication project on a 100,000+ record CRM database using **Levenshtein distance scoring** with weighted fields to calculate duplicate probability. This tool demonstrates that capability in an interactive, deployable format.

Arnaud's background:
- Payplug (BPCE Group): Sales/RevOps — CRM management (HubSpot/Salesforce), deduplication using Levenshtein distance, dashboards, pipeline analysis, automation (Python, VBA, Apps Script, Zapier)
- NATO: Finance operations in SAP/Oracle — 80-120 transactions/day, data integrity, compliance
- Audit: Financial data review, internal controls, documentation verification for 15+ clients
- Skills: Python, Excel (VBA), SQL, Google Apps Script, Zapier, Streamlit

---

## WHAT TO BUILD

A **Streamlit web app** called **"DedupPro"** — an interactive Probabilistic Record Deduplication Tool that lets users upload a CSV, automatically detect and score duplicate records using Levenshtein distance and weighted field matching, and review/resolve duplicates through an intuitive interface.

---

## CORE FUNCTIONALITY

### 1. Demo Mode (default on load — THIS IS THE MOST IMPORTANT THING)
- Pre-loaded with realistic sample CRM/sales data (see data spec below)
- User sees the full deduplication analysis immediately without uploading anything
- The hiring manager will click the link, spend 30 seconds, and decide. Make those 30 seconds count.
- Show: total records, duplicates found, duplicate rate, confidence distribution, and a preview of detected pairs

### 2. Upload Mode
- User uploads a CSV file
- App auto-detects columns and suggests which fields to use for matching
- User can adjust field weights before running
- Clear instructions and a downloadable template CSV

### 3. Matching Engine (THE BRAIN — this is what makes the tool special)

#### How it works:

**Step 1: Field Selection & Weighting**
User (or demo default) selects which fields to compare and assigns weights:

| Field | Default Weight | Why |
|-------|---------------|-----|
| Company Name | 30% | Primary identifier, most important |
| Email Domain | 20% | Strong signal — same domain = likely same company |
| Phone | 15% | Good signal but formatting varies |
| Address / City | 15% | Helps confirm but can have typos |
| Contact Name | 10% | People change roles, less reliable |
| Website | 10% | Strong signal when available |

**Step 2: Pairwise Comparison**
For every pair of records, calculate a similarity score per field:

- **String fields (Company Name, Contact Name, Address):** Use **Levenshtein distance** normalized to a 0-100 similarity score
  - Formula: `similarity = (1 - (levenshtein_distance / max(len(a), len(b)))) * 100`
  - Example: "Emerson Electric Co" vs "Emerson Electric Company" → very high score
  - Example: "Copeland Corp" vs "Copeland Corporation HK" → high score
  - Example: "Copeland Corp" vs "Daikin Industries" → very low score

- **Email domain:** Extract domain, compare with exact match (100) or Levenshtein (partial)
  - "john@copeland.com" vs "jane@copeland.com" → domain match = 100
  - "info@copeland.com" vs "info@copeland-hk.com" → partial match via Levenshtein

- **Phone:** Normalize (strip spaces, dashes, country codes), then exact or partial match

- **Website:** Normalize (strip www, http, trailing slashes), then exact or Levenshtein

**Step 3: Weighted Score Calculation**
```
total_score = sum(field_similarity * field_weight) for each field
```
Result: a score from 0-100 for each pair

**Step 4: Classification**
| Score | Classification | Action |
|-------|---------------|--------|
| 90-100 | Definite Duplicate | Auto-flag for merge |
| 75-89 | Probable Duplicate | Flag for review |
| 60-74 | Possible Duplicate | Suggest review |
| Below 60 | Not a Duplicate | Ignore |

**Step 5: Blocking (Performance Optimization)**
Don't compare every record to every other record (N² problem). Use blocking:
- Block on first 3 characters of company name
- Block on email domain
- Block on city
- Only compare records within the same block
- This reduces computation dramatically for large datasets

### 4. Dashboard / Results View

#### A. Summary Cards (top of page)
- **Total Records:** count
- **Duplicates Found:** count of pairs scoring 60+
- **Duplicate Rate:** % of database affected
- **Data Quality Score:** 100 minus duplicate rate (higher = cleaner)

#### B. Score Distribution
- **Histogram:** distribution of all pairwise scores (shows the bell curve of matches)
- **Donut chart:** breakdown by classification (Definite / Probable / Possible / Clean)

#### C. Duplicate Pairs Table (the main event)
Interactive table showing:
- Record A (company name, email, phone, etc.)
- Record B (company name, email, phone, etc.)
- Overall Score (with colour coding: red 90+, orange 75-89, yellow 60-74)
- Per-field scores (expandable)
- Action buttons: "Merge" / "Not a Duplicate" / "Review Later"

**Highlight the differences:** When showing a pair, visually highlight the characters that differ between the two records. This is the "aha moment" — the user sees exactly why two records were flagged and where the discrepancy is.

#### D. Field Analysis
- **Bar chart:** which fields have the most mismatches (shows where data quality is worst)
- **Table:** field-by-field analysis — avg similarity score, most common issues

#### E. Cluster View
- Some duplicates come in clusters (3+ records that are all the same entity)
- Show clusters with all related records grouped together
- This is important for CRM cleanup — you don't just merge pairs, you merge clusters

#### F. Before/After Summary
- Show what the database would look like after deduplication
- Record count reduction
- Estimated data quality improvement

### 5. Configuration Panel (sidebar)
- Adjust field weights with sliders
- Set minimum score threshold
- Choose which fields to include
- Toggle blocking on/off
- Re-run analysis with new settings

### 6. Export
- Download duplicate pairs report as CSV
- Download recommended merge list
- Download cleaned dataset (with duplicates flagged)

---

## SAMPLE DATA SPECIFICATION

### File: sample_crm_data.csv

Generate **200 records** simulating a B2B HVAC/climate technology company's CRM (matching Copeland's industry).

**Columns:**
- `record_id` — e.g., "CRM-0001"
- `company_name` — the main matching field
- `contact_name` — first + last name
- `email` — business email
- `phone` — with country codes
- `address` — street address
- `city` — city
- `country` — country
- `website` — company website
- `industry` — HVAC, Manufacturing, Construction, etc.
- `account_owner` — sales rep name
- `created_date` — when the record was created
- `last_activity` — last interaction date
- `revenue` — annual revenue estimate
- `status` — Active, Inactive, Prospect

### Duplicate Scenarios (build these intentionally into the data):

**1. Obvious duplicates (score 90+) — ~15 pairs:**
- Exact same company, slightly different contact: "Daikin Industries Ltd" / "Daikin Industries Ltd" with different contact names
- Typo in company name: "Carrier Global Corporation" / "Carrier Global Corpration"
- Different formatting: "Johnson Controls Int'l" / "Johnson Controls International"
- Same email domain, same phone, different address format

**2. Probable duplicates (score 75-89) — ~10 pairs:**
- Abbreviations: "Trane Technologies PLC" / "Trane Tech"
- Regional variants: "Mitsubishi Electric Asia" / "Mitsubishi Electric (HK)"
- Different office same company: "Honeywell Building Solutions" / "Honeywell Hong Kong Ltd"
- Merged/acquired: "Emerson Climate Technologies" / "Copeland (formerly Emerson)"

**3. Possible duplicates (score 60-74) — ~8 pairs:**
- Similar names different companies: "Asia Air Conditioning" / "Asia AC Solutions"
- Parent/subsidiary: "Danfoss Group" / "Danfoss Hong Kong"
- Different entity same brand: "LG Electronics HVAC" / "LG Air Solution"

**4. Clean records (score below 60) — ~167 records:**
- Completely distinct companies with no confusion

### Use realistic HVAC/climate industry companies:
- Daikin, Carrier, Trane, Johnson Controls, Honeywell, Mitsubishi Electric, LG, Samsung HVAC, Panasonic, Fujitsu General, Hitachi, Midea, Gree, Haier, York, Lennox, Rheem, Bosch Thermotechnology
- Regional distributors: "Pacific HVAC Solutions", "Asia Cold Chain Logistics", "Greater Bay Area Cooling Systems", "Dragon Air Engineering HK"
- End customers: "Swire Properties", "Sun Hung Kai Properties", "Cathay Pacific Services", "MTR Corporation", "Hospital Authority HK", "HK International Airport"

### Make the data messy in realistic ways:
- Phone formatting inconsistencies: "+852 2123 4567" vs "852-21234567" vs "(852) 2123-4567"
- Address variations: "Unit 1201, 12/F, Tower 2, Times Square" vs "12F Tower Two Times Square"
- Email domains: some use company domain, some use gmail/yahoo
- Missing fields: ~10% of records have blank phone, ~5% have blank email
- Date formatting: mix of "2025-01-15" and "15/01/2025" and "Jan 15, 2025"
- Case inconsistencies: "DAIKIN INDUSTRIES" vs "Daikin Industries" vs "daikin industries"

---

## UI / DESIGN

### Colour Scheme (Copeland-inspired — clean, professional, sustainability-focused):
- Primary: `#0077B6` (Copeland blue)
- Secondary: `#023E8A` (dark blue)
- Accent: `#00B4D8` (lighter blue)
- Background: `#F8F9FA` (light grey)
- Cards: `#FFFFFF` with subtle shadow
- Success/Clean: `#22C55E` (green — sustainability nod)
- Warning/Review: `#F59E0B` (amber)
- Error/Definite Duplicate: `#EF4444` (red)
- Text: `#1A1A2E`
- Muted: `#6B7280`

### Layout:
```
┌──────────────────────────────────────────────────┐
│  🔍 DedupPro — Probabilistic Record Deduplication│
│  Built by Arnaud Chacon                           │
├──────────────────────────────────────────────────┤
│                                                  │
│  SIDEBAR:                    MAIN AREA:          │
│  ┌──────────────┐           ┌──────────────────┐ │
│  │ Mode:        │           │ Summary Cards    │ │
│  │ [Demo][Upload]│          │ [Records][Dupes] │ │
│  │              │           │ [Rate][Quality]  │ │
│  │ Field Weights│           ├──────────────────┤ │
│  │ Company: ████│           │                  │ │
│  │ Email:   ███ │           │ Score Distrib.   │ │
│  │ Phone:   ██  │           │ (histogram +     │ │
│  │ Address: ██  │           │  donut chart)    │ │
│  │ Contact: █   │           │                  │ │
│  │ Website: █   │           ├──────────────────┤ │
│  │              │           │                  │ │
│  │ Threshold:   │           │ TABS:            │ │
│  │ [====60====] │           │ [Duplicate Pairs]│ │
│  │              │           │ [Clusters]       │ │
│  │ [Run Analysis]│          │ [Field Analysis] │ │
│  │              │           │ [Before/After]   │ │
│  │ [Export ▼]   │           │ [Export]         │ │
│  └──────────────┘           └──────────────────┘ │
│                                                  │
│  Footer: Built by Arnaud Chacon | LinkedIn       │
└──────────────────────────────────────────────────┘
```

---

## TECH STACK

- **Streamlit** — main framework
- **Pandas** — data processing
- **python-Levenshtein** or **rapidfuzz** — Levenshtein distance calculation (rapidfuzz is faster)
- **Plotly** — charts
- **NumPy** — calculations

### Dependencies (requirements.txt):
```
streamlit
pandas
plotly
numpy
rapidfuzz
openpyxl
```

**IMPORTANT:** Use `rapidfuzz` not `python-Levenshtein` — it's faster and has better API. If rapidfuzz isn't available, fall back to `thefuzz` or implement Levenshtein manually.

---

## FILE STRUCTURE

```
dedup-pro/
├── app.py                    # Main Streamlit app
├── matching_engine.py        # Levenshtein + weighted scoring logic
├── blocking.py               # Blocking strategy for performance
├── sample_data.py            # Generate realistic sample CRM data
├── styles.py                 # Custom CSS and colour constants
├── utils.py                  # Helper functions (formatting, normalization)
├── requirements.txt          # Dependencies
├── README.md                 # Project description
├── tasks/
│   ├── todo.md               # Build checklist (for your own tracking)
│   └── lessons.md            # Self-improvement log
├── data/
│   └── sample_crm.csv        # Pre-generated sample data
└── CLAUDE.md                 # This file
```

---

## MATCHING ENGINE DETAIL (matching_engine.py)

```python
from rapidfuzz import fuzz, distance

def normalize_string(s):
    """Lowercase, strip whitespace, remove common suffixes"""
    if pd.isna(s) or s == "":
        return ""
    s = str(s).lower().strip()
    # Remove common corporate suffixes
    for suffix in [" ltd", " ltd.", " limited", " inc", " inc.", " corp", " corp.", 
                   " corporation", " co.", " company", " plc", " pte", " gmbh",
                   " s.a.", " s.a", " ag", " llc"]:
        if s.endswith(suffix):
            s = s[:-len(suffix)].strip()
    return s

def normalize_phone(phone):
    """Strip everything except digits"""
    if pd.isna(phone):
        return ""
    return re.sub(r'[^0-9]', '', str(phone))

def normalize_email_domain(email):
    """Extract domain from email"""
    if pd.isna(email) or "@" not in str(email):
        return ""
    return str(email).lower().split("@")[1].strip()

def levenshtein_similarity(a, b):
    """Calculate normalized Levenshtein similarity (0-100)"""
    if not a or not b:
        return 0
    max_len = max(len(a), len(b))
    if max_len == 0:
        return 100
    dist = distance.Levenshtein.distance(a, b)
    return round((1 - dist / max_len) * 100, 1)

def compare_records(record_a, record_b, field_weights):
    """
    Compare two records across all weighted fields.
    Returns total score (0-100) and per-field scores.
    """
    scores = {}
    
    # Company name (Levenshtein on normalized)
    scores['company_name'] = levenshtein_similarity(
        normalize_string(record_a['company_name']),
        normalize_string(record_b['company_name'])
    )
    
    # Email domain (exact or Levenshtein)
    domain_a = normalize_email_domain(record_a.get('email', ''))
    domain_b = normalize_email_domain(record_b.get('email', ''))
    scores['email'] = 100 if domain_a == domain_b and domain_a != "" else levenshtein_similarity(domain_a, domain_b)
    
    # Phone (normalized digit comparison)
    phone_a = normalize_phone(record_a.get('phone', ''))
    phone_b = normalize_phone(record_b.get('phone', ''))
    if phone_a and phone_b:
        # Compare last 8 digits (ignore country code variations)
        scores['phone'] = 100 if phone_a[-8:] == phone_b[-8:] else levenshtein_similarity(phone_a, phone_b)
    else:
        scores['phone'] = 0
    
    # Address (Levenshtein on normalized)
    scores['address'] = levenshtein_similarity(
        normalize_string(record_a.get('address', '') + ' ' + record_a.get('city', '')),
        normalize_string(record_b.get('address', '') + ' ' + record_b.get('city', ''))
    )
    
    # Contact name (Levenshtein)
    scores['contact_name'] = levenshtein_similarity(
        normalize_string(record_a.get('contact_name', '')),
        normalize_string(record_b.get('contact_name', ''))
    )
    
    # Website (normalized comparison)
    web_a = normalize_string(record_a.get('website', '')).replace('www.', '').replace('http://', '').replace('https://', '')
    web_b = normalize_string(record_b.get('website', '')).replace('www.', '').replace('http://', '').replace('https://', '')
    scores['website'] = levenshtein_similarity(web_a, web_b)
    
    # Weighted total
    total = sum(scores[field] * field_weights.get(field, 0) for field in scores)
    total = round(total / sum(field_weights.values()) if sum(field_weights.values()) > 0 else 0, 1)
    
    return total, scores
```

---

## CRITICAL IMPLEMENTATION NOTES

1. **Demo mode must work perfectly on first load.** No errors, no blank screens, no "please upload a file" message. The user opens the link and sees results immediately.

2. **The diff highlighting on duplicate pairs is the wow factor.** When showing "Carrier Global Corporation" vs "Carrier Global Corpration", highlight the missing 'o' in red. Use `difflib` or character-by-character comparison to show exactly what's different. This is what makes a finance person go "oh that's clever."

3. **The weight sliders in the sidebar should update results in real-time** (or with a "Re-run" button). This shows the tool is configurable, not just a static report.

4. **Handle edge cases:**
   - Empty/null fields should not crash the app — score them as 0
   - Records with all blank fields should be flagged separately ("incomplete records")
   - Very short company names (1-2 chars) should be handled carefully with Levenshtein
   - Unicode characters in company names (common in APAC data)

5. **Performance:** 200 records with blocking should process in under 2 seconds. Without blocking, 200 records = ~20,000 pairs which is still fast. Don't over-optimize but don't ignore it either.

6. **The Cluster View is important.** If records A, B, and C are all duplicates of each other, show them as one cluster, not three separate pairs. Use union-find or simple graph traversal to build clusters from pairwise matches.

7. **Currency/number formatting:** Revenue should show with commas and currency symbols. Percentages should show as "78%" not "0.78".

8. **The Before/After tab should be compelling.** Show: "200 records → 167 unique records after dedup. 33 duplicates removed. Data quality improved from 83.5% to 100%." Make it visual with a simple bar chart or counter animation.

9. **Error handling on upload:** If someone uploads a bad CSV, show a friendly message: "We couldn't read your file. Please make sure it's a CSV with column headers. Here's a template you can use." Include a downloadable template.

10. **Footer:** "Built by Arnaud Chacon as a demonstration of probabilistic record matching using Levenshtein distance scoring. This tool was created as part of a portfolio project. | LinkedIn | Email"

---

## README.md

```markdown
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

## Why I Built This
At Payplug (French payments fintech), I designed and executed a deduplication 
project on a 100,000+ record CRM database using Levenshtein distance scoring 
with weighted fields. This tool is a productized version of that methodology, 
built to demonstrate the approach interactively.

## Tech Stack
Python, Streamlit, Pandas, rapidfuzz, Plotly

## About Me
Arnaud Chacon — RevOps & Data Operations Analyst
- LinkedIn: [link]
- Email: arnaudchacon@gmail.com
```

---

## FINAL REMINDER

**Test everything before declaring done.** Run through the pre-deployment checklist at the top of this file. Open the app, click every tab, try uploading a file, try exporting, resize the window, check on mobile. If anything breaks, fix it. The user should not have to debug anything.
