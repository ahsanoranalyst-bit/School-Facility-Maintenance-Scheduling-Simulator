


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

# --- 3. UNIQUE PDF ENGINE (Admin, Summary, Vendor) ---
class FacilityPDF(FPDF):
    def header_design(self, title, color_rgb):
        self.set_fill_color(*color_rgb) 
        self.rect(0, 0, 210, 35, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, st.session_state.org_name.upper(), ln=True, align='C')
        self.set_font("Arial", 'B', 12)
        self.cell(0, 5, title, ln=True, align='C')
        self.ln(20)

def generate_admin_report(df):
    """منفرد ایڈمن رپورٹ: فوکس رسک اور ہیلتھ اسکور پر"""
    pdf = FacilityPDF()
    pdf.add_page()
    pdf.header_design("EXECUTIVE RISK & AUDIT REPORT", (31, 78, 121)) # Dark Blue
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%d-%m-%Y')}", ln=True) [cite: 2026-02-10]
    
    # Table Header
    pdf.set_fill_color(200, 200, 200)
    cols = [("Asset Name", 70), ("Health %", 30), ("Risk Level", 40), ("Audit Cost", 50)]
    for txt, w in cols: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()
    
    pdf.set_font("Arial", '', 9)
    for _, row in df.iterrows():
        score = int(row['Predictive Score']) [cite: 2026-02-14]
        risk_lvl = "CRITICAL" if score < 45 else "STABLE"
        pdf.cell(70, 8, str(row['Asset']), 1)
        pdf.cell(30, 8, f"{score}%", 1, 0, 'C')
        pdf.cell(40, 8, risk_lvl, 1, 0, 'C')
        pdf.cell(50, 8, f"{row['Est. Repair Cost']:,.0f}", 1, 1, 'R')
    return pdf.output(dest='S').encode('latin-1')

def generate_summary_report(df):
    """سمری رپورٹ: جیسا آپ نے کہا اسے ویسا ہی رکھا گیا ہے"""
    pdf = FacilityPDF()
    pdf.add_page()
    pdf.header_design("INSTITUTIONAL SUMMARY", (46, 117, 182))
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%d-%m-%Y')}", ln=True) [cite: 2026-02-10]
    
    for _, row in df.iterrows():
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 8, f"Asset: {row['Asset']}", ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 6, f"Qty: {int(row['Qty'])} | Next Service: {row['Next_Service']} | Score: {row['Predictive Score']}%", ln=True) [cite: 2026-02-14]
        pdf.ln(2)
    return pdf.output(dest='S').encode('latin-1')

def generate_vendor_report(df):
    """منفرد ونڈر رپورٹ: فوکس صرف کوانٹٹی اور کام کی تفصیل پر"""
    pdf = FacilityPDF()
    pdf.add_page()
    pdf.header_design("VENDOR PURCHASE & SERVICE ORDER", (34, 139, 34)) # Forest Green
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "Service Details for Maintenance Team", ln=True)
    
    # Table Header
    pdf.set_fill_color(220, 230, 210)
    cols = [("Required Item", 100), ("Quantity", 40), ("Priority", 50)]
    for txt, w in cols: pdf.cell(w, 10, txt, 1, 0, 'C', True)
    pdf.ln()
    
    pdf.set_font("Arial", '', 10)
    for _, row in df.iterrows():
        priority = "URGENT" if row['Predictive Score'] < 45 else "ROUTINE" [cite: 2026-02-14]
        pdf.cell(100, 10, f"Service for {row['Asset']}", 1)
        pdf.cell(40, 10, str(int(row['Qty'])), 1, 0, 'C')
        pdf.cell(50, 10, priority, 1, 1, 'C')
    return pdf.output(dest='S').encode('latin-1')

