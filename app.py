import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sqlite3
from datetime import datetime, date

# ---------------------------------------------------------
# PAGE CONFIGURATION (Optimized for Mobile)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Family Wealth & Trajectory",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Mobile CSS styling
st.markdown("""
<style>
    .metric-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 48px;
        font-weight: 600;
    }
    .badge-paid {
        background-color: #DCFCE7;
        color: #166534;
        padding: 3px 8px;
        border-radius: 5px;
        font-size: 12px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATABASE SETUP (Local SQLite for quick logging & sinking funds)
# ---------------------------------------------------------
DB_FILE = "family_finances.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            amount REAL,
            category TEXT,
            person TEXT,
            note TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS sinking_funds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fund_name TEXT UNIQUE,
            current_balance REAL,
            target_buffer REAL
        )
    """)
    # Seed default sinking funds if empty
    default_funds = [
        ("VW Golf Maintenance", 150.0, 500.0),
        ("Kia Ceed Servicing", 200.0, 500.0),
        ("Camper & Holiday", 350.0, 1200.0),
        ("Home & Garden Emergency", 250.0, 800.0)
    ]
    for name, bal, tgt in default_funds:
        c.execute("INSERT OR IGNORE INTO sinking_funds (fund_name, current_balance, target_buffer) VALUES (?, ?, ?)", (name, bal, tgt))
    conn.commit()
    conn.close()

init_db()

