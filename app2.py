import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── PAGE CONFIG ──────────────────────────────────────────────────
st.set_page_config(
    page_title="India Healthcare Investment Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── PALETTE ──────────────────────────────────────────────────────
NAVY   = "#083A4F"
GOLD   = "#A5BD66"
AQUA   = "#C0D5D6"
TEAL   = "#407E8C"
SAND   = "#E5E1DD"

NAVY_DARK  = "#052838"
NAVY_MID   = "#0a4a63"
GOLD_DARK  = "#8a9f52"
TEAL_DARK  = "#2e5c68"
TEAL_LIGHT = "#5a9eae"

# ── CUSTOM CSS ───────────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    .stApp {{
        background: linear-gradient(160deg, {NAVY_DARK} 0%, {NAVY} 60%, {NAVY_DARK} 100%);
        color: {SAND};
        font-family: 'Inter', sans-serif;
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {NAVY_DARK} 0%, {NAVY_MID} 100%);
        border-right: 1px solid {TEAL_DARK};
    }}
    [data-testid="stSidebar"] * {{
        color: {AQUA} !important;
    }}

    /* Hero */
    .hero {{
        background: linear-gradient(135deg, {NAVY_DARK} 0%, {NAVY_MID} 60%, {NAVY_DARK} 100%);
        border: 1px solid {TEAL_DARK};
        border-radius: 16px;
        padding: 48px 56px;
        margin-bottom: 36px;
        position: relative;
        overflow: hidden;
    }}
    .hero::after {{
        content: '';
        position: absolute;
        top: -80px; right: -80px;
        width: 320px; height: 320px;
        background: radial-gradient(circle, rgba(165,189,102,0.07) 0%, transparent 70%);
        pointer-events: none;
    }}
    .hero-eyebrow {{
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: {GOLD};
        margin-bottom: 14px;
    }}
    .hero-title {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 48px;
        font-weight: 700;
        color: {SAND};
        line-height: 1.1;
        margin-bottom: 16px;
    }}
    .hero-title em {{
        color: {GOLD};
        font-style: italic;
    }}
    .hero-body {{
        font-size: 15px;
        color: {AQUA};
        font-weight: 300;
        max-width: 580px;
        line-height: 1.7;
        margin-bottom: 28px;
    }}
    .hero-pill {{
        display: inline-block;
        background: rgba(165,189,102,0.1);
        border: 1px solid rgba(165,189,102,0.25);
        border-radius: 100px;
        padding: 6px 16px;
        margin-right: 10px;
        font-size: 12px;
        color: {GOLD};
        font-weight: 500;
    }}

    /* Ranking cards */
    .rank-card {{
        background: linear-gradient(160deg, {NAVY_MID} 0%, {NAVY} 100%);
        border: 1px solid {TEAL_DARK};
        border-radius: 12px;
        padding: 22px 20px;
        text-align: center;
        height: 100%;
        transition: border-color 0.2s;
    }}
    .rank-card:hover {{ border-color: {GOLD}; }}
    .rank-label {{
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}
    .rank-name {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 18px;
        font-weight: 600;
        color: {SAND};
        margin-bottom: 10px;
        line-height: 1.25;
    }}
    .rank-score {{
        font-size: 32px;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }}
    .rank-denom {{
        font-size: 14px;
        color: {AQUA};
        font-weight: 300;
    }}
    .rank-bar-bg {{
        height: 3px;
        background: rgba(192,213,214,0.12);
        border-radius: 2px;
        margin-top: 14px;
        overflow: hidden;
    }}

    /* Section labels */
    .sec-eyebrow {{
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: {GOLD};
        margin-bottom: 6px;
    }}
    .sec-title {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 28px;
        font-weight: 600;
        color: {SAND};
        margin-bottom: 4px;
    }}
    .sec-desc {{
        font-size: 13px;
        color: {AQUA};
        opacity: 0.7;
        margin-bottom: 20px;
    }}

    /* Insight box */
    .insight {{
        background: rgba(64,126,140,0.08);
        border-left: 3px solid {TEAL};
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        margin-top: 16px;
        font-size: 13px;
        color: {AQUA};
        line-height: 1.65;
    }}

    /* Divider */
    .divider {{
        border: none;
        border-top: 1px solid {TEAL_DARK};
        margin: 40px 0;
        opacity: 0.4;
    }}

    #MainMenu, footer, .stDeployButton {{ display: none; }}
