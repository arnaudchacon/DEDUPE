"""
Copeland brand colour scheme and custom CSS for DedupPro.
Colours pulled from Copeland's actual website.
"""

# ── Backgrounds ──────────────────────────────────────────────────────
BG_PAGE = "#FFFFFF"
BG_CARDS = "#F5F5F4"
BG_HEADER = "#000E57"
BG_SIDEBAR = "#F5F5F4"

# ── Brand colours ────────────────────────────────────────────────────
PRIMARY = "#0F3CFF"       # Copeland brand blue — main accent
SECONDARY = "#000E57"     # Navy — headers, dark elements
ACCENT_GREEN = "#93C8A1"  # Jade — clean/success
ACCENT_CORAL = "#DE8269"  # Soft adobe — warnings
ACCENT_LILAC = "#CCD1FF"  # Cool lilac — subtle highlights
ACCENT_WARM = "#ABA18B"   # Warm gray — muted elements

# ── Text ─────────────────────────────────────────────────────────────
TEXT_PRIMARY = "#2A2A26"
TEXT_SECONDARY = "#6A6960"
TEXT_REVERSED = "#FFFFFF"
TEXT_LINK = "#3155A4"
TEXT_ERROR = "#D31245"
TEXT_WARNING = "#F8B11E"

# ── Borders / shadows ───────────────────────────────────────────────
BORDER = "#CECDC9"
SHADOW = "#E1E1DE"

# ── Classification colours ───────────────────────────────────────────
CLASSIFICATION_COLORS = {
    "Definite Duplicate": TEXT_ERROR,
    "Probable Duplicate": ACCENT_CORAL,
    "Possible Duplicate": TEXT_WARNING,
    "Clean Records": ACCENT_GREEN,
    "Not a Duplicate": ACCENT_GREEN,
}

# Card top-border colours (one per summary card)
CARD_COLORS = {
    "total_records": PRIMARY,
    "duplicates_found": ACCENT_CORAL,
    "duplicate_rate": TEXT_WARNING,
    "data_quality": ACCENT_GREEN,
}

# ── Plotly chart template ────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor=BG_PAGE,
    plot_bgcolor=BG_PAGE,
    font=dict(
        family="Aileron, Helvetica Neue, Arial, sans-serif",
        color=TEXT_PRIMARY,
        size=13,
    ),
    xaxis=dict(
        gridcolor=SHADOW,
        linecolor=BORDER,
        tickfont=dict(color=TEXT_SECONDARY, size=11),
        title_font=dict(color=TEXT_PRIMARY, size=13),
    ),
    yaxis=dict(
        gridcolor=SHADOW,
        linecolor=BORDER,
        tickfont=dict(color=TEXT_SECONDARY, size=11),
        title_font=dict(color=TEXT_PRIMARY, size=13),
    ),
    margin=dict(l=50, r=30, t=40, b=50),
)


