import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="LifeShield", page_icon="🛡️")

DATA_FILE = "lifeshield_history.csv"

def load_data():
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
        "vit": 72, "fin": 70, "sav": 3500, "burn": 450
    }

# --- PAGE 1: DAILY INPUTS ---
if st.session_state.step == 1:
    st.title("🛡️ LifeShield")
    st.subheader("Daily Biometrics & Pulse")

    with st.container(border=True):
        m_opts = {1: "🔴 Burnout", 2: "🟠 Strained", 3: "🟡 Managing", 4: "🟢 Resilient", 5: "🌟 Energised"}
        m_val = st.select_slider("How do you feel?", options=[1, 2, 3, 4, 5], value=st.session_state.d["mood"], format_func=lambda x: m_opts[x])

    col1, col2 = st.columns(2)
    with col1:
        hr_val = st.number_input("Heart Rate BPM", 40, 180, int(st.session_state.d["hr"]), 1)
    with col2:
        sleep_val = st.slider("Sleep Hours", 3.0, 11.0, float(st.session_state.d["sleep"]), 0.5)

    strain_val = st.slider("Shift Strain (1-5)", 1, 5, int(st.session_state.d["strain"]))

    st.subheader("Behavioral Signals")
    c1, c2 = st.columns(2)
    with c1:
        c_val = st.select_slider("Clarity", [1, 2, 3, 4, 5], st.session_state.d["clarity"])
        e_val = st.select_slider("Physical Ease", [1, 2, 3, 4, 5], st.session_state.d["ease"])
    with c2:
        p_val = st.select_slider("Patience", [1, 2, 3, 4, 5], st.session_state.d["patience"])
        calm_val = st.select_slider("Financial Calm", [1, 2, 3, 4, 5], st.session_state.d["calm"])

    debt = max(0.0, 7.5 - sleep_val)
    hr_pen = max(0.0, (hr_val - 75) * 0.4) if hr_val > 75 else 0.0
    bonus = (c_val + e_val + p_val + calm_val) - 12
    vit_calc = int(max(5, min(100, 85 - (debt * 10) - (strain_val * 6) + (bonus * 2.2) - hr_pen)))

    hist = load_data()
    avg_vit = vit_calc
    if not hist.empty and "Vitality" in hist.columns:
        recent = hist.tail(7)["Vitality"].tolist()
        avg_vit = sum(recent) / len(recent)

    if vit_calc >= 75 and avg_vit >= 70:
        status_txt = "Optimal Vitality (Strong buffer)"
    elif vit_calc < 50 or avg_vit < 55:
        status_txt = "High Burnout Risk (Fatigue accumulation)"
    else:
        status_txt = "Managing Baseline (Steady)"

    st.session_state.d.update({
        "mood": m_val, "hr": hr_val, "sleep": sleep_val, "strain": strain_val,
        "clarity": c_val, "ease": e_val, "patience": p_val, "calm": calm_val,
        "vit": vit_calc, "status": status_txt
    })

    with st.container(border=True):
        st.metric("Vitality Index", f"{vit_calc} / 100")
        if vit_calc >= 75:
            st.success(status_txt)
        elif vit_calc >= 50:
            st.warning(status_txt)
        else:
            st.error(status_txt)

    if st.button("Save & Review Status →", use_container_width=True, type="primary"):
        st.session_state.step = 2
        st.rerun()

# --- PAGE 2: SUMMARY BUBBLES ---
elif st.session_state.step == 2:
    st.title("🛡️ LifeShield State")

    vit = st.session_state.d["vit"]
    sav = st.session_state.d["sav"]
    burn = st.session_state.d["burn"]
    runway = round(sav / burn, 1)
    fin_score = int(min(100, max(10, (runway / 12.0) * 100)))
    st.session_state.d["fin"] = fin_score

    with st.container(border=True):
        st.markdown("### 🔵 BIOLOGICAL VITALITY")
        st.metric("Vitality", f"{vit} / 100")
        st.info(st.session_state.d.get("status", "Steady"))
        st.caption(f"Sleep: {st.session_state.d['sleep']}h | HR: {st.session_state.d['hr']} BPM | Strain: {st.session_state.d['strain']}/5")

    with st.container(border=True):
        st.markdown("### 🟢 FINANCIAL HEALTH")
        st.metric("Financial Score", f"{fin_score} / 100")
        if fin_score >= 70:
            st.success("SHIELDED RUNWAY")
        elif fin_score >= 45:
            st.warning("MODERATE BUFFER")
        else:
            st.error("VULNERABLE RUNWAY")
        st.caption(f"Savings: £{sav:,} | Runway: {runway} Weeks")

    if vit < 55 and runway < 8:
        st.error("⚠️ COUPLED RISK: Low vitality with thin savings runway.")

    b1, b2 = st.columns([1, 2])
    with b1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with b2:
        if st.button("Planner →", use_container_width=True, type="primary"):
            st.session_state.step = 3
            st.rerun()

# --- PAGE 3: PLANNER & DATA ---
elif st.session_state.step == 3:
    st.title("🛡️ Financial Planner")

    f1, f2 = st.columns(2)
    with f1:
        s_val = st.number_input("Liquid Savings (£)", 0, value=int(st.session_state.d["sav"]), step=250)
    with f2:
        b_val = st.number_input("Weekly Outgoings (£)", 100, value=int(st.session_state.d["burn"]), step=25)

    st.session_state.d["sav"] = s_val
    st.session_state.d["burn"] = b_val
    runway_calc = round(s_val / b_val, 1)

    st.subheader("⚡ Emergency Blip Test")
    v_blip = st.slider("Unexpected Expense (£)", 0, 2000, 0, 100)
    rest_wks = st.slider("Unpaid Leave (Weeks)", 0, 4, 0, 1)

    post_sav = max(0, s_val - v_blip - (rest_wks * b_val))
    post_runway = round(post_sav / b_val, 1)

    with st.container(border=True):
        rc1, rc2 = st.columns(2)
        with rc1:
            st.metric("Standard Runway", f"{runway_calc} Wks")
        with rc2:
            st.metric("Post-Blip Runway", f"{post_runway} Wks")

    if st.button("💾 Lock Log Entry", use_container_width=True, type="primary"):
        today = datetime.date.today().strftime("%Y-%m-%d")
        row = pd.DataFrame([{
            "Date": today, "Mood": int(st.session_state.d["mood"]),
            "HeartRate": int(st.session_state.d["hr"]), "Sleep": float(st.session_state.d["sleep"]),
            "Strain": int(st.session_state.d["strain"]), "Clarity": int(st.session_state.d["clarity"]),
            "Ease": int(st.session_state.d["ease"]), "Patience": int(st.session_state.d["patience"]),
            "Calm": int(st.session_state.d["calm"]), "Vitality": int(st.session_state.d["vit"]),
            "FinScore": int(st.session_state.d["fin"]), "Runway": float(runway_calc)
        }])

        if os.path.exists(DATA_FILE):
            h_df = pd.read_csv(DATA_FILE)
            h_df["Date"] = h_df["Date"].astype(str)
            h_df = h_df[h_df["Date"] != today]
            h_df = pd.concat([h_df, row], ignore_index=True)
        else:
            h_df = row
        h_df.to_csv(DATA_FILE, index=False)
        st.success(f"Saved for {today}!")

    st.divider()
    hist_df = load_data()
    if not hist_df.empty:
        if len(hist_df) > 1:
            st.line_chart(hist_df.set_index("Date")[["Vitality", "FinScore", "Runway"]])
        csv_bytes = hist_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv_bytes, "lifeshield_history.csv", "text/csv", use_container_width=True)

    if st.button("← Back to Start", use_container_width=True):
        st.session_state.step = 1
        st.rerun()
