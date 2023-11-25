import streamlit as st
from app.models import User, SessionLocal
from datetime import datetime, timedelta
import pytz
import os

from dotenv import load_dotenv

from app.utils import get_today

with SessionLocal() as session:
    users = session.query(User).all()

name_dict = {user.user_id: user.name for user in users}

# name_dict = {1: "Jake", 2: "Jim", 3: "Bob"}

with st.form("Test Form"):
    selected_name = st.selectbox(
        "Choose a name",
        options=[None] + list(name_dict.keys()),
        format_func=lambda x: "Choose a name" if x is None else name_dict[x],
    )

    start_date, end_date = st.date_input(
        "Choose start and end dates",
        (datetime.today(), datetime.today() + timedelta(days=6)),
    )

    submitted = st.form_submit_button("Go")

    if submitted:
        st.write(f"Id:{selected_name} | Name: {name_dict[selected_name]}")

        st.write(f"Start: {start_date}, End: {end_date}")


tz_now = get_today()

st.write(f'The time is {tz_now.strftime("%H:%M")}')