</style>
""", unsafe_allow_html=True)

# ── CHART HELPER ─────────────────────────────────────────────────
def dark_layout(fig, height=420, title=""):
    fig.update_layout(
        height=height,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=AQUA, size=12),
        xaxis=dict(gridcolor=TEAL_DARK, zeroline=False,
                   tickfont=dict(color=AQUA)),
        yaxis=dict(gridcolor=TEAL_DARK, zeroline=False,
                   tickfont=dict(color=AQUA)),
        margin=dict(l=20, r=30, t=40, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)",
                    font=dict(color=AQUA)),
        title=dict(text=title,
                   font=dict(color=SAND, size=14,
                             family="Cormorant Garamond"))
    )
    return fig

# ── LOAD DATA ────────────────────────────────────────────────────
data_path = "C:/Users/hprai/OneDrive/Desktop/Python/Healtcare/India healthcare Analysis/Data"

@st.cache_data
def load_data():
    att = pd.read_csv(f"{data_path}/attractiveness_index.csv",
                      index_col=0, names=["sector","score"],
                      header=0)
    wt  = pd.read_csv(f"{data_path}/weighted_scores.csv",
                      index_col=0)
    return att, wt

attractiveness, weighted = load_data()
ranked = attractiveness.sort_values(
    "score", ascending=False).reset_index()

base_weights = pd.Series({
    "Market Size": 0.15, "CAGR": 0.25,
    "Disease Burden": 0.15, "Supply Gap": 0.15,
    "Policy Tailwinds": 0.10, "Digital Readiness": 0.10,
    "Competition (inv.)": 0.05, "Capital Efficiency": 0.05
})
raw_recovered = weighted.div(base_weights, axis=0)

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='padding:8px 0 20px;'>
        <div style='font-size:10px;letter-spacing:0.2em;
                    text-transform:uppercase;color:{GOLD};
                    font-weight:600;margin-bottom:8px;'>
            Project Brief
        </div>
        <div style='font-family:Cormorant Garamond,serif;
                    font-size:22px;font-weight:700;
                    color:{SAND};line-height:1.25;
                    margin-bottom:10px;'>
            India Healthcare<br>Intelligence
        </div>
        <div style='font-size:12px;color:{AQUA};
                    line-height:1.7;opacity:0.8;'>
            PE investment prioritization<br>
            across 5 healthcare verticals
        </div>
    </div>
    <hr style='border:none;border-top:1px solid {TEAL_DARK};
               margin:16px 0;opacity:0.4;'>
    <div style='font-size:10px;letter-spacing:0.15em;
                text-transform:uppercase;color:{GOLD};
                opacity:0.7;margin-bottom:12px;
                font-weight:600;'>
        Client Context
    </div>
    <div style='font-size:12px;color:{AQUA};line-height:2;'>
        <b style='color:{SAND};'>Persona:</b> Mid- large Indian PE firm<br>
        <b style='color:{SAND};'>Deploy:</b> ₹500-1500 crores<br>
        <b style='color:{SAND};'>Horizon:</b> 5-year hold<br>
        <b style='color:{SAND};'>Market:</b> India<br>
        <b style='color:{SAND};'>As of:</b> June 2026
    </div>
    <hr style='border:none;border-top:1px solid {TEAL_DARK};
               margin:16px 0;opacity:0.4;'>
    <div style='font-size:10px;letter-spacing:0.15em;
                text-transform:uppercase;color:{GOLD};
                opacity:0.7;margin-bottom:12px;
                font-weight:600;'>
        Data Sources
    </div>
    <div style='font-size:11px;color:{AQUA};
                line-height:2;opacity:0.8;'>
        MoHFW National Health Accounts<br>
        Rural Health Statistics 2021-22<br>
        NMHS 2015-16 · NIMHANS<br>
        ABDM Dashboard · Jun 2026<br>
        IBEF Healthcare Report 2026<br>
        Population Projections 2036
    </div>
    <hr style='border:none;border-top:1px solid {TEAL_DARK};
               margin:16px 0;opacity:0.4;'>
    <div style='font-size:10px;color:{TEAL};
                text-align:center;line-height:1.8;'>
        Python · Streamlit · Plotly
    </div>
    """, unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────
