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

# --- Helper: Load History & Calculate Adaptive Baselines ---
def load_history():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
            return df.sort_values("Date")
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

# --- Session State Management ---
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
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
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
                position: relative;
                z-index: 2;
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 100%;
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
                width: 26px;
                height: 26px;
                border-radius: 50%;
                background: #ffffff;
                cursor: pointer;
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
            face.setAttribute("fill", "#ef4444");
            face.setAttribute("stroke", "#b91c1c");
            mouth.setAttribute("d", "M 32 74 Q 50 54 68 74");
            leftBrow.setAttribute("d", "M 28 36 Q 35 30 42 35");
            rightBrow.setAttribute("d", "M 58 35 Q 65 30 72 36");
            title.innerText = "Burnout";
            title.style.color = "#ef4444";
        } else if (val == 2) {
            face.setAttribute("fill", "#f97316");
            face.setAttribute("stroke", "#c2410c");
            mouth.setAttribute("d", "M 34 71 Q 50 62 66 71");
            leftBrow.setAttribute("d", "M 28 34 Q 35 31 42 34");
            rightBrow.setAttribute("d", "M 58 34 Q 65 31 72 34");
            title.innerText = "Strained";
            title.style.color = "#f97316";
        } else if (val == 3) {
            face.setAttribute("fill", "#f59e0b");
            face.setAttribute("stroke", "#b45309");
            mouth.setAttribute("d", "M 34 68 Q 50 68 66 68");
            leftBrow.setAttribute("d", "M 28 32 Q 35 32 42 32");
            rightBrow.setAttribute("d", "M 58 32 Q 65 32 72 32");
            title.innerText = "Managing baseline";
            title.style.color = "#f59e0b";
        } else if (val == 4) {
            face.setAttribute("fill", "#84cc16");
            face.setAttribute("stroke", "#4d7c0f");
            mouth.setAttribute("d", "M 32 64 Q 50 73 68 64");
            leftBrow.setAttribute("d", "M 28 30 Q 35 29 42 32");
            rightBrow.setAttribute("d", "M 58 32 Q 65 29 72 30");
            title.innerText = "Resilient";
            title.style.color = "#84cc16";
        } else {
            face.setAttribute("fill", "#10b981");
            face.setAttribute("stroke", "#047857");
            mouth.setAttribute("d", "M 30 62 Q 50 80 70 62");
            leftBrow.setAttribute("d", "M 28 28 Q 35 26 42 30");
            rightBrow.setAttribute("d", "M 58 30 Q 65 26 72 28");
            title.innerText = "Energised";
            title.style.color = "#10b981";
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
            step=1,
            help="Resting morning HR or post-shift reading."
        )
    with col_sleep:
        sleep_input = st.slider("Hours Slept", 3.0, 11.0, float(st.session_state.daily_data["sleep"]), 0.5)

    strain_input = st.slider("Work / Shift Strain (1-5)", 1, 5, int(st.session_state.daily_data["strain"]),
                            help="1: Off/Rest Day, 3: Standard Shift, 5: Heavy Overtime / Physically Exhausting")

    st.divider()

    # Behavioral Signals (Left = Low / Fatigued, Right = High / Optimal)
    st.subheader("🧠 Behavioral & Focus Signals")

    b_col1, b_col2 = st.columns(2)
    with b_col1:
        cognitive_clarity = st.select_slider(
            "Focus / Clarity",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.daily_data["cognitive_clarity"],
            format_func=lambda x: {
                1: "1 - Brain Fog",
                2: "2 - Sluggish",
                3: "3 - Standard",
                4: "4 - Clear",
                5: "5 - Peak Flow"
            }[x]
        )
        physical_ease = st.select_slider(
            "Physical Comfort",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.daily_data["physical_ease"],
            format_func=lambda x: {
                1: "1 - Heavy Aches",
                2: "2 - Stiff / Sore",
                3: "3 - Normal",
                4: "4 - Limber",
                5: "5 - Light & Rested"
            }[x]
        )
    with b_col2:
        social_patience = st.select_slider(
            "Social Patience",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.daily_data["social_patience"],
            format_func=lambda x: {
                1: "1 - Short Fuse",
                2: "2 - Low Patience",
                3: "3 - Neutral",
                4: "4 - Patient",
                5: "5 - Connected"
            }[x]
        )
        financial_calm = st.select_slider(
            "Financial Peace of Mind",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.daily_data["financial_calm"],
            format_func=lambda x: {
                1: "1 - High Dread",
                2: "2 - Noticeable Unease",
                3: "3 - Baseline",
                4: "4 - In Control",
                5: "5 - Calm & Confident"
            }[x]
        )

    # Dynamic Vitality Calculation
    sleep_debt = max(0.0, 7.5 - sleep_input)
    hr_penalty = max(0, (hr_input - 75) * 0.4) if hr_input > 75 else 0
    behavioral_bonus = (cognitive_clarity + physical_ease + social_patience + financial_calm) - 12

    calculated_vitality = int(max(5, min(100, 
        85 
        - (sleep_debt * 10) 
        - (strain_input * 6) 
        + (behavioral_bonus * 2.2) 
        - hr_penalty
    )))

    # Historical Adaptive Correlation
    history_df = load_history()
    rolling_vitality_avg = calculated_vitality
    if not history_df.empty and "Vitality" in history_df.columns:
        last_7_days = history_df.tail(7)["Vitality"].tolist()
        rolling_vitality_avg = sum(last_7_days) / len(last_7_days)

    if calculated_vitality >= 75 and rolling_vitality_avg >= 70:
        burnout_status = "Optimal Vitality (Strong, consistent physiological buffer)"
        status_color = "#10b981"
    elif calculated_vitality < 50 or rolling_vitality_avg < 55:
        burnout_status = "High Burnout Risk (Fatigue accumulation threatening capacity)"
        status_color = "#ef4444"
    else:
        burnout_status = "Managing Baseline (Steady, but monitor weekly recovery)"
        status_color = "#f59e0b"

    st.session_state.daily_data.update({
        "heart_rate": hr_input,
        "sleep": sleep_input,
        "strain": strain_input,
        "cognitive_clarity": cognitive_clarity,
        "physical_ease": physical_ease,
        "social_patience": social_patience,
        "financial_calm": financial_calm,
        "vitality": calculated_vitality,
        "rolling_vitality_avg": round(rolling_vitality_avg, 1),
        "burnout_status": burnout_status
    })

    st.markdown(f"""
    <div style="background-color: #131b2e; border-left: 6px solid {status_color}; border-radius: 14px; padding: 16px; margin: 20px 0; text-align: center;">
        <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Calculated Biological Vitality</div>
        <div style="font-size: 2.2rem; font-weight: 800; color: {status_color};">{calculated_vitality} / 100</div>
        <div style="font-size: 0.88rem; color: {status_color}; font-weight: 600; margin-top: 4px;">{burnout_status}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💾 Save Check-in & Review Status →", use_container_width=True, type="primary"):
        st.session_state.current_step = 2
        st.rerun()

# ==============================================================================
# SCREEN 2: BUBBLE STATUS CARDS (CLEAN TITLES & AUTO SCROLL TO TOP)
# ==============================================================================
elif st.session_state.current_step == 2:
    # Auto-scroll browser window to top on page render
    components.html("<script>window.parent.scrollTo(0, 0);</script>", height=0)

    st.title("🛡️ LifeShield State")
    st.caption("Step 2 of 3: Daily Summary Cards")

    vitality = st.session_state.daily_data["vitality"]
    savings = st.session_state.daily_data["savings"]
    weekly_burn = st.session_state.daily_data["weekly_burn"]
    runway_weeks = round(savings / weekly_burn, 1)

    # 12+ weeks of runway = 100 pts
    financial_health_score = int(min(100, max(10, (runway_weeks / 12.0) * 100)))
    st.session_state.daily_data["financial_score"] = financial_health_score

    # Bubble 1: Biological Vitality (Single Blue Pill Badge, No Duplicate Title)
    v_color = "#10b981" if vitality >= 75 else ("#f59e0b" if vitality >= 50 else "#ef4444")
    
    st.markdown(f"""
    <div class="bubble-card" style="border-color: {v_color};">
        <div class="swipe-pill" style="color: #38bdf8; border-color: #0284c7;">BIOLOGICAL VITALITY</div>
        <div style="font-size: 3.8rem; font-weight: 800; color: {v_color}; margin: 8px 0;">{vitality}<span style="font-size: 1.5rem; color: #8b949e;">/100</span></div>
        <div style="color: {v_color}; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">
            {st.session_state.daily_data['burnout_status']}
        </div>
        <div style="margin-top: 14px; color: #cbd5e1; font-size: 0.92rem;">
            Sleep: <b>{st.session_state.daily_data['sleep']}h</b> | HR: <b>{st.session_state.daily_data['heart_rate']} BPM</b> | Shift Load: <b>{st.session_state.daily_data['strain']}/5</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bubble 2: Financial Health (Single Green Pill Badge, No Duplicate Title)
    f_color = "#10b981" if financial_health_score >= 70 else ("#f59e0b" if financial_health_score >= 45 else "#ef4444")
    f_badge = "SHIELDED RUNWAY" if financial_health_score >= 70 else ("MODERATE BUFFER" if financial_health_score >= 45 else "VULNERABLE RUNWAY")

    st.markdown(f"""
    <div class="bubble-card" style="border-color: {f_color};">
        <div class="swipe-pill" style="color: #4ade80; border-color: #166534;">FINANCIAL HEALTH</div>
        <div style="font-size: 3.8rem; font-weight: 800; color: {f_color}; margin: 8px 0;">{financial_health_score}<span style="font-size: 1.5rem; color: #8b949e;">/100</span></div>
        <div style="background-color: {f_color}22; color: {f_color}; display: inline-block; padding: 6px 14px; border-radius: 12px; font-weight: 700; font-size: 0.9rem;">
            {f_badge}
        </div>
        <div style="margin-top: 14px; color: #cbd5e1; font-size: 0.95rem;">
            Liquid Buffer: <b>£{savings:,}</b> | Safe Runway: <b>{runway_weeks} Weeks</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if vitality < 55 and runway_weeks < 8:
        st.error("⚠️ COUPLED RISK ALERT: Persistent low vitality alongside a thin financial buffer (< 8 weeks). Physical downtime risks acute financial friction.")

    # Navigation Buttons
    st.write("")
    col_back, col_next = st.columns([1, 2])
    with col_back:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    with col_next:
        if st.button("👉 Swipe to Interactive Planner →", use_container_width=True, type="primary"):
            st.session_state.current_step = 3
            st.rerun()

# ==============================================================================
# SCREEN 3: INTERACTIVE PLANNER, BLIP SIMULATOR & CSV EXPORT
# ==============================================================================
elif st.session_state.current_step == 3:
    components.html("<script>window.parent.scrollTo(0, 0);</script>", height=0)

    st.title("🛡️ Financial Shield & Planner")
    st.caption("Step 3 of 3: Interactive Budget & Data Management")

    st.subheader("Household Economic Controls")
    col_sav, col_burn = st.columns(2)
    with col_sav:
        savings_adj = st.number_input(
            "Liquid Emergency Buffer (£)", 
            min_value=0, 
            value=int(st.session_state.daily_data["savings"]), 
            step=250
        )
    with col_burn:
        burn_adj = st.number_input(
            "Weekly Baseline Burn (£)", 
            min_value=100, 
            value=int(st.session_state.daily_data["weekly_burn"]), 
            step=25,
            help="Fixed basics: rent/mortgage, council tax, food essentials, core transport"
        )

    income_adj = st.number_input(
        "Estimated Monthly Net Household Income (£)",
        min_value=0,
        value=int(st.session_state.daily_data["monthly_income"]),
        step=100
    )

    st.session_state.daily_data["savings"] = savings_adj
    st.session_state.daily_data["weekly_burn"] = burn_adj
    st.session_state.daily_data["monthly_income"] = income_adj

    calc_runway = round(savings_adj / burn_adj, 1)

    st.divider()

    st.subheader("⚡ Future Blip Simulator")
    st.caption("Test how unforeseen emergencies or rest periods affect your shield.")

    blip_col1, blip_col2 = st.columns(2)
    with blip_col1:
        vehicle_blip = st.slider("Emergency Repair / Bill (£)", 0, 2000, 0, 100)
    with blip_col2:
        unpaid_rest_weeks = st.slider("Fatigue / Unpaid Recovery (Weeks)", 0, 4, 0, 1)

    blip_savings = max(0, savings_adj - vehicle_blip - (unpaid_rest_weeks * burn_adj))
    blip_runway = round(blip_savings / burn_adj, 1)

    st.markdown(f"""
    <div style="background-color: #131b2e; border: 1px solid #233554; border-radius: 16px; padding: 18px; margin-top: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #94a3b8;">Standard Safe Runway:</span>
            <span style="font-weight: 700; color
