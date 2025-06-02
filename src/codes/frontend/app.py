import streamlit as st
from pathlib import Path
import sys

# Add backend directory to path
sys.path.append(str(Path(__file__).parent.parent / 'backend'))
from backend import AuthManager

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Initialize auth manager
auth = AuthManager()

def main():
    st.title("My Streamlit App")

    if not st.session_state.authenticated:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Login"):
                if auth.login_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        with col2:
            if st.button("Register"):
                if auth.register_user(username, password):
                    st.success("Registered successfully! Please login.")
                else:
                    st.error("Username already exists")
    else:
        st.write(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
        
        # Your main app content here
        st.subheader("Main Content")
        st.write("Add your application content here")

if __name__ == "__main__":
    main()