def log_expense(amount, category, person, note):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO transactions (timestamp, amount, category, person, note) VALUES (?, ?, ?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M"), amount, category, person, note))
    conn.commit()
    conn.close()

def get_recent_expenses(limit=10):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(f"SELECT timestamp, person, category, amount, note FROM transactions ORDER BY id DESC LIMIT {limit}", conn)
    conn.close()
    return df

def get_sinking_funds():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT fund_name, current_balance, target_buffer FROM sinking_funds", conn)
    conn.close()
    return df

def update_sinking_fund(fund_name, new_bal):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE sinking_funds SET current_balance = ? WHERE fund_name = ?", (new_bal, fund_name))
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# NAVIGATION (Mobile Tabs)
# ---------------------------------------------------------
tab_quick_log, tab_simulator, tab_sinking, tab_budget = st.tabs([
    "⚡ Quick Log", 
    "📈 4-Yr Trajectory", 
    "🛡️ Sinking Pots", 
    "📋 Fixed Budget"
])

# ---------------------------------------------------------
# TAB 1: QUICK LOG (Fast phone entry for daily cash drag)
# ---------------------------------------------------------
with tab_quick_log:
    st.subheader("⚡ Quick Log Expense")
    st.caption("Track daily flexible outgoings in under 5 seconds.")

    with st.form("quick_log_form", clear_on_submit=True):
        col_amt, col_cat = st.columns([1, 1])
        with col_amt:
            amount = st.number_input("Amount (£)", min_value=0.01, step=1.00, format="%.2f")
        with col_cat:
            category = st.selectbox("Category", [
                "Groceries / Food Top-up",
                "Fuel / Commuting",
                "Vape / Personal",
                "Kids & School",
                "Car Maintenance / Spares",
                "DIY / Hardware",
                "Eating Out / Takeaway",
                "Other Discretionary"
            ])
        
        col_who, col_note = st.columns([1, 1])
        with col_who:
            person = st.selectbox("Logged By", ["Liam", "Lucy"])
        with col_note:
            note = st.text_input("Note (Optional)", placeholder="e.g. Morrisons, wiper blades, school book")

        submit = st.form_submit_button("Record Expense", use_container_width=True)
        if submit:
            if amount > 0:
                log_expense(amount, category, person, note)
                st.success(f"Logged £{amount:.2f} under {category}!")
            else:
                st.error("Please enter a valid amount.")

    st.markdown("---")
    st.subheader("🕒 Recent Logs")
    recent_df = get_recent_expenses(8)
    if not recent_df.empty:
        for _, row in recent_df.iterrows():
            st.markdown(
                f"**£{row['amount']:.2f}** — `{row['category']}` &nbsp;|&nbsp; *{row['person']}* &nbsp;|&nbsp; <small style='color:grey'>{row['timestamp']}</small> {f'— <i>{row["note"]}</i>' if row['note'] else ''}",
                unsafe_allow_html=True
            )
    else:
        st.info("No discretionary transactions logged yet. Add your first one above!")

# ---------------------------------------------------------
# TAB 2: 4-YEAR TRAJECTORY SIMULATOR (Dynamic Behavior Sliders)
# ---------------------------------------------------------
with tab_simulator:
    st.subheader("📈 Interactive 4-Year Trajectory")
    st.caption("Adjust your real-world behavioural levers to see how your net balance compounds through 2030.")

    with st.expander("⚙️ Adjust Behavioural Levers", expanded=True):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            starting_net = st.number_input("Starting Position (£)", value=-8000.0, step=250.0, format="%.0f")
            overtime_shifts = st.slider("Extra Shift / Overtime Capacity (£/mo)", 0, 800, 200, step=50,
                                       help="Additional HGV runs or weekend work")
            discretionary_spend = st.slider("Discretionary / Spending Drag (£/mo)", 50, 600, 180, step=25,
                                           help="Target for untracked casual spending (vapes, snacks, tools)")
        with col_s2:
            sinking_allowance = st.slider("Annual Sinking Buffer (£/yr)", 0, 2400, 1000, step=100,
                                         help="Pre-funded buffer to absorb car repairs, camper costs, and holidays smoothly")
            growth_rate = st.slider("Surplus Cash Yield (% p.a.)", 1.0, 7.0, 4.0, step=0.5,
                                   help="Interest rate once total balance moves above £0")
            debt_repayment = st.number_input("Active Debt Payment (£/mo)", value=230.0, step=25.0,
                                             help="Virgin Money CC (£200) + HMRC (£30)")

    # 48-Month Dynamic Calculation
    months = 48
    base_net_income = 1757.00 + 170.20  # £1,927.20
    fixed_bills = 1151.54               # Rent, council tax, energy, 2 cars, subs
    family_essentials = 375.45          # Food, school meals, haircuts, uniforms
    
    # 3 Scenario Simulations:
    # 1. User Customized (from sliders)
    # 2. Aggressive Snowball (£450 extra, £80 drag, £1200 buffer)
    # 3. Status Quo / Drift (£0 extra, £450 drag, £0 buffer)

    def run_projection(extra_inc, disc_spend, annual_shock, starting_bal, yield_pct, debt_pay):
        balance = starting_bal
        history = [balance]
        monthly_shock = annual_shock / 12.0
        
        for m in range(1, months + 1):
            cur_income = base_net_income + extra_inc
            # Debt phase logic: months 1-18 active, then clears and rolls into surplus
            cur_debt = debt_pay if m <= 18 else 0.0
            total_outgoings = fixed_bills + family_essentials + disc_spend + cur_debt + monthly_shock
            surplus = cur_income - total_outgoings
            
            # Compound interest on positive balance
            interest = (balance * (yield_pct / 100.0 / 12.0)) if balance > 0 else 0.0
            balance += (surplus + interest)
            history.append(balance)
        return history

    proj_custom = run_projection(overtime_shifts, discretionary_spend, sinking_allowance, starting_net, growth_rate, debt_repayment)
    proj_aggressive = run_projection(450, 80, 1200, starting_net, 4.5, 305)
    proj_drift = run_projection(0, 450, 0, starting_net, 1.0, 230)

    # Key Milestone Metrics
    def get_parity_month(traj):
        for idx, val in enumerate(traj):
            if val >= 0:
                return idx
        return None

    p_custom = get_parity_month(proj_custom)
    parity_str = f"Month {p_custom} ({['Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct'][(p_custom-1)%12]} {2026 + (p_custom+9)//12})" if p_custom else "Beyond 48m"

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("£0 Debt Parity Milestone", parity_str)
    with col_m2:
        st.metric("Year 2 Balance (Oct 2028)", f"£{proj_custom[24]:,.0f}", delta=f"{proj_custom[24]-starting_net:+,.0f}")
    with col_m3:
        st.metric("Year 4 Balance (Oct 2030)", f"£{proj_custom[48]:,.0f}", delta=f"{proj_custom[48]-starting_net:+,.0f}")

    # Plotly Visual Curve
    dates = pd.date_range(start="2026-10-01", periods=49, freq="MS")
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates, y=proj_custom,
        mode="lines",
        name="Your Dynamic Plan",
        line=dict(color="#0D9488", width=4)
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=proj_aggressive,
        mode="lines",
        name="Aggressive Snowball",
        line=dict(color="#059669", width=2, dash="dot")
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=proj_drift,
        mode="lines",
        name="Unbuffered Drift",
        line=dict(color="#EF4444", width=2, dash="dash")
    ))

    # Zero Line
    fig.add_hline(y=0, line_dash="solid", line_color="#94A3B8", annotation_text="£0 Parity (Debt Free)", annotation_position="top left")

    fig.update_layout(
        title="Projected Net Trajectory (48 Months)",
        margin=dict(l=10, r=10, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title="",
        yaxis_title="Net Worth (£)",
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: SINKING FUNDS & CAR POTS (Preventing the Dips)
# ---------------------------------------------------------
with tab_sinking:
    st.subheader("🛡️ Virtual Sinking Pots")
    st.caption("Prevent sudden £500-£1,000 drops on your chart by building dedicated buffers.")

    funds_df = get_sinking_funds()
    for _, f in funds_df.iterrows():
        pct = min(1.0, max(0.0, f["current_balance"] / f["target_buffer"]))
        st.write(f"**{f['fund_name']}** — £{f['current_balance']:.0f} / £{f['target_buffer']:.0f} ({pct*100:.0f}%)")
        st.progress(pct)
        with st.expander(f"Update {f['fund_name']} Balance"):
            new_val = st.number_input(f"New Balance for {f['fund_name']}", value=float(f["current_balance"]), step=20.0, key=f["fund_name"])
            if st.button(f"Save {f['fund_name']}", key=f"btn_{f['fund_name']}"):
                update_sinking_fund(f["fund_name"], new_val)
                st.rerun()

# ---------------------------------------------------------
# TAB 4: FIXED BUDGET BREAKDOWN
# ---------------------------------------------------------
with tab_budget:
    st.subheader("📋 Core Household Budget Baseline")
    st.caption("Synchronised with your active October 2026 finances.")

    b_col1, b_col2 = st.columns(2)
    with b_col1:
        st.markdown("""
        **Fixed Outgoings (£1,151.54/mo):**
        - Rent: £495.37
        - Council Tax: £139.15
        - Octopus Electricity: £130.00
        - Water: £52.85
        - TV Licence: £15.00
        - Broadband: £20.00
        - Hometree: £20.91
        - Building Insurance: £23.54
        - VW Golf Mk6 (Tax & Ins): £43.39
        - Kia Cee'd (Tax & Ins): £60.28
        - Fuel: £100.00
        - Life & Income Ins: £51.05
        - Subscriptions (Phones, Disney+, Google, etc.): £81.01
        """)
    with b_col2:
        st.markdown("""
        **Flexible & Family Outgoings (£375.45/mo):**
        - Groceries Baseline: £133.20
        - School Dinners: £48.00
        - School Uniforms: £15.00
        - Kids Haircuts: £15.00
        - Toiletries & Vapes: £25.00
        - Birthdays / Kids Fund: £40.00
        - Passports Fund: £18.25
        
        **Active Debt Repayments (£230.00/mo):**
        - Virgin Money 0% CC: £200.00 *(Clears by ~Month 18)*
        - HMRC: £30.00
        """)
