import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(page_title="EduSi | Smart Education Hub", layout="wide", page_icon="💠")

# --- URLs & IDs ---
whatsapp_url = "https://wa.me/923245277654"
video_id = "aDIUEaVF8v4"

# 2. CSS for Design and Blinking Effect
st.markdown(f"""
    <style>
        .stApp {{ background: #050505 !important; color: #ffffff !important; }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{ 
            background-color: #080808 !important; 
            border-right: 2px solid #00f2ff !important; 
        }}

        /* --- LOGO BLINKING EFFECT (EduSi) --- */
        .logo-ring {{
            width: 100px; height: 100px; margin: 0 auto;
            border: 2px solid #00f2ff; border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            box-shadow: 0 0 20px #00f2ff;
            animation: blink-glow 1.5s infinite alternate;
        }}
        @keyframes blink-glow {{
            from {{ opacity: 1; box-shadow: 0 0 10px #00f2ff; }}
            to {{ opacity: 0.7; box-shadow: 0 0 35px #00f2ff; }}
        }}
        .logo-ring h2 {{ color: #00f2ff; margin: 0; font-family: sans-serif; font-size: 1.2rem; }}

        /* Blinking Buttons Style */
        div.stButton > button {{
            background: transparent !important; color: #00f2ff !important;
            border: 1px solid #00f2ff !important; width: 100%; font-weight: bold;
            animation: button-pulse 2s infinite ease-in-out;
            transition: 0.4s;
        }}
        @keyframes button-pulse {{
            0% {{ border-color: #00f2ff; box-shadow: 0 0 5px #00f2ff; }}
            50% {{ border-color: #ffd700; box-shadow: 0 0 15px #ffd700; }}
            100% {{ border-color: #00f2ff; box-shadow: 0 0 5px #00f2ff; }}
        }}
        div.stButton > button:hover {{ 
            background: #00f2ff !important; color: #000 !important; 
            box-shadow: 0 0 30px #00f2ff !important;
        }}

        /* Card Styling */
        .module-card {{
            background: rgba(255, 255, 255, 0.02); padding: 15px; 
            border-left: 3px solid #00f2ff; border-radius: 5px; margin-bottom: 5px;
        }}
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Setup
with st.sidebar:
    st.markdown('<div class="logo-ring"><h2>EduSi</h2></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#00f2ff;'>SYSTEM INTELLIGENCE</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # یہاں خود بخود آپ کے سائیڈ بار مینیو میں پیجز آئیں گے
    st.markdown("<p style='color:#ffd700; font-size:12px;'>ACTIVE MODULES</p>", unsafe_allow_html=True)
    
    # واٹس ایپ بٹن
    st.markdown(f'<a href="{whatsapp_url}" style="text-decoration:none;"><div style="padding:10px; border:1px solid #00f2ff; color:#00f2ff; text-align:center; border-radius:5px;">💬 CONNECT SUPPORT</div></a>', unsafe_allow_html=True)

# 4. Main Dashboard UI
st.markdown("<h1 style='text-align:center; color:#00f2ff; letter-spacing:4px;'>SMART EDUCATION HUB</h1>", unsafe_allow_html=True)

# Video Banner
st.markdown(f"""
    <div style="width: 100%; height: 400px; border-radius: 15px; border: 1px solid #00f2ff; overflow: hidden; margin-bottom: 30px;">
        <iframe width="100%" height="100%" src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
    </div>
""", unsafe_allow_html=True)

# 5. Modules Grid (Linked to Pages)
st.markdown("<h2 style='color:#00f2ff;'>🛠 Intelligence Modules</h2>", unsafe_allow_html=True)

# آپ کے پوسٹر کے مطابق تمام 22 ماڈیولز
modules = [
    ("Class 1-10 Schooling", "schooling.py"), ("FSC & O-Level", "fsc_olevel.py"),
    ("University Guidance", "uni_guidance.py"), ("Digital Academic Notes", "notes.py"),
    ("Free Book Access", "books.py"), ("Online Tuition Classes", "online_tuition.py"),
    ("Exam Preparation", "exam_prep.py"), ("Research & Creative", "research.py"),
    ("Skill Development", "skill_dev.py"), ("Build Traiting Enhaince", "training.py"),
    ("Home Tuition", "home_tuition.py"), ("Academy Classes", "academy.py"),
    ("Online Live Tuition", "live_tuition.py"), ("Study Groups", "study_groups.py"),
    ("Scholarship Guidance", "scholarship.py"), ("Science & Tech", "science_tech.py"),
    ("STEM & Language", "stem_language.py"), ("Ethical Education", "ethics.py"),
    ("Career Path Analysis", "career.py"), ("Project & Thesis", "thesis.py"),
    ("Personalized Learning", "learning_plans.py"), ("Progress Analytics", "analytics.py")
]

# Grid Logic
for i in range(0, len(modules), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(modules):
            title, file_name = modules[i+j]
            with cols[j]:
                st.markdown(f"<div class='module-card'><h4 style='margin:0; color:#ffd700; font-size:14px;'>{title}</h4></div>", unsafe_allow_html=True)
                
                # اہم بات: یہاں st.page_link استعمال کیا ہے تاکہ کلک کرنے پر وہ اس پیج پر چلا جائے
                # آپ کو اپنے 'pages' فولڈر میں یہ فائلیں (مثلا schooling.py) بنانی ہوں گی
                page_path = f"pages/{file_name}"
                if os.path.exists(page_path):
                    st.page_link(page_path, label=f"Access {title} Core", icon="🚀")
                else:
                    # اگر پیج ابھی نہیں بنا تو یہ بٹن دکھائے گا
                    if st.button(f"Sync {title}", key=f"btn_{i+j}"):
                        st.info(f"Please create '{file_name}' in your 'pages' folder to activate this link.")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#444;'>BY SYSTEM INTELLIGENCE 2026 | AHSAN KHAN</p>", unsafe_allow_html=True)
