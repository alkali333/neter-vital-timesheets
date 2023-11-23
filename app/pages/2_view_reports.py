import streamlit as st

import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.orm import Session


from utils import print_session_state, format_timedelta
from models import User, Shift, SessionLocal


if st.session_state.is_admin:
    # Display the admin interface
    st.title("Display Shifts")

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
                    "Total Time Worked": format_timedelta(shift.total_time_worked),
                    "Break Taken": format_timedelta(shift.total_break),
                    "Payable Hours": format_timedelta(shift.payable_hours),
                }
            )

        # Create a DataFrame from the list of dictionaries
        shifts_df = pd.DataFrame(shifts_data)

        # Display the DataFrame as a table in Streamlit
        st.table(shifts_df)


else:
    "Only the administrator can view this page"


print_session_state()
