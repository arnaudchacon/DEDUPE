"""
Copeland-inspired colour scheme and custom CSS for DedupPro.
"""

# Colour palette
PRIMARY = "#0077B6"
SECONDARY = "#023E8A"
ACCENT = "#00B4D8"
BACKGROUND = "#F8F9FA"
CARD_BG = "#FFFFFF"
SUCCESS = "#22C55E"
WARNING = "#F59E0B"
ERROR = "#EF4444"
TEXT = "#1A1A2E"
MUTED = "#6B7280"

# Classification colours
CLASSIFICATION_COLORS = {
    "Definite Duplicate": ERROR,
    "Probable Duplicate": WARNING,
    "Possible Duplicate": "#FBBF24",
    "Not a Duplicate": SUCCESS,
}


def get_custom_css():
    """Return custom CSS for the Streamlit app."""
    return f"""
    <style>
        /* Global styles */
        .stApp {{
            background-color: {BACKGROUND};
        }}

        /* Header */
        .main-header {{
            background: linear-gradient(135deg, {SECONDARY} 0%, {PRIMARY} 50%, {ACCENT} 100%);
            padding: 1.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            color: white;
        }}
        .main-header h1 {{
            color: white;
            font-size: 1.8rem;
            margin: 0;
            font-weight: 700;
        }}
        .main-header p {{
            color: rgba(255,255,255,0.85);
            margin: 0.3rem 0 0 0;
            font-size: 0.95rem;
        }}

        /* Metric cards */
        .metric-card {{
            background: {CARD_BG};
            border-radius: 10px;
            padding: 1.2rem 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            border-left: 4px solid {PRIMARY};
            text-align: center;
        }}
        .metric-card .metric-value {{
            font-size: 2rem;
            font-weight: 700;
            color: {TEXT};
            margin: 0.3rem 0;
        }}
        .metric-card .metric-label {{
            font-size: 0.8rem;
            color: {MUTED};
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }}

        /* Score badges */
        .score-badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.85rem;
        }}
        .score-definite {{
            background-color: #FEE2E2;
            color: #991B1B;
        }}
        .score-probable {{
            background-color: #FEF3C7;
            color: #92400E;
        }}
        .score-possible {{
            background-color: #FEF9C3;
            color: #854D0E;
        }}

        /* Duplicate pair card */
        .pair-card {{
            background: {CARD_BG};
            border-radius: 10px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            border: 1px solid #E5E7EB;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 1.5rem;
            color: {MUTED};
            font-size: 0.85rem;
            border-top: 1px solid #E5E7EB;
            margin-top: 2rem;
        }}
        .footer a {{
            color: {PRIMARY};
            text-decoration: none;
        }}

        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: {CARD_BG};
        }}
        section[data-testid="stSidebar"] .stSlider > div > div > div {{
            color: {PRIMARY};
        }}

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] button {{
            color: {MUTED};
            font-weight: 500;
        }}
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
            color: {PRIMARY};
            border-bottom-color: {PRIMARY};
        }}

        /* Hide Streamlit default elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Cluster card */
        .cluster-card {{
            background: {CARD_BG};
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 0.8rem;
            border: 1px solid #E5E7EB;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }}
        .cluster-header {{
            font-weight: 600;
            color: {SECONDARY};
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }}
    </style>
    """
