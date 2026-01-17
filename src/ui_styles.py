import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
            /* --- GLOBAL FONTS & BACKGROUND --- */
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;400&display=swap');
            
            .stApp {
                background-color: #050505;
                background-image: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #000000 100%);
                font-family: 'Roboto Mono', monospace;
            }
            
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Orbitron', sans-serif !important;
                color: #fff;
                text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
            }

            /* --- SIDEBAR CYBERPUNK STYLE --- */
            section[data-testid="stSidebar"] {
                background-color: #0a0a0a;
                border-right: 1px solid #333;
                box-shadow: 5px 0 15px rgba(0, 0, 0, 0.5);
            }
            
            /* --- CUSTOM BUTTONS --- */
            div.stButton > button {
                background: transparent !important;
                border: 1px solid #00f3ff !important;
                color: #00f3ff !important;
                border-radius: 0px !important; /* Sharp edges */
                font-family: 'Orbitron', sans-serif !important;
                transition: all 0.3s ease;
                box-shadow: 0 0 5px rgba(0, 243, 255, 0.2);
            }
            
            div.stButton > button:hover {
                background: #00f3ff !important;
                color: #000 !important;
                box-shadow: 0 0 20px #00f3ff;
                transform: scale(1.02);
            }

            /* Primary Action Button (The Analyze Button) */
            button[kind="primary"] {
                background: linear-gradient(45deg, #ff00ff, #00f3ff) !important;
                border: none !important;
                color: #000 !important;
                font-weight: bold !important;
            }

            /* --- INPUT FIELDS & TEXT AREAS --- */
            .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
                background-color: #111 !important;
                color: #00f3ff !important;
                border: 1px solid #333 !important;
                border-radius: 0px !important;
            }
            
            .stTextInput input:focus, .stTextArea textarea:focus {
                border-color: #ff00ff !important;
                box-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
            }

            /* --- METRIC CARDS --- */
            div[data-testid="stMetricValue"] {
                color: #00f3ff !important;
                font-family: 'Orbitron', sans-serif;
                text-shadow: 0 0 10px #00f3ff;
            }
            div[data-testid="stMetricLabel"] {
                color: #b0b0b0 !important;
            }
            
            /* Custom Card Container */
            .metric-card {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 3px solid #ff00ff;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
                backdrop-filter: blur(5px);
                border-radius: 5px;
            }

            /* --- TABS --- */
            .stTabs [data-baseweb="tab-list"] {
                gap: 10px;
            }
            .stTabs [data-baseweb="tab"] {
                background-color: transparent;
                border: 1px solid #333;
                color: #fff;
                border-radius: 0px;
            }
            .stTabs [aria-selected="true"] {
                border-bottom: 2px solid #ff00ff !important;
                color: #ff00ff !important;
            }

            /* --- SPINNER --- */
            .stSpinner > div {
                border-top-color: #00f3ff !important;
            }
            
            /* --- STATUS CONTAINER --- */
            div[data-testid="stStatusWidget"] {
                background-color: #111;
                border: 1px solid #00f3ff;
            }
        </style>
    """, unsafe_allow_html=True)

def display_metric_card(col, title, value):
    """Helper to display metrics with the new card style"""
    col.markdown(f"""
    <div class="metric-card" style="padding: 15px; text-align: center;">
        <p style="margin: 0; font-size: 0.9rem; color: #aaa; text-transform: uppercase; letter-spacing: 1px;">{title}</p>
        <p style="margin: 0; font-size: 1.8rem; font-weight: bold; color: #00f3ff; font-family: 'Orbitron', sans-serif; text-shadow: 0 0 10px rgba(0, 243, 255, 0.6);">{value}</p>
    </div>
    """, unsafe_allow_html=True)