st.markdown(f"""
<div class='hero'>
    <div class='hero-eyebrow'>
        PE Investment Intelligence · India · 2026
    </div>
    <div class='hero-title'>
        Where Should <em>₹1500 crores</em><br>Go in Indian Healthcare?
    </div>
    <div class='hero-body'>
        A data-driven sector prioritization model ranking 5 healthcare 
        verticals across 8 weighted investment dimensions — built on 
        government datasets, demographic signals, and market intelligence.
    </div>
    <div>
        <span class='hero-pill'>5 Sectors Analysed</span>
        <span class='hero-pill'>8 Scoring Dimensions</span>
        <span class='hero-pill'>11 Real Datasets</span>
        <span class='hero-pill'>₹31.9 Lakh Crore Market</span>
    </div>
    <div style='margin-top:24px;font-size:12px;
                    color:{TEAL};letter-spacing:0.1em;'>
            Analysis by <strong style='color:{AQUA};'>
            Nidhi Pandey</strong> · June 2026
    </div>
</div>
""", unsafe_allow_html=True)

# ── RANKING CARDS ────────────────────────────────────────────────
st.markdown(f"""
<div class='sec-eyebrow'>Primary Output</div>
<div class='sec-title'>Sector Attractiveness Rankings</div>
<div class='sec-desc'>
    Weighted multi-criteria index · Higher = stronger investment case
</div>
""", unsafe_allow_html=True)

rank_colors = [GOLD, TEAL_LIGHT, AQUA, TEAL, AQUA]
rank_labels = ["#1 · Top Pick", "#2 · Strong",
               "#3 · Consider", "#4 · Watch", "#5 · Lowest"]

