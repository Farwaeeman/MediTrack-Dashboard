import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MediTrack Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS — PREMIUM DARK SAAS THEME
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #0c1220 !important;
    color: #e2e8f0 !important;
}
.stApp, [data-testid="stAppViewContainer"] { background-color: #0c1220 !important; }
[data-testid="stHeader"] { background: #0c1220 !important; box-shadow: none !important; }
.block-container { padding: 0 2rem 4rem 2rem !important; max-width: 1440px !important; }
#MainMenu, footer { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1020 0%, #0c1525 100%) !important;
    border-right: 1px solid rgba(76,201,240,0.08) !important;
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }

/* ── Metric Cards ── */
[data-testid="metric-container"] {
    background: #131e2e !important;
    border: 1px solid rgba(76,201,240,0.1) !important;
    border-radius: 14px !important;
    padding: 20px 22px !important;
    position: relative !important;
    overflow: hidden !important;
    transition: border-color 0.25s, box-shadow 0.25s, transform 0.2s !important;
}
[data-testid="metric-container"]::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(76,201,240,0.35), transparent);
}
[data-testid="metric-container"]:hover {
    border-color: rgba(76,201,240,0.3) !important;
    box-shadow: 0 0 24px rgba(76,201,240,0.1) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stMetricLabel"] p {
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 1.6px !important;
    text-transform: uppercase !important;
    color: #475569 !important;
}
[data-testid="stMetricValue"] {
    font-size: 30px !important;
    font-weight: 800 !important;
    color: #f1f5f9 !important;
    letter-spacing: -0.8px !important;
    line-height: 1.1 !important;
}
[data-testid="stMetricDelta"] > div {
    font-size: 11px !important;
    font-weight: 600 !important;
    margin-top: 4px !important;
}

/* ── Tabs ── */
[data-baseweb="tab-list"] {
    background: #131e2e !important;
    border: 1px solid rgba(76,201,240,0.1) !important;
    border-radius: 12px !important;
    padding: 5px !important;
    gap: 2px !important;
    margin-bottom: 22px !important;
}
button[data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #475569 !important;
    background: transparent !important;
    border-radius: 8px !important;
    padding: 9px 20px !important;
    transition: all 0.2s !important;
    letter-spacing: 0.1px !important;
}
button[data-baseweb="tab"]:hover {
    color: #94a3b8 !important;
    background: rgba(255,255,255,0.04) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: rgba(76,201,240,0.12) !important;
    color: #4CC9F0 !important;
    border: 1px solid rgba(76,201,240,0.2) !important;
    box-shadow: 0 0 16px rgba(76,201,240,0.12) !important;
}
[data-baseweb="tab-highlight"] { display: none !important; }
[data-baseweb="tab-panel"] { padding: 0 !important; }

