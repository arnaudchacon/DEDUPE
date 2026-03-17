"""
Copeland brand colour scheme and custom CSS for DedupPro.
Colours pulled from Copeland's actual website.
LIGHT THEME ONLY. No black backgrounds anywhere.
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
    """Return custom CSS for the Streamlit app — LIGHT THEME ONLY."""
    return """
    <style>
        /* ══════════════════════════════════════════════════════════════
           GLOBAL LIGHT THEME OVERRIDE — NO BLACK BACKGROUNDS ANYWHERE
           ══════════════════════════════════════════════════════════════ */
        [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF !important;
        }
        [data-testid="stHeader"] {
            background-color: #FFFFFF !important;
        }
        .main .block-container {
            background-color: #FFFFFF !important;
        }
        .stApp {
            background-color: #FFFFFF !important;
            color: #2A2A26 !important;
        }

        /* Force ALL text to dark on main content */
        .main p, .main span, .main label, .main div,
        .main li, .main td, .main th,
        .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
            color: #2A2A26 !important;
        }

        /* ── HEADER BANNER — white text on navy ─────────────────────── */
        .header-banner {
            background-color: #000E57 !important;
            padding: 2rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        }
        .header-banner h1,
        .header-banner h2,
        .header-banner p,
        .header-banner span,
        .header-banner div {
            color: #FFFFFF !important;
        }
        .header-banner .header-subtitle {
            color: #CCD1FF !important;
        }

        /* ── SUMMARY METRIC CARDS ───────────────────────────────────── */
        .metric-card {
            background: #FFFFFF !important;
            border-radius: 10px;
            padding: 1.2rem 1rem;
            box-shadow: 0 1px 4px #E1E1DE;
            border-top: 4px solid #0F3CFF;
            text-align: center;
        }
        .metric-card .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #2A2A26 !important;
            margin: 0.3rem 0;
        }
        .metric-card .metric-label {
            font-size: 0.8rem;
            color: #6A6960 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }

        /* ── SCORE BADGES ───────────────────────────────────────────── */
        .score-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.85rem;
        }
        .score-definite {
            background-color: #D31245;
            color: #FFFFFF !important;
        }
        .score-probable {
            background-color: #DE8269;
            color: #FFFFFF !important;
        }
        .score-possible {
            background-color: #F8B11E;
            color: #2A2A26 !important;
        }

        /* ── DETAIL CARD (pair comparison) ──────────────────────────── */
        .detail-card {
            background: #FFFFFF !important;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px #E1E1DE;
            border: 1px solid #CECDC9;
        }
        .detail-card * {
            color: #2A2A26 !important;
        }
        .detail-card .detail-card-header {
            font-size: 1.1rem;
            font-weight: 600;
            color: #000E57 !important;
            margin-bottom: 0.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #CCD1FF;
        }
        .detail-card .score-badge {
            color: #FFFFFF !important;
        }
        .detail-card .score-possible {
            color: #2A2A26 !important;
        }

        /* ── PAIR CARD (summary box) ────────────────────────────────── */
        .pair-card {
            background: #FFFFFF !important;
            border-radius: 10px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 4px #E1E1DE;
            border: 1px solid #CECDC9;
        }
        .pair-card * {
            color: #2A2A26 !important;
        }

        /* ── CLUSTER HEADER ─────────────────────────────────────────── */
        .cluster-header {
            font-weight: 600;
            color: #000E57 !important;
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }

        /* ── FOOTER ─────────────────────────────────────────────────── */
        .footer {
            text-align: center;
            padding: 1.5rem;
            color: #6A6960 !important;
            font-size: 0.85rem;
            border-top: 1px solid #CECDC9;
            margin-top: 2rem;
        }
        .footer * {
            color: #6A6960 !important;
        }
        .footer a {
            color: #3155A4 !important;
            text-decoration: none;
        }
        .footer strong {
            color: #2A2A26 !important;
        }

        /* ══════════════════════════════════════════════════════════════
           SIDEBAR — light grey background, dark text, blue controls
           ══════════════════════════════════════════════════════════════ */
        [data-testid="stSidebar"] {
            background-color: #F5F5F4 !important;
        }
        [data-testid="stSidebar"] * {
            color: #2A2A26 !important;
        }

        /* ── SLIDER — ALL BLUE ──────────────────────────────────────── */
        [data-testid="stSlider"] > div > div > div {
            background: #0F3CFF !important;
        }
        [data-testid="stSlider"] [role="slider"] {
            background-color: #0F3CFF !important;
            border-color: #0F3CFF !important;
        }
        .stSlider div[data-baseweb="slider"] div[role="progressbar"] {
            background-color: #0F3CFF !important;
        }
        .stSlider [data-baseweb="slider"] div[data-testid="stTickBar"] {
            background: #CCD1FF !important;
        }
        /* Slider filled track */
        .stSlider > div > div > div > div {
            background-color: #0F3CFF !important;
        }
        .stSlider > div > div > div > div > div {
            background-color: #0F3CFF !important;
        }

        /* ── TOGGLE — BLUE WHEN ACTIVE ──────────────────────────────── */
        [data-testid="stToggle"] span[data-checked="true"] {
            background-color: #0F3CFF !important;
        }
        /* Broader toggle selectors */
        .stToggle [data-baseweb="toggle"] input:checked + div {
            background-color: #0F3CFF !important;
        }
        .stToggle div[role="checkbox"][aria-checked="true"] {
            background-color: #0F3CFF !important;
        }

        /* ── BUTTONS — WHITE TEXT ON BLUE ───────────────────────────── */
        .stButton > button {
            background-color: #0F3CFF !important;
            color: #FFFFFF !important;
            border: none !important;
            font-weight: 600 !important;
            border-radius: 8px;
        }
        .stButton > button:hover {
            background-color: #000E57 !important;
            color: #FFFFFF !important;
        }
        .stButton > button:active {
            background-color: #000E57 !important;
            color: #FFFFFF !important;
        }
        /* Sidebar button specifically */
        [data-testid="stSidebar"] .stButton > button {
            background-color: #0F3CFF !important;
            color: #FFFFFF !important;
        }

        /* ── DOWNLOAD BUTTONS — white bg, blue text, blue border ──── */
        .stDownloadButton > button {
            background-color: #FFFFFF !important;
            color: #0F3CFF !important;
            border: 1px solid #0F3CFF !important;
            font-weight: 600 !important;
            border-radius: 8px;
        }
        .stDownloadButton > button:hover {
            background-color: #F5F5F4 !important;
            color: #0F3CFF !important;
        }

        /* ── SELECTBOX / DROPDOWN — white bg, dark text ─────────────── */
        div[data-baseweb="select"] {
            background-color: #FFFFFF !important;
        }
        div[data-baseweb="select"] span {
            color: #2A2A26 !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            border-color: #CECDC9 !important;
        }
        [data-baseweb="menu"] {
            background-color: #FFFFFF !important;
        }
        [data-baseweb="menu"] li {
            color: #2A2A26 !important;
            background-color: #FFFFFF !important;
        }
        [data-baseweb="menu"] li:hover {
            background-color: #F5F5F4 !important;
        }

        /* ── DATAFRAME / TABLE — force light ────────────────────────── */
        [data-testid="stDataFrame"] {
            background-color: #FFFFFF !important;
        }
        [data-testid="stDataFrame"] * {
            color: #2A2A26 !important;
        }
        [data-testid="stDataFrame"] thead tr {
            background-color: #F5F5F4 !important;
        }
        .stDataFrame, .stDataFrame td, .stDataFrame th {
            color: #2A2A26 !important;
            background-color: #FFFFFF !important;
        }

        /* ── TABS — dark text, blue active ──────────────────────────── */
        .stTabs [data-baseweb="tab-list"] button {
            color: #6A6960 !important;
            font-weight: 500;
        }
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            color: #0F3CFF !important;
            border-bottom-color: #0F3CFF !important;
        }

        /* ── EXPANDER — light bg, dark text ─────────────────────────── */
        .streamlit-expanderHeader {
            background-color: #F5F5F4 !important;
            color: #2A2A26 !important;
        }
        .streamlit-expanderContent {
            background-color: #FFFFFF !important;
            color: #2A2A26 !important;
        }
        [data-testid="stExpander"] * {
            color: #2A2A26 !important;
        }
        [data-testid="stExpander"] details[open] > div {
            background-color: #FFFFFF !important;
        }
        [data-testid="stExpanderDetails"] {
            background-color: #FFFFFF !important;
        }

        /* ── METRIC WIDGET (blocking stats) ─────────────────────────── */
        [data-testid="stMetric"] {
            background-color: #FFFFFF !important;
        }
        [data-testid="stMetric"] * {
            color: #2A2A26 !important;
        }

        /* ── TEXT INPUT / FILE UPLOADER ──────────────────────────────── */
        [data-testid="stFileUploader"] {
            background-color: #FFFFFF !important;
        }

        /* ── SPACING ────────────────────────────────────────────────── */
        .block-container {
            padding-top: 1rem;
        }

        /* ── HIDE STREAMLIT DEFAULT ELEMENTS ────────────────────────── */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """
