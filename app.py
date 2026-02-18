

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
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

# --- 3. DATA STORAGE ---
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame(columns=["Asset", "Qty", "Age Value", "Age Unit", "Service Cost", "Last Service", "Warranty"])

# --- 4. PDF ENGINE ---
class FacilityPDF(FPDF):
    def header(self):
        self.set_fill_color(31, 78, 121)
        self.rect(0, 0, 210, 35, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 18)
        self.cell(0, 10, st.session_state.org_name.upper(), ln=True, align='C')
        self.ln(20)

def generate_pdf_report(df, budget_info):
    pdf = FacilityPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "FINANCIAL AUDIT SUMMARY", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(60, 8, "Total Budget", 1); pdf.cell(130, 8, f"Rs. {budget_info['total']:,.0f}", 1, 1)
    pdf.cell(60, 8, "Final Expense", 1); pdf.cell(130, 8, f"Rs. {budget_info['spent']:,.0f}", 1, 1)
    pdf.cell(60, 8, "Remaining Balance", 1); pdf.cell(130, 8, f"Rs. {budget_info['remaining']:,.0f}", 1, 1)
    pdf.ln(10)
    return pdf.output(dest='S').encode('latin-1')

# --- 5. SIDEBAR (Maintaining All Features) ---
with st.sidebar:
    st.title(f"🏢 {st.session_state.org_name}")
    st.divider()
    total_budget = st.number_input("💰 Available Budget (Rs.)", min_value=0.0, value=1000000.0)
    profit_perc = st.slider("📈 Profit / Parts Buffer (%)", 1, 200, 20) #
    st.divider()
    if st.button("🔴 Logout"):
        st.session_state.clear()
        st.rerun()

# --- 6. MAIN INTERFACE ---
tabs = st.tabs(["📋 Inventory Management", "📊 Strategic Risk Analytics", "📅 Service Schedule"])

with tabs[0]:
    st.header("Asset Registry")
    with st.expander("➕ Register New Asset"):
        with st.form("asset_form"):
            c1, c2, c3 = st.columns(3)
            name = c1.text_input("Asset Name")
            qty = c2.number_input("Quantity", min_value=1, step=1)
            cost = c3.number_input("Service Cost Per Unit (Rs.)", min_value=0.0)
            
            c4, c5 = st.columns(2)
            age_val = c4.number_input("Current Age", min_value=0.0)
            age_unit = c5.selectbox("Time Unit", ["Years", "Months"])
            
            c6, c7 = st.columns(2)
            ls_date = c6.date_input("Last Service Date", format="DD/MM/YYYY")
            wr_date = c7.date_input("Warranty Expiry Date", format="DD/MM/YYYY")
            
            if st.form_submit_button("Add to Inventory"):
                new_data = {
                    "Asset": name, "Qty": qty, "Age Value": age_val, 
                    "Age Unit": age_unit, "Service Cost": cost, 
                    "Last Service": ls_date.strftime('%d-%m-%Y'), # Corrected format
                    "Warranty": wr_date.strftime('%d-%m-%Y') # Corrected format
                }
                st.session_state.assets = pd.concat([st.session_state.assets, pd.DataFrame([new_data])], ignore_index=True)
                st.rerun()

    st.subheader("Inventory Ledger")
    st.session_state.assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)

with tabs[1]:
    if not st.session_state.assets.empty:
        df = st.session_state.assets.copy()
        
        # Financial & Risk Logic
        df['Base_Total'] = df['Qty'] * df['Service Cost']
        df['Markup'] = df['Base_Total'] * (profit_perc / 100)
        df['Final_Total'] = df['Base_Total'] + df['Markup']
        
        # Predictive Score (5th Point)
        df['Years'] = df.apply(lambda x: x['Age Value'] if x['Age Unit']=="Years" else x['Age Value']/12, axis=1)
        df['Predictive Score'] = (100 - (df['Years'] * 7.5)).clip(lower=5, upper=100)
        
        total_exp = df['Final_Total'].sum()
        balance = total_budget - total_exp
        
        st.title("Strategic Risk Analytics")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Financial Exposure", f"Rs. {total_exp:,.0f}")
        m2.metric("Budget Remaining", f"Rs. {balance:,.0f}")
        m3.metric("Critical Assets", len(df[df['Predictive Score'] < 40]))
        m4.metric("Avg Health", f"{int(df['Predictive Score'].mean())}%")
        m5.metric("Predictive Score", f"{int(df['Predictive Score'].min())}%") #
        
        st.divider()
        st.subheader("📊 Risk vs. Repair Cost")
        fig = px.bar(df, x="Asset", y="Final_Total", color="Predictive Score", title="Maintenance Cost Analysis")
        st.plotly_chart(fig, use_container_width=True)
        
        pdf_bytes = generate_pdf_report(df, {"total": total_budget, "spent": total_exp, "remaining": balance})
        st.download_button("📥 Download Summary PDF", pdf_bytes, "Facility_Report.pdf")
    else:
        st.info("No data available.")

with tabs[2]:
    st.subheader("📅 Maintenance Timeline")
    if not st.session_state.assets.empty:
        # Simple Logic to show next due date (Just for visualization)
        df_sche = st.session_state.assets.copy()
        st.table(df_sche[["Asset", "Last Service", "Warranty"]])
