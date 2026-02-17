

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from fpdf import FPDF

# --- 1. CONFIGURATION & AUTH ---
MASTER_KEY = "Ahsan123"
PROJECT_ID = "INV_SMART_2026"

st.set_page_config(page_title="Executive Inventory Suite", layout="wide", page_icon="📊")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'school_name' not in st.session_state: st.session_state.school_name = ""

# --- LOGIN SYSTEM ---
if not st.session_state.auth:
    st.title("🛡️ Enterprise System Activation")
    auth_key = st.text_input("Enter License Key", type="password", help="Contact administrator for access.")
    if st.button("Unlock System", use_container_width=True):
        if auth_key == MASTER_KEY:
            st.session_state.auth = True
            st.success("Access Granted!")
            st.rerun()
        else: st.error("Invalid Key! Please check your credentials.")
    st.stop()

if st.session_state.auth and not st.session_state.school_name:
    st.title("🏫 Organization Registration")
    s_name = st.text_input("Enter Organization Name", placeholder="e.g. Global Tech Solutions")
    if st.button("Initialize Workspace"):
        if s_name:
            st.session_state.school_name = s_name
            st.rerun()
        else: st.warning("Please enter a valid organization name.")
    st.stop()

# --- 2. SIDEBAR CONTROLS ---
with st.sidebar:
    st.header(f"🏢 {st.session_state.school_name}")
    st.caption(f"Project ID: {PROJECT_ID}")
    st.divider()
   
    with st.expander("📈 Forecasting Parameters", expanded=True):
        multiplier = 1.8 if st.checkbox("Peak Season Mode") else 1.0
        lead_buffer = st.slider("Safety Buffer (Days)", 0, 15, 3)

    with st.expander("💰 Profit & Budgeting", expanded=True):
        # Guideline: Profit level 1 to 200
        profit_percent = st.slider("Profit Markup (%)", 1, 200, 20)
        budget_cap = st.number_input("Max Budget Limit (USD/PKR)", 1000, 10000000, 500000)

    st.sidebar_markdown("---")
    if st.button("🔴 Secure Logout", use_container_width=True):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- 3. PROFESSIONAL PDF GENERATOR ---
def generate_pdf(data_list, report_type, stats=None):
    pdf = FPDF()
    pdf.add_page()
   
    # Elegant Blue Header
    pdf.set_fill_color(20, 40, 80)
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 15, st.session_state.school_name.upper(), ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"{report_type} AUDIT REPORT", ln=True, align='C')
    pdf.cell(0, 5, f"Date: {datetime.now().strftime('%d %b, %Y | %H:%M')}", ln=True, align='C')
    pdf.ln(25)

    if report_type == "ADMIN" and stats:
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 12)
        pdf.set_fill_color(245, 245, 245)
        pdf.cell(0, 10, " EXECUTIVE FINANCIAL OVERVIEW", 0, 1, 'L', True)
        pdf.set_font("Arial", '', 10)
        pdf.ln(2)
        pdf.cell(63, 8, f" Total Investment: {stats['total_p']:,.0f}", 0, 0)
        pdf.cell(63, 8, f" Est. Profit: {stats['total_e']:,.0f}", 0, 0)
        pdf.cell(63, 8, f" Budget Delta: {stats['rem']:,.0f}", 0, 1)
        pdf.ln(5)

    # Table Header
    pdf.set_fill_color(40, 80, 120)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 9)
   
    if report_type == "ADMIN":
        # Point 5: Predictive Score included
        cols = [("Item Description", 50), ("Stock", 15), ("Pred. Score", 25), ("Cost", 30), ("Profit", 30), ("Total", 40)]
    else:
        cols = [("Item Name", 90), ("Order Qty", 40), ("Unit Cost", 30), ("Subtotal", 30)]

    for txt, w in cols: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()

    # Table Data
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 8)
    for item in data_list:
        if report_type == "VENDOR" and "REORDER" not in item['Status']: continue
       
        if report_type == "ADMIN":
            pdf.cell(50, 8, str(item['Item']), 1)
            pdf.cell(15, 8, str(item['Stock']), 1, 0, 'C')
            pdf.cell(25, 8, f"{item['Score']}%", 1, 0, 'C') 
            pdf.cell(30, 8, f"{item['Purchase_Cost']:,.0f}", 1, 0, 'R')
            pdf.cell(30, 8, f"{item['Profit']:,.0f}", 1, 0, 'R')
            pdf.cell(40, 8, f"{item['Revenue']:,.0f}", 1, 1, 'R')
        else:
            pdf.cell(90, 8, str(item['Item']), 1)
            pdf.cell(40, 8, str(item['MOQ']), 1, 0, 'C')
            pdf.cell(30, 8, f"{item['Unit_Price']:,.0f}", 1, 0, 'R')
            pdf.cell(30, 8, f"{item['Purchase_Cost']:,.0f}", 1, 1, 'R')
           
    return pdf.output(dest='S').encode('latin-1')

# --- 4. CORE APPLICATION TABS ---
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["Item", "Current Qty", "Damage Rate (%)", "Unit Cost", "MOQ", "Lead Time"])

