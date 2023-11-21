import streamlit as st
from datetime import datetime, timezone
import os
from dotenv import find_dotenv
from streamlit_autorefresh import st_autorefresh

from utils import format_timedelta
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

# Initialise state variables that are not set right away
if "user_id" not in st.session_state:
    st.session_state.user_id = None


if "status" not in st.session_state:
    st.session_state.status = "Not started working today"


# callback function so no need for re-run
def logout():
    st.session_state.user_id = None


# Set up an auto-refresh interval of 30 seconds
# This is to keep the work hours updated for working users
refresh_interval_ms = 30 * 1000  # Convert seconds to milliseconds
st_autorefresh(interval=refresh_interval_ms, key="data_refresh")


st.sidebar.image("./images/logo.png", width=222)
# Get the current date and time in UTC
current_utc_datetime = datetime.now(timezone.utc)

formatted_date = current_utc_datetime.strftime("%d %B %Y")

st.header(formatted_date)


# break show time before end
# fix "end my break"


# Callback function for handling login
def handle_login(email, password):
    with SessionLocal() as session:
        authenticated = authenticate(session, User, email, password)

    if authenticated:
        with SessionLocal() as session:
            user_in_db = session.query(User).filter_by(email=email).first()

        st.session_state.user_id = user_in_db.user_id
        st.session_state.user_name = user_in_db.name
        st.rerun()
    else:
        st.sidebar.error("The login details are incorrect")


# Check if the user is not logged in
if not st.session_state.user_id:
    # Use a form for the login inputs and button
    with st.sidebar.form(key="login_form"):
        email = st.text_input("Email", value="jake@alkalimedia.co.uk")
        password = st.text_input(
            "Password", type="password", value=os.getenv("DEBUGGING_PASSWORD")
        )

        # Create a form and use the 'on_click' parameter to specify the callback function
        if st.form_submit_button(label="Login"):
            handle_login(email, password)


else:
    st.sidebar.write(f"Welcome {st.session_state.user_name}")
    status_placeholder = st.sidebar.empty()
    st.sidebar.button(label="Log Out", on_click=logout)

    with SessionLocal() as session:
        # check if there is already a shift today
        user_shift_today = find_shift_for_user_today(
            user_id=st.session_state.user_id, session=session
        )
        if user_shift_today:
            # store the shift ID in a session variable
            st.session_state.shift_id = user_shift_today.shift_id

            status_placeholder.write(f"Status: {user_shift_today.status}")

            st.write(
                f"Time worked today: {format_timedelta(user_shift_today.total_time_worked) or 'None'}"
            )

            # show total break or current break duration depending on if user is on break
            if user_shift_today.status == "on break":
                st.write(
                    f"Current break duration: {format_timedelta(user_shift_today.current_break_duration)}"
                )
            else:
                st.write(
                    f"Break taken today: {format_timedelta(user_shift_today.total_break) or 'None'}"
                )

            if user_shift_today.status == "working":
                if st.button(label="Start My Break", use_container_width=True):
                    with SessionLocal() as session:
                        start_break(
                            shift_id=st.session_state.shift_id,
                            session=session,
                        )
                        st.rerun()
                st.write("\n\n\n\n")
                confirm_end_shift = st.checkbox(
                    "Confirm you want to end your shift and submit your hours for today."
                )
                if st.button(label="End My Shift", use_container_width=True):
                    if confirm_end_shift:
                        with SessionLocal() as session:
                            end_shift(
                                shift_id=st.session_state.shift_id, session=session
                            )
                            st.rerun()
                    else:
                        st.warning(
                            "Please confirm you want to end your shift by ticking the checkbox"
                        )
            elif user_shift_today.status == "on break":
                if st.button(label="End My Break", use_container_width=True):
                    with SessionLocal() as session:
                        end_break(shift_id=st.session_state.shift_id, session=session)
                        st.rerun()
            elif user_shift_today.status == "not working":
                st.write("You have finished your shift today")
                st.write(
                    f"Total payable time:{format_timedelta(user_shift_today.payable_hours)}"
                )
                # if st.button(label="Resume my shift", use_container_width=True):
                #     resume_shift(shift_id=st.session_state.shift_id, session=session)
                #     st.rerun()

        else:
            status_placeholder.write("Your shift has not yet started")
            if st.button(label="Start My Shift", use_container_width=True):
                with SessionLocal() as session:
                    start_shift(user_id=st.session_state.user_id, session=session)
                    st.rerun()


# What happens to an ended shift? Do I need a function to resume it?
