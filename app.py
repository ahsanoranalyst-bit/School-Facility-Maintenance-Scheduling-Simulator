import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fpdf import FPDF
import plotly.express as px

# --- 1. SYSTEM CONFIGURATION ---
MASTER_KEY = "Ahsan123"
PROJECT_ID = "PK_FACILITY_PRO_2026"

st.set_page_config(page_title="Facility Intelligence Suite", layout="wide", page_icon="🏢")

# Professional Blue Theme CSS
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 5px solid #1f4e79; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #e1e4e8; border-radius: 5px 5px 0 0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #1f4e79 !important; color: white !important; }
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
        st.title("🛡️ System Activation")
        key = st.text_input("License Key", type="password", placeholder="Enter your key...")
        if st.button("Activate Portal", use_container_width=True):
            if key == MASTER_KEY:
                st.session_state.auth = True
                st.rerun()
            else: st.error("Access Key Incorrect")
    st.stop()

if st.session_state.auth and not st.session_state.org_name:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🏫 Institution Setup")
        name = st.text_input("Enter School/Organization Name")
        if st.button("Start System", use_container_width=True):
            if name: 
                st.session_state.org_name = name
                st.rerun()
    st.stop()

# --- 4. ADVANCED PDF ENGINE (PROFESSIONAL BLUE THEME) ---
class ProfessionalPDF(FPDF):
    def header(self):
        self.set_fill_color(31, 78, 121) # Professional Deep Blue
        self.rect(0, 0, 210, 40, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 18)
        self.cell(0, 15, st.session_state.org_name.upper(), ln=True, align='C')
        self.set_font("Arial", '', 10)
        self.cell(0, 5, "FACILITY AUDIT & RISK MANAGEMENT REPORT", ln=True, align='C')
        self.ln(25)

def generate_report(df, r_title, r_type="ADMIN"):
    pdf = ProfessionalPDF()
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    
    # Executive Stats Box
    pdf.set_fill_color(235, 241, 245)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, f" REPORT TYPE: {r_title}", 0, 1, 'L', True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f" Total Expenditure Risk: PKR {df['Repair Cost'].sum():,.0f}", ln=True)
    pdf.ln(5)

    # Table Header
    pdf.set_fill_color(46, 117, 182) # Blue Header
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 9)
    
    if r_type == "ORDER":
        cols = [("Asset Description", 90), ("Qty", 30), ("Status", 30), ("Budget (PKR)", 40)]
    else:
        cols = [("Asset", 60), ("Qty", 20), ("Risk (PKR)", 40), ("Health %", 30), ("Alert Level", 40)]

    for txt, w in cols: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()

    # Table Data
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 8)
    for _, row in df.iterrows():
        if r_type == "ORDER" and row['Health Score'] > 50: continue
        
        if r_type == "ORDER":
            pdf.cell(90, 8, str(row['Asset']), 1)
            pdf.cell(30, 8, str(row['Qty']), 1, 0, 'C')
            pdf.cell(30, 8, "URGENT" if row['Health Score'] < 40 else "ROUTINE", 1, 0, 'C')
            pdf.cell(40, 8, f"{row['Repair Cost']:,.0f}", 1, 1, 'R')
        else:
            pdf.cell(60, 8, str(row['Asset']), 1)
            pdf.cell(20, 8, str(row['Qty']), 1, 0, 'C')
            pdf.cell(40, 8, f"{row['Repair Cost']:,.0f}", 1, 0, 'R')
            pdf.cell(30, 8, f"{row['Health Score']}%", 1, 0, 'C')
            pdf.cell(40, 8, "CRITICAL" if row['Health Score'] < 50 else "STABLE", 1, 1, 'C')
            
    return pdf.output(dest='S').encode('latin-1')

# --- 5. DATA PROCESSING ---
labor_rate = st.sidebar.number_input("Labor Rate (PKR/hr)", 500, 10000, 1500)
markup = st.sidebar.slider("Parts Markup (%)", 0, 50, 20) / 100

def get_intel(df):
    df = df.copy()
    # Fixed formula to avoid warnings
    df['Risk_Factor'] = df['Avg Age (Yrs)'] * df['Warranty'].apply(lambda x: 1.6 if str(x).lower() == "expired" else 1.0)
    df['Repair Cost'] = (df['Risk_Factor'] * 6000) * (1 + markup) * df['Qty']
    df['Health Score'] = (100 - (df['Risk_Factor'] * 5.5)).clip(lower=5, upper=100).astype(int)
    return df

processed_df = get_intel(st.session_state.assets)

# --- 6. MAIN INTERFACE ---
tabs = st.tabs(["📝 Asset Inventory", "📅 Service Log", "📊 Predictive Intelligence"])

with tabs[0]:
    st.subheader("Asset Ledger & Bulk Import")
    up = st.file_uploader("Upload Master Excel", type="xlsx")
    if up: 
        st.session_state.assets = pd.read_excel(up)
        st.rerun()
    st.session_state.assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)

with tabs[1]:
    st.subheader("Next Maintenance Schedule")
    sched_df = processed_df.copy()
    sched_df['Due Date'] = (datetime.today() + timedelta(days=60)).strftime('%Y-%m-%d')
    st.dataframe(sched_df[['Asset', 'Last Service', 'Due Date', 'Health Score']], use_container_width=True)

# --- TAB 3: INTELLIGENCE & EXPORT (Based on your Images) ---
with tabs[2]:
    st.title("Predictive Risk Intelligence")
    
    # KPI Row
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Asset Risk (PKR)", f"Rs. {processed_df['Repair Cost'].sum():,.0f}")
    c2.metric("Critical Assets", len(processed_df[processed_df['Health Score'] < 50]))
    c3.metric("Avg Health Score", f"{int(processed_df['Health Score'].mean())}%")
    
    st.divider()
    
    # Visual Analytics Row
    left, right = st.columns([1.6, 1])
    
    with left:
        st.subheader("Executed Purchase & Repair Overview")
        # Professional Bar Chart
        fig = px.bar(processed_df, x='Asset', y='Repair Cost', 
                     color='Health Score', color_continuous_scale='Blues',
                     labels={'Repair Cost': 'Budget (PKR)'},
                     template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    
    with right:
        st.subheader("Health Score Breakdown")
        for _, r in processed_df.iterrows():
            st.write(f"**{r['Asset']}**")
            h_color = "red" if r['Health Score'] < 50 else "#1f4e79"
            st.markdown(f"<p style='color:{h_color}; font-weight:bold; margin-bottom:0;'>Score: {r['Health Score']}%</p>", unsafe_allow_html=True)
            st.progress(r['Health Score'] / 100)

    st.divider()
    
    # Document Export Center
    st.subheader("📥 Document Export Center")
    e1, e2, e3 = st.columns(3)
    
    with e1:
        admin_pdf = generate_report(processed_df, "EXECUTIVE ADMIN AUDIT", "ADMIN")
        st.download_button("Download Admin Audit", admin_pdf, "Admin_Audit.pdf", use_container_width=True)
            
    with e2:
        sum_pdf = generate_report(processed_df, "INSTITUTIONAL SUMMARY", "SUMMARY")
        st.download_button("Download Summary Report", sum_pdf, "Summary_Report.pdf", use_container_width=True)
            
    with e3:
        order_pdf = generate_report(processed_df, "MAINTENANCE PURCHASE ORDER", "ORDER")
        st.download_button("Generate Vendor Order", order_pdf, "Purchase_Order.pdf", use_container_width=True)

st.sidebar.divider()
st.sidebar.caption(f"Secure Portal v2.0 | {st.session_state.org_name}")
