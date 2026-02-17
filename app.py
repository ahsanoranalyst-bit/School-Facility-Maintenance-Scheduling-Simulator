


import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fpdf import FPDF
import io

# --- 1. GLOBAL CONFIGURATION ---
MASTER_KEY = "Ahsan123"
PROJECT_ID = "PK_FACILITY_PRO_2026"

st.set_page_config(page_title="Institutional Facility Management System", layout="wide", page_icon="🇵🇰")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'org_name' not in st.session_state: st.session_state.org_name = ""
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame([
        {"Asset": "Split AC Units", "Qty": 20, "Avg Age (Yrs)": 3, "Last Service": "2023-10-01", "Warranty": "2025-01-01"},
        {"Asset": "Core i5 Computers", "Qty": 50, "Avg Age (Yrs)": 2, "Last Service": "2024-01-15", "Warranty": "2025-06-01"},
        {"Asset": "Main Water Boring", "Qty": 1, "Avg Age (Yrs)": 12, "Last Service": "2022-05-20", "Warranty": "Expired"}
    ])

# --- 2. AUTHENTICATION ---
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🛡️ Enterprise Activation")
        auth_key = st.text_input("Enter License Key", type="password")
        if st.button("Activate License", use_container_width=True):
            if auth_key == MASTER_KEY:
                st.session_state.auth = True
                st.rerun()
            else: st.error("Invalid Key.")
    st.stop()

if st.session_state.auth and not st.session_state.org_name:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🏫 Institution Registration")
        o_name = st.text_input("Enter School/Institution Name")
        if st.button("Register"):
            if o_name:
                st.session_state.org_name = o_name
                st.rerun()
    st.stop()

# --- 3. ADVANCED PDF REPORT ENGINE ---
class FacilityPDF(FPDF):
    def header(self):
        self.set_fill_color(0, 102, 51) # PK Green
        self.rect(0, 0, 210, 35, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 18)
        self.cell(0, 10, st.session_state.org_name.upper(), ln=True, align='C')
        self.set_font("Arial", '', 10)
        self.cell(0, 5, "Institutional Maintenance & Risk Audit", ln=True, align='C')
        self.ln(20)

def generate_multi_report(df, r_type, stats):
    pdf = FacilityPDF()
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    
    # Title Section
    pdf.set_font("Arial", 'B', 14)
    titles = {
        "ADMIN": "EXECUTIVE AUDIT & RISK OVERVIEW",
        "SUMMARY": "INSTITUTIONAL MAINTENANCE SUMMARY",
        "ORDER": "MAINTENANCE PURCHASE ORDER (VENDORS)"
    }
    pdf.cell(0, 10, titles[r_type], ln=True, align='L')
    pdf.set_font("Arial", 'I', 9)
    pdf.cell(0, 5, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.ln(5)

    # Summary Dashboard
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 10, f" Key Metrics - Total Risk: PKR {stats['total_pkr']:,.0f} | Units: {stats['total_units']}", 0, 1, 'L', True)
    pdf.ln(5)

    # Table Setup
    pdf.set_fill_color(50, 50, 50)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 8)
    
    if r_type == "ORDER":
        cols = [("Asset Item", 90), ("Quantity", 30), ("Status", 30), ("Est. Cost", 40)]
    else:
        cols = [("Asset Description", 60), ("Qty", 20), ("Risk (PKR)", 40), ("Health Score", 35), ("Next Date", 35)]

    for txt, w in cols: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()

    # Table Data
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 8)
    for _, row in df.iterrows():
        if r_type == "ORDER" and row['Predictive Score'] > 50: continue # Only show urgent orders
        
        if r_type == "ORDER":
            pdf.cell(90, 8, str(row['Asset']), 1)
            pdf.cell(30, 8, str(row['Qty']), 1, 0, 'C')
            pdf.cell(30, 8, "Urgent" if row['Predictive Score'] < 40 else "Routine", 1, 0, 'C')
            pdf.cell(40, 8, f"{row['Est. Repair Cost']:,.0f}", 1, 1, 'R')
        else:
            pdf.cell(60, 8, str(row['Asset']), 1)
            pdf.cell(20, 8, str(row['Qty']), 1, 0, 'C')
            pdf.cell(40, 8, f"{row['Est. Repair Cost']:,.0f}", 1, 0, 'R')
            pdf.cell(35, 8, f"{row['Predictive Score']}%", 1, 0, 'C')
            pdf.cell(35, 8, str(row['Next_Service']), 1, 1, 'C')
            
    return pdf.output(dest='S').encode('latin-1')

