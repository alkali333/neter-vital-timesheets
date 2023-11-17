import streamlit as st
from datetime import datetime, timezone
import os
from dotenv import find_dotenv

from utils import format_timedelta, calculate_hours_worked
from models import User, Shift, SessionLocal
from db_functions import (
    authenticate,
    find_shift_for_user_today,
    start_shift,
    start_break,
    end_break,
    end_shift,
    resume_shift,
)

find_dotenv()


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
    password = st.sidebar.text_input(
        "Password", type="password", value=os.getenv("DEBUGGING_PASSWORD")
    )

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
            st.sidebar.write("The login details are incorrect")

else:
    st.write(f"Welcome {st.session_state.user_name}")

    with SessionLocal() as session:
        user_shift_today = find_shift_for_user_today(
            user_id=st.session_state.user_id, session=session
        )
        if user_shift_today:
            # store the shift ID in a session variable
            st.session_state.shift_id = user_shift_today.shift_id

            st.write(f"Status: {user_shift_today.status}")

            # if they are not currently working, get the total from the db
            if user_shift_today == "not working":
                hours_worked = user_shift_today.total_worked
            # if they are working, use the current time
            else:
                hours_worked = calculate_hours_worked(user_shift_today.start_time)

            st.write(f"Time worked today: {format_timedelta(hours_worked)}")
            st.write(
                f"Break taken today: {format_timedelta(user_shift_today.total_break)}"
            )
            if user_shift_today.status == "working":
                if st.button(label="Start My Break", use_container_width=True):
                    with SessionLocal() as session:
                        start_break(
                            shift_id=st.session_state.shift_id,
                            session=session,
                        )
                        st.rerun()
                if st.button(label="End My Shift", use_container_width=True):
                    with SessionLocal() as session:
                        end_shift(shift_id=st.session_state.shift_id, session=session)
                        st.rerun()
            elif user_shift_today.status == "on break":
                if st.button(label="End My Break", use_container_width=True):
                    with SessionLocal() as session:
                        end_break(shift_id=st.session_state.shift_id, session=session)
                        st.rerun()
            elif user_shift_today.status == "not working":
                st.write("You have finished your shift today")
                if st.button(label="Resume my shift", use_container_width=True):
                    resume_shift(shift_id=st.session_state.shift_id, session=session)
                    st.rerun()

        else:
            if st.button(label="Start My Shift", use_container_width=True):
                with SessionLocal() as session:
                    start_shift(user_id=st.session_state.user_id, session=session)
                    st.rerun()


# What happens to an ended shift? Do I need a function to resume it?
