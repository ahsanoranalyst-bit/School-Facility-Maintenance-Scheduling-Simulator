


import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fpdf import FPDF
import plotly.express as px

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Institutional Facility Management", layout="wide", page_icon="🏢")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px; padding: 10px; }
    .stTabs [aria-selected="true"] { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION INITIALIZATION ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'org_name' not in st.session_state: st.session_state.org_name = ""
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame([
        {"Asset": "Air Conditioners", "Qty": 20, "Avg Age (Yrs)": 3, "Last Service": "2023-10-01", "Warranty": "2025-01-01"},
        {"Asset": "Computers", "Qty": 50, "Avg Age (Yrs)": 2, "Last Service": "2024-01-15", "Warranty": "2025-06-01"},
        {"Asset": "Plumbing System", "Qty": 1, "Avg Age (Yrs)": 15, "Last Service": "2022-05-20", "Warranty": "Expired"},
        {"Asset": "Ceiling Fans", "Qty": 100, "Avg Age (Yrs)": 5, "Last Service": "2023-08-10", "Warranty": "Expired"}
    ])

# --- 3. AUTHENTICATION ---
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🛡️ Secure Activation")
        key = st.text_input("License Key", type="password")
        if st.button("Unlock System", use_container_width=True):
            if key == "Ahsan123":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Access Denied.")
    st.stop()

if st.session_state.auth and not st.session_state.org_name:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🏫 Organization Setup")
        name = st.text_input("Organization Name")
        if st.button("Initialize", use_container_width=True):
            if name: 
                st.session_state.org_name = name
                st.rerun()
    st.stop()

# --- 4. DATA PROCESSING ---
labor_rate = st.sidebar.number_input("Labor Rate (PKR/hr)", 500, 10000, 1500)
markup = st.sidebar.slider("Parts Buffer (%)", 0, 50, 15) / 100

def calculate_intelligence(df):
    df = df.copy()
    # Risk factor calculation
    df['Risk Factor'] = df['Avg Age (Yrs)'] * df['Warranty'].apply(lambda x: 1.5 if x == "Expired" else 1.0)
    # Estimated Repair Cost based on PKR 5,000 unit cost scaling
    df['Repair Cost'] = (df['Risk Factor'] * 5000) * (1 + markup) * df['Qty']
    # Health Score Logic
    df['Health Score'] = (100 - (df['Risk Factor'] * 5)).clip(lower=5, upper=100).astype(int)
    return df

processed_df = calculate_intelligence(st.session_state.assets)

# --- 5. PDF GENERATOR ---
def create_pdf(df, title, type="ADMIN"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 102, 51) # Green Header
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, st.session_state.org_name.upper(), ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, title, ln=True, align='C')
    pdf.ln(25)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 9)
    
    if type == "ORDER":
        cols = [("Asset Item", 90), ("Qty", 30), ("Urgency", 30), ("Budget (PKR)", 40)]
    else:
        cols = [("Asset", 60), ("Qty", 20), ("Risk (PKR)", 45), ("Health", 30), ("Status", 35)]

    for txt, w in cols: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()

    pdf.set_font("Arial", '', 8)
    for _, row in df.iterrows():
        if type == "ORDER" and row['Health Score'] > 50: continue
        if type == "ORDER":
            pdf.cell(90, 8, str(row['Asset']), 1)
            pdf.cell(30, 8, str(row['Qty']), 1, 0, 'C')
            pdf.cell(30, 8, "High" if row['Health Score'] < 40 else "Normal", 1, 0, 'C')
            pdf.cell(40, 8, f"{row['Repair Cost']:,.0f}", 1, 1, 'R')
        else:
            pdf.cell(60, 8, str(row['Asset']), 1)
            pdf.cell(20, 8, str(row['Qty']), 1, 0, 'C')
            pdf.cell(45, 8, f"{row['Repair Cost']:,.0f}", 1, 0, 'R')
            pdf.cell(30, 8, f"{row['Health Score']}%", 1, 0, 'C')
            pdf.cell(35, 8, "Critical" if row['Health Score'] < 50 else "Stable", 1, 1, 'C')
            
    return pdf.output(dest='S').encode('latin-1')

# --- 6. MAIN UI ---
tabs = st.tabs(["📋 Asset Management", "📅 Maintenance Schedule", "🧠 Predictive Intelligence"])

with tabs[0]:
    st.subheader("Master Asset Inventory")
    col_up, col_dn = st.columns([2,1])
    with col_up:
        uploaded = st.file_uploader("Import Excel Database", type="xlsx")
        if uploaded: 
            st.session_state.assets = pd.read_excel(uploaded)
            st.rerun()
    st.session_state.assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)

with tabs[1]:
    st.subheader("Inspection Forecast")
    sched_df = processed_df.copy()
    sched_df['Next Service'] = (datetime.today() + timedelta(days=90)).strftime('%Y-%m-%d')
    st.table(sched_df[['Asset', 'Last Service', 'Next Service', 'Health Score']])

# --- TAB 3: PREDICTIVE RISK INTELLIGENCE (Based on Images) ---
with tabs[2]:
    st.title("Predictive Risk Intelligence")
    
    # KPI Row
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Asset Risk (PKR)", f"Rs. {processed_df['Repair Cost'].sum():,.0f}")
    k2.metric("Critical Assets", len(processed_df[processed_df['Health Score'] < 50]))
    k3.metric("Avg. Health Score", f"{int(processed_df['Health Score'].mean())}%")
    
    st.divider()
    
    # Charts Row (As per Image 1 & 2)
    left_col, right_col = st.columns([1.5, 1])
    
    with left_col:
        st.subheader("Executed Purchase & Repair Overview")
        fig = px.bar(processed_df, x='Asset', y='Repair Cost', 
                     color='Health Score', color_continuous_scale='RdYlGn',
                     labels={'Repair Cost': 'Cost (PKR)'},
                     template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    
    with right_col:
        st.subheader("Health Score Breakdown")
        for _, row in processed_df.iterrows():
            st.write(f"**{row['Asset']}**")
            color = "red" if row['Health Score'] < 50 else "green"
            st.markdown(f"<p style='color:{color}; font-size:12px; margin-bottom:0px;'>Score: {row['Health Score']}%</p>", unsafe_allow_html=True)
            st.progress(row['Health Score'] / 100)

    st.divider()
    
    # Export Center
    st.subheader("📊 Document Export Center")
    ex1, ex2, ex3 = st.columns(3)
    
    with ex1:
        if st.button("Generate Admin Audit (PDF)", use_container_width=True):
            pdf = create_pdf(processed_df, "EXECUTIVE ADMIN AUDIT", "ADMIN")
            st.download_button("Download Admin PDF", pdf, "Admin_Audit.pdf")
            
    with ex2:
        if st.button("Generate Institutional Summary", use_container_width=True):
            pdf = create_pdf(processed_df, "INSTITUTIONAL SUMMARY REPORT", "SUMMARY")
            st.download_button("Download Summary PDF", pdf, "Summary_Report.pdf")
            
    with ex3:
        if st.button("Generate Vendor Purchase Order", use_container_width=True):
            pdf = create_pdf(processed_df, "OFFICIAL MAINTENANCE ORDER", "ORDER")
            st.download_button("Download Order PDF", pdf, "Purchase_Order.pdf")

st.sidebar.markdown("---")
st.sidebar.caption(f"Portal Version: {PROJECT_ID}")
