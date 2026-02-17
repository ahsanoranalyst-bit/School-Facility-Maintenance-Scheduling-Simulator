

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fpdf import FPDF
import io

# --- 1. GLOBAL CONFIGURATION & SECURITY ---
MASTER_KEY = "Ahsan123"
PROJECT_ID = "PK_FACILITY_PRO_2026"

st.set_page_config(
    page_title="Institutional Facility Management System",
    layout="wide",
    page_icon="🇵🇰"
)

# Initialize Session States
if 'auth' not in st.session_state: st.session_state.auth = False
if 'org_name' not in st.session_state: st.session_state.org_name = ""
if 'assets' not in st.session_state:
    # Default data in PKR
    st.session_state.assets = pd.DataFrame([
        {"Asset": "Split AC Units", "Qty": 20, "Avg Age (Yrs)": 3, "Last Service": "2023-10-01", "Warranty": "2025-01-01"},
        {"Asset": "Core i5 Computers", "Qty": 50, "Avg Age (Yrs)": 2, "Last Service": "2024-01-15", "Warranty": "2025-06-01"},
        {"Asset": "Main Water Boring", "Qty": 1, "Avg Age (Yrs)": 12, "Last Service": "2022-05-20", "Warranty": "Expired"},
        {"Asset": "UPS Backup System", "Qty": 5, "Avg Age (Yrs)": 4, "Last Service": "2023-12-01", "Warranty": "Expired"}
    ])

# --- 2. AUTHENTICATION GATEWAY ---
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("🛡️ Enterprise Activation")
        st.info("Authorized Personnel Only - Pakistan Region")
        auth_key = st.text_input("Enter License Key", type="password", placeholder="PK-XXXX-XXXX")
        if st.button("Activate License", use_container_width=True):
            if auth_key == MASTER_KEY:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid License Key. Please contact the administrator.")
    st.stop()

# Organization Setup
if st.session_state.auth and not st.session_state.org_name:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🏫 Organization Registration")
        o_name = st.text_input("Enter School/Institution Name", placeholder="e.g. Beaconhouse or Government College")
        if st.button("Complete Registration"):
            if o_name:
                st.session_state.org_name = o_name
                st.rerun()
            else: st.warning("Institution name is required for reporting.")
    st.stop()

# --- 3. PROFESSIONAL INSTITUTIONAL REPORT ENGINE ---
def generate_summary_pdf(df, stats):
    pdf = FPDF()
    pdf.add_page()
    
    # Official Letterhead Design
    pdf.set_fill_color(0, 102, 51) # Pakistani Green
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 22)
    pdf.cell(0, 15, st.session_state.org_name.upper(), ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"OFFICIAL FACILITY AUDIT & MAINTENANCE SUMMARY", ln=True, align='C')
    pdf.cell(0, 5, f"Issued Date: {datetime.now().strftime('%d %B, %Y')}", ln=True, align='C')
    pdf.ln(25)

    # Summary Dashboard
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(230, 240, 230)
    pdf.cell(0, 12, " 1. EXECUTIVE FINANCIAL OVERVIEW", 0, 1, 'L', True)
    pdf.set_font("Arial", '', 11)
    pdf.ln(2)
    pdf.cell(100, 8, f" Total Maintenance Risk Exposure: PKR {stats['total_risk']:,.2f}", 0, 1)
    pdf.cell(100, 8, f" Operational Budget Buffer: {stats['markup']}%", 0, 1)
    pdf.cell(100, 8, f" Total Asset Units Audited: {stats['total_qty']}", 0, 1)
    pdf.ln(10)

    # Table Header
    pdf.set_fill_color(40, 80, 120)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 9)
    headers = [("Asset Description", 60), ("Qty", 20), ("Age", 20), ("Risk Value (PKR)", 45), ("Health Score", 35)]
    for txt, w in headers: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()

    # Table Body
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 9)
    for _, row in df.iterrows():
        pdf.cell(60, 9, str(row['Asset']), 1)
        pdf.cell(20, 9, str(row['Qty']), 1, 0, 'C')
        pdf.cell(20, 9, str(row['Avg Age (Yrs)']), 1, 0, 'C')
        pdf.cell(45, 9, f"{row['Est. Repair Cost']:,.0f}", 1, 0, 'R')
        pdf.cell(35, 9, f"{row['Predictive Score']}%", 1, 1, 'C')

    # Footer
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "This is a computer-generated institutional report. No signature required.", 0, 0, 'C')
        
    return pdf.output(dest='S').encode('latin-1')

