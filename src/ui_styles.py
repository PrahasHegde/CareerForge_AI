import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>

    /* =======================
       DESIGN TOKENS
    ======================== */
    :root {
        --bg-main: #0b1020;
        --bg-card: rgba(20, 28, 58, 0.55);
        --border-subtle: rgba(148, 163, 184, 0.12);
        --accent: #6366f1;
        --accent-soft: rgba(99, 102, 241, 0.15);
        --text-main: #e5e7eb;
        --text-muted: #94a3b8;
    }

    /* =======================
       GLOBAL RESET
    ======================== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body, [class*="css"] {
        font-family: Inter, -apple-system, BlinkMacSystemFont,
                     "Segoe UI", Roboto, sans-serif;
    }

    body {
        background: radial-gradient(1200px 600px at 10% -10%, #1e293b 0%, transparent 40%),
                    var(--bg-main);
        color: var(--text-main);
        overflow-x: hidden;
    }

    /* =======================
       HERO BANNER
    ======================== */
    .hero-banner {
        padding: 72px 48px;
        border-radius: 24px;
        background:
            linear-gradient(
                180deg,
                rgba(99,102,241,0.12),
                rgba(99,102,241,0.02)
            ),
            var(--bg-card);
        border: 1px solid var(--border-subtle);
        backdrop-filter: blur(18px);
        text-align: center;
        margin: 48px 0 56px;
    }

    .hero-banner-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #e0e7ff, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 16px;
    }

    .hero-banner-subtitle {
        max-width: 760px;
        margin: 0 auto;
        font-size: 1.1rem;
        line-height: 1.7;
        color: var(--text-muted);
    }

    /* =======================
       INPUT CARD
    ======================== */
    .input-card {
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        border: 1px solid var(--border-subtle);
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 28px;
    }

    /* =======================
       METRIC CARDS
    ======================== */
    .metric-card {
        background: linear-gradient(
            180deg,
            rgba(255,255,255,0.04),
            rgba(255,255,255,0.01)
        );
        border: 1px solid var(--border-subtle);
        border-radius: 18px;
        padding: 22px;
        height: 100%;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 40px rgba(0,0,0,0.35);
    }

    .metric-icon {
        font-size: 1.6rem;
        opacity: 0.9;
        margin-bottom: 10px;
    }

    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 2.1rem;
        font-weight: 700;
        color: #e0e7ff;
    }

    /* =======================
       BUTTONS
    ======================== */
    .stButton > button {
        background: linear-gradient(
            135deg,
            #6366f1,
            #4f46e5
        );
        color: #fff;
        font-weight: 600;
        font-size: 0.95rem;
        border-radius: 12px;
        padding: 14px 26px;
        border: none;
        transition: all 0.25s ease;
        box-shadow: 0 12px 28px rgba(79,70,229,0.35);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 18px 44px rgba(79,70,229,0.45);
    }

    /* =======================
       TABS (CLEANER)
    ======================== */
    button[data-baseweb="tab"] {
        font-weight: 600;
        color: var(--text-muted);
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #e0e7ff;
        border-bottom: 2px solid var(--accent);
    }

    </style>
    """, unsafe_allow_html=True)


def display_metric_card(col, title, value, icon="📊"):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)


def display_hero_banner(title, subtitle):
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-banner-title">{title}</div>
        <div class="hero-banner-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)
