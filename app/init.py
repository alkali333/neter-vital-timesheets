import os
import streamlit as st
from datetime import datetime

from utils import logout
from models import SessionLocal
from db_functions import handle_login


def init_app():
    """Intialises state variables, creates sidebar, creates header and welcome"""
    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "user_name" not in st.session_state:
        st.session_state.user_name = None

    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False

    st.sidebar.image("./images/logo.png", width=222)

    if not st.session_state.user_id:
        # Use a form for the login inputs and button
        with st.sidebar.form(key="login_form"):
            email = st.text_input("Email", value="jake@alkalimedia.co.uk")
            password = st.text_input(
                "Password", type="password", value=os.getenv("DEBUGGING_PASSWORD")
            )

            # Create a form and use the 'on_click' parameter to specify the callback function
            if st.form_submit_button(label="Login"):
                with SessionLocal() as session:
                    handle_login(email, password, session)

    if st.session_state.user_id:
        st.sidebar.write(f"Logged in as {st.session_state.user_name}")
        st.sidebar.button(label="Log Out", on_click=logout)

    current_datetime = datetime.now()

    st.header(current_datetime.strftime("%d %B %Y"))
    st.info(f"Welcome, {st.session_state.user_name or 'Please Log In'}")
