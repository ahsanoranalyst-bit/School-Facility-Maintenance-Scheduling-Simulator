


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

# --- 3. MULTI-REPORT PDF ENGINE (Updated with Financials) ---
class FacilityPDF(FPDF):
    def header(self):
        self.set_fill_color(31, 78, 121)
        self.rect(0, 0, 210, 35, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 18)
        self.cell(0, 10, st.session_state.org_name.upper(), ln=True, align='C')
        self.set_font("Arial", '', 10)
        self.cell(0, 5, "Institutional Maintenance & Financial Risk Audit", ln=True, align='C')
        self.ln(20)

def generate_multi_report(df, r_type, budget_info=None):
    pdf = FacilityPDF()
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 14)
    
    # Financial Summary Header for PDF
    if budget_info:
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 10, "FINANCIAL OVERVIEW", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.cell(90, 8, f"Initial Budget: Rs. {budget_info['total']:,.0f}", 1)
        pdf.cell(90, 8, f"Remaining: Rs. {budget_info['remaining']:,.0f}", 1, 1)
        pdf.ln(5)
   
    if r_type == "ADMIN":
        title, cols = "EXECUTIVE ADMINISTRATIVE AUDIT", [("Asset Item", 60), ("Qty", 20), ("Total Cost", 35), ("Health %", 30), ("Warranty", 40)]
    elif r_type == "SUMMARY":
        title, cols = "ASSEMBLY SUMMARY REPORT", [("Asset Item", 90), ("Quantity", 40), ("Health Score", 55)]
    else:
        title, cols = "CRITICAL BUNDLE & VENDOR ORDER", [("Critical Item", 80), ("Qty", 30), ("Priority", 35), ("Est. Cost", 40)]
        df = df[df['Predictive Score'] < 45]

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, title, ln=True, align='L')
    pdf.set_font("Arial", 'I', 9); pdf.cell(0, 5, f"Report Date: {datetime.now().strftime('%d-%m-%Y')}", ln=True); pdf.ln(5)

    pdf.set_fill_color(46, 117, 182); pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", 'B', 9)
    for txt, w in cols: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()

    pdf.set_text_color(0, 0, 0); pdf.set_font("Arial", '', 8)
    for _, row in df.iterrows():
        if r_type == "ADMIN":
            pdf.cell(60, 8, str(row['Asset']), 1); pdf.cell(20, 8, str(int(row['Qty'])), 1, 0, 'C')
            pdf.cell(35, 8, f"{row['Final_Cost']:,.0f}", 1, 0, 'R'); pdf.cell(30, 8, f"{int(row['Predictive Score'])}%", 1, 0, 'C')
            pdf.cell(40, 8, str(row['Warranty']), 1, 1, 'C')
        elif r_type == "SUMMARY":
            pdf.cell(90, 8, str(row['Asset']), 1); pdf.cell(40, 8, str(int(row['Qty'])), 1, 0, 'C')
            pdf.cell(55, 8, f"{int(row['Predictive Score'])}%", 1, 1, 'C')
        elif r_type == "ORDER":
            pdf.cell(80, 8, str(row['Asset']), 1); pdf.cell(30, 8, str(int(row['Qty'])), 1, 0, 'C')
            pdf.cell(35, 8, "CRITICAL", 1, 0, 'C'); pdf.cell(40, 8, f"{row['Final_Cost']:,.0f}", 1, 1, 'R')
    return pdf.output(dest='S').encode('latin-1')

# --- 4. DATA LOGIC ---
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame(columns=["Asset", "Qty", "Avg Age (Yrs)", "Service Cost", "Last Service", "Warranty"])

with st.sidebar:
    st.title(f"🏢 {st.session_state.org_name}")
    st.divider()
    # Manual Budget Input
    total_budget = st.number_input("💰 Total Available Budget (Rs.)", min_value=0.0, value=1000000.0)
    # Profit slider 1 to 200 [cite: 2025-12-29]
    parts_markup = st.slider("Profit / Parts Buffer (%)", 1, 200, 20) / 100
    
    # Driver Logic Persistence [cite: 2026-02-12]
    st.info("🚛 **Driver Schedule:**\n1. Pickup: Furthest first.\n2. Drop-off: Closest first.")
    
    if st.button("🔴 Logout"):
        st.session_state.clear()
        st.rerun()

tabs = st.tabs(["📋 Inventory Management", "📊 Strategic Analytics", "📅 Maintenance Schedule"])