# --- 4. SIDEBAR (PKR LOCALIZATION) ---
with st.sidebar:
    st.title(f"🏢 {st.session_state.org_name}")
    st.caption(f"Portal ID: {PROJECT_ID}")
    st.divider()

    with st.expander("💰 Financial Settings (PKR)", expanded=True):
        labor_rate = st.number_input("Labor Rate (Rs/hr)", 100, 5000, 1500)
        parts_markup = st.slider("Parts Buffer (%)", 0, 100, 20) / 100

    with st.expander("📞 Emergency Directory", expanded=False):
        st.text_area("Contact List", "Electrician: 0300-1234567\nPlumber: 0321-9876543\nIT Support: 042-3555555", height=100)

    st.divider()
    if st.button("🔴 Secure Logout", use_container_width=True):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- 5. MAIN WORKSPACE ---
tabs = st.tabs(["📋 Master Inventory", "📅 Maintenance Schedule", "🧠 Intelligence & Analytics"])

# TAB 1: ASSET MANAGEMENT & EXCEL IMPORT
with tabs[0]:
    st.subheader("Asset Health & Documentation (PKR)")
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        uploaded_file = st.file_uploader("📂 Bulk Import Assets (Excel)", type=["xlsx"])
        if uploaded_file:
            st.session_state.assets = pd.read_excel(uploaded_file)
            st.success("Master Ledger Updated!")
    with col_b:
        st.info("Template columns: Asset, Qty, Avg Age (Yrs), Last Service, Warranty.")

    st.divider()
    edited_assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)
    st.session_state.assets = edited_assets

# TAB 2: FORECASTED SCHEDULE
with tabs[1]:
    st.subheader("Inspection Forecast (Next 365 Days)")
    today = datetime.today()
    schedule_data = []
    
    for _, row in edited_assets.iterrows():
        try:
            last_dt = pd.to_datetime(row['Last Service'])
            interval = 180 if row['Avg Age (Yrs)'] > 5 else 365
            next_service = last_dt + timedelta(days=interval)
            days_rem = (next_service - today).days
            
            schedule_data.append({
                "Asset": row['Asset'],
                "Next Service": next_service.strftime("%Y-%m-%d"),
                "Urgency": "🚨 URGENT" if days_rem < 15 else "🟢 STABLE",
                "Days Left": days_rem
            })
        except: continue
    
    st.dataframe(pd.DataFrame(schedule_data), use_container_width=True, hide_index=True)

# TAB 3: INTELLIGENCE & INSTITUTIONAL REPORTING
with tabs[2]:
    st.subheader("Predictive Risk Intelligence")
    
    risk_df = edited_assets.copy()
    # Risk logic for PKR values
    risk_df['Risk Factor'] = risk_df['Avg Age (Yrs)'] * risk_df['Warranty'].apply(lambda x: 1.8 if str(x).lower() == "expired" else 1.0)
    # Scaled repair cost to PKR (Base 5000 Rs per unit risk)
    risk_df['Est. Repair Cost'] = (risk_df['Risk Factor'] * 5000) * (1 + parts_markup) * risk_df['Qty']
    
    # 5. Predictive Maintenance Score (Higher Age = Lower Score)
    risk_df['Predictive Score'] = (100 - (risk_df['Risk Factor'] * 6)).clip(lower=5, upper=100).astype(int)
    
    total_risk = risk_df['Est. Repair Cost'].sum()
    
    # Analytics Dashboard
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Asset Risk (PKR)", f"Rs. {total_risk:,.0f}")
    k2.metric("Critical Assets", len(risk_df[risk_df['Predictive Score'] < 45]))
    k3.metric("Avg. Health Score", f"{int(risk_df['Predictive Score'].mean())}%")

    st.divider()
    
    g1, g2 = st.columns([2, 1])
    with g1:
        st.write("### Projected Expenditure (PKR)")
        st.bar_chart(risk_df.set_index("Asset")["Est. Repair Cost"])
    
    with g2:
        st.write("### Health Matrix")
        # Visual styling for the health matrix
        for _, r in risk_df.sort_values(by="Predictive Score").iterrows():
            st.write(f"**{r['Asset']}**")
            color = "red" if r['Predictive Score'] < 50 else "green"
            st.markdown(f"<span style='color:{color}'>Score: {r['Predictive Score']}%</span>", unsafe_allow_html=True)
            st.progress(r['Predictive Score']/100)

    st.divider()
    
    # INSTITUTIONAL REPORT SECTION
    st.write("### Institutional Audit Generation")
    col_rep1, col_rep2 = st.columns([2, 1])
    with col_rep1:
        st.success("Audit Summary Ready. This report is designed for submission to Board of Directors / Management.")
    
    with col_rep2:
        audit_stats = {
            'total_risk': total_risk, 
            'markup': parts_markup*100, 
            'total_qty': risk_df['Qty'].sum()
        }
        report_pdf = generate_summary_pdf(risk_df, audit_stats)
        
        st.download_button(
            label="📥 Download Official Institutional Summary",
            data=report_pdf,
            file_name=f"{st.session_state.org_name}_Summary_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
