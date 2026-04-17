import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(
    page_title="EduSi | Smart Education Hub",
    layout="wide",
    page_icon="💠"
)

# --- URLs & IDs ---
whatsapp_url = "https://wa.me/923245277654"
website_url = "https://www.ahsanoranalyst.online/"
video_id = "aDIUEaVF8v4"

# 2. Advanced CSS for Clickable Cards and UI
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

        /* EduSi Logo Blinking Effect */
        .logo-ring {{
            width: 100px; height: 100px; margin: 0 auto;
            border: 2px solid #00f2ff; border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            box-shadow: 0 0 20px #00f2ff;
            animation: blink-glow 1.5s infinite alternate;
        }}
        @keyframes blink-glow {{
            from {{ opacity: 1; box-shadow: 0 0 10px #00f2ff; }}
            to {{ opacity: 0.5; box-shadow: 0 0 35px #00f2ff; }}
        }}
        .logo-ring h2 {{ color: #00f2ff; margin: 0; font-family: 'Arial', sans-serif; font-weight: bold; }}

        /* Sidebar Buttons */
        .sidebar-link {{
            display: block; padding: 12px; margin: 10px 0;
            text-align: center; border-radius: 8px;
            border: 1px solid #00f2ff; color: #00f2ff !important;
            text-decoration: none; font-weight: bold;
            transition: 0.3s;
        }}
        .sidebar-link:hover {{ background: #00f2ff; color: #000 !important; box-shadow: 0 0 15px #00f2ff; }}

        /* Video Container - Hidden YouTube UI */
        .video-wrapper {{
            position: relative; width: 100%; height: 450px; 
            border-radius: 20px; border: 1px solid #00f2ff; 
            overflow: hidden; margin-bottom: 40px;
        }}
        .video-wrapper iframe {{
            position: absolute; top: -60px; left: 0; width: 100%; height: calc(100% + 120px);
            pointer-events: none;
        }}

        /* Clickable Card Design */
        div.stButton > button {{
            background: rgba(255, 255, 255, 0.03) !important;
            color: #ffd700 !important;
            border: 1px solid rgba(0, 242, 255, 0.3) !important;
            border-left: 4px solid #00f2ff !important;
            height: 100px !important;
            width: 100% !important;
            font-size: 16px !important;
            font-weight: bold !important;
            text-align: center !important;
            white-space: normal !important;
            transition: 0.4s !important;
            animation: card-pulse 3s infinite;
        }}
        
        @keyframes card-pulse {{
            0% {{ border-color: rgba(0, 242, 255, 0.3); }}
            50% {{ border-color: #ffd700; box-shadow: 0 0 10px rgba(255, 215, 0, 0.2); }}
            100% {{ border-color: rgba(0, 242, 255, 0.3); }}
        }}

        div.stButton > button:hover {{
            background: #00f2ff !important;
            color: #000 !important;
            box-shadow: 0 0 25px #00f2ff !important;
            transform: translateY(-5px);
        }}
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Setup
with st.sidebar:
    st.markdown('<div class="logo-ring"><h2>EduSi</h2></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#00f2ff;'>SYSTEM INTELLIGENCE</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # External Links
    st.markdown(f'<a href="{website_url}" target="_blank" class="sidebar-link">🌐 OFFICIAL WEBSITE</a>', unsafe_allow_html=True)
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="sidebar-link">💬 WHATSAPP SUPPORT</a>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.sidebar.button("🏠 RESET DASHBOARD"):
        st.rerun()

# 4. Main Header
st.markdown("<h1 style='text-align:center; color:#00f2ff; letter-spacing:3px;'>SMART EDUCATION HUB</h1>", unsafe_allow_html=True)

# 5. Professional Video Banner
st.markdown(f"""
    <div class="video-wrapper">
        <iframe src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0&showinfo=0&rel=0&modestbranding=1" 
        frameborder="0" allow="autoplay; encrypted-media"></iframe>
    </div>
""", unsafe_allow_html=True)

# 6. Intelligence Modules (22 Linked Modules)
st.markdown("<h2 style='color:#00f2ff; border-left: 5px solid #ffd700; padding-left: 15px;'>ACADEMIC MODULES</h2>", unsafe_allow_html=True)

modules = [
    ("CLASS 1-10 SCHOOLING", "schooling.py"), ("FSC & O-LEVEL PREP", "fsc.py"),
    ("UNIVERSITY GUIDANCE", "uni.py"), ("DIGITAL ACADEMIC NOTES", "notes.py"),
    ("FREE BOOK ACCESS", "books.py"), ("ONLINE TUITION CLASSES", "online.py"),
    ("EXAM PREPARATION", "exams.py"), ("RESEARCH & CREATIVE", "research.py"),
    ("SKILL DEVELOPMENT", "skills.py"), ("TRAITING ENHANCEMENT", "training.py"),
    ("HOME TUITION (MATCHING)", "home.py"), ("ACADEMY CLASSES", "academy.py"),
    ("ONLINE LIVE TUITION", "live.py"), ("STUDY GROUPS", "groups.py"),
    ("SCHOLARSHIP GUIDANCE", "scholarships.py"), ("SCIENCE & TECH FOCUS", "science.py"),
    ("STEM & LANGUAGES", "stem.py"), ("ETHICAL EDUCATION", "ethics.py"),
    ("CAREER PATH ANALYSIS", "career.py"), ("PROJECT & THESIS", "thesis.py"),
    ("LEARNING PLANS", "plans.py"), ("PROGRESS ANALYTICS", "analytics.py")
]

# Grid Logic for Clickable Cards
for i in range(0, len(modules), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(modules):
            title, file_name = modules[i+j]
            with cols[j]:
                # Check if file exists in 'pages/' folder
                page_path = f"pages/{file_name}"
                
                if os.path.exists(page_path):
                    # If page exists, show clickable link card
                    st.page_link(page_path, label=title, icon="💠")
                else:
                    # If page doesn't exist, show a button (for testing)
                    if st.button(title, key=f"btn_{i+j}"):
                        st.warning(f"Core '{file_name}' not found in 'pages/' folder.")

# 7. Footer
st.markdown("<br><hr><p style='text-align:center; color:#444;'>SYSTEM INTELLIGENCE 2026 | AHSAN KHAN (MS MATHEMATICS)</p>", unsafe_allow_html=True)
