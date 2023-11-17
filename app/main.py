import streamlit as st
from models import User, Shift, SessionLocal
from db_functions import (
    authenticate,
    find_shift_for_user_today,
    start_shift,
    start_break,
    end_break,
)
from datetime import datetime, timezone


st.set_page_config(
    page_title="Neter Vital Timesheet",
    page_icon=":herb:",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)


st.title("Neter Vital Timesheet")
# Get the current date and time in UTC
current_utc_datetime = datetime.now(timezone.utc)

# Format the date and time in a nice format, for example: 'YYYY-MM-DD HH:MM:SS'
formatted_date = current_utc_datetime.strftime("%Y-%m-%d %H:%M:%S")

st.header(formatted_date)


# user not logged in
if "user_id" not in st.session_state:
    email = st.sidebar.text_input("Email", value="jake@alkalimedia.co.uk")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        with SessionLocal() as session:
            authenticated = authenticate(session, User, email, password)

        if authenticated:
            with SessionLocal() as session:
                user_in_db = session.query(User).filter_by(email=email).first()

                st.session_state.user_id = user_in_db.user_id
                # store user name
                st.session_state.user_name = user_in_db.name

else:
    st.write(f"Welcome {st.session_state.user_name}")

    with SessionLocal() as session:
        user_shift_today = find_shift_for_user_today(
            user_id=st.session_state.user_id, session=session
        )
        if user_shift_today:
            # store the shift ID in a session variable
            st.session_state.shift_id = user_shift_today.shift_id

            if user_shift_today.status == "working":
                if st.button(label="Start My Break", use_container_width=True):
                    with SessionLocal() as session:
                        start_break(
                            shift_id=st.session_state.shift_id,
                            session=session,
                        )
                        st.rerun()
                # need option to end shift
            elif user_shift_today.status == "on break":
                st.button(label="End My Break", use_container_width=True)

        else:
            if st.button(label="Start My Shift", use_container_width=True):
                with SessionLocal() as session:
                    start_shift(user_id=st.session_state.user_id, session=session)
                    st.rerun()


# What happens to an ended shift? Do I need a function to resume it?
