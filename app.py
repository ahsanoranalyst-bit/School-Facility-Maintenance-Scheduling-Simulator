

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fpdf import FPDF
import plotly.express as px

# --- 1. SETTINGS ---
MASTER_KEY = "Ahsan123"
PROJECT_ID = "FACILITY_INTEL_2026"

st.set_page_config(page_title="Professional Maintenance Suite", layout="wide", page_icon="🛠️")

# Blue Theme CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; border-bottom: 5px solid #1f4e79; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .stTabs [aria-selected="true"] { background-color: #1f4e79 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'org_name' not in st.session_state: st.session_state.org_name = ""
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame([
        {"Asset": "Air Conditioners", "Qty": 20, "Avg Age (Yrs)": 3, "Last Service": "2023-10-01", "Warranty": "2025-01-01"},
        {"Asset": "Core i5 PCs", "Qty": 50, "Avg Age (Yrs)": 2, "Last Service": "2024-01-15", "Warranty": "2025-06-01"},
        {"Asset": "Main Generator", "Qty": 1, "Avg Age (Yrs)": 8, "Last Service": "2023-05-20", "Warranty": "Expired"}
    ])

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🛡️ System Activation")
        key = st.text_input("Enter License Key", type="password")
        if st.button("Unlock Portal", use_container_width=True):
            if key == MASTER_KEY:
                st.session_state.auth = True
                st.rerun()
    st.stop()

if st.session_state.auth and not st.session_state.org_name:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🏫 Organization Registration")
        o_name = st.text_input("Enter Institution Name")
        if st.button("Complete Registration"):
            if o_name: st.session_state.org_name = o_name; st.rerun()
    st.stop()

# --- 3. PROFESSIONAL SIDEBAR (ONLY RELEVANT CONTROLS) ---
with st.sidebar:
    st.title(f"🏢 {st.session_state.org_name}")
    st.divider()
    st.subheader("📊 Financial Parameters")
    labor_rate = st.number_input("Labor Rate (PKR/hr)", 500, 10000, 1500)
    profit_margin = st.slider("Budget Buffer (%)", 1, 200, 20) # Profit level 1-200
    
    st.divider()
    st.info(f"System Version: 2.0\nProject ID: {PROJECT_ID}")
    
    if st.button("🔴 Secure Logout", use_container_width=True):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- 4. DATA ENGINE ---
def process_intel(df):
    temp = df.copy()
    # Risk calculation logic
    temp['Risk_F'] = temp['Avg Age (Yrs)'] * temp['Warranty'].apply(lambda x: 1.6 if str(x).lower() == "expired" else 1.0)
    # Scaled to PKR
    temp['Repair Cost'] = (temp['Risk_F'] * 5500) * (1 + (profit_margin/100)) * temp['Qty']
    # 5. Predictive Maintenance Score (5th Point)
    temp['Predictive Score'] = (100 - (temp['Risk_F'] * 6)).clip(lower=5, upper=100).astype(int)
    return temp

final_df = process_intel(st.session_state.assets)

# --- 5. PDF REPORT ENGINE (BLUE THEME) ---
def generate_admin_report(df):
    pdf = FPDF()
    pdf.add_page()
    # Header
    pdf.set_fill_color(31, 78, 121) 
    pdf.rect(0, 0, 210, 35, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 15, st.session_state.org_name.upper(), ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, "EXECUTIVE ASSET AUDIT REPORT", ln=True, align='C')
    pdf.ln(25)
    
    # Financial Stats Box
    pdf.set_fill_color(235, 240, 250)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f" Summary: Total Maintenance Exposure PKR {df['Repair Cost'].sum():,.0f}", 0, 1, 'L', True)
    pdf.ln(5)

    # Table
    pdf.set_fill_color(46, 117, 182)
    pdf.set_text_color(255, 255, 255)
    headers = [("Asset", 70), ("Qty", 20), ("Budget (PKR)", 40), ("Score", 30), ("Status", 30)]
    for txt, w in headers: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 9)
    for _, row in df.iterrows():
        pdf.cell(70, 9, str(row['Asset']), 1)
        pdf.cell(20, 9, str(row['Qty']), 1, 0, 'C')
        pdf.cell(40, 9, f"{row['Repair Cost']:,.0f}", 1, 0, 'R')
        pdf.cell(30, 9, f"{row['Predictive Score']}%", 1, 0, 'C')
        pdf.cell(30, 9, "Critical" if row['Predictive Score'] < 50 else "Stable", 1, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- 6. MAIN WORKSPACE ---
tabs = st.tabs(["📝 Asset Inventory", "🧠 Predictive Intelligence"])

with tabs[0]:
    st.subheader("Asset Management Ledger")
    # Table data management
    st.session_state.assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)

with tabs[1]:
    st.title("Predictive Risk Intelligence")
    
    # Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Asset Risk (PKR)", f"Rs. {final_df['Repair Cost'].sum():,.0f}")
    m2.metric("Critical Items", len(final_df[final_df['Predictive Score'] < 50]))
    m3.metric("Avg System Health", f"{int(final_df['Predictive Score'].mean())}%")

    st.divider()
    
    # Professional Dashboard Visuals
    
    c1, c2 = st.columns([1.6, 1])
    with c1:
        st.subheader("Repair Budget Distribution")
        fig = px.bar(final_df, x='Asset', y='Repair Cost', color='Predictive Score', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("Asset Health Matrix")
        for _, r in final_df.iterrows():
            st.write(f"**{r['Asset']}**")
            st.progress(r['Predictive Score']/100)

    st.divider()
    
    # Export Section
    st.subheader("📥 Official Audit Generation")
    if st.button("Generate Executive Admin Report (Blue)", use_container_width=True):
        report_pdf = generate_admin_report(final_df)
        st.download_button("Download Admin PDF", report_pdf, "Admin_Audit_Report.pdf", use_container_width=True)
