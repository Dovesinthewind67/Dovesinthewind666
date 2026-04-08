import streamlit as st
import datetime

# --- CONFIG ---
st.set_page_config(page_title="Dovesinthewind69 Bank", page_icon="🏦", layout="centered")

# --- SESSION STATE INITIALIZATION ---
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'balance' not in st.session_state:
    st.session_state.balance = 500  
if 'history' not in st.session_state:
    st.session_state.history = [] 
# --- LOGIN PAGE ---
if not st.session_state.is_logged_in:
    st.markdown("<h1 style='text-align: center;'>🔐 DOVESINTHEWIND69 BANK LOGIN </h1>", unsafe_allow_html=True)
    
    with st.container(border=True):
        user_input = st.text_input("Username", placeholder="Enter your username")
        pass_input = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        if col2.button("Sign In", use_container_width=True):
            if user_input == "ozone" and pass_input == "282007":
                st.session_state.is_logged_in = True
                st.session_state.user_name = "ozone"
                st.success("Login successful!")
                st.rerun() 
            else:
                st.error("Login failed. Please check your credentials.")

# --- MAIN APP PAGE ---
else:
    # Sidebar
    st.sidebar.title("🏧 ATM Menu")
    st.sidebar.markdown(f"**Welcome, {st.session_state.user_name}!**")
    st.sidebar.divider()
    
    st.sidebar.metric(label="Current Balance", value=f"{st.session_state.balance:,.2f} ฿")
    
    if st.sidebar.button("Logout", icon="🚀"):
        st.session_state.is_logged_in = False
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
                elif amount > st.session_state.balance:
                    st.error(f"❌ Error: Insufficient funds. (Available: {st.session_state.balance} ฿)")
                elif amount > 1000:
                    st.error("❌ Error: Maximum withdrawal limit is 1,000 ฿ per transaction.")
                else:
                    st.session_state.balance -= amount
                    now = datetime.datetime.now().strftime("%H:%M:%S")
                    st.session_state.history.append(f"[-] {now} | Withdrew {amount:,.2f} ฿")
                    st.balloons()
                    st.success(f"✅ Withdrawal successful! Remaining: {st.session_state.balance:,.2f} ฿")

        elif "Deposit" in choice:
            st.subheader("💵 Deposit")
            amount = st.number_input("Enter amount to deposit:", min_value=0, step=100)
            
            if st.button("Confirm Deposit", type="primary"):
                if amount <= 0:
                    st.warning("Please enter an amount greater than 0.")
                elif amount > 5000: # เพิ่มลิมิตฝากให้เยอะขึ้นหน่อย
                    st.error("❌ Error: Deposit limit exceeded (Max 5,000).")
                else:
                    st.session_state.balance += amount
                    now = datetime.datetime.now().strftime("%H:%M:%S")
                    st.session_state.history.append(f"[+] {now} | Deposited {amount:,.2f} ฿")
                    st.toast(f"Successfully deposited {amount} Baht!", icon='💰')
                    st.success(f"✅ Deposit successful! Total Balance: {st.session_state.balance:,.2f} ฿")

    with tab2:
        st.subheader("🕒 Recent Transactions")
        if not st.session_state.history:
            st.info("No transactions yet.")
        else:
            for item in reversed(st.session_state.history):
                st.text(item)

    with tab3:
        st.subheader("Account Settings")
        st.write(f"Account Name: {st.session_state.user_name}")
        st.write(f"Account Status: Active")
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

    st.divider()
    st.caption("© 2026 Dovesinthewind69 Bank Digital System")
