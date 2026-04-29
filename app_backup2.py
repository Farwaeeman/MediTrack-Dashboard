import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediTrack Pro",
    layout="wide",
    page_icon="🩺",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark background */
.stApp {
    background-color: #080c14;
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0d1424 !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * {
    color: #94a3b8 !important;
}
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #e2e8f0 !important;
}

/* Main content padding */
.block-container {
    padding: 1.5rem 2rem 2rem 2rem !important;
    max-width: 100% !important;
}

/* KPI Cards */
[data-testid="metric-container"] {
    background: #0d1424;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem 1.2rem !important;
}
[data-testid="metric-container"] label {
    color: #475569 !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e2e8f0 !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 12px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: #0d1424;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    gap: 4px;
    padding: 0 4px;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    border-radius: 8px 8px 0 0 !important;
    color: #475569 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(99,102,241,0.12) !important;
    color: #a5b4fc !important;
    border-bottom: 2px solid #6366f1 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1rem !important;
}

/* Selectbox / multiselect */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background-color: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* Radio */
.stRadio > div {
    gap: 8px;
}
.stRadio label {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 8px 14px !important;
    color: #94a3b8 !important;
    font-size: 13px !important;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.06) !important;
}

/* Dataframe */
.stDataFrame {
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
}

/* Checkbox */
.stCheckbox label {
    color: #94a3b8 !important;
    font-size: 13px !important;
}

/* Caption */
.stCaption {
    color: #334155 !important;
    font-size: 11px !important;
}

