

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

# --- 3. MULTI-REPORT PDF ENGINE ---
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
    
    # 5th Point logic: Predictive Score/Health %
    if r_type == "ADMIN":
        title, cols = "EXECUTIVE ADMINISTRATIVE AUDIT", [("Asset Item", 60), ("Qty", 20), ("Risk Cost", 35), ("Health %", 30), ("Next Service", 40)]
    elif r_type == "SUMMARY":
        title, cols = "ASSEMBLY SUMMARY REPORT", [("Asset Item", 90), ("Quantity", 40), ("Health Score", 55)]
    else:
        title, cols = "CRITICAL BUNDLE & VENDOR ORDER", [("Critical Item", 80), ("Qty", 30), ("Priority", 35), ("Est. Cost", 40)]
        df = df[df['Predictive Score'] < 45]

    pdf.cell(0, 10, title, ln=True, align='L')
    pdf.set_font("Arial", 'I', 9); pdf.cell(0, 5, f"Report Date: {datetime.now().strftime('%d-%m-%Y')}", ln=True); pdf.ln(5)

    pdf.set_fill_color(46, 117, 182); pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", 'B', 9)
    for txt, w in cols: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()

    pdf.set_text_color(0, 0, 0); pdf.set_font("Arial", '', 8)
    for _, row in df.iterrows():
        # --- FIXED DATE FORMATTING FOR PDF (DD-MM-YYYY) ---
        n_date = pd.to_datetime(row['Next_Service']).strftime('%d-%m-%Y') if pd.notna(row['Next_Service']) else "N/A"
        
        if r_type == "ADMIN":
            pdf.cell(60, 8, str(row['Asset']), 1); pdf.cell(20, 8, str(int(row['Qty'])), 1, 0, 'C')
            pdf.cell(35, 8, f"{row['Est. Repair Cost']:,.0f}", 1, 0, 'R'); pdf.cell(30, 8, f"{int(row['Predictive Score'])}%", 1, 0, 'C')
            pdf.cell(40, 8, n_date, 1, 1, 'C') # Next Service in DD-MM-YYYY
        elif r_type == "SUMMARY":
            pdf.cell(90, 8, str(row['Asset']), 1); pdf.cell(40, 8, str(int(row['Qty'])), 1, 0, 'C')
            pdf.cell(55, 8, f"{int(row['Predictive Score'])}%", 1, 1, 'C')
        elif r_type == "ORDER":
            pdf.cell(80, 8, str(row['Asset']), 1); pdf.cell(30, 8, str(int(row['Qty'])), 1, 0, 'C')
            pdf.cell(35, 8, "CRITICAL", 1, 0, 'C'); pdf.cell(40, 8, f"{row['Est. Repair Cost']:,.0f}", 1, 1, 'R')
    return pdf.output(dest='S').encode('latin-1')

# --- 4. DATA LOGIC & SESSION STATE ---
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame([
        {"Asset": "Air Conditioners", "Qty": 20, "Avg Age (Yrs)": 3, "Last Service": "01-10-2023", "Warranty": "01-01-2025", "Term Value": 6, "Term Type": "Months"},
    ])

