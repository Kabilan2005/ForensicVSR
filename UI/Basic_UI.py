import streamlit as st
from streamlit_option_menu import option_menu 

st.set_page_config(page_title="Forensic VSR System", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Top Title Styling */
        .top-title {
            text-align: center;
            padding: 10px;
            font-size: 36px;
            font-weight: bold;
            color: #FF4B4B;
            border-bottom: 2px solid #ddd;
            margin-bottom: 20px;
        }

        /* Bottom Nav Bar Container */
        .nav-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #0E1117;
            z-index: 999;
            padding: 10px 0;
            border-top: 1px solid #333;
        }
    </style>
    <div class="top-title">CCTV FORENSIC UPSCALING SYSTEM</div>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "Home"

def show_home():
    st.subheader("Investigation Case Books")
    st.write("Each 'Book' represents a specific case file containing multiple videos and logs.")
    
    cols = st.columns(3)
    with cols[0]:
        st.info("📖 **Case #2026-DEL-01**\n\nLocation: New Delhi\nStatus: Active")
        if st.button("Open Case 01"):
            st.session_state.page = "Investigation"
            st.rerun()
            
    with cols[1]:
        st.info("📖 **Case #2026-MUM-05**\n\nLocation: Mumbai\nStatus: Pending")
        st.button("Open Case 05", disabled=True)
        
    with cols[2]:
        st.success("➕ **New Case**\n\nCreate a new investigation book.")
        st.button("Create New")

def show_investigation():
    st.subheader("📹 Video Analysis Desk")
    st.info("This is where we will upload, zoom, and clip videos in the next module.")
    if st.button("⬅️ Back to Books"):
        st.session_state.page = "Home"
        st.rerun()

if st.session_state.page == "Home":
    show_home()
elif st.session_state.page == "Investigation":
    show_investigation()

with st.container():
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["Home", "Investigation", "Techniques", "Settings"],
        icons=["house", "camera-video", "cpu", "gear"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "orange", "font-size": "20px"}, 
            "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#FF4B4B"},
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)

if selected != st.session_state.page:
    st.session_state.page = selected
    st.rerun()