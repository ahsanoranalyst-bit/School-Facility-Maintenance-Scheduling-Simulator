import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fpdf import FPDF
import io

# --- 1. GLOBAL CONFIGURATION & SECURITY ---
MASTER_KEY = "Ahsan123"
PROJECT_ID = "FAC_MAINT_PRO_2026"

st.set_page_config(
    page_title="Facility Intelligence & Maintenance Suite",
    layout="wide",
    page_icon="🛠️"
)

# Initialize Session States
if 'auth' not in st.session_state: st.session_state.auth = False
if 'org_name' not in st.session_state: st.session_state.org_name = ""
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame([
        {"Asset": "Air Conditioners", "Qty": 20, "Avg Age (Yrs)": 3, "Last Service": "2023-10-01", "Warranty": "2025-01-01"},
        {"Asset": "Computers", "Qty": 50, "Avg Age (Yrs)": 2, "Last Service": "2024-01-15", "Warranty": "2025-06-01"},
        {"Asset": "Plumbing System", "Qty": 1, "Avg Age (Yrs)": 15, "Last Service": "2022-05-20", "Warranty": "Expired"}
    ])

# --- 2. AUTHENTICATION GATEWAY ---
if not st.session_state.auth:
    st.container()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🛡️ Secure System Activation")
        st.markdown("Please enter your corporate license key to access the maintenance simulator.")
        auth_key = st.text_input("License Key", type="password", placeholder="••••••••")
        if st.button("Activate System", use_container_width=True):
            if auth_key == MASTER_KEY:
                st.session_state.auth = True
                st.success("System Authenticated Successfully!")
                st.rerun()
            else:
                st.error("Invalid License Key. Access Denied.")
    st.stop()

# Organization Setup
if st.session_state.auth and not st.session_state.org_name:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🏫 Organization Setup")
        o_name = st.text_input("Enter Institution/School Name", placeholder="e.g. Cambridge International")
        if st.button("Initialize Workspace"):
            if o_name:
                st.session_state.org_name = o_name
                st.rerun()
            else: st.warning("Organization name is mandatory.")
    st.stop()

# --- 3. PROFESSIONAL PDF ENGINE ---
def generate_professional_pdf(df, stats):
    pdf = FPDF()
    pdf.add_page()
    
    # Header Branding
    pdf.set_fill_color(20, 40, 80)
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 15, st.session_state.org_name.upper(), ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"EXECUTIVE FACILITY AUDIT - {datetime.now().strftime('%d %B %Y')}", ln=True, align='C')
    pdf.ln(25)

    # Financial Summary Box
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(245, 245, 245)
    pdf.cell(0, 12, " FINANCIAL RISK SUMMARY", 0, 1, 'L', True)
    pdf.set_font("Arial", '', 11)
    pdf.ln(2)
    pdf.cell(100, 8, f" Estimated Total Risk Value: ${stats['total_risk']:,.2f}", 0, 1)
    pdf.cell(100, 8, f" Project ID: {PROJECT_ID}", 0, 1)
    pdf.ln(10)

    # Data Table Header
    pdf.set_fill_color(40, 80, 120)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 9)
    headers = [("Asset Description", 60), ("Qty", 20), ("Age", 20), ("Estimated Cost", 45), ("Health Score", 35)]
    for txt, w in headers: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()

    # Data Table Body
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 9)
    for _, row in df.iterrows():
        pdf.cell(60, 9, str(row['Asset']), 1)
        pdf.cell(20, 9, str(row['Qty']), 1, 0, 'C')
        pdf.cell(20, 9, str(row['Avg Age (Yrs)']), 1, 0, 'C')
        pdf.cell(45, 9, f"${row['Est. Repair Cost']:,.2f}", 1, 0, 'R')
        pdf.cell(35, 9, f"{row['Predictive Score']}%", 1, 1, 'C')
        
    return pdf.output(dest='S').encode('latin-1')

