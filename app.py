import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(page_title="System Intelligence | Ahsan Khan", layout="wide", page_icon="💠")

# --- Direct Payment Links ---
basic_link = "https://ahsankhan.lemonsqueezy.com/checkout/buy/ba3a76f7-4acc-4643-a838-9dc4085af6dc"
turbo_link = "https://wa.me/923245277654" 
enterprise_link = "https://ahsankhan.lemonsqueezy.com/checkout/buy/6245738f-4d29-4a0a-a574-e9a0e8838124"
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
    
    /* --- ANIMATION: NEON BLINK/PULSE --- */
    @keyframes neonBlink {{
        0% {{ border-color: #64ffda; box-shadow: 0 0 5px #64ffda; }}
        50% {{ border-color: #fff; box-shadow: 0 0 20px #64ffda, 0 0 30px #64ffda; }}
        100% {{ border-color: #64ffda; box-shadow: 0 0 5px #64ffda; }}
    }}

    @keyframes goldBlink {{
        0% {{ border-color: #ffd700; box-shadow: 0 0 5px #ffd700; }}
        50% {{ border-color: #fff; box-shadow: 0 0 20px #ffd700, 0 0 30px #ffd700; }}
        100% {{ border-color: #ffd700; box-shadow: 0 0 5px #ffd700; }}
    }}

    /* Pricing Cards Base */
    .pricing-card {{
        background: #112240; padding: 30px; border-radius: 25px; text-align: center;
        display: flex; flex-direction: column; justify-content: space-between;
        height: 720px; transition: 0.4s; border: 2px solid rgba(100, 255, 218, 0.1);
    }}
    
    /* --- Applying Animations based on your UI images --- */
    .basic-card:hover {{ animation: neonBlink 1.5s infinite; }}
    .popular-card {{ border: 3px solid #64ffda !important; animation: neonBlink 2s infinite; }}
    .enterprise-card:hover {{ animation: goldBlink 1.5s infinite; }}

    /* Pricing Labels */
    .price-tag {{ margin: 15px 0; }}
    .old-price {{ text-decoration: line-through; color: #888; font-size: 1.1rem; }}
    .new-price {{ font-size: 2.5rem; color: #fff; font-weight: 900; }}
    .per-year {{ color: #64ffda; font-size: 0.8rem; font-weight: bold; letter-spacing: 1px; text-transform: uppercase; }}

    /* Bank Box Design from your Images */
    .bank-box {{
        background: rgba(0,0,0,0.3); padding: 15px; border-radius: 15px;
        text-align: left; border: 1px dashed rgba(100, 255, 218, 0.4); margin: 15px 0;
    }}
    .bank-row {{ display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.8rem; }}
    .bank-label {{ color: #888; }}
    .bank-value {{ color: #fff; font-weight: bold; font-family: monospace; }}

    /* --- BUTTONS: No White, Only Cyan/Gold --- */
    .plan-btn {{
        display: block; padding: 15px; border-radius: 12px; text-decoration: none !important;
        font-weight: 900; text-align: center; transition: 0.4s; text-transform: uppercase;
    }}
    .btn-cyan {{ border: 2px solid #64ffda; color: #64ffda !important; background: rgba(100, 255, 218, 0.05); }}
    .btn-cyan:hover {{ background: #64ffda !important; color: #020c1b !important; box-shadow: 0 0 20px #64ffda; }}
    
    .btn-gold {{ border: 2px solid #ffd700; color: #ffd700 !important; background: rgba(255, 215, 0, 0.05); }}
    .btn-gold:hover {{ background: #ffd700 !important; color: #020c1b !important; box-shadow: 0 0 20px #ffd700; }}

    /* Sidebar Fixes */
    [data-testid="stSidebar"] {{ background-color: #112240 !important; border-right: 3px solid #64ffda; }}
    .sidebar-btn {{
        text-decoration: none; display: block; border: 1px solid #64ffda;
        padding: 12px; text-align: center; border-radius: 10px;
        color: white !important; font-weight: bold; margin-bottom: 12px;
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
        st.markdown(f"<h3 style='color:#64ffda; text-align:center;'>📂 {st.session_state.selected_industry} Portal</h3>", unsafe_allow_html=True)
        # Dynamic project list
        if st.button("🏠 Exit to Dashboard", use_container_width=True):
            st.session_state.selected_industry = None
            st.rerun()

# --- MAIN DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#64ffda;'>SYSTEM INTELLIGENCE</h1>", unsafe_allow_html=True)

if not st.session_state.selected_industry:
    # Video Section
    video_id = "aDIUEaVF8v4"
    st.markdown(f'<div style="width: 100%; height: 400px; border-radius: 20px; border: 3px solid #64ffda; overflow: hidden; position: relative; margin-bottom: 40px;"><iframe style="position: absolute; top: -65px; left: 0; width: 100%; height: calc(100% + 130px); pointer-events: none;" src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0" frameborder="0"></iframe></div>', unsafe_allow_html=True)

    # Industry Grid
    for i in range(0, len(industries), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(industries):
                name = industries[i+j]
                with cols[j]:
                    st.markdown(f'<div style="background:rgba(17,34,64,0.9); border:2px solid #64ffda; padding:20px; border-radius:15px 15px 0 0; text-align:center; height:110px; display:flex; flex-direction:column; justify-content:center;"><div style="color:white; font-size:22px; font-weight:900;">{name}</div><div style="color:#64ffda; font-size:12px;">NEURAL ENGINE SYNC</div></div>', unsafe_allow_html=True)
                    if st.button(f"Access Intelligence Core", key=f"btn_{i+j}", use_container_width=True):
                        st.session_state.selected_industry = name
                        st.rerun()

# --- PRICING SECTION ---
st.markdown("<br><h2 style='text-align:center; color:white;'>Yearly Optimization Licenses</h2>", unsafe_allow_html=True)

bank_html = """
<div class="bank-box">
    <div class="bank-row"><span class="bank-label">Title:</span><span class="bank-value" style="color:#64ffda">Ahsan Khan</span></div>
    <div class="bank-row"><span class="bank-label">Bank:</span><span class="bank-value">NayaPay (EMI) PK</span></div>
    <div class="bank-row"><span class="bank-label">IBAN:</span><span class="bank-value">PK93 NAYA 1234 5032 4527 7654</span></div>
</div>
"""

p1, p2, p3 = st.columns(3, gap="medium")

with p1:
    st.markdown(f"""
    <div class="pricing-card basic-card">
        <div>
            <h3 style="color:#bdc3c7;">Basic Core</h3>
            <div class="price-tag"><span class="old-price">$79</span> <span class="new-price">$49</span></div>
            <span class="per-year">YEARLY / SINGLE SECTOR</span>
            <ul style="color:white; text-align:left; font-size:0.85rem; padding-left:15px; line-height:2;">
                <li>✔ 1 Selected Sector Access</li><li>✔ 7 Base Optimization Models</li><li>✔ Standard Analytics Shell</li>
            </ul>
        </div>
        {bank_html}
        <a href="{basic_link}" target="_blank" class="plan-btn btn-cyan">DEPLOY BASIC</a>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown(f"""
    <div class="pricing-card popular-card">
        <div style="background:#64ffda; color:#020c1b; font-size:0.7rem; font-weight:900; padding:3px 15px; border-radius:20px; width:fit-content; margin:-45px auto 10px auto; box-shadow: 0 0 10px #64ffda;">MOST POPULAR</div>
        <div>
            <h3 style="color:#fff;">Turbo Standard</h3>
            <div class="price-tag"><span class="old-price">$299</span> <span class="new-price">$199</span></div>
            <span class="per-year">YEARLY / SECTOR MASTERY</span>
            <ul style="color:white; text-align:left; font-size:0.85rem; padding-left:15px; line-height:2;">
                <li>✔ Full Library (1 Sector)</li><li>✔ Enterprise AI Core</li><li>✔ Priority WhatsApp Sync</li>
            </ul>
        </div>
        {bank_html}
        <a href="{turbo_link}" target="_blank" class="plan-btn btn-cyan" style="background:#64ffda; color:#020c1b !important;">GET TURBO ACCESS</a>
    </div>
    """, unsafe_allow_html=True)

with p3:
    st.markdown(f"""
    <div class="pricing-card enterprise-card">
        <div>
            <h3 style="color:#ffd700;">Enterprise Pro</h3>
            <div class="price-tag"><span class="old-price">$750</span> <span class="new-price">$499</span></div>
            <span class="per-year">YEARLY / MULTI-SECTOR</span>
            <ul style="color:white; text-align:left; font-size:0.85rem; padding-left:15px; line-height:2;">
                <li>✔ 3 Selected Sectors</li><li>✔ Custom Neural Integration</li><li>✔ 24/7 Dedicated Support</li>
            </ul>
        </div>
        {bank_html}
        <a href="{enterprise_link}" target="_blank" class="plan-btn btn-gold">SELECT ELITE</a>
    </div>
    """, unsafe_allow_html=True)
