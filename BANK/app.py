import streamlit as st
import datetime

# --- CONFIG ---
st.set_page_config(page_title="Dovesinthewind69 Bank", page_icon="🏦", layout="centered")

# --- SESSION STATE INITIALIZATION ---
# เก็บข้อมูลผู้ใช้หลายคนใน Dictionary {username: password}
if 'users_db' not in st.session_state:
    st.session_state.users_db = {"ozone": "282007"}  # บัญชีเริ่มต้น

# เก็บยอดเงินแยกตาม User {username: balance}
if 'user_balances' not in st.session_state:
    st.session_state.user_balances = {"ozone": 500.0}

# เก็บประวัติแยกตาม User {username: [history_list]}
if 'user_histories' not in st.session_state:
    st.session_state.user_histories = {"ozone": []}

if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# --- LOGIN & SIGN UP PAGE ---
if not st.session_state.is_logged_in:
    st.markdown("<h1 style='text-align: center;'>🔐 DOVESINTHEWIND69 BANK</h1>", unsafe_allow_html=True)
    
    auth_mode = st.tabs(["Login", "Sign up"])

    # --- TAB: LOGIN ---
    with auth_mode[0]:
        with st.container(border=True):
            user_input = st.text_input("Username", key="login_user")
            pass_input = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Sign In", use_container_width=True, type="primary"):
                if user_input in st.session_state.users_db and st.session_state.users_db[user_input] == pass_input:
                    st.session_state.is_logged_in = True
                    st.session_state.current_user = user_input
                    st.success(f"ยินดีต้อนรับคุณ {user_input}!")
                    st.rerun()
                else:
                    st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

    # --- TAB: SIGN UP ---
    with auth_mode[1]:
        with st.container(border=True):
            new_user = st.text_input("สร้าง Username", key="reg_user")
            new_pass = st.text_input("สร้าง Password", type="password", key="reg_pass")
            confirm_pass = st.text_input("ยืนยัน Password", type="password", key="reg_confirm")
            
            if st.button("Register Now", use_container_width=True):
                if not new_user or not new_pass:
                    st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")
                elif new_user in st.session_state.users_db:
                    st.error("ชื่อผู้ใช้นี้มีคนใช้แล้ว")
                elif new_pass != confirm_pass:
                    st.error("รหัสผ่านไม่ตรงกัน")
                else:
                    # บันทึกข้อมูลผู้ใช้ใหม่ลงใน Session State
                    st.session_state.users_db[new_user] = new_pass
                    st.session_state.user_balances[new_user] = 0.0  # เริ่มต้น 0 บาท
                    st.session_state.user_histories[new_user] = []
                    st.success("สมัครสมาชิกสำเร็จ! กรุณาไปที่หน้า Login")

# --- MAIN APP PAGE ---
else:
    user = st.session_state.current_user
    
    # Sidebar
    st.sidebar.title("🏧 ATM Menu")
    st.sidebar.markdown(f"**Welcome, {user}!**")
    st.sidebar.divider()
    
    # ดึงค่าเงินปัจจุบันของผู้ใช้
    current_bal = st.session_state.user_balances[user]
    st.sidebar.metric(label="Current Balance", value=f"{current_bal:,.2f} ฿")
    
    if st.sidebar.button("Logout", icon="🚀"):
        st.session_state.is_logged_in = False
        st.session_state.current_user = None
        st.rerun()

    # Main Content
    st.title("🏦 Banking Services")
    tab1, tab2, tab3 = st.tabs(["💰 Transactions", "📜 History", "⚙️ Settings"])

    with tab1:
        choice = st.radio("Select Service", ["Withdrawal (ถอนเงิน)", "Deposit (ฝากเงิน)"], horizontal=True)
        st.divider()

        if "Withdrawal" in choice:
            st.subheader("💳 Withdrawal")
            amount = st.number_input("Enter amount to withdraw:", min_value=0, step=100)
            
            if st.button("Confirm Withdrawal", type="primary"):
                if amount <= 0:
                    st.warning("Please enter an amount greater than 0.")
                elif amount > st.session_state.user_balances[user]:
                    st.error(f"❌ Error: Insufficient funds. (Available: {st.session_state.user_balances[user]} ฿)")
                elif amount > 1000:
                    st.error("❌ Error: Maximum withdrawal limit is 1,000 ฿ per transaction.")
                else:
                    st.session_state.user_balances[user] -= amount
                    now = datetime.datetime.now().strftime("%H:%M:%S")
                    st.session_state.user_histories[user].append(f"[-] {now} | Withdrew {amount:,.2f} ฿")
                    st.balloons()
                    st.success(f"✅ Withdrawal successful!")
                    st.rerun()

        elif "Deposit" in choice:
            st.subheader("💵 Deposit")
            amount = st.number_input("Enter amount to deposit:", min_value=0, step=100)
            
            if st.button("Confirm Deposit", type="primary"):
                if amount <= 0:
                    st.warning("Please enter an amount greater than 0.")
                elif amount > 5000:
                    st.error("❌ Error: Deposit limit exceeded (Max 5,000).")
                else:
                    st.session_state.user_balances[user] += amount
                    now = datetime.datetime.now().strftime("%H:%M:%S")
                    st.session_state.user_histories[user].append(f"[+] {now} | Deposited {amount:,.2f} ฿")
                    st.toast(f"Successfully deposited {amount} Baht!", icon='💰')
                    st.success(f"✅ Deposit successful!")
                    st.rerun()

    with tab2:
        st.subheader("🕒 Recent Transactions")
        history = st.session_state.user_histories[user]
        if not history:
            st.info("No transactions yet.")
        else:
            for item in reversed(history):
                st.text(item)

    with tab3:
        st.subheader("Account Settings")
        st.write(f"Account Name: {user}")
        st.write(f"Account Status: Active")
        if st.button("Clear History"):
            st.session_state.user_histories[user] = []
            st.rerun()

    st.divider()
    st.caption("© 2026 Dovesinthewind69 Bank Digital System")
