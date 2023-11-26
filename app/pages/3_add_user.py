import streamlit as st
from werkzeug.security import generate_password_hash
from models import SessionLocal, User
from init import init_app


init_app()

st.title(":female-scientist: Add New Worker")

if st.session_state.is_admin:
    with st.form("new_user_form", clear_on_submit=True):
        st.write("Add a New User")
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit_button = st.form_submit_button("Create User")
        role = st.radio("Select Role:", ["User", "Administrator"])

        if submit_button:
            if password == confirm_password:
                # Hash the password
                hashed_password = generate_password_hash(password)
                # Create a new User instance
                new_user = User(
                    name=name, email=email, password=hashed_password, role=role
                )
                # Add to the session and commit
                with SessionLocal() as session:
                    session.add(new_user)
                    try:
                        session.commit()
                        st.success("User added successfully.")
                    except Exception as e:
                        session.rollback()
                        st.error(f"An error occurred: {e}")
            else:
                st.error("Passwords do not match.")
else:
    st.warning("Only an administrator can view this page")
