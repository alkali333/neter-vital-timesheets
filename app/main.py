import streamlit as st
from datetime import datetime, timezone
import os
from dotenv import find_dotenv
from streamlit_autorefresh import st_autorefresh

from utils import (
    format_timedelta,
    print_session_state,
    get_closest_clock_icon,
    get_spiritual_quote,
)
from init import init_app

from models import User, Shift, SessionLocal
from db_functions import (
    find_shift_for_user_today,
    start_shift,
    start_break,
    end_break,
    end_shift,
    create_default_user,
    handle_login,
)

find_dotenv()


st.set_page_config(
    page_title="Neter Vital Timesheet",
    page_icon=":herb:",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

init_app()

current_datetime = datetime.now()

st.title(f':date: {current_datetime.strftime("%d %B %Y")}')
st.header(get_closest_clock_icon() + current_datetime.strftime("%H:%M"))
st.info(f"Welcome, {st.session_state.user_name or 'Please Log In'}")

# Set up an auto-refresh interval of 30 seconds
# This is to keep the work hours updated for working users
refresh_interval_ms = 30 * 1000  # Convert seconds to milliseconds
st_autorefresh(interval=refresh_interval_ms, key="data_refresh")


with SessionLocal() as session:
    create_default_user(session)

# has the user logged in?
if st.session_state.user_id:
    status_placeholder = st.sidebar.empty()

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
            elif user_shift_today.status == "finished working":
                st.info(
                    f"You have finished your shift today. Total payable time:{format_timedelta(user_shift_today.payable_hours)}"
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


# print_session_state()

st.success(get_spiritual_quote())
