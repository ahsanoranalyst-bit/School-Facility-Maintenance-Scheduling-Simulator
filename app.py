import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(page_title="System Intelligence | Ahsan Khan", layout="wide", page_icon="💠")

# --- Links & Contact Details ---
website_url = "https://sysintel.vercel.app/"
whatsapp_url = "https://wa.me/923245277654"

# 2. Advanced UI Styling (CSS)
st.markdown(f"""
    <style>
    /* Main App Background */
    .stApp {{
        background: radial-gradient(circle at top right, #0a111a, #050505);
        color: #ccd6f6;
    }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: #0a111a !important;
        border-right: 2px solid #00f2ff;
    }}

    /* Sidebar Buttons */
    .sidebar-btn {{
        text-decoration: none;
        display: block;
        border: 1px solid #00f2ff;
        padding: 12px;
        text-align: center;
        border-radius: 10px;
        color: #00f2ff !important;
        font-weight: bold;
        margin-bottom: 12px;
        transition: 0.3s all;
    }}
    .sidebar-btn:hover {{
        background-color: #00f2ff !important;
        color: #050505 !important;
        box-shadow: 0 0 15px #00f2ff;
    }}

    /* Industry Cards */
    .portal-box {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 242, 255, 0.2);
        padding: 20px;
        border-radius: 15px 15px 0px 0px;
        text-align: center;
        height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .stButton>button {{
        width: 100% !important;
        background-color: rgba(0, 242, 255, 0.1) !important;
        color: #00f2ff !important;
        border: 1px solid #00f2ff !important;
        border-radius: 0px 0px 15px 15px !important;
        font-weight: bold !important;
        height: 50px !important;
    }}
    
    .stButton>button:hover {{
        background-color: #00f2ff !important;
        color: #050505 !important;
        box-shadow: 0 0 20px #00f2ff;
    }}

    /* Pricing Section */
    .pricing-card {{
        background: rgba(255, 255, 255, 0.02);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid rgba(0, 242, 255, 0.2);
        height: 100%;
    }}
    .premium-border {{ border: 2px solid #ffd700 !important; }}

    /* Payment Gateway Box (As per website) */
    .payment-box {{
        background: rgba(0, 0, 0, 0.4);
        padding: 15px;
        border-radius: 12px;
        border: 1px dashed #444;
        margin-top: 20px;
        text-align: left;
    }}
    .bank-row {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 5px;
    }}
    .bank-label {{ color: #888; font-size: 0.8rem; }}
    .bank-value {{ color: #fff; font-weight: bold; font-family: monospace; font-size: 0.9rem; }}

    /* Mobile Responsive Payment Fix */
    @media (max-width: 768px) {{
        .bank-row {{ flex-direction: column; gap: 2px; }}
        .bank-value {{ word-break: break-all; }}
    }}
    </style>
""", unsafe_allow_html=True)

# 3. State & Mapping
if 'selected_industry' not in st.session_state:
    st.session_state.selected_industry = None

industries = ["Agricultural", "Airline", "Bank", "Construction", "Diplomacy", "E-Commerce", "Education", "Energy Company", "Food Service", "Healthcare", "Hotel", "Insurance", "Manufacturing", "Military & Defense", "Pharmaceutical", "Real Estate", "Retail Chain", "Shipping Company", "Telecommunication", "Transmission", "Transportation"]

