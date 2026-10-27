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

# Custom Mobile-Friendly Dark Styling
st.markdown("""
<style>
    .main {
        background-color: #0d1117;
    }
    .bubble-card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 2px solid #30363d;
        border-radius: 24px;
        padding: 24px;
        margin: 16px 0;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .swipe-pill {
        display: inline-block;
        background-color: #21262d;
        color: #58a6ff;
        padding: 8px 18px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 12px;
        border: 1px solid #30363d;
    }
    div.stButton > button {
        border-radius: 12px;
        height: 3.2em;
        font-weight: 600;
        font-size: 1.05rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Management (Multi-Page Navigation) ---
if "current_step" not in st.session_state:
    st.session_state.current_step = 1

if "daily_data" not in st.session_state:
    st.session_state.daily_data = {
        "mood": 3,
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
# SCREEN 1: DAILY PULSE, MOOD FACE & BIOLOGICAL VITALITY
# ==============================================================================
if st.session_state.current_step == 1:
    st.title("🛡️ LifeShield")
    st.caption("Step 1 of 3: Daily Biological Check-in")

    # Animated Dynamic Face with Live Morphing Slider
    face_slider_html = """
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; background: #161b22; padding: 22px; border-radius: 20px; border: 1px solid #30363d; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
        <style>
            @keyframes subtleBreathe {
                0% { transform: translateY(0px) scale(1); }
                50% { transform: translateY(-4px) scale(1.02); }
                100% { transform: translateY(0px) scale(1); }
            }
            .interactive-face {
                animation: subtleBreathe 3.5s ease-in-out infinite;
                filter: drop-shadow(0px 8px 16px rgba(0,0,0,0.4));
                transition: all 0.25s ease;
            }
            .slider-range {
                -webkit-appearance: none;
                width: 90%;
                height: 10px;
                border-radius: 5px;
                background: linear-gradient(to right, #ef4444, #f97316, #f59e0b, #84cc16, #10b981);
                outline: none;
                margin-top: 20px;
                margin-bottom: 8px;
            }
            .slider-range::-webkit-slider-thumb {
                -webkit-appearance: none;
                appearance: none;
                width: 26px;
                height: 26px;
                border-radius: 50%;
                background: #ffffff;
                cursor: pointer;
                box-shadow: 0 0 10px rgba(0,0,0,0.5);
                border: 2px solid #0d1117;
            }
        </style>
        
        <div style="font-size: 1.2rem; font-weight: 700; color: #f0f6fc; margin-bottom: 14px;">How are you feeling today?</div>
        
        <!-- Live Morphing Face -->
        <svg id="moodFace" class="interactive-face" width="130" height="130" viewBox="0 0 100 100">
            <circle id="faceBg" cx="50" cy="50" r="45" fill="#f59e0b" stroke="#d97706" stroke-width="3.5"/>
            <circle id="leftEye" cx="35" cy="40" r="4.5" fill="#1e293b"/>
            <circle id="rightEye" cx="65" cy="40" r="4.5" fill="#1e293b"/>
            <path id="leftBrow" d="M 28 32 Q 35 32 42 32" stroke="#1e293b" stroke-width="3" stroke-linecap="round" fill="none"/>
            <path id="rightBrow" d="M 58 32 Q 65 32 72 32" stroke="#1e293b" stroke-width="3" stroke-linecap="round" fill="none"/>
            <path id="mouth" d="M 34 68 Q 50 68 66 68" stroke="#1e293b" stroke-width="4" stroke-linecap="round" fill="none"/>
        </svg>

        <div id="moodTitle" style="margin-top: 14px; font-weight: 700; color: #f59e0b; font-size: 1.05rem;">Steady / Managing</div>

        <input type="range" min="1" max="5" value="3" class="slider-range" id="moodRange" oninput="handleSlide(this.value)">
        <div style="display: flex; justify-content: space-between; width: 90%; font-size: 0.75rem; color: #8b949e; font-weight: 600;">
            <span>Exhausted</span>
            <span>Low</span>
            <span>Steady</span>
            <span>Good</span>
            <span>Energised</span>
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
            face.setAttribute("fill", "#ef4444");
            face.setAttribute("stroke", "#b91c1c");
            mouth.setAttribute("d", "M 32 74 Q 50 54 68 74"); // Deep frown
            leftBrow.setAttribute("d", "M 28 36 Q 35 30 42 35");
            rightBrow.setAttribute("d", "M 58 35 Q 65 30 72 36");
            title.innerText = "Exhausted / Burnout Alert";
            title.style.color = "#ef4444";
        } else if (val == 2) {
            face.setAttribute("fill", "#f97316");
            face.setAttribute("stroke", "#c2410c");
            mouth.setAttribute("d", "M 34 71 Q 50 62 66 71"); // Soft frown
            leftBrow.setAttribute("d", "M 28 34 Q 35 31 42 34");
            rightBrow.setAttribute("d", "M 58 34 Q 65 31 72 34");
            title.innerText = "Low Energy / Strained";
            title.style.color = "#f97316";
        } else if (val == 3) {
            face.setAttribute("fill", "#f59e0b");
            face.setAttribute("stroke", "#b45309");
            mouth.setAttribute("d", "M 34 68 Q 50 68 66 68"); // Flat neutral
            leftBrow.setAttribute("d", "M 28 32 Q 35 32 42 32");
            rightBrow.setAttribute("d", "M 58 32 Q 65 32 72 32");
            title.innerText = "Steady / Managing Baseline";
            title.style.color = "#f59e0b";
        } else if (val == 4) {
            face.setAttribute("fill", "#84cc16");
            face.setAttribute("stroke", "#4d7c0f");
            mouth.setAttribute("d", "M 32 64 Q 50 73 68 64"); // Soft smile
            leftBrow.setAttribute("d", "M 28 30 Q 35 29 42 32");
            rightBrow.setAttribute("d", "M 58 32 Q 65 29 72 30");
            title.innerText = "Good / Resilient";
            title.style.color = "#84cc16";
        } else {
            face.setAttribute("fill", "#10b981");
            face.setAttribute("stroke", "#047857");
            mouth.setAttribute("d", "M 30 62 Q 50 80 70 62"); // Big grin
            leftBrow.setAttribute("d", "M 28 28 Q 35 26 42 30");
            rightBrow.setAttribute("d", "M 58 30 Q 65 26 72 28");
            title.innerText = "Optimal Vitality / Energised";
            title.style.color = "#10b981";
        }
    }
    </script>
    """
    components.html(face_slider_html, height=275)

    # Feeling Selection & Heart Rate Inputs
    col_feel, col_hr = st.columns([2, 1])
    with col_feel:
        mood_input = st.select_slider(
            "Confirm Mood Score (1-5)",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.daily_data["mood"],
            format_func=lambda x: {
                1: "1 - Exhausted", 
                2: "2 - Low", 
                3: "3 - Steady", 
                4: "4 - Good", 
                5: "5 - Energised"
            }[x]
        )
    with col_hr:
        hr_input = st.number_input(
            "Heart Rate (BPM)",
            min_value=40,
            max_value=175,
            value=st.session_state.daily_data["heart_rate"],
            step=1
        )

    st.subheader("Shift & Physical Load")
    col_sleep, col_strain = st.columns(2)
    with col_sleep:
        sleep_input = st.slider("Hours Slept", 3.0, 11.0, float(st.session_state.daily_data["sleep"]), 0.5)
    with col_strain:
        strain_input = st.slider("Work / Shift Strain (1-5)", 1, 5, int(st.session_state.daily_data["strain"]),
                                help="1: Rest Day, 3: Standard Shift, 5: Heavy Overtime / Physically Demanding")

    # Dynamic Biological Vitality Calculation
    sleep_debt = max(0.0, 7.5 - sleep_input)
    hr_penalty = max(0, (hr_input - 75) * 0.4) if hr_input > 75 else 0
    calculated_vitality = int(max(5, min(100, 100 - (sleep_debt * 13) - (strain_input * 7) + ((mood_input - 3) * 6) - hr_penalty)))

    # Save calculated vitality into session
    st.session_state.daily_data.update({
        "mood": mood_input,
        "heart_rate": hr_input,
        "sleep": sleep_input,
        "strain": strain_input,
        "vitality": calculated_vitality
    })

    # Live Vitality Display on Screen 1
    v_color = "#10b981" if calculated_vitality >= 70 else ("#f59e0b" if calculated_vitality >= 45 else "#ef4444")
    st.markdown(f"""
    <div style="background-color: #161b22; border-left: 6px solid {v_color}; border-radius: 12px; padding: 16px; margin:
