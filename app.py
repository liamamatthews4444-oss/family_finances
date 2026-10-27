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
        background-color: #0e1117;
    }
    .metric-card {
        background-color: #1a1f29;
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        text-align: center;
    }
    .stSlider > div {
        color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ LifeShield")
st.caption("Balancing Family Financial Runway & Biological Vitality")

# --- Interactive Reactive Face & Feeling Scale ---
st.subheader("Daily Pulse Check-in")

# HTML/SVG interactive face with live morphing and subtle animation
face_html = """
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; background: #161b22; padding: 20px; border-radius: 16px; border: 1px solid #30363d; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
    <style>
        @keyframes gentleFloat {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-5px) rotate(1deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }
        .animated-face {
            animation: gentleFloat 4s ease-in-out infinite;
            filter: drop-shadow(0px 8px 16px rgba(0,0,0,0.3));
        }
    </style>
    
    <div style="font-size: 1.15rem; font-weight: 600; color: #f0f6fc; margin-bottom: 12px;">How are you feeling today?</div>
    
    <!-- Dynamic SVG Face -->
    <svg id="moodFace" class="animated-face" width="120" height="120" viewBox="0 0 100 100">
        <!-- Face Circle -->
        <circle id="faceBg" cx="50" cy="50" r="45" fill="#f59e0b" stroke="#d97706" stroke-width="3"/>
        <!-- Eyes -->
        <circle id="leftEye" cx="35" cy="40" r="4.5" fill="#1e293b"/>
        <circle id="rightEye" cx="65" cy="40" r="4.5" fill="#1e293b"/>
        <!-- Eyebrows -->
        <path id="leftBrow" d="M 28 32 Q 35 32 42 32" stroke="#1e293b" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <path id="rightBrow" d="M 58 32 Q 65 32 72 32" stroke="#1e293b" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <!-- Mouth (Morphs between frown, neutral, and smile) -->
        <path id="mouth" d="M 32 68 Q 50 68 68 68" stroke="#1e293b" stroke-width="3.5" stroke-linecap="round" fill="none"/>
    </svg>

    <div id="moodLabel" style="margin-top: 10px; font-weight: 600; color: #f59e0b; font-size: 0.95rem;">Neutral / Managing</div>
</div>

<script>
function updateFace(val) {
    const face = document.getElementById("faceBg");
    const mouth = document.getElementById("mouth");
    const leftBrow = document.getElementById("leftBrow");
    const rightBrow = document.getElementById("rightBrow");
    const label = document.getElementById("moodLabel");
    
    if (val == 1) {
        face.setAttribute("fill", "#ef4444");
        face.setAttribute("stroke", "#dc2626");
        mouth.setAttribute("d", "M 32 72 Q 50 56 68 72"); // Deep frown
        leftBrow.setAttribute("d", "M 28 35 Q 35 30 42 34");
        rightBrow.setAttribute("d", "M 58 34 Q 65 30 72 35");
        label.innerText = "Drained / Burnout Warning";
        label.style.color = "#ef4444";
    } else if (val == 2) {
        face.setAttribute("fill", "#f97316");
        face.setAttribute("stroke", "#ea580c");
        mouth.setAttribute("d", "M 34 70 Q 50 62 66 70"); // Slight frown
        leftBrow.setAttribute("d", "M 28 33 Q 35 31 42 33");
        rightBrow.setAttribute("d", "M 58 33 Q 65 31 72 33");
        label.innerText = "Low Energy / Strained";
        label.style.color = "#f97316";
    } else if (val == 3) {
        face.setAttribute("fill", "#f59e0b");
        face.setAttribute("stroke", "#d97706");
        mouth.setAttribute("d", "M 34 68 Q 50 68 66 68"); // Flat neutral
        leftBrow.setAttribute("d", "M 28 32 Q 35 32 42 32");
        rightBrow.setAttribute("d", "M 58 32 Q 65 32 72 32");
        label.innerText = "Steady / Managing Baseline";
        label.style.color = "#f59e0b";
    } else if (val == 4) {
        face.setAttribute("fill", "#84cc16");
        face.setAttribute("stroke", "#65a30d");
        mouth.setAttribute("d", "M 32 64 Q 50 72 68 64"); // Soft smile
        leftBrow.setAttribute("d", "M 28 30 Q 35 29 42 32");
        rightBrow.setAttribute("d", "M 58 32 Q 65 29 72 30");
        label.innerText = "Good / Resilient";
        label.style.color = "#84cc16";
    } else {
        face.setAttribute("fill", "#10b981");
        face.setAttribute("stroke", "#059669");
        mouth.setAttribute("d", "M 30 62 Q 50 78 70 62"); // Big grin
        leftBrow.setAttribute("d", "M 28 29 Q 35 27 42 31");
        rightBrow.setAttribute("d", "M 58 31 Q 65 27 72 29");
        label.innerText = "Optimal Vitality / Energized";
        label.style.color = "#10b981";
    }
}
</script>
"""
components.html(face_html, height=210)

# Inputs for Feeling Scale & Heart Rate
col_m1, col_m2 = st.columns([2, 1])

with col_m1:
    mood_score = st.select_slider(
        "Feeling Scale",
        options=[1, 2, 3, 4, 5],
        value=3,
        format_func=lambda x: {
            1: "1 - Exhausted",
            2: "2 - Low",
            3: "3 - Steady",
            4: "4 - Good",
            5: "5 - Energised"
        }[x]
    )

with col_m2:
    heart_rate = st.number_input(
        "Heart Rate (BPM)",
        min_value=40,
        max_value=180,
        value=68,
        step=1,
        help="Enter resting morning heart rate or post-shift reading."
    )

st.divider()

# --- Daily Sleep & Shift Work Inputs ---
st.subheader("Shift & Physical Load")
col1, col2 = st.columns(2)

with col1:
    sleep_hours = st.slider("Hours Slept", min_value=3.0, max_value=11.0, value=7.0, step=0.5)
with col2:
    shift_strain = st.slider("Work / Shift Strain (1-5)", min_value=1, max_value=5, value=3, 
                             help="1: Off/Rest, 3: Standard Shift, 5: Heavy Overtime / Physically Grueling")

# --- Biological Vitality Calculation ---
# Target baseline 7.5 hrs sleep.
sleep_debt = max(0.0, 7.5 - sleep_hours)

# Heart rate penalty: HR > 75 resting elevates physical stress multiplier
hr_penalty = max(0, (heart_rate - 75) * 0.4) if heart_rate > 75 else 0

vitality_score = int(max(5, min(100, 
    100 
    - (sleep_debt * 12) 
    - (shift_strain * 7) 
    + ((mood_score - 3) * 6) 
    - hr_penalty
)))

# Determine Vitality Status
if vitality_score >= 75:
    status_color = "#10b981"
    status_text = "Optimal & Shielded"
elif vitality_score >= 45:
    status_color = "#f59e0b"
    status_text = "Managing / Minor Strain"
else:
    status_color = "#ef4444"
    status_text = "Burnout Risk: Physical Reserve Low"

# Display Vitality Card
st.markdown(f"""
<div class="metric-card" style="border-left: 6px solid {status_color};">
    <div style="font-size: 0.9rem; color: #94a3b8;">Biological Vitality Index</div>
    <div style="font-size: 2.2rem; font-weight: 700; color: {status_color};">{vitality_score} / 100</div>
    <div style="font-size: 0.95rem; font-weight: 500; color: #e2e8f0;">{status_text}</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- Household Economic Buffer ---
st.subheader("Family Financial Runway")

col_f1, col_f2 = st.columns(2)
with col_f1:
    savings_buffer = st.number_input("Liquid Emergency Cash (£)", min_value=0, value=3500, step=250)
with col_f2:
    weekly_burn = st.number_input("Baseline Weekly Essentials (£)", min_value=100, value=450, step=25, 
                                 help="Mortgage/Rent, Food basics, Council tax, Utilities, Core transport")

runway_weeks = round(savings_buffer / weekly_burn, 1)

# Financial Runway Card
runway_color = "#10b981" if runway_weeks >= 12 else ("#f59e0b" if runway_weeks >= 6 else "#ef4444")
st.markdown(f"""
<div class="metric-card" style="border-left: 6px solid {runway_color};">
    <div style="font-size: 0.9rem; color: #94a3b8;">Safe Financial Runway</div>
    <div style="font-size: 2.2rem; font-weight: 700; color: {runway_color};">{runway_weeks} Weeks</div>
    <div style="font-size: 0.85rem; color: #94a3b8;">Time household can fully cover essentials without new income</div>
</div>
""", unsafe_allow_html=True)

# --- Shield Warning Indicator (The Link Between Body & Bank) ---
if vitality_score < 45 and runway_weeks < 8:
    st.error("⚠️ CRITICAL SHIELD ALERT: High physical fatigue combined with an emergency buffer under 8 weeks. Taking sudden unpaid sickness or missing overtime creates acute budget vulnerability.")
elif vitality_score < 45:
    st.warning("⚠️ VITALITY WARNING: Physical reserves are drained. Your cash buffer absorbs the shock, but prioritize sleep and active recovery to avoid forced time off.")

# --- Save Today's Pulse to Local History ---
st.divider()
DATA_FILE = "lifeshield_history.csv"

if st.button("💾 Save Today's Check-in to History", use_container_width=True):
    today = datetime.date.today().strftime("%Y-%m-%d")
    new_entry = pd.DataFrame([{
        "Date": today,
        "Mood": mood_score,
        "HeartRate": heart_rate,
        "Sleep": sleep_hours,
        "Strain": shift_strain,
        "Vitality": vitality_score,
        "RunwayWeeks": runway_weeks
    }])
    
    if os.path.exists(DATA_FILE):
        history_df = pd.read_csv(DATA_FILE)
        # Avoid duplicate entries for the same date
        history_df = history_df[history_df["Date"] != today]
        history_df = pd.concat([history_df, new_entry], ignore_index=True)
    else:
        history_df = new_entry
        
    history_df.to_csv(DATA_FILE, index=False)
    st.success(f"Saved check-in for {today}!")

# Display Historical Trends if available
if os.path.exists(DATA_FILE):
    st.subheader("Historical Mood & Vitality Trends")
    hist = pd.read_csv(DATA_FILE)
    if len(hist) > 1:
        st.line_chart(hist.set_index("Date")[["Vitality", "Mood", "RunwayWeeks"]])
    else:
        st.caption("Log at least 2 days to visualize correlation curves.")
