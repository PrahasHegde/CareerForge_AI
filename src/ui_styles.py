import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    body {
        background: radial-gradient(circle at top, #0f172a, #020617);
        color: #e5e7eb;
    }

    #MainMenu, footer, header {visibility: hidden;}

    h1, h2, h3 {
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 22px;
        transition: all 0.3s ease;
        text-align: center;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(79, 70, 229, 0.5);
        box-shadow: 0 25px 50px rgba(79, 70, 229, 0.15);
    }
    </style>
    """, unsafe_allow_html=True)


def display_metric_card(col, title, value):
    """
    Renders a premium SaaS-style metric card
    """
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size:0.9rem; color:#9ca3af; margin-bottom:6px;">
                {title}
            </div>
            <div style="font-size:2rem; font-weight:700; color:#e5e7eb;">
                {value}
            </div>
        </div>
        """, unsafe_allow_html=True)
