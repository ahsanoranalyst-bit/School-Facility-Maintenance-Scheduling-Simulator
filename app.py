import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(page_title="System Intelligence | Ahsan Khan", layout="wide", page_icon="💠")

# --- Links & Pricing Details ---
basic_doc_url = "https://ahsankhan.lemonsqueezy.com/checkout/buy/ba3a76f7-4acc-4643-a838-9dc4085af6dc"
premium_doc_url = "https://ahsankhan.lemonsqueezy.com/checkout/buy/6245738f-4d29-4a0a-a574-e9a0e8838124"
website_url = "https://www.ahsanoranalyst.online/"
whatsapp_url = "https://wa.me/923245277654"

# 2. Modern UI Styling (CSS)
st.markdown(f"""
    <style>
    /* Global Styles */
    .stApp {{
        background: radial-gradient(circle at top center, #0a111a 0%, #050505 100%);
        color: #ffffff;
    }}

    /* --- LOGO BLINKING EFFECT --- */
    .logo-container {{
        text-align: center;
        padding: 20px;
    }}
    .logo-ring {{
        width: 100px; height: 100px; margin: 0 auto;
        border: 2px solid #00f2ff; border-radius: 50%;
        display: flex; justify-content: center; align-items: center;
        background: rgba(0, 0, 0, 0.8);
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
        transition: all 0.4s ease;
        animation: blink-glow 1.5s infinite alternate;
    }}
    @keyframes blink-glow {{
        from {{ opacity: 1; box-shadow: 0 0 10px #00f2ff; }}
        to {{ opacity: 0.7; box-shadow: 0 0 30px #00f2ff; }}
    }}
    .logo-ring h2 {{ color: #00f2ff; margin: 0; font-family: sans-serif; letter-spacing: 2px; }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: #050505 !important;
        border-right: 1px solid #00f2ff;
    }}
    
    /* Sidebar Project Glow */
    [data-testid="stSidebarNav"] ul li div a span {{
        color: #00f2ff !important;
        font-weight: bold !important;
        text-shadow: 0 0 5px rgba(0, 242, 255, 0.5);
    }}
    [data-testid="stSidebarNav"] ul li a:hover span {{
        color: #ffd700 !important;
        text-shadow: 0 0 15px #ffd700 !important;
    }}

    /* Industry Portal Boxes */
    .portal-box {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 242, 255, 0.2);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        transition: 0.3s;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-bottom: 0px !important;
    }}
    .portal-box:hover {{
        border-color: #00f2ff;
        background: rgba(0, 242, 254, 0.08);
        transform: translateY(-5px);
    }}

    /* Custom Buttons */
    .stButton>button {{
        width: 100% !important;
        background-color: transparent !important;
        color: #00f2ff !important;
        border: 1px solid #00f2ff !important;
        border-radius: 0px 0px 12px 12px !important;
        font-weight: bold !important;
        height: 45px !important;
        margin-top: -1px !important;
        transition: 0.3s !important;
    }}
    .stButton>button:hover {{
        background-color: #00f2ff !important;
        color: #000 !important;
        box-shadow: 0 0 20px #00f2ff;
    }}

    /* Pricing Cards */
    .pricing-card {{
        background: rgba(255,255,255,0.03);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(0, 242, 255, 0.2);
        text-align: center;
    }}
    
    /* Footer Styling */
    .footer-text {{
        text-align: center;
        color: #444;
        padding: 50px;
        font-size: 14px;
        border-top: 1px solid #111;
    }}
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Header & Logo
with st.sidebar:
    st.markdown("""
        <div class="logo-container">
            <div class="logo-ring"><h2>SI</h2></div>
            <p style="color:#00f2ff; font-weight:bold; margin-top:10px;">CORE ENGINE V2.0</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<a href="{whatsapp_url}" style="text-decoration:none;"><div style="padding:10px; border:1px solid #00f2ff; color:#00f2ff; text-align:center; border-radius:5px; margin-bottom:10px;">💬 WHATSAPP SUPPORT</div></a>', unsafe_allow_html=True)
    st.markdown("---")

# 4. State & Industry Mapping
if 'selected_industry' not in st.session_state:
    st.session_state.selected_industry = None

industries = ["Agricultural", "Airline", "Bank", "Construction", "Diplomacy", "E-Commerce", "Education", "Energy Company", "Food Service", "Healthcare", "Hotel", "Insurance", "Manufacturing", "Military & Defense", "Pharmaceutical", "Real Estate", "Retail Chain", "Shipping Company", "Telecommunication", "Transmission", "Transportation"]

industry_map = {i: i[:4].upper() for i in industries}

# 5. Main Dashboard Logic
if not st.session_state.selected_industry:
    # Header Section
    st.markdown("<h1 style='text-align:center; color:#00f2ff; letter-spacing:5px;'>SYSTEM INTELLIGENCE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#ffd700; text-transform:uppercase;'>Deterministic Optimization for 21 Industrial Sectors</p>", unsafe_allow_html=True)

    # YouTube Video Banner
    video_id = "aDIUEaVF8v4"
    st.markdown(f'<div style="width: 100%; height: 350px; border-radius: 15px; border: 1px solid #00f2ff; overflow: hidden; margin: 30px 0;"><iframe style="width: 100%; height: 100%;" src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>', unsafe_allow_html=True)

    # Smart Tutoring Hub (Added as requested)
    with st.expander("📚 VIEW SMART TUTORING HUB & FEE STRUCTURE"):
        st.markdown("""
            <table style="width:100%; color:white; border-collapse: collapse; background:rgba(0,0,0,0.3);">
                <tr style="border-bottom: 1px solid #00f2ff; color:#00f2ff;">
                    <th style="padding:10px;">Level</th><th style="padding:10px;">Fee (PKR)</th>
                </tr>
                <tr><td style="padding:10px;">Class 1-8</td><td style="padding:10px;">4,000 - 6,000 / Subject</td></tr>
                <tr><td style="padding:10px;">Matric / O-Levels</td><td style="padding:10px;">6,000 - 10,000 / Subject</td></tr>
                <tr><td style="padding:10px;">FSc / A-Levels</td><td style="padding:10px;">10,000 - 15,000 / Subject</td></tr>
            </table>
            <p style="color:#ffd700; font-size:12px; margin-top:10px;">*Special cash prizes for top performers up to $150.</p>
        """, unsafe_allow_html=True)

    st.markdown("<h3 style='color:#00f2ff; margin-top:40px;'>Select Industrial Intelligence Core:</h3>", unsafe_allow_html=True)
    
    # Industry Grid
    for i in range(0, len(industries), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(industries):
                name = industries[i+j]
                with cols[j]:
                    st.markdown(f'<div class="portal-box"><div style="color:#ffd700; font-size:18px; font-weight:bold;">{name}</div><div style="color:#00f2ff; font-size:10px; margin-top:5px;">NEURAL CORE ACTIVE</div></div>', unsafe_allow_html=True)
                    if st.button(f"Sync {name}", key=f"btn_{i+j}"):
                        st.session_state.selected_industry = name
                        st.rerun()

else:
    # Industry Specific View
    prefix = industry_map.get(st.session_state.selected_industry)
    st.markdown(f"<h1 style='color:#00f2ff;'>{st.session_state.selected_industry} Portal</h1>", unsafe_allow_html=True)
    
    if st.button("⬅ Return to Global Dashboard"):
        st.session_state.selected_industry = None
        st.rerun()

    st.info(f"Accessing {st.session_state.selected_industry} deterministic models. Use the sidebar to navigate specific projects.")

# 6. Pricing Section
st.markdown("---")
st.markdown("<h2 style='text-align:center;'>Strategic License Deployment</h2>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    st.markdown(f"""
    <div class="pricing-card">
        <h3 style="color:#ccc;">BASIC ANALYTICS</h3>
        <h2 style="color:white;">$116</h2>
        <ul style="text-align:left; color:#888; font-size:14px;">
            <li>✔ Industry Standard Models</li>
            <li>✔ Core Resource Planning</li>
            <li>✔ Standard Email Support</li>
        </ul>
        <a href="{basic_doc_url}" style="text-decoration:none;"><div style="padding:10px; background:#00f2ff; color:black; border-radius:5px; font-weight:bold;">DEPLOY BASIC</div></a>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="pricing-card" style="border-color:#ffd700;">
        <h3 style="color:#ffd700;">PREMIUM ENTERPRISE</h3>
        <h2 style="color:white;">$399</h2>
        <ul style="text-align:left; color:#888; font-size:14px;">
            <li>✔ Full Optimization Suite</li>
            <li>✔ 24/7 Priority WhatsApp</li>
            <li>✔ Custom Multi-Sector Access</li>
        </ul>
        <a href="{premium_doc_url}" style="text-decoration:none;"><div style="padding:10px; background:#ffd700; color:black; border-radius:5px; font-weight:bold;">DEPLOY PREMIUM</div></a>
    </div>
    """, unsafe_allow_html=True)

# 7. Footer
st.markdown("""
    <div class="footer-text">
        SYSTEM INTELLIGENCE TURBO CORE © 2026 | Founded by Ahsan Khan (MS Mathematics)
    </div>
""", unsafe_allow_html=True)
