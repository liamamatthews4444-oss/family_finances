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
        font-size: 2.8rem;
        font-weight: 800;
    }

    /* Throbbing Red Alert Animation */
    @keyframes throbPulseRed {
        0% {
            box-shadow: 0 0 14px rgba(239, 68, 68, 0.4), inset 0 0 10px rgba(239, 68, 68, 0.2);
            border-color: rgba(239, 68, 68, 0.6);
        }
        50% {
            box-shadow: 0 0 35px rgba(239, 68, 68, 0.85), inset 0 0 20px rgba(239, 68, 68, 0.45);
            border-color: rgba(239, 68, 68, 1);
            transform: scale(1.01);
        }
        100% {
            box-shadow: 0 0 14px rgba(239, 68, 68, 0.4), inset 0 0 10px rgba(239, 68, 68, 0.2);
            border-color: rgba(239, 68, 68, 0.6);
        }
    }

    /* Gentle Green Resilient Glow Animation */
    @keyframes steadyGlowGreen {
        0% {
            box-shadow: 0 0 16px rgba(16, 185, 129, 0.35), inset 0 0 8px rgba(16, 185, 129, 0.15);
        }
        50% {
            box-shadow: 0 0 30px rgba(16, 185, 129, 0.7), inset 0 0 16px rgba(16, 185, 129, 0.3);
        }
        100% {
            box-shadow: 0 0 16px rgba(16, 185, 129, 0.35), inset 0 0 8px rgba(16, 185, 129, 0.15);
        }
    }

    /* Ambient Amber Glow Animation */
    @keyframes steadyGlowAmber {
        0% {
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.3), inset 0 0 8px rgba(245, 158, 11, 0.15);
        }
        50% {
            box-shadow: 0 0 26px rgba(245, 158, 11, 0.6), inset 0 0 14px rgba(245, 158, 11, 0.25);
        }
        100% {
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.3), inset 0 0 8px rgba(245, 158, 11, 0.15);
        }
    }

    .vitality-glow-box {
        border-radius: 20px;
        padding: 24px;
        margin: 22px 0;
        text-align: center;
        transition: all 0.4s ease-in-out;
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

# --- Live Google Sheet Connection ---
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTpkmYNnZU1yZr__I9f0UwDbJxG7Hr68Kt7X4IfzO1FYRT4LjcxIVtI68ewN6E0sQfx711PSk8fJVlB/pub?gid=184144388&single=true&output=csv"

@st.cache_data(ttl=300)
def load_live_sheet_data():
    try:
        df_hist = pd.read_csv(SHEET_CSV_URL, header=None, usecols=[0, 1])
        df_hist.columns = ["Date_Raw", "Bal_Raw"]
        df_hist["Date"] = pd.to_datetime(df_hist["Date_Raw"], format="%d/%m/%Y", errors="coerce")
        clean_bal = df_hist["Bal_Raw"].astype(str).str.replace(",", "", regex=False).str.replace("£", "", regex=False).str.strip()
        df_hist["Balance"] = pd.to_numeric(clean_bal, errors="coerce")
        df_hist = df_hist.dropna(subset=["Date", "Balance"]).sort_values("Date")
        df_hist["Debt Remaining (£)"] = df_hist["Balance"].apply(lambda x: abs(x) if x < 0 else 0)
        df_hist["Stored Cash (£)"] = df_hist["Balance"].apply(lambda x: x if x > 0 else 0)
        chart_df = df_hist.set_index("Date")[["Debt Remaining (£)", "Stored Cash (£)"]]

        df_full = pd.read_csv(SHEET_CSV_URL, header=None)
       sav = pd.to_numeric(str(df_full.iloc[46, 6]).replace(",", "").replace("£", "").strip(), errors="coerce")
        inv = pd.to_numeric(str(df_full.iloc[47, 6]).replace(",", "").replace("£", "").strip(), errors="coerce")
        sav_val = float(sav) if pd.notnull(sav) else 1287.0
        inv_val = float(inv) if pd.notnull(inv) else 127.33
        reserves = round(sav_val + inv_val, 2)
        return chart_df, sav_val, inv_val, reserves
    except Exception:
        return pd.DataFrame(), 1287.0, 127.33, 1414.33

live_chart_data, sheet_savings, sheet_investments, sheet_total_reserves = load_live_sheet_data()

# --- Session State ---
if "current_step" not in st.session_state:
    st.session_state.current_step = 1

if "daily_data" not in st.session_state:
    st.session_state.daily_data = {
if st.session_state.daily_data.get("savings") == 3500:
    st.session_state.daily_data["savings"] = float(sheet_total_reserves)
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
        "savings": float(sheet_total_reserves),
        "monthly_nut": 1850
    }

# ==============================================================================
# SCREEN 1: REAL-SKY MOOD FACE & ADAPTIVE CHECK-IN
# ==============================================================================
if st.session_state.current_step == 1:
    st.title("🛡️ LifeShield")
    st.caption("Daily Biometrics & Adaptive Health Pulse")

    # Load Face Component from separate face.html file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    face_path = os.path.join(script_dir, "face.html")

    if os.path.exists(face_path):
        with open(face_path, "r", encoding="utf-8") as f:
            components.html(f.read(), height=310)
    elif os.path.exists("face.html"):
        with open("face.html", "r", encoding="utf-8") as f:
            components.html(f.read(), height=310)
    else:
        st.warning("⚠️ face.html not found. Make sure face.html is uploaded in your repository root.")

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

    # Dynamic Vitality Calculation
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

   # Dynamic Blended Gradient & Animation styling based on state
    if calculated_vitality >= 75:
        # Green steady, energised glow
        card_style = """
            background: linear-gradient(145deg, #062e24 0%, #0b1716 100%);
            border: 2px solid #10b981;
            animation: steadyGlowGreen 3.5s ease-in-out infinite;
        """
        score_color = "#34d399"
        status_color = "#6ee7b7"
    elif calculated_vitality < 50 or rolling_vitality_avg < 55:
        # Blended Red throbbing warning pulse
        card_style = """
            background: linear-gradient(145deg, #3b0d0c 0%, #170707 100%);
            border: 2px solid #ef4444;
            animation: throbPulseRed 1.8s ease-in-out infinite;
        """
        score_color = "#f87171"
        status_color = "#fca5a5"
    else:
        # Amber/Orange baseline gentle glow
        card_style = """
            background: linear-gradient(145deg, #33200a 0%, #13100a 100%);
            border: 2px solid #f59e0b;
            animation: steadyGlowAmber 3.2s ease-in-out infinite;
        """
        score_color = "#fbbf24"
        status_color = "#fcd34d"

    vitality_card_html = f"""
    <div class="vitality-glow-box" style="{card_style}">
        <div style="font-size: 0.85rem; letter-spacing: 0.08em; text-transform: uppercase; color: #94a3b8; font-weight: 700; margin-bottom: 6px;">
            CALCULATED BIOLOGICAL VITALITY
        </div>
        <div style="font-size: 3.4rem; font-weight: 800; color: {score_color}; line-height: 1.1; margin-bottom: 10px;">
            {calculated_vitality} <span style="font-size: 1.4rem; font-weight: 600; color: #94a3b8;">/ 100</span>
        </div>
        <div style="font-size: 1.05rem; font-weight: 700; color: {status_color};">
            {burnout_status}
        </div>
    </div>
    """
    st.markdown(vitality_card_html, unsafe_allow_html=True)

    if st.button("💾 Save Check-in & Review Status →", use_container_width=True, type="primary"):
        st.session_state.current_step = 2
        st.rerun()

# ==============================================================================
# SCREEN 2: BUBBLE STATUS CARDS
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

    # Runway Display
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

    # 4-Year Debt-to-0 & Wealth Trajectory Curve
    st.subheader("📈 4-Year Debt-to-0 & Wealth Curve")
    st.caption("Structural journey from historical debt into positive reserves.")

    if not live_chart_data.empty:
        st.line_chart(live_chart_data)
    else:
        st.info("Fetching live spreadsheet curve...")

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
            st.metric("Standard Runway", f"{calc_runway} Wks")
        with r2:
            st.metric("Post-Blip Runway", f"{blip_runway} Wks")

    st.divider()

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
