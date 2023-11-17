import streamlit as st
from models import User, Shift

st.set_page_config(
    page_title="Neter Vital Timesheet",
    page_icon=":herb:",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)


st.title("Neter Vital Timesheet")