/* ── Selects / Inputs ── */
div[data-baseweb="select"] > div {
    background: #131e2e !important;
    border: 1px solid rgba(76,201,240,0.12) !important;
    border-radius: 9px !important;
    color: #cbd5e1 !important;
    font-size: 13px !important;
    transition: border-color 0.2s !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: rgba(76,201,240,0.4) !important;
    box-shadow: 0 0 0 3px rgba(76,201,240,0.06) !important;
}
div[data-baseweb="select"] * { color: #cbd5e1 !important; }
div[data-baseweb="popover"] {
    background: #131e2e !important;
    border: 1px solid rgba(76,201,240,0.15) !important;
    border-radius: 10px !important;
    box-shadow: 0 16px 48px rgba(0,0,0,0.5) !important;
}
li[role="option"] { color: #cbd5e1 !important; font-size: 13px !important; }
li[role="option"]:hover { background: rgba(76,201,240,0.08) !important; }

[data-testid="stTextInput"] > div > div {
    background: #131e2e !important;
    border: 1px solid rgba(76,201,240,0.12) !important;
    border-radius: 9px !important;
    transition: all 0.2s !important;
}
[data-testid="stTextInput"] > div > div:focus-within {
    border-color: rgba(76,201,240,0.4) !important;
    box-shadow: 0 0 0 3px rgba(76,201,240,0.06) !important;
}
[data-testid="stTextInput"] input {
    color: #cbd5e1 !important;
    font-size: 13px !important;
    background: transparent !important;
}
[data-testid="stTextInput"] input::placeholder { color: #334155 !important; }

/* ── Slider ── */
[data-testid="stSlider"] [role="slider"] {
    background: #4CC9F0 !important;
    border: 2px solid #0c1220 !important;
    box-shadow: 0 0 10px rgba(76,201,240,0.4) !important;
}
[data-testid="stSlider"] > div > div > div { background: #1e2d42 !important; }
[data-testid="stSlider"] > div > div > div > div { background: #4CC9F0 !important; }

/* ── Radio ── */
[data-testid="stRadio"] > div { gap: 6px !important; }
[data-testid="stRadio"] label {
    background: #131e2e;
    border: 1px solid rgba(76,201,240,0.1);
    border-radius: 8px;
    padding: 7px 14px;
    font-size: 12px;
    font-weight: 600;
    color: #64748b;
    cursor: pointer;
    transition: all 0.15s;
}
[data-testid="stRadio"] label:hover {
    border-color: rgba(76,201,240,0.3);
    color: #4CC9F0;
}

/* ── Multiselect ── */
[data-baseweb="tag"] {
    background: rgba(76,201,240,0.1) !important;
    border: 1px solid rgba(76,201,240,0.2) !important;
    border-radius: 5px !important;
}
[data-baseweb="tag"] span { color: #4CC9F0 !important; font-weight: 600 !important; font-size: 11px !important; }

/* ── Widget Labels ── */
[data-testid="stWidgetLabel"] p {
    font-size: 10px !important;
    font-weight: 700 !important;
    color: #334155 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.3px !important;
}

/* ── Checkbox ── */
[data-testid="stCheckbox"] label {
    font-size: 12px !important;
    color: #64748b !important;
    font-weight: 600 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0c1220; }
::-webkit-scrollbar-thumb { background: rgba(76,201,240,0.15); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(76,201,240,0.3); }

hr { border-color: rgba(76,201,240,0.08) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# COLOR SYSTEM — CONSISTENT PROFESSIONAL PALETTE
# ─────────────────────────────────────────────
# Primary: cyan-blue (brand accent for most charts)
# Semantic: green=good, amber=medium, red=risk
PRIMARY  = "#4CC9F0"   # Main chart color
PRIMARY2 = "#38a3c4"   # Slightly deeper variant
PRIMARY_DIM = "rgba(76,201,240,0.08)"
SUCCESS  = "#22C55E"   # Green — good / low risk
WARNING  = "#F59E0B"   # Amber — medium
DANGER   = "#EF4444"   # Red — high risk
NEUTRAL  = "#334d66"   # Muted bar (non-highlighted)

# Plotly surface
PBG  = "#131e2e"
PGRD = "rgba(255,255,255,0.03)"
PFNT = "#475569"

# Department colors — muted, coherent family
DEPT_HEX = {
    "General":       "#4CC9F0",   # Primary cyan
    "Cardiology":    "#7C3AED",   # Violet — distinctive for cardiac
    "Joint & Mobility": "#38BDF8",# Sky blue
    "Dermatology":   "#6EE7B7",   # Mint green
    "Kids Health":   "#A78BFA",   # Soft lavender
}

# Internal keys (data keys stay as original for filtering logic)
DEPT_DISPLAY = {
    "General":       "General",
    "Cardiology":    "Cardiology",
    "Orthopedics":   "Joint & Mobility",
    "Dermatology":   "Dermatology",
    "Pediatrics":    "Kids Health",
}
DEPT_DISPLAY_REV = {v: k for k, v in DEPT_DISPLAY.items()}

DEPT_ICN = {
    "General":       "◈",
    "Cardiology":    "◉",
    "Orthopedics":   "◎",
    "Dermatology":   "◆",
    "Pediatrics":    "◇",
}
DEPT_EMOJI = {
    "General":       "🏥",
    "Cardiology":    "🫀",
    "Orthopedics":   "🦴",
    "Dermatology":   "🌿",
    "Pediatrics":    "👶",
}

# ─────────────────────────────────────────────
# PLOTLY THEME FUNCTION
# ─────────────────────────────────────────────
def sfig(fig, h=320, legend=False):
    fig.update_layout(
        paper_bgcolor=PBG,
        plot_bgcolor=PBG,
        font=dict(family="Inter", color=PFNT, size=11),
        height=h,
        margin=dict(l=8, r=8, t=30, b=8),
        showlegend=legend,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(size=11, color="#64748b")
        ),
        xaxis=dict(
            gridcolor=PGRD,
            linecolor="rgba(76,201,240,0.08)",
            tickfont=dict(size=11, color="#475569"),
            showline=True
        ),
        yaxis=dict(
            gridcolor=PGRD,
            linecolor="rgba(0,0,0,0)",
            tickfont=dict(size=11, color="#475569")
        ),
    )
    return fig

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
CITIES = ["Karachi","Lahore","Islamabad","Peshawar","Multan"]
DEPTS  = ["General","Cardiology","Orthopedics","Dermatology","Pediatrics"]

np.random.seed(42)

monthly = pd.DataFrame({
    "month":     pd.date_range("2024-01", periods=12, freq="MS"),
    "appts":     np.random.randint(1280, 1460, 12),
    "rev":       np.random.randint(3_200_000, 3_800_000, 12),
    "noshow":    np.round(np.random.uniform(16, 22, 12), 1),
    "cancelled": np.round(np.random.uniform(8, 13, 12), 1),
    "completed": np.round(np.random.uniform(65, 75, 12), 1),
})

city_df = pd.DataFrame({
    "city":         CITIES,
    "revenue":      [11.0, 8.5, 7.7, 7.5, 7.3],
    "trend":        [5.6, 2.1, 1.8, 3.2, -0.9],
    "appts":        [5800, 4900, 4600, 4200, 3900],
    "noshow":       [19.2, 18.1, 17.8, 20.1, 19.5],
    "satisfaction": [4.3, 4.1, 4.5, 3.9, 4.2],
})

dept_df = pd.DataFrame({
    "dept":         DEPTS,
    "revenue":      [10.5, 10.2, 9.8, 6.8, 4.4],
    "noshow":       [17.2, 22.0, 17.0, 23.2, 17.4],
    "appts":        [6800, 5200, 5600, 3900, 3500],
    "avg_wait":     [12, 22, 18, 15, 10],
    "satisfaction": [4.2, 3.8, 4.0, 3.6, 4.5],
})

RAW_DOCS = [
    ("Prof. Dr. Amna Siddiqui","Dermatology","Consultant",188,0.33,34.6),
    ("Prof. Dr. Sara Malik",   "Cardiology", "Consultant",153,0.44,31.4),
    ("Dr. Sara Khan",          "Dermatology","Junior",    186,0.19,28.0),
    ("Dr. Ahmed Siddiqui",     "Dermatology","Junior",    237,0.32,26.6),
    ("Dr. Usman Baig",         "Dermatology","Senior",    194,0.33,25.8),
    ("Dr. Ali Malik",          "Dermatology","Senior",    169,0.30,25.4),
    ("Dr. Usman Khan",         "Cardiology", "Mid",       178,0.43,25.3),
    ("Prof. Dr. Fatima Khan",  "Cardiology", "Consultant",183,0.90,25.1),
    ("Dr. Maryam Malik",       "Cardiology", "Junior",    152,0.34,25.0),
    ("Prof. Dr. Zainab Baig",  "Cardiology", "Consultant",157,0.71,24.8),
    ("Dr. Bilal Raza",         "General",    "Senior",    210,0.55,18.9),
    ("Dr. Hina Tariq",         "Pediatrics", "Mid",       195,0.28,17.4),
    ("Dr. Kamran Sheikh",      "Orthopedics","Senior",    221,0.62,16.8),
    ("Dr. Nadia Qureshi",      "General",    "Junior",    175,0.21,15.2),
    ("Dr. Tariq Jameel",       "Pediatrics", "Consultant",198,0.48,14.6),
]
doc_df = pd.DataFrame(
    RAW_DOCS,
    columns=["Doctor","Department","Seniority","Appointments","Revenue","No-Show %"]
)

days_df = pd.DataFrame({
    "day":         ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
    "count":       [3950,3800,3750,3900,3700,3600,1200],
    "noshow_rate": [18.2,17.9,18.5,17.4,19.8,17.1,23.4],
})

# ─── COMPUTED SIGNALS ───
worst_dept = dept_df.loc[dept_df["noshow"].idxmax()]
worst_doc  = doc_df.loc[doc_df["No-Show %"].idxmax()]
worst_day  = days_df.loc[days_df["count"].idxmin()]
top_city   = city_df.loc[city_df["revenue"].idxmax()]
worst_dept_display = DEPT_DISPLAY.get(worst_dept["dept"], worst_dept["dept"])

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def sec(title, sub=""):
    s = (f'<span style="font-size:11px;color:#334155;font-weight:500;margin-left:10px">{sub}</span>'
         if sub else "")
    return (f'<div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:12px;'
            f'letter-spacing:-0.1px">{title}{s}</div>')

def ns_color(v):
    return DANGER if v > 30 else WARNING if v > 25 else SUCCESS

def risk_tag(v):
    c, bg, lbl = (
        (DANGER,  "rgba(239,68,68,0.12)",   "High")   if v > 30 else
        (WARNING, "rgba(245,158,11,0.12)",  "Medium") if v > 25 else
        (SUCCESS, "rgba(34,197,94,0.12)",   "Low")
    )
    return (f'<span style="background:{bg};color:{c};border-radius:5px;padding:3px 10px;'
            f'font-size:10px;font-weight:700;border:1px solid {c}28">{lbl}</span>')

def dept_color(dept_key):
    display = DEPT_DISPLAY.get(dept_key, dept_key)
    return DEPT_HEX.get(display, PRIMARY)

def dept_label(dept_key):
    return DEPT_DISPLAY.get(dept_key, dept_key)

def dept_emoji(dept_key):
    return DEPT_EMOJI.get(dept_key, "🏥")

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:8px 0 20px">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
            <div style="background:linear-gradient(135deg,#0e7490,#4CC9F0);width:42px;height:42px;
                 border-radius:11px;display:flex;align-items:center;justify-content:center;
                 box-shadow:0 4px 16px rgba(76,201,240,0.25)">
                <span style="font-size:20px">🏥</span>
            </div>
            <div>
                <div style="font-size:16px;font-weight:800;color:#f1f5f9;letter-spacing:-0.4px">MediTrack</div>
                <div style="font-size:9px;color:#334155;text-transform:uppercase;letter-spacing:2px;font-weight:600">Analytics Pro</div>
            </div>
        </div>
        <div style="background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.2);
             border-radius:8px;padding:8px 12px;display:flex;align-items:center;gap:8px">
            <div style="width:6px;height:6px;background:#22C55E;border-radius:50%;
                 box-shadow:0 0 8px rgba(34,197,94,0.6)"></div>
            <span style="font-size:11px;color:#4ade80;font-weight:600">Live · 25,000 records</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size:9px;font-weight:700;color:#1e3a5f;text-transform:uppercase;'
        'letter-spacing:1.5px;margin-bottom:8px">Filters</div>',
        unsafe_allow_html=True
    )
    city_filter = st.multiselect("Cities", CITIES, default=CITIES)
    dept_filter = st.multiselect("Departments", DEPTS, default=DEPTS)

    st.markdown("---")
    st.markdown(
        '<div style="font-size:9px;font-weight:700;color:#1e3a5f;text-transform:uppercase;'
        'letter-spacing:1.5px;margin-bottom:10px">Quick Stats</div>',
        unsafe_allow_html=True
    )
    st.metric("Total Appointments", "25,000", "+4.2%")
    st.metric("Total Revenue", "₨ 41.7M", "+8.1%")

    st.markdown("---")
    st.markdown("""
    <div style="font-size:10px;color:#1e3a5f;text-align:center;font-weight:500;line-height:1.6">
        Pakistan Private Healthcare<br>Network · FY 2024
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div style="padding:24px 0 20px;margin-bottom:24px;border-bottom:1px solid rgba(76,201,240,0.08)">
    <div style="display:flex;align-items:flex-start;justify-content:space-between">
        <div>
            <div style="font-size:24px;font-weight:800;color:#f1f5f9;letter-spacing:-0.6px;line-height:1.1">
                MediTrack Analytics
            </div>
            <div style="font-size:12px;color:#334155;margin-top:5px;font-weight:500">
                Pakistan Private Healthcare Network &nbsp;·&nbsp; 5 Cities &nbsp;·&nbsp; 5 Departments
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;margin-top:4px">
            <div style="background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.2);
                 border-radius:7px;padding:6px 14px;font-size:11px;color:#4ade80;font-weight:600;
                 display:flex;align-items:center;gap:6px">
                <div style="width:5px;height:5px;background:#22C55E;border-radius:50%;
                     box-shadow:0 0 6px #22C55E"></div>
                Live
            </div>
            <div style="background:#131e2e;border:1px solid rgba(76,201,240,0.1);
                 border-radius:7px;padding:6px 14px;font-size:11px;color:#475569;font-weight:600">
                FY 2024
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Appointments",    "25,000",   "+4.2% vs last qtr")
k2.metric("Total Revenue",   "₨ 41.7M",  "+8.1% vs last qtr")
k3.metric("Completion Rate", "70.4%",    "+2.1 pts")
k4.metric("No-Show Rate",    "18.8%",    "▲ 0.8 pts")
k5.metric("Cancellations",   "10.8%",    "↓ −0.3 pts")

# ─────────────────────────────────────────────
# ALERT BANNER
# ─────────────────────────────────────────────
st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="background:rgba(245,158,11,0.06);border:1px solid rgba(245,158,11,0.2);
     border-left:3px solid {WARNING};border-radius:10px;padding:12px 18px;
     display:flex;align-items:center;gap:12px">
    <span style="font-size:15px;flex-shrink:0">⚠</span>
    <div style="font-size:12.5px;color:#d4a017;font-weight:500;line-height:1.5">
        <b style="color:{WARNING}">Attention Required:</b>
        {dept_emoji(worst_dept['dept'])} <b>{worst_dept_display}</b> department has the highest no-show rate at
        <b style="color:{WARNING}">{worst_dept['noshow']}%</b>.
        Scheduling review recommended.
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SMART INSIGHTS ROW
# ─────────────────────────────────────────────
st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
st.markdown(
    '<div style="font-size:9px;font-weight:700;color:#1e3a5f;text-transform:uppercase;'
    'letter-spacing:1.5px;margin-bottom:10px">Smart Insights</div>',
    unsafe_allow_html=True
)

ins_data = [
    ("Highest No-Show",
     f"{dept_emoji(worst_dept['dept'])} {worst_dept_display} leads with {worst_dept['noshow']}% no-show rate",
     f"{worst_dept['noshow']}%", DANGER,
     "rgba(239,68,68,0.06)", "rgba(239,68,68,0.14)"),
    ("Staff Risk Flag",
     f"Dr. {worst_doc['Doctor'].split('Dr.')[-1].strip()} — {worst_doc['No-Show %']}% missed appointments",
     f"{worst_doc['No-Show %']}%", WARNING,
     "rgba(245,158,11,0.06)", "rgba(245,158,11,0.14)"),
    ("Lowest Volume Day",
     f"{worst_day['day']}s show only {worst_day['count']:,} appointments network-wide",
     f"{worst_day['count']:,}", PRIMARY,
     "rgba(76,201,240,0.06)", "rgba(76,201,240,0.14)"),
    ("Revenue Leader",
     f"{top_city['city']} leads all cities at ₨{top_city['revenue']}M revenue",
     f"+{top_city['trend']}%", SUCCESS,
     "rgba(34,197,94,0.06)", "rgba(34,197,94,0.14)"),
]

ic = st.columns(4)
for col, (label, text, val, color, bg, bdr) in zip(ic, ins_data):
    with col:
        st.markdown(f"""
        <div style="background:{bg};border:1px solid {bdr};border-radius:10px;
             padding:14px 16px;transition:border-color 0.2s">
            <div style="font-size:9px;font-weight:700;color:{color};text-transform:uppercase;
                 letter-spacing:1.1px;margin-bottom:6px">{label}</div>
            <div style="font-size:11.5px;color:#64748b;line-height:1.55;margin-bottom:10px;
                 font-weight:400">{text}</div>
            <div style="font-size:21px;font-weight:800;color:{color};letter-spacing:-0.5px">{val}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS — UPDATED NAMES
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "◈  Performance Overview",
    "🧬  Departments",
    "◉  Medical Staff",
    "◎  Patient Reliability",
])

# ══════════════════════════════════════════════
# TAB 1 — PERFORMANCE OVERVIEW
# ══════════════════════════════════════════════
with tab1:

    # Filter bar
    fc1, fc2, fc3 = st.columns([2, 2.5, 1.5])
    with fc1:
        city_t1 = st.multiselect("Cities", CITIES, default=CITIES, key="t1_c")
    with fc2:
        dr = st.radio(
            "Period",
            ["Last 3 Months", "Last 6 Months", "Full Year 2024"],
            horizontal=True, key="t1_dr"
        )
    with fc3:
        show_avg = st.checkbox("Show rolling average", value=True, key="t1_avg")

    n_mo = {"Last 3 Months": 3, "Last 6 Months": 6, "Full Year 2024": 12}[dr]
    mdf  = monthly.tail(n_mo).copy()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Row 1: Revenue by city + Appointment trend ──
    r1a, r1b = st.columns(2)

    with r1a:
        st.markdown(sec("Revenue by City", "PKR millions"), unsafe_allow_html=True)
        # Single color, highlight max
        bar_c = [PRIMARY if v == max(city_df["revenue"]) else NEUTRAL for v in city_df["revenue"]]
        fig = go.Figure(go.Bar(
            x=city_df["city"], y=city_df["revenue"],
            marker=dict(color=bar_c, line=dict(width=0), cornerradius=5),
            text=[f"₨{v}M" for v in city_df["revenue"]],
            textposition="outside",
            textfont=dict(size=11, color="#64748b"),
        ))
        fig.update_layout(bargap=0.38)
        st.plotly_chart(sfig(fig), use_container_width=True)

        p_cols = st.columns(5)
        for i, (_, row) in enumerate(city_df.iterrows()):
            c  = SUCCESS if row["trend"] >= 0 else DANGER
            bg = "rgba(34,197,94,0.08)" if row["trend"] >= 0 else "rgba(239,68,68,0.08)"
            ar = "↑" if row["trend"] >= 0 else "↓"
            p_cols[i].markdown(f"""
            <div style="background:{bg};color:{c};border-radius:6px;padding:5px 3px;
                 text-align:center;font-size:10px;font-weight:600;margin-top:-6px;
                 border:1px solid {c}22">
                {row['city']}<br><span style="font-size:12px;font-weight:700">{ar}{abs(row['trend'])}%</span>
            </div>""", unsafe_allow_html=True)

    with r1b:
        st.markdown(sec("Monthly Appointment Trend", f"Last {n_mo} months"), unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=mdf["month"], y=mdf["appts"],
            mode="lines+markers",
            line=dict(color=PRIMARY, width=2.5, shape="spline"),
            marker=dict(size=7, color=PRIMARY, line=dict(color="#0c1220", width=2)),
            fill="tozeroy",
            fillcolor="rgba(76,201,240,0.06)",
            name="Appointments"
        ))
        if show_avg:
            fig2.add_trace(go.Scatter(
                x=mdf["month"], y=mdf["appts"].rolling(3, min_periods=1).mean(),
                mode="lines",
                line=dict(color=WARNING, width=1.8, dash="dot"),
                name="3-mo average"
            ))
        st.plotly_chart(sfig(fig2, legend=True), use_container_width=True)

    # ── Row 2: Monthly revenue + Day of week ──
    r2a, r2b = st.columns(2)

    with r2a:
        st.markdown(sec("Monthly Revenue", "PKR 2024"), unsafe_allow_html=True)
        # Single-color gradient, not rainbow
        fig3 = go.Figure(go.Bar(
            x=mdf["month"].dt.strftime("%b"),
            y=mdf["rev"],
            marker=dict(
                color=mdf["rev"],
                colorscale=[[0, "#1a3550"], [1, PRIMARY]],
                line=dict(width=0),
                cornerradius=5
            ),
            text=[f"₨{v/1e6:.2f}M" for v in mdf["rev"]],
            textposition="outside",
            textfont=dict(size=10, color="#64748b")
        ))
        fig3.update_layout(bargap=0.28)
        st.plotly_chart(sfig(fig3), use_container_width=True)

    with r2b:
        st.markdown(sec("Volume by Day of Week", "With no-show rate overlay"), unsafe_allow_html=True)
        fig4 = make_subplots(specs=[[{"secondary_y": True}]])
        # Primary color for bars, red only for Sunday (meaningful semantic)
        day_c = [DANGER if d == "Sun" else PRIMARY2 if d in ["Mon","Thu"] else NEUTRAL
                 for d in days_df["day"]]
        fig4.add_trace(go.Bar(
            x=days_df["day"], y=days_df["count"],
            marker=dict(color=day_c, line=dict(width=0), cornerradius=4),
            name="Appointments",
            text=days_df["count"].apply(lambda v: f"{v:,}"),
            textposition="outside",
            textfont=dict(size=10, color="#64748b")
        ), secondary_y=False)
        fig4.add_trace(go.Scatter(
            x=days_df["day"], y=days_df["noshow_rate"],
            mode="lines+markers",
            name="No-Show %",
            line=dict(color=WARNING, width=2, dash="dot"),
            marker=dict(size=6, color=WARNING, line=dict(color="#0c1220", width=1.5))
        ), secondary_y=True)
        fig4.update_layout(
            paper_bgcolor=PBG, plot_bgcolor=PBG,
            height=320, margin=dict(l=8, r=8, t=30, b=8),
            bargap=0.3, showlegend=True,
            legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0, font=dict(size=11, color="#64748b")),
            font=dict(family="Inter", color="#64748b", size=11),
            xaxis=dict(gridcolor=PGRD, linecolor="rgba(76,201,240,0.08)", tickfont=dict(size=11, color="#475569")),
            yaxis=dict(gridcolor=PGRD, linecolor="rgba(0,0,0,0)", tickfont=dict(size=11, color="#475569")),
            yaxis2=dict(tickfont=dict(size=11, color=WARNING), showgrid=False)
        )
        st.plotly_chart(fig4, use_container_width=True)

    # ── Row 3: Outcome breakdown (stacked area) ──
    st.markdown(sec("Monthly Outcome Breakdown", "Completion · No-Show · Cancelled (%)"),
                unsafe_allow_html=True)
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=mdf["month"], y=mdf["completed"],
        mode="lines", line=dict(color=SUCCESS, width=0),
        fill="tozeroy", fillcolor="rgba(34,197,94,0.14)",
        name="Completed %", stackgroup="one"
    ))
    fig5.add_trace(go.Scatter(
        x=mdf["month"], y=mdf["noshow"],
        mode="lines", line=dict(color=WARNING, width=0),
        fill="tonexty", fillcolor="rgba(245,158,11,0.16)",
        name="No-Show %", stackgroup="one"
    ))
    fig5.add_trace(go.Scatter(
        x=mdf["month"], y=mdf["cancelled"],
        mode="lines", line=dict(color=DANGER, width=0),
        fill="tonexty", fillcolor="rgba(239,68,68,0.12)",
        name="Cancelled %", stackgroup="one"
    ))
    fig5.add_hline(
        y=18.8, line_dash="dot", line_color=WARNING,
        annotation_text="Avg No-Show 18.8%",
        annotation_font=dict(color=WARNING, size=10),
        annotation_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(sfig(fig5, h=260, legend=True), use_container_width=True)

    # ── Row 4: Satisfaction + City no-show ──
    r4a, r4b = st.columns(2)
    with r4a:
        st.markdown(sec("Patient Satisfaction by City", "Rating out of 5.0"), unsafe_allow_html=True)
        # Semantic: green=high score, amber=mid, red=low — meaningful conditional coloring
        sat_colors = [
            SUCCESS if v >= 4.3 else WARNING if v >= 4.0 else DANGER
            for v in city_df["satisfaction"]
        ]
        fig_s = go.Figure(go.Bar(
            x=city_df["city"], y=city_df["satisfaction"],
            marker=dict(color=sat_colors, line=dict(width=0), cornerradius=5),
            text=[f"{v}" for v in city_df["satisfaction"]],
            textposition="outside", textfont=dict(size=12, color="#64748b")
        ))
        fig_s.update_layout(yaxis_range=[3.5, 5])
        st.plotly_chart(sfig(fig_s, h=260), use_container_width=True)

    with r4b:
        st.markdown(sec("No-Show Rate by City", "vs network avg 18.8%"), unsafe_allow_html=True)
        # Semantic conditional: red=high, amber=mid, green=low
        clr_ns = [DANGER if v > 19.5 else WARNING if v > 18.5 else SUCCESS for v in city_df["noshow"]]
        fig_n = go.Figure(go.Bar(
            x=city_df["noshow"], y=city_df["city"],
            orientation="h",
            marker=dict(color=clr_ns, line=dict(width=0), cornerradius=4),
            text=[f"{v}%" for v in city_df["noshow"]],
            textposition="outside", textfont=dict(size=11, color="#64748b")
        ))
        fig_n.add_vline(
            x=18.8, line_dash="dot", line_color="#334d66",
            annotation_text="Avg 18.8%",
            annotation_font=dict(color="#475569", size=11)
        )
        st.plotly_chart(sfig(fig_n, h=260), use_container_width=True)


# ══════════════════════════════════════════════
# TAB 2 — DEPARTMENTS
# ══════════════════════════════════════════════
with tab2:

    sl_sel = st.multiselect(
        "Select Departments", DEPTS,
        default=DEPTS, key="sl2",
        format_func=lambda x: f"{dept_emoji(x)} {dept_label(x)}"
    )
    if not sl_sel:
        sl_sel = DEPTS
    dv = dept_df[dept_df["dept"].isin(sl_sel)].copy()

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # Department summary cards
    dc = st.columns(len(sl_sel))
    for i, dept in enumerate(sl_sel):
        c      = dept_color(dept)
        icon   = dept_emoji(dept)
        dlabel = dept_label(dept)
        row    = dept_df[dept_df["dept"] == dept].iloc[0]
        ns_c   = DANGER if row["noshow"] > 20 else WARNING if row["noshow"] > 18 else SUCCESS
        with dc[i]:
            st.markdown(f"""
            <div style="background:#131e2e;border:1px solid rgba(76,201,240,0.08);
                 border-top:2px solid {c};border-radius:12px;padding:18px 12px;text-align:center;
                 box-shadow:0 4px 20px rgba(0,0,0,0.3);
                 transition:border-color 0.2s,box-shadow 0.2s">
                <div style="font-size:26px;margin-bottom:10px">{icon}</div>
                <div style="font-size:11px;font-weight:700;color:{c};margin-bottom:6px;
                     letter-spacing:0.2px">{dlabel}</div>
                <div style="font-size:20px;font-weight:800;color:#f1f5f9;letter-spacing:-0.4px">
                    ₨{row["revenue"]}M
                </div>
                <div style="font-size:10px;color:#334155;margin-top:3px;font-weight:500">
                    {row["appts"]:,} appointments
                </div>
                <div style="margin-top:11px;background:{ns_c}12;color:{ns_c};
                     border:1px solid {ns_c}28;border-radius:6px;padding:4px 8px;
                     font-size:11px;font-weight:700">
                    No-Show: {row["noshow"]}%
                </div>
                <div style="margin-top:5px;font-size:10px;color:#334155;font-weight:400">
                    avg wait {row["avg_wait"]} min
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(sec("Revenue by Department", "PKR millions"), unsafe_allow_html=True)
        # Single primary color — highlight top earner
        max_rev = dv["revenue"].max()
        rev_colors = [PRIMARY if v == max_rev else NEUTRAL for v in dv["revenue"]]
        fig = go.Figure(go.Bar(
            x=[dept_label(d) for d in dv["dept"]],
            y=dv["revenue"],
            marker=dict(color=rev_colors, line=dict(width=0), cornerradius=5),
            text=[f"₨{v}M" for v in dv["revenue"]],
            textposition="outside", textfont=dict(size=11, color="#64748b")
        ))
        fig.update_layout(bargap=0.35)
        st.plotly_chart(sfig(fig), use_container_width=True)

    with c2:
        st.markdown(sec("No-Show Rate by Department"), unsafe_allow_html=True)
        # Semantic conditional color — meaningful
        bc = [DANGER if v > 20 else WARNING if v > 18 else SUCCESS for v in dv["noshow"]]
        fig2 = go.Figure(go.Bar(
            x=dv["noshow"],
            y=[dept_label(d) for d in dv["dept"]],
            orientation="h",
            marker=dict(color=bc, line=dict(width=0), cornerradius=4),
            text=[f"{v}%" for v in dv["noshow"]],
            textposition="outside", textfont=dict(size=12, color="#64748b")
        ))
        fig2.add_vline(
            x=18.8, line_dash="dot", line_color="#334d66",
            annotation_text="Avg 18.8%",
            annotation_font=dict(color="#475569", size=10)
        )
        fig2.update_layout(bargap=0.32)
        st.plotly_chart(sfig(fig2), use_container_width=True)

    p1, p2 = st.columns(2)

    with p1:
        st.markdown(sec("Appointment Share by Department"), unsafe_allow_html=True)
        # Muted monochromatic family — not rainbow
        pie_colors = [
            "rgba(76,201,240,0.9)",
            "rgba(56,163,196,0.85)",
            "rgba(14,116,144,0.8)",
            "rgba(110,231,183,0.85)",
            "rgba(167,139,250,0.8)",
        ]
        fig_p = go.Figure(go.Pie(
            labels=[dept_label(d) for d in dv["dept"]],
            values=dv["appts"], hole=0.54,
            marker=dict(
                colors=pie_colors[:len(dv)],
                line=dict(color="#0c1220", width=2.5)
            ),
            textfont=dict(size=11, color="#e2e8f0")
        ))
        fig_p.update_layout(
            paper_bgcolor=PBG, plot_bgcolor=PBG, height=290,
            margin=dict(l=4, r=4, t=28, b=4), showlegend=True,
            font=dict(color="#64748b", family="Inter"),
            legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0, font=dict(size=11, color="#94a3b8")),
            annotations=[dict(
                text="<b>Appts</b>", x=0.5, y=0.5,
                font=dict(size=12, color="#94a3b8"), showarrow=False
            )]
        )
        st.plotly_chart(fig_p, use_container_width=True)

    with p2:
        st.markdown(sec("Satisfaction by Department", "Rating out of 5.0"), unsafe_allow_html=True)
        sat_v = dept_df[dept_df["dept"].isin(sl_sel)]
        # Semantic conditional
        sat_clr = [
            SUCCESS if v >= 4.2 else WARNING if v >= 4.0 else DANGER
            for v in sat_v["satisfaction"]
        ]
        fig_s2 = go.Figure(go.Bar(
            x=[dept_label(d) for d in sat_v["dept"]],
            y=sat_v["satisfaction"],
            marker=dict(color=sat_clr, line=dict(width=0), cornerradius=5),
            text=[f"{v}" for v in sat_v["satisfaction"]],
            textposition="outside", textfont=dict(size=11, color="#64748b")
        ))
        fig_s2.update_layout(yaxis_range=[3, 5], bargap=0.35)
        st.plotly_chart(sfig(fig_s2, h=290), use_container_width=True)

    # Bubble chart — size=appointments, color=severity
    st.markdown(sec("Appointments vs No-Show Rate", "Bubble size = Revenue · Color = risk level"),
                unsafe_allow_html=True)
    bubble_colors = [
        DANGER if ns > 20 else WARNING if ns > 18 else SUCCESS
        for ns in dv["noshow"]
    ]
    fig_b = go.Figure()
    for idx, (_, row) in enumerate(dv.iterrows()):
        c = DANGER if row["noshow"] > 20 else WARNING if row["noshow"] > 18 else SUCCESS
        fig_b.add_trace(go.Scatter(
            x=[row["appts"]], y=[row["noshow"]],
            mode="markers+text",
            text=[dept_label(row["dept"])],
            textposition="top center",
            textfont=dict(size=11, color="#94a3b8"),
            marker=dict(
                size=row["revenue"] * 7,
                color=c,
                opacity=0.75,
                line=dict(color=c, width=1.5)
            ),
            name=dept_label(row["dept"]),
            showlegend=False
        ))
    fig_b.update_layout(
        xaxis_title="Appointments",
        yaxis_title="No-Show Rate (%)"
    )
    st.plotly_chart(sfig(fig_b, h=320), use_container_width=True)

    # Heatmap — smooth gradient
    st.markdown(sec("No-Show Heatmap", "City × Department (%)"), unsafe_allow_html=True)
    np.random.seed(99)
    hm = np.round(np.random.uniform(15, 25, (len(CITIES), len(sl_sel))), 1)
    fig_h = go.Figure(go.Heatmap(
        z=hm,
        x=[dept_label(d) for d in sl_sel],
        y=CITIES,
        # Smooth gradient: low=green, mid=amber, high=red
        colorscale=[
            [0.0,  "rgba(34,197,94,0.6)"],
            [0.4,  "rgba(34,197,94,0.3)"],
            [0.55, "rgba(245,158,11,0.6)"],
            [0.75, "rgba(245,158,11,0.8)"],
            [1.0,  "rgba(239,68,68,0.9)"],
        ],
        text=hm, texttemplate="%{text}%",
        textfont=dict(color="#f1f5f9", size=12, family="Inter"),
        showscale=True,
        colorbar=dict(
            tickfont=dict(color="#64748b", family="Inter"),
            outlinewidth=0,
            ticksuffix="%"
        ),
        zmin=14, zmax=26
    ))
    st.plotly_chart(sfig(fig_h, h=270), use_container_width=True)


# ══════════════════════════════════════════════
# TAB 3 — MEDICAL STAFF
# ══════════════════════════════════════════════
with tab3:

    f1, f2, f3 = st.columns([2.5, 2, 2])
    with f1:
        srch = st.text_input(
            "Search by name",
            placeholder="e.g. Sara, Ahmed, Fatima…",
            key="doc_search"
        )
    with f2:
        dept_f = st.selectbox(
            "Department",
            ["All Departments"] + DEPTS,
            key="doc_dept",
            format_func=lambda x: x if x == "All Departments" else f"{dept_emoji(x)} {dept_label(x)}"
        )
    with f3:
        sort_s = st.selectbox("Sort By", [
            "No-Show % — High to Low",
            "No-Show % — Low to High",
            "Appointments — High to Low",
            "Revenue — High to Low",
        ], key="doc_sort")

    fdf = doc_df.copy()
    if srch and srch.strip():
        fdf = fdf[fdf["Doctor"].str.contains(srch.strip(), case=False, na=False)]
    if dept_f != "All Departments":
        fdf = fdf[fdf["Department"] == dept_f]

    sm = {
        "No-Show % — High to Low":    ("No-Show %",    False),
        "No-Show % — Low to High":    ("No-Show %",    True),
        "Appointments — High to Low": ("Appointments", False),
        "Revenue — High to Low":      ("Revenue",      False),
    }
    sc, asc = sm[sort_s]
    fdf = fdf.sort_values(sc, ascending=asc).reset_index(drop=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if fdf.empty:
        st.markdown("""
        <div style="background:#131e2e;border:1px solid rgba(76,201,240,0.08);border-radius:12px;
             padding:60px;text-align:center">
            <div style="font-size:32px;margin-bottom:12px">◎</div>
            <div style="font-size:15px;font-weight:700;color:#f1f5f9">No staff members match your search</div>
            <div style="font-size:12px;color:#334155;margin-top:6px">Try a different name or department</div>
        </div>""", unsafe_allow_html=True)
    else:
        # Summary metrics
        sm1, sm2, sm3, sm4 = st.columns(4)
        sm1.metric("Staff Shown",       str(len(fdf)))
        sm2.metric("Avg No-Show %",     f"{fdf['No-Show %'].mean():.1f}%")
        sm3.metric("Avg Appointments",  f"{int(fdf['Appointments'].mean()):,}")
        sm4.metric("Highest No-Show",   f"{fdf['No-Show %'].max()}%")

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        top_worst = fdf.nlargest(3, "No-Show %")
        top_best  = fdf.nsmallest(3, "No-Show %")

        pc1, pc2 = st.columns(2)

        with pc1:
            st.markdown(sec("High Risk — Needs Attention"), unsafe_allow_html=True)
            for _, row in top_worst.iterrows():
                c    = DANGER if row["No-Show %"] > 30 else WARNING
                bg   = "rgba(239,68,68,0.05)" if row["No-Show %"] > 30 else "rgba(245,158,11,0.05)"
                bdr  = "rgba(239,68,68,0.18)" if row["No-Show %"] > 30 else "rgba(245,158,11,0.18)"
                icon = dept_emoji(row["Department"])
                pct  = int(min(row["No-Show %"] / 40 * 100, 100))
                dlbl = dept_label(row["Department"])
                st.markdown(f"""
                <div style="background:#131e2e;border:1px solid {bdr};border-left:3px solid {c};
                     border-radius:10px;padding:14px 16px;margin-bottom:8px">
                    <div style="display:flex;align-items:center;justify-content:space-between">
                        <div style="display:flex;align-items:center;gap:12px;flex:1">
                            <div style="background:{c}10;width:38px;height:38px;border-radius:9px;
                                 display:flex;align-items:center;justify-content:center;font-size:18px;
                                 border:1px solid {c}20;flex-shrink:0">{icon}</div>
                            <div style="flex:1">
                                <div style="font-size:13px;font-weight:600;color:#e2e8f0">{row["Doctor"]}</div>
                                <div style="font-size:11px;color:#334155;margin-top:2px">
                                    {dlbl} · {row["Seniority"]} · {row["Appointments"]} appts
                                </div>
                                <div style="background:#1e2d42;border-radius:3px;height:3px;margin-top:8px">
                                    <div style="width:{pct}%;height:100%;background:{c};border-radius:3px"></div>
                                </div>
                            </div>
                        </div>
                        <div style="text-align:right;margin-left:14px;flex-shrink:0">
                            <div style="font-size:22px;font-weight:800;color:{c};letter-spacing:-0.5px">
                                {row["No-Show %"]}%
                            </div>
                            <div style="background:{c}12;color:{c};border-radius:5px;padding:2px 8px;
                                 font-size:10px;font-weight:700;display:inline-block;margin-top:4px">
                                Review Needed
                            </div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

        with pc2:
            st.markdown(sec("High Reliability — Top Performers"), unsafe_allow_html=True)
            for _, row in top_best.iterrows():
                icon = dept_emoji(row["Department"])
                pct  = int(min(row["No-Show %"] / 40 * 100, 100))
                dlbl = dept_label(row["Department"])
                st.markdown(f"""
                <div style="background:#131e2e;border:1px solid rgba(34,197,94,0.16);
                     border-left:3px solid {SUCCESS};border-radius:10px;padding:14px 16px;margin-bottom:8px">
                    <div style="display:flex;align-items:center;justify-content:space-between">
                        <div style="display:flex;align-items:center;gap:12px;flex:1">
                            <div style="background:rgba(34,197,94,0.08);width:38px;height:38px;border-radius:9px;
                                 display:flex;align-items:center;justify-content:center;font-size:18px;
                                 border:1px solid rgba(34,197,94,0.18);flex-shrink:0">{icon}</div>
                            <div style="flex:1">
                                <div style="font-size:13px;font-weight:600;color:#e2e8f0">{row["Doctor"]}</div>
                                <div style="font-size:11px;color:#334155;margin-top:2px">
                                    {dlbl} · {row["Seniority"]} · {row["Appointments"]} appts
                                </div>
                                <div style="background:#1e2d42;border-radius:3px;height:3px;margin-top:8px">
                                    <div style="width:{pct}%;height:100%;background:{SUCCESS};border-radius:3px"></div>
                                </div>
                            </div>
                        </div>
                        <div style="text-align:right;margin-left:14px;flex-shrink:0">
                            <div style="font-size:22px;font-weight:800;color:{SUCCESS};letter-spacing:-0.5px">
                                {row["No-Show %"]}%
                            </div>
                            <div style="background:rgba(34,197,94,0.1);color:{SUCCESS};border-radius:5px;
                                 padding:2px 8px;font-size:10px;font-weight:700;display:inline-block;margin-top:4px">
                                Reliable
                            </div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

        ch1, ch2 = st.columns(2)

        with ch1:
            st.markdown(sec("No-Show Rate by Staff Member"), unsafe_allow_html=True)
            # Semantic conditional only — not random colors per bar
            bc2 = [DANGER if v > 30 else WARNING if v > 25 else PRIMARY for v in fdf["No-Show %"]]
            fig = go.Figure(go.Bar(
                x=fdf["Doctor"].str.split("Dr.").str[-1].str.strip(),
                y=fdf["No-Show %"],
                marker=dict(color=bc2, line=dict(width=0), cornerradius=4),
                text=[f"{v}%" for v in fdf["No-Show %"]],
                textposition="outside", textfont=dict(size=11, color="#64748b")
            ))
            fig.update_layout(bargap=0.3, xaxis_tickangle=-30)
            st.plotly_chart(sfig(fig, h=300), use_container_width=True)

        with ch2:
            st.markdown(sec("Appointments vs No-Show", "Bubble size = Revenue · Color = risk"),
                        unsafe_allow_html=True)
            # Color by severity, not by department rainbow
            fig2 = go.Figure()
            for _, row in fdf.iterrows():
                c = DANGER if row["No-Show %"] > 30 else WARNING if row["No-Show %"] > 25 else SUCCESS
                fig2.add_trace(go.Scatter(
                    x=[row["Appointments"]], y=[row["No-Show %"]],
                    mode="markers",
                    marker=dict(
                        size=row["Revenue"] * 28,
                        color=c, opacity=0.7,
                        line=dict(color=c, width=1)
                    ),
                    text=row["Doctor"],
                    hoverinfo="text+x+y",
                    showlegend=False
                ))
            st.plotly_chart(sfig(fig2, h=300), use_container_width=True)

        # Full table
        st.markdown(sec("Staff Performance Table"), unsafe_allow_html=True)
        TH = ("padding:10px 14px;text-align:left;font-size:9px;text-transform:uppercase;"
              "letter-spacing:1.5px;color:#334155;font-weight:700;border-bottom:1px solid rgba(76,201,240,0.08);"
              "background:#0f1a2c")

        tbl = (f'<div style="background:#131e2e;border:1px solid rgba(76,201,240,0.08);border-radius:12px;'
               f'overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.3)">'
               f'<table style="width:100%;border-collapse:collapse;font-size:12px">'
               f'<thead><tr>'
               f'<th style="{TH}">#</th>'
               f'<th style="{TH}">Name</th>'
               f'<th style="{TH}">Department</th>'
               f'<th style="{TH}">Level</th>'
               f'<th style="{TH};text-align:right">Appts</th>'
               f'<th style="{TH};text-align:right">Revenue</th>'
               f'<th style="{TH};text-align:right">No-Show %</th>'
               f'<th style="{TH};text-align:center">Risk</th>'
               f'</tr></thead><tbody>')

        for i, (_, row) in enumerate(fdf.iterrows()):
            rc   = DANGER if i == 0 else WARNING if i == 1 else "#334d66"
            c    = ns_color(row["No-Show %"])
            dc   = dept_color(row["Department"])
            dlbl = dept_label(row["Department"])
            demj = dept_emoji(row["Department"])
            bw   = int(min(row["No-Show %"] / 40, 1.0) * 60)
            bg   = "#0f1a2c" if i % 2 == 0 else "#131e2e"
            tbl += (f'<tr style="background:{bg};border-bottom:1px solid rgba(76,201,240,0.05)">'
                    f'<td style="padding:10px 14px;color:{rc};font-weight:700">#{i+1}</td>'
                    f'<td style="padding:10px 14px;font-weight:600;color:#e2e8f0">{row["Doctor"]}</td>'
                    f'<td style="padding:10px 14px">'
                    f'<span style="background:{dc}14;color:{dc};border-radius:5px;padding:2px 8px;'
                    f'font-size:10px;font-weight:700;border:1px solid {dc}28">'
                    f'{demj} {dlbl}</span></td>'
                    f'<td style="padding:10px 14px;color:#475569;font-weight:400">{row["Seniority"]}</td>'
                    f'<td style="padding:10px 14px;text-align:right;font-family:monospace;'
                    f'color:#94a3b8;font-weight:500">{row["Appointments"]}</td>'
                    f'<td style="padding:10px 14px;text-align:right;font-family:monospace;'
                    f'color:{SUCCESS};font-weight:500">₨{row["Revenue"]}M</td>'
                    f'<td style="padding:10px 14px;text-align:right;white-space:nowrap">'
                    f'<span style="font-weight:700;font-size:14px;color:{c}">{row["No-Show %"]}%</span>'
                    f'<div style="background:#1e2d42;border-radius:3px;height:3px;width:60px;'
                    f'margin-top:5px;display:inline-block;vertical-align:middle;margin-left:8px">'
                    f'<div style="width:{bw}px;height:100%;background:{c};border-radius:3px"></div>'
                    f'</div></td>'
                    f'<td style="padding:10px 14px;text-align:center">{risk_tag(row["No-Show %"])}</td>'
                    f'</tr>')

        tbl += "</tbody></table></div>"
        st.markdown(tbl, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 — PATIENT RELIABILITY
# ══════════════════════════════════════════════
with tab4:

    BASE  = {"General":17.2,"Cardiology":22.0,"Orthopedics":17.0,"Dermatology":23.2,"Pediatrics":17.4}
    C_MOD = {"Karachi":1.05,"Lahore":0.95,"Islamabad":1.02,"Peshawar":1.08,"Multan":0.98}
    D_MOD = {"Mon":1.05,"Tue":1.0,"Wed":1.02,"Thu":0.98,"Fri":1.10,"Sat":0.90,"Sun":1.30}
    P_MOD = {"New Patient":1.20,"Returning":0.85}
    V_MOD = {"First Visit":1.25,"Follow-up":0.90,"Referral":1.10}

    st.markdown(f"""
    <div style="background:rgba(76,201,240,0.05);border:1px solid rgba(76,201,240,0.12);
         border-left:3px solid {PRIMARY};border-radius:10px;padding:13px 18px;margin-bottom:22px;
         display:flex;align-items:center;gap:12px">
        <span style="font-size:16px;flex-shrink:0">◎</span>
        <div style="font-size:12.5px;color:#64748b;font-weight:500">
            <b style="color:{PRIMARY}">Patient Reliability Predictor</b> — Configure appointment parameters
            to get an instant no-show probability estimate with recommended actions.
            All inputs update results in real time.
        </div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown(f"""
        <div style="background:#131e2e;border:1px solid rgba(76,201,240,0.1);border-radius:14px;
             border-top:2px solid {PRIMARY};padding:20px 20px 8px;
             box-shadow:0 4px 20px rgba(0,0,0,0.3)">
            <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:3px">
                Appointment Parameters
            </div>
            <div style="font-size:11px;color:#334155;margin-bottom:18px">
                All fields update the prediction in real time
            </div>
        </div>
        """, unsafe_allow_html=True)

        p_dept = st.selectbox(
            "Department",
            DEPTS, key="p_dept",
            format_func=lambda x: f"{dept_emoji(x)} {dept_label(x)}"
        )
        p_city  = st.selectbox("City", CITIES, key="p_city")
        p_day   = st.selectbox("Day of Week", ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], key="p_day")
        p_pt    = st.radio("Patient Type", ["New Patient","Returning"], horizontal=True, key="p_pt")
        p_visit = st.radio("Visit Type", ["First Visit","Follow-up","Referral"], horizontal=True, key="p_visit")
        p_adj   = st.slider("Manual Adjustment (%)", -10, 10, 0, key="p_adj")

        # Reference tiles
        dept_base = BASE[p_dept]
        city_rate = round(city_df[city_df["city"] == p_city]["noshow"].values[0], 1)
        d_label   = dept_label(p_dept)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        bt1, bt2, bt3 = st.columns(3)
        for c_col, lbl, val, color, bg in [
            (bt1, d_label,    f"{dept_base}%",        PRIMARY, "rgba(76,201,240,0.06)"),
            (bt2, p_city,     f"{city_rate}%",         SUCCESS, "rgba(34,197,94,0.06)"),
            (bt3, p_day,      f"×{D_MOD[p_day]}",      WARNING, "rgba(245,158,11,0.06)"),
        ]:
            c_col.markdown(f"""
            <div style="background:{bg};border:1px solid {color}18;border-radius:9px;
                 padding:12px 8px;text-align:center">
                <div style="font-size:9px;color:{color};font-weight:700;text-transform:uppercase;
                     letter-spacing:0.9px;margin-bottom:4px">{lbl}</div>
                <div style="font-size:20px;font-weight:800;color:{color};letter-spacing:-0.5px">{val}</div>
            </div>""", unsafe_allow_html=True)

    with right:
        prob = (BASE[p_dept] * C_MOD[p_city] * D_MOD[p_day]
                * P_MOD[p_pt] * V_MOD[p_visit])
        prob = max(min(round(prob + p_adj, 1), 99.0), 1.0)

        if prob < 20:
            rlbl, rc, rbg, rbdr = "Low Risk",    SUCCESS, "rgba(34,197,94,0.06)",  "rgba(34,197,94,0.2)"
            recs     = ["Send standard SMS reminder","No additional action needed","Standard scheduling applies"]
            rec_icon = "◈"
        elif prob < 28:
            rlbl, rc, rbg, rbdr = "Medium Risk", WARNING, "rgba(245,158,11,0.06)", "rgba(245,158,11,0.2)"
            recs     = ["Send WhatsApp reminder 24h before","Avoid overbooking this slot","Follow up if unconfirmed"]
            rec_icon = "◉"
        else:
            rlbl, rc, rbg, rbdr = "High Risk",   DANGER,  "rgba(239,68,68,0.06)",  "rgba(239,68,68,0.2)"
            recs     = ["Call patient directly to confirm","Consider double-booking","Alert scheduling coordinator"]
            rec_icon = "◎"

        # Gauge chart — single-color, semantic
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob,
            number={"suffix": "%", "font": {"size": 52, "family": "Inter", "color": rc}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "#334155",
                    "tickfont": {"size": 10, "color": "#334155"}
                },
                "bar":        {"color": rc, "thickness": 0.26},
                "bgcolor":    "#0f1a2c",
                "borderwidth": 0,
                "steps": [
                    {"range": [0,   20],  "color": "rgba(34,197,94,0.08)"},
                    {"range": [20,  28],  "color": "rgba(245,158,11,0.08)"},
                    {"range": [28, 100],  "color": "rgba(239,68,68,0.08)"},
                ],
                "threshold": {
                    "line":      {"color": rc, "width": 2},
                    "thickness": 0.75,
                    "value":     prob
                }
            }
        ))
        gauge_fig.update_layout(
            paper_bgcolor="#131e2e",
            font=dict(color="#475569", family="Inter"),
            height=240,
            margin=dict(l=20, r=20, t=16, b=8)
        )

        st.markdown(f"""
        <div style="background:#131e2e;border:1px solid {rbdr};border-radius:14px;
             border-top:2px solid {rc};padding:22px 22px 18px;
             box-shadow:0 8px 32px rgba(0,0,0,0.4)">
            <div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:1.6px;
                 color:#334155;text-align:center;margin-bottom:8px">
                Estimated No-Show Probability
            </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(gauge_fig, use_container_width=True)

        pct_bar = int((prob / 100) * 100)
        st.markdown(f"""
            <div style="display:flex;justify-content:center;margin:-6px 0 16px">
                <div style="background:{rbg};color:{rc};border:1px solid {rbdr};border-radius:7px;
                     padding:6px 22px;font-size:13px;font-weight:700;letter-spacing:0.2px">
                    {rec_icon} {rlbl}
                </div>
            </div>

            <div style="background:#1e2d42;border-radius:6px;height:8px;margin-bottom:6px;overflow:hidden">
                <div style="width:{pct_bar}%;height:100%;background:{rc};border-radius:6px"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:9px;
                 color:#1e3a5f;font-weight:600;margin-bottom:18px">
                <span>0%</span><span>20% Low</span><span>28% Med</span><span>100%</span>
            </div>

            <div style="background:{rbg};border:1px solid {rbdr};border-radius:9px;padding:14px 16px">
                <div style="font-size:9px;font-weight:700;color:{rc};text-transform:uppercase;
                     letter-spacing:1.2px;margin-bottom:10px">Recommended Actions</div>
        """, unsafe_allow_html=True)

        for r_item in recs:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
                <div style="width:5px;height:5px;background:{rc};border-radius:50%;flex-shrink:0"></div>
                <span style="font-size:12px;color:#64748b;font-weight:500">{r_item}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        # Contributing factors
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:9px;font-weight:700;color:#1e3a5f;text-transform:uppercase;'
            'letter-spacing:1.5px;margin-bottom:10px">Contributing Factors</div>',
            unsafe_allow_html=True
        )

        f1c, f2c, f3c, f4c, f5c = st.columns(5)
        factors = [
            ("Dept",   d_label,   f"{dept_base}% base",           PRIMARY),
            ("City",   p_city,    f"×{C_MOD[p_city]}",            SUCCESS),
            ("Day",    p_day,     f"×{D_MOD[p_day]}",             WARNING),
            ("Type",   "New" if "New" in p_pt else "Return",
                       "+20%" if "New" in p_pt else "−15%",        DANGER),
            ("Visit",  p_visit.split()[0],
                       f"×{V_MOD[p_visit]}",                       PRIMARY2),
        ]
        for col, (label, val, eff, color) in zip([f1c, f2c, f3c, f4c, f5c], factors):
            col.markdown(f"""
            <div style="background:#0f1a2c;border:1px solid rgba(76,201,240,0.08);
                 border-top:2px solid {color};border-radius:9px;padding:10px 6px;text-align:center">
                <div style="font-size:9px;color:{color};text-transform:uppercase;letter-spacing:0.9px;
                     font-weight:700;margin-bottom:4px">{label}</div>
                <div style="font-size:11px;font-weight:700;color:#94a3b8;margin-top:2px">{val}</div>
                <div style="font-size:10px;color:#334155;margin-top:1px;font-weight:400">{eff}</div>
            </div>""", unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:18px;border-top:1px solid rgba(76,201,240,0.06)">
    <span style="font-size:10px;color:#1e3a5f;font-weight:600;letter-spacing:1.5px;text-transform:uppercase">
        MediTrack Analytics · Pakistan Private Healthcare Network · FY 2024
    </span>
</div>
""", unsafe_allow_html=True)
