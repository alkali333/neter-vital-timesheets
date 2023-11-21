import streamlit as st
from datetime import timedelta, timezone, datetime
from models import (
    User,
    Shift,
    SessionLocal,
)  # Assuming your SQLAlchemy models are in models.py

st.title("Shifts Admin Screen")

# Initialize session state variables if they don't exist
if "selected_user_id" not in st.session_state:
    st.session_state["selected_user_id"] = None

if "selected_shift_id" not in st.session_state:
    st.session_state["selected_shift_id"] = None

# Dropdown to select a user
with SessionLocal() as session:
    users = session.query(User).all()
user_id_name_dict = {user.user_id: user.name for user in users}
selected_user_id = st.selectbox(
    "Select a user",
    options=[None] + list(user_id_name_dict.keys()),
    format_func=lambda x: "Select a user" if x is None else user_id_name_dict[x],
)

# Button to confirm user selection and store it in session state
if st.button("Confirm User"):
    st.session_state["selected_user_id"] = selected_user_id
    st.session_state["selected_shift_id"] = None  # Reset shift selection

# Display the selected user
if st.session_state["selected_user_id"]:
    st.write(
        f"User selected: {user_id_name_dict[st.session_state['selected_user_id']]}"
    )

# Dropdown to select a shift after a user has been selected
if st.session_state["selected_user_id"]:
    with SessionLocal() as session:
        recent_shifts = (
            session.query(Shift)
            .filter(Shift.user_id == st.session_state["selected_user_id"])
            .order_by(Shift.date.desc(), Shift.start_time.desc())
            .limit(7)  # show the most recent 7 shifts
            .all()
        )
    shift_id_date_dict = {shift.shift_id: shift.date for shift in recent_shifts}
    selected_shift_id = st.selectbox(
        "Select a shift",
        options=[None] + list(shift_id_date_dict.keys()),
        format_func=lambda x: "Select a shift"
        if x is None
        else shift_id_date_dict[x].strftime("%Y-%m-%d %H:%M"),
    )

    # Button to confirm shift selection and store it in session state
    if st.button("Confirm Shift"):
        st.session_state["selected_shift_id"] = selected_shift_id

# Form to edit the selected shift
if st.session_state["selected_shift_id"]:
    with SessionLocal() as session:
        shift_to_edit = session.query(Shift).get(st.session_state["selected_shift_id"])
        with st.form(f"shift_{shift_to_edit.shift_id}"):
            date = st.date_input("Date", shift_to_edit.date)
            start_time = st.time_input("Start Time", shift_to_edit.start_time)
            end_time = st.time_input("End Time", shift_to_edit.end_time)

            # Create two columns for the total break hours and minutes inputs
            col1, col2 = st.columns(2)
            with col1:
                total_break_hours = st.number_input(
                    "Total Break Hours",
                    min_value=0,
                    max_value=23,
                    value=shift_to_edit.total_break.seconds // 3600,
                )
            with col2:
                total_break_minutes = st.number_input(
                    "Total Break Minutes",
                    min_value=0,
                    max_value=59,
                    value=(shift_to_edit.total_break.seconds // 60) % 60,
                    step=1,
                )

            # Convert the input hours and minutes to a timedelta
            total_break = timedelta(
                hours=total_break_hours, minutes=total_break_minutes
            )

            status = st.selectbox(
                "Status",
                ("working", "on break", "not working"),
                index=("working", "on break", "not working").index(
                    shift_to_edit.status
                ),
            )

            if st.form_submit_button("Update Shift"):
                # You can adjust the timezone offset as needed, here using UTC/GMT
                timezone_utc = timezone(timedelta(hours=0))

                # Combine date and time to create datetime objects with timezone information
                start_datetime = datetime.combine(date, start_time).replace(
                    tzinfo=timezone_utc
                )
                end_datetime = datetime.combine(date, end_time).replace(
                    tzinfo=timezone_utc
                )

                shift_to_edit.date = date
                shift_to_edit.start_time = start_time
                shift_to_edit.end_time = end_time
                shift_to_edit.total_break = total_break
                shift_to_edit.status = status
                session.commit()
                st.success("Shift updated successfully!")
