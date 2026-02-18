


import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from fpdf import FPDF

# --- 1. GLOBAL CONFIGURATION ---
MASTER_KEY = "Ahsan123"
st.set_page_config(page_title="Facility Intelligence Suite", layout="wide", page_icon="🏢")

# --- 2. AUTHENTICATION ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'org_name' not in st.session_state: st.session_state.org_name = ""

if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🛡️ System Activation")
        key = st.text_input("Enter License Key", type="password")
        if st.button("Unlock Portal"):
            if key == MASTER_KEY:
                st.session_state.auth = True
                st.rerun()
            else: st.error("Invalid Key.")
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

# --- 3. PDF REPORT ENGINE (ENGLISH) ---
class FacilityPDF(FPDF):
    def header(self):
        self.set_fill_color(31, 78, 121)
        self.rect(0, 0, 210, 35, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 18)
        self.cell(0, 10, st.session_state.org_name.upper(), ln=True, align='C')
        self.set_font("Arial", '', 10)
        self.cell(0, 5, "Asset Maintenance & Financial Audit Report", ln=True, align='C')
        self.ln(20)

def generate_pdf_report(df, budget_info):
    pdf = FacilityPDF()
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    
    # Financial Summary Table
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "FINANCIAL SUMMARY", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(60, 8, "Total Budget", 1); pdf.cell(130, 8, f"Rs. {budget_info['total']:,.0f}", 1, 1)
    pdf.cell(60, 8, "Projected Expense", 1); pdf.cell(130, 8, f"Rs. {budget_info['spent']:,.0f}", 1, 1)
    pdf.cell(60, 8, "Profit/Markup", 1); pdf.cell(130, 8, f"Rs. {budget_info['profit']:,.0f}", 1, 1)
    pdf.cell(60, 8, "Remaining Balance", 1); pdf.cell(130, 8, f"Rs. {budget_info['remaining']:,.0f}", 1, 1)
    pdf.ln(10)

    # Asset Table
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(60, 10, "Asset Name", 1, 0, 'C', True)
    pdf.cell(20, 10, "Qty", 1, 0, 'C', True)
    pdf.cell(40, 10, "Warranty Exp.", 1, 0, 'C', True)
    pdf.cell(40, 10, "Unit Cost", 1, 0, 'C', True)
    pdf.cell(30, 10, "Total", 1, 1, 'C', True)

    pdf.set_font("Arial", '', 9)
    for _, row in df.iterrows():
        pdf.cell(60, 8, str(row['Asset']), 1)
        pdf.cell(20, 8, str(row['Qty']), 1, 0, 'C')
        pdf.cell(40, 8, str(row['Warranty']), 1, 0, 'C')
        pdf.cell(40, 8, f"{row['Service Cost']:,.0f}", 1, 0, 'R')
        pdf.cell(30, 8, f"{row['Final_Total']:,.0f}", 1, 1, 'R')
        
    return pdf.output(dest='S').encode('latin-1')

# --- 4. DATA STORAGE ---
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame(columns=["Asset", "Qty", "Age Value", "Age Unit", "Service Cost", "Last Service", "Warranty"])

# --- 5. SIDEBAR CONTROLS ---
with st.sidebar:
    st.title(f"🏢 {st.session_state.org_name}")
    st.divider()
    total_budget = st.number_input("💰 Available Budget (Rs.)", min_value=0.0, value=1000000.0)
    profit_perc = st.slider("📈 Profit Margin (%)", 0, 200, 20)
    st.divider()
    if st.button("🔴 Logout"):
        st.session_state.clear()
        st.rerun()

# --- 6. MAIN CONTENT ---
tabs = st.tabs(["📋 Inventory Management", "📊 Financial Analytics", "📅 Service Schedules"])

with tabs[0]:
    st.header("Asset Registry")
    
    with st.expander("➕ Register New Asset"):
        with st.form("asset_form"):
            c1, c2, c3 = st.columns(3)
            name = c1.text_input("Asset Name")
            qty = c2.number_input("Quantity", min_value=1, step=1)
            cost = c3.number_input("Service Cost Per Unit (Rs.)", min_value=0.0)
            
            c4, c5, c6 = st.columns(3)
            age_val = c4.number_input("Current Age", min_value=0.0)
            age_unit = c5.selectbox("Time Unit", ["Years", "Months"])
            warranty = c6.date_input("Warranty Expiry Date")
            
            if st.form_submit_button("Add to Inventory"):
                new_data = {
                    "Asset": name, "Qty": qty, "Age Value": age_val, 
                    "Age Unit": age_unit, "Service Cost": cost, 
                    "Last Service": datetime.now().strftime('%Y-%m-%d'),
                    "Warranty": warranty.strftime('%Y-%m-%d')
                }
                st.session_state.assets = pd.concat([st.session_state.assets, pd.DataFrame([new_data])], ignore_index=True)
                st.rerun()

    st.subheader("Current Inventory Ledger")
    st.session_state.assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)

with tabs[1]:
    if not st.session_state.assets.empty:
        df = st.session_state.assets.copy()
        
        # Financial Logic
        df['Base_Total'] = df['Qty'] * df['Service Cost']
        df['Markup_Amount'] = df['Base_Total'] * (profit_perc / 100)
        df['Final_Total'] = df['Base_Total'] + df['Markup_Amount']
        
        # Predictive Health Score (Point 5)
        df['Years'] = df.apply(lambda x: x['Age Value'] if x['Age Unit']=="Years" else x['Age Value']/12, axis=1)
        df['Predictive Score'] = (100 - (df['Years'] * 7)).clip(lower=0, upper=100)
        
        total_exp = df['Final_Total'].sum()
        total_profit = df['Markup_Amount'].sum()
        balance = total_budget - total_exp
        
        # Dashboard Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Budget Balance", f"Rs. {balance:,.0f}", delta="Remaining")
        m2.metric("Total Expense", f"Rs. {total_exp:,.0f}", delta=f"Profit: {total_profit:,.0f}")
        m3.metric("Avg Asset Health", f"{int(df['Predictive Score'].mean())}%")
        
        st.divider()
        
        # Export
        budget_summary = {"total": total_budget, "spent": total_exp, "profit": total_profit, "remaining": balance}
        pdf_bytes = generate_pdf_report(df, budget_summary)
        st.download_button("📥 Download PDF Audit Report", pdf_bytes, "Maintenance_Report.pdf", "application/pdf")
        
    else:
        st.warning("No data available. Please add assets in the Inventory tab.")
