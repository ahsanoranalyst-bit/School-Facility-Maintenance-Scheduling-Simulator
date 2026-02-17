import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fpdf import FPDF
import plotly.express as px

# --- 1. GLOBAL CONFIGURATION & BRANDING ---
MASTER_KEY = "Ahsan123"
PROJECT_ID = "PK_FACILITY_PRO_2026"

st.set_page_config(page_title="Facility Intelligence Suite", layout="wide", page_icon="🏢")

# Professional Blue Theme Styling
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-bottom: 4px solid #1f4e79; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #e1e4e8; border-radius: 5px; padding: 10px 25px; }
    .stTabs [aria-selected="true"] { background-color: #1f4e79 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'org_name' not in st.session_state: st.session_state.org_name = ""

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🛡️ System Activation")
        key = st.text_input("Enter License Key", type="password")
        if st.button("Unlock Portal", use_container_width=True):
            if key == MASTER_KEY:
                st.session_state.auth = True
                st.rerun()
            else: st.error("Invalid Activation Key.")
    st.stop()

if st.session_state.auth and not st.session_state.org_name:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🏫 Institution Registration")
        o_name = st.text_input("Enter Organization Name")
        if st.button("Complete Setup"):
            if o_name:
                st.session_state.org_name = o_name
                st.rerun()
    st.stop()

# --- 3. MULTI-REPORT PDF ENGINE (Strict DD-MM-YYYY) ---
class FacilityPDF(FPDF):
    def header(self):
        self.set_fill_color(31, 78, 121) 
        self.rect(0, 0, 210, 35, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 18)
        self.cell(0, 10, st.session_state.org_name.upper(), ln=True, align='C')
        self.set_font("Arial", '', 10)
        self.cell(0, 5, "Institutional Maintenance & Risk Audit", ln=True, align='C')
        self.ln(20)

def generate_multi_report(df, r_type):
    pdf = FacilityPDF()
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
   
    pdf.set_font("Arial", 'B', 14)
    titles = {"ADMIN": "EXECUTIVE AUDIT", "SUMMARY": "INSTITUTIONAL SUMMARY", "ORDER": "VENDOR PURCHASE ORDER"}
    pdf.cell(0, 10, titles[r_type], ln=True, align='L')
    pdf.set_font("Arial", 'I', 9)
    # Fixed Date Format [cite: 2026-02-10]
    pdf.cell(0, 5, f"Report Date: {datetime.now().strftime('%d-%m-%Y')}", ln=True)
    pdf.ln(5)

    pdf.set_fill_color(46, 117, 182) 
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 9)
   
    if r_type == "ORDER":
        cols = [("Asset Item", 90), ("Qty", 30), ("Status", 30), ("PKR Cost", 40)]
    else:
        cols = [("Asset Description", 60), ("Qty", 20), ("Risk (PKR)", 40), ("Health Score", 35), ("Next Date", 35)]

    for txt, w in cols: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 8)
    for _, row in df.iterrows():
        if r_type == "ORDER":
            pdf.cell(90, 8, str(row['Asset']), 1)
            pdf.cell(30, 8, str(row['Qty']), 1, 0, 'C')
            pdf.cell(30, 8, "Urgent" if row['Predictive Score'] < 45 else "Routine", 1, 0, 'C')
            pdf.cell(40, 8, f"{row['Est. Repair Cost']:,.0f}", 1, 1, 'R')
        else:
            pdf.cell(60, 8, str(row['Asset']), 1)
            pdf.cell(20, 8, str(row['Qty']), 1, 0, 'C')
            pdf.cell(40, 8, f"{row['Est. Repair Cost']:,.0f}", 1, 0, 'R')
            pdf.cell(35, 8, f"{row['Predictive Score']}%", 1, 0, 'C')
            # Format date in PDF [cite: 2026-02-10]
            n_date = pd.to_datetime(row['Next_Service']).strftime('%d-%m-%Y')
            pdf.cell(35, 8, n_date, 1, 1, 'C')
           
    return pdf.output(dest='S').encode('latin-1')

# --- 4. DATA LOGIC (Restored Initial State) ---
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame([
        {"Asset": "Air Conditioners", "Qty": 20, "Avg Age (Yrs)": 3, "Last Service": "01-10-2023", "Warranty": "01-01-2025"},
        {"Asset": "Computers", "Qty": 50, "Avg Age (Yrs)": 2, "Last Service": "15-01-2024", "Warranty": "01-06-2025"},
        {"Asset": "Plumbing System", "Qty": 1, "Avg Age (Yrs)": 15, "Last Service": "20-05-2022", "Warranty": "Expired"}
    ])

