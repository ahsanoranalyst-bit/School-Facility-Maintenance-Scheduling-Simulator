import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from fpdf import FPDF

# --- 1. CONFIGURATION & AUTH (Feature from Code 1) ---
MASTER_KEY = "Ahsan123"
PROJECT_ID = "INV_SMART_2026"

st.set_page_config(page_title="Professional Inventory Forecaster", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'school_name' not in st.session_state: st.session_state.school_name = ""

# --- LOGIN SYSTEM ---
if not st.session_state.auth:
    st.title("🛡️ System Activation")
    auth_key = st.text_input("Enter License Key", type="password")
    if st.button("Unlock System", use_container_width=True):
        if auth_key == MASTER_KEY:
            st.session_state.auth = True
            st.rerun()
        else: st.error("Invalid Key!")
    st.stop()

if st.session_state.auth and not st.session_state.school_name:
    st.title("🏫 Organization Registration")
    s_name = st.text_input("Enter Organization Name")
    if st.button("Register & Proceed"):
        st.session_state.school_name = s_name
        st.rerun()
    st.stop()

# --- 2. SIDEBAR (Style from Code 1) ---
with st.sidebar:
    st.title(f"🏢 {st.session_state.school_name}")
    st.info(f"Project ID: {PROJECT_ID}")
   
    with st.expander("📈 Forecast Controls", expanded=True):
        multiplier = 1.8 if st.checkbox("Peak Season?") else 1.0
        lead_buffer = st.slider("Lead Time Buffer (Days)", 0, 15, 3)

    with st.expander("💰 Financial Settings", expanded=True):
        profit_percent = st.slider("Profit Markup (%)", 1, 200, 20)
        budget_cap = st.number_input("Total Budget Limit (PKR)", 1000, 10000000, 500000)

    if st.button("🔴 Logout", use_container_width=True):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- 3. PROFESSIONAL PDF GENERATOR ---
def generate_pdf(data_list, report_type, stats=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(31, 73, 125)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 12, st.session_state.school_name.upper(), ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"{report_type} REPORT - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
    pdf.ln(20)

    if report_type == "ADMIN" and stats:
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, " EXECUTIVE FINANCIAL SUMMARY", 0, 1, 'L', True)
        pdf.set_font("Arial", '', 10)
        pdf.ln(2)
        pdf.cell(63, 8, f" Total Investment: PKR {stats['total_p']:,.0f}", 0, 0)
        pdf.cell(63, 8, f" Est. Net Profit: PKR {stats['total_e']:,.0f}", 0, 0)
        pdf.cell(63, 8, f" Remaining Budget: PKR {stats['rem']:,.0f}", 0, 1)
        pdf.ln(5)

    pdf.set_fill_color(51, 122, 183)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 9)
   
    if report_type == "ADMIN":
        cols = [("Item", 55), ("Stock", 15), ("Score", 20), ("Cost", 30), ("Profit", 30), ("Total", 40)]
    else:
        cols = [("Item Name", 90), ("Order Qty", 40), ("Unit Price", 30), ("Subtotal", 30)]

    for txt, w in cols: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 8)
    for item in data_list:
        if report_type == "VENDOR" and "REORDER" not in item['Status']: continue
        if report_type == "ADMIN":
            pdf.cell(55, 8, str(item['Item']), 1)
            pdf.cell(15, 8, str(item['Stock']), 1, 0, 'C')
            pdf.cell(20, 8, f"{item['Score']}%", 1, 0, 'C')
            pdf.cell(30, 8, f"{item['Purchase_Cost']:,.0f}", 1, 0, 'R')
            pdf.cell(30, 8, f"{item['Profit']:,.0f}", 1, 0, 'R')
            pdf.cell(40, 8, f"{item['Revenue']:,.0f}", 1, 1, 'R')
        else:
            pdf.cell(90, 8, str(item['Item']), 1)
            pdf.cell(40, 8, str(item['MOQ']), 1, 0, 'C')
            pdf.cell(30, 8, f"{item['Unit_Price']:,.0f}", 1, 0, 'R')
            pdf.cell(30, 8, f"{item['Purchase_Cost']:,.0f}", 1, 1, 'R')
           
    return pdf.output(dest='S').encode('latin-1')

# --- 4. DATA INITIALIZATION (From Code 2) ---
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame(columns=["Item", "Current Qty", "Damage Rate (%)", "Unit Cost", "MOQ", "Lead Time"])

