


import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fpdf import FPDF

# --- 1. CONFIGURATION & AUTH (Professional Framework) ---
MASTER_KEY = "Ahsan123"
PROJECT_ID = "FAC_MAINT_2026"

st.set_page_config(page_title="Facility Maintenance Suite", layout="wide", page_icon="🛠️")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'org_name' not in st.session_state: st.session_state.org_name = ""

# --- ACCESS CONTROL SYSTEM ---
if not st.session_state.auth:
    st.title("🛡️ Secure System Activation")
    auth_key = st.text_input("Enter License Key", type="password")
    if st.button("Unlock Management Suite", use_container_width=True):
        if auth_key == MASTER_KEY:
            st.session_state.auth = True
            st.rerun()
        else: st.error("Invalid Key! Access Denied.")
    st.stop()

if st.session_state.auth and not st.session_state.org_name:
    st.title("🏫 Institution Registration")
    o_name = st.text_input("Enter School/Organization Name")
    if st.button("Register & Initialize"):
        if o_name:
            st.session_state.org_name = o_name
            st.rerun()
        else: st.warning("Organization name is required.")
    st.stop()

# --- 2. PROFESSIONAL SIDEBAR ---
with st.sidebar:
    st.title(f"🏢 {st.session_state.org_name}")
    st.info(f"System ID: {PROJECT_ID}")
    st.divider()

    with st.expander("💰 Financial Parameters", expanded=True):
        labor_rate = st.number_input("Labor Charge ($/hr)", 10, 200, 45)
        parts_markup = st.slider("Parts Buffer (%)", 0, 50, 15) / 100

    with st.expander("📞 Emergency Network", expanded=False):
        st.text_area("Vendor Contacts", "Electrician: 555-0101\nPlumber: 555-0202\nIT Support: 555-0303", height=100)

    st.divider()
    if st.button("🔴 Secure Logout", use_container_width=True):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- 3. AUDIT REPORT GENERATOR (PDF) ---
def generate_audit_pdf(data_list, stats):
    pdf = FPDF()
    pdf.add_page()
    
    # Header Band
    pdf.set_fill_color(31, 73, 125)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, st.session_state.org_name.upper(), ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, f"FACILITY AUDIT REPORT - {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
    pdf.ln(25)

    # Executive Summary
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, " EXECUTIVE FINANCIAL SUMMARY", 0, 1, 'L', True)
    pdf.set_font("Arial", '', 10)
    pdf.ln(2)
    pdf.cell(90, 8, f" Total Facility Risk Value: ${stats['total_risk']:,.2f}", 0, 1)
    pdf.cell(90, 8, f" Labor Rate: ${labor_rate}/hr", 0, 1)
    pdf.ln(5)

    # Table Header
    pdf.set_fill_color(51, 122, 183)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 9)
    cols = [("Asset Name", 70), ("Quantity", 30), ("Age", 20), ("Risk Cost", 40), ("Status", 30)]
    for txt, w in cols: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()

    # Table Data
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 9)
    for _, row in data_list.iterrows():
        pdf.cell(70, 8, str(row['Asset']), 1)
        pdf.cell(30, 8, str(row['Qty']), 1, 0, 'C')
        pdf.cell(20, 8, str(row['Avg Age (Yrs)']), 1, 0, 'C')
        pdf.cell(40, 8, f"${row['Est. Repair Cost']:,.2f}", 1, 0, 'R')
        pdf.cell(30, 8, "Exp" if row['Warranty'] == "Expired" else "Active", 1, 1, 'C')
        
    return pdf.output(dest='S').encode('latin-1')

# --- 4. DATA OPS ---
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame([
        {"Asset": "Air Conditioners", "Qty": 20, "Avg Age (Yrs)": 3, "Last Service": "2023-10-01", "Warranty": "2025-01-01"},
        {"Asset": "Computers", "Qty": 50, "Avg Age (Yrs)": 2, "Last Service": "2024-01-15", "Warranty": "2025-06-01"},
        {"Asset": "Plumbing System", "Qty": 1, "Avg Age (Yrs)": 15, "Last Service": "2022-05-20", "Warranty": "Expired"},
        {"Asset": "Ceiling Fans", "Qty": 100, "Avg Age (Yrs)": 5, "Last Service": "2023-08-10", "Warranty": "Expired"}
    ])

tabs = st.tabs(["📋 Asset Inventory", "📅 Maintenance Schedule", "📊 Risk Analytics"])

# --- TAB 1: ASSET MANAGEMENT ---
with tabs[0]:
    st.subheader("Asset Health & Documentation")
    edited_assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)
    st.session_state.assets = edited_assets

# --- TAB 2: SCHEDULING ---
with tabs[1]:
    st.subheader("Routine Inspection Forecast")
    today = datetime.today()
    schedule_list = []
   
    for _, row in edited_assets.iterrows():
        try:
            last_dt = datetime.strptime(row['Last Service'], "%Y-%m-%d")
            interval = 180 if row['Avg Age (Yrs)'] > 5 else 365
            next_service = last_dt + timedelta(days=interval)
            days_until = (next_service - today).days
            
            schedule_list.append({
                "Asset": row['Asset'],
                "Next Inspection": next_service.strftime("%Y-%m-%d"),
                "Days Remaining": days_until,
                "Urgency": "🚨 High Priority" if days_until < 15 else "✅ Normal"
            })
        except: continue
   
    st.dataframe(pd.DataFrame(schedule_list), use_container_width=True)

# --- TAB 3: FINANCIAL RISK (Section D & Predictive Score) ---
with tabs[2]:
    st.subheader("Projected Maintenance Expenditure")
    
    risk_df = edited_assets.copy()
    risk_df['Risk Factor'] = risk_df['Avg Age (Yrs)'] * risk_df['Warranty'].apply(lambda x: 1.5 if x == "Expired" else 1.0)
    risk_df['Est. Repair Cost'] = (risk_df['Risk Factor'] * 100) * (1 + parts_markup)
    
    # 5. Predictive Maintenance Score (As per guideline)
    risk_df['Maintenance Score'] = (100 - (risk_df['Risk Factor'] * 5)).clip(lower=0)

    total_risk = risk_df['Est. Repair Cost'].sum()
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Total Facility Risk Value", f"${total_risk:,.2f}")
        st.divider()
        st.write("**Asset Condition (Predictive Score)**")
        for _, r in risk_df.iterrows():
            st.write(f"{r['Asset']}: {r['Maintenance Score']}%")
            st.progress(r['Maintenance Score']/100)

    with c2:
        st.bar_chart(risk_df.set_index("Asset")["Est. Repair Cost"])

    st.divider()
    st.subheader("Executive Exports")
    report_stats = {'total_risk': total_risk}
    pdf_data = generate_audit_pdf(risk_df, report_stats)
    st.download_button("📥 Download Executive Audit Report", pdf_data, "Facility_Audit.pdf", use_container_width=True)
