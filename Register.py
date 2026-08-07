import streamlit as st

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    
st.title("Welcome")
st.subheader("Register")

name = st.text_input("Enter your name:")
# Selectbox
Department = st.selectbox("Select your Department:", ["Sale","Institute", "Accounting", "Engineering","Managerial"],
                          index=None,
                          placeholder="Choose your department..."
                          )
if st.button("Login",icon=":material/login:", type="primary"):
    if not st.session_state['logged_in']:
        if name:
            st.session_state['user_dept'] = Department
            st.session_state['user_name'] = name
            st.session_state['logged_in'] = True
            st.success(f"Welcome! Redirecting...")
            st.switch_page("Pages/Data_analysis.py")
        else:
            st.error("Please enter your details first.")
            
       
        

    