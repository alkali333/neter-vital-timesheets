import streamlit as st
from datetime import timedelta
from sqlalchemy import create_engine
from models import (
    User,
    Shift,
    SessionLocal,
)  # Replace 'your_model_file' with the actual name of the file containing your SQLAlchemy models.
import pandas as pd


def main():
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
                .limit(5)
                .all()
            )
            for shift in shifts:
                with st.form(f"shift_{shift.shift_id}"):
                    st.write(f"Shift ID: {shift.shift_id}")
                    date = st.date_input("Date", shift.date)
                    start_time = st.time_input("Start Time", shift.start_time)
                    end_time = st.time_input("End Time", shift.end_time)
                    total_break = st.time_input(
                        "Total Break",
                        value=(shift.total_break or timedelta()),
                        format="HH:mm",
                    )  # Assuming total_break is of type timedelta
                    status = st.selectbox(
                        "Status",
                        ("working", "on break", "not working"),
                        index=("working", "on break", "not working").index(
                            shift.status
                        ),
                    )
                    submitted = st.form_submit_button("Update Shift")
                    if submitted:
                        shift.date = date
                        shift.start_time = start_time
                        shift.end_time = end_time
                        # Convert total_break from time to timedelta
                        shift.total_break = timedelta(
                            hours=total_break.hour, minutes=total_break.minute
                        )
                        shift.status = status
                        session.commit()
                        st.success("Shift updated successfully!")


if __name__ == "__main__":
    main()
