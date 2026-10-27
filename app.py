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
    .main { background-color: #0b0f19; }
    div.stButton > button {
        border-radius: 12px;
        height: 3.2em;
        font-weight: 600;
        font-size: 1.05rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 3rem;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "lifeshield_history.csv"

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
        "monthly_nut": 1850
    }

# ==============================================================================
# SCREEN 1: REAL-SKY MOOD FACE & ADAPTIVE CHECK-IN
# ==============================================================================
if st.session_state.current_step == 1:
    st.title("🛡️ LifeShield")
    st.caption("Daily Biometrics & Adaptive Health Pulse")

    if os.path.exists("face.html"):
        with open("face.html", "r", encoding="utf-8") as f:
            components.html(f.read(), height=310)

    col_hr, col_sleep = st.columns(2)
    with col_hr:
        hr_input = st.number_input(
            "Heart Rate (BPM)",
            min_value=40,
            max_value=175,
            value=int(st.session_state.daily_data["heart_rate"]),
            step=1
        )
    with col_sleep:
        sleep_input = st.slider(
            "Hours Slept",
            3.0, 11.0,
            float(st.session_state.daily_data["sleep"]),
            0.5
        )

    strain_input = st.slider(
        "Work / Shift Strain (1-5)",
        1, 5,
        int(st.session_state.daily_data["strain"]),
        help="1: Rest Day, 3: Standard Shift, 5: Heavy Overtime"
    )

    st.divider()
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
                2: "2 - Unease",
                3: "3 - Baseline",
                4: "4 - In Control",
                5: "5 - Calm & Confident"
            }[x]
        )

    # Calculation
    sleep_debt = max(0.0, 7.5 - sleep_input)
    hr_penalty = max(0.0, (hr_input - 75) * 0.4) if hr_input > 75 else 0.0
    behavioral_bonus = (cognitive_clarity + physical_ease + social_patience + financial_calm) - 12
    calculated_vitality = int(max(5, min(100, 85 - (sleep_debt * 10) - (strain_input * 6) + (behavioral_bonus * 2.2) - hr_penalty)))

    history_df = load_history()
    rolling_vitality_avg = calculated_vitality
    if not history_df.empty and "Vitality" in history_df.columns:
        last_7_days = history_df.tail(7)["Vitality"].tolist()
        rolling_vitality_avg = sum(last_7_days) / len(last_7_days)

    if calculated_vitality >= 75 and rolling_vitality_avg >= 70:
        burnout_status = "Optimal Vitality (Strong buffer)"
    elif calculated_vitality < 50 or rolling_vitality_avg < 55:
        burnout_status = "High Burnout Risk (Fatigue accumulating)"
    else:
        burnout_status = "Managing Baseline (Steady)"

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

    with st.container(border=True):
        st.caption("CALCULATED BIOLOGICAL VITALITY")
        st.metric("Vitality Index", f"{calculated_vitality} / 100")
        if calculated_vitality >= 75:
            st.success(burnout_status)
        elif calculated_vitality >= 50:
            st.warning(burnout_status)
        else:
            st.error(burnout_status)

    if st.button("💾 Save Check-in & Review Status →", use_container_width=True, type="primary"):
        st.session_state.current_step = 2
        st.rerun()