industry_map = {
    "Agricultural": "AGRI", "Airline": "AIRL", "Bank": "BANK", "Construction": "CONS",
    "Diplomacy": "DIPL", "E-Commerce": "ECOM", "Education": "EDUC", "Energy Company": "ENER",
    "Food Service": "FOOD", "Healthcare": "HEAL", "Hotel": "HOTE", "Insurance": "INSU",
    "Manufacturing": "MANU", "Military & Defense": "MILI", "Pharmaceutical": "PHAR",
    "Real Estate": "REAL", "Retail Chain": "RETA", "Shipping Company": "SHIP",
    "Telecommunication": "TELE", "Transmission": "TRANSM", "Transportation": "TRANSPO"
}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#00f2ff;'>CORE ENGINE</h2>", unsafe_allow_html=True)
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="sidebar-btn">💬 WHATSAPP SUPPORT</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="{website_url}" target="_blank" class="sidebar-btn">🌐 OFFICIAL WEBSITE</a>', unsafe_allow_html=True)
    st.markdown("---")
    
    if st.session_state.selected_industry:
        prefix = industry_map.get(st.session_state.selected_industry, "NONE")
        st.markdown(f"<h3 style='color:#00f2ff; text-align:center;'>📂 {st.session_state.selected_industry} Portal</h3>", unsafe_allow_html=True)
        
        if os.path.exists("pages"):
            files = sorted([f for f in os.listdir("pages") if f.upper().startswith(prefix)])
            st.markdown("<p style='color:#888; font-weight:bold; font-size:12px;'>STANDARD MODULES</p>", unsafe_allow_html=True)
            for f in files:
                if "PREM" not in f.upper():
                    name = f.replace(f"{prefix}_", "").replace(".py", "").replace("_", " ").title()
                    st.page_link(f"pages/{f}", label=f"🔓 {name}")
            
            st.markdown("<p style='color:#ffd700; font-weight:bold; font-size:12px; margin-top:15px;'>ENTERPRISE MODULES</p>", unsafe_allow_html=True)
            for f in files:
                if "PREM" in f.upper():
                    name = f.replace(f"{prefix}_", "").replace("PREM_", "").replace(".py", "").replace("_", " ").title()
                    st.page_link(f"pages/{f}", label=f"🔒 {name} (Locked)")

        st.markdown("---")
        if st.button("🏠 Exit to Dashboard", use_container_width=True):
            st.session_state.selected_industry = None
            st.rerun()

# --- MAIN DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>SYSTEM INTELLIGENCE</h1>", unsafe_allow_html=True)

if not st.session_state.selected_industry:
    # Industry Grid
    for i in range(0, len(industries), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(industries):
                name = industries[i+j]
                with cols[j]:
                    st.markdown(f'<div class="portal-box"><div style="color:white; font-size:20px; font-weight:bold;">{name}</div><div style="color:#00f2ff; font-size:11px; margin-top:5px;">OPTIMIZATION CORE</div></div>', unsafe_allow_html=True)
                    if st.button(f"Access Intelligence", key=f"btn_{i+j}", use_container_width=True):
                        st.session_state.selected_industry = name
                        st.rerun()

# --- NEW PAYMENT SECTION (Replacing Lemon Squeezy) ---
st.markdown("<br><h2 style='text-align:center; color:white;'>Secure License Activation</h2>", unsafe_allow_html=True)
p1, p2 = st.columns(2, gap="large")

payment_html = f"""
<div class="payment-box">
    <div class="bank-row"><span class="bank-label">Title:</span><span class="bank-value" style="color:#00a651">Ahsan Khan</span></div>
    <div class="bank-row"><span class="bank-label">Bank:</span><span class="bank-value">NayaPay (EMI) PK</span></div>
    <div class="bank-row"><span class="bank-label">IBAN:</span><span class="bank-value">PK93 NAYA 1234 5032 4527 7654</span></div>
</div>
<div style="text-align:center; margin-top:15px;">
    <a href="{whatsapp_url}" target="_blank" style="color:#00f2ff; text-decoration:none; font-weight:bold; font-size:14px;">🚀 Send Screenshot for Activation</a>
</div>
"""

with p1:
    st.markdown(f"""
    <div class="pricing-card">
        <h3 style="color:#bdc3c7; margin-bottom:5px;">BASIC CORE</h3>
        <div style="font-size: 28px; font-weight: bold;">$49 <span style="font-size:14px; color:#666; text-decoration:line-through;">$79</span></div>
        <p style="color:#00f2ff; font-size:13px;">Single Sector Access</p>
        {payment_html}
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown(f"""
    <div class="pricing-card premium-border">
        <h3 style="color:#ffd700; margin-bottom:5px;">TURBO STANDARD</h3>
        <div style="font-size: 28px; font-weight: bold;">$199 <span style="font-size:14px; color:#666; text-decoration:line-through;">$299</span></div>
        <p style="color:#ffd700; font-size:13px;">Full Sector Mastery</p>
        {payment_html}
    </div>
    """, unsafe_allow_html=True)