/* Headings */
h1 { color: #f1f5f9 !important; font-weight: 800 !important; letter-spacing: -1px !important; }
h2 { color: #e2e8f0 !important; font-weight: 700 !important; }
h3 { color: #cbd5e1 !important; font-weight: 600 !important; }

/* Section headers */
.section-header {
    font-size: 13px;
    font-weight: 600;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 12px;
    margin-top: 4px;
}

/* KPI accent borders */
.kpi-blue  { border-top: 2px solid #6366f1 !important; }
.kpi-green { border-top: 2px solid #10b981 !important; }
.kpi-amber { border-top: 2px solid #f59e0b !important; }
.kpi-red   { border-top: 2px solid #ef4444 !important; }

/* Risk badge */
.risk-high { background: rgba(239,68,68,0.12); border: 1px solid rgba(239,68,68,0.3); color: #f87171; padding: 10px 14px; border-radius: 8px; font-size: 13px; font-weight: 500; }
.risk-med  { background: rgba(245,158,11,0.12); border: 1px solid rgba(245,158,11,0.3); color: #fbbf24; padding: 10px 14px; border-radius: 8px; font-size: 13px; font-weight: 500; }
.risk-low  { background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.3); color: #34d399; padding: 10px 14px; border-radius: 8px; font-size: 13px; font-weight: 500; }

/* Info box */
.info-box {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 13px;
    color: #a5b4fc;
    margin-bottom: 12px;
}

/* Factor card */
.factor-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 12px 14px;
    font-size: 13px;
}
.factor-label { color: #334155; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.factor-val   { color: #e2e8f0; font-weight: 600; margin-bottom: 2px; }
.factor-note  { color: #64748b; font-size: 11px; }
</style>
""", unsafe_allow_html=True)

# ── PLOTLY THEME ──────────────────────────────────────────────────────────────
PLOT_BG   = "#0d1424"
PAPER_BG  = "#0d1424"
GRID_COL  = "rgba(255,255,255,0.04)"
TICK_COL  = "#475569"
FONT_FAM  = "Inter, system-ui, sans-serif"
DEPT_COLORS = {
    "Cardiology":  "#3b82f6",
    "Dermatology": "#a855f7",
    "General":     "#10b981",
    "Orthopedics": "#f59e0b",
    "Pediatrics":  "#ec4899",
}

def apply_theme(fig, height=320):
    fig.update_layout(
        height=height,
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(family=FONT_FAM, color=TICK_COL, size=12),
        margin=dict(l=10, r=10, t=36, b=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(255,255,255,0.06)",
            font=dict(color="#94a3b8", size=11)
        ),
        title_font=dict(color="#e2e8f0", size=14, family=FONT_FAM),
        xaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL), linecolor="rgba(0,0,0,0)", zeroline=False),
        yaxis=dict(gridcolor=GRID_COL, tickfont=dict(color=TICK_COL), linecolor="rgba(0,0,0,0)", zeroline=False),
    )
    return fig

# ── DATA ──────────────────────────────────────────────────────────────────────
DEPARTMENTS = ["General", "Cardiology", "Orthopedics", "Dermatology", "Pediatrics"]
CITIES      = ["Karachi", "Lahore", "Islamabad", "Peshawar", "Multan"]
DAY_ORDER   = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

@st.cache_data
def load_data():
    conn = sqlite3.connect('/home/farwa-eeman/Desktop/MediTrack/meditrack.db')
    appointments = pd.read_sql("SELECT * FROM appointments", conn)
    doctors      = pd.read_sql("SELECT * FROM doctors", conn)
    conn.close()

    appointments['appointment_date'] = pd.to_datetime(appointments['appointment_date'])
    appointments['month']   = appointments['appointment_date'].dt.strftime('%b %Y')
    appointments['weekday'] = appointments['appointment_date'].dt.day_name()
    appointments['revenue'] = appointments['consultation_fee']
    appointments['year_month'] = appointments['appointment_date'].dt.to_period('M').astype(str)
    return appointments, doctors

df, doctors_df = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='display:flex;align-items:center;gap:10px;padding:4px 0 20px 0'>
        <div style='width:36px;height:36px;border-radius:9px;background:linear-gradient(135deg,#6366f1,#3b82f6);
                    display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;color:#fff'>M+</div>
        <div>
            <div style='font-size:15px;font-weight:700;color:#f1f5f9;letter-spacing:-0.4px'>MediTrack</div>
            <div style='font-size:10px;color:#334155;text-transform:uppercase;letter-spacing:1px'>Analytics Pro</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Filters</div>", unsafe_allow_html=True)
    selected_cities = st.multiselect("Cities", options=CITIES, default=CITIES)
    selected_depts  = st.multiselect("Departments", options=DEPARTMENTS, default=DEPARTMENTS)

    st.divider()
    st.markdown("<div class='section-header'>Quick Stats</div>", unsafe_allow_html=True)

    fdf_all = df[(df['city'].isin(selected_cities)) & (df['department'].isin(selected_depts))]
    comp  = (fdf_all['status'] == 'completed').mean() * 100
    nshow = (fdf_all['status'] == 'no-show').mean()   * 100

    st.markdown(f"""
    <div style='display:flex;flex-direction:column;gap:8px;margin-top:4px'>
        <div style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);border-radius:8px;padding:10px 12px'>
            <div style='font-size:10px;color:#334155;text-transform:uppercase;letter-spacing:1px'>Completion Rate</div>
            <div style='font-size:18px;font-weight:700;color:#f1f5f9;margin-top:2px'>{comp:.1f}%</div>
            <div style='font-size:11px;color:#34d399'>Active appointments</div>
        </div>
        <div style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);border-radius:8px;padding:10px 12px'>
            <div style='font-size:10px;color:#334155;text-transform:uppercase;letter-spacing:1px'>No-Show Rate</div>
            <div style='font-size:18px;font-weight:700;color:#f87171;margin-top:2px'>{nshow:.1f}%</div>
            <div style='font-size:11px;color:#f87171'>Missed appointments</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style='display:flex;align-items:center;gap:6px;margin-top:4px'>
        <div style='width:7px;height:7px;border-radius:50%;background:#10b981'></div>
        <span style='font-size:12px;color:#34d399'>Live Data</span>
    </div>
    """, unsafe_allow_html=True)

# ── FILTERED DATA ─────────────────────────────────────────────────────────────
filtered_df = df[
    (df['city'].isin(selected_cities)) &
    (df['department'].isin(selected_depts))
]

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom:20px'>
    <h1 style='font-size:26px;margin-bottom:4px'>MediTrack Analytics</h1>
    <p style='color:#475569;font-size:13px;margin:0'>Private Healthcare Network &nbsp;·&nbsp; Karachi · Lahore · Islamabad · Peshawar · Multan</p>
</div>
""", unsafe_allow_html=True)

# ── KPI ROW ───────────────────────────────────────────────────────────────────
total_appts   = len(filtered_df)
total_rev     = filtered_df['revenue'].sum()
comp_rate     = (filtered_df['status'] == 'completed').mean() * 100
no_show_rate  = (filtered_df['status'] == 'no-show').mean()   * 100
cancelled_rate = (filtered_df['status'] == 'cancelled').mean() * 100

k1, k2, k3, k4, k5 = st.columns(5)
with k1: st.metric("Total Appointments",  f"{total_appts:,}",      delta="↑ 4.2% vs last qtr")
with k2: st.metric("Total Revenue",       f"PKR {total_rev/1e6:.1f}M", delta="↑ 8.1% vs last qtr")
with k3: st.metric("Completion Rate",     f"{comp_rate:.1f}%",     delta="↑ 2.1% vs last month")
with k4: st.metric("No-Show Rate",        f"{no_show_rate:.1f}%",  delta=f"▲ {no_show_rate-18:.1f}% baseline", delta_color="inverse")
with k5: st.metric("Cancelled Rate",      f"{cancelled_rate:.1f}%")

st.divider()

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈  Revenue & Trends",
    "🏥  Department Performance",
    "👨‍⚕️  Doctor Analysis",
    "🔮  No-Show Predictor"
])

# ═══════════════════════════════════════════════════════════════
# TAB 1 — REVENUE & TRENDS
# ═══════════════════════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        city_rev = filtered_df.groupby('city')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)
        colors = ["#10b981" if r == city_rev['revenue'].max() else "#6366f1" for r in city_rev['revenue']]
        fig = go.Figure(go.Bar(
            x=city_rev['city'], y=city_rev['revenue']/1e6,
            marker_color=colors, marker_line_width=0,
            text=[f"{v:.1f}M" for v in city_rev['revenue']/1e6],
            textposition='outside', textfont=dict(color="#94a3b8", size=11)
        ))
        fig.update_traces(marker_cornerradius=4)
        apply_theme(fig)
        fig.update_layout(title="Revenue by City (PKR M)", yaxis_title="PKR Millions")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        status_counts = filtered_df['status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        STATUS_COLORS = {'completed':'#10b981','no-show':'#ef4444','cancelled':'#f59e0b','rescheduled':'#3b82f6'}
        fig = go.Figure(go.Pie(
            labels=status_counts['status'],
            values=status_counts['count'],
            hole=0.55,
            marker_colors=[STATUS_COLORS.get(s, '#6366f1') for s in status_counts['status']],
            textinfo='label+percent',
            textfont=dict(color="#e2e8f0", size=11),
            hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
        ))
        apply_theme(fig)
        fig.update_layout(title="Appointment Status Distribution", showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    # Monthly trend
    monthly = (
        filtered_df.groupby('year_month')
        .agg(Appointments=('appointment_id','count'), Revenue=('revenue','sum'))
        .reset_index().sort_values('year_month')
    )
    monthly['Revenue_M'] = monthly['Revenue'] / 1e6

    metric_choice = st.radio("View metric:", ["Appointments", "Revenue (PKR M)"], horizontal=True)
    y_col   = "Appointments" if "Appoint" in metric_choice else "Revenue_M"
    y_label = "Appointments" if "Appoint" in metric_choice else "PKR Millions"

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly['year_month'], y=monthly[y_col],
        mode='lines+markers',
        line=dict(color='#6366f1', width=2.5),
        marker=dict(color='#6366f1', size=6),
        fill='tozeroy',
        fillcolor='rgba(99,102,241,0.08)',
        hovertemplate="<b>%{x}</b><br>" + y_label + ": %{y:,.1f}<extra></extra>"
    ))
    apply_theme(fig, height=260)
    fig.update_layout(title="Monthly Performance Trend", yaxis_title=y_label)
    st.plotly_chart(fig, use_container_width=True)

    # Day of week
    dow = filtered_df.groupby('weekday').size().reset_index(name='count')
    dow['weekday'] = pd.Categorical(dow['weekday'], categories=DAY_ORDER, ordered=True)
    dow = dow.sort_values('weekday')
    bar_colors = ["#ef4444" if d == "Sunday" else "#6366f1" if c > dow['count'].quantile(0.6) else "#4f46e5"
                  for d, c in zip(dow['weekday'], dow['count'])]

    fig = go.Figure(go.Bar(
        x=dow['weekday'], y=dow['count'],
        marker_color=bar_colors, marker_line_width=0,
        text=dow['count'], textposition='outside',
        textfont=dict(color="#94a3b8", size=10),
        hovertemplate="<b>%{x}</b><br>Appointments: %{y:,}<extra></extra>"
    ))
    fig.update_traces(marker_cornerradius=4)
    apply_theme(fig, height=240)
    fig.update_layout(title="Appointments by Day of Week")
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 2 — DEPARTMENT PERFORMANCE
# ═══════════════════════════════════════════════════════════════
with tab2:
    dept_perf = filtered_df.groupby('department').agg(
        Appointments=('appointment_id','count'),
        Revenue=('revenue','sum'),
        No_Show_Rate=('status', lambda x: round((x=='no-show').mean()*100, 1))
    ).reset_index()
    dept_perf['Revenue_M']  = dept_perf['Revenue'] / 1e6
    dept_perf['Color']      = dept_perf['department'].map(DEPT_COLORS)
    dept_perf['NS_Color']   = dept_perf['No_Show_Rate'].apply(
        lambda x: "#ef4444" if x > 20 else "#f59e0b" if x > 18 else "#10b981"
    )

    c3, c4 = st.columns(2)
    with c3:
        fig = go.Figure(go.Bar(
            x=dept_perf['department'], y=dept_perf['Revenue_M'],
            marker_color=dept_perf['Color'].tolist(), marker_line_width=0,
            text=[f"{v:.1f}M" for v in dept_perf['Revenue_M']],
            textposition='outside', textfont=dict(color="#94a3b8", size=11),
            hovertemplate="<b>%{x}</b><br>Revenue: PKR %{y:.2f}M<extra></extra>"
        ))
        fig.update_traces(marker_cornerradius=4)
        apply_theme(fig)
        fig.update_layout(title="Revenue by Department (PKR M)")
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        fig = go.Figure(go.Bar(
            x=dept_perf['No_Show_Rate'], y=dept_perf['department'],
            orientation='h',
            marker_color=dept_perf['NS_Color'].tolist(), marker_line_width=0,
            text=[f"{v}%" for v in dept_perf['No_Show_Rate']],
            textposition='outside', textfont=dict(color="#94a3b8", size=11),
            hovertemplate="<b>%{y}</b><br>No-Show Rate: %{x:.1f}%<extra></extra>"
        ))
        fig.update_traces(marker_cornerradius=4)
        apply_theme(fig)
        fig.update_layout(title="No-Show Rate by Department (%)", xaxis_title="No-Show %")
        st.plotly_chart(fig, use_container_width=True)

    # Summary table
    st.markdown("<div class='section-header' style='margin-top:8px'>Department Summary</div>", unsafe_allow_html=True)
    sort_col = st.selectbox("Sort by", ["Revenue_M","Appointments","No_Show_Rate"], format_func=lambda x: x.replace("_"," ").replace("M"," (M PKR)"))
    table = dept_perf[['department','Appointments','Revenue_M','No_Show_Rate']].sort_values(sort_col, ascending=False).copy()
    table.columns = ['Department','Appointments','Revenue (PKR M)','No-Show Rate (%)']
    table['Revenue (PKR M)'] = table['Revenue (PKR M)'].round(2)
    st.dataframe(
        table.style
            .background_gradient(subset=['No-Show Rate (%)'], cmap='RdYlGn_r')
            .background_gradient(subset=['Revenue (PKR M)'], cmap='Blues')
            .format({'Revenue (PKR M)': '{:.2f}', 'No-Show Rate (%)': '{:.1f}%', 'Appointments': '{:,}'}),
        use_container_width=True, hide_index=True
    )

# ═══════════════════════════════════════════════════════════════
# TAB 3 — DOCTOR ANALYSIS
# ═══════════════════════════════════════════════════════════════
with tab3:
    doctor_perf = (
        filtered_df.groupby('doctor_id')
        .agg(
            Appointments=('appointment_id','count'),
            Revenue=('revenue','sum'),
            No_Show_Rate=('status', lambda x: round((x=='no-show').mean()*100,1))
        ).reset_index()
    )
    doctor_perf = doctor_perf.merge(
        doctors_df[['doctor_id','name','seniority','department']], on='doctor_id', how='left'
    )
    doctor_perf['Revenue_M'] = doctor_perf['Revenue'] / 1e6

    filter_col, _ = st.columns([2, 3])
    with filter_col:
        dept_filter = st.selectbox("Filter by Department", ["All"] + DEPARTMENTS)

    plot_df = doctor_perf if dept_filter == "All" else doctor_perf[doctor_perf['department'] == dept_filter]
    top10   = plot_df.sort_values('No_Show_Rate', ascending=False).head(10)

    bar_colors = [
        "#ef4444" if r > 30 else "#f59e0b" if r > 25 else "#6366f1"
        for r in top10['No_Show_Rate']
    ]
    fig = go.Figure(go.Bar(
        x=top10['name'], y=top10['No_Show_Rate'],
        marker_color=bar_colors, marker_line_width=0,
        text=[f"{v:.1f}%" for v in top10['No_Show_Rate']],
        textposition='outside', textfont=dict(color="#94a3b8", size=10),
        hovertemplate="<b>%{x}</b><br>No-Show Rate: %{y:.1f}%<br>Appointments: %{customdata:,}<extra></extra>",
        customdata=top10['Appointments']
    ))
    fig.update_traces(marker_cornerradius=4)
    apply_theme(fig, height=300)
    fig.update_layout(
        title="Top 10 Doctors — Highest No-Show Rate",
        xaxis_tickangle=-20,
        yaxis_title="No-Show Rate (%)",
        yaxis_range=[0, top10['No_Show_Rate'].max() * 1.2]
    )
    st.plotly_chart(fig, use_container_width=True)

    # Scatter: Appointments vs No-Show Rate
    fig2 = px.scatter(
        plot_df, x='Appointments', y='No_Show_Rate', color='department',
        size='Revenue_M', hover_name='name',
        color_discrete_map=DEPT_COLORS,
        labels={'No_Show_Rate':'No-Show Rate (%)','Revenue_M':'Revenue (M PKR)'},
        title="Appointments vs No-Show Rate (bubble = revenue)"
    )
    apply_theme(fig2, height=300)
    fig2.update_traces(marker=dict(opacity=0.85, line=dict(width=0)))
    st.plotly_chart(fig2, use_container_width=True)

    # Doctor table
    st.markdown("<div class='section-header' style='margin-top:8px'>Full Doctor Table</div>", unsafe_allow_html=True)

    def risk_label(r):
        if r > 30: return "🔴 High"
        if r > 25: return "🟡 Medium"
        return "🟢 Low"

    tbl = top10[['name','department','seniority','Appointments','Revenue_M','No_Show_Rate']].copy()
    tbl['Risk'] = tbl['No_Show_Rate'].apply(risk_label)
    tbl.columns = ['Doctor','Department','Seniority','Appointments','Revenue (M PKR)','No-Show %','Risk Level']
    st.dataframe(
        tbl.style
            .background_gradient(subset=['No-Show %'], cmap='RdYlGn_r')
            .format({'Revenue (M PKR)': '{:.2f}', 'No-Show %': '{:.1f}', 'Appointments': '{:,}'}),
        use_container_width=True, hide_index=True
    )

# ═══════════════════════════════════════════════════════════════
# TAB 4 — NO-SHOW PREDICTOR
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class='info-box'>
        Configure the appointment parameters below. The model estimates no-show probability
        based on department baseline rates, city patterns, patient type, and day-of-week effects.
    </div>
    """, unsafe_allow_html=True)

    colA, colB = st.columns(2)
    with colA:
        p_dept = st.selectbox("Department", DEPARTMENTS, key="pred_dept")
        p_city = st.selectbox("City",        CITIES,       key="pred_city")
        p_day  = st.selectbox("Day of Week", DAY_ORDER,    key="pred_day")
    with colB:
        p_type = st.radio("Patient Type", ["New Patient","Returning Patient"], key="pred_type")

        # Pull real baseline from DB if available
        if len(filtered_df) > 0:
            dept_base = filtered_df[filtered_df['department'] == p_dept]
            real_base = (dept_base['status'] == 'no-show').mean() * 100 if len(dept_base) > 0 else 18.0
        else:
            real_base = 18.0

        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);
                    border-radius:8px;padding:12px 14px;margin-top:8px'>
            <div style='font-size:10px;color:#334155;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px'>
                {p_dept} Baseline (from your data)
            </div>
            <div style='font-size:22px;font-weight:700;color:#e2e8f0'>{real_base:.1f}%</div>
            <div style='font-size:11px;color:#64748b'>average no-show rate in this department</div>
        </div>
        """, unsafe_allow_html=True)

    # Prediction model
    DEPT_BASE  = {"Cardiology":21.0,"Dermatology":21.5,"General":17.0,"Orthopedics":17.0,"Pediatrics":17.0}
    CITY_MOD   = {"Karachi":1.05,"Lahore":0.95,"Islamabad":1.02,"Multan":1.08,"Peshawar":0.98}
    DAY_MOD    = {"Monday":1.05,"Tuesday":1.0,"Wednesday":1.02,"Thursday":0.98,"Friday":1.1,"Saturday":0.9,"Sunday":1.3}
    TYPE_MOD   = {"New Patient":1.2,"Returning Patient":0.85}

    base  = DEPT_BASE.get(p_dept, 18.0)
    prob  = base * CITY_MOD.get(p_city,1) * DAY_MOD.get(p_day,1) * TYPE_MOD.get(p_type,1)
    prob  = min(round(prob), 99)
    risk  = "High" if prob >= 28 else "Medium" if prob >= 20 else "Low"
    rc    = {"High":"risk-high","Medium":"risk-med","Low":"risk-low"}
    action = {
        "High":   "🚨 Call the patient directly — consider overbooking this slot.",
        "Medium": "⚠️  Send an automated SMS/WhatsApp reminder 24h before.",
        "Low":    "✅  No action needed — standard confirmation is sufficient."
    }

    st.divider()
    res1, res2 = st.columns([1, 2])

    with res1:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob,
            number=dict(suffix="%", font=dict(color="#e2e8f0", size=40, family=FONT_FAM)),
            gauge=dict(
                axis=dict(range=[0,100], tickcolor="#334155", tickfont=dict(color="#475569")),
                bar=dict(color="#ef4444" if risk=="High" else "#f59e0b" if risk=="Medium" else "#10b981"),
                bgcolor="rgba(255,255,255,0.04)",
                borderwidth=0,
                steps=[
                    dict(range=[0,20],  color="rgba(16,185,129,0.1)"),
                    dict(range=[20,28], color="rgba(245,158,11,0.1)"),
                    dict(range=[28,100],color="rgba(239,68,68,0.1)"),
                ],
                threshold=dict(line=dict(color="#e2e8f0",width=2), thickness=0.75, value=prob)
            )
        ))
        gauge.update_layout(
            height=240, paper_bgcolor=PLOT_BG,
            margin=dict(l=20,r=20,t=20,b=10),
            font=dict(family=FONT_FAM, color=TICK_COL)
        )
        st.plotly_chart(gauge, use_container_width=True)

    with res2:
        st.markdown(f"""
        <div class='{rc[risk]}' style='margin-bottom:12px'>
            <strong>{risk} Risk — {prob}% probability</strong><br>
            <span style='font-size:12px;opacity:0.85'>{action[risk]}</span>
        </div>
        """, unsafe_allow_html=True)

        city_note  = {"Karachi":"+5%","Lahore":"-5%","Islamabad":"+2%","Multan":"+8%","Peshawar":"-2%"}
        day_note   = {"Monday":"+5%","Tuesday":"Baseline","Wednesday":"+2%","Thursday":"-2%","Friday":"+10%","Saturday":"-10%","Sunday":"+30%"}
        type_note  = {"New Patient":"+20%","Returning Patient":"-15%"}

        factors = [
            ("Dept. Baseline",  p_dept,  f"{base:.0f}% base rate"),
            ("City Modifier",   p_city,  city_note.get(p_city,"")),
            ("Day of Week",     p_day,   day_note.get(p_day,"")),
            ("Patient Type",    p_type.replace(" Patient",""), type_note.get(p_type,"")),
        ]

        fcols = st.columns(4)
        for i, (label, val, note) in enumerate(factors):
            with fcols[i]:
                st.markdown(f"""
                <div class='factor-card'>
                    <div class='factor-label'>{label}</div>
                    <div class='factor-val'>{val}</div>
                    <div class='factor-note'>{note}</div>
                </div>
                """, unsafe_allow_html=True)

        # Probability bar
        bar_color = "#ef4444" if risk=="High" else "#f59e0b" if risk=="Medium" else "#10b981"
        st.markdown(f"""
        <div style='margin-top:14px'>
            <div style='font-size:10px;color:#334155;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px'>Probability Gauge</div>
            <div style='background:rgba(255,255,255,0.06);border-radius:100px;height:10px;overflow:hidden'>
                <div style='width:{prob}%;height:100%;background:{bar_color};border-radius:100px;
                            transition:width 0.7s ease'></div>
            </div>
            <div style='display:flex;justify-content:space-between;font-size:10px;color:#334155;margin-top:4px'>
                <span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.divider()
c_left, c_right = st.columns([3,1])
with c_left:
    if st.checkbox("Show sample raw data (first 500 rows)"):
        st.dataframe(filtered_df.head(500), use_container_width=True)
with c_right:
    st.caption("MediTrack Analytics Pro · Private Healthcare Network")
