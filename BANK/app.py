import streamlit as st
import datetime

# --- CONFIG ---
st.set_page_config(page_title="DovesInTheWind69 Bank", page_icon="💎", layout="centered")

# --- LANGUAGE DICTIONARY ---
LANGUAGES = {
    "TH": {
        "welcome": "ยินดีต้อนรับสู่",
        "sub_welcome": "Developed by โอโซนบ้านร้อง",
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
        "sub_welcome": "Developed by โอโซนบ้านร้อง",
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
    st.session_state.user_balances = {"ozone": 9999.00}
if 'user_histories' not in st.session_state:
    st.session_state.user_histories = {"ozone": []}
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

def t(key):
    return LANGUAGES[st.session_state.lang][key]

# ============================================================
# PREMIUM CSS — replaces original minimal styles
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@200;300;400;500;600&family=Sarabun:wght@300;400;500&display=swap');

/* ── Base ─────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Sarabun', 'Kanit', sans-serif;
    background: #0a0f1e !important;
}
.stApp {
    background: radial-gradient(ellipse at 20% 0%, #0d1f44 0%, #0a0f1e 60%) !important;
}

/* ── Sidebar ──────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1a35 0%, #091229 100%) !important;
    border-right: 1px solid rgba(100,160,255,0.12) !important;
}
[data-testid="stSidebar"] * { color: #c8d8f0 !important; }
[data-testid="stSidebar"] .stSelectbox label { color: #7aa0d4 !important; font-size: 12px !important; }

/* ── Inputs & Forms ───────────────────────────────────── */
.stTextInput input, .stNumberInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(100,160,255,0.2) !important;
    border-radius: 10px !important;
    color: #e8f0ff !important;
    padding: 10px 14px !important;
    transition: border-color .2s, box-shadow .2s;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: rgba(100,180,255,0.5) !important;
    box-shadow: 0 0 0 3px rgba(80,140,255,0.12) !important;
}
.stTextInput label, .stNumberInput label {
    color: #7aa0d4 !important;
    font-size: 13px !important;
    font-weight: 400 !important;
}

/* ── Primary Buttons ──────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1a56c4 0%, #2d7fff 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-family: 'Kanit', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: .03em !important;
    padding: 10px 0 !important;
    box-shadow: 0 4px 20px rgba(45,127,255,0.3) !important;
    transition: all .2s !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1e65e0 0%, #4a90ff 100%) !important;
    box-shadow: 0 6px 28px rgba(45,127,255,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Secondary Buttons ────────────────────────────────── */
.stButton > button:not([kind="primary"]) {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(100,160,255,0.2) !important;
    border-radius: 12px !important;
    color: #a0c0f0 !important;
    font-family: 'Kanit', sans-serif !important;
    transition: all .2s !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: rgba(100,160,255,0.1) !important;
    border-color: rgba(100,160,255,0.4) !important;
    color: #d0e4ff !important;
}

/* ── Tabs ─────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 14px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(100,160,255,0.1) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    color: #6890c0 !important;
    font-family: 'Kanit', sans-serif !important;
    font-weight: 400 !important;
    transition: all .2s !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(45,127,255,0.2) !important;
    color: #a0d0ff !important;
    font-weight: 500 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 20px !important;
}

/* ── Alerts ───────────────────────────────────────────── */
.stAlert {
    border-radius: 12px !important;
    border: none !important;
}
.stAlert[data-type="error"] {
    background: rgba(200,60,60,0.15) !important;
    border-left: 3px solid #e05050 !important;
}
.stAlert[data-type="success"] {
    background: rgba(30,180,100,0.12) !important;
    border-left: 3px solid #30c880 !important;
}
.stAlert[data-type="info"] {
    background: rgba(50,120,220,0.12) !important;
    border-left: 3px solid #4090e0 !important;
}

/* ── Divider ──────────────────────────────────────────── */
hr { border-color: rgba(100,160,255,0.1) !important; }

/* ── Subheader / Text ─────────────────────────────────── */
h2, h3, [data-testid="stSubheader"] {
    color: #c0d8f8 !important;
    font-family: 'Kanit', sans-serif !important;
    font-weight: 400 !important;
}
p, .stMarkdown p, .stCaption { color: #7090b8 !important; }

/* ── Number input spinner ─────────────────────────────── */
.stNumberInput button {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(100,160,255,0.2) !important;
    color: #a0c0f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("<div style='padding:8px 0 4px;'><span style='font-size:18px;font-family:Kanit,sans-serif;font-weight:500;color:#a0c8f8;'>🌐 Language</span></div>", unsafe_allow_html=True)
    st.session_state.lang = st.selectbox(
        "Select Language", options=["TH", "EN"],
        index=0 if st.session_state.lang == "TH" else 1,
        label_visibility="collapsed"
    )

    if st.session_state.is_logged_in:
        st.divider()
        st.markdown(f"""
            <div style='
                background: rgba(45,127,255,0.1);
                border: 1px solid rgba(100,160,255,0.2);
                border-radius: 12px;
                padding: 12px 14px;
                margin-bottom: 12px;
            '>
                <div style='font-size:11px;color:#5a80b0;font-family:Sarabun,sans-serif;margin-bottom:2px;'>Signed in as</div>
                <div style='font-size:15px;color:#a0d0ff;font-family:Kanit,sans-serif;font-weight:500;'>👤 {st.session_state.current_user}</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button(t("logout"), use_container_width=True):
            st.session_state.is_logged_in = False
            st.rerun()

# ============================================================
# AUTH SCREEN
# ============================================================
if not st.session_state.is_logged_in:

    # Hero header
    st.markdown("""
        <div style='text-align:center;padding:40px 0 10px;'>
            <div style='
                display:inline-block;
                font-size:52px;
                line-height:1;
                filter: drop-shadow(0 0 24px rgba(80,160,255,0.5));
            '>💎</div>
            <h1 style='
                font-family:Kanit,sans-serif;
                font-weight:200;
                font-size:30px;
                letter-spacing:.15em;
                color:#c8e0ff;
                margin:12px 0 4px;
                text-transform:uppercase;
            '>DOVESINTHEWIND69</h1>
            <div style='
                font-family:Kanit,sans-serif;
                font-weight:600;
                font-size:13px;
                letter-spacing:.35em;
                color:#2d7fff;
                text-transform:uppercase;
                margin-bottom:6px;
            '>DIGITAL BANK</div>
            <div style='
                font-size:12px;
                color:#3a5880;
                font-family:Sarabun,sans-serif;
                margin-bottom:32px;
            '>Developed by โอโซนบ้านร้อง</div>
        </div>
    """, unsafe_allow_html=True)

    # Auth card
    st.markdown("""
        <div style='
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(100,160,255,0.15);
            border-radius: 20px;
            padding: 28px 28px 8px;
            backdrop-filter: blur(10px);
            max-width: 420px;
            margin: 0 auto;
        '>
    """, unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs([f"🔒 {t('login')}", f"📝 {t('signup')}"])

    with tab_login:
        with st.form("l_form"):
            u = st.text_input(t("user_label"))
            p = st.text_input(t("pass_label"), type="password")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
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
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            if st.form_submit_button(t("btn_signup"), use_container_width=True):
                if new_p == conf_p and new_u:
                    st.session_state.users_db[new_u] = new_p
                    st.session_state.user_balances[new_u] = 0.0
                    st.session_state.user_histories[new_u] = []
                    st.success("Account created! Please login.")
                else:
                    st.error("Passwords don't match or username empty / ข้อมูลไม่ถูกต้อง")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# MAIN DASHBOARD
# ============================================================
else:
    user = st.session_state.current_user
    balance = st.session_state.user_balances[user]

    # ── Balance Card ──────────────────────────────────────
    st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #0d2260 0%, #1a3d8f 50%, #0f2a6e 100%);
            border: 1px solid rgba(80,140,255,0.25);
            border-radius: 24px;
            padding: 36px 32px;
            text-align: center;
            position: relative;
            overflow: hidden;
            margin-bottom: 24px;
            box-shadow: 0 20px 60px rgba(10,20,60,0.6), 0 0 0 1px rgba(80,140,255,0.1);
        '>
            <!-- decorative glow orbs -->
            <div style='
                position:absolute;top:-40px;right:-40px;
                width:160px;height:160px;
                background:radial-gradient(circle,rgba(45,127,255,0.2) 0%,transparent 70%);
                border-radius:50%;pointer-events:none;
            '></div>
            <div style='
                position:absolute;bottom:-30px;left:-30px;
                width:120px;height:120px;
                background:radial-gradient(circle,rgba(80,200,255,0.1) 0%,transparent 70%);
                border-radius:50%;pointer-events:none;
            '></div>

            <div style='
                font-family:Sarabun,sans-serif;
                font-size:12px;
                letter-spacing:.2em;
                color:rgba(160,200,255,0.7);
                text-transform:uppercase;
                margin-bottom:10px;
            '>{t('balance_title')}</div>
            <div style='
                font-family:Kanit,sans-serif;
                font-weight:300;
                font-size:48px;
                color:#e8f4ff;
                line-height:1;
                letter-spacing:-.01em;
                text-shadow:0 0 40px rgba(80,160,255,0.4);
            '>{balance:,.2f} <span style='font-size:24px;color:#5090d0;'>฿</span></div>
            <div style='
                margin-top:16px;
                display:inline-block;
                background:rgba(45,127,255,0.15);
                border:1px solid rgba(45,127,255,0.3);
                border-radius:20px;
                padding:4px 16px;
                font-size:12px;
                color:#80b8f0;
                font-family:Sarabun,sans-serif;
                letter-spacing:.05em;
            '>{t('acc_type')}</div>
        </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────
    t1, t2, t3 = st.tabs([f"💸 {t('tab_trans')}", f"📜 {t('tab_hist')}", f"⚙️ {t('tab_sett')}"])

    with t1:
        col1, col2 = st.columns(2, gap="medium")

        with col1:
            st.markdown(f"""
                <div style='
                    background:rgba(30,180,100,0.06);
                    border:1px solid rgba(30,180,100,0.2);
                    border-radius:16px;
                    padding:16px 16px 4px;
                    margin-bottom:12px;
                '>
                <div style='
                    font-family:Kanit,sans-serif;font-size:16px;
                    font-weight:500;color:#40c880;margin-bottom:12px;
                '>🟢 {t("dep_title")}</div>
            """, unsafe_allow_html=True)
            amt_d = st.number_input(t("amount"), min_value=0, key="d", step=100, label_visibility="collapsed")
            if st.button(t("btn_confirm"), key="bd", use_container_width=True, type="primary"):
                if amt_d > 0:
                    st.session_state.user_balances[user] += amt_d
                    st.session_state.user_histories[user].append(
                        f"🟢 {datetime.datetime.now().strftime('%d/%m %H:%M')} | {t('dep_title')}: +{amt_d:,.2f} ฿"
                    )
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div style='
                    background:rgba(220,60,60,0.06);
                    border:1px solid rgba(220,60,60,0.2);
                    border-radius:16px;
                    padding:16px 16px 4px;
                    margin-bottom:12px;
                '>
                <div style='
                    font-family:Kanit,sans-serif;font-size:16px;
                    font-weight:500;color:#e06060;margin-bottom:12px;
                '>🔴 {t("with_title")}</div>
            """, unsafe_allow_html=True)
            amt_w = st.number_input(t("amount"), min_value=0, key="w", step=100, label_visibility="collapsed")
            if st.button(t("btn_confirm"), key="bw", use_container_width=True):
                if amt_w > 0:
                    if amt_w <= st.session_state.user_balances[user]:
                        st.session_state.user_balances[user] -= amt_w
                        st.session_state.user_histories[user].append(
                            f"🔴 {datetime.datetime.now().strftime('%d/%m %H:%M')} | {t('with_title')}: -{amt_w:,.2f} ฿"
                        )
                        st.rerun()
                    else:
                        st.error(t("error_balance"))
            st.markdown("</div>", unsafe_allow_html=True)

    with t2:
        hist = st.session_state.user_histories[user]
        if not hist:
            st.markdown(f"""
                <div style='
                    text-align:center;padding:48px 0;
                    color:rgba(100,140,200,0.5);
                    font-family:Sarabun,sans-serif;font-size:15px;
                '>
                    <div style='font-size:32px;margin-bottom:10px;opacity:.4;'>📭</div>
                    {t("history_empty")}
                </div>
            """, unsafe_allow_html=True)
        else:
            for i, item in enumerate(reversed(hist)):
                is_dep = "🟢" in item
                accent = "rgba(30,180,100,0.6)" if is_dep else "rgba(220,60,60,0.6)"
                bg = "rgba(30,180,100,0.05)" if is_dep else "rgba(220,60,60,0.05)"
                st.markdown(f"""
                    <div style='
                        background:{bg};
                        border:1px solid rgba(100,160,255,0.08);
                        border-left:3px solid {accent};
                        border-radius:12px;
                        padding:12px 16px;
                        margin-bottom:8px;
                        font-family:Sarabun,sans-serif;
                        font-size:14px;
                        color:#a0c0e8;
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                    '>
                        <span>{item}</span>
                    </div>
                """, unsafe_allow_html=True)

    with t3:
        st.markdown(f"""
            <div style='
                background:rgba(255,255,255,0.03);
                border:1px solid rgba(100,160,255,0.12);
                border-radius:16px;
                padding:20px 20px 8px;
                margin-bottom:16px;
            '>
                <div style='
                    font-family:Kanit,sans-serif;font-size:16px;
                    color:#80b8f0;margin-bottom:14px;font-weight:400;
                '>Account Info</div>
                <div style='display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(100,160,255,0.08);'>
                    <span style='color:#3a6090;font-family:Sarabun,sans-serif;font-size:13px;'>{t("user_label")}</span>
                    <span style='color:#a0c8f0;font-family:Kanit,sans-serif;font-size:13px;font-weight:500;'>{user}</span>
                </div>
                <div style='display:flex;justify-content:space-between;padding:10px 0;'>
                    <span style='color:#3a6090;font-family:Sarabun,sans-serif;font-size:13px;'>Type</span>
                    <span style='
                        background:rgba(45,127,255,0.15);
                        border:1px solid rgba(45,127,255,0.25);
                        border-radius:8px;
                        padding:2px 10px;
                        color:#6090d8;
                        font-size:12px;
                        font-family:Sarabun,sans-serif;
                    '>Savings ออมทรัพย์</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button(t("clear_hist"), type="secondary"):
            st.session_state.user_histories[user] = []
            st.rerun()

    # ── Footer ────────────────────────────────────────────
    st.markdown("""
        <div style='
            text-align:center;
            margin-top:32px;
            padding:16px 0;
            border-top:1px solid rgba(100,160,255,0.08);
            font-family:Sarabun,sans-serif;
            font-size:11px;
            color:rgba(60,100,160,0.6);
            letter-spacing:.05em;
        '>
            © 2026 DOVESINTHEWIND69 BANK DIGITAL SYSTEM · Developed by โอโซนบ้านร้อง
        </div>
    """, unsafe_allow_html=True)