cols = st.columns(5)
for i, col in enumerate(cols):
    with col:
        score = ranked.iloc[i]["score"]
        bar_pct = int((score / 10) * 100)
        c = rank_colors[i]
        st.markdown(f"""
        <div class='rank-card'>
            <div class='rank-label' style='color:{c};'>
                {rank_labels[i]}
            </div>
            <div class='rank-name'>{ranked.iloc[i]['sector']}</div>
            <div class='rank-score' style='color:{c};'>
                {score}<span class='rank-denom'>/10</span>
            </div>
            <div class='rank-bar-bg'>
                <div style='width:{bar_pct}%;height:100%;
                            background:{c};border-radius:2px;'>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── CHARTS ROW ───────────────────────────────────────────────────
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.markdown(f"""
    <div class='sec-eyebrow'>Rankings</div>
    <div class='sec-title'>Attractiveness Index</div>
    """, unsafe_allow_html=True)

    bar_colors_list = [GOLD, TEAL_LIGHT, AQUA, TEAL, TEAL_DARK]
    fig_bar = go.Figure(go.Bar(
        x=ranked["score"],
        y=ranked["sector"],
        orientation="h",
        marker=dict(
            color=bar_colors_list,
            line=dict(color="rgba(0,0,0,0)")
        ),
        text=ranked["score"].apply(lambda x: f"{x:.2f}"),
        textposition="outside",
        textfont=dict(color=SAND, size=13, family="Inter")
    ))
    fig_bar = dark_layout(fig_bar, title="Score out of 10")
    fig_bar.update_xaxes(range=[0, 8])
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.markdown(f"""
    <div class='sec-eyebrow'>Strategic View</div>
    <div class='sec-title'>Risk — Opportunity Matrix</div>
    """, unsafe_allow_html=True)

    risk_data = pd.DataFrame({
        "sector": ["Digital Health", "Elderly Care",
                   "Mental Health", "Rural Primary Care",
                   "Diagnostics"],
        "attractiveness": [6.36, 5.58, 5.21, 5.15, 5.05],
        "execution_risk": [6.5, 7.2, 5.8, 8.1, 4.2],
        "market_size":    [5.4, 12.2, 0.48, 0.59, 10.95],
        "color": [GOLD, TEAL_LIGHT, AQUA, TEAL, GOLD_DARK]
    })

    fig_m = go.Figure()
    for _, row in risk_data.iterrows():
        fig_m.add_trace(go.Scatter(
            x=[row["attractiveness"]],
            y=[row["execution_risk"]],
            mode="markers+text",
            name=row["sector"],
            text=[row["sector"]],
            textposition="top center",
            textfont=dict(size=11, color=SAND,
                          family="Inter"),
            marker=dict(
                size=row["market_size"] * 4 + 15,
                color=row["color"],
                opacity=0.9,
                line=dict(color="rgba(255,255,255,0.15)",
                          width=1)
            )
        ))

    fig_m.add_hline(y=6.0, line_dash="dot",
                    line_color=TEAL_DARK, line_width=1)
    fig_m.add_vline(x=5.5, line_dash="dot",
                    line_color=TEAL_DARK, line_width=1)

    for text, x, y in [
        ("High Opp · High Risk", 6.55, 9.4),
        ("High Opp · Low Risk ⭐", 6.55, 3.6),
        ("Low Opp · High Risk", 4.15, 9.4),
        ("Low Opp · Low Risk", 4.15, 3.6)
    ]:
        fig_m.add_annotation(
            x=x, y=y, text=text, showarrow=False,
            font=dict(size=10, color=TEAL,
                      family="Inter"))

    fig_m = dark_layout(fig_m)
    fig_m.update_xaxes(range=[4, 7.2],
                        title="Attractiveness →")
    fig_m.update_yaxes(range=[3, 10],
                        title="Risk →")
    fig_m.update_layout(showlegend=False)
    st.plotly_chart(fig_m, use_container_width=True)

# ── DEEP DIVE ────────────────────────────────────────────────────
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.markdown(f"""
<div class='sec-eyebrow'>Deep Dive</div>
<div class='sec-title'>Dimension-by-Dimension Breakdown</div>
<div class='sec-desc'>
    Select a sector to understand exactly why it scored the way it did
</div>
""", unsafe_allow_html=True)

selected = st.selectbox(
    "sector",
    options=ranked["sector"].tolist(),
    label_visibility="collapsed"
)

sector_raw = raw_recovered[selected]
sector_df = pd.DataFrame({
    "Dimension": sector_raw.index,
    "Score": sector_raw.values.round(1)
}).sort_values("Score", ascending=True)

col_r, col_b = st.columns(2)

with col_r:
    fig_radar = go.Figure(go.Scatterpolar(
        r=sector_df["Score"].tolist() +
          [sector_df["Score"].iloc[0]],
        theta=sector_df["Dimension"].tolist() +
              [sector_df["Dimension"].iloc[0]],
        fill="toself",
        fillcolor=f"rgba(165,189,102,0.12)",
        line=dict(color=GOLD, width=2),
        marker=dict(color=GOLD, size=7)
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 10],
                gridcolor=TEAL_DARK,
                tickfont=dict(color=AQUA, size=9),
                tickcolor=TEAL_DARK
            ),
            angularaxis=dict(
                gridcolor=TEAL_DARK,
                tickfont=dict(color=AQUA, size=11,
                              family="Inter")
            )
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=AQUA, family="Inter"),
        margin=dict(l=50, r=50, t=50, b=50),
        height=380,
        title=dict(
            text=f"{selected} — Radar",
            font=dict(color=SAND, size=14,
                      family="Cormorant Garamond"))
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col_b:
    bar_c = [GOLD if s >= 7
             else TEAL if s >= 4
             else "#c0392b"
             for s in sector_df["Score"]]

    fig_dim = go.Figure(go.Bar(
        x=sector_df["Score"],
        y=sector_df["Dimension"],
        orientation="h",
        marker=dict(color=bar_c,
                    line=dict(color="rgba(0,0,0,0)")),
        text=sector_df["Score"],
        textposition="outside",
        textfont=dict(color=SAND, size=12, family="Inter")
    ))
    fig_dim = dark_layout(fig_dim, height=380,
                           title=f"{selected} — By Dimension")
    fig_dim.update_xaxes(range=[0, 12])
    st.plotly_chart(fig_dim, use_container_width=True)

top_d = sector_df.loc[sector_df["Score"].idxmax(), "Dimension"]
low_d = sector_df.loc[sector_df["Score"].idxmin(), "Dimension"]
tot   = attractiveness.loc[selected, "score"]

st.markdown(f"""
<div class='insight'>
    💡 <strong style='color:{SAND};'>{selected}</strong> scores 
    <strong style='color:{GOLD};'>{tot}/10</strong> overall. 
    Strongest dimension: 
    <strong style='color:{GOLD};'>{top_d}</strong>. 
    Weakest: 
    <strong style='color:#c0392b;'>{low_d}</strong>. 
    Gold bars = strong (7+) · Teal = moderate (4–7) · 
    Red = needs attention (&lt;4).
</div>
""", unsafe_allow_html=True)

# ── WEIGHT SLIDERS ───────────────────────────────────────────────
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.markdown(f"""
<div class='sec-eyebrow'>Sensitivity Analysis</div>
<div class='sec-title'>Adjust Weights — Watch Rankings Shift</div>
<div class='sec-desc'>
    Reprioritize dimensions to match your investment thesis. 
    Weights must sum to 100%.
</div>
""", unsafe_allow_html=True)

cs, cr = st.columns([1, 2])

with cs:
    w1 = st.slider("Market Size",        0, 30, 15, 5)
    w2 = st.slider("CAGR (Growth Rate)", 0, 40, 25, 5)
    w3 = st.slider("Disease Burden",     0, 30, 15, 5)
    w4 = st.slider("Supply Gap",         0, 30, 15, 5)
    w5 = st.slider("Policy Tailwinds",   0, 20, 10, 5)
    w6 = st.slider("Digital Readiness",  0, 20, 10, 5)
    w7 = st.slider("Competition (inv.)", 0, 20,  5, 5)
    w8 = st.slider("Capital Efficiency", 0, 20,  5, 5)

    tw = w1+w2+w3+w4+w5+w6+w7+w8

    if tw != 100:
        st.markdown(f"""
        <div style='background:rgba(192,57,43,0.1);
                    border:1px solid rgba(192,57,43,0.3);
                    border-radius:8px;padding:10px 14px;
                    font-size:12px;color:#e88;margin-top:8px;'>
            ⚠️ Weights sum to <strong>{tw}%</strong>. 
            Adjust to reach 100%.
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background:rgba(165,189,102,0.1);
                    border:1px solid rgba(165,189,102,0.3);
                    border-radius:8px;padding:10px 14px;
                    font-size:12px;color:{GOLD};margin-top:8px;'>
            ✅ Weights sum to 100% — rankings updated
        </div>""", unsafe_allow_html=True)

with cr:
    if tw == 100:
        nw = pd.Series({
            "Market Size": w1/100, "CAGR": w2/100,
            "Disease Burden": w3/100, "Supply Gap": w4/100,
            "Policy Tailwinds": w5/100,
            "Digital Readiness": w6/100,
            "Competition (inv.)": w7/100,
            "Capital Efficiency": w8/100
        })
        ns = raw_recovered.multiply(nw, axis=0).sum()
        nr = ns.round(2).sort_values(
            ascending=False).reset_index()
        nr.columns = ["sector", "score"]

        nr_colors = [GOLD, TEAL_LIGHT, AQUA,
                     TEAL, TEAL_DARK]

        fig_n = go.Figure(go.Bar(
            x=nr["score"], y=nr["sector"],
            orientation="h",
            marker=dict(color=nr_colors,
                        line=dict(color="rgba(0,0,0,0)")),
            text=nr["score"].apply(lambda x: f"{x:.2f}"),
            textposition="outside",
            textfont=dict(color=SAND, size=13,
                          family="Inter")
        ))
        fig_n = dark_layout(
            fig_n, title="Updated Rankings")
        fig_n.update_xaxes(range=[0, 11])
        st.plotly_chart(fig_n, use_container_width=True)

        orig = ranked["sector"].tolist()
        new  = nr["sector"].tolist()
        if orig != new:
            st.markdown(f"""
            <div class='insight' 
                 style='border-left-color:{GOLD};'>
                ⚡ Rankings shifted. Original #1: 
                <strong>{orig[0]}</strong> → 
                New #1: 
                <strong style='color:{GOLD};'>{new[0]}</strong>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='insight' 
                 style='border-left-color:{GOLD};'>
                ✅ Rankings unchanged — the prioritization 
                is robust to these weight adjustments.
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='display:flex;align-items:center;
                    justify-content:center;height:280px;
                    color:{TEAL_DARK};font-size:14px;
                    border:1px dashed {TEAL_DARK};
                    border-radius:12px;font-family:Inter;'>
            👈 Adjust sliders until weights sum to 100%
        </div>""", unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────────
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align:center;padding:16px 0 40px;'>
    <div style='font-family:Cormorant Garamond,serif;
                font-size:18px;color:{TEAL};
                margin-bottom:8px;'>
        India Healthcare Sector Prioritization Model
    </div>
    <div style='font-size:11px;color:{TEAL_DARK};
                line-height:2;'>
        Data: MoHFW · RHS · NMHS · ABDM · IBEF · 
        Census of India · June 2026<br>
        Python · Streamlit · Plotly
    </div>
</div>
""", unsafe_allow_html=True)