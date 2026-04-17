import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(page_title="EduSi | Smart Education Hub", layout="wide", page_icon="💠")

# --- URLs & IDs ---
whatsapp_url = "https://wa.me/923245277654"
website_url = "https://www.ahsanoranalyst.online/"
video_id = "aDIUEaVF8v4"

# 2. CSS Overhaul
st.markdown(f"""
    <style>
        .stApp {{ background: #050505 !important; color: #ffffff !important; }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{ 
            background-color: #080808 !important; 
            border-right: 2px solid #00f2ff !important; 
        }}

        /* EduSi Logo Blinking */
        .logo-ring {{
            width: 90px; height: 90px; margin: 0 auto;
            border: 2px solid #00f2ff; border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            box-shadow: 0 0 20px #00f2ff;
            animation: blink-glow 1.5s infinite alternate;
        }}
        @keyframes blink-glow {{ from {{ opacity: 1; }} to {{ opacity: 0.5; }} }}

        /* Video Container */
        .video-container {{
            width: 100%; height: 400px; border-radius: 15px; 
            border: 1px solid #00f2ff; overflow: hidden; margin-bottom: 30px;
        }}

        /* Industrial Card Design */
        .module-card {{
            background: rgba(255, 255, 255, 0.03); 
            padding: 20px; 
            border-radius: 10px 10px 0 0; 
            border: 1px solid rgba(0, 242, 255, 0.2);
            border-bottom: none;
            text-align: center;
            transition: 0.3s;
        }}
        
        /* Navigation Link Styling */
        .stPageLink {{
            background: rgba(0, 242, 255, 0.1) !important;
            border: 1px solid #00f2ff !important;
            border-radius: 0 0 10px 10px !important;
            text-align: center !important;
            transition: 0.4s !important;
        }}
        .stPageLink:hover {{
            background: #00f2ff !important;
            box-shadow: 0 0 20px #00f2ff;
        }}
        .stPageLink p {{ color: #00f2ff !important; font-weight: bold !important; }}
        .stPageLink:hover p {{ color: #000 !important; }}
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown('<div class="logo-ring"><h2>EduSi</h2></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#00f2ff;'>SYSTEM INTELLIGENCE</h3>", unsafe_allow_html=True)
    st.markdown(f'<a href="{website_url}" target="_blank" style="text-decoration:none; color:#00f2ff; display:block; text-align:center; border:1px solid #00f2ff; padding:8px; border-radius:5px; margin-top:10px;">🌐 OFFICIAL WEBSITE</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="text-decoration:none; color:#00f2ff; display:block; text-align:center; border:1px solid #00f2ff; padding:8px; border-radius:5px; margin-top:10px;">💬 WHATSAPP SUPPORT</a>', unsafe_allow_html=True)

# 4. Main Banner
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>SMART EDUCATION HUB</h1>", unsafe_allow_html=True)
st.markdown(f'<div class="video-container"><iframe width="100%" height="100%" src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0" frameborder="0" allow="autoplay; encrypted-media"></iframe></div>', unsafe_allow_html=True)

# 5. Fixed Modules Grid
modules = [
    ("Class 1-10 Schooling", "schooling.py"), ("FSC & O-Level", "fsc.py"),
    ("University Guidance", "uni.py"), ("Digital Notes", "notes.py"),
    ("Free Book Access", "books.py"), ("Online Tuition", "online.py"),
    ("Exam Preparation", "exams.py"), ("Research Skills", "research.py"),
    ("Skill Development", "skills.py"), ("Traiting Enhance", "training.py"),
    ("Home Tuition", "home.py"), ("Academy Classes", "academy.py"),
    ("Live Interactive", "live.py"), ("Study Groups", "groups.py"),
    ("Scholarships", "scholarships.py"), ("Science & Tech", "science.py"),
    ("STEM Language", "stem.py"), ("Ethical Education", "ethics.py"),
    ("Career Analysis", "career.py"), ("Project & Thesis", "thesis.py"),
    ("Learning Plans", "plans.py"), ("Progress Analytics", "analytics.py")
]

st.markdown("<h2 style='color:#ffd700;'>🛠 Intelligence Modules</h2>", unsafe_allow_html=True)

for i in range(0, len(modules), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(modules):
            title, file_name = modules[i+j]
            with cols[j]:
                # اوپر والا حصہ (ڈیزائن کارڈ)
                st.markdown(f"""
                    <div class="module-card">
                        <h4 style="margin:0; color:#ffd700;">{title}</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                # نیچے والا حصہ (اصلی نیویگیشن بٹن)
                page_path = f"pages/{file_name}"
                if os.path.exists(page_path):
                    st.page_link(page_path, label="ENTER SYSTEM CORE")
                else:
                    # اگر فائل نہیں ہے تو یہ بٹن غیر فعال (Disabled) نظر آئے گا
                    st.markdown(f"<div style='text-align:center; padding:10px; border:1px solid #333; color:#444; border-radius: 0 0 10px 10px;'>Locked / Not Found</div>", unsafe_allow_html=True)

st.markdown("<br><hr><p style='text-align:center; color:#444;'>SYSTEM INTELLIGENCE 2026 | AHSAN KHAN</p>", unsafe_allow_html=True)