def get_custom_css():
    """Return custom CSS for the Streamlit app."""
    return f"""
    <style>
        /* ── Google Fonts (fallback for Aileron) ────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        /* ── Global ────────────────────────────────────────────────── */
        .stApp {{
            background-color: {BG_PAGE};
            font-family: "Aileron", "Inter", "Helvetica Neue", Helvetica, Arial, sans-serif;
            font-weight: 300;
            color: {TEXT_PRIMARY};
        }}

        /* Force all Streamlit text elements to dark */
        .stApp p, .stApp span, .stApp label,
        .stApp li, .stApp td, .stApp th, .stApp h1, .stApp h2,
        .stApp h3, .stApp h4, .stApp h5, .stApp h6,
        .stApp .stMarkdown, .stApp .stText {{
            color: {TEXT_PRIMARY} !important;
        }}

        /* ── Header banner ─────────────────────────────────────────── */
        .main-header {{
            background-color: {BG_HEADER};
            padding: 1.8rem 2rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
        }}
        .main-header h1 {{
            color: {TEXT_REVERSED} !important;
            font-family: "STIX Two Text", "Times New Roman", serif;
            font-size: 1.8rem;
            font-weight: 400;
            margin: 0;
        }}
        .main-header p {{
            color: {ACCENT_LILAC} !important;
            margin: 0.3rem 0 0 0;
            font-size: 0.95rem;
        }}

        /* ── Summary metric cards ──────────────────────────────────── */
        .metric-card {{
            background: {BG_PAGE};
            border-radius: 10px;
            padding: 1.2rem 1rem;
            box-shadow: 0 1px 4px {SHADOW};
            border-top: 4px solid {PRIMARY};
            border-left: none;
            text-align: center;
        }}
        .metric-card .metric-value {{
            font-size: 2rem;
            font-weight: 700;
            color: {TEXT_PRIMARY} !important;
            margin: 0.3rem 0;
        }}
        .metric-card .metric-label {{
            font-size: 0.8rem;
            color: {TEXT_SECONDARY} !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }}

        /* ── Score badges ──────────────────────────────────────────── */
        .score-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.85rem;
        }}
        .score-definite {{
            background-color: {TEXT_ERROR};
            color: {TEXT_REVERSED} !important;
        }}
        .score-probable {{
            background-color: {ACCENT_CORAL};
            color: {TEXT_REVERSED} !important;
        }}
        .score-possible {{
            background-color: {TEXT_WARNING};
            color: {TEXT_PRIMARY} !important;
        }}

        /* ── Detail card (pair comparison) ─────────────────────────── */
        .detail-card {{
            background: {BG_PAGE};
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px {SHADOW};
            border: 1px solid {BORDER};
        }}
        .detail-card-header {{
            font-size: 1.1rem;
            font-weight: 600;
            color: {SECONDARY} !important;
            margin-bottom: 0.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {ACCENT_LILAC};
        }}

        /* ── Pair card (summary box) ──────────────────────────────── */
        .pair-card {{
            background: {BG_PAGE};
            border-radius: 10px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 4px {SHADOW};
            border: 1px solid {BORDER};
            color: {TEXT_PRIMARY} !important;
        }}
        .pair-card h4, .pair-card li, .pair-card strong {{
            color: {TEXT_PRIMARY} !important;
        }}

        /* ── Cluster card ──────────────────────────────────────────── */
        .cluster-card {{
            background: {BG_PAGE};
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 0.8rem;
            border: 1px solid {BORDER};
            box-shadow: 0 1px 2px {SHADOW};
        }}
        .cluster-header {{
            font-weight: 600;
            color: {SECONDARY} !important;
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }}

        /* ── Footer ────────────────────────────────────────────────── */
        .footer {{
            text-align: center;
            padding: 1.5rem;
            color: {TEXT_SECONDARY} !important;
            font-size: 0.85rem;
            border-top: 1px solid {BORDER};
            margin-top: 2rem;
        }}
        .footer a {{
            color: {TEXT_LINK} !important;
            text-decoration: none;
        }}
        .footer strong {{
            color: {TEXT_PRIMARY} !important;
        }}

        /* ── Sidebar ───────────────────────────────────────────────── */
        section[data-testid="stSidebar"] {{
            background-color: {BG_SIDEBAR};
        }}
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {{
            color: {TEXT_PRIMARY} !important;
        }}

        /* ── Slider — brand blue thumb, track, and fill ────────────── */
        .stSlider [data-baseweb="slider"] div[role="slider"] {{
            background-color: {PRIMARY} !important;
            border-color: {PRIMARY} !important;
        }}
        .stSlider [data-baseweb="slider"] div[data-testid="stTickBar"] {{
            background: {ACCENT_LILAC} !important;
        }}
        /* Slider track fill (the coloured part) */
        .stSlider > div > div > div > div {{
            background-color: {PRIMARY} !important;
        }}
        .stSlider > div > div > div > div > div {{
            background-color: {PRIMARY} !important;
        }}
        [data-testid="stSlider"] [role="slider"] {{
            background-color: {PRIMARY} !important;
        }}
        /* Slider track background (unfilled part) */
        [data-testid="stSlider"] [data-testid="stTickBar"] > div {{
            background: {ACCENT_LILAC} !important;
        }}

        /* ── Button — brand blue, white text ───────────────────────── */
        .stButton > button {{
            background-color: {PRIMARY} !important;
            color: {TEXT_REVERSED} !important;
            border: none !important;
            border-radius: 8px;
        }}
        .stButton > button:hover {{
            background-color: {SECONDARY} !important;
            color: {TEXT_REVERSED} !important;
        }}
        .stButton > button[kind="primary"],
        .stButton > button[data-testid="stBaseButton-primary"] {{
            background-color: {PRIMARY} !important;
            border-color: {PRIMARY} !important;
            color: {TEXT_REVERSED} !important;
        }}

        /* ── Selectbox / Dropdown ──────────────────────────────────── */
        div[data-baseweb="select"] {{
            background-color: {BG_PAGE} !important;
        }}
        div[data-baseweb="select"] span {{
            color: {TEXT_PRIMARY} !important;
        }}
        div[data-baseweb="select"] > div {{
            background-color: {BG_PAGE} !important;
            border-color: {BORDER} !important;
        }}
        /* Dropdown menu items */
        [data-baseweb="menu"] li {{
            color: {TEXT_PRIMARY} !important;
            background-color: {BG_PAGE} !important;
        }}
        [data-baseweb="menu"] li:hover {{
            background-color: {BG_CARDS} !important;
        }}

        /* ── Toggle styling ────────────────────────────────────────── */
        .stToggle label span {{
            color: {TEXT_PRIMARY} !important;
        }}

        /* ── Tab styling ───────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] button {{
            color: {TEXT_SECONDARY} !important;
            font-weight: 500;
        }}
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
            color: {PRIMARY} !important;
            border-bottom-color: {PRIMARY} !important;
        }}

        /* ── Expander styling ──────────────────────────────────────── */
        .streamlit-expanderHeader {{
            background-color: {BG_CARDS} !important;
            color: {TEXT_PRIMARY} !important;
            font-size: 0.95rem;
        }}
        .streamlit-expanderHeader p, .streamlit-expanderHeader span {{
            color: {TEXT_PRIMARY} !important;
        }}
        details > summary {{
            color: {TEXT_PRIMARY} !important;
        }}
        details > summary > span {{
            color: {TEXT_PRIMARY} !important;
        }}
        /* Expander content — white background, dark text */
        .streamlit-expanderContent {{
            background-color: {BG_PAGE} !important;
            color: {TEXT_PRIMARY} !important;
        }}
        .streamlit-expanderContent p,
        .streamlit-expanderContent span,
        .streamlit-expanderContent div,
        .streamlit-expanderContent label {{
            color: {TEXT_PRIMARY} !important;
        }}
        /* Also target the newer Streamlit expander structure */
        [data-testid="stExpander"] details[open] > div {{
            background-color: {BG_PAGE} !important;
        }}
        [data-testid="stExpander"] div[data-testid="stExpanderDetails"] {{
            background-color: {BG_PAGE} !important;
        }}

        /* ── Dataframe / table text ────────────────────────────────── */
        .stDataFrame td, .stDataFrame th {{
            color: {TEXT_PRIMARY} !important;
        }}

        /* ── Spacing ───────────────────────────────────────────────── */
        .block-container {{
            padding-top: 1rem;
        }}

        /* ── Hide Streamlit default elements ───────────────────────── */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
    """
