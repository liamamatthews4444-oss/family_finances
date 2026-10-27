import streamlit as st
import pandas as pd
import datetime
import os
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(
    page_title="LifeShield: Family & Vitality",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Global Styling
st.markdown("""
<style>
    .main {
        background-color: #0b0f19;
    }
    div.stButton > button {
        border-radius: 12px;
        height: 3.2em;
        font-weight: 600;
        font-size: 1.05rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 3.2rem;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "lifeshield_history.csv"

# --- History Loader ---
def load_history():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
            return df.sort_values("Date")
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

# --- Session State ---
if "current_step" not in st.session_state:
    st.session_state.current_step = 1

if "daily_data" not in st.session_state:
    st.session_state.daily_data = {
        "mood": 3,
        "heart_rate": 68,
        "sleep": 7.0,
        "strain": 3,
        "cognitive_clarity": 3,
        "physical_ease": 3,
        "social_patience": 3,
        "financial_calm": 3,
        "vitality": 72,
        "financial_score": 70,
        "savings": 3500,
        "weekly_burn": 450,
        "monthly_income": 2600
    }

# ==============================================================================
# SCREEN 1: REAL-SKY MOOD FACE & ADAPTIVE CHECK-IN
# ==============================================================================
if st.session_state.current_step == 1:
    st.title("🛡️ LifeShield")
    st.caption("Daily Biometrics & Adaptive Health Pulse")

    real_sky_face_html = """
    <div style="position: relative; overflow: hidden; border-radius: 24px; padding: 32px 16px; font-family: -apple-system, BlinkMacSystemFont, sans-serif; box-shadow: 0 16px 35px rgba(0, 0, 0, 0.6); display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <style>
            @keyframes panClouds {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            .sky-background {
                position: absolute;
                top: 0; left: 0; width: 100%; height: 100%;
                background: linear-gradient(rgba(11, 15, 25, 0.25), rgba(11, 15, 25, 0.65)),
                            url('https://images.unsplash.com/photo-1534088568595-a066f410bcda?auto=format&fit=crop&w=1200&q=80');
                background-size: 200% 200%;
                animation: panClouds 75s ease-in-out infinite;
                z-index: 1;
            }
            @keyframes subtleFloat {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-6px); }
                100% { transform: translateY(0px); }
            }
            .face-wrapper {
                position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; width: 100%;
            }
            .interactive-face {
                animation: subtleFloat 4s ease-in-out infinite;
                filter: drop-shadow(0px 12px 20px rgba(0,0,0,0.6));
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .clean-slider {
                -webkit-appearance: none;
                width: 82%;
                height: 8px;
                border-radius: 4px;
                background: linear-gradient(to right, #ef4444, #f97316, #f59e0b, #84cc16, #10b981);
                outline: none;
                margin-top: 24px;
            }
            .clean-slider::-webkit-slider-thumb {
                -webkit-appearance: none;
                appearance: none;
                width: 26px; height: 26px; border-radius: 50%;
                background: #ffffff; cursor: pointer;
                box-shadow: 0 0 14px rgba(0,0,0,0.7);
                border: 2px solid #0f172a;
            }
        </style>
        <div class="sky-background"></div>
        <div class="face-wrapper">
            <div style="font-size: 1.3rem; font-weight: 700; color: #ffffff; text-shadow: 0 2px 10px rgba(0,0,0,0.8); margin-bottom: 18px;">How are you feeling right now?</div>
            <svg id="moodFace" class="interactive-face" width="130" height="130" viewBox="0 0 100 100">
                <circle id="faceBg" cx="50" cy="50" r="45" fill="#f59e0b" stroke="#d97706" stroke-width="3.5"/>
                <circle id="leftEye" cx="35" cy="40" r="4.5" fill="#0f172a"/>
                <circle id="rightEye" cx="65" cy="40" r="4.5" fill="#0f172a"/>
                <path id="leftBrow" d="M 28 32 Q 35 32 42 32" stroke="#0f172a" stroke-width="3" stroke-linecap="round" fill="none"/>
                <path id="rightBrow" d="M 58 32 Q 65 32 72 32" stroke="#0f172a" stroke-width="3" stroke-linecap="round" fill="none"/>
                <path id="mouth" d="M 34 68 Q 50 68 66 68" stroke="#0f172a" stroke-width="4" stroke-linecap="round" fill="none"/>
            </svg>
            <div id="moodTitle" style="margin-top: 14px; font-weight: 800; color: #f59e0b; font-size: 1.15rem; text-shadow
