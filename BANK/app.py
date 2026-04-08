import streamlit as st
import datetime
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Dovesinthewind69 Bank | Digital Banking", page_icon="💎", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&display=swap');
    
    * { font-family: 'Kanit', sans-serif; }
    
    .main { background-color: #f0f2f6; }
    
    /* สไตล์บัตรยอดเงิน */
    .balance-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 30px;
        border-radius: 24px;
        color: white;
        text-align: left;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(30, 60, 114, 0.2);
        position: relative;
        overflow: hidden;
    }
    .balance-card::after {
        content: "VISA";
        position: absolute;
        bottom: 20px;
        right: 30px;
        font-weight: bold;
        opacity: 0.3;
        font-size: 1.5rem;
    }

    /* สไตล์รายการประวัติ */
    .history-item {
        background: white;
        padding: 15px 20px;
        border-radius: 15px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        border: 1px solid #eee;
    }
    
    .status-up { color: #28a745; font-weight: 600; }
    .status-down { color: #dc3545; font-weight: 600; }
    
    /* ปุ่ม */
    .stButton>button {
        border-radius: 10px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'users_db' not in st.session_state:
    st.session_state.users_db = {"ozone": "282007", "admin": "1234"}
if 'user_balances' not in st.session_state:
    st.session_state.user_balances = {"ozone": 500.0, "admin": 1000000.0}
if 'user_histories' not in st.session_state:
    st.session_state.user_histories = {"ozone": [], "admin": []}
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# --- AUTHENTICATION INTERFACE ---
if not st.session_state.is_logged_in:
    st.markdown("<h1 style='text-align: center; color: #1e3c72;'>💎 DOVESINTHEWIND69 BANK</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        auth_mode = st.tabs(["🔐 เข้าสู่ระบบ", "✨ เปิดบัญชีใหม่"])

        with auth_mode[0]:
            with st.form("login_form"):
                user_input = st.text_input("ชื่อผู้ใช้งาน (Username)")
                pass_input = st.text_input("รหัสผ่าน (Password)", type="password")
                if st.form_submit_button("ยืนยันตัวตน", use_container_width=True, type="primary"):
                    if user_input in st.session_state.users_db and st.session_state.users_db[user_input] == pass_input:
                        st.session_state.is_logged_in = True
                        st.session_state.current_user = user_input
                        st.rerun()
                    else:
                        st.error("ข้อมูลไม่ถูกต้อง กรุณาลองใหม่")

        with auth_mode[1]:
            with st.form("reg_form"):
                new_user = st.text_input("ตั้งชื่อผู้ใช้งาน")
                new_pass = st.text_input("ตั้งรหัสผ่าน", type="password")
                confirm_pass = st.text_input("ยืนยันรหัสผ่าน", type="password")
                if st.form_submit_button("ลงทะเบียน", use_container_width=True):
                    if not new_user or not new_pass:
                        st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")
                    elif new_user in st.session_state.users_db:
                        st.error("ชื่อผู้ใช้งานนี้ถูกใช้ไปแล้ว")
                    elif new_pass != confirm_pass:
                        st.error("รหัสผ่านไม่ตรงกัน")
                    else:
                        st.session_state.users_db[new_user] = new_pass
                        st.session_state.user_balances[new_user] = 0.0
                        st.session_state.user_histories[new_user] = []
                        st.success("สร้างบัญชีสำเร็จ! กรุณาเข้าสู่ระบบ")

# --- MAIN DASHBOARD ---
else:
    user = st.session_state.current_user
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 💳 สวัสดี,คุณ {user}")
        st.caption("สถานะบัญชี: ปกติ (Verified)")
        st.divider()
        if st.button("ออกจากระบบ", use_container_width=True):
            st.session_state.is_logged_in = False
            st.rerun()

    # Dashboard Header
    st.markdown(f"""
        <div class="balance-card">
            <p style='margin:0; opacity:0.8; font-size: 0.9rem;'>ยอดเงินที่ใช้ได้ทั้งหมด</p>
            <h1 style='margin:0; font-size: 2.8rem;'>{st.session_state.user_balances[user]:,.2f} <span style='font-size: 1.2rem;'>THB</span></h1>
            <p style='margin-top:15px; font-size: 0.8rem; opacity:0.6;'>เลขบัญชี: 000-xxxx-{user[:2].upper()}</p>
        </div>
    """, unsafe_allow_html=True)

    # Features
    tab1, tab2, tab3 = st.tabs(["🔄 ธุรกรรม", "📑 ประวัติ", "⚙️ ตั้งค่า"])

    with tab1:
        m_col1, m_col2 = st.columns(2)
        
        with m_col1:
            with st.expander("📥 ฝากเงิน (Deposit)", expanded=True):
                d_amount = st.number_input("จำนวนเงินที่ต้องการฝาก", min_value=0.0, step=100.0, key="d_val")
                if st.button("ยืนยันการฝาก", type="primary", use_container_width=True):
                    if d_amount > 0:
                        st.session_state.user_balances[user] += d_amount
                        now = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
                        st.session_state.user_histories[user].append({"type": "IN", "msg": f"ฝากเงินสด", "amt": d_amount, "time": now})
                        st.toast(f"ฝากเงินสำเร็จ +{d_amount:,.2f} ฿")
                        st.rerun()

        with m_col2:
            with st.expander("📤 ถอนเงิน (Withdraw)", expanded=True):
                w_amount = st.number_input("จำนวนเงินที่ต้องการถอน", min_value=0.0, step=100.0, key="w_val")
                if st.button("ยืนยันการถอน", use_container_width=True):
                    if w_amount > st.session_state.user_balances[user]:
                        st.error("ยอดเงินไม่เพียงพอ")
                    elif w_amount > 0:
                        st.session_state.user_balances[user] -= w_amount
                        now = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
                        st.session_state.user_histories[user].append({"type": "OUT", "msg": f"ถอนเงินสด", "amt": w_amount, "time": now})
                        st.rerun()

        st.divider()
        
        # --- NEW FEATURE: TRANSFER ---
        st.subheader("💸 โอนเงินไปยังผู้ใช้อื่น")
        with st.container(border=True):
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                target_user = st.selectbox("เลือกผู้รับเงิน", options=[u for u in st.session_state.users_db.keys() if u != user])
            with t_col2:
                t_amount = st.number_input("ระบุจำนวนเงินโอน", min_value=0.0, step=50.0)
            
            if st.button("ยืนยันการโอนเงิน", use_container_width=True, type="primary"):
                if t_amount > st.session_state.user_balances[user]:
                    st.error("ยอดเงินไม่เพียงพอสำหรับการโอน")
                elif t_amount <= 0:
                    st.warning("กรุณาระบุจำนวนเงินที่ถูกต้อง")
                else:
                    # หักเงินผู้โอน
                    st.session_state.user_balances[user] -= t_amount
                    # เพิ่มเงินผู้รับ
                    st.session_state.user_balances[target_user] += t_amount
                    
                    now = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
                    # บันทึกประวัติทั้งสองฝ่าย
                    st.session_state.user_histories[user].append({"type": "OUT", "msg": f"โอนให้คุณ {target_user}", "amt": t_amount, "time": now})
                    st.session_state.user_histories[target_user].append({"type": "IN", "msg": f"รับเงินจาก {user}", "amt": t_amount, "time": now})
                    
                    st.success(f"โอนเงินให้ {target_user} สำเร็จ!")
                    st.balloons()
                    st.rerun()

    with tab2:
        st.subheader("รายการล่าสุด")
        history = st.session_state.user_histories[user]
        if not history:
            st.info("ยังไม่มีรายการธุรกรรมในขณะนี้")
        else:
            for item in reversed(history):
                color_class = "status-up" if item['type'] == "IN" else "status-down"
                prefix = "+" if item['type'] == "IN" else "-"
                
                st.markdown(f"""
                <div class="history-item">
                    <div>
                        <small style='color:gray;'>{item['time']}</small><br>
                        <strong>{item['msg']}</strong>
                    </div>
                    <div class="{color_class}">
                        {prefix}{item['amt']:,.2f} ฿
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        st.subheader("การจัดการบัญชี")
        col_a, col_b = st.columns(2)
        with col_a:
            st.info(f"**Username:** {user}\n\n**ประเภท:** ออมทรัพย์ดิจิทัล")
        with col_b:
            if st.button("🗑️ ล้างประวัติธุรกรรม", use_container_width=True):
                st.session_state.user_histories[user] = []
                st.rerun()
        
        st.divider()
        st.caption("ระบบรักษาความปลอดภัย DoveSecure™ ทำงานอยู่")

    st.markdown("<p style='text-align: center; color: #bdc3c7; font-size: 0.8rem; margin-top: 50px;'>© 2026 DOVESINTHEWIND69 BANKING GROUP. All Rights Reserved.</p>", unsafe_allow_html=True)
