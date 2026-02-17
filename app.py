

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fpdf import FPDF
import plotly.express as px

# --- 1. GLOBAL CONFIGURATION ---
MASTER_KEY = "Ahsan123"
PROJECT_ID = "PK_FACILITY_PRO_2026"

st.set_page_config(page_title="Facility Intelligence Suite", layout="wide", page_icon="🏢")

# Custom CSS for Blue Theme
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-bottom: 4px solid #1f4e79; }
    .sidebar .sidebar-content { background-image: linear-gradient(#1f4e79, #2e75b6); color: white; }
    .stTabs [aria-selected="true"] { background-color: #1f4e79 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'org_name' not in st.session_state: st.session_state.org_name = ""

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🛡️ Secure Portal Activation")
        key = st.text_input("License Key", type="password")
        if st.button("Unlock System", use_container_width=True):
            if key == MASTER_KEY:
                st.session_state.auth = True
                st.rerun()
    st.stop()

if st.session_state.auth and not st.session_state.org_name:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🏫 Institution Registration")
        o_name = st.text_input("Enter School/Organization Name")
        if st.button("Initialize Workspace"):
            if o_name: st.session_state.org_name = o_name; st.rerun()
    st.stop()

# --- 3. PROFESSIONAL SIDEBAR (MENU BAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3062/3062410.png", width=70)
    st.title(f"{st.session_state.org_name}")
    st.caption(f"Project ID: {PROJECT_ID} [cite: 2026-01-24]")
    
    st.divider()
    
    st.subheader("⚙️ Maintenance Controls")
    labor_rate = st.number_input("Labor Rate (PKR/hr)", 100, 10000, 1500)
    # Profit level scale 1 to 200 [cite: 2025-12-29]
    profit_scale = st.slider("Profit Level Scaling", 1, 200, 20) 
    
    st.divider()
    
    st.subheader("🚐 Logistics Management")
    # Driver management based on distance requirements [cite: 2026-02-12]
    st.info("Pick-up: Furthest First | Drop-off: Nearest First [cite: 2026-02-12]")
    km_rate = st.number_input("Timing per KM (Mins)", 1, 60, 5) # [cite: 2026-02-10]
    
    st.divider()
    
    if st.button("🔴 Secure Logout", use_container_width=True):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- 4. PDF ENGINE (BLUE THEME) ---
class CorporatePDF(FPDF):
    def header(self):
        self.set_fill_color(31, 78, 121) 
        self.rect(0, 0, 210, 35, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 18)
        self.cell(0, 10, st.session_state.org_name.upper(), ln=True, align='C')
        self.ln(20)

def generate_report(df, r_type):
    pdf = CorporatePDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Report: {r_type}", ln=True)
    
    pdf.set_fill_color(46, 117, 182)
    pdf.set_text_color(255, 255, 255)
    cols = [("Asset", 70), ("Qty", 20), ("Risk (PKR)", 40), ("Score", 30), ("Status", 30)]
    for txt, w in cols: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 8)
    for _, row in df.iterrows():
        pdf.cell(70, 8, str(row['Asset']), 1)
        pdf.cell(20, 8, str(row['Qty']), 1, 0, 'C')
        pdf.cell(40, 8, f"{row['Repair Cost']:,.0f}", 1, 0, 'R')
        pdf.cell(30, 8, f"{row['Predictive Score']}%", 1, 0, 'C')
        pdf.cell(30, 8, "Critical" if row['Predictive Score'] < 50 else "Stable", 1, 1, 'C')
    return pdf.output(dest='S').encode('latin-1')

# --- 5. CORE LOGIC ---
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame([
        {"Asset": "AC Units", "Qty": 20, "Avg Age (Yrs)": 3, "Last Service": "2023-10-01", "Warranty": "2025-01-01"},
        {"Asset": "Computers", "Qty": 50, "Avg Age (Yrs)": 2, "Last Service": "2024-01-15", "Warranty": "2025-06-01"},
        {"Asset": "Generator", "Qty": 1, "Avg Age (Yrs)": 8, "Last Service": "2023-05-20", "Warranty": "Expired"}
    ])

tabs = st.tabs(["📋 Inventory", "📅 Logistics", "📊 Predictive Intelligence"])

with tabs[0]:
    st.subheader("Master Asset Ledger")
    st.session_state.assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)

with tabs[1]:
    st.subheader("Driver Schedule & Route Timing")
    # Logistics logic based on KM timings [cite: 2026-02-10]
    log_df = pd.DataFrame([
        {"Person": "Far Side Student", "Distance (KM)": 15, "Role": "Pick-up"},
        {"Person": "Near Side Student", "Distance (KM)": 3, "Role": "Pick-up"}
    ])
    log_df['Est. Time (Mins)'] = log_df['Distance (KM)'] * km_rate
    st.table(log_df)

with tabs[2]:
    st.title("Predictive Risk Intelligence")
    
    # Advanced math for PKR risk and 5th point Score [cite: 2026-02-14]
    df = st.session_state.assets.copy()
    df['Risk_F'] = df['Avg Age (Yrs)'] * df['Warranty'].apply(lambda x: 1.7 if str(x).lower() == "expired" else 1.0)
    df['Repair Cost'] = (df['Risk_F'] * 5000) * (1 + (profit_scale/100)) * df['Qty']
    df['Predictive Score'] = (100 - (df['Risk_F'] * 6)).clip(lower=5, upper=100).astype(int)

    m1, m2, m3 = st.columns(3)
    m1.metric("Risk Exposure (PKR)", f"Rs. {df['Repair Cost'].sum():,.0f}")
    m2.metric("Critical Items", len(df[df['Predictive Score'] < 50]))
    m3.metric("System Health", f"{int(df['Predictive Score'].mean())}%")

    st.divider()
    
    
    c_left, c_right = st.columns([1.6, 1])
    with c_left:
        st.subheader("Executed Purchase & Repair Overview")
        fig = px.bar(df, x='Asset', y='Repair Cost', color='Predictive Score', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    with c_right:
        st.subheader("Health Matrix Breakdown")
        for _, r in df.iterrows():
            st.write(f"**{r['Asset']}**")
            st.progress(r['Predictive Score']/100)

    st.divider()
    
    st.subheader("📊 Reports Export")
    pdf_bytes = generate_report(df, "ADMIN AUDIT")
    st.download_button("📥 Download Admin Audit (Blue)", pdf_bytes, "Audit.pdf", use_container_width=True)
