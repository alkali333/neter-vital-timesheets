from datetime import timedelta, time
import streamlit as st


def format_timedelta(td):
    if not td:
        return "None"
    total_minutes = td.total_seconds() // 60
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{int(hours)} hours {int(minutes)} minutes"


def timedelta_to_time(td):
    seconds = td.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return time(hours, minutes)


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
