import streamlit as st
import datetime

# --- CONFIG ---
st.set_page_config(page_title="Doves Bank", page_icon="🏦", layout="centered")

# --- CUSTOM CSS (เพิ่มความสวยงาม) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Kanit', sans-serif;
    }
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .balance-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .history-item {
        background: white;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 8px;
        border-left: 5px solid #764ba2;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'users_db' not in st.session_state:
    st.session_state.users_db = {"ozone": "282007"}
if 'user_balances' not in st.session_state:
    st.session_state.user_balances = {"ozone": 500.0}
if 'user_histories' not in st.session_state:
    st.session_state.user_histories = {"ozone": []}
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# --- LOGIN & SIGN UP PAGE ---
if not st.session_state.is_logged_in:
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🏦 DOVES BANK</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Secure & Simple Digital Banking</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_mode = st.tabs(["🔒 Login", "📝 Sign Up"])

        # --- TAB: LOGIN ---
        with auth_mode[0]:
            with st.form("login_form"):
                user_input = st.text_input("Username")
                pass_input = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Sign In", use_container_width=True)
                
                if submit_login:
                    if user_input in st.session_state.users_db and st.session_state.users_db[user_input] == pass_input:
                        st.session_state.is_logged_in = True
                        st.session_state.current_user = user_input
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")

        # --- TAB: SIGN UP ---
        with auth_mode[1]:
            with st.form("reg_form"):
                new_user = st.text_input("Create Username")
                new_pass = st.text_input("Create Password", type="password")
                confirm_pass = st.text_input("Confirm Password", type="password")
                submit_reg = st.form_submit_button("Create Account", use_container_width=True)
                
                if submit_reg:
                    if not new_user or not new_pass:
                        st.warning("Please fill in all fields.")
                    elif new_user in st.session_state.users_db:
                        st.error("Username already taken.")
                    elif new_pass != confirm_pass:
                        st.error("Passwords do not match.")
                    else:
                        st.session_state.users_db[new_user] = new_pass
                        st.session_state.user_balances[new_user] = 0.0
                        st.session_state.user_histories[new_user] = []
                        st.success("Registration successful! Please login.")

# --- MAIN APP PAGE ---
else:
    user = st.session_state.current_user
    
    # Sidebar
    st.sidebar.markdown(f"### 👤 Profile")
    st.sidebar.info(f"**User:** {user}")
    
    if st.sidebar.button("Logout", use_container_width=True, icon="🚪"):
        st.session_state.is_logged_in = False
        st.session_state.current_user = None
        st.rerun()

    # Dashboard Header
    st.markdown(f"""
        <div class="balance-card">
            <p style='margin:0; opacity:0.8;'>Total Balance</p>
            <h1 style='margin:0; font-size: 2.5rem;'>{st.session_state.user_balances[user]:,.2f} ฿</h1>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["💸 Transactions", "📜 History", "⚙️ Account"])

    with tab1:
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("💵 Deposit")
            d_amount = st.number_input("Amount to deposit", min_value=0, step=100, key="dep")
            if st.button("Confirm Deposit", type="primary", use_container_width=True):
                if 0 < d_amount <= 5000:
                    st.session_state.user_balances[user] += d_amount
                    now = datetime.datetime.now().strftime("%d %b, %H:%M")
                    st.session_state.user_histories[user].append(f"🟢 | {now} | Deposit: +{d_amount:,.2f} ฿")
                    st.toast("Deposit Successful!", icon="💰")
                    st.rerun()
                else:
                    st.error("Limit: 1 - 5,000 ฿")

        with col_right:
            st.subheader("💳 Withdraw")
            w_amount = st.number_input("Amount to withdraw", min_value=0, step=100, key="with")
            if st.button("Confirm Withdraw", use_container_width=True):
                if w_amount > st.session_state.user_balances[user]:
                    st.error("Insufficient balance.")
                elif 0 < w_amount <= 1000:
                    st.session_state.user_balances[user] -= w_amount
                    now = datetime.datetime.now().strftime("%d %b, %H:%M")
                    st.session_state.user_histories[user].append(f"🔴 | {now} | Withdraw: -{w_amount:,.2f} ฿")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Limit: 1 - 1,000 ฿")

    with tab2:
        st.subheader("Transaction History")
        history = st.session_state.user_histories[user]
        if not history:
            st.info("No transactions found.")
        else:
            for item in reversed(history):
                st.markdown(f'<div class="history-item">{item}</div>', unsafe_allow_html=True)

    with tab3:
        st.subheader("Account Info")
        st.write(f"**Username:** {user}")
        st.write("**Account Type:** Saving Account")
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.user_histories[user] = []
            st.rerun()

    st.divider()
    st.markdown("<p style='text-align: center; color: gray; font-size: 0.8rem;'>© 2026 DOVES BANK DIGITAL SYSTEM v2.0</p>", unsafe_allow_html=True)
