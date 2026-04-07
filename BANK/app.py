import streamlit as st

st.set_page_config(page_title="Dovesinthewind69", page_icon="🏦")

if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

if not st.session_state.is_logged_in:
    st.header("🔐 Login to ATM")
    
    user_input = st.text_input("Username", placeholder="Enter your username")
    pass_input = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Sign In"):
        if user_input == "ozone" and pass_input == "282007":
            st.session_state.is_logged_in = True
            st.success("Login successful!")
            st.rerun() 
        else:
            st.error("Login failed. Please check your credentials.")
            if user_input != "dovesinthewind69":
                st.warning("Username 'doves' not found.")
            elif pass_input != "282007":
                st.warning("Incorrect password for 'ozone'.")

else:
    st.sidebar.title("ATM Menu")
    st.sidebar.write(f"👤 User: **ozone**")
    if st.sidebar.button("Log out"):
        st.session_state.is_logged_in = False
        st.rerun()

    st.title("🏦 Banking Services")
    
    choice = st.radio("Please select a service:", ["Withdrawal (ถอนเงิน)", "Deposit (ฝากเงิน)"])

    st.divider()

    if "Withdrawal" in choice:
        st.subheader("💳 Withdrawal Mode")
        amount = st.number_input("Enter amount to withdraw:", min_value=0, step=100)
        
        if st.button("Confirm Withdrawal"):
            if amount > 1000:
                st.error("❌ Error: Withdrawal limit exceeded (Max 1000).")
            elif amount > 500:
                st.warning("⚠️ Error: Insufficient funds.")
            elif amount <= 0:
                st.info("💡 Please enter an amount greater than 0.")
            else:
                st.success(f"✅ Withdrawal successful! Please take your cash: {amount:,} Baht.")

    elif "Deposit" in choice:
        st.subheader("💰 Deposit Mode")
        amount = st.number_input("Enter amount to deposit:", min_value=0, step=100)
        
        if st.button("Confirm Deposit"):
            if amount > 1000:
                st.error("❌ Error: Deposit limit exceeded.")
            elif amount > 500:
                st.warning("⚠️ Error: Deposit amount too high for this machine.")
            elif amount <= 0:
                st.info("💡 Please enter an amount greater than 0.")
            else:
                st.success(f"✅ Deposit successful! Amount {amount:,} Baht has been added.")
        