# --- 4. DATA LOGIC ---
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame([
        {"Asset": "Air Conditioners", "Qty": 20, "Avg Age (Yrs)": 3, "Last Service": "01-10-2023", "Warranty": "01-01-2025"},
        {"Asset": "Computers", "Qty": 50, "Avg Age (Yrs)": 2, "Last Service": "15-01-2024", "Warranty": "01-06-2025"},
        {"Asset": "Plumbing System", "Qty": 1, "Avg Age (Yrs)": 15, "Last Service": "20-05-2022", "Warranty": "Expired"}
    ])

with st.sidebar:
    st.title(f"🏢 {st.session_state.org_name}")
    st.divider()
    parts_markup = st.slider("Parts Buffer (%)", 1, 200, 20) / 100 [cite: 2025-12-29]
    st.info("🚛 Driver Schedule Rule:\nPick: Farthest ➔ Closest\nDrop: Closest ➔ Farthest [cite: 2026-02-12]")
    if st.button("🔴 Logout"):
        st.session_state.clear()
        st.rerun()

tabs = st.tabs(["📋 Inventory", "📅 Schedule", "📊 Intelligence"])

with tabs[0]:
    st.session_state.assets = st.data_editor(st.session_state.assets, num_rows="dynamic", use_container_width=True)

with tabs[1]:
    st.subheader("Maintenance Forecast (DD-MM-YYYY)")
    sched_df = st.session_state.assets.copy().dropna(subset=['Asset'])
    sched_df['Last Service Date'] = pd.to_datetime(sched_df['Last Service'], dayfirst=True, errors='coerce')
    
    def calc_next(r):
        if pd.isna(r['Last Service Date']): return None
        days = 180 if r['Avg Age (Yrs)'] > 5 else 365 [cite: 2026-02-10]
        return (r['Last Service Date'] + timedelta(days=days)).date()

    sched_df['Next_Service'] = sched_df.apply(calc_next, axis=1)
    
    display_df = sched_df[['Asset', 'Last Service', 'Next_Service']].copy()
    display_df['Last Service'] = pd.to_datetime(display_df['Last Service'], dayfirst=True, errors='coerce').dt.strftime('%d-%m-%Y') [cite: 2026-02-10]
    display_df['Next_Service'] = pd.to_datetime(display_df['Next_Service']).dt.strftime('%d-%m-%Y') [cite: 2026-02-10]
    st.dataframe(display_df.fillna("N/A"), use_container_width=True)

with tabs[2]:
    st.title("Intelligence Dashboard")
    risk_df = sched_df.copy()
    risk_df['Avg Age (Yrs)'] = pd.to_numeric(risk_df['Avg Age (Yrs)'], errors='coerce').fillna(0)
    risk_df['Qty'] = pd.to_numeric(risk_df['Qty'], errors='coerce').fillna(1)
    risk_df['Risk_F'] = risk_df['Avg Age (Yrs)'] * risk_df['Warranty'].apply(lambda x: 1.7 if str(x).lower() == "expired" else 1.0)
    risk_df['Est. Repair Cost'] = (risk_df['Risk_F'] * 5500) * (1 + parts_markup) * risk_df['Qty']
    
    # 5th Point: Predictive Score [cite: 2026-02-14]
    scores = (100 - (risk_df['Risk_F'] * 6)).clip(lower=5, upper=100)
    risk_df['Predictive Score'] = scores.fillna(50).astype(int)

    # Export Section
    st.subheader("📊 منفرد رپورٹس ڈاؤن لوڈ کریں")
    c1, c2, c3 = st.columns(3)
    c1.download_button("📥 Admin Audit Report", generate_admin_report(risk_df), "Admin_Audit.pdf", use_container_width=True)
    c2.download_button("📥 Summary Report", generate_summary_report(risk_df), "Summary_Report.pdf", use_container_width=True)
    c3.download_button("📋 Vendor Order PDF", generate_vendor_report(risk_df), "Vendor_Order.pdf", use_container_width=True)

    # Progress Bars
    for _, r in risk_df.iterrows():
        st.write(f"**{r['Asset']} Health**")
        st.progress(r['Predictive Score']/100)
