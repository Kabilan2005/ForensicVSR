import streamlit as st
from streamlit_option_menu import option_menu
# Ensure all UI modules are imported
from UI import home_page, investigation_page, techniques_page, export_page

# 1. Page Configuration
st.set_page_config(page_title="Forensic VSR System", layout="wide", initial_sidebar_state="collapsed")

# 2. Advanced CSS Injection
st.markdown("""
    <style>
        .nav-wrapper {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #0E1117;
            z-index: 1000;
            border-top: 1px solid #333;
            padding: 5px 0;
        }
        .main .block-container {
            padding-bottom: 100px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Session State Initialization
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# 4. Define the Navigation Function
def render_nav():
    # Define the order of pages clearly
    nav_options = ["Home", "Investigation", "Techniques", "Export"]
    nav_icons = ["house", "camera-reels", "cpu", "download"]
    
    try:
        default_idx = nav_options.index(st.session_state.page)
    except ValueError:
        default_idx = 0

    st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=nav_options,
        icons=nav_icons,
        menu_icon="cast",
        default_index=default_idx,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#FF4B4B", "font-size": "18px"}, 
            "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "--hover-color": "#262730"},
            "nav-link-selected": {"background-color": "#FF4B4B", "color": "white"},
        }
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return selected

# 5. EXECUTION FLOW
selected_page = render_nav()

# Only rerun if the page actually changed to avoid infinite loops
if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

# 6. Page Routing Logic
if st.session_state.page == "Home":
    home_page.show()
elif st.session_state.page == "Investigation":
    investigation_page.show()
elif st.session_state.page == "Techniques":
    techniques_page.show()
elif st.session_state.page == "Export":
    export_page.show()