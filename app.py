
import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(page_title="System Intelligence | Ahsan Khan", layout="wide", page_icon="💠")

# --- Links & Pricing Details ---
basic_doc_url = "https://ahsankhan.lemonsqueezy.com/checkout/buy/ba3a76f7-4acc-4643-a838-9dc4085af6dc"
premium_doc_url = "https://ahsankhan.lemonsqueezy.com/checkout/buy/6245738f-4d29-4a0a-a574-e9a0e8838124"
website_url = "https://sysintel.vercel.app/"
whatsapp_url = "https://wa.me/923245277654"
google_url = "https://www.ahsanoranalyst.online/home"

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

    /* --- SIDEBAR BUTTONS GLOW EFFECT --- */
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
        transform: scale(1.02);
    }}

    /* --- MASTER GLOWING EFFECT FOR SIDEBAR PROJECTS --- */
    [data-testid="stSidebarNav"] ul li div a span,
    .stPageLink a p {{
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
        transition: 0.4s all ease-in-out;
    }}

    [data-testid="stSidebarNav"] ul li a:hover span,
    .stPageLink a:hover p {{
        color: #64ffda !important;
        text-shadow: 0 0 15px #64ffda, 0 0 25px #64ffda !important;
        transform: translateX(8px);
    }}

    /* --- PRICING CARDS ANIMATIONS --- */
    @keyframes silverPulse {{
        0% {{ border-color: #bdc3c7; box-shadow: 0 0 10px rgba(189, 195, 199, 0.3); }}
        50% {{ border-color: #ffffff; box-shadow: 0 0 25px rgba(255, 255, 255, 0.6); }}
        100% {{ border-color: #bdc3c7; box-shadow: 0 0 10px rgba(189, 195, 199, 0.3); }}
    }}
    @keyframes goldPulse {{
        0% {{ border-color: #ffd700; box-shadow: 0 0 10px rgba(255, 215, 0, 0.3); }}
        50% {{ border-color: #ffaa00; box-shadow: 0 0 25px rgba(255, 170, 0, 0.5); }}
        100% {{ border-color: #ffd700; box-shadow: 0 0 10px rgba(255, 215, 0, 0.3); }}
    }}

    /* --- INDUSTRY CARDS DESIGN --- */
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
        margin-bottom: 0px !important;
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
        margin-top: -1px !important;
    }}
   
    .stButton>button:hover {{
        background-color: white !important;
        color: #020c1b !important;
        box-shadow: 0 0 20px white;
    }}

    /* --- PRICING CARDS --- */
    .pricing-card {{
        background: #112240; padding: 40px; border-radius: 25px; text-align: center;
        display: flex; flex-direction: column; justify-content: space-between;
        height: 600px;
    }}
    .basic-card {{ border: 3px solid #bdc3c7 !important; animation: silverPulse 3s infinite ease-in-out; }}
    .premium-card {{ border: 3px solid #ffd700 !important; animation: goldPulse 2.5s infinite ease-in-out; }}

    .deploy-btn {{
        display: block; padding: 15px; border-radius: 12px; text-decoration: none !important;
        font-weight: 900; text-align: center; transition: 0.4s; margin-top: 20px;
    }}
    .basic-btn {{ border: 2px solid #bdc3c7; color: white !important; background: rgba(255,255,255,0.05); }}
    .basic-btn:hover {{ background: white !important; color: black !important; box-shadow: 0 0 20px white; }}
   
    .premium-btn {{ border: 2px solid #ffd700; color: #ffd700 !important; background: rgba(255, 215, 0, 0.05); }}
    .premium-btn:hover {{ background: #ffd700 !important; color: black !important; box-shadow: 0 0 20px #ffd700; }}
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
   
    # Glowing Action Buttons
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="sidebar-btn">💬 WHATSAPP SUPPORT</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="{website_url}" target="_blank" class="sidebar-btn">🌐 OFFICIAL WEBSITE</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="{website_url}" target="_blank" class="sidebar-btn">🌐 GOOGLE LIBARAY</a>', unsafe_allow_html=True)
    st.markdown("---")
   
    if st.session_state.selected_industry:
        prefix = industry_map.get(st.session_state.selected_industry, "NONE")
        st.markdown(f"<h3 style='color:#64ffda; text-align:center;'>📂 {st.session_state.selected_industry} Portal</h3>", unsafe_allow_html=True)
       
        # --- DYNAMIC PROJECT LOADER WITH LOCKING LOGIC ---
        if os.path.exists("pages"):
            files = sorted([f for f in os.listdir("pages") if f.upper().startswith(prefix)])
           
            # 1. STANDARD MODULES (UNLOCKED)
            st.markdown("<p style='color:#bdc3c7; font-weight:bold; font-size:12px; letter-spacing:1px;'>STANDARD MODULES</p>", unsafe_allow_html=True)
            for f in files:
                if "PREM" not in f.upper():
                    name = f.replace(f"{prefix}_", "").replace(".py", "").replace("_", " ").title()
                    st.page_link(f"pages/{f}", label=f"🔓 {name}")
           
            # 2. ENTERPRISE MODULES (LOCKED)
            st.markdown("<p style='color:#ffd700; font-weight:bold; font-size:12px; margin-top:15px; letter-spacing:1px;'>ENTERPRISE MODULES</p>", unsafe_allow_html=True)
           
            # Example of how to add a Locked Project manually or via naming
            # If a file in 'pages' folder has 'PREM' in its name, it shows here
            premium_found = False
            for f in files:
                if "PREM" in f.upper():
                    premium_found = True
                    name = f.replace(f"{prefix}_", "").replace("PREM_", "").replace(".py", "").replace("_", " ").title()
                    st.page_link(f"pages/{f}", label=f"🔒 {name} (Locked)")
           
            # Manual example if no file exists yet
            if not premium_found:
                st.markdown(f"<div style='font-size:14px; color:#ffd700; padding:5px; border-left:2px solid #ffd700; margin-left:5px;'>🔒 {st.session_state.selected_industry} Pro Optimizer (Premium)</div>", unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🏠 Exit to Dashboard", use_container_width=True):
            st.session_state.selected_industry = None
            st.rerun()

# --- MAIN DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#64ffda;'>SYSTEM INTELLIGENCE</h1>", unsafe_allow_html=True)

if not st.session_state.selected_industry:
    # YouTube Video Restored
    video_id = "aDIUEaVF8v4"
    st.markdown(f'<div style="width: 100%; height: 400px; border-radius: 20px; border: 3px solid #64ffda; overflow: hidden; position: relative; margin-bottom: 40px;"><iframe style="position: absolute; top: -65px; left: 0; width: 100%; height: calc(100% + 130px); pointer-events: none;" src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0" frameborder="0"></iframe></div>', unsafe_allow_html=True)

    # Industry Grid
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

# --- PRICING SECTION ---
st.markdown("<br><h2 style='text-align:center; color:white;'>Strategic License Deployment</h2>", unsafe_allow_html=True)
p1, p2 = st.columns(2, gap="large")

with p1:
    st.markdown(f"""
    <div class="pricing-card basic-card">
        <div>
            <h3 style="color:#bdc3c7;">Basic Core</h3>
            <div style="font-size: 32px; color: white; font-weight: bold;">$49 <span style="font-size:16px; color:#64ffda; text-decoration:line-through;">$79</span></div>
            <p style="color:#64ffda;">Standard Access - Save 23%</p>
            <ul style="color:white; text-align:left; list-style:none; padding:0; font-size:15px; line-height:2.6;">
                <li>✔ 1 Selected Sector Access</li><li>✔ 7 Base Optimization Projects</li><li>✔ Standard Logic Access</li>
                <li>✔ Email Support</li><li style="color:#bdc3c7;">✖ Full Library Access</li>
            </ul>
        </div>
        <a href="{basic_doc_url}" target="_blank" class="deploy-btn basic-btn">SELECT BASIC</a>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown(f"""
    <div class="pricing-card premium-card">
        <div>
            <h3 style="color:#ffd700;">Enterprise Pro</h3>
            <div style="font-size: 32px; color: white; font-weight: bold;">$499 <span style="font-size:16px; color:#ffd700; text-decoration:line-through;">$750</span></div>
            <p style="color:#ffd700;">Full Optimization Power - Save 27%</p>
            <ul style="color:white; text-align:left; list-style:none; padding:0; font-size:15px; line-height:2.6;">
                <li>✔ 3 Selected Sectors Access</li><li>✔ Complete Suite (All 3 Feilds)</li><li>✔ Custom Development Integration</li>
                <li>✔ 24/7 Dedicated Support </li><li style="color:#ffd700; font-weight:bold;">💎 Unlimited Full Access</li>
            </ul>
        </div>
        <a href="{premium_doc_url}" target="_blank" class="deploy-btn premium-btn">SELECT ELITE</a>
    </div>
    """, unsafe_allow_html=True)
