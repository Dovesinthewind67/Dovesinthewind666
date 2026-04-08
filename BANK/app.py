import streamlit as st
import datetime

# --- CONFIG ---
st.set_page_config(page_title="Doves Bank", page_icon="💎", layout="centered")

# --- LANGUAGE DICTIONARY ---
LANGUAGES = {
    "TH": {
        "welcome": "ยินดีต้อนรับสู่",
        "sub_welcome": "Developed by โอโซนบ้านร้อง", # เปลี่ยนตามคำขอ
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
        "sub_welcome": "Developed by Ozone Ban Rong", # เปลี่ยนให้ล้อกันในภาษาอังกฤษ
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
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .developer-tag {
        color: #764ba2; font-weight: 500; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🌐 Language")
    st.session_state.lang = st.selectbox("Select Language", options=["TH", "EN"], index=0 if st.session_state.lang == "TH" else 1)
    
    if st.session_state.is_logged_in:
        st.divider()
        st.write(f"👤 **{st.session_state.current_user}**")
        if st.button(
