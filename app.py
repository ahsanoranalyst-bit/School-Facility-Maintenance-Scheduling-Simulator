import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="School Facility Maintenance Simulator", layout="wide")

st.title("🛠️ School Facility Maintenance & Scheduling Simulator")

# --- INITIAL DATA (Section A & B) ---
if 'assets' not in st.session_state:
    st.session_state.assets = pd.DataFrame([
        {"Asset": "Air Conditioners", "Qty": 20, "Avg Age (Yrs)": 3, "Last Service": "2023-10-01", "Warranty": "2025-01-01"},
        {"Asset": "Computers", "Qty": 50, "Avg Age (Yrs)": 2, "Last Service": "2024-01-15", "Warranty": "2025-06-01"},
        {"Asset": "Plumbing System", "Qty": 1, "Avg Age (Yrs)": 15, "Last Service": "2022-05-20", "Warranty": "Expired"},
        {"Asset": "Ceiling Fans", "Qty": 100, "Avg Age (Yrs)": 5, "Last Service": "2023-08-10", "Warranty": "Expired"}
    ])

# --- SIDEBAR: COSTS & CONTACTS (Section C & D) ---
with st.sidebar:
    st.header("Section D: Financial Estimates")
    labor_rate = st.number_input("External Labor Charge ($/hr)", 10, 200, 45)
    parts_markup = st.slider("Spare Parts Buffer (%)", 0, 50, 15) / 100

    st.header("Section C: Emergency Contacts")
    st.text_area("Contacts", "Electrician: 555-0101\nPlumber: 555-0202\nIT Support: 555-0303")

# --- MAIN INTERFACE ---
tab1, tab2, tab3 = st.tabs(["📋 Asset Inventory", "📅 Maintenance Schedule", "📉 Financial Risk"])

with tab1:
    st.subheader("Section A & B: Asset Health & Logs")
    edited_assets = st.data_editor(st.session_state.assets, num_rows="dynamic")
    st.session_state.assets = edited_assets

with tab2:
    st.subheader("Section C: Routine Inspection Forecast")
    
    # Logic: Predict next service based on age and last service
    today = datetime.today()
    schedule_data = []
    
    for _, row in edited_assets.iterrows():
        last_dt = datetime.strptime(row['Last Service'], "%Y-%m-%d")
        # Older assets need more frequent checks (e.g., every 6 months vs 12)
        interval = 180 if row['Avg Age (Yrs)'] > 5 else 365
        next_service = last_dt + timedelta(days=interval)
        
        days_until = (next_service - today).days
        
        schedule_data.append({
            "Asset": row['Asset'],
            "Next Inspection": next_service.strftime("%Y-%m-%d"),
            "Urgency": "High" if days_until < 15 else "Normal",
            "Days Remaining": days_until
        })
    
    st.table(pd.DataFrame(schedule_data))

with tab3:
    st.subheader("Section D: Projected Repair Costs")
    
    # Simulated Risk Analysis
    risk_df = edited_assets.copy()
    # Risk factor: Age * (1.5 if Warranty Expired else 1.0)
    risk_df['Risk Factor'] = risk_df['Avg Age (Yrs)'] * risk_df['Warranty'].apply(lambda x: 1.5 if x == "Expired" else 1.0)
    risk_df['Est. Repair Cost'] = (risk_df['Risk Factor'] * 100) * (1 + parts_markup)
    
    total_risk = risk_df['Est. Repair Cost'].sum()
    
    st.metric("Total Facility Risk Value", f"${total_risk:,.2f}")

    st.bar_chart(risk_df.set_index("Asset")["Est. Repair Cost"])
