import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fpdf import FPDF
import plotly.express as px

# --- 1. GLOBAL SETTINGS ---
# Security key for system access
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
    st.session_state.assets = pd.DataFrame(columns=["Asset", "Qty", "Avg Age (Yrs)", "Service Cost", "Last Service", "Warranty"])

# --- 4. SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.title(f"🏢 {st.session_state.org_name}")
    st.divider()
    # Global Budget Input
    total_budget = st.number_input("💰 Total Available Budget (Rs.)", min_value=0.0, value=1000000.0)
    # Profit Margin Slider (Range 1-200) [cite: 2025-12-29]
    parts_markup = st.slider("Profit / Parts Buffer (%)", 1, 200, 20) / 100
    
    st.divider()
    if st.button("🔴 Logout"):
        st.session_state.clear()
        st.rerun()

# --- 5. MAIN INTERFACE (Corrected Tab Order) ---
# Inventory first, then Schedule, then Analytics
tabs = st.tabs(["📋 Inventory Management", "📅 Maintenance Schedule", "📊 Strategic Analytics"])

# --- TAB 1: INVENTORY MANAGEMENT ---
with tabs[0]:
    st.header("Asset Registry")
    with st.expander("➕ Register New Asset Details"):
        with st.form("asset_form"):
            c1, c2, c3 = st.columns(3)
            name = c1.text_input("Asset Name")
            qty = c2.number_input("Quantity", min_value=1, step=1)
            cost = c3.number_input("Service Cost Per Unit (Rs.)", min_value=0.0)
            
            c4, c5, c6 = st.columns(3)
            age_val = c4.number_input("Current Age (Years)", min_value=0.0)
            # Date forced to DD/MM/YYYY [cite: 2026-02-10]
            ls_date = c5.date_input("Last Service Date", format="DD/MM/YYYY")
            wr_date = c6.date_input("Warranty Expiry Date", format="DD/MM/YYYY")
            
            if st.form_submit_button("Add to Inventory"):
                new_data = {
                    "Asset": name, "Qty": qty, "Avg Age (Yrs)": age_val, 
                    "Service Cost": cost, 
                    "Last Service": ls_date.strftime('%d-%m-%Y'),
                    "Warranty": wr_date.strftime('%d-%m-%Y')
                }
                st.session_state.assets = pd.concat([st.session_state.assets, pd.DataFrame([new_data])], ignore_index=True)
                st.rerun()

    st.subheader("Inventory Ledger")
    st.session_state.assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)

# --- TAB 2: MAINTENANCE SCHEDULE ---
with tabs[1]:
    st.header("📅 Service Forecasting & Cycles")
    if not st.session_state.assets.empty:
        sched_df = st.session_state.assets.copy()
        # Ensure correct date parsing for calculation [cite: 2026-02-10]
        sched_df['Last Service Date'] = pd.to_datetime(sched_df['Last Service'], dayfirst=True, errors='coerce')
        
        # Maintenance timing logic (1 year cycle) [cite: 2026-02-10]
        sched_df['Next Service Due'] = (sched_df['Last Service Date'] + timedelta(days=365)).dt.strftime('%d-%m-%Y')
        
        st.table(sched_df[['Asset', 'Qty', 'Last Service', 'Next Service Due', 'Warranty']])
    else:
        st.info("Please add assets in the Inventory Management tab.")

# --- TAB 3: STRATEGIC ANALYTICS (FINANCIALS) ---
with tabs[2]:
    st.title("Strategic Risk & Financial Analytics")
    if not st.session_state.assets.empty:
        df = st.session_state.assets.copy()
        
        # Financial Calculations (Total Payments)
        df['Final_Cost'] = (df['Qty'] * df['Service Cost']) * (1 + parts_markup)
        
        # Predictive Score Calculation (Added as 5th Point) [cite: 2026-02-14]
        df['Risk_Factor'] = pd.to_numeric(df['Avg Age (Yrs)'], errors='coerce').fillna(0) * 1.5
        df['Predictive Score'] = (100 - (df['Risk_Factor'] * 5)).clip(lower=5, upper=100).astype(int)
        
        total_exp = df['Final_Cost'].sum()
        balance = total_budget - total_exp
        
        # Metrics Display (Shows full payment amounts clearly)
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Financial Exposure", f"Rs. {total_exp:,.2f}") 
        m2.metric("Remaining Balance", f"Rs. {balance:,.2f}")
        m3.metric("Critical Items", len(df[df['Predictive Score'] < 45]))
        m4.metric("Avg System Health", f"{int(df['Predictive Score'].mean())}%")
        m5.metric("Predictive Score", f"{int(df['Predictive Score'].min())}%") # 5th point
        
        st.divider()
        st.subheader("📊 Expense vs. Asset Health Distribution")
        # Visualizing full payments in chart
        fig = px.bar(df, x="Asset", y="Final_Cost", color="Predictive Score", 
                     color_continuous_scale='RdYlGn', 
                     labels={'Final_Cost': 'Total Cost (Rs.)'},
                     title="Asset-wise Maintenance Cost Analytics")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for analytics. Register assets first.")