# --- 4. SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3062/3062410.png", width=80)
    st.title(f"{st.session_state.org_name}")
    st.caption(f"Portal: {PROJECT_ID}")
    st.divider()

    with st.expander("💰 Budgetary Constants", expanded=True):
        labor_rate = st.number_input("Labor Rate ($/hr)", 10, 500, 45)
        parts_markup = st.slider("Parts Buffer (%)", 0, 100, 15) / 100

    with st.expander("📞 Vendor Directory", expanded=False):
        st.info("Emergency Contacts")
        st.text_area("Live Directory", "Electrician: 555-0101\nPlumber: 555-0202\nIT Support: 555-0303", height=100)

    st.divider()
    if st.button("🔴 Secure Logout", use_container_width=True):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- 5. MAIN WORKSPACE ---
tabs = st.tabs(["📋 Asset Management", "📅 Maintenance Schedule", "📊 Intelligence & Risk"])

# TAB 1: ASSET HEALTH & BULK IMPORT
with tabs[0]:
    st.subheader("Asset Inventory & Health Documentation")
    
    # Excel Import Logic
    c1, c2 = st.columns([2, 1])
    with c1:
        uploaded_file = st.file_uploader("📂 Bulk Import Master Inventory (Excel)", type=["xlsx"])
        if uploaded_file:
            st.session_state.assets = pd.read_excel(uploaded_file)
            st.success("Database Synchronized Successfully!")
    
    with c2:
        st.info("Note: Excel must contain columns: Asset, Qty, Avg Age (Yrs), Last Service, Warranty.")

    st.divider()
    st.write("### Live Asset Ledger")
    edited_assets = st.data_editor(
        st.session_state.assets, 
        num_rows="dynamic", 
        use_container_width=True
    )
    st.session_state.assets = edited_assets

# TAB 2: FORECASTED SCHEDULE
with tabs[1]:
    st.subheader("Routine Inspection Forecast")
    today = datetime.today()
    schedule_data = []
    
    for _, row in edited_assets.iterrows():
        try:
            last_dt = pd.to_datetime(row['Last Service'])
            interval = 180 if row['Avg Age (Yrs)'] > 5 else 365
            next_service = last_dt + timedelta(days=interval)
            days_remaining = (next_service - today).days
            
            schedule_data.append({
                "Asset Component": row['Asset'],
                "Next Scheduled Check": next_service.strftime("%Y-%m-%d"),
                "Priority Status": "🚨 CRITICAL" if days_remaining < 15 else "🟢 STABLE",
                "Days Until Due": days_remaining
            })
        except: continue
    
    st.table(pd.DataFrame(schedule_data))

# TAB 3: ANALYTICS & PDF REPORTING
with tabs[2]:
    st.subheader("Financial Intelligence & Predictive Scoring")
    
    risk_df = edited_assets.copy()
    # Logic: Age * Warranty Multiplier
    risk_df['Risk Factor'] = risk_df['Avg Age (Yrs)'] * risk_df['Warranty'].apply(lambda x: 1.5 if str(x).lower() == "expired" else 1.0)
    risk_df['Est. Repair Cost'] = (risk_df['Risk Factor'] * 100) * (1 + parts_markup)
    
    # 5th Point: Predictive Maintenance Score
    risk_df['Predictive Score'] = (100 - (risk_df['Risk Factor'] * 5)).clip(lower=0).astype(int)
    
    total_risk = risk_df['Est. Repair Cost'].sum()
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Facility Risk Value", f"${total_risk:,.2f}")
    kpi2.metric("Labor Overhead", f"${labor_rate}/hr")
    kpi3.metric("Critical Assets", len(risk_df[risk_df['Predictive Score'] < 40]))

    st.divider()
    
    col_chart, col_score = st.columns([2, 1])
    with col_chart:
        st.write("### Cost Exposure by Asset")
        st.bar_chart(risk_df.set_index("Asset")["Est. Repair Cost"])
    
    with col_score:
        st.write("### Predictive Health Scores")
        st.dataframe(risk_df[['Asset', 'Predictive Score']].sort_values(by="Predictive Score"), hide_index=True)

    st.divider()
    
    # Export Center
    st.write("### Report Export Center")
    report_stats = {'total_risk': total_risk}
    pdf_bytes = generate_professional_pdf(risk_df, report_stats)
    
    st.download_button(
        label="📥 Download Executive PDF Audit",
        data=pdf_bytes,
        file_name=f"{st.session_state.org_name}_Audit_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
