import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(
    page_title="System Intelligence | Smart Education Hub",
    layout="wide",
    page_icon="💠"
)

# --- Constants & Asset Links ---
WHATSAPP_LINK = "https://wa.me/923245277654"
WEBSITE_LINK = "https://www.ahsanoranalyst.online/"
# High-Quality Video ID
YOUTUBE_ID = "aDIUEaVF8v4" 

# 2. Advanced CSS for Exact Symmetry and HD UI
st.markdown(f"""
    <style>
        /* Global Environment */
        .stApp {{
            background: #050505 !important;
            color: #ffffff !important;
        }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{ 
            background-color: #080808 !important; 
            border-right: 2px solid #00f2ff !important; 
        }}

        /* Symmetrical Logo Branding */
        .logo-ring {{
            width: 100px; height: 100px; margin: 0 auto;
            border: 2px solid #00f2ff; border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
            animation: pulse-glow 2s infinite alternate;
        }}
        @keyframes pulse-glow {{
            from {{ opacity: 1; transform: scale(1); }}
            to {{ opacity: 0.6; transform: scale(1.05); box-shadow: 0 0 40px #00f2ff; }}
        }}
        .logo-ring h2 {{ color: #00f2ff; margin: 0; font-family: 'Inter', sans-serif; font-weight: 800; }}

        /* Sidebar Navigation Links */
        .nav-btn {{
            display: block; padding: 12px; margin: 10px 0;
            text-align: center; border-radius: 8px;
            border: 1.5px solid #00f2ff; color: #00f2ff !important;
            text-decoration: none; font-weight: bold;
            transition: all 0.3s ease;
        }}
        .nav-btn:hover {{ background: #00f2ff; color: #000 !important; box-shadow: 0 0 20px #00f2ff; }}

        /* HD Video Container - Crop Fixed for Clarity */
        .video-engine {{
            position: relative; width: 100%; height: 500px; 
            border-radius: 15px; border: 2px solid #00f2ff; 
            overflow: hidden; margin-bottom: 40px;
            background: #000;
        }}
        .video-engine iframe {{
            position: absolute; top: -65px; left: 0; width: 100%; height: calc(100% + 130px);
            pointer-events: none;
        }}

        /* EXACT SYMMETRICAL BORDERS FOR MODULE BUTTONS */
        div.stButton > button {{
            background: rgba(255, 255, 255, 0.02) !important;
            color: #ffd700 !important;
            border: 2px solid #00f2ff !important; /* Fixed Exact Border */
            border-radius: 10px !important;
            height: 85px !important;
            width: 100% !important;
            font-size: 14px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            transition: 0.4s all cubic-bezier(0.4, 0, 0.2, 1) !important;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        div.stButton > button:hover {{
            background: #00f2ff !important;
            color: #000 !important;
            box-shadow: 0 0 30px rgba(0, 242, 254, 0.8) !important;
            transform: scale(1.02);
        }}

        /* Ensuring st.page_link also follows the same symmetry */
        .stPageLink {{
            border: 2px solid #00f2ff !important;
            border-radius: 10px !important;
            background: rgba(0, 242, 255, 0.05) !important;
        }}
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Setup
with st.sidebar:
    st.markdown('<div class="logo-ring"><h2>EduSi</h2></div>', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#00f2ff; margin-top:10px;'>SYSTEM INTELLIGENCE</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown(f'<a href="{WEBSITE_LINK}" target="_blank" class="nav-btn">🌐 OFFICIAL WEBSITE</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="{WHATSAPP_LINK}" target="_blank" class="nav-btn">💬 WHATSAPP SUPPORT</a>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.sidebar.button("🔄 REFRESH CORE"):
        st.rerun()

# 4. Main Dashboard Header
st.markdown("<h1 style='text-align:center; color:#00f2ff; letter-spacing:4px; font-weight:900;'>SMART EDUCATION HUB</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888; margin-top:-15px;'>Real-World Academic Problem Solver | Personalised Learning Systems</p>", unsafe_allow_html=True)

# 5. HD Video Section (Optimized Pixels & Hidden Controls)
# Adding vq=hd1080 to the URL to force high quality
st.markdown(f"""
    <div class="video-engine">
        <iframe src="https://www.youtube.com/embed/{YOUTUBE_ID}?autoplay=1&mute=1&loop=1&playlist={YOUTUBE_ID}&controls=0&showinfo=0&rel=0&modestbranding=1&vq=hd1080" 
        frameborder="0" allow="autoplay; encrypted-media"></iframe>
    </div>
""", unsafe_allow_html=True)

# 6. Academic Intelligence Modules (22 Symmetrical Units)
st.markdown("<h2 style='color:#ffd700; border-left: 6px solid #00f2ff; padding-left: 15px; margin-bottom:25px;'>INTELLIGENCE MODULES</h2>", unsafe_allow_html=True)

# Full module list from your official poster
modules = [
    ("Schooling (1-10)", "schooling.py"), ("FSc & O-Level", "fsc.py"),
    ("University Guidance", "uni.py"), ("Digital Notes", "notes.py"),
    ("Free Book Access", "books.py"), ("Online Tuition", "online.py"),
    ("Exam Preparation", "exams.py"), ("Creative Thinking", "research.py"),
    ("Skill Development", "skills.py"), ("Trait Enhance", "training.py"),
    ("Home Tuition", "home.py"), ("Academy Classes", "academy.py"),
    ("Live Interactive", "live.py"), ("Study Groups", "groups.py"),
    ("Scholarships", "scholarships.py"), ("Science & Tech", "science.py"),
    ("STEM Language", "stem.py"), ("Ethical Education", "ethics.py"),
    ("Career Analysis", "career.py"), ("Project & Thesis", "thesis.py"),
    ("Learning Plans", "plans.py"), ("Parent Analytics", "analytics.py")
]

# Unified Grid Generation
for i in range(0, len(modules), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(modules):
            title, file_name = modules[i+j]
            with cols[j]:
                page_path = f"pages/{file_name}"
                
                # Symmetrical Click-Logic
                if os.path.exists(page_path):
                    st.page_link(page_path, label=title, icon="💠")
                else:
                    # Placeholder button for local testing
                    if st.button(title, key=f"btn_{i+j}"):
                        st.info(f"Deployment Required: Create '{file_name}' in the 'pages' directory.")

# 7. Professional Footer
st.markdown("<br><hr><p style='text-align:center; color:#444; font-weight:bold;'>SYSTEM INTELLIGENCE © 2026 | DEVELOPED BY AHSAN KHAN</p>", unsafe_allow_html=True)
