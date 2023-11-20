import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import User, Shift, SessionLocal

# Display the admin interface
st.title("Admin Dashboard")

# Week selector
selected_week = st.date_input("Select the week", datetime.today())
start_of_week = selected_week - timedelta(days=selected_week.weekday())  # Monday
end_of_week = start_of_week + timedelta(days=6)  # Sunday

# Query for shifts in the selected week
with SessionLocal() as db_session:
    shifts_in_week = (
        db_session.query(Shift)
        .filter(Shift.date >= start_of_week, Shift.date <= end_of_week)
        .join(User)
        .order_by(Shift.date, Shift.start_time)
        .all()
    )

    # Create a list of dictionaries, each representing a row in the DataFrame
    shifts_data = []
    for shift in shifts_in_week:
        shifts_data.append(
            {
                "User": shift.user.name,
                "Date": shift.date,
                "Start": shift.start_time,
                "End": shift.end_time,
                "Status": shift.status,
                "Total Hours": shift.total_time_worked.total_seconds() / 3600
                if shift.total_time_worked
                else None,  # Convert Duration to hours
                "Total Break": shift.total_break.total_seconds() / 3600
                if shift.total_break
                else None,  # Convert Duration to hours
                "Total Payable Hours": shift.payable_hours.total_seconds() / 3600
                if shift.payable_hours
                else None,  # Convert Duration to hours
            }
        )

    # Create a DataFrame from the list of dictionaries
    shifts_df = pd.DataFrame(shifts_data)

    # Display the DataFrame as a table in Streamlit
    st.table(shifts_df)
