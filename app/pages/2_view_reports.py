import streamlit as st

import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from utils import print_session_state, format_timedelta, timedelta_to_time_string
from init import init_app
from models import User, Shift, SessionLocal

init_app()

st.title(":calendar: View Shift Reports")

if st.session_state.is_admin:
    with st.form(key="my_form"):
        # British date format applied to the date picker
        start_date, end_date = st.date_input(
            "Choose start and end dates",
            (datetime.today(), datetime.today() + timedelta(days=6)),
            format="DD/MM/YYYY",  # Modified to British date format
        )

        # Dropdown to select a user
        with SessionLocal() as session:
            users = session.query(User).all()
            user_id_name_dict = {user.user_id: user.name for user in users}
            selected_user_id = st.selectbox(
                "Select a user",
                options=[None] + list(user_id_name_dict.keys()),
                format_func=lambda x: "Select a user"
                if x is None
                else user_id_name_dict[x],
            )

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")

        if submitted:
            with SessionLocal() as db_session:
                query = db_session.query(Shift).filter(
                    Shift.date >= start_date, Shift.date <= end_date
                )

                if selected_user_id is not None:
                    query = query.filter(Shift.user_id == selected_user_id)

                query = query.join(User).order_by(Shift.date, Shift.start_time)

                shifts_in_week = query.all()

                if shifts_in_week:
                    shifts_data = []
                    total_payable_hours = timedelta()
                    for shift in shifts_in_week:
                        total_payable_hours += shift.payable_hours
                        shifts_data.append(
                            {
                                "User": shift.user.name,
                                # Date formatted to British date style
                                "Date": shift.date.strftime("%d/%m/%Y"),
                                "Start": shift.start_time.strftime("%H:%M"),
                                "End": shift.end_time.strftime("%H:%M"),
                                "Status": shift.status,
                                "Total Time:": format_timedelta(
                                    shift.total_time_worked
                                ),
                                "Break": format_timedelta(shift.total_break),
                                "Payable Hours": format_timedelta(shift.payable_hours),
                            }
                        )

                    shifts_df = pd.DataFrame(shifts_data)
                    st.table(shifts_df.set_index("User"))

                    st.info(
                        f"""
                            {format_timedelta(total_payable_hours)} Total Payable Hours for 
                            {start_date.strftime("%d/%m/%Y")} - {end_date.strftime("%d/%m/%Y")}
                         """
                    )
                else:
                    st.write("No shifts for selected dates")

else:
    st.warning("Only an administrator can view this page")

# print_session_state()
