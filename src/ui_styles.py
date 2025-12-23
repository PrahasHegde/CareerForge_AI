import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* IMPORT FONT */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        /* 1. GLOBAL RESET & BACKGROUND */
        .stApp {
            background: radial-gradient(circle at top right, #131720 0%, #0E1117 100%);
            font-family: 'Inter', sans-serif;
            color: #E0E0E0;
        }
        
        /* 2. SIDEBAR STYLING */
        section[data-testid="stSidebar"] {
            background-color: #0E1117;
            border-right: 1px solid #1E232B;
        }
        
        /* Sidebar Titles/Text */
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {
            color: #FFFFFF;
            font-weight: 600;
        }

        /* 3. INPUT FIELDS (Clean & Dark) */
        .stTextInput > div > div > input, 
        .stTextArea > div > div > textarea, 
        .stSelectbox > div > div > div {
            background-color: #1E232B;
            color: white;
            border: 1px solid #2E3642;
            border-radius: 8px;
            transition: border-color 0.3s ease;
        }
        .stTextInput > div > div > input:focus, 
        .stTextArea > div > div > textarea:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 0 1px #4CAF50;
        }

        /* 4. BUTTONS (Neon Gradient) */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #00C853 0%, #B2FF59 100%);
            color: #000000;
            border: none;
            padding: 14px 24px;
            font-weight: 700;
            letter-spacing: 0.5px;
            border-radius: 8px;
            text-transform: uppercase;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 200, 83, 0.3);
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 200, 83, 0.4);
            color: #000000;
        }
        /* Secondary Buttons (Outlined) */
        .stDownloadButton > button {
            background: transparent;
            border: 1px solid #4CAF50;
            color: #4CAF50;
        }

        /* 5. METRIC CARDS (Glassmorphism) */
        .metric-card {
            background: rgba(30, 35, 43, 0.6);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 24px 16px;
            text-align: center;
            transition: transform 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            border-color: rgba(76, 175, 80, 0.3);
        }
        .metric-value {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(45deg, #4CAF50, #81C784);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 4px;
        }
        .metric-label {
            font-size: 0.85rem;
            color: #B0B3B8;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 500;
        }

        /* 6. TABS */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px;
            color: #9E9E9E;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(76, 175, 80, 0.1);
            color: #4CAF50;
        }

        /* 7. HEADERS */
        h1 {
            background: linear-gradient(90deg, #FFFFFF 0%, #B0B3B8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            letter-spacing: -1px;
        }
        h2, h3 {
            color: #FFFFFF;
            font-weight: 600;
        }
        
        /* 8. TOAST NOTIFICATIONS */
        div[data-baseweb="toast"] {
            background-color: #1E232B;
            color: white;
            border: 1px solid #2E3642;
        }
        </style>
    """, unsafe_allow_html=True)

def display_metric_card(col, label, value, sub_label=""):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
            <div style="font-size: 0.75rem; color: #666; margin-top: 4px;">{sub_label}</div>
        </div>
        """, unsafe_allow_html=True)