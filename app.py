import streamlit as st
import pandas as pd
import datetime
import os

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
    .main { background-color: #0b0f19; }
    div.stButton > button {
        border-radius: 12px;
        height: 3.2em;
        font-weight: 600;
        font-size: 1.05rem;
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
# SCREEN 1: DAILY BIOLOGICAL PULSE
# ==============================================================================
if st.session_state.current_step == 1:
    st.title("🛡️ LifeShield")
    st.caption("Daily Biometrics & Adaptive Health Pulse")

    # Pure Python Mood Selector
    with st.container(border=True):
        st.subheader("How are you feeling right now?")
        mood_input = st.select_slider(
            "State",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.daily_data["mood"],
            format_func=lambda x: {
                1: "🔴 Burnout",
                2: "🟠 Strained",
                3: "🟡 Managing baseline",
                4: "🟢 Resilient",
                5: "🌟 Energised"
            }[x],
            label_visibility="collapsed"
        )
        
        # Display corresponding mood feedback
        mood_labels = {
            1: ("Burnout", "High risk of physical exhaustion. Rest needed."),
            2: ("Strained", "Fatigue accumulating. Pace today's output."),
            3: ("Managing baseline", "Steady energy. Operating within normal bounds."),
            4: ("Resilient", "Good capacity and physical reserve."),
            5: ("Energised", "Optimal vitality. High focus and endurance.")
        }
        title, desc = mood_labels[mood_input]
        st.info(f"**{title}**: {desc}")

    st.write("")
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
        help="1: Rest Day, 3: Standard Shift, 5: Heavy Overtime / Physically Exhausting"
    )

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

    # Historical Rolling Baseline Check
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
        "mood": mood_input,
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

    # Summary Card
    with st.container(border=True):
        st.caption("CALCULATED BIOLOGICAL VITALITY")
        st.metric(label="Vitality Index", value=f"{calculated_vitality} / 100")
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
# SCREEN 2: BUBBLE STATUS REVIEW
# ==============================================================================
elif st.session_state.current_step == 2:
    st.title("🛡️ LifeShield State")
    st.caption("Step 2 of 3: Daily Summary Cards")

    vitality = st.session_state.daily_data["vitality"]
    savings = st.session_state.daily_data["savings"]
    weekly_burn = st.session_state.daily_data["weekly_burn"]
    runway_weeks = round(savings / weekly_burn, 1)

    financial_health_score = int(min(100, max(10, (runway_weeks / 12.0) * 100)))
    st.session_state.daily_data["financial_score"] = financial_health_score

    # Bubble 1: Biological Vitality
    with st.container(border=True):
        st.markdown("### 🔵 BIOLOGICAL VITALITY")
        st.metric(label="Current Index", value=f"{vitality} / 100")
        if vitality >= 75:
            st.success(st.session_state.daily_data["burnout_status"])
        elif vitality >= 50:
            st.warning(st.session_state.daily_data["burnout_status"])
        else:
            st.error(st.session_state.daily_data["burnout_status"])
        st.caption(f"Sleep: **{st.session_state.daily_data['sleep']}h** | HR: **{st.session_state.daily_data['heart_rate']} BPM** | Shift: **{st.session_state.daily_data['strain']}/5**")

    # Bubble 2: Financial Health
    with st.container(border=True):
        st.markdown("### 🟢 FINANCIAL HEALTH")
        st.metric(label="Health Index", value=f"{financial_health_score} / 100")
        if financial_health_score >= 70:
            st.success("SHIELDED RUNWAY")
        elif financial_health_score >= 45:
            st.warning("MODERATE BUFFER")
        else:
            st.error("VULNERABLE RUNWAY")
        st.caption(f"Buffer: **£{savings:,}** | Safe Runway: **{runway_weeks} Weeks**")

    if vitality < 55 and runway_weeks < 8:
        st.error("⚠️ COUPLED RISK ALERT: Low vitality alongside a thin financial buffer (< 8 weeks).")

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
# SCREEN 3: INTERACTIVE PLANNER & LOGGING
# ==============================================================================
elif st.session_state.current_step == 3:
    st.title("🛡️ Financial Shield & Planner")
    st.caption("Step 3 of 3: Interactive Budget & Data Management")

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
            step=25
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
    blip_col1, blip_col2 = st.columns(2)
    with blip_col1:
        vehicle_blip = st.slider("Emergency Repair / Bill (£)", 0, 2000, 0, 100)
    with blip_col2:
        unpaid_rest_weeks = st.slider("Fatigue / Unpaid Recovery (Weeks)", 0, 4, 0, 1)

    blip_savings = max(0, savings_adj - vehicle_blip - (unpaid_rest_weeks * burn_adj))
    blip_runway = round(blip_savings / burn_adj, 1)

    with st.container(border=True):
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.metric(label="Standard Safe Runway", value=f"{calc_runway} Wks")
        with col_r2:
            st.metric(label="Post-Blip Protected Runway", value=f"{blip_runway} Wks")

    st.divider()

    if st.button("💾 Lock Today's Log", use_container_width=True, type="primary"):
        today = datetime.date.today().strftime("%Y-%m-%d")
        new_row = pd.DataFrame([{
            "Date": today,
            "Mood": int(st.session_state.daily_data["mood"]),
            "HeartRate": int(st.session_state.daily_data["heart_rate"]),
            "Sleep": float(st.session_state.daily_data["sleep"]),
            "Strain": int(st.session_state.daily_data["strain"]),
            "CognitiveClarity": int(st.session_state.daily_data["cognitive_clarity"]),
            "PhysicalEase": int(st.session_state.daily_data["physical_ease"]),
            "SocialPatience": int(st.session_state.daily_data["social_patience"]),
            "FinancialCalm": int(st.session_state.daily_data["financial_calm"]),
            "Vitality": int(st.session_state.daily_data["vitality"]),
            "FinancialScore": int(st.session_state.daily_data["financial_score"]),
            "RunwayWeeks": float(calc_runway)
        }])

        if os.path.exists(DATA_FILE):
            history_df = pd.read_csv(DATA_FILE)
            history_df["Date"] = history_df["Date"].astype(str)
            history_df = history_df[history_df["Date"] != today]
            history_df = pd.concat([history_df, new_row], ignore_index=True)
        else:
            history_df = new_row
        history_df.to_csv(DATA_FILE, index=False)
        st.success(f"Check-in successfully locked for {today}!")

    st.divider()
    st.subheader("📊 History & Data Export")

    history_df = load_history()
    if not history_df.empty:
        if len(history_df) > 1:
            st.line_chart(history_df.set_index("Date")[["Vitality", "FinancialScore", "RunwayWeeks"]])

        min_date = history_df["Date"].min()
        max_date = history_df["Date"].max()

        export_range = st.date_input(
            "Select Date Range to Export",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        if isinstance
