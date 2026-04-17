import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(page_title="EduSi | Smart Education Hub", layout="wide", page_icon="💠")

# --- URLs & Contact Info ---
whatsapp_url = "https://wa.me/923245277654"
website_url = "https://www.ahsanoranalyst.online/"
video_id = "aDIUEaVF8v4"

# 2. Professional CSS (Blinking, Layout, and Video Framing)
st.markdown(f"""
    <style>
        .stApp {{ background: #050505 !important; color: #ffffff !important; }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{ 
            background-color: #080808 !important; 
            border-right: 2px solid #00f2ff !important; 
        }}

        /* --- EduSi LOGO BLINKING --- */
        .logo-ring {{
            width: 100px; height: 100px; margin: 0 auto;
            border: 2px solid #00f2ff; border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            box-shadow: 0 0 20px #00f2ff;
            animation: blink-glow 1.5s infinite alternate;
        }}
        @keyframes blink-glow {{
            from {{ opacity: 1; box-shadow: 0 0 10px #00f2ff; }}
            to {{ opacity: 0.6; box-shadow: 0 0 35px #00f2ff; }}
        }}
        .logo-ring h2 {{ color: #00f2ff; margin: 0; font-family: sans-serif; font-weight: bold; }}

        /* Sidebar Custom Buttons */
        .sidebar-btn {{
            display: block; padding: 10px; margin: 10px 0;
            text-align: center; border-radius: 8px;
            border: 1px solid #00f2ff; color: #00f2ff !important;
            text-decoration: none; font-weight: bold;
            transition: 0.3s;
        }}
        .sidebar-btn:hover {{ background: #00f2ff; color: #000 !important; box-shadow: 0 0 15px #00f2ff; }}

        /* --- CLEAN VIDEO FRAME (No YouTube UI) --- */
        .video-container {{
            position: relative; width: 100%; height: 450px; 
            border-radius: 20px; border: 1px solid #00f2ff; 
            overflow: hidden; margin-bottom: 35px;
            box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
        }}
        .video-container iframe {{
            position: absolute; top: -60px; left: 0; width: 100%; height: calc(100% + 120px);
            pointer-events: none; /* اس سے یوٹیوب کے بٹنز پر کلک نہیں ہوگا */
        }}

        /* Blinking Action Buttons */
        div.stButton > button {{
            background: transparent !important; color: #00f2ff !important;
            border: 1px solid #00f2ff !important; width: 100%; font-weight: bold;
            animation: pulse-border 2s infinite;
        }}
        @keyframes pulse-border {{
            0% {{ border-color: #00f2ff; }}
            50% {{ border-color: #ffd700; box-shadow: 0 0 10px #ffd700; }}
            100% {{ border-color: #00f2ff; }}
        }}
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Setup
with st.sidebar:
    st.markdown('<div class="logo-ring"><h2>EduSi</h2></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#00f2ff; margin-bottom:20px;'>CORE ENGINE</h3>", unsafe_allow_html=True)
    
    # Navigation Buttons
    st.markdown(f'<a href="{website_url}" target="_blank" class="sidebar-btn">🌐 OFFICIAL WEBSITE</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="sidebar-btn">💬 WHATSAPP SUPPORT</a>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🏠 BACK TO DASHBOARD"):
        st.rerun()

# 4. Main UI Header
st.markdown("<h1 style='text-align:center; color:#00f2ff; letter-spacing:3px;'>SYSTEM INTELLIGENCE</h1>", unsafe_allow_html=True)

# 5. Optimized Video Section (یوٹیوب کی لک ختم کر دی گئی ہے)
st.markdown(f"""
    <div class="video-container">
        <iframe src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0&showinfo=0&rel=0&modestbranding=1" 
        frameborder="0" allow="autoplay; encrypted-media"></iframe>
    </div>
""", unsafe_allow_html=True)

# 6. Intelligence Modules (22 Modules from Poster)
st.markdown("<h2 style='color:#ffd700; border-left: 5px solid #00f2ff; padding-left: 15px;'>ACADEMIC MODULES</h2>", unsafe_allow_html=True)

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

# Grid Layout for 22 Modules
for i in range(0, len(modules), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(modules):
            title, file_name = modules[i+j]
            with cols[j]:
                # Card Background
                st.markdown(f"<div style='background:rgba(255,255,255,0.03); padding:12px; border-radius:5px; border-bottom:2px solid #00f2ff;'> <p style='margin:0; color:#ccc; font-size:14px; font-weight:bold;'>{title}</p></div>", unsafe_allow_html=True)
                
                # Page Link Logic
                page_path = f"pages/{file_name}"
                if os.path.exists(page_path):
                    st.page_link(page_path, label=f"Open {title} Core", icon="🔓")
                else:
                    st.button(f"Sync {title}", key=f"btn_{i+j}")

# 7. Footer
st.markdown("<br><hr><p style='text-align:center; color:#444;'>SYSTEM INTELLIGENCE 2026 | AHSAN KHAN (MS MATHEMATICS)</p>", unsafe_allow_html=True)