tabs = st.tabs(["📋 Management", "📊 Analytics", "💰 Financials"])

# --- TAB 1: MANAGEMENT ---
with tabs[0]:
    with st.expander("➕ Manual Entry Form", expanded=False):
        with st.form("manual_entry", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            f_item = c1.text_input("Item Name")
            f_qty = c2.number_input("Current Qty", 0)
            f_dmg = c3.number_input("Damage %", 0, 100, 2)
            c4, c5, c6 = st.columns(3)
            f_cst = c4.number_input("Unit Cost", 0)
            f_moq = c5.number_input("MOQ", 1)
            f_led = c6.number_input("Lead Days", 1)
            if st.form_submit_button("Add Item"):
                if f_item:
                    new_df = pd.DataFrame([{"Item": f_item, "Current Qty": f_qty, "Damage Rate (%)": f_dmg, "Unit Cost": f_cst, "MOQ": f_moq, "Lead Time": f_led}])
                    st.session_state.inventory_data = pd.concat([st.session_state.inventory_data, new_df], ignore_index=True)
                    st.rerun()

    uploaded_file = st.file_uploader("📂 Bulk Import Excel", type=["xlsx", "xls"])
    if uploaded_file:
        st.session_state.inventory_data = pd.read_excel(uploaded_file)

    st.subheader("Inventory Records")
    st.session_state.inventory_data = st.data_editor(st.session_state.inventory_data, num_rows="dynamic", use_container_width=True)

# --- CALCULATION ENGINE (Logic from Code 2) ---
results = []
for _, row in st.session_state.inventory_data.iterrows():
    p_cost = row['MOQ'] * row['Unit Cost']
    profit = p_cost * (profit_percent / 100)
    rev = p_cost + profit
   
    rop = (row['Current Qty'] * 0.05 * multiplier) * (row['Lead Time'] + lead_buffer)
    # Predictive Score (Point 5 from your rules)
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
        st.subheader("Performance Visualizations")
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("**Profit vs Cost Analysis**")
            st.bar_chart(res_df.set_index('Item')[['Purchase_Cost', 'Profit']])
        with g2:
            st.markdown("**Inventory Score Comparison**")
            st.line_chart(res_df.set_index('Item')['Score'])
       
        st.divider()
        st.subheader("Predictive Health Matrix") # 5th Point
        m_cols = st.columns(3)
        for i, row in res_df.iterrows():
            with m_cols[i % 3]:
                st.metric(row['Item'], f"{row['Score']}%", delta=row['Status'], delta_color="normal" if "HEALTHY" in row['Status'] else "inverse")
    else: st.info("Enter data to see analytics.")

# --- TAB 3: FINANCIALS ---
with tabs[2]:
    if not res_df.empty:
        t_p = res_df['Purchase_Cost'].sum()
        t_e = res_df['Profit'].sum()
        t_r = res_df['Revenue'].sum()
        rem = budget_cap - t_r

        st.subheader("Financial Summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Investment", f"PKR {t_p:,.0f}")
        c2.metric("Projected Profit", f"PKR {t_e:,.0f}", f"{profit_percent}% Markup")
        c3.metric("Market Revenue", f"PKR {t_r:,.0f}")

        st.divider()
        b1, b2 = st.columns(2)
        b1.metric("Budget Limit", f"PKR {budget_cap:,.0f}")
        b2.metric("Remaining Balance", f"PKR {rem:,.0f}", delta_color="normal" if rem >= 0 else "inverse")
        if rem < 0: st.error(f"Budget Exceeded by PKR {abs(rem):,.0f}")

        st.divider()
        st.subheader("Export Center")
        d1, d2 = st.columns(2)
       
        audit_stats = {'total_p': t_p, 'total_e': t_e, 'rem': rem}
        admin_pdf = generate_pdf(results, "ADMIN", stats=audit_stats)
        d1.download_button("📩 Download Full Admin Audit", admin_pdf, "Admin_Audit.pdf", use_container_width=True)
       
        vendor_pdf = generate_pdf(results, "VENDOR")
        d2.download_button("📦 Download Vendor Order (Reorders Only)", vendor_pdf, "Purchase_Order.pdf", use_container_width=True)
    else: st.info("Financial reports will appear here after data entry.")
