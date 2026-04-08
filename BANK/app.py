import streamlit as st
import datetime
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title=" DOVESINTHEWIND69 BANK ", page_icon="💎", layout="wide")

# --- LUXURY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Kanit:wght@200;400&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Kanit', sans-serif;
        background-color: #0f0f0f;
    }
    h1, h2, h3 {
        font-family: 'Cinzel', serif;
        color: #D4AF37 !important; /* Gold */
    }

    /* Luxury Card */
    .luxury-card {
        background: linear-gradient(145deg, #1a1a1a, #2d2d2d);
        border: 1px solid #D4AF37;
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }
    
    .gold-text { color: #D4AF37; font-weight: bold; }
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161616;
        border-right: 1px solid #D4AF37;
    }

    /* Status Items */
    .status-box {
        padding: 15px;
        border-radius: 12px;
        background: #262626;
        border-left: 4px solid #D4AF37;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'users_db' not in st.session_state:
    st.session_state.users_db = {"ozone": "282007", "vip_guest": "1234"}
if 'user_balances' not in st.session_state:
    st.session_state.user_balances = {"ozone": 500000.0, "vip_guest": 10.0}
if 'user_histories' not in st.session_state:
    st.session_state.user_histories = {"ozone": [], "vip_guest": []}
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# --- UTILITY FUNCTIONS ---
def add_history(user, type_icon, msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.user_histories[user].append({"time": now, "type": type_icon, "detail": msg})

def get_tier(balance):
    if balance >= 1000000: return "💎 PLATINUM ELITE"
    if balance >= 100000: return "🏆 GOLD MEMBER"
    return "💳 SILVER MEMBER"

# --- LOGIN / SIGNUP ---
if not st.session_state.is_logged_in:
    st.markdown("<h1 style='text-align: center;'>DOVES LUXE BANK</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #D4AF37;'>EXCLUSIVITY IN EVERY TRANSACTION</p>", unsafe_allow_html=True)
    
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        tab_log, tab_reg = st.tabs(["AUTHENTICATION", "OPEN ACCOUNT"])
        with tab_log:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("ENTER THE VAULT", use_container_width=True):
                if u in st.session_state.users_db and st.session_state.users_db[u] == p:
                    st.session_state.is_logged_in = True
                    st.session_state.current_user = u
                    st.rerun()
                else: st.error("Access Denied.")
        with tab_reg:
            nu = st.text_input("New Username")
            np = st.text_input("New Password", type="password")
            if st.button("JOIN EXCLUSIVE CLUB", use_container_width=True):
                if nu and np:
                    st.session_state.users_db[nu] = np
                    st.session_state.user_balances[nu] = 0.0
                    st.session_state.user_histories[nu] = []
                    st.success("Account Created.")

# --- MAIN APP ---
else:
    user = st.session_state.current_user
    balance = st.session_state.user_balances[user]
    tier = get_tier(balance)

    # Sidebar
    st.sidebar.markdown(f"### {tier}")
    st.sidebar.markdown(f"**Welcome, Mr./Ms. {user.capitalize()}**")
    if st.sidebar.button("LOGOUT", icon="🔒"):
        st.session_state.is_logged_in = False
        st.rerun()

    # Dashboard Header
    st.markdown(f"""
        <div class="luxury-card">
            <p style='margin:0; letter-spacing: 3px; font-size: 0.9rem;'>AVAILABLE LIQUIDITY</p>
            <h1 style='margin:10px 0; font-size: 3.5rem; color: white !important;'>฿ {balance:,.2f}</h1>
            <p style='margin:0; color: #D4AF37;'>{tier}</p>
        </div>
    """, unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["💰 TRANSFER & PAY", "📈 ANALYTICS", "📜 HISTORY", "🛠 SERVICES"])

    with t1:
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Internal Transfer")
            target_user = st.selectbox("Select Payee", [u for u in st.session_state.users_db.keys() if u != user])
            t_amount = st.number_input("Amount (฿)", min_value=0.0, step=1000.0)
            if st.button("SEND FUNDS", type="primary", use_container_width=True):
                if balance >= t_amount > 0:
                    st.session_state.user_balances[user] -= t_amount
                    st.session_state.user_balances[target_user] += t_amount
                    add_history(user, "📤", f"Transferred to {target_user}: -{t_amount:,.2f}")
                    add_history(target_user, "📥", f"Received from {user}: +{t_amount:,.2f}")
                    st.success("Transfer Completed Successfully.")
                    st.rerun()
                else: st.error("Invalid Amount or Insufficient Funds.")

        with col_b:
            st.subheader("Quick Actions")
            action = st.segmented_control("Type", ["Deposit", "Withdraw"])
            amt = st.number_input("Transaction Amount", min_value=0.0, key="quick_amt")
            if st.button("EXECUTE", use_container_width=True):
                if action == "Deposit":
                    st.session_state.user_balances[user] += amt
                    add_history(user, "💰", f"Cash Deposit: +{amt:,.2f}")
                    st.rerun()
                elif action == "Withdraw" and balance >= amt:
                    st.session_state.user_balances[user] -= amt
                    add_history(user, "💸", f"Cash Withdrawal: -{amt:,.2f}")
                    st.rerun()

    with t2:
        st.subheader("Wealth Insights")
        if not st.session_state.user_histories[user]:
            st.info("No data to analyze.")
        else:
            # จำลองกราฟการเงิน
            chart_data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'Wealth': [balance * 0.8, balance * 0.85, balance * 0.9, balance * 0.95, balance * 0.98, balance]
            })
            st.line_chart(chart_data.set_index('Month'), color="#D4AF37")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Account Status", "Active")
            c2.metric("Interest Rate", "2.5% p.a.")
            c3.metric("Limit per day", "฿ 5M")

    with t3:
        st.subheader("Statement of Records")
        for h in reversed(st.session_state.user_histories[user]):
            st.markdown(f"""
                <div class="status-box">
                    <span style='font-size: 1.2rem;'>{h['type']}</span> 
                    <span style='color: gray; font-size: 0.8rem;'>{h['time']}</span><br>
                    <b>{h['detail']}</b>
                </div>
            """, unsafe_allow_html=True)

    with t4:
        st.subheader("Premium Concierge")
        with st.expander("Update Security PIN"):
            st.text_input("Old PIN", type="password")
            st.text_input("New PIN", type="password")
            st.button("Update")
        
        if st.button("REQUEST PREMIUM CREDIT CARD", use_container_width=True):
            st.toast("Application received. Our concierge will contact you.", icon="💎")

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #444;'>ESTABLISHED 2026 | DOVESINTHEWIND69 BANK DIGITAL SYSTEM</p>", unsafe_allow_html=True)
