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

# Custom Styling
st.markdown("""
<style>
    .main {
        background-color: #0b0f19;
    }
    .bubble-card {
        background: linear-gradient(145deg, #131b2e, #0b0f19);
        border: 2px solid #233554;
        border-radius: 24px;
        padding: 24px;
        margin: 16px 0;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .swipe-pill {
        display: inline-block;
        background-color: #1e293b;
        color: #38bdf8;
        padding: 8px 18px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 12px;
        border: 1px solid #334155;
    }
    div.stButton > button {
        border-radius: 12px;
        height: 3.2em;
        font-weight: 600;
        font-size: 1.05rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Management ---
if "current_step" not in st.session_state:
    st.session_state.current_step = 1

if "daily_data" not in st.session_state:
    st.session_state.daily_data = {
        "present_mood": 3,
        "life_outlook": 3,
        "heart_rate": 68,
        "sleep": 7.0,
        "strain": 3,
        "vitality": 72,
        "financial_score": 70,
        "savings": 3500,
        "weekly_burn": 450,
        "monthly_income": 2600
    }

# ==============================================================================
# SCREEN 1: DAILY PULSE, CLOUD SKY FACE & PREDICTIVE METRICS
# ==============================================================================
if st.session_state.current_step == 1:
    st.title("🛡️ LifeShield")
    st.caption("Daily Biometrics & Trajectory Pulse")

    # Translucent Sky & Moving Cloud Container with Reactive Face
    sky_face_html = """
    <div style="position: relative; overflow: hidden; border-radius: 24px; border: 1px solid rgba(56, 189, 248, 0.25); background: linear-gradient(180deg, #0284c7 0%, #0369a1 40%, #0f172a 100%); padding: 24px 16px; font-family: -apple-system, BlinkMacSystemFont, sans-serif; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.45);">
        
        <style>
            /* Drifting Cloud Animations */
            @keyframes driftSlow {
                0% { transform: translateX(-120px); opacity: 0.35; }
                50% { opacity: 0.65; }
                100% { transform: translateX(450px); opacity: 0.35; }
            }
            @keyframes driftFast {
                0% { transform: translateX(-80px); opacity: 0.25; }
                50% { opacity: 0.55; }
                100% { transform: translateX(420px); opacity: 0.25; }
            }
            @keyframes subtleBreathe {
                0% { transform: translateY(0px) scale(1); }
                50% { transform: translateY(-5px) scale(1.02); }
                100% { transform: translateY(0px) scale(1); }
            }
            .cloud-bg-1 {
                position: absolute;
                top: 15px;
                left: 0;
                animation: driftSlow 34s linear infinite;
                pointer-events: none;
            }
            .cloud-bg-2 {
                position: absolute;
                top: 75px;
                left: 0;
                animation: driftFast 22s linear infinite;
                pointer-events: none;
            }
            .interactive-face {
                animation: subtleBreathe 3.5s ease-in-out infinite;
                filter: drop-shadow(0px 10px 18px rgba(0,0,0,0.5));
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .slider-range {
                -webkit-appearance: none;
                width: 92%;
                height: 10px;
                border-radius: 6px;
                background: linear-gradient(to right, #ef4444, #f97316, #f59e0b, #84cc16, #10b981);
                outline: none;
                margin-top: 18px;
                margin-bottom: 6px;
            }
            .slider-range::-webkit-slider-thumb {
                -webkit-appearance: none;
                appearance: none;
                width: 26px;
                height: 26px;
                border-radius: 50%;
                background: #ffffff;
                cursor: pointer;
                box-shadow: 0 0 12px rgba(0,0,0,0.6);
                border: 2px solid #0369a1;
            }
        </style>

        <!-- Background Clouds -->
        <svg class="cloud-bg-1" width="160" height="60" viewBox="0 0 100 45" fill="#ffffff">
            <path d="M 20 3