with st.sidebar:
    st.title(f"🏢 {st.session_state.org_name}")
    st.divider()
    st.subheader("💰 Financial Budget")
    starting_balance = st.number_input("Starting Balance", min_value=0, value=1000000)
    parts_markup = st.slider("Parts Buffer (%)", 1, 200, 20) / 100
    if st.button("🔴 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

tabs = st.tabs(["📋 Inventory Management", "📅 Service Schedule", "📊 Predictive Intelligence"])

with tabs[0]:
    st.subheader("Asset Health Ledger")
    up = st.file_uploader("📂 Import Assets", type=["xlsx", "csv"])
    if up:
        st.session_state.assets = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
        st.success("Database Updated!")

    with st.expander("➕ Register New Asset"):
        with st.form("add_form"):
            c1, c2, c3 = st.columns(3)
            a_name = c1.text_input("Asset Name")
            a_qty = c2.number_input("Quantity", min_value=1, value=1)
            a_age = c3.number_input("Age (Years)", min_value=0.0, value=1.0)
            
            c4, c5, c6, c7 = st.columns(4)
            a_svc = c4.date_input("Last Service Date")
            a_war = c5.date_input("Warranty Expiry")
            a_term_val = c6.number_input("Term Value", min_value=1, value=6)
            a_term_type = c7.selectbox("Term Type", ["Months", "Years"])
            
            if st.form_submit_button("Add to Ledger"):
                new_entry = {"Asset": a_name, "Qty": a_qty, "Avg Age (Yrs)": a_age,
                            "Last Service": a_svc.strftime('%d-%m-%Y'),
                            "Warranty": a_war.strftime('%d-%m-%Y'),
                            "Term Value": a_term_val, "Term Type": a_term_type}
                st.session_state.assets = pd.concat([st.session_state.assets, pd.DataFrame([new_entry])], ignore_index=True)
                st.rerun()

    st.session_state.assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)

with tabs[1]:
    st.subheader("Automated Service Forecast")
    sched_df = st.session_state.assets.copy().dropna(subset=['Asset'])
    sched_df['Last Service Date'] = pd.to_datetime(sched_df['Last Service'], dayfirst=True, errors='coerce')
    
    def calc_next(r):
        if pd.isna(r['Last Service Date']): return None
        val = int(r['Term Value'])
        days = val * 30 if r['Term Type'] == "Months" else val * 365
        return (r['Last Service Date'] + timedelta(days=days)).date()

    sched_df['Next_Service'] = sched_df.apply(calc_next, axis=1)
    display_df = sched_df[['Asset', 'Term Value', 'Term Type', 'Last Service', 'Next_Service']].copy()
    display_df['Next_Service'] = pd.to_datetime(display_df['Next_Service']).dt.strftime('%d-%m-%Y')
    st.dataframe(display_df.fillna("N/A"), use_container_width=True)

with tabs[2]:
    st.title("Strategic Risk Analytics")
    risk_df = sched_df.copy()
    risk_df['Avg Age (Yrs)'] = pd.to_numeric(risk_df['Avg Age (Yrs)'], errors='coerce').fillna(0)
    risk_df['Qty'] = pd.to_numeric(risk_df['Qty'], errors='coerce').fillna(1)
    
    risk_df['Risk_F'] = risk_df['Avg Age (Yrs)'] * risk_df['Warranty'].apply(lambda x: 1.7 if str(x).lower() == "expired" else 1.0)
    risk_df['Est. Repair Cost'] = (risk_df['Risk_F'] * 5500) * (1 + parts_markup) * risk_df['Qty']
    risk_df['Predictive Score'] = (100 - (risk_df['Risk_F'] * 6)).clip(lower=5, upper=100).astype(int)

    total_cost = risk_df['Est. Repair Cost'].sum()
    current_bal = starting_balance - total_cost

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Financial Exposure", f"{total_cost:,.0f}")
    m2.metric("Remaining Balance", f"{current_bal:,.0f}", delta=f"-{total_cost:,.0f}", delta_color="inverse")
    m3.metric("Critical Items", len(risk_df[risk_df['Predictive Score'] < 45]))
    m4.metric("Avg System Health", f"{int(risk_df['Predictive Score'].mean()) if not risk_df.empty else 0}%")

    st.divider()
    
    if not risk_df.empty:
        st.subheader("📥 Export Departmental Reports")
        c1, c2, c3 = st.columns(3)
        # Reports will now use the DD-MM-YYYY format for the service dates
        c1.download_button("Admin Audit Report", generate_multi_report(risk_df, "ADMIN"), "Admin_Audit.pdf", use_container_width=True)
        c2.download_button("Asset Summary PDF", generate_multi_report(risk_df, "SUMMARY"), "Summary.pdf", use_container_width=True)
        c3.download_button("Critical Orders List", generate_multi_report(risk_df, "ORDER"), "Orders.pdf", use_container_width=True)
