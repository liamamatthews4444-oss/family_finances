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
            <path d="M 20 35 A 15 15 0 0 1 35 15 A 20 20 0 0 1 70 18 A 15 15 0 0 1 85 35 Z"/>
        </svg>
        <svg class="cloud-bg-2" width="120" height="45" viewBox="0 0 100 45" fill="#e0f2fe">
            <path d="M 20 35 A 12 12 0 0 1 32 18 A 18 18 0 0 1 65 20 A 12 12 0 0 1 80 35 Z"/>
        </svg>

        <!-- Translucent Frosted Glass Card -->
        <div style="position: relative; z-index: 2; background: rgba(15, 23, 42, 0.72); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); border-radius: 18px; border: 1px solid rgba(255, 255, 255, 0.15); padding: 18px 12px; display: flex; flex-direction: column; align-items: center;">
            <div style="font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin-bottom: 12px; letter-spacing: -0.01em;">How are you feeling right now?</div>

            <!-- Morphing Reactive SVG Face -->
            <svg id="moodFace" class="interactive-face" width="125" height="125" viewBox="0 0 100 100">
                <circle id="faceBg" cx="50" cy="50" r="45" fill="#f59e0b" stroke="#d97706" stroke-width="3.5"/>
                <circle id="leftEye" cx="35" cy="40" r="4.5" fill="#0f172a"/>
                <circle id="rightEye" cx="65" cy="40" r="4.5" fill="#0f172a"/>
                <path id="leftBrow" d="M 28 32 Q 35 32 42 32" stroke="#0f172a" stroke-width="3" stroke-linecap="round" fill="none"/>
                <path id="rightBrow" d="M 58 32 Q 65 32 72 32" stroke="#0f172a" stroke-width="3" stroke-linecap="round" fill="none"/>
                <path id="mouth" d="M 34 68 Q 50 68 66 68" stroke="#0f172a" stroke-width="4" stroke-linecap="round" fill="none"/>
            </svg>

            <!-- State Title -->
            <div id="moodTitle" style="margin-top: 12px; font-weight: 700; color: #f59e0b; font-size: 1.1rem;">Managing baseline</div>

            <!-- Face Controller Range -->
            <input type="range" min="1" max="5" value="3" class="slider-range" id="moodRange" oninput="handleSlide(this.value)">
            
            <!-- Scale Labels -->
            <div style="display: flex; justify-content: space-between; width: 92%; font-size: 0.72rem; color: #cbd5e1; font-weight: 600; padding: 0 4px; box-sizing: border-box;">
                <span style="text-align: left;">Burnout</span>
                <span style="text-align: center;">Strained</span>
                <span style="text-align: center;">Managing baseline</span>
                <span style="text-align: center;">Resilient</span>
                <span style="text-align: right;">Energised</span>
            </div>
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
            title.innerText = "Burnout";
            title.style.color = "#ef4444";
        } else if (val == 2) {
            face.setAttribute("fill", "#f97316");
            face.setAttribute("stroke", "#c2410c");
            mouth.setAttribute("d", "M 34 71 Q 50 62 66 71"); // Slight frown
            leftBrow.setAttribute("d", "M 28 34 Q 35 31 42 34");
            rightBrow.setAttribute("d", "M 58 34 Q 65 31 72 34");
            title.innerText = "Strained";
            title.style.color = "#f97316";
        } else if (val == 3) {
            face.setAttribute("fill", "#f59e0b");
            face.setAttribute("stroke", "#b45309");
            mouth.setAttribute("d", "M 34 68 Q 50 68 66 68"); // Neutral line
            leftBrow.setAttribute("d", "M 28 32 Q 35 32 42 32");
            rightBrow.setAttribute("d", "M 58 32 Q 65 32 72 32");
            title.innerText = "Managing baseline";
            title.style.color = "#f59e0b";
        } else if (val == 4) {
            face.setAttribute("fill", "#84cc16");
            face.setAttribute("stroke", "#4d7c0f");
            mouth.setAttribute("d", "M 32 64 Q 50 73 68 64"); // Soft smile
            leftBrow.setAttribute("d", "M 28 30 Q 35 29 42 32");
            rightBrow.setAttribute("d", "M 58 32 Q 65 29 72 30");
            title.innerText = "Resilient";
            title.style.color = "#84cc16";
        } else {
            face.setAttribute("fill", "#10b981");
            face.setAttribute("stroke", "#047857");
            mouth.setAttribute("d", "M 30 62 Q 50 80 70 62"); // Big grin
            leftBrow.setAttribute("d", "M 28 28 Q 35 26 42 30");
            rightBrow.setAttribute("d", "M 58 30 Q 65 26 72 28");
            title.innerText = "Energised";
            title.style.color = "#10b981";
        }
    }
    </script>
    """
    components.html(sky_face_html, height=310)

    # Metric 1 (Present State Log) & Heart Rate
    col_feel, col_hr = st.columns([2, 1])
    with col_feel:
        present_mood = st.select_slider(
            "Log Present Feeling",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.daily_data["present_mood"],
            format_func=lambda x: {
                1: "1 - Burnout", 
                2: "2 - Strained", 
                3: "3 - Managing baseline", 
                4: "4 - Resilient", 
                5: "5 - Energised"
            }[x]
        )
    with col_hr:
        hr_input = st.number_input(
            "Heart Rate (BPM)",
            min_value=40,
            max_value=175,
            value=st.session_state.daily_data["heart_rate"],
            step=1,
            help="Resting morning HR or post-shift reading."
        )

    # Metric 2: Predictive Life Outlook / Forward Trajectory (Recognising Patterns)
    st.markdown("#### 🔭 Forward Trajectory & Momentum")
    st.caption("How do you feel about the upcoming 7-14 day demands and financial momentum?")
    outlook_input = st.select_slider(
        "Life & Financial Outlook",
        options=[1, 2, 3, 4, 5],
        value=st.session_state.daily_data["life_outlook"],
        format_func=lambda x: {
            1: "1 - High Friction / Overloaded",
            2: "2 - Heavy Drag / Under Pressure",
            3: "3 - Balanced Trajectory",
            4: "4 - Confident / Steady Flow",
            5: "5 - Gaining Momentum & Expansion"
        }[x]
    )

    st.divider()

    # Shift & Physical Strain Inputs
    st.subheader("Shift & Physical Load")
    col_sleep, col_strain = st.columns(2)
    with col_sleep:
        sleep_input = st.slider("Hours Slept", 3.0, 11.0, float(st.session_state.daily_data["sleep"]), 0.5)
    with col_strain:
        strain_input = st.slider("Work / Shift Strain (1-5)", 1, 5, int(st.session_state.daily_data["strain"]),
                                help="1: Rest Day, 3: Standard Shift, 5: Heavy Overtime / High Physical Demand")

    # Dynamic Biological Vitality Calculation
    sleep_debt = max(0.0, 7.5 - sleep_input)
    hr_penalty = max(0, (hr_input - 75) * 0.4) if hr_input > 75 else 0
    calculated_vitality = int(max(5, min(100, 
        100 
        - (sleep_debt * 12) 
        - (strain_input * 7) 
        + ((present_mood - 3) * 5) 
        + ((outlook_input - 3) * 4) 
        - hr_penalty
    )))

    # Save inputs into session
    st.session_state.daily_data.update({
        "present_mood": present_mood,
        "life_outlook": outlook_input,
        "heart_rate": hr_input,
        "sleep": sleep_input,
        "strain": strain_input,
        "vitality": calculated_vitality
    })

    # Biological Vitality Badge
    v_color = "#10b981" if calculated_vitality >= 70 else ("#f59e0b" if calculated_vitality >= 45 else "#ef4444")
    st.markdown(f"""
    <div style="background-color: #131b2e; border-left: 6px solid {v_color}; border-radius: 14px; padding: 16px; margin: 16px 0; text-align: center;">
        <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Calculated Biological Vitality</div>
        <div style="font-size: 2.2rem; font-weight: 800; color: {v_color};">{calculated_vitality} / 100</div>
    </div>
    """, unsafe_allow_html=True)

    # Save and Move to Screen 2
    if st.button("💾 Save Check-in & Review Status →", use_container_width=True, type="primary"):
        st.session_state.current_step = 2
        st.rerun()

# ==============================================================================
# SCREEN 2: BUBBLE STATUS CARDS (VITALITY & FINANCIAL HEALTH OUT OF 100)
# ==============================================================================
elif st.session_state.current_step == 2:
    st.title("🛡️ LifeShield State")
    st.caption("Step 2 of 3: Daily Summary Cards")

    vitality = st.session_state.daily_data["vitality"]
    savings = st.session_state.daily_data["savings"]
    weekly_burn = st.session_state.daily_data["weekly_burn"]
    runway_weeks = round(savings / weekly_burn, 1)

    # Financial Health Score out of 100 (12+ weeks of runway = 100 pts)
    financial_health_score = int(min(100, max(10, (runway_weeks / 12.0) * 100)))
    st.session_state.daily_data["financial_score"] = financial_health_score

    # Bubble 1: Biological Vitality State
    v_color = "#10b981" if vitality >= 70 else ("#f59e0b" if vitality >= 45 else "#ef4444")
    v_badge = "OPTIMAL RESERVE" if vitality >= 70 else ("ELEVATED STRAIN" if vitality >= 45 else "BURNOUT WARNING")
    
    st.markdown(f"""
    <div class="bubble-card" style="border-color: {v_color};">
        <div class="swipe-pill">BUBBLE 1: BIOLOGICAL STATE</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #94a3b8;">Biological Vitality Index</div>
        <div style="font-size: 3.6rem; font-weight: 800; color: {v_color}; margin: 8px 0;">{vitality}<span style="font-size: 1.5rem; color: #94a3b8;">/100</span></div>
        <div style="background-color: {v_color}22; color: {v_color}; display: inline-block; padding: 6px 14px; border-radius: 12px; font-weight: 700; font-size: 0.9rem;">
            {v_badge}
        </div>
        <div style="margin-top: 14px; color: #cbd5e1; font-size: 0.95rem;">
            Sleep: <b>{st.session_state.daily_data['sleep']}h</b> | Heart Rate: <b>{st.session_state.daily_data['heart_rate']} BPM</b> | Shift Strain: <b>{st.session_state.daily_data['strain']}/5</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bubble 2: Financial Health State
    f_color = "#10b981" if financial_health_score >= 70 else ("#f59e0b" if financial_health_score >= 45 else "#ef4444")
    f_badge = "SHIELDED RUNWAY" if financial_health_score >= 70 else ("MODERATE BUFFER" if financial_health_score >= 45 else "VULNERABLE RUNWAY")

    st.markdown(f"""
    <div class="bubble-card" style="border-color: {f_color};">
        <div class="swipe-pill" style="color: #4ade80; border-color: #166534;">BUBBLE 2: ECONOMIC HEALTH</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #94a3b8;">Current Financial Health</div>
        <div style="font-size: 3.6rem; font-weight: 800; color: {f_color}; margin: 8px 0;">{financial_health_score}<span style="font-size: 1.5rem; color: #94a3b8;">/100</span></div>
        <div style="background-color: {f_color}22; color: {f_color}; display: inline-block; padding: 6px 14px; border-radius: 12px; font-weight: 700; font-size: 0.9rem;">
            {f_badge}
        </div>
        <div style="margin-top: 14px; color: #cbd5e1; font-size: 0.95rem;">
            Liquid Buffer: <b>£{savings:,}</b> | Safe Runway: <b>{runway_weeks} Weeks</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
# SCREEN 3: INTERACTIVE SAVINGS, INCOME & FUTURE BLIP SIMULATOR
# ==============================================================================
elif st.session_state.current_step == 3:
    st.title("🛡️ Financial Shield & Planner")
    st.caption("Step 3 of 3: Interactive Budget & Future Blip Testing")

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

    # Future Blip Simulator
    st.subheader("⚡ Future Blip Simulator")
    st.caption("Test how unforeseen emergencies or rest periods affect your shield.")

    blip_col1, blip_col2 = st.columns(2)
    with blip_col1:
        vehicle_blip = st.slider("Emergency Repair / Bill (£)", 0, 2000, 0, 100)
    with blip_col2:
        unpaid_rest_weeks = st.slider("Fatigue / Unpaid Recovery (Weeks)", 0, 4, 0, 1)

    # Calculate Impact of Blip
    blip_savings = max(0, savings_adj - vehicle_blip - (unpaid_rest_weeks * burn_adj))
    blip_runway = round(blip_savings / burn_adj, 1)

    st.markdown(f"""
    <div style="background-color: #131b2e; border: 1px solid #233554; border-radius: 16px; padding: 18px; margin-top: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #94a3b8;">Standard Safe Runway:</span>
            <span style="font-weight: 700; color: #38bdf8;">{calc_runway} Weeks</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
            <span style="color: #94a3b8;">Post-Blip Protected Runway:</span>
            <span style="font-weight: 700; color: {'#10b981' if blip_runway >= 8 else '#ef4444'};">{blip_runway} Weeks</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Save Check-in Entry to CSV File
    st.divider()
    DATA_FILE = "lifeshield_history.csv"

    if st.button("💾 Commit Today's Log to Long-Term Trends", use_container_width=True, type="primary"):
        today = datetime.date.today().strftime("%Y-%m-%d")
        new_row = pd.DataFrame([{
            "Date": today,
            "PresentMood": st.session_state.daily_data["present_mood"],
            "LifeOutlook": st.session_state.daily_data["life_outlook"],
            "HeartRate": st.session_state.daily_data["heart_rate"],
            "Sleep": st.session_state.daily_data["sleep"],
            "Strain": st.session_state.daily_data["strain"],
            "Vitality": st.session_state.daily_data["vitality"],
            "FinancialScore": st.session_state.daily_data["financial_score"],
            "Savings": savings_adj,
            "RunwayWeeks": calc_runway
        }])

        if os.path.exists(DATA_FILE):
            history_df = pd.read_csv(DATA_FILE)
            history_df = history_df[history_df["Date"] != today]
            history_df = pd.concat([history_df, new_row], ignore_index=True)
        else:
            history_df = new_row

        history_df.to_csv(DATA_FILE, index=False)
        st.success(f"Check-in successfully locked for {today}!")

    # Display History Graph if available
    if os.path.exists(DATA_FILE):
        hist = pd.read_csv(DATA_FILE)
        if len(hist) > 1:
            st.subheader("Historical Vitality vs Financial Shield")
            st.line_chart(hist.set_index("Date")[["Vitality", "FinancialScore", "RunwayWeeks"]])

    if st.button("← Return to Daily Pulse", use_container_width=True):
        st.session_state.current_step = 1
        st.rerun()
