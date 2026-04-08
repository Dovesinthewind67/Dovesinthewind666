import streamlit as st
import datetime

# --- CONFIG ---
st.set_page_config(page_title="DovesInTheWind69 Bank", page_icon="💎", layout="centered")

# --- LANGUAGE DICTIONARY ---
LANGUAGES = {
    "TH": {
        "welcome": "ยินดีต้อนรับสู่",
        "sub_welcome": "ระบบธนาคารดิจิทัล",
        "login": "เข้าสู่ระบบ",
        "signup": "เปิดบัญชี",
        "user_label": "ชื่อผู้ใช้งาน",
        "pass_label": "รหัสผ่าน",
        "confirm_pass": "ยืนยันรหัสผ่าน",
        "btn_signin": "ยืนยันตัวตน",
        "btn_signup": "สร้างบัญชีใหม่",
        "balance_title": "ยอดเงินที่ใช้ได้",
        "tab_trans": "ธุรกรรม",
        "tab_hist": "ประวัติ",
        "tab_sett": "ตั้งค่า",
        "dep_title": "ฝากเงิน",
        "with_title": "ถอนเงิน",
        "transfer_title": "โอนเงิน",
        "amount": "ระบุจำนวนเงิน",
        "btn_confirm": "ยืนยันรายการ",
        "history_empty": "ไม่พบประวัติธุรกรรม",
        "logout": "ออกจากระบบ",
        "success": "ทำรายการสำเร็จ",
        "error_balance": "ยอดเงินไม่เพียงพอ",
        "acc_type": "ประเภทบัญชี: ออมทรัพย์",
        "clear_hist": "ล้างประวัติธุรกรรม"
    },
    "EN": {
        "welcome": "Welcome to",
        "sub_welcome": "Secure & Simple Digital Banking",
        "login": "Login",
        "signup": "Sign Up",
        "user_label": "Username",
        "pass_label": "Password",
        "confirm_pass": "Confirm Password",
        "btn_signin": "Sign In",
        "btn_signup": "Create Account",
        "balance_title": "Available Balance",
        "tab_trans": "Transactions",
        "tab_hist": "History",
        "tab_sett": "Settings",
        "dep_title": "Deposit",
        "with_title": "Withdraw",
        "transfer_title": "Transfer",
        "amount": "Enter Amount",
        "btn_confirm": "Confirm",
        "history_empty": "No transaction history",
        "logout": "Logout",
        "success": "Transaction Successful",
        "error_balance": "Insufficient balance",
        "acc_type": "Account Type: Savings",
        "clear_hist": "Clear History"
    }
}

# --- SESSION STATE ---
if 'lang' not in st.session_state:
    st.session_state.lang = "TH"
if 'users_db' not in st.session_state:
    st.session_state.users_db = {"ozone": "282007"}
if 'user_balances' not in st.session_state:
    st.session_state.user_balances = {"ozone": 500.0}
if 'user_histories' not in st.session_state:
    st.session_state.user_histories = {"ozone": []}
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

# Helper function to get text
def t(key):
    return LANGUAGES[st.session_state.lang][key]

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500&display=swap');
    html, body, [class*="css"] { font-family: 'Kanit', sans-serif; }
    .balance-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 30px; border-radius: 20px; color: white; text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .history-item {
        background: white; padding: 12px; border-radius: 12px;
        margin-bottom: 8px; border-left: 5px solid #2a5298;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR LANGUAGE & LOGOUT ---
with st.sidebar:
    st.title("🌐 Language / ภาษา")
    st.session_state.lang = st.selectbox("Select Language", options=["TH", "EN"], index=0 if st.session_state.lang == "TH" else 1)
    
    if st.session_state.is_logged_in:
        st.divider()
        st.write(f"👤 **{st.session_state.current_user}**")
        if st.button(t("logout"), use_container_width=True):
            st.session_state.is_logged_in = False
            st.rerun()

# --- AUTHENTICATION ---
if not st.session_state.is_logged_in:
    st.markdown(f"<h1 style='text-align: center; color: #1e3c72;'>💎 DOVESINTHEWIND69 BANK</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: gray;'>{t('sub_welcome')}</p>", unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs([f"🔒 {t('login')}", f"📝 {t('signup')}"])

    with tab_login:
        with st.form("l_form"):
            u = st.text_input(t("user_label"))
            p = st.text_input(t("pass_label"), type="password")
            if st.form_submit_button(t("btn_signin"), use_container_width=True, type="primary"):
                if u in st.session_state.users_db and st.session_state.users_db[u] == p:
                    st.session_state.is_logged_in = True
                    st.session_state.current_user = u
                    st.rerun()
                else:
                    st.error("Invalid credentials / ข้อมูลไม่ถูกต้อง")

    with tab_signup:
        with st.form("s_form"):
            new_u = st.text_input(t("user_label"))
            new_p = st.text_input(t("pass_label"), type="password")
            conf_p = st.text_input(t("confirm_pass"), type="password")
            if st.form_submit_button(t("btn_signup"), use_container_width=True):
                if new_p == conf_p and new_u:
                    st.session_state.users_db[new_u] = new_p
                    st.session_state.user_balances[new_u] = 0.0
                    st.session_state.user_histories[new_u] = []
                    st.success("Account created! Please login.")
                else:
                    st.error("Error in details / ข้อมูลไม่ถูกต้อง")

# --- MAIN APP ---
else:
    user = st.session_state.current_user
    
    st.markdown(f"""
        <div class="balance-card">
            <small>{t('balance_title')}</small>
            <h1 style='margin:0;'>{st.session_state.user_balances[user]:,.2f} ฿</h1>
        </div>
    """, unsafe_allow_html=True)

    t1, t2, t3 = st.tabs([f"💸 {t('tab_trans')}", f"📜 {t('tab_hist')}", f"⚙️ {t('tab_sett')}"])

    with t1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(t("dep_title"))
            amt_d = st.number_input(t("amount"), min_value=0, key="d", step=100)
            if st.button(t("btn_confirm"), key="bd", use_container_width=True, type="primary"):
                if amt_d > 0:
                    st.session_state.user_balances[user] += amt_d
                    st.session_state.user_histories[user].append(f"🟢 {datetime.datetime.now().strftime('%H:%M')} | {t('dep_title')}: +{amt_d:,.2f}")
                    st.rerun()

        with col2:
            st.subheader(t("with_title"))
            amt_w = st.number_input(t("amount"), min_value=0, key="w", step=100)
            if st.button(t("btn_confirm"), key="bw", use_container_width=True):
                if amt_w > 0:
                    if amt_w <= st.session_state.user_balances[user]:
                        st.session_state.user_balances[user] -= amt_w
                        st.session_state.user_histories[user].append(f"🔴 {datetime.datetime.now().strftime('%H:%M')} | {t('with_title')}: -{amt_w:,.2f}")
                        st.rerun()
                    else:
                        st.error(t("error_balance"))

    with t2:
        st.subheader(t("tab_hist"))
        hist = st.session_state.user_histories[user]
        if not hist:
            st.info(t("history_empty"))
        else:
            for item in reversed(hist):
                st.markdown(f"<div class='history-item'>{item}</div>", unsafe_allow_html=True)

    with t3:
        st.subheader(t("tab_sett"))
        st.write(f"**{t('user_label')}:** {user}")
        st.write(f"**{t('acc_type')}**")
        if st.button(t("clear_hist"), type="secondary"):
            st.session_state.user_histories[user] = []
            st.rerun()

    st.divider()
    st.caption("© 2026 DOVESINTHEWIND69 BANK DIGITAL SYSTEM - Developed by โอโซนบ้านร้อง.")
