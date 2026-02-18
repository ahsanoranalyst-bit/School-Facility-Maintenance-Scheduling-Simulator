import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fpdf import FPDF
import plotly.express as px

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

# --- 3. UPDATED PDF ENGINE WITH FINANCIAL SUMMARY ---
class FacilityPDF(FPDF):
    def header(self):
        self.set_fill_color(31, 78, 121)
        self.rect(0, 0, 210, 35, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 18)
        self.cell(0, 10, st.session_state.org_name.upper(), ln=True, align='C')
        self.set_font("Arial", '', 10)
        self.cell(0, 5, "Detailed Financial & Maintenance Audit", ln=True, align='C')
        self.ln(20)

def generate_multi_report(df, r_type, budget_info):
    pdf = FacilityPDF()
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    
    # Financial Summary Section in PDF
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "FINANCIAL SUMMARY", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(90, 8, f"Initial Budget: Rs. {budget_info['total']:,.0f}", 1)
    pdf.cell(90, 8, f"Total Estimated Cost: Rs. {budget_info['spent']:,.0f}", 1, 1)
    pdf.cell(90, 8, f"Total Profit Margin: Rs. {budget_info['profit']:,.0f}", 1)
    pdf.cell(90, 8, f"Remaining Balance: Rs. {budget_info['remaining']:,.0f}", 1, 1)
    pdf.ln(10)

    # Table Logic
    pdf.set_font("Arial", 'B', 11)
    title = "EXECUTIVE SUMMARY REPORT"
    cols = [("Asset Item", 70), ("Qty", 20), ("Unit Cost", 30), ("Total Cost", 40), ("Health", 30)]
    
    pdf.cell(0, 10, title, ln=True, align='L')
    pdf.set_fill_color(46, 117, 182); pdf.set_text_color(255, 255, 255)
    for txt, w in cols: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()

    pdf.set_text_color(0, 0, 0); pdf.set_font("Arial", '', 9)
    for _, row in df.iterrows():
        pdf.cell(70, 8, str(row['Asset']), 1)
        pdf.cell(20, 8, str(int(row['Qty'])), 1, 0, 'C')
        pdf.cell(30, 8, f"{row['Service Cost']:,.0f}", 1, 0, 'R')
        pdf.cell(40, 8, f"{row['Final_Total']:,.0f}", 1, 0, 'R')
        pdf.cell(30, 8, f"{int(row['Predictive Score'])}%", 1, 1, 'C')
        
    return pdf.output(dest='S').encode('latin-1')

# --- 4. DATA INITIALIZATION ---
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame(columns=["Asset", "Qty", "Age Value", "Age Unit", "Service Cost", "Last Service", "Warranty"])

with st.sidebar:
    st.title(f"🏢 {st.session_state.org_name}")
    st.divider()
    
    # NEW: Budget Input
    total_budget = st.number_input("💰 Set Available Budget (Rs.)", min_value=0.0, value=1000000.0, step=1000.0)
    
    # Profit Slider
    profit_perc = st.slider("📈 Profit Margin (%)", 0, 200, 20)
    
    st.divider()
    if st.button("🔴 Logout"):
        st.session_state.clear()
        st.rerun()

# --- 5. MAIN INTERFACE ---
tabs = st.tabs(["📋 Inventory & Costs", "📊 Financial Analytics", "📅 Service Schedule"])

with tabs[0]:
    st.subheader("Asset Ledger with Manual Pricing")
    
    with st.expander("➕ Add New Asset & Set Price"):
        with st.form("add_form"):
            c1, c2, c3 = st.columns(3)
            a_name = c1.text_input("Asset Name")
            a_qty = c2.number_input("Quantity", min_value=1, value=1)
            a_cost = c3.number_input("Service Cost per Unit", min_value=0.0, value=5000.0)
            
            c4, c5 = st.columns(2)
            a_age_val = c4.number_input("Age Value", min_value=0.0, value=1.0)
            a_age_unit = c5.selectbox("Unit", ["Years", "Months"])
            
            if st.form_submit_button("Save Asset"):
                new_row = {"Asset": a_name, "Qty": a_qty, "Age Value": a_age_val, "Age Unit": a_age_unit, 
                           "Service Cost": a_cost, "Last Service": "01-01-2024", "Warranty": "Active"}
                st.session_state.assets = pd.concat([st.session_state.assets, pd.DataFrame([new_row])], ignore_index=True)
                st.rerun()

    st.session_state.assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)

with tabs[1]:
    st.title("Strategic Financial Analytics")
    df = st.session_state.assets.copy()
    
    if not df.empty:
        # Financial Calculations
        df['Base_Total'] = df['Qty'] * df['Service Cost']
        df['Profit_Amount'] = df['Base_Total'] * (profit_perc / 100)
        df['Final_Total'] = df['Base_Total'] + df['Profit_Amount']
        
        # Predictive Score Logic
        df['Years_Calc'] = df.apply(lambda r: r['Age Value'] if r['Age Unit'] == "Years" else r['Age Value'] / 12, axis=1)
        df['Predictive Score'] = (100 - (df['Years_Calc'] * 6)).clip(lower=5, upper=100).astype(int)

        total_spent = df['Final_Total'].sum()
        total_profit = df['Profit_Amount'].sum()
        remaining = total_budget - total_spent
        
        # Metrics Display
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Available Budget", f"Rs. {total_budget:,.0f}")
        m2.metric("Total Est. Cost", f"Rs. {total_spent:,.0f}", delta=f"-{total_spent:,.0f}", delta_color="inverse")
        m3.metric("Profit Earned", f"Rs. {total_profit:,.0f}")
        
        if remaining >= 0:
            m4.metric("Remaining Balance", f"Rs. {remaining:,.0f}", delta="Within Budget")
        else:
            m4.metric("Remaining Balance", f"Rs. {remaining:,.0f}", delta="Budget Overrun", delta_color="inverse")

        st.divider()
        
        # PDF Export with Financial Data
        budget_data = {"total": total_budget, "spent": total_spent, "profit": total_profit, "remaining": remaining}
        if st.download_button("📥 Download Financial Summary PDF", 
                               generate_multi_report(df, "SUMMARY", budget_data), 
                               "Financial_Summary.pdf"):
            st.success("Report Generated!")
    else:
        st.info("Please add assets to see financial analytics.")
