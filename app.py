import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fpdf import FPDF
import plotly.express as px

# --- 1. GLOBAL SETTINGS ---
MASTER_KEY = "Ahsan123"
st.set_page_config(page_title="Facility Intelligence Suite", layout="wide", page_icon="🏢")

# --- 2. AUTHENTICATION SYSTEM ---
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
        self.cell(0, 5, "Asset Maintenance & Financial Audit Report", ln=True, align='C')
        self.ln(20)

def generate_multi_report(df, r_type, budget_info):
    pdf = FacilityPDF()
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    
    if r_type == "ADMIN":
        title, cols = "EXECUTIVE ADMINISTRATIVE AUDIT", [("Asset", 60), ("Qty", 20), ("Total Cost", 35), ("Health %", 30), ("Warranty", 40)]
    elif r_type == "SUMMARY":
        title, cols = "ASSEMBLY SUMMARY REPORT", [("Asset", 90), ("Quantity", 40), ("Health Score", 55)]
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

# --- 4. DATA STORAGE ---
if 'assets' not in st.session_state:
    # Columns aligned with user Excel sheet
    st.session_state.assets = pd.DataFrame(columns=["Asset", "Qty", "Age Value", "Age Unit", "Service Cost", "Last Service", "Warranty"])

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title(f"🏢 {st.session_state.org_name}")
    st.divider()
    total_budget = st.number_input("💰 Set Total Budget (Rs.)", min_value=0.0, value=1000000.0)
    # Profit level slider (1 to 200) [cite: 2025-12-29]
    parts_markup = st.slider("Profit / Parts Buffer (%)", 1, 200, 20) / 100
    st.divider()
    if st.button("🔴 Logout System"):
        st.session_state.clear()
        st.rerun()

# --- 6. MAIN INTERFACE ---
tabs = st.tabs(["📋 Inventory Management", "📅 Maintenance Schedule", "📊 Strategic Analytics"])

# --- TAB 1: INVENTORY MANAGEMENT ---
with tabs[0]:
    st.header("Asset Registry & Import")
    
    # Restored Excel/CSV Import with full column support
    up = st.file_uploader("📂 Import Assets from Excel/CSV", type=["xlsx", "csv"])
    if up:
        try:
            imported_df = pd.read_excel(up) if up.name.endswith('xlsx') else pd.read_csv(up)
            st.session_state.assets = imported_df
            st.success("Database Updated from File!")
        except Exception as e:
            st.error(f"Import failed: {e}")

    with st.expander("➕ Add New Asset Manually"):
        with st.form("manual_entry"):
            c1, c2, c3 = st.columns(3)
            name = c1.text_input("Asset Name")
            qty = c2.number_input("Quantity", min_value=1, step=1)
            cost = c3.number_input("Service Cost Per Unit (Rs.)", min_value=0.0)
            
            c4, c5 = st.columns(2)
            age_val = c4.number_input("Age Value", min_value=0.0)
            age_unit = c5.selectbox("Age Unit", ["Years", "Months"])
            
            c6, c7 = st.columns(2)
            ls_date = c6.date_input("Last Service Date", format="DD/MM/YYYY")
            wr_date = c7.date_input("Warranty Expiry Date", format="DD/MM/YYYY")
            
            if st.form_submit_button("Save to Inventory"):
                new_row = {
                    "Asset": name, "Qty": qty, "Age Value": age_val, 
                    "Age Unit": age_unit, "Service Cost": cost, 
                    "Last Service": ls_date.strftime('%d-%m-%Y'), 
                    "Warranty": wr_date.strftime('%d-%m-%Y')
                }
                st.session_state.assets = pd.concat([st.session_state.assets, pd.DataFrame([new_row])], ignore_index=True)
                st.rerun()
    
    st.subheader("Inventory Ledger")
    st.session_state.assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)

# --- TAB 2: MAINTENANCE SCHEDULE ---
with tabs[1]:
    st.header("📅 Service Forecasting")
    if not st.session_state.assets.empty:
        sched_df = st.session_state.assets.copy()
        # Enforce DD-MM-YYYY format [cite: 2026-02-10]
        sched_df['Last Service Date'] = pd.to_datetime(sched_df['Last Service'], dayfirst=True, errors='coerce')
        sched_df['Next Service Due'] = (sched_df['Last Service Date'] + timedelta(days=365)).dt.strftime('%d-%m-%Y')
        st.table(sched_df[['Asset', 'Qty', 'Last Service', 'Next Service Due', 'Warranty']])
    else:
        st.info("No data available. Please import or add assets.")

# --- TAB 3: STRATEGIC ANALYTICS ---
with tabs[2]:
    st.title("Strategic Risk & Financial Analytics")
    if not st.session_state.assets.empty:
        df = st.session_state.assets.copy()
        
        # Financial Logic
        df['Final_Cost'] = (pd.to_numeric(df['Qty'], errors='coerce').fillna(0) * pd.to_numeric(df['Service Cost'], errors='coerce').fillna(0)) * (1 + parts_markup)
        
        # Predictive Scoring Logic (Point 5)
        df['Years_Norm'] = df.apply(lambda x: x['Age Value'] if x['Age Unit'] == 'Years' else x['Age Value']/12, axis=1)
        df['Predictive Score'] = (100 - (df['Years_Norm'] * 5.5)).clip(lower=5, upper=100).astype(int)
        
        total_exp = df['Final_Cost'].sum()
        balance = total_budget - total_exp
        
        # High-visibility Metrics
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.markdown(f"**Financial Exposure** \n### Rs. {total_exp:,.0f}")
        m2.markdown(f"**Remaining Balance** \n### Rs. {balance:,.0f}")
        m3.markdown(f"**Critical Items** \n### {len(df[df['Predictive Score'] < 45])}")
        m4.markdown(f"**Avg System Health** \n### {int(df['Predictive Score'].mean())}%")
        m5.markdown(f"**Predictive Score** \n### {int(df['Predictive Score'].min())}%")
        
        st.divider()
        st.subheader("📊 Cost vs. Health Distribution")
        fig = px.bar(df, x="Asset", y="Final_Cost", color="Predictive Score", 
                     color_continuous_scale='RdYlGn', labels={'Final_Cost': 'Total Expense (Rs.)'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Restored PDF Reports
        st.divider()
        st.subheader("📥 Export Professional Reports")
        c1, c2, c3 = st.columns(3)
        b_info = {"total": total_budget, "spent": total_exp, "remaining": balance}
        c1.download_button("Admin Audit (PDF)", generate_multi_report(df, "ADMIN", b_info), "Admin_Audit.pdf", use_container_width=True)
        c2.download_button("Assembly Summary (PDF)", generate_multi_report(df, "SUMMARY", b_info), "Summary_Report.pdf", use_container_width=True)
        c3.download_button("Order Bundle (PDF)", generate_multi_report(df, "ORDER", b_info), "Order_Bundle.pdf", use_container_width=True)
    else:
        st.warning("Dashboard empty. Please register assets in Tab 1.")
