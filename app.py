import streamlit as st

# 1. Page Config
st.set_page_config(page_title="System Intelligence | Smart Education Hub", layout="wide", page_icon="💠")

# --- URLs ---
whatsapp_url = "https://wa.me/923245277654"
video_id = "aDIUEaVF8v4"

# 2. Advanced CSS for Blinking and Industrial Look
st.markdown(f"""
    <style>
        .stApp {{ background: #050505 !important; color: #ffffff !important; }}
        
        /* Sidebar Logo */
        [data-testid="stSidebar"] {{ background-color: #080808 !important; border-right: 2px solid #00f2ff !important; }}
        .sidebar-logo-ring {{
            width: 80px; height: 80px; margin: 0 auto;
            border: 2px solid #00f2ff; border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            box-shadow: 0 0 20px #00f2ff;
            animation: pulse-glow 2s infinite alternate;
        }}
        @keyframes pulse-glow {{ from {{ transform: scale(1); }} to {{ transform: scale(1.05); }} }}
        
        /* Video Banner */
        .video-wrapper {{
            width: 100%; height: 450px; border-radius: 15px; 
            border: 1px solid #00f2ff; overflow: hidden; margin-bottom: 40px;
        }}

        /* Blinking Buttons */
        div.stButton > button {{
            background: transparent !important; color: #00f2ff !important;
            border: 1px solid #00f2ff !important; width: 100%; font-weight: bold;
            animation: button-blink 2s infinite ease-in-out;
        }}
        @keyframes button-blink {{
            0% {{ border-color: #00f2ff; box-shadow: 0 0 5px #00f2ff; }}
            50% {{ border-color: #ffd700; box-shadow: 0 0 15px #ffd700; }}
            100% {{ border-color: #00f2ff; box-shadow: 0 0 5px #00f2ff; }}
        }}
        div.stButton > button:hover {{ background: #00f2ff !important; color: #000 !important; }}

        /* Table Style */
        .glass-table {{
            width: 100%; border-collapse: collapse; background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(0, 242, 255, 0.2);
        }}
        .glass-table th {{ background: rgba(0, 242, 255, 0.1); color: #00f2ff; padding: 15px; }}
        .glass-table td {{ padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); }}
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar (Fixing the KeyError)
with st.sidebar:
    st.markdown('<div class="sidebar-logo-ring"><h2 style="color:#00f2ff; margin:0;">SI</h2></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#00f2ff;'>SMART EDUCATION HUB</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # KeyError Fix: Removed st.page_link for app.py to avoid path issues
    if st.button("🏠 Home Dashboard"):
        st.rerun()
        
    st.markdown(f'<a href="{whatsapp_url}" style="text-decoration:none;"><div style="padding:10px; border:1px solid #00f2ff; color:#00f2ff; text-align:center; border-radius:5px; margin-top:10px;">💬 CONNECT SUPPORT</div></a>', unsafe_allow_html=True)

# 4. Header & Video
st.markdown("<h1 style='text-align:center; color:#00f2ff; letter-spacing:4px;'>SYSTEM INTELLIGENCE</h1>", unsafe_allow_html=True)
st.markdown(f'<div class="video-wrapper"><iframe width="100%" height="100%" src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>', unsafe_allow_html=True)

# 5. Price Table (Based on your poster info)
st.markdown("<h2 style='color:#ffd700;'>📊 Academic Optimizer Fee Structure</h2>", unsafe_allow_html=True)
st.markdown("""
    <table class="glass-table">
        <tr><th>Class / Level</th><th>Format</th><th>Monthly Fee (PKR)</th></tr>
        <tr><td>Class 1-10 & Foundations</td><td>Online / Home</td><td>4,000 - 8,000</td></tr>
        <tr><td>FSC & O-Level (Cambridge)</td><td>Academy / Live</td><td>8,000 - 12,000</td></tr>
        <tr><td>University & Thesis Support</td><td>Interactive Core</td><td>15,000 - 25,000</td></tr>
    </table>
""", unsafe_allow_html=True)

# 6. 22 Modules (Exact from your uploaded poster)
st.markdown("<h2 style='color:#00f2ff; margin-top:40px;'>🛠 Intelligence Modules</h2>", unsafe_allow_html=True)

modules = [
    ("Schooling (1-10)", "Foundations optimization."), ("FSC & O-Level", "Cambridge prep."),
    ("Uni Guidance", "Advanced subjects."), ("Digital Library", "Academic notes."),
    ("Free Book Access", "Curriculum guides."), ("Online Tuition", "Personalized classes."),
    ("Exam Prep", "All levels support."), ("Creative Thinking", "Research skills."),
    ("Skill Dev", "Critical thinking."), ("Training Enhance", "Growth tracking."),
    ("Home Tuition", "Parent-Tutor matching."), ("Academy Classes", "Academy/Home."),
    ("Online Live", "Interactive tuition."), ("Study Groups", "Peer learning."),
    ("Scholarships", "Application guidance."), ("Science & Tech", "Subject focus."),
    ("STEM Language", "Communication skills."), ("Ethical Education", "Values-based."),
    ("Career Analysis", "Path for students."), ("Project & Thesis", "University support."),
    ("Learning Plans", "Personalized data."), ("Progress Analytics", "For parents.")
]

for i in range(0, len(modules), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(modules):
            title, desc = modules[i+j]
            with cols[j]:
                st.markdown(f"<div style='background:rgba(255,255,255,0.02); padding:15px; border-left:3px solid #00f2ff; border-radius:5px;'> <h4 style='margin:0; color:#ffd700;'>{title}</h4><p style='margin:0; font-size:12px; color:#888;'>{desc}</p></div>", unsafe_allow_html=True)
                st.button(f"Sync {title}", key=f"mod_{i+j}")

st.markdown("<br><p style='text-align:center; color:#333;'>SYSTEM INTELLIGENCE © 2026 | Ahsan Khan (MS Mathematics)</p>", unsafe_allow_html=True)