with st.sidebar:
    st.title(f"🏢 {st.session_state.org_name}")
    st.divider()
    labor_rate = st.number_input("Labor Rate (Rs/hr)", 100, 5000, 1500)
    # Profit level buffer 1-200 [cite: 2025-12-29]
    parts_markup = st.slider("Parts Buffer (%)", 1, 200, 20) / 100 
    if st.button("🔴 Logout"):
        st.session_state.clear()
        st.rerun()

tabs = st.tabs(["📋 Inventory Management", "📅 Service Schedule", "📊 Predictive Intelligence"])

with tabs[0]:
    st.subheader("Asset Health Ledger")
    
    # Restored Import Feature
    up = st.file_uploader("📂 Import Excel (XLSX)", type=["xlsx"])
    if up: st.session_state.assets = pd.read_excel(up)

    # Restored Manual Entry
    with st.expander("➕ Add New Asset Details"):
        with st.form("add_form"):
            c1, c2, c3 = st.columns(3)
            a_name = c1.text_input("Asset Name")
            a_qty = c2.number_input("Quantity", min_value=1)
            a_age = c3.number_input("Age (Yrs)", min_value=0.0)
            c4, c5 = st.columns(2)
            # Date format enforcement [cite: 2026-02-10]
            a_svc = c4.date_input("Last Service", format="DD/MM/YYYY")
            a_war = c5.date_input("Warranty Expiry", format="DD/MM/YYYY")
            if st.form_submit_button("Save Asset"):
                new_data = {"Asset": a_name, "Qty": a_qty, "Avg Age (Yrs)": a_age, 
                            "Last Service": a_svc.strftime('%d-%m-%Y'), 
                            "Warranty": a_war.strftime('%d-%m-%Y')}
                st.session_state.assets = pd.concat([st.session_state.assets, pd.DataFrame([new_data])], ignore_index=True)
                st.rerun()

    st.session_state.assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)

with tabs[1]:
    st.subheader("Maintenance Forecast (DD-MM-YYYY)")
    sched_df = st.session_state.assets.copy()
    
    # Fix timestamps and format strictly [cite: 2026-02-10]
    sched_df['Last Service'] = pd.to_datetime(sched_df['Last Service'], dayfirst=True)
    # Timing logic [cite: 2026-02-10]
    sched_df['Next_Service'] = sched_df.apply(lambda r: (r['Last Service'] + timedelta(days=180 if r['Avg Age (Yrs)'] > 5 else 365)).date(), axis=1)
    
    # Display table with fixed DD-MM-YYYY format
    display_df = sched_df[['Asset', 'Last Service', 'Next_Service']].copy()
    display_df['Last Service'] = display_df['Last Service'].dt.strftime('%d-%m-%Y')
    display_df['Next_Service'] = pd.to_datetime(display_df['Next_Service']).dt.strftime('%d-%m-%Y')
    st.dataframe(display_df, use_container_width=True)

with tabs[2]:
    st.title("Predictive Risk Intelligence")
   
    risk_df = sched_df.copy()
    risk_df['Risk_F'] = risk_df['Avg Age (Yrs)'] * risk_df['Warranty'].apply(lambda x: 1.7 if str(x).lower() == "expired" else 1.0)
    risk_df['Est. Repair Cost'] = (risk_df['Risk_F'] * 5500) * (1 + parts_markup) * risk_df['Qty']
    
    # 5. Predictive Score calculation [cite: 2026-02-14]
    risk_df['Predictive Score'] = (100 - (risk_df['Risk_F'] * 6)).clip(lower=5, upper=100).astype(int)

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Asset Risk (PKR)", f"Rs. {risk_df['Est. Repair Cost'].sum():,.0f}")
    m2.metric("Critical Assets", len(risk_df[risk_df['Predictive Score'] < 45]))
    m3.metric("System Health", f"{int(risk_df['Predictive Score'].mean())}%")

    st.divider()
   
    # Restored Relational Features (Progress bars and Professional Chart)
    col_chart, col_health = st.columns([1.6, 1])
    with col_chart:
        st.write("### Executed Purchase & Repair Overview")
        fig = px.bar(risk_df, x='Asset', y='Est. Repair Cost', color='Predictive Score', color_continuous_scale='Blues', template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
   
    with col_health:
        st.write("### Health Score Breakdown")
        for _, r in risk_df.iterrows():
            st.write(f"**{r['Asset']}**")
            st.progress(r['Predictive Score']/100)
   
    st.divider()
    st.subheader("📊 Document Export Center")
    c1, c2, c3 = st.columns(3)
    c1.download_button("📥 Admin Audit Report", generate_multi_report(risk_df, "ADMIN"), "Admin_Audit.pdf", use_container_width=True)
    c2.download_button("📥 Summary Report", generate_multi_report(risk_df, "SUMMARY"), "Summary.pdf", use_container_width=True)
    c3.download_button("📋 Vendor Order PDF", generate_multi_report(risk_df, "ORDER"), "Order.pdf", use_container_width=True)
