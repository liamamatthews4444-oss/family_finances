import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="LifeShield", page_icon="🛡️", layout="centered")

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

if "step" not in st.session_state:
    st.session_state.step = 1

if "d" not in st.session_state:
    st.session_state.d = {
        "mood": 3, "hr": 68, "sleep": 7.0, "strain": 3,
        "clarity": 3, "ease": 3, "patience": 3, "calm": 3,
        "vit": 72, "fin": 70, "sav": 3500, "burn": 450, "inc": 2600
    }

# --- SCREEN 1: DAILY CHECK-IN ---
if st.session_state.step == 1:
    st.title("🛡️ LifeShield")
    st.caption("Step 1: Daily Biometrics & Pulse")

    with st.container(border=True):
        st.subheader("How are you feeling right now?")
        mood_opts = {1: "🔴 Burnout", 2: "🟠 Strained", 3: "🟡 Managing", 4: "🟢 Resilient", 5: "🌟 Energised"}
        m_val = st.select_slider("State", options=[1, 2, 3, 4, 5], value=st.session_state.d["mood"], format_func=lambda x: mood_opts[x])

    col1, col2 = st.columns(2)
    with col1:
        hr_val = st.number_input("Heart Rate (BPM)", min_value=40, max_value=175, value=int(st.session_state.d["hr"]), step=1)
    with col2:
        sleep_val = st.slider("Hours Slept", 3.0, 11.0, float(st.session_state.d["sleep"]), 0.5)

    strain_val = st.slider("Work / Shift Strain (1-5)", 1, 5, int(st.session_state.d["strain"]))

    st.subheader("🧠 Focus & Behavioral Signals")
    c1, c2 = st.columns(2)
    with c1:
        c_val = st.select_slider("Focus / Clarity", options=[1, 2, 3, 4, 5], value=st.session_state.d["clarity"])
        e_val = st.select_slider("Physical Comfort", options=[1, 2, 3, 4, 5], value=st.session_state.d["ease"])
    with c2:
        p_val = st.select_slider("Social Patience", options=[1, 2, 3, 4, 5], value=st.session_state.d["patience"])
        calm_val = st.select_slider("Financial Peace of Mind", options=[1, 2, 3, 4, 5], value=st.session_state.d["calm"])

    # Calculations
    debt = max(0.0, 7.5 - sleep_val)
    hr_pen = max(0.0, (hr_val - 75) * 0.4) if hr_val > 75 else 0.0
    bonus = (c_val + e_val + p_val + calm_val) - 12
    vit_calc = int(max(5, min(100, 85 - (debt * 10) - (strain_val * 6) + (bonus * 2.2) - hr_pen)))

    hist = load_history()
    avg_vit = vit_calc
    if not hist.empty and "Vitality" in hist.columns:
        recent = hist.tail(7)["Vitality"].tolist()
        avg_vit = sum(recent) / len(recent)

    if vit_calc >= 75 and avg_vit >= 70:
        status_txt = "Optimal Vitality (Strong buffer)"
    elif vit_calc < 50 or avg_vit < 55:
        status_txt = "High Burnout Risk (Fatigue accumulating)"
    else:
        status_txt = "Managing Baseline (Steady)"

    st.session_state.d.update({
        "mood": m_val, "hr": hr_val, "sleep": sleep_val, "strain": strain_val,
        "clarity": c_val, "ease": e_val, "patience": p_val, "calm": calm_val,
        "vit": vit_calc, "status": status_txt
    })

    with st.container(border=True):
        st.metric(label="Calculated Vitality Index", value=f"{vit_calc} / 100")
        if vit_calc >= 75:
            st.success(status_txt)
        elif vit_calc >= 50:
            st.warning(status_txt)
        else:
            st.error(status_txt)

    if st.button("💾 Save Check-in & Review Status →", use_container_width=True, type="primary"):
        st.session_state.step = 2
        st.rerun()

# --- SCREEN 2: BUBBLE STATUS REVIEW ---
elif st.session_state.step == 2:
    st.title("🛡️ LifeShield State")
    st.caption("Step 2: Daily Summary Cards")

    vit = st.session_state.d["vit"]
    sav = st.session_state.d["sav"]
    burn = st.session_state.d["burn"]
    runway = round(sav / burn, 1)
    fin_score = int(min(100, max(10, (runway / 12.0) * 100)))
    st.session_state.d["fin"] = fin_score

    with st.container(border=True):
        st.markdown("### 🔵 BIOLOGICAL VITALITY")
        st.metric(label="Vitality Index", value=f"{vit} / 100")
        st.info(st.session_state.d.get("status", "Managing Baseline"))
        st.caption(f"Sleep: {st.session_state.d['sleep']}h | HR: {st.session_state.d['hr']} BPM | Strain: {st.session_state.d['strain']}/5")

    with st.container(border=True):
        st.markdown("### 🟢 FINANCIAL HEALTH")
        st.metric(label="Health Index", value=f"{fin_score} / 100")
        if fin_score >= 70:
            st.success("SHIELDED RUNWAY")
        elif fin_score >= 45:
            st.warning("MODERATE BUFFER")
        else:
            st.error("VULNERABLE RUNWAY")
        st.caption(f"Buffer: £{sav:,} | Safe Runway: {runway} Weeks")

    if vit < 55 and runway < 8:
        st.error("⚠️ COUPLED RISK ALERT: Low vitality alongside a thin financial buffer.")

    b_col1, b_col2 = st.columns([1, 2])
    with b_col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with b_col2:
        if st.button("👉 Swipe to Planner →", use_container_width=True, type="primary"):
            st.session_state.step = 3
            st.rerun()

# --- SCREEN 3: INTERACTIVE PLANNER & LOGGING ---
elif st.session_state.step == 3:
    st.title("🛡️ Financial Shield & Planner")
    st.caption("Step 3: Interactive Budget & Data Management")

    f_col1, f_col2 = st.columns(2)
    with f_col1:
        s_val = st.number_input("Liquid Emergency Buffer (£)", min_value=0, value=int(st.session_state.d["sav"]), step=250)
    with f_col2:
        b_val = st.number_input("Weekly Baseline Burn (£)", min_value=100, value=int(st.session_state.d["burn"]), step=25)

    st.session_state.d["sav"] = s_val
    st.session_state.d["burn"] = b_val
    runway_calc = round(s_val / b_val, 1)

    st.divider()
    st.subheader("⚡ Future Blip Simulator")
    sim1, sim2 = st.columns(2)
    with sim1:
        v_blip = st.slider("Emergency Repair / Bill (£)", 0, 2000, 0, 100)
    with sim2:
        rest_wks = st.slider("Fatigue / Unpaid Recovery (
