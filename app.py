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

    # Load Face Component from separate file
    if os.path.exists("face.html"):
        with open("face.html", "r", encoding="utf-8") as f:
            components.html(f.read(), height=310)

    # Biometrics Row
    col_hr, col_sleep = st.columns(2)
    with col_hr:
        hr_input = st.number_input(
            "Heart Rate (BPM)",
            min_value=40,
            max_value=175,
            value=int(st.session_state.daily_data["heart_rate"]),
            step=1,
            help="Resting morning HR or post-shift reading."
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
        help="1: Off/Rest Day, 3: Standard Shift, 5: Heavy Overtime / Physically Exhausting"
    )

    st.divider()

    # Behavioral Signals (Left = Negative, Right = Positive)
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
    hr_penalty = max(0.0, (hr_input - 75) * 0.4) if hr_input > 75 else 0.0
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

    summary_box = (
        '<div style="background-color: #131b2e; border-left: 6px solid ' + status_color + '; border-radius: 14px; padding: 16px; margin: 20px 0; text-align: center;">'
        '<div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Calculated Biological Vitality</div>'
        '<div style="font-size: 2.2rem; font-weight: 800; color: ' + status_color + ';">' + str(calculated_vitality) + ' / 100</div>'
        '<div style="font-size: 0.88rem; color: ' + status_color + '; font-weight: 600; margin-top: 4px;">' + burnout_status + '</div>'
        '</div>'
    )
    st.markdown(summary_box, unsafe_allow_html=True)

    if st.button("💾 Save Check-in & Review Status →", use_container_width=True, type="primary"):
        st.session_state.current_step = 2
        st.rerun()

# ==============================================================================
# SCREEN 2: BUBBLE STATUS CARDS (AUTO SCROLL TO TOP)
# ==============================================================================
elif st.session_state.current_step == 2:
    components.html("<script>window.parent.scrollTo(0, 0);</script>", height=0)

    st.title("🛡️ LifeShield State")
    st.caption("Step 2 of 3: Daily Summary Cards")

    vitality = st.session_state.daily_data["vitality"]
    savings = st.session_state.daily_data["savings"]
    weekly_burn = st.session_state.daily_data["weekly_burn"]
    runway_weeks = round(savings / weekly_burn, 1)

    financial_health_score = int(min(100, max(10, (runway_weeks / 12.0) * 100)))
    st.session_state.daily_data["financial_score"] = financial_health_score

    v_color = "#10b981" if vitality >= 75 else ("#f59e0b" if vitality >= 50 else "#ef4444")
    f_color = "#10b981" if financial_health_score >= 70 else ("#f59e0b" if financial_health_score >= 45 else "#ef4444")
    f_badge = "SHIELDED RUNWAY" if financial_health_score >= 70 else ("MODERATE BUFFER" if financial_health_score >= 45 else "VULNERABLE RUNWAY")

    b1_html = (
        '<div class="bubble-card" style="border-color: ' + v_color + ';">'
        '<div class="swipe-pill" style="color: #38bdf8; border-color: #0284c7;">BIOLOGICAL VITALITY</div>'
        '<div style="font-size: 3.8rem; font-weight: 800; color: ' + v_color + '; margin: 8px 0;">' + str(vitality) + '<span style="font-size: 1.5rem; color: #8b949e;">/100</span></div>'
        '<div style="color: ' + v_color + '; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">' + str(st.session_state.daily_data['burnout_status']) + '</div>'
        '<div style="margin-top: 14px; color: #cbd5e1; font-size: 0.92rem;">'
        'Sleep: <b>' + str(st.session_state.daily_data['sleep']) + 'h</b> | HR: <b>' + str(st.session_state.daily_data['heart_rate']) + ' BPM</b> | Shift Load: <b>' + str(st.session_state.daily_data['strain']) + '/5</b>'
        '</div></div>'
    )
    st.markdown(b1_html, unsafe_allow_html=True)

    b2_html = (
        '<div class="bubble-card" style="border-color: ' + f_color + ';">'
        '<div class="swipe-pill" style="color: #4ade80; border-color: #166534;">FINANCIAL HEALTH</div>'
        '<div style="font-size: 3.8rem; font-weight: 800; color: ' + f_color + '; margin: 8px 0;">' + str(financial_health_score) + '<span style="font-size: 1.5rem; color: #8b949e;">/100</span></div>'
        '<div style="background-color: ' + f_color + '22; color: ' + f_color + '; display: inline-block; padding: 6px 14px; border-radius: 12px; font-weight: 700; font-size: 0.9rem;">' + f_badge + '</div>'
        '<div style="margin-top: 14px; color: #cbd5e1; font-size: 0.95rem;">'
        'Liquid Buffer: <b>£' + f"{savings:,}" + '</b> | Safe Runway: <b>' + str(runway_weeks) + ' Weeks</b>'
        '</div></div>'
    )
    st.markdown(b2_html, unsafe_allow_html=True)

    if vitality < 55 and runway_weeks < 8:
        st.error("⚠️ COUPLED RISK ALERT: Persistent low vitality alongside a thin financial buffer (< 8 weeks). Physical downtime risks acute financial friction.")

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
# SCREEN 3: INTERACTIVE PLANNER, BLIP SIMULATOR & EXPORT
# ==============================================================================
elif st.session_state.current_step == 3:
    components.html("<script>window.parent.scrollTo(0, 0);</script>", height=0)

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
    blip_color = "#10b981" if blip_runway >= 8 else "#ef4444"

    sim_box = (
        '<div style="background-color: #131b2e; border: 1px solid #233554; border-radius: 16px; padding: 18px; margin-top: 10px;">'
        '<div style="display: flex; justify-content: space-between; align-items: center;">'
        '<span style="color: #94a3b8;">Standard Safe Runway:</span>'
        '<span style="font-weight: 700; color: #38bdf8;">' + str(calc_runway) + ' Weeks</span>'
        '</div>'
        '<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">'
        '<span style="color: #94a3b8;">Post-Blip Protected Runway:</span>'
        '<span style="font-weight: 700; color: ' + blip_color + ';">' + str(blip_runway) + ' Weeks</span>'
        '</div></div>'
    )
    st.markdown(sim_box, unsafe_allow_html=True)

    st.divider()

    # Save to Local CSV
    if st.button("💾 Lock Today's Log", use_container_width=True, type="primary"):
        today = datetime.date.today().strftime("%Y-%m-%d")
        new_row = pd.DataFrame([{
            "Date": today,
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
        st.success(f"Check-in locked for {today}!")

    # Historical Trends & Export
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

        if isinstance(export_range, tuple) and len(export_range) == 2:
            start_d, end_d = export_range
            filtered_df = history_df[(history_df["Date"] >= start_d) & (history_df["Date"] <= end_d)]
            csv_data = filtered_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label=f"📥 Download CSV ({start_d} to {end_d})",
                data=csv_data,
                file_name=f"lifeshield_data_{start_d}_{end_d}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.caption("No history entries recorded yet.")

    if st.button("← Return to Daily Pulse", use_container_width=True):
        st.session_state.current_step = 1
        st.rerun()
