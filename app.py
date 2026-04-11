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
        background: radial-gradient(circle at top right, #0a192f, #020c1b);
        color: #ccd6f6;
    }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: #112240 !important;
        border-right: 3px solid #64ffda;
    }}

    .sidebar-btn {{
        text-decoration: none;
        display: block;
        border: 1px solid #64ffda;
        padding: 12px;
        text-align: center;
        border-radius: 10px;
        color: white !important;
        font-weight: bold;
        margin-bottom: 12px;
        transition: 0.3s all ease-in-out;
    }}
    .sidebar-btn:hover {{
        background-color: #64ffda !important;
        color: #020c1b !important;
        box-shadow: 0 0 20px #64ffda;
    }}

    /* Industry Cards */
    .portal-box {{
        background: rgba(17,34,64,0.9);
        border: 2px solid #64ffda;
        padding: 20px;
        border-radius: 15px 15px 0px 0px;
        text-align: center;
        border-bottom: none !important;
        height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .stButton>button {{
        width: 100% !important;
        background-color: rgba(100, 255, 218, 0.1) !important;
        color: white !important;
        border: 2px solid #64ffda !important;
        border-top: none !important;
        border-radius: 0px 0px 15px 15px !important;
        font-weight: bold !important;
        height: 50px !important;
    }}

    /* Pricing Section Updates */
    .pricing-card {{
        background: #112240; padding: 30px; border-radius: 25px; text-align: center;
        display: flex; flex-direction: column; justify-content: space-between;
        height: 700px; /* Increased for payment details */
    }}
    .basic-card {{ border: 3px solid #bdc3c7 !important; }}
    .premium-card {{ border: 3px solid #ffd700 !important; }}

    /* Bank Details Styling */
    .bank-info-box {{
        background: rgba(0,0,0,0.3);
        padding: 15px;
        border-radius: 12px;
        border: 1px dashed rgba(100, 255, 218, 0.3);
        margin: 15px 0;
        text-align: left;
    }}
    .bank-line {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding-bottom: 3px;
        font-size: 0.85rem;
    }}
    .bank-label {{ color: #888; }}
    .bank-val {{ color: #fff; font-weight: bold; font-family: monospace; }}

    .whatsapp-notice {{
        display: block;
        background: #64ffda;
        color: #020c1b !important;
        padding: 12px;
        border-radius: 10px;
        text-decoration: none !important;
        font-weight: 800;
        margin-top: 10px;
        font-size: 0.9rem;
    }}

    /* Mobile Responsive */
    @media (max-width: 768px) {{
        .bank-line {{ flex-direction: column; }}
        .bank-val {{ word-break: break-all; }}
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
    st.markdown("<h2 style='text-align:center; color:#64ffda;'>CORE ENGINE</h2>", unsafe_allow_html=True)
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="sidebar-btn">💬 WHATSAPP SUPPORT</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="{website_url}" target="_blank" class="sidebar-btn">🌐 OFFICIAL WEBSITE</a>', unsafe_allow_html=True)
    st.markdown("---")
    
    if st.session_state.selected_industry:
        prefix = industry_map.get(st.session_state.selected_industry, "NONE")
        st.markdown(f"<h3 style='color:#64ffda; text-align:center;'>📂 {st.session_state.selected_industry} Portal</h3>", unsafe_allow_html=True)
        
        if os.path.exists("pages"):
            files = sorted([f for f in os.listdir("pages") if f.upper().startswith(prefix)])
            st.markdown("<p style='color:#bdc3c7; font-weight:bold; font-size:12px; letter-spacing:1px;'>STANDARD MODULES</p>", unsafe_allow_html=True)
            for f in files:
                if "PREM" not in f.upper():
                    name = f.replace(f"{prefix}_", "").replace(".py", "").replace("_", " ").title()
                    st.page_link(f"pages/{f}", label=f"🔓 {name}")
            
            st.markdown("<p style='color:#ffd700; font-weight:bold; font-size:12px; margin-top:15px; letter-spacing:1px;'>ENTERPRISE MODULES</p>", unsafe_allow_html=True)
            for f in files:
                if "PREM" in f.upper():
                    name = f.replace(f"{prefix}_", "").replace("PREM_", "").replace(".py", "").replace("_", " ").title()
                    st.page_link(f"pages/{f}", label=f"🔒 {name} (Locked)")

        st.markdown("---")
        if st.button("🏠 Exit to Dashboard", use_container_width=True):
            st.session_state.selected_industry = None
            st.rerun()

# --- MAIN DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#64ffda;'>SYSTEM INTELLIGENCE</h1>", unsafe_allow_html=True)

if not st.session_state.selected_industry:
    # YouTube Video (RETAINED)
    video_id = "aDIUEaVF8v4"
    st.markdown(f'<div style="width: 100%; height: 400px; border-radius: 20px; border: 3px solid #64ffda; overflow: hidden; position: relative; margin-bottom: 40px;"><iframe style="position: absolute; top: -65px; left: 0; width: 100%; height: calc(100% + 130px); pointer-events: none;" src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0" frameborder="0"></iframe></div>', unsafe_allow_html=True)

    # Industry Grid (RETAINED)
    for i in range(0, len(industries), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(industries):
                name = industries[i+j]
                with cols[j]:
                    st.markdown(f'<div class="portal-box"><div style="color:white; font-size:22px; font-weight:900;">{name}</div><div style="color:#64ffda; font-size:12px; font-weight:bold; margin-top:5px;">NEURAL ENGINE SYNC</div></div>', unsafe_allow_html=True)
                    if st.button(f"Access Intelligence Core", key=f"btn_{i+j}", use_container_width=True):
                        st.session_state.selected_industry = name
                        st.rerun()

# --- PRICING SECTION (UPDATED WITH BANKING) ---
st.markdown("<br><h2 style='text-align:center; color:white;'>Strategic License Deployment</h2>", unsafe_allow_html=True)

# Shared Banking HTML
bank_html = """
<div class="bank-info-box">
    <div class="bank-line"><span class="bank-label">Title:</span><span class="bank-val" style="color:#64ffda">Ahsan Khan</span></div>
    <div class="bank-line"><span class="bank-label">Bank:</span><span class="bank-val">NayaPay Pakistan</span></div>
    <div class="bank-line"><span class="bank-label">IBAN:</span><span class="bank-val">PK93 NAYA 1234 5032 4527 7654</span></div>
</div>
"""

p1, p2 = st.columns(2, gap="large")

with p1:
    st.markdown(f"""
    <div class="pricing-card basic-card">
        <div>
            <h3 style="color:#bdc3c7;">BASIC ANALYTICS</h3>
            <div style="font-size: 32px; color: white; font-weight: bold;">$116 <span style="font-size:16px; color:#64ffda; text-decoration:line-through;">$150</span></div>
            <p style="color:#64ffda;">Standard Access - Save 23%</p>
            <ul style="color:white; text-align:left; list-style:none; padding:0; font-size:14px; line-height:2;">
                <li>✔ Industry Standard Models</li><li>✔ Foundational Resource Planning</li>
                <li>✔ Up to 5 Projects Included</li>
            </ul>
        </div>
        {bank_html}
        <a href="{whatsapp_url}" target="_blank" class="whatsapp-notice">🚀 SEND SCREENSHOT TO ACTIVATE</a>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown(f"""
    <div class="pricing-card premium-card">
        <div>
            <h3 style="color:#ffd700;">PREMIUM ENTERPRISE</h3>
            <div style="font-size: 32px; color: white; font-weight: bold;">$399 <span style="font-size:16px; color:#ffd700; text-decoration:line-through;">$550</span></div>
            <p style="color:#ffd700;">Full Optimization Power - Save 27%</p>
            <ul style="color:white; text-align:left; list-style:none; padding:0; font-size:14px; line-height:2;">
                <li>✔ Full Profit Maximizer Suite</li><li>✔ Real-time Logistics Sync</li>
                <li>✔ 24/7 Priority Support</li><li>💎 Unlimited Full Access</li>
            </ul>
        </div>
        {bank_html}
        <a href="{whatsapp_url}" target="_blank" class="whatsapp-notice" style="background:#ffd700">💎 SEND SCREENSHOT TO ACTIVATE</a>
    </div>
    """, unsafe_allow_html=True)
