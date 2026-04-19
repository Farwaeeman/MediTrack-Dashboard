import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(page_title="MediTrack Dashboard", layout="wide", page_icon="🩺")

st.title("🩺 MediTrack Analytics Dashboard")
st.subheader("Private Healthcare Network • Karachi • Lahore • Islamabad • Peshawar • Multan")

# Load Data
@st.cache_data
def load_data():
    conn = sqlite3.connect('meditrack.db')
    appointments = pd.read_sql("SELECT * FROM appointments", conn)
    doctors = pd.read_sql("SELECT * FROM doctors", conn)
    conn.close()
    
    appointments['appointment_date'] = pd.to_datetime(appointments['appointment_date'])
    appointments['month'] = appointments['appointment_date'].dt.strftime('%b %Y')
    appointments['weekday'] = appointments['appointment_date'].dt.day_name()
    appointments['revenue'] = appointments['consultation_fee']
    
    return appointments, doctors

df, doctors_df = load_data()

# Define departments and cities here (so no error)
DEPARTMENTS = ["General", "Cardiology", "Orthopedics", "Dermatology", "Pediatrics"]
CITIES = ["Karachi", "Lahore", "Islamabad", "Peshawar", "Multan"]

# Sidebar Filters
st.sidebar.header("🔍 Filters")
selected_cities = st.sidebar.multiselect("Select Cities", options=CITIES, default=CITIES)
selected_depts = st.sidebar.multiselect("Select Departments", options=DEPARTMENTS, default=DEPARTMENTS)

# Filtered Data
filtered_df = df[(df['city'].isin(selected_cities)) & (df['department'].isin(selected_depts))]

# ==================== KPIs ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Appointments", f"{len(filtered_df):,}")
with col2:
    st.metric("Total Revenue", f"PKR {filtered_df['revenue'].sum():,}")
with col3:
    completion_rate = (filtered_df['status'] == 'completed').mean() * 100
    st.metric("Completion Rate", f"{completion_rate:.1f}%")
with col4:
    no_show_rate = (filtered_df['status'] == 'no-show').mean() * 100
    st.metric("No-Show Rate", f"{no_show_rate:.1f}%")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["📈 Revenue & Trends", "🏥 Department Performance", "👨‍⚕️ Doctor Analysis", "🔮 No-Show Prediction"])

with tab1:
    c1, c2 = st.columns(2)
    
    with c1:
        city_rev = filtered_df.groupby('city')['revenue'].sum().reset_index()
        fig1 = px.bar(city_rev, x='city', y='revenue', title="Revenue by City (PKR)", color='city', text_auto='.2s')
        st.plotly_chart(fig1, use_container_width=True)
    
    with c2:
        monthly = filtered_df.groupby('month').size().reset_index(name='appointments')
        fig2 = px.line(monthly, x='month', y='appointments', title="Monthly Appointment Trend", markers=True)
        st.plotly_chart(fig2, use_container_width=True)

    # Day of Week
    dow = filtered_df.groupby('weekday').size().reset_index(name='count')
    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    dow['weekday'] = pd.Categorical(dow['weekday'], categories=day_order, ordered=True)
    dow = dow.sort_values('weekday')
    
    fig3 = px.bar(dow, x='weekday', y='count', title="Appointments by Day of Week")
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    dept_perf = filtered_df.groupby('department').agg(
        Appointments=('appointment_id', 'count'),
        Revenue=('revenue', 'sum'),
        No_Show_Rate=('status', lambda x: (x=='no-show').mean()*100)
    ).reset_index()
    
    c3, c4 = st.columns(2)
    with c3:
        fig4 = px.bar(dept_perf, x='department', y='Revenue', title="Revenue by Department")
        st.plotly_chart(fig4, use_container_width=True)
    
    with c4:
        fig5 = px.bar(dept_perf, x='department', y='No_Show_Rate', title="No-Show Rate by Department (%)")
        st.plotly_chart(fig5, use_container_width=True)

with tab3:
    doctor_perf = filtered_df.groupby('doctor_id').agg(
        Appointments=('appointment_id', 'count'),
        No_Show_Rate=('status', lambda x: (x == 'no-show').mean() * 100)
    ).reset_index()
    
    doctor_perf = doctor_perf.merge(doctors_df[['doctor_id', 'name', 'seniority', 'department']], on='doctor_id')
    doctor_perf = doctor_perf.sort_values('No_Show_Rate', ascending=False).head(10)
    
    fig6 = px.bar(doctor_perf, x='name', y='No_Show_Rate', 
                  title="Top 10 Doctors with Highest No-Show Rate (%)",
                  color='department', text_auto='.1f')
    st.plotly_chart(fig6, use_container_width=True)

with tab4:
    st.subheader("No-Show Prediction Tool")
    st.write("Helps management decide whom to send reminders to.")

    colA, colB = st.columns(2)
    with colA:
        p_dept = st.selectbox("Department", options=DEPARTMENTS)
        p_city = st.selectbox("City", options=CITIES)
    with colB:
        p_type = st.radio("Patient Type", ["New Patient", "Returning Patient"])
        p_day = st.selectbox("Day of Week", ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])

    # Simple prediction logic
    prob = 14
    if p_type == "New Patient": prob += 12
    if p_day in ['Saturday', 'Sunday']: prob += 10
    if p_dept in ['Dermatology', 'Cardiology']: prob += 7

    prob = min(prob, 50)

    st.metric("Predicted No-Show Probability", f"{prob}%")

    if prob >= 30:
        st.error("🔴 High Risk - Send reminder 48 hours before")
    elif prob >= 20:
        st.warning("🟡 Medium Risk - Send reminder")
    else:
        st.success("🟢 Low Risk")

# Raw Data
if st.checkbox("Show Sample Raw Data"):
    st.dataframe(filtered_df.head(500))

st.caption("MediTrack Analytics Dashboard | Assignment - Farwa")
