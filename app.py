import streamlit as st

# 1. Page Config
st.set_page_config(page_title="System Intelligence | Core Engine", layout="wide", page_icon="💠")

# --- URLs ---
whatsapp_url = "https://wa.me/923245277654"
video_id = "aDIUEaVF8v4"

# 2. Extreme CSS Injection (Streamlit Overhaul)
st.markdown(f"""
    <style>
        /* Global Background */
        .stApp {{
            background: #050505 !important;
            color: #ffffff !important;
        }}

        /* --- SIDEBAR LOGO & STYLE --- */
        [data-testid="stSidebar"] {{
            background-color: #080808 !important;
            border-right: 2px solid #00f2ff !important;
            padding-top: 20px;
        }}
        
        .sidebar-logo-ring {{
            width: 80px; height: 80px; margin: 0 auto;
            border: 2px solid #00f2ff; border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            box-shadow: 0 0 20px #00f2ff;
            animation: pulse-glow 2s infinite alternate;
        }}
        @keyframes pulse-glow {{
            from {{ box-shadow: 0 0 10px #00f2ff; transform: scale(1); }}
            to {{ box-shadow: 0 0 30px #00f2ff; transform: scale(1.05); }}
        }}
        .sidebar-logo-ring h2 {{ color: #00f2ff; margin: 0; font-family: 'Orbitron', sans-serif; }}

        /* --- VIDEO BANNER --- */
        .video-wrapper {{
            width: 100%; height: 400px; border-radius: 15px; 
            border: 1px solid #00f2ff; overflow: hidden; margin-bottom: 40px;
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
        }}

        /* --- PRICE TABLE DESIGN --- */
        .glass-table {{
            width: 100%; border-collapse: collapse; background: rgba(255, 255, 255, 0.03);
            border-radius: 12px; overflow: hidden; border: 1px solid rgba(0, 242, 255, 0.2);
        }}
        .glass-table th {{ background: rgba(0, 242, 255, 0.1); color: #00f2ff; padding: 20px; text-align: left; }}
        .glass-table td {{ padding: 18px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #ddd; }}

        /* --- NEON BUTTONS & CARDS --- */
        div.stButton > button {{
            background: transparent !important;
            color: #00f2ff !important;
            border: 1px solid #00f2ff !important;
            width: 100%;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: 0.4s;
            animation: button-blink 2s infinite ease-in-out;
        }}
        @keyframes button-blink {{
            0% {{ border-color: #00f2ff; box-shadow: 0 0 5px #00f2ff; }}
            50% {{ border-color: #ffd700; box-shadow: 0 0 15px #ffd700; }}
            100% {{ border-color: #00f2ff; box-shadow: 0 0 5px #00f2ff; }}
        }}
        div.stButton > button:hover {{
            background: #00f2ff !important;
            color: #000 !important;
            box-shadow: 0 0 30px #00f2ff !important;
            transform: translateY(-3px);
        }}

        /* Industry Card Style */
        .card-box {{
            background: rgba(255, 255, 255, 0.02);
            padding: 20px; border-radius: 10px;
            border-left: 3px solid #00f2ff;
            margin-bottom: 10px;
        }}
        .card-box h3 {{ color: #ffd700; font-size: 1.1rem; margin: 0; }}
        .card-box p {{ color: #888; font-size: 0.8rem; margin: 5px 0 0 0; }}
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Logic
with st.sidebar:
    st.markdown('<div class="sidebar-logo-ring"><h2>SI</h2></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#00f2ff;'>SYSTEM INTELLIGENCE</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("app.py", label="🏠 Main Dashboard", icon="⚡")
    st.markdown(f'<a href="{whatsapp_url}" style="text-decoration:none;"><div style="padding:10px; border:1px solid #00f2ff; color:#00f2ff; text-align:center; border-radius:5px; margin-top:20px;">💬 WHATSAPP CONNECT</div></a>', unsafe_allow_html=True)

# 4. Main Dashboard UI
st.markdown("<h1 style='text-align:center; color:#00f2ff; letter-spacing:5px;'>EDU-SI ENGINE</h1>", unsafe_allow_html=True)

# YouTube Wallpaper Video
st.markdown(f"""
    <div class="video-wrapper">
        <iframe width="100%" height="100%" src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0" 
        frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    </div>
""", unsafe_allow_html=True)

# 5. Price Structure Section
st.markdown("<h2 style='color:#ffd700;'>📊 Academic Optimization Core</h2>", unsafe_allow_html=True)
st.markdown("""
    <table class="glass-table">
        <tr><th>Category</th><th>Session Type</th><th>Fee Structure (PKR)</th></tr>
        <tr><td>Primary (1-8)</td><td>Individual / Group</td><td>4,000 - 6,000</td></tr>
        <tr><td>Matric / O-Levels</td><td>Advanced Prep</td><td>6,000 - 10,000</td></tr>
        <tr><td>FSc / A-Levels</td><td>Professional Logic</td><td>10,000 - 15,000</td></tr>
    </table>
    <p style='color:#00f2ff; font-size:13px; margin-top:10px;'>* Reward: Cash prizes for top 6 performers authorized by System Intelligence.</p>
""", unsafe_allow_html=True)

# 6. 22 Industry Modules Grid
st.markdown("<h2 style='color:#00f2ff; margin-top:50px;'>🛠 Intelligence Modules</h2>", unsafe_allow_html=True)

modules = [
    ("Grades 1-12", "Tracking excellence."), ("FSC & O-Level", "Exam optimization."),
    ("A-Level Prep", "Resource integration."), ("Uni Guidance", "Strategic analysis."),
    ("Digital Notes", "Knowledge base."), ("Resource Lib", "Global content."),
    ("Free Books", "Equity allocation."), ("Curriculum", "Adaptive roadmaps."),
    ("Online Tuition", "Virtual environments."), ("Exam Prep", "Stress analysis."),
    ("Creative Lab", "Heuristic models."), ("Skill Dev", "Masterclasses."),
    ("Critical Thinking", "Logic training."), ("Training+", "Growth feedback."),
    ("Home Tuition", "Smart matching."), ("Academy Core", "Hub management."),
    ("Live Classes", "Data-driven teaching."), ("Peer Learn", "Study networks."),
    ("Scholarships", "Funding support."), ("STEM Master", "Specialized tech."),
    ("STEM Language", "Coding logic."), ("Thesis Support", "Research engine.")
]

# Generate Grid
for i in range(0, len(modules), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(modules):
            title, desc = modules[i+j]
            with cols[j]:
                st.markdown(f"""
                    <div class="card-box">
                        <h3>{title}</h3>
                        <p>{desc}</p>
                    </div>
                """, unsafe_allow_html=True)
                # Blinking Button
                if st.button(f"Deploy {title}", key=f"mod_{i+j}"):
                    st.write(f"System Intelligence: {title} Module Activated.")

# 7. Pricing License Section
st.markdown("---")
p1, p2 = st.columns(2)
with p1:
    st.markdown('<div style="padding:30px; border:2px solid #ccc; border-radius:15px; text-align:center;">'
                '<h3 style="color:#ccc;">BASIC ANALYTICS</h3><h1>$116</h1>'
                '<p>Core Models Included</p></div>', unsafe_allow_html=True)
    st.button("DEPLOY BASIC LICENSE", key="buy_basic")

with p2:
    st.markdown('<div style="padding:30px; border:2px solid #ffd700; border-radius:15px; text-align:center;">'
                '<h3 style="color:#ffd700;">PREMIUM ENTERPRISE</h3><h1>$399</h1>'
                '<p>Full Unlimited Access</p></div>', unsafe_allow_html=True)
    st.button("DEPLOY PREMIUM LICENSE", key="buy_prem")

st.markdown("<br><p style='text-align:center; color:#333;'>SYSTEM INTELLIGENCE © 2026 | AHSAN KHAN</p>", unsafe_allow_html=True)
