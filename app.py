import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(
    page_title="EduSi | High-Performance Dashboard",
    layout="wide",
    page_icon="💠"
)

# --- Configuration & Links ---
WHATSAPP_LINK = "https://wa.me/923245277654"
WEBSITE_LINK = "https://sysintel.vercel.app/"
LOGOUT_URL = "https://edusi.vercel.app/" # Put your Vercel link here
YOUTUBE_ID = "aDIUEaVF8v4" 

# 2. Advanced CSS for Exact Symmetry and HD Display
st.markdown(f"""
    <style>
        /* Global Background */
        .stApp {{
            background: #050505 !important;
            color: #ffffff !important;
        }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{ 
            background-color: #080808 !important; 
            border-right: 2px solid #00f2ff !important; 
        }}

        /* Symmetrical Logo Pulse */
        .logo-ring {{
            width: 100px; height: 100px; margin: 0 auto;
            border: 2px solid #00f2ff; border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            box-shadow: 0 0 20px #00f2ff;
            animation: pulse-glow 2s infinite alternate;
        }}
        @keyframes pulse-glow {{
            from {{ transform: scale(1); box-shadow: 0 0 10px #00f2ff; }}
            to {{ transform: scale(1.05); box-shadow: 0 0 30px #00f2ff; }}
        }}
        .logo-ring h2 {{ color: #00f2ff; margin: 0; font-weight: bold; font-family: sans-serif; }}

        /* Sidebar Navigation Buttons */
        .nav-link {{
            display: block; padding: 12px; margin: 10px 0;
            text-align: center; border-radius: 8px;
            border: 1.5px solid #00f2ff; color: #00f2ff !important;
            text-decoration: none; font-weight: bold;
        }}
        .nav-link:hover {{ background: #00f2ff; color: #000 !important; box-shadow: 0 0 15px #00f2ff; }}

        /* Logout Button Style */
        .logout-link {{
            display: block; padding: 12px; margin-top: 50px;
            text-align: center; border-radius: 8px;
            border: 1.5px solid #ff4b4b; color: #ff4b4b !important;
            text-decoration: none; font-weight: bold;
            background: rgba(255, 75, 75, 0.1);
        }}

        /* HD VIDEO CONTAINER - Enhanced Sharpness */
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

        /* FIXED SYMMETRICAL MODULE BOXES */
        div.stButton > button {{
            background: rgba(255, 255, 255, 0.02) !important;
            color: #ffd700 !important;
            border: 2px solid #00f2ff !important; 
            border-radius: 10px !important;
            /* CRITICAL: Fixed height and width for symmetry */
            height: 90px !important;
            width: 100% !important;
            font-size: 14px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: 0.3s ease-in-out !important;
            display: flex; align-items: center; justify-content: center;
        }}
        
        div.stButton > button:hover {{
            background: #00f2ff !important;
            color: #000 !important;
            box-shadow: 0 0 25px #00f2ff !important;
            transform: scale(1.02);
        }}

        /* Symmetrical PageLink Overrides */
        .stPageLink {{
            height: 90px !important;
            border: 2px solid #00f2ff !important;
            border-radius: 10px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Engine
with st.sidebar:
    st.markdown('<div class="logo-ring"><h2>EduSi</h2></div>', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#00f2ff;'>SYSTEM INTELLIGENCE</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown(f'<a href="{WEBSITE_LINK}" target="_blank" class="nav-link">🌐 OFFICIAL WEBSITE</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="{WHATSAPP_LINK}" target="_blank" class="nav-link">💬 CONNECT SUPPORT</a>', unsafe_allow_html=True)
    
    st.markdown(f'<a href="{LOGOUT_URL}" class="logout-link">🔒 LOGOUT SYSTEM</a>', unsafe_allow_html=True)

# 4. Main UI Header
st.markdown("<h1 style='text-align:center; color:#00f2ff; letter-spacing:3px;'>SMART EDUCATION HUB</h1>", unsafe_allow_html=True)

# 5. HD Video Section (Forced 1080p Pixels)
st.markdown(f"""
    <div class="video-engine">
        <iframe src="https://www.youtube.com/embed/{YOUTUBE_ID}?autoplay=1&mute=1&loop=1&playlist={YOUTUBE_ID}&controls=0&modestbranding=1&vq=hd1080" 
        frameborder="0" allow="autoplay; encrypted-media"></iframe>
    </div>
""", unsafe_allow_html=True)

# 6. Academic Modules (22 Symmetrical Units)
st.markdown("<h2 style='color:#ffd700; border-left: 5px solid #00f2ff; padding-left: 15px;'>ACADEMIC MODULES</h2>", unsafe_allow_html=True)

modules = [
    ("Schooling (1-10)", "schooling.py"), ("FSc & O-Level", "fsc.py"),
    ("Uni Guidance", "uni.py"), ("Academic Notes", "notes.py"),
    ("Free Resources", "books.py"), ("Online Tuition", "online.py"),
    ("Exam Preparation", "exams.py"), ("Creative Thinking", "research.py"),
    ("Skill Development", "skills.py"), ("Trait Enhance", "training.py"),
    ("Home Tuition", "home.py"), ("Academy Classes", "academy.py"),
    ("Live Interactive", "live.py"), ("Study Groups", "groups.py"),
    ("Scholarships", "scholarships.py"), ("Science & Tech", "science.py"),
    ("STEM Language", "stem.py"), ("Ethical Education", "ethics.py"),
    ("Career Analysis", "career.py"), ("Project & Thesis", "thesis.py"),
    ("Learning Plans", "plans.py"), ("Parent Analytics", "analytics.py")
]

# Grid Logic
for i in range(0, len(modules), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(modules):
            title, file_name = modules[i+j]
            with cols[j]:
                page_path = f"pages/{file_name}"
                if os.path.exists(page_path):
                    st.page_link(page_path, label=title, icon="💠")
                else:
                    if st.button(title, key=f"btn_{i+j}"):
                        st.info(f"System Link: pages/{file_name} needed.")

# 7. Footer
st.markdown("<br><hr><p style='text-align:center; color:#444;'>SYSTEM INTELLIGENCE © 2026 | DESIGNED BY AHSAN KHAN</p>", unsafe_allow_html=True)