# --- 4. DATA LOGIC ---
with st.sidebar:
    st.title(f"🏢 {st.session_state.org_name}")
    labor_rate = st.number_input("Labor Rate (Rs/hr)", 100, 5000, 1500)
    parts_markup = st.slider("Parts Buffer (%)", 0, 100, 20) / 100
    if st.button("🔴 Logout"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

tabs = st.tabs(["📋 Inventory Management", "📅 Service Schedule", "🧠 Intelligence Analytics"])

# --- TAB 1: MANAGEMENT ---
with tabs[0]:
    st.subheader("Asset Health Documentation")
    uploaded_file = st.file_uploader("📂 Import Master Excel", type=["xlsx"])
    if uploaded_file:
        st.session_state.assets = pd.read_excel(uploaded_file)
    
    edited_assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)
    st.session_state.assets = edited_assets

# --- TAB 2: SCHEDULING ---
with tabs[1]:
    st.subheader("Maintenance Forecast")
    today = datetime.today()
    schedule_list = []
    for i, row in edited_assets.iterrows():
        last_dt = pd.to_datetime(row['Last Service'])
        interval = 180 if row['Avg Age (Yrs)'] > 5 else 365
        nxt = (last_dt + timedelta(days=interval)).date()
        schedule_list.append(nxt)
    
    display_df = edited_assets.copy()
    display_df['Next_Service'] = schedule_list
    st.dataframe(display_df[['Asset', 'Last Service', 'Next_Service']], use_container_width=True)

# --- TAB 3: INTELLIGENCE ANALYTICS (PKR) ---
with tabs[2]:
    st.subheader("Predictive Risk Intelligence & Reports")
    
    # Advanced Intelligence Logic
    risk_df = edited_assets.copy()
    risk_df['Next_Service'] = schedule_list
    risk_df['Risk Factor'] = risk_df['Avg Age (Yrs)'] * risk_df['Warranty'].apply(lambda x: 1.8 if str(x).lower() == "expired" else 1.0)
    risk_df['Est. Repair Cost'] = (risk_df['Risk Factor'] * 5000) * (1 + parts_markup) * risk_df['Qty']
    risk_df['Predictive Score'] = (100 - (risk_df['Risk Factor'] * 6)).clip(lower=5, upper=100).astype(int)

    # Professional Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Asset Risk (PKR)", f"Rs. {risk_df['Est. Repair Cost'].sum():,.0f}")
    m2.metric("Critical Assets", len(risk_df[risk_df['Predictive Score'] < 45]))
    m3.metric("System Health", f"{int(risk_df['Predictive Score'].mean())}%")

    st.divider()
    
    # Visualization like the Image
    col_chart, col_health = st.columns([2, 1])
    with col_chart:
        st.write("### Executed Purchase & Repair Overview")
        st.bar_chart(risk_df.set_index("Asset")["Est. Repair Cost"])
    
    with col_health:
        st.write("### Health Score Breakdown")
        for _, r in risk_df.iterrows():
            st.write(f"**{r['Asset']}**")
            st.progress(r['Predictive Score']/100)
    
    st.divider()

    # MULTI-REPORT EXPORT SECTION (As per your request)
    st.subheader("📊 Document Export Center")
    exp_stats = {'total_pkr': risk_df['Est. Repair Cost'].sum(), 'total_units': risk_df['Qty'].sum()}
    
    c1, c2, c3 = st.columns(3)
    
    # 1. Admin Audit
    admin_pdf = generate_multi_report(risk_df, "ADMIN", exp_stats)
    c1.download_button("📥 Download Admin Audit", admin_pdf, "Admin_Audit.pdf", use_container_width=True)
    
    # 2. Institutional Summary (Assembly Report)
    summary_pdf = generate_multi_report(risk_df, "SUMMARY", exp_stats)
    c2.download_button("📥 Download Summary Report", summary_pdf, "Institution_Summary.pdf", use_container_width=True)
    
    # 3. Maintenance Order
    order_pdf = generate_multi_report(risk_df, "ORDER", exp_stats)
    c3.download_button("📋 Generate Vendor Order", order_pdf, "Maintenance_Order.pdf", use_container_width=True)