with tabs[0]:
    st.subheader("Asset Health Ledger")
    
    with st.expander("➕ Add New Asset Details"):
        with st.form("add_form"):
            c1, c2, c3 = st.columns(3)
            a_name = c1.text_input("Asset Name")
            a_qty = c2.number_input("Quantity", min_value=1, value=1)
            # Manual Unit Cost - Replaces the fixed 5500
            a_cost = c3.number_input("Service Cost Per Unit (Rs.)", min_value=0.0, value=0.0)
            
            c4, c5, c6 = st.columns(3)
            a_age = c4.number_input("Age (Yrs)", min_value=0.0, value=1.0)
            # Date Inputs enforced in DD/MM/YYYY [cite: 2026-02-10]
            a_svc = c5.date_input("Last Service Date", format="DD/MM/YYYY")
            a_war = c6.date_input("Warranty Expiry", format="DD/MM/YYYY")
            
            if st.form_submit_button("Save Asset"):
                new_data = {"Asset": a_name, "Qty": a_qty, "Avg Age (Yrs)": a_age, "Service Cost": a_cost,
                            "Last Service": a_svc.strftime('%d-%m-%Y'),
                            "Warranty": a_war.strftime('%d-%m-%Y')}
                st.session_state.assets = pd.concat([st.session_state.assets, pd.DataFrame([new_data])], ignore_index=True)
                st.rerun()

    st.session_state.assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)

with tabs[1]:
    st.title("Strategic Risk & Financial Analytics")
    if not st.session_state.assets.empty:
        risk_df = st.session_state.assets.copy()
        risk_df['Avg Age (Yrs)'] = pd.to_numeric(risk_df['Avg Age (Yrs)'], errors='coerce').fillna(0)
        
        # Financial Logic
        risk_df['Final_Cost'] = (risk_df['Qty'] * risk_df['Service Cost']) * (1 + parts_markup)
        
        # Predictive Score as 5th Point [cite: 2026-02-14]
        risk_df['Risk_Factor'] = risk_df['Avg Age (Yrs)'] * 1.2
        risk_df['Predictive Score'] = (100 - (risk_df['Risk_Factor'] * 5)).clip(lower=5, upper=100).astype(int)

        total_spent = risk_df['Final_Cost'].sum()
        remaining_balance = total_budget - total_spent
        
        # 5 Dashboard Metrics
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Financial Exposure", f"Rs. {total_spent:,.0f}")
        m2.metric("Remaining Balance", f"Rs. {remaining_balance:,.0f}", delta=f"{ (remaining_balance/total_budget)*100:.1f}%")
        m3.metric("Critical Items", len(risk_df[risk_df['Predictive Score'] < 45]))
        m4.metric("Avg System Health", f"{int(risk_df['Predictive Score'].mean())}%")
        m5.metric("Predictive Score", f"{int(risk_df['Predictive Score'].min())}%", help="This is the 5th key predictive metric.")

        st.divider()
        st.subheader("📊 Expense vs. Asset Health")
        fig = px.bar(risk_df, x='Asset', y='Final_Cost', color='Predictive Score',
                     color_continuous_scale='RdYlGn', template="plotly_white", height=500)
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader("📥 Export Reports")
        budget_info = {"total": total_budget, "remaining": remaining_balance}
        c1, c2, c3 = st.columns(3)
        c1.download_button("Admin Audit", generate_multi_report(risk_df, "ADMIN", budget_info), "Admin_Audit.pdf", use_container_width=True)
        c2.download_button("Assembly Summary", generate_multi_report(risk_df, "SUMMARY"), "Summary.pdf", use_container_width=True)
        c3.download_button("Bundle Order", generate_multi_report(risk_df, "ORDER"), "Orders.pdf", use_container_width=True)
    else:
        st.info("No assets found. Add items in Inventory tab.")

with tabs[2]:
    st.subheader("Maintenance Forecast (DD-MM-YYYY)")
    if not st.session_state.assets.empty:
        sched_df = st.session_state.assets.copy()
        sched_df['Last Service Date'] = pd.to_datetime(sched_df['Last Service'], dayfirst=True, errors='coerce')
        
        # Timing based on kilometers/age as per instruction [cite: 2026-02-10]
        def calc_next(r):
            if pd.isna(r['Last Service Date']): return "N/A"
            days = 180 if r['Avg Age (Yrs)'] > 5 else 365
            return (r['Last Service Date'] + timedelta(days=days)).strftime('%d-%m-%Y')

        sched_df['Next Service Due'] = sched_df.apply(calc_next, axis=1)
        st.table(sched_df[['Asset', 'Qty', 'Last Service', 'Next Service Due', 'Warranty']])
