import streamlit as st
from datetime import timedelta
from models import (
    User,
    Shift,
    SessionLocal,
)  # Replace 'your_model_file' with the actual name of the file containing your SQLAlchemy models.
import pandas as pd


st.title("Shifts Admin Screen")

# Dropdown to select a user
with SessionLocal() as session:
    users = session.query(User).all()
user_id_name_dict = {user.user_id: user.name for user in users}
selected_user_id = st.selectbox(
    "Select a user",
    options=list(user_id_name_dict.keys()),
    format_func=lambda x: user_id_name_dict[x],
)

# Button to show shifts
if st.button("Show Shifts"):
    with SessionLocal() as session:
        shifts = (
            session.query(Shift)
            .filter(Shift.user_id == selected_user_id)
            .order_by(Shift.date.desc(), Shift.start_time.desc())
            .limit(7)  # show the last week only
            .all()
        )
        for shift in shifts:
            with st.form(f"shift_{shift.shift_id}"):
                st.write(f"Shift ID: {shift.shift_id}")
                date = st.date_input("Date", shift.date)
                start_time = st.time_input("Start Time", shift.start_time)
                end_time = st.time_input("End Time", shift.end_time)

                # Create two columns for the total break hours and minutes inputs
                col1, col2 = st.columns(2)
                with col1:
                    total_break_hours = st.number_input(
                        "Total Break Hours",
                        min_value=0,
                        max_value=23,
                        value=shift.total_break.seconds // 3600,
                    )
                with col2:
                    total_break_minutes = st.number_input(
                        "Total Break Minutes",
                        min_value=0,
                        max_value=59,
                        value=(shift.total_break.seconds // 60) % 60,
                        step=1,
                    )

                # Convert the input hours and minutes to a timedelta
                total_break = timedelta(
                    hours=total_break_hours, minutes=total_break_minutes
                )

                status = st.selectbox(
                    "Status",
                    ("working", "on break", "not working"),
                    index=("working", "on break", "not working").index(shift.status),
                )

                if st.form_submit_button("Update Shift"):
                    shift.date = date
                    shift.start_time = start_time
                    shift.end_time = end_time
                    shift.total_break = total_break
                    shift.status = status
                    session.commit()
                    st.success("Shift updated successfully!")
