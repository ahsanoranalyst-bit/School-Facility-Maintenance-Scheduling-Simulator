import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(page_title="System Intelligence | EduSi Core", layout="wide", page_icon="💠")

# --- URLs & Pricing ---
whatsapp_url = "https://wa.me/923245277654"
basic_doc_url = "https://ahsankhan.lemonsqueezy.com/checkout/buy/ba3a76f7-4acc-4643-a838-9dc4085af6dc"
premium_doc_url = "https://ahsankhan.lemonsqueezy.com/checkout/buy/6245738f-4d29-4a0a-a574-e9a0e8838124"

# 2. Complete HTML/CSS UI Injection
st.markdown(f"""
    <style>
        /* Base Styling */
        .stApp {{
            background: radial-gradient(circle at top center, #0a111a 0%, #050505 100%);
            color: #ffffff;
        }}

        /* --- LOGO BLINKING EFFECT --- */
        .header-section {{ padding: 20px 0; text-align: center; }}
        .logo-ring {{
            width: 90px; height: 90px; margin: 0 auto;
            border: 2px solid #00f2ff; border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            background: rgba(0, 0, 0, 0.8);
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
            transition: all 0.4s ease;
            cursor: pointer;
            animation: blink-glow 1.5s infinite alternate;
        }}
        @keyframes blink-glow {{
            from {{ opacity: 1; box-shadow: 0 0 10px #00f2ff; }}
            to {{ opacity: 0.8; box-shadow: 0 0 35px #00f2ff; }}
        }}
        .logo-ring h2 {{ color: #00f2ff; margin: 0; font-size: 1.4rem; letter-spacing: 1px; }}

        /* --- BANNER ZOOM EFFECT --- */
        .banner-container {{ 
            width: 100%; border-radius: 15px; overflow: hidden; 
            border: 1px solid rgba(0, 242, 255, 0.2); margin-bottom: 30px;
        }}
        .banner-container img {{ 
            width: 100%; transition: transform 0.8s ease, filter 0.8s ease;
            filter: brightness(0.7);
        }}
        .banner-container:hover img {{ transform: scale(1.05); filter: brightness(1); }}

        /* --- PRICE TABLE --- */
        .price-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: rgba(255,255,255,0.03); border-radius: 10px; overflow: hidden; }}
        .price-table th {{ background: rgba(0, 242, 255, 0.1); color: #00f2ff; padding: 15px; text-align: left; }}
        .price-table td {{ padding: 15px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #ccc; }}

        /* --- GRID CARDS --- */
        .feature-card {{
            background: rgba(255, 255, 255, 0.03); padding: 25px; border-radius: 12px;
            border: 1px solid rgba(0, 242, 255, 0.2); text-align: left; transition: all 0.4s ease;
            height: 180px;
        }}
        .feature-card:hover {{ border-color: #00f2ff; transform: translateY(-8px); background: rgba(0, 242, 254, 0.08); }}
        .feature-card h3 {{ color: #ffd700; margin: 0 0 10px; font-size: 1.1rem; text-transform: uppercase; }}
        .feature-card p {{ color: #aaa; font-size: 0.85rem; margin: 0; }}

        /* Hide Streamlit elements to keep it clean */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Configuration
with st.sidebar:
    st.markdown("""
        <div class="logo-ring"><h2>SI</h2></div>
        <p style='text-align:center; color:#00f2ff; font-weight:bold; margin-top:10px;'>CORE ENGINE V3.0</p>
    """, unsafe_allow_html=True)
    st.markdown(f'<a href="{whatsapp_url}" style="text-decoration:none;"><div style="padding:10px; border:1px solid #00f2ff; color:#00f2ff; text-align:center; border-radius:5px;">💬 CONNECT SUPPORT</div></a>', unsafe_allow_html=True)
    st.markdown("---")

# 4. State Management
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# 5. Dashboard View
if st.session_state.page == "Dashboard":
    # Header & Logo
    st.markdown('<div class="header-section"><div class="logo-ring"><h2>EduSi</h2></div></div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; color:#00f2ff; letter-spacing:3px;'>SYSTEM INTELLIGENCE</h1>", unsafe_allow_html=True)
    
    # Banner (Wallpaper with Hover Effect)
    st.markdown(f"""
        <div class="banner-container">
            <img src="https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80" alt="Banner">
        </div>
    """, unsafe_allow_html=True)

    # Fee Structure Table
    st.markdown("<h3 style='color:#00f2ff; border-left: 4px solid #00f2ff; padding-left: 10px;'>ACADEMIC OPTIMIZATION FEES</h3>", unsafe_allow_html=True)
    st.markdown("""
        <table class="price-table">
            <tr><th>Level</th><th>Format</th><th>Fee (PKR)</th></tr>
            <tr><td>Class 1-8</td><td>Home / Online</td><td>4,000 - 6,000</td></tr>
            <tr><td>Matric / O-Levels</td><td>Academy / Home</td><td>6,000 - 10,000</td></tr>
            <tr><td>FSc / A-Levels</td><td>Live Interactive</td><td>10,000 - 15,000</td></tr>
        </table>
    """, unsafe_allow_html=True)

    # 22 Intelligence Modules Grid
    st.markdown("<h3 style='color:#00f2ff; margin-top:40px; border-left: 4px solid #00f2ff; padding-left: 10px;'>INTELLIGENCE MODULES</h3>", unsafe_allow_html=True)
    
    modules = [
        ("Grades 1-12", "Tracking primary & secondary excellence."),
        ("FSC & O-Level", "Targeted board exam optimization."),
        ("A-Level (Cambridge)", "Advanced resource integration."),
        ("University Guidance", "Strategic success analysis."),
        ("Digital Notes", "Structured subject knowledge base."),
        ("Resource Library", "Premium global academic content."),
        ("Free Book Access", "Deterministic equity allocation."),
        ("Curriculum Guides", "Adaptive board roadmaps."),
        ("Online Tuition", "Virtual learning environments."),
        ("Exam Prep", "Logic-based stress analysis."),
        ("Creative Thinking", "Heuristic problem-solving models."),
        ("Skill Development", "Future-ready masterclasses."),
        ("Critical Thinking", "Advanced cognitive logic training."),
        ("Training Enhance", "Continuous growth feedback loops."),
        ("Home Tuition", "Smart tutor matching algorithms."),
        ("Academy Classes", "Physical learning hub management."),
        ("Live Tuition", "Real-time data-driven teaching."),
        ("Peer Learning", "Collaborative study networks."),
        ("Scholarships", "Data-driven funding support."),
        ("Science & Tech", "Specialized STEM master modules."),
        ("STEM Language", "Technical communication & coding."),
        ("Project & Thesis", "University research support.")
    ]

    # Grid Display
    for i in range(0, len(modules), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(modules):
                title, desc = modules[i+j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="feature-card">
                            <h3>{title}</h3>
                            <p>{desc}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Sync {title}", key=f"mod_{i+j}", use_container_width=True):
                        st.session_state.page = title
                        st.rerun()

# 6. Pricing Deployment
st.markdown("---")
col_p1, col_p2 = st.columns(2)
with col_p1:
    st.markdown(f'<a href="{basic_doc_url}" style="text-decoration:none;"><div style="padding:20px; border:1px solid #ccc; text-align:center; border-radius:10px; color:white;">DEPLOY BASIC ANALYTICS ($116)</div></a>', unsafe_allow_html=True)
with col_p2:
    st.markdown(f'<a href="{premium_doc_url}" style="text-decoration:none;"><div style="padding:20px; border:1px solid #ffd700; text-align:center; border-radius:10px; color:#ffd700;">DEPLOY PREMIUM ENTERPRISE ($399)</div></a>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#444;'>BY SYSTEM INTELLIGENCE 2026 | AHSAN KHAN</p>", unsafe_allow_html=True)