tabs = st.tabs(["📋 Inventory Management", "📊 Smart Analytics", "💰 Financial Control"])

# --- TAB 1: MANAGEMENT ---
with tabs[0]:
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.subheader("Add New Asset")
        with st.form("manual_entry", clear_on_submit=True):
            f_item = st.text_input("Item Name")
            f_qty = st.number_input("Current Stock", 0)
            f_dmg = st.slider("Damage Rate (%)", 0, 100, 2)
            f_cst = st.number_input("Unit Purchase Cost", 0)
            f_moq = st.number_input("Reorder Quantity (MOQ)", 1)
            f_led = st.number_input("Lead Time (Days)", 1)
            if st.form_submit_button("➕ Register Item"):
                if f_item:
                    new_entry = pd.DataFrame([{"Item": f_item, "Current Qty": f_qty, "Damage Rate (%)": f_dmg, "Unit Cost": f_cst, "MOQ": f_moq, "Lead Time": f_led}])
                    st.session_state.inventory_data = pd.concat([st.session_state.inventory_data, new_entry], ignore_index=True)
                    st.rerun()

    with col_b:
        st.subheader("Bulk Import")
        uploaded_file = st.file_uploader("Upload Excel Spreadsheet", type=["xlsx"])
        if uploaded_file:
            st.session_state.inventory_data = pd.read_excel(uploaded_file)
            st.success("Master Data Synchronized!")

    st.divider()
    st.subheader("Inventory Master Ledger")
    st.session_state.inventory_data = st.data_editor(st.session_state.inventory_data, num_rows="dynamic", use_container_width=True)

# --- CALCULATION ENGINE ---
results = []
for _, row in st.session_state.inventory_data.iterrows():
    p_cost = row['MOQ'] * row['Unit Cost']
    profit = p_cost * (profit_percent / 100)
    rev = p_cost + profit
   
    rop = (row['Current Qty'] * 0.05 * multiplier) * (row['Lead Time'] + lead_buffer)
    # Predictive Score Calculation
    score = round((min(row['Current Qty']/(rop*2 if rop>0 else 1), 1.0)*100)*(1-(row['Damage Rate (%)']/100)), 1)
   
    results.append({
        "Item": row['Item'], "Stock": row['Current Qty'], "Score": score,
        "Status": "🚨 REORDER" if row['Current Qty'] <= rop else "✅ HEALTHY",
        "Purchase_Cost": p_cost, "Profit": profit, "Revenue": rev,
        "MOQ": row['MOQ'], "Unit_Price": row['Unit Cost']
    })
res_df = pd.DataFrame(results)

# --- TAB 2: ANALYTICS ---
with tabs[1]:
    if not res_df.empty:
        st.subheader("Predictive Health & Performance")
        m_cols = st.columns(3)
        for i, row in res_df.iterrows():
            with m_cols[i % 3]:
                # Predictive Score highlighted as per instructions
                st.metric(
                    label=f"🎯 {row['Item']}", 
                    value=f"Score: {row['Score']}%", 
                    delta=row['Status'], 
                    delta_color="normal" if "HEALTHY" in row['Status'] else "inverse"
                )
        
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.bar_chart(res_df.set_index('Item')[['Purchase_Cost', 'Profit']])
            st.caption("Investment vs Profit Distribution")
        with c2:
            st.line_chart(res_df.set_index('Item')['Score'])
            st.caption("Item Health Score Comparison")
    else: st.info("Enter data to generate predictive insights.")

# --- TAB 3: FINANCIALS ---
with tabs[2]:
    if not res_df.empty:
        t_p = res_df['Purchase_Cost'].sum()
        t_e = res_df['Profit'].sum()
        t_r = res_df['Revenue'].sum()
        rem = budget_cap - t_r

        st.subheader("Financial Performance Dashboard")
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Investment", f"{t_p:,.0f}")
        kpi2.metric("Projected Profit", f"{t_e:,.0f}", f"{profit_percent}% Markup")
        kpi3.metric("Projected Revenue", f"{t_r:,.0f}")

        st.divider()
        b1, b2 = st.columns(2)
        b1.metric("Budget Allocation", f"{budget_cap:,.0f}")
        b2.metric("Balance Available", f"{rem:,.0f}", delta_color="normal" if rem >= 0 else "inverse")
        
        if rem < 0: 
            st.error(f"⚠️ Budget Alert: Threshold exceeded by {abs(rem):,.0f}")

        st.divider()
        st.subheader("Export Center")
        d1, d2 = st.columns(2)
       
        audit_stats = {'total_p': t_p, 'total_e': t_e, 'rem': rem}
        admin_pdf = generate_pdf(results, "ADMIN", stats=audit_stats)
        d1.download_button("📥 Export Admin Financial Audit", admin_pdf, "Admin_Report.pdf", use_container_width=True)
       
        vendor_pdf = generate_pdf(results, "VENDOR")
        d2.download_button("📦 Export Vendor Purchase Order", vendor_pdf, "Purchase_Order.pdf", use_container_width=True)
    else: st.info("Financial summaries will appear once inventory records are added.")
