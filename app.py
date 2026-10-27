import streamlit as st
import pandas as pd
import datetime
import os
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection

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
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 12px;
        border: 1px solid #334155;
        letter-spacing: 0.04em;
    }
    div.stButton > button {
        border-radius: 12px;
        height: 3.2em;
        font-weight: 600;
        font-size: 1.05rem;
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "lifeshield_history.csv"

# --- Safe Multi-Source Data Loader ---
def load_history():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl="0m")
        if df is not None and not df.empty and "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
            return df.sort_values("Date")
    except Exception:
        pass

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
            <div id="moodTitle" style="margin-top: 14px; font-weight: 800; color: #f59e0b; font-size: 1.15rem; text-shadow: 0 2px 8px rgba(0,0,0,0.8);">Managing baseline</div>
            <input type="range" min="1" max="5" value="3" class="clean-slider" id="moodRange" oninput="handleSlide(this.value)">
        </div>
    </div>
    <script>
    function handleSlide(val) {
        const face = document.getElementById("faceBg");
        const mouth = document.getElementById("mouth");
        const leftBrow = document.getElementById("leftBrow");
        const rightBrow = document.getElementById("rightBrow");
        const title = document.getElementById("moodTitle");
        
        if (val == 1) {
            face.setAttribute("fill", "#ef4444"); face.setAttribute("stroke", "#b91c1c");
            mouth.setAttribute("d", "M 32 74 Q 50 54 68 74");
            leftBrow.setAttribute("d", "M 28 36 Q 35 30 42 35"); rightBrow.setAttribute("d", "M 58 35 Q 65 30 72 36");
            title.innerText = "Burnout"; title.style.color = "#ef4444";
        } else if (val == 2) {
            face.setAttribute("fill", "#f97316"); face.setAttribute("stroke", "#c2410c");
            mouth.setAttribute("d", "M 34 71 Q 50 62 66 71");
            leftBrow.setAttribute("d", "M 28 34 Q 35 31 42 34"); rightBrow.setAttribute("d", "M 58 34 Q 65 31 72 34");
            title.innerText = "Strained"; title.style.color = "#f97316";
        } else if (val == 3) {
            face.setAttribute("fill", "#f59e0b"); face.setAttribute("stroke", "#b45309");
            mouth.setAttribute("d", "M 34 68 Q 50 68 66 68");
            leftBrow.setAttribute("d", "M 28 32 Q 35 32 42 32"); rightBrow.setAttribute("d", "M 58 32 Q 65 32 72 32");
            title.innerText = "Managing baseline"; title.style.color = "#f59e0b";
        } else if (val == 4) {
            face.setAttribute("fill", "#84cc16"); face.setAttribute("stroke", "#4d7c0f");
            mouth.setAttribute("d", "M 32 64 Q 50 73 68 64");
            leftBrow.setAttribute("d", "M 28 30 Q 35 29 42 32"); rightBrow.setAttribute("d", "M 58 32 Q 65 29 72 30");
            title.innerText = "Resilient"; title.style.color = "#84cc16";
        } else {
            face.setAttribute("fill", "#10b981"); face.setAttribute("stroke", "#047857");
            mouth.setAttribute("d", "M 30 62 Q 50 80 70 62");
            leftBrow.setAttribute("d", "M 28 28 Q 35 26 42 30"); rightBrow.setAttribute("d", "M 58 30 Q 65 26 72 28");
            title.innerText = "Energised"; title.style.color = "#10b981";
        }
    }
    </script>
    """
    components.html(real_sky_face_html, height=310)

    # Biometrics Row
    col_hr, col_sleep = st.columns(2)
    with col_hr:
        hr_input = st.number_input(
            "Heart Rate (BPM)",
            min_value=40,
            max_value=175,
            value=st.session_state.daily_data["heart_rate"],
            step=1
        )
    with col_sleep:
        sleep_input = st.slider("Hours Slept", 3.0, 11.0, float(st.session_state.daily_data["sleep"]), 0.5)

    strain_input = st.slider("Work / Shift Strain (1-5)", 1, 5, int(st.session_state.daily_data["strain"]))

    st.divider()

    st.subheader("🧠 Behavioral & Focus Signals")
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        cognitive_clarity = st.select_slider(
            "Focus / Clarity",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.daily_data["cognitive_clarity"],
            format_func=lambda x: {1: "1 - Brain Fog", 2: "2 - Sluggish", 3: "3 - Standard", 4: "4 - Clear", 5: "5 - Peak Flow"}[x]
        )
        physical_ease = st.select_slider(
            "Physical Comfort",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.daily_data["physical_ease"],
            format_func=lambda x: {1: "1 - Heavy Aches", 2: "2 - Stiff / Sore", 3: "3 - Normal", 4: "4 - Limber", 5: "5 - Light & Rested"}[x]
        )
    with b_col2:
        social_patience = st.select_slider(
            "Social Patience",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.daily_data["social_patience"],
            format_func=lambda x: {1: "1 - Short Fuse", 2: "2 - Low Patience", 3: "3 - Neutral", 4: "4 - Patient", 5: "5 - Connected"}[x]
        )
        financial_calm = st.select_slider(
            "Financial Peace of Mind",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.daily_data["financial_calm"],
            format_func=lambda x: {1: "1 - High Dread", 2: "2 - Unease", 3: "3 - Baseline", 4: "4 - In Control", 5: "5 - Calm"}[x]
        )

    # Dynamic Vitality Calculation
    sleep_debt = max(0.0, 7.5 - sleep_input)
    hr_penalty = max(0, (hr_input - 75) * 0.4) if hr_input > 75 else 0
    behavioral_bonus = (cognitive_clarity + physical_ease + social_patience + financial_calm) - 12

    calculated_vitality = int(max(5, min(100, 
        85 - (sleep_debt * 10) - (strain_input * 6) + (behavioral_bonus * 2.2) - hr_penalty
    )))

    # Historical Correlation
    history_df = load_history()
    rolling_vitality_avg = calculated_vitality
    if not history_df.empty and "Vitality" in history_df.columns:
        last_7_days = history_df.tail(7)["Vitality"].tolist()
        rolling_vitality_avg = sum(last_7_days) / len(last_7_days)

    if calculated_vitality >= 75 and rolling_vitality_avg >= 70:
        burnout_status = "Optimal Vitality (Strong buffer)"
        status_color = "#10b981"
    elif calculated_vitality < 50 or rolling_vitality_avg < 55:
        burnout_status = "High Burnout Risk (Fatigue accumulating)"
        status_color = "#ef4444"
    else:
        burnout_status = "Managing Baseline (Steady)"
        status_color = "#f59e0b"

    st.session_state.daily_data.update({