# ==============================================================================
# SCREEN 2: BUBBLE STATUS CARDS (NATIVE STREAMLIT CONTAINERS)
# ==============================================================================
elif st.session_state.current_step == 2:
    components.html("<script>window.parent.scrollTo(0, 0);</script>", height=0)

    st.title("🛡️ LifeShield State")
    st.caption("Step 2 of 3: Daily Summary Cards")

    vitality = st.session_state.daily_data["vitality"]
    savings = st.session_state.daily_data["savings"]
    monthly_nut = st.session_state.daily_data["monthly_nut"]
    weekly_burn = monthly_nut / 4.33
    runway_weeks = round(savings / weekly_burn, 1)

    financial_health_score = int(min(100, max(10, (runway_weeks / 12.0) * 100)))
    st.session_state.daily_data["financial_score"] = financial_health_score

    # Bubble 1: Biological Vitality
    with st.container(border=True):
        st.markdown("### 🔵 BIOLOGICAL VITALITY")
        st.metric("Vitality Score", f"{vitality} / 100")
        if vitality >= 75:
            st.success(st.session_state.daily_data["burnout_status"])
        elif vitality >= 50:
            st.warning(st.session_state.daily_data["burnout_status"])
        else:
            st.error(st.session_state.daily_data["burnout_status"])
        st.caption(f"Sleep: {st.session_state.daily_data['sleep']}h | HR: {st.session_state.daily_data['heart_rate']} BPM | Strain: {st.session_state.daily_data['strain']}/5")

    # Bubble 2: Financial Health
    with st.container(border=True):
        st.markdown("### 🟢 FINANCIAL HEALTH")
        st.metric("Health Score", f"{financial_health_score} / 100")
        if financial_health_score >= 70:
            st.success("SHIELDED RUNWAY")
        elif financial_health_score >= 45:
            st.warning("MODERATE BUFFER")
        else:
            st.error("VULNERABLE RUNWAY")
        st.caption(f"Liquid Cushion: £{savings:,} | Safe Runway: {runway_weeks} Weeks")

    if vitality < 55 and runway_weeks < 8:
        st.error("⚠️ COUPLED RISK ALERT: Low vitality alongside thin savings runway (< 8 weeks).")

    col_back, col_next = st.columns([1, 2])
    with col_back:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    with col_next:
        if st.button("👉 Swipe to Financial Shield →", use_container_width=True, type="primary"):
            st.session_state.current_step = 3
            st.rerun()

# ==============================================================================
# SCREEN 3: FINANCIAL RESILIENCE SHIELD & TRAJECTORY
# ==============================================================================
elif st.session_state.current_step == 3:
    components.html("<script>window.parent.scrollTo(0, 0);</script>", height=0)

    st.title("🛡️ Financial Resilience Shield")
    st.caption("Step 3 of 3: Core Stored Reserves & Trajectory")

    col_sav, col_nut = st.columns(2)
    with col_sav:
        savings_adj = st.number_input(
            "Stored Liquid Cash (£)",
            min_value=0,
            value=int(st.session_state.daily_data["savings"]),
            step=250,
            help="Total accessible emergency cash."
        )
    with col_nut:
        nut_adj = st.number_input(
            "Monthly Survival Nut (£)",
            min_value=500,
            value=int(st.session_state.daily_data["monthly_nut"]),
            step=50,
            help="Fixed essentials: housing, council tax, core food, utilities, fixed debt."
        )

    st.session_state.daily_data["savings"] = savings_adj
    st.session_state.daily_data["monthly_nut"] = nut_adj

    weekly_burn = nut_adj / 4.33
    calc_runway = round(savings_adj / weekly_burn, 1)

    # Native Runway Display
    with st.container(border=True):
        st.caption("AUTOPILOT FAMILY RUNWAY")
        st.metric("Survival Runway", f"{calc_runway} Weeks")
        if calc_runway >= 12:
            st.success("Solid buffer: Over 3 months of survival expenses secured.")
        elif calc_runway >= 6:
            st.warning("Moderate buffer: 6 to 12 weeks of survival expenses.")
        else:
            st.error("Thin buffer: Under 6 weeks of essential living costs.")

    st.divider()

    # 4-Year Long-Term Debt-to-0 & Wealth Trajectory
    st.subheader("📈 4-Year Debt-to-0 & Wealth Curve")
    st.caption("Structural journey from historical debt into positive reserves.")

    wealth_data = pd.DataFrame({
        "Period": ["2023 H1", "2023 H2", "2024 H1", "2024 H2", "2025 H1", "2025 H2", "2026 H1", "Present"],
        "Debt Remaining": [8200, 6800, 5400, 3900, 2400, 1100, 450, 0],
        "Liquid Reserves": [800, 1100, 1400, 1900, 2400, 2900, 3200, savings_adj]
    }).set_index("Period")

    st.line_chart(wealth_data)

    st.divider()

    # Reality Blip Stress-Test
    st.subheader("⚡ Reality 'Blip' Stress-Test")
    st.caption("Test how unforeseen friction affects your runway.")

    blip_col1, blip_col2 = st.columns(2)
    with blip_col1:
        vehicle_blip = st.slider("Emergency Repair (£)", 0, 2000, 0, 100)
    with blip_col2:
        unpaid_rest_weeks = st.slider("Unpaid Leave (Weeks)", 0, 4, 0, 1)

    blip_savings = max(0, savings_adj - vehicle_blip - (unpaid_rest_weeks * weekly_burn))
    blip_runway = round(blip_savings / weekly_burn, 1)

    with st.container(border=True):
        r1, r2 = st.columns(2)
        with r1:
