"""
DedupPro — Probabilistic Record Deduplication Tool
Main Streamlit application.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import os

from matching_engine import find_duplicates, build_clusters, DEFAULT_WEIGHTS
from blocking import generate_blocks, get_blocking_stats
from sample_data import generate_sample_data
from styles import (
    get_custom_css, PLOTLY_LAYOUT,
    PRIMARY, SECONDARY, BG_PAGE, BG_CARDS, BG_HEADER,
    ACCENT_GREEN, ACCENT_CORAL, ACCENT_LILAC, ACCENT_WARM,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_REVERSED, TEXT_LINK,
    TEXT_ERROR, TEXT_WARNING, BORDER, SHADOW,
    CLASSIFICATION_COLORS, CARD_COLORS,
)
from utils import (
    format_currency, format_percentage, classify_score, score_color,
    generate_diff_html,
)

# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="DedupPro — Record Deduplication",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)


# ── Helper: Plotly layout with overrides ─────────────────────────────
def plotly_layout(**overrides):
    """Return a copy of the standard Plotly layout with optional overrides."""
    layout = {**PLOTLY_LAYOUT}
    for k, v in overrides.items():
        if k in layout and isinstance(layout[k], dict) and isinstance(v, dict):
            layout[k] = {**layout[k], **v}
        else:
            layout[k] = v
    return layout


# ── Helper: run analysis (cached) ───────────────────────────────────
@st.cache_data(show_spinner=False)
def run_analysis(df_json, weights_tuple, threshold, use_blocking):
    """Run deduplication analysis. Inputs serialised for caching."""
    df = pd.read_json(io.StringIO(df_json), orient="records")
    field_weights = dict(weights_tuple)

    candidate_pairs = None
    blocking_stats = None
    if use_blocking:
        candidate_pairs = generate_blocks(df)
        blocking_stats = get_blocking_stats(df, candidate_pairs)

    duplicates = find_duplicates(
        df, field_weights=field_weights,
        threshold=threshold, candidate_pairs=candidate_pairs,
    )
    clusters = build_clusters(duplicates)
    return duplicates, clusters, blocking_stats


# ── Header ───────────────────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
    <h1>🔍 DedupPro — Probabilistic Record Deduplication</h1>
    <p>Detect and score duplicate CRM records using Levenshtein distance with configurable field weights</p>
</div>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    mode = st.radio("**Data Source**", ["Demo Data", "Upload CSV"], horizontal=True)

    st.markdown("---")
    st.markdown("**Field Weights**")
    w_company = st.slider("Company Name", 0, 50, 30, key="w_company")
    w_email = st.slider("Email Domain", 0, 50, 20, key="w_email")
    w_phone = st.slider("Phone", 0, 50, 15, key="w_phone")
    w_address = st.slider("Address / City", 0, 50, 15, key="w_address")
    w_contact = st.slider("Contact Name", 0, 50, 10, key="w_contact")
    w_website = st.slider("Website", 0, 50, 10, key="w_website")

    field_weights = {
        "company_name": w_company,
        "email": w_email,
        "phone": w_phone,
        "address": w_address,
        "contact_name": w_contact,
        "website": w_website,
    }

    st.markdown("---")
    threshold = st.slider("**Minimum Score Threshold**", 0, 100, 60)
    use_blocking = st.toggle("**Use Blocking (faster)**", value=True)

    st.markdown("---")
    run_btn = st.button("🔄 Run Analysis", use_container_width=True, type="primary")


# ── Load data ────────────────────────────────────────────────────────
df = None

if mode == "Demo Data":
    csv_path = os.path.join(os.path.dirname(__file__), "data", "sample_crm.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = generate_sample_data()
else:
    uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.success(f"Loaded {len(df)} records with {len(df.columns)} columns.")
        except Exception as e:
            st.error(
                "We couldn't read your file. Please make sure it's a CSV with column headers."
            )
            template = pd.DataFrame({
                "record_id": ["CRM-0001"], "company_name": ["Acme Corp"],
                "contact_name": ["John Doe"], "email": ["john@acme.com"],
                "phone": ["+1 555 123 4567"], "address": ["123 Main St"],
                "city": ["New York"], "country": ["USA"],
                "website": ["www.acme.com"], "industry": ["Manufacturing"],
            })
            st.download_button(
                "📥 Download CSV Template",
                template.to_csv(index=False),
                "dedup_template.csv",
                "text/csv",
            )
            df = None
    else:
        st.info("👆 Upload a CSV file to get started, or switch to **Demo Data** in the sidebar.")
        template = pd.DataFrame({
            "record_id": ["CRM-0001"], "company_name": ["Acme Corp"],
            "contact_name": ["John Doe"], "email": ["john@acme.com"],
            "phone": ["+1 555 123 4567"], "address": ["123 Main St"],
            "city": ["New York"], "country": ["USA"],
            "website": ["www.acme.com"], "industry": ["Manufacturing"],
        })
        st.download_button(
            "📥 Download CSV Template",
            template.to_csv(index=False),
            "dedup_template.csv",
            "text/csv",
        )

if df is None:
    st.stop()

# ── Run analysis ─────────────────────────────────────────────────────
weights_tuple = tuple(sorted(field_weights.items()))
df_json = df.to_json(orient="records")

with st.spinner("Analyzing records for duplicates..."):
    duplicates, clusters, blocking_stats = run_analysis(
        df_json, weights_tuple, threshold, use_blocking,
    )

# Compute summary stats
total_records = len(df)
dup_count = len(duplicates)
dup_record_ids = set()
for d in duplicates:
    dup_record_ids.add(d["record_id_a"])
    dup_record_ids.add(d["record_id_b"])
records_affected = len(dup_record_ids)
dup_rate = (records_affected / total_records * 100) if total_records > 0 else 0
quality_score = 100 - dup_rate

# ── Summary Cards ────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card" style="border-top-color:{CARD_COLORS['total_records']}">
        <div class="metric-label">Total Records</div>
        <div class="metric-value">{total_records:,}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card" style="border-top-color:{CARD_COLORS['duplicates_found']}">
        <div class="metric-label">Duplicate Pairs Found</div>
        <div class="metric-value">{dup_count}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card" style="border-top-color:{CARD_COLORS['duplicate_rate']}">
        <div class="metric-label">Duplicate Rate</div>
        <div class="metric-value">{format_percentage(dup_rate)}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card" style="border-top-color:{CARD_COLORS['data_quality']}">
        <div class="metric-label">Data Quality Score</div>
        <div class="metric-value">{format_percentage(quality_score)}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Score Distribution Charts ────────────────────────────────────────
if duplicates:
    col_hist, col_donut = st.columns(2)

    scores = [d["total_score"] for d in duplicates]

    with col_hist:
        fig_hist = px.histogram(
            x=scores, nbins=20,
            labels={"x": "Duplicate Score", "y": "Count"},
            title="Score Distribution",
            color_discrete_sequence=[PRIMARY],
        )
        fig_hist.update_layout(**plotly_layout(
            xaxis=dict(gridcolor=SHADOW, linecolor=BORDER,
                       tickfont=dict(color=TEXT_SECONDARY, size=11),
                       title_font=dict(color=TEXT_PRIMARY, size=13),
                       title="Duplicate Score", showgrid=True),
            yaxis=dict(gridcolor=SHADOW, linecolor=BORDER,
                       tickfont=dict(color=TEXT_SECONDARY, size=11),
                       title_font=dict(color=TEXT_PRIMARY, size=13),
                       title="Number of Pairs", showgrid=True),
            title=dict(text="Score Distribution",
                       font=dict(color=TEXT_PRIMARY, size=16, weight=600)),
        ))
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_donut:
        classifications = [d["classification"] for d in duplicates]
        class_counts = pd.Series(classifications).value_counts()
        clean_count = total_records - records_affected
        all_categories = {
            "Definite Duplicate": class_counts.get("Definite Duplicate", 0),
            "Probable Duplicate": class_counts.get("Probable Duplicate", 0),
            "Possible Duplicate": class_counts.get("Possible Duplicate", 0),
            "Clean Records": clean_count,
        }
        donut_colors = [TEXT_ERROR, ACCENT_CORAL, TEXT_WARNING, ACCENT_GREEN]

        fig_donut = go.Figure(data=[go.Pie(
            labels=list(all_categories.keys()),
            values=list(all_categories.values()),
            hole=0.5,
            marker=dict(colors=donut_colors),
            textinfo="label+value",
            textfont=dict(size=12, color=TEXT_PRIMARY),
        )])
        fig_donut.update_layout(**plotly_layout(
            title=dict(text="Record Classification",
                       font=dict(color=TEXT_PRIMARY, size=16, weight=600)),
            showlegend=False,
        ))
        st.plotly_chart(fig_donut, use_container_width=True)

# ── Blocking stats ───────────────────────────────────────────────────
if blocking_stats and use_blocking:
    with st.expander("📊 Blocking Performance"):
        bc1, bc2, bc3 = st.columns(3)
        bc1.metric("Total Possible Pairs", f"{blocking_stats['total_possible_pairs']:,}")
        bc2.metric("Candidate Pairs (after blocking)", f"{blocking_stats['candidate_pairs']:,}")
        bc3.metric("Reduction", f"{blocking_stats['reduction_percent']}%")


# ── Tabs ─────────────────────────────────────────────────────────────
tab_pairs, tab_clusters, tab_field, tab_before_after, tab_export = st.tabs([
    "🔗 Duplicate Pairs", "🧩 Clusters", "📊 Field Analysis",
    "📈 Before / After", "📥 Export",
])

# ── Tab 1: Duplicate Pairs ───────────────────────────────────────────
with tab_pairs:
    if not duplicates:
        st.info("No duplicate pairs found at the current threshold.")
    else:
        filter_col1, filter_col2 = st.columns([1, 3])
        with filter_col1:
            filter_class = st.selectbox(
                "Filter by classification",
                ["All", "Definite Duplicate", "Probable Duplicate", "Possible Duplicate"],
            )

        filtered = duplicates if filter_class == "All" else [
            d for d in duplicates if d["classification"] == filter_class
        ]

        st.markdown(f"**Showing {len(filtered)} pairs** (sorted by score, highest first)")

        for i, dup in enumerate(filtered[:50]):
            score = dup["total_score"]
            cls = dup["classification"]

            # Badge colour for the score
            if score >= 90:
                badge_bg, badge_text = TEXT_ERROR, TEXT_REVERSED
                badge_class = "score-definite"
            elif score >= 75:
                badge_bg, badge_text = ACCENT_CORAL, TEXT_REVERSED
                badge_class = "score-probable"
            else:
                badge_bg, badge_text = TEXT_WARNING, TEXT_PRIMARY
                badge_class = "score-possible"

            # Expander label includes company names + score preview
            expander_label = f"{dup['company_a']}  ↔  {dup['company_b']}  —  Score: {score}  [{cls}]"

            with st.expander(expander_label, expanded=(i < 3)):
                # Score badge
                st.markdown(
                    f'<span class="score-badge {badge_class}">Score: {score} — {cls}</span>',
                    unsafe_allow_html=True,
                )

                rec_a = df.iloc[dup["idx_a"]]
                rec_b = df.iloc[dup["idx_b"]]

                # Side-by-side comparison with diff highlighting
                fields_to_diff = [
                    ("Company Name", "company_name"),
                    ("Contact Name", "contact_name"),
                    ("Email", "email"),
                    ("Phone", "phone"),
                    ("Address", "address"),
                    ("City", "city"),
                    ("Website", "website"),
                ]

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**Record A** ({dup['record_id_a']})")
                with col_b:
                    st.markdown(f"**Record B** ({dup['record_id_b']})")

                for label, field in fields_to_diff:
                    val_a = str(rec_a.get(field, "")) if pd.notna(rec_a.get(field, "")) else ""
                    val_b = str(rec_b.get(field, "")) if pd.notna(rec_b.get(field, "")) else ""
                    diff_a, diff_b = generate_diff_html(val_a, val_b)

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(
                            f"<small style='color:{TEXT_SECONDARY}'>{label}</small><br>"
                            f"<span style='color:{TEXT_PRIMARY}'>{diff_a}</span>",
                            unsafe_allow_html=True,
                        )
                    with col_b:
                        st.markdown(
                            f"<small style='color:{TEXT_SECONDARY}'>{label}</small><br>"
                            f"<span style='color:{TEXT_PRIMARY}'>{diff_b}</span>",
                            unsafe_allow_html=True,
                        )

                # Per-field scores — horizontal bars with conditional colouring
                st.markdown(f"<p style='color:{TEXT_PRIMARY};font-weight:600;margin-top:0.8rem'>Field Similarity Scores</p>", unsafe_allow_html=True)
                fs = dup["field_scores"]
                field_labels = {
                    "company_name": "Company",
                    "email": "Email",
                    "phone": "Phone",
                    "address": "Address",
                    "contact_name": "Contact",
                    "website": "Website",
                }
                bar_colors = [score_color(fs.get(k, 0)) for k in field_labels]

                fig_fields = go.Figure(data=[go.Bar(
                    x=[fs.get(k, 0) for k in field_labels],
                    y=list(field_labels.values()),
                    orientation="h",
                    marker_color=bar_colors,
                    text=[f"{fs.get(k, 0):.0f}" for k in field_labels],
                    textposition="inside",
                    textfont=dict(color=TEXT_PRIMARY, size=12),
                )])
                fig_fields.update_layout(**plotly_layout(
                    height=200,
                    margin=dict(l=70, r=30, t=10, b=10),
                    xaxis=dict(range=[0, 100], title="Similarity Score",
                               gridcolor=SHADOW, linecolor=BORDER,
                               tickfont=dict(color=TEXT_SECONDARY, size=11),
                               title_font=dict(color=TEXT_PRIMARY, size=12),
                               showgrid=True),
                    yaxis=dict(tickfont=dict(color=TEXT_PRIMARY, size=12),
                               gridcolor=SHADOW, linecolor=BORDER),
                ))
                st.plotly_chart(fig_fields, use_container_width=True)


# ── Tab 2: Clusters ─────────────────────────────────────────────────
with tab_clusters:
    if not clusters:
        st.info("No duplicate clusters found.")
    else:
        st.markdown(f"**{len(clusters)} duplicate clusters** detected (groups of 2+ records that are all the same entity)")

        for i, cluster_ids in enumerate(clusters):
            cluster_df = df[df["record_id"].isin(cluster_ids)].copy()
            size = len(cluster_df)
            companies = cluster_df["company_name"].unique()
            label = companies[0] if len(companies) > 0 else "Unknown"

            st.markdown(
                f'<div class="cluster-header">Cluster {i+1} — {size} records — "{label}"</div>',
                unsafe_allow_html=True,
            )

            display_cols = ["record_id", "company_name", "contact_name", "email", "phone", "city"]
            available_cols = [c for c in display_cols if c in cluster_df.columns]
            st.dataframe(
                cluster_df[available_cols].reset_index(drop=True),
                use_container_width=True,
                hide_index=True,
            )
            st.markdown("---")


# ── Tab 3: Field Analysis ───────────────────────────────────────────
with tab_field:
    if not duplicates:
        st.info("No duplicates to analyze.")
    else:
        st.markdown("### Field-by-Field Analysis")
        st.markdown("Which fields contribute most to duplicate detection?")

        field_names = ["company_name", "email", "phone", "address", "contact_name", "website"]
        field_labels_map = {
            "company_name": "Company Name",
            "email": "Email Domain",
            "phone": "Phone",
            "address": "Address / City",
            "contact_name": "Contact Name",
            "website": "Website",
        }

        avg_scores = {}
        low_scores_count = {}
        for f in field_names:
            vals = [d["field_scores"].get(f, 0) for d in duplicates]
            avg_scores[f] = sum(vals) / len(vals) if vals else 0
            low_scores_count[f] = sum(1 for v in vals if v < 50)

        # Bar chart with conditional colours
        bar_colors_field = [
            ACCENT_GREEN if avg_scores[f] >= 80 else
            TEXT_WARNING if avg_scores[f] >= 60 else
            TEXT_ERROR
            for f in field_names
        ]

        fig_avg = go.Figure(data=[go.Bar(
            x=[avg_scores[f] for f in field_names],
            y=[field_labels_map[f] for f in field_names],
            orientation="h",
            marker_color=bar_colors_field,
            text=[f"{avg_scores[f]:.1f}" for f in field_names],
            textposition="inside",
            textfont=dict(color=TEXT_PRIMARY, size=12),
        )])
        fig_avg.update_layout(**plotly_layout(
            title=dict(text="Average Similarity Score by Field (across duplicate pairs)",
                       font=dict(color=TEXT_PRIMARY, size=14, weight=600)),
            xaxis=dict(range=[0, 100], title="Average Score",
                       gridcolor=SHADOW, linecolor=BORDER, showgrid=True,
                       tickfont=dict(color=TEXT_SECONDARY, size=11),
                       title_font=dict(color=TEXT_PRIMARY, size=13)),
            yaxis=dict(tickfont=dict(color=TEXT_PRIMARY, size=12),
                       gridcolor=SHADOW, linecolor=BORDER),
            height=300,
            margin=dict(l=120, r=30, t=50, b=40),
        ))
        st.plotly_chart(fig_avg, use_container_width=True)

        # Mismatch table
        st.markdown("### Mismatch Summary")
        mismatch_data = []
        for f in field_names:
            mismatch_data.append({
                "Field": field_labels_map[f],
                "Avg Similarity": f"{avg_scores[f]:.1f}",
                "Low Matches (<50)": low_scores_count[f],
                "Weight": f"{field_weights.get(f, 0)}%",
            })
        st.dataframe(pd.DataFrame(mismatch_data), use_container_width=True, hide_index=True)


# ── Tab 4: Before / After ───────────────────────────────────────────
with tab_before_after:
    st.markdown("### Deduplication Impact")

    unique_after = total_records - (records_affected - len(clusters))
    records_removed = total_records - unique_after
    quality_before = quality_score
    quality_after = 100.0

    col_ba1, col_ba2 = st.columns(2)

    with col_ba1:
        fig_ba = go.Figure(data=[
            go.Bar(
                name="Before", x=["Records"], y=[total_records],
                marker_color=ACCENT_CORAL, text=[f"{total_records:,}"],
                textposition="outside", textfont=dict(color=TEXT_PRIMARY),
            ),
            go.Bar(
                name="After Dedup", x=["Records"], y=[unique_after],
                marker_color=ACCENT_GREEN, text=[f"{unique_after:,}"],
                textposition="outside", textfont=dict(color=TEXT_PRIMARY),
            ),
        ])
        fig_ba.update_layout(**plotly_layout(
            title=dict(text="Record Count: Before vs After",
                       font=dict(color=TEXT_PRIMARY, size=14, weight=600)),
            barmode="group",
            height=350,
            margin=dict(t=50, b=30, l=50, r=30),
            yaxis=dict(title="Number of Records", gridcolor=SHADOW,
                       linecolor=BORDER, showgrid=True,
                       tickfont=dict(color=TEXT_SECONDARY, size=11),
                       title_font=dict(color=TEXT_PRIMARY, size=13)),
            xaxis=dict(tickfont=dict(color=TEXT_PRIMARY, size=12)),
            legend=dict(font=dict(color=TEXT_PRIMARY)),
        ))
        st.plotly_chart(fig_ba, use_container_width=True)

    with col_ba2:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=quality_after,
            delta={"reference": quality_before, "increasing": {"color": ACCENT_GREEN}},
            title={"text": "Data Quality Score", "font": {"color": TEXT_PRIMARY, "size": 16}},
            number={"font": {"color": TEXT_PRIMARY}},
            gauge={
                "axis": {"range": [0, 100], "tickfont": {"color": TEXT_SECONDARY}},
                "bar": {"color": ACCENT_GREEN},
                "steps": [
                    {"range": [0, 60], "color": "#FDECED"},
                    {"range": [60, 80], "color": "#FEF3C7"},
                    {"range": [80, 100], "color": "#E8F5E9"},
                ],
            },
        ))
        fig_gauge.update_layout(
            height=350, margin=dict(t=50, b=30),
            paper_bgcolor=BG_PAGE,
            font=dict(color=TEXT_PRIMARY),
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Summary text
    st.markdown(f"""
    <div class="pair-card">
        <h4 style="margin-top:0;color:{TEXT_PRIMARY} !important">📋 Summary</h4>
        <ul style="color:{TEXT_PRIMARY}">
            <li><strong>{total_records:,}</strong> total records → <strong>{unique_after:,}</strong> unique records after deduplication</li>
            <li><strong>{records_removed}</strong> duplicate records identified for merge/removal</li>
            <li><strong>{len(clusters)}</strong> duplicate clusters detected</li>
            <li>Data quality improved from <strong>{format_percentage(quality_before)}</strong> to <strong>{format_percentage(quality_after)}</strong></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ── Tab 5: Export ────────────────────────────────────────────────────
with tab_export:
    st.markdown("### Export Results")

    if not duplicates:
        st.info("No duplicates to export.")
    else:
        col_e1, col_e2, col_e3 = st.columns(3)

        with col_e1:
            st.markdown("**Duplicate Pairs Report**")
            pairs_data = []
            for d in duplicates:
                row = {
                    "Record A ID": d["record_id_a"],
                    "Company A": d["company_a"],
                    "Record B ID": d["record_id_b"],
                    "Company B": d["company_b"],
                    "Score": d["total_score"],
                    "Classification": d["classification"],
                }
                for field, score_val in d["field_scores"].items():
                    row[f"Score_{field}"] = score_val
                pairs_data.append(row)
            pairs_df = pd.DataFrame(pairs_data)
            st.download_button(
                "📥 Download Pairs CSV",
                pairs_df.to_csv(index=False),
                "duplicate_pairs_report.csv",
                "text/csv",
                use_container_width=True,
            )

        with col_e2:
            st.markdown("**Merge Recommendations**")
            merge_data = []
            for d in duplicates:
                if d["total_score"] >= 75:
                    merge_data.append({
                        "Keep Record": d["record_id_a"],
                        "Merge Record": d["record_id_b"],
                        "Company": d["company_a"],
                        "Score": d["total_score"],
                        "Action": "Auto-merge" if d["total_score"] >= 90 else "Review & merge",
                    })
            if merge_data:
                merge_df = pd.DataFrame(merge_data)
                st.download_button(
                    "📥 Download Merge List",
                    merge_df.to_csv(index=False),
                    "merge_recommendations.csv",
                    "text/csv",
                    use_container_width=True,
                )
            else:
                st.caption("No records scored high enough for merge recommendation.")

        with col_e3:
            st.markdown("**Flagged Dataset**")
            flagged_df = df.copy()
            flagged_df["is_duplicate"] = flagged_df["record_id"].isin(dup_record_ids)
            best_scores = {}
            for d in duplicates:
                for rid in [d["record_id_a"], d["record_id_b"]]:
                    if rid not in best_scores or d["total_score"] > best_scores[rid]:
                        best_scores[rid] = d["total_score"]
            flagged_df["best_match_score"] = flagged_df["record_id"].map(best_scores).fillna(0)
            flagged_df["duplicate_classification"] = flagged_df["best_match_score"].apply(
                lambda x: classify_score(x) if x >= 60 else "Clean"
            )
            st.download_button(
                "📥 Download Flagged Dataset",
                flagged_df.to_csv(index=False),
                "cleaned_dataset.csv",
                "text/csv",
                use_container_width=True,
            )


# ── Footer ───────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    Built by <strong>Arnaud Chacon</strong> as a demonstration of probabilistic record matching
    using Levenshtein distance scoring. This tool was created as part of a portfolio project.<br>
    <a href="https://www.linkedin.com/in/arnaudchacon/" target="_blank">LinkedIn</a> ·
    <a href="mailto:arnaudchacon@gmail.com">arnaudchacon@gmail.com</a>
</div>
""", unsafe_allow_html=True)
