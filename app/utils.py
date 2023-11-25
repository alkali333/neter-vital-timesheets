from datetime import timedelta, time
import streamlit as st
from datetime import datetime


# def local_now():
#     timezone = pytz.timezone(os.getenv("TIMEZONE", "UTC"))
#     utc_now = datetime.utcnow()
#     return utc_now.replace(tzinfo=pytz.utc).astimezone(timezone)


def logout():
    st.session_state.user_id = None
    st.session_state.is_admin = False
    st.session_state.user_name = None


def format_timedelta(td):
    if not td:
        return "None"
    total_minutes = td.total_seconds() // 60
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{int(hours)}:{int(minutes)}"


def timedelta_to_time(td):
    seconds = td.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return time(hours, minutes)


def timedelta_to_time_string(td):
    seconds = td.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    # Format the time as a string
    time_string = "{:02d}:{:02d}".format(hours, minutes)

    return time_string


# Function to convert datetime.time to timedelta
def time_to_timedelta(t):
    return timedelta(hours=t.hour, minutes=t.minute)


def print_session_state():
    st.write("\n\n\n\n\n\n")
    st.write("debugging info:")
    session_state_str = " | ".join(
        [f"{key}: {value}" for key, value in st.session_state.items()]
    )
    st.write(session_state_str)
