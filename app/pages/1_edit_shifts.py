import streamlit as st
from datetime import timedelta, datetime

from sqlalchemy.exc import IntegrityError

from init import init_app

from utils import print_session_state
from models import (
    User,
    Shift,
    SessionLocal,
)

init_app()


st.title(":lower_left_fountain_pen: Edit Shifts Manually")

if st.session_state.is_admin == True:
    # Initialize session state variables if they don't exist
    if "selected_user_id" not in st.session_state:
        st.session_state.selected_user_id = None

    if "selected_shift_id" not in st.session_state:
        st.session_state.selected_shift_id = None

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
        st.session_state.selected_user_id = selected_user_id
        st.session_state.selected_shift_id = None  # Reset shift selection
        st.session_state.selected_user_name = user_id_name_dict.get(
            selected_user_id, None
        )

    # Display the selected user
    if st.session_state["selected_user_id"]:
        st.info(
            f"User selected: {user_id_name_dict[st.session_state.selected_user_id]}"
        )
        if st.session_state.selected_shift_id is None:
            with st.form("new_shift_form"):
                # British date format applied to the date picker
                new_shift_date = st.date_input("New Shift Date", format="DD/MM/YYYY")
                create_shift_button = st.form_submit_button("Create New Shift")

            if create_shift_button:
                with SessionLocal() as session:
                    new_shift = Shift(
                        user_id=st.session_state.selected_user_id,
                        date=new_shift_date,
                        status="working",
                        # Add other fields as necessary, e.g. start_time, end_time, total_break
                    )
                    try:
                        session.add(new_shift)
                        session.commit()
                        st.success(
                            f"Shift on {new_shift_date.strftime('%d/%m/%Y')} created successfully for user {user_id_name_dict[st.session_state.selected_user_id]}"
                        )
                    except IntegrityError:
                        st.error(
                            f"A shift for user {user_id_name_dict[st.session_state.selected_user_id]} on {new_shift_date.strftime('%d/%m/%Y')} already exists."
                        )
            session.rollback()  # Roll back the session to a clean state

    # Dropdown to select a shift after a user has been selected
    if st.session_state.selected_user_id:
        with SessionLocal() as session:
            recent_shifts = (
                session.query(Shift)
                .filter(Shift.user_id == st.session_state.selected_user_id)
                .order_by(Shift.date.desc(), Shift.start_time.desc())
                .limit(14)  # show the most recent 14 shifts
                .all()
            )
        shift_id_date_dict = {shift.shift_id: shift.date for shift in recent_shifts}
        selected_shift_id = st.selectbox(
            "Edit existing shift",
            options=[None] + list(shift_id_date_dict.keys()),
            format_func=lambda x: "Select shift"
            if x is None
            else shift_id_date_dict[x].strftime("%a %d/%m/%y"),  # British date format
        )

        # Button to confirm shift selection and store it in session state
        if st.button("Edit Shift"):
            st.session_state.selected_shift_id = selected_shift_id
            st.rerun()

    # Form to edit the selected shift
    if st.session_state.selected_shift_id:
        with SessionLocal() as session:
            shift_to_edit = session.get(Shift, st.session_state.selected_shift_id)

            st.info(
                f"Editing Shift for {st.session_state.selected_user_name} on {shift_to_edit.date.strftime('%d/%m/%Y')}",  # British date format
                icon="📅",
            )

            with st.form(f"shift_{shift_to_edit.shift_id}"):
                # British date format applied to the date picker
                date = st.date_input(
                    "Date", shift_to_edit.date, format="DD/MM/YYYY", disabled=True
                )
                start_time = st.time_input(
                    "Start Time",
                    value=shift_to_edit.start_time,
                    step=timedelta(minutes=15),
                )
                end_time = st.time_input(
                    "End Time", value=shift_to_edit.end_time, step=timedelta(minutes=15)
                )
                break_hours = (
                    int(shift_to_edit.total_break.total_seconds() // 3600)
                    if shift_to_edit.total_break
                    else 0
                )
                break_minutes = (
                    int((shift_to_edit.total_break.total_seconds() % 3600) // 60)
                    if shift_to_edit.total_break
                    else 0
                )

                col1, col2 = st.columns(2)
                with col1:
                    total_break_hours = st.number_input(
                        "Total Break Hours",
                        min_value=0,
                        max_value=23,
                        value=break_hours,
                    )
                with col2:
                    total_break_minutes = st.number_input(
                        "Total Break Minutes",
                        min_value=0,
                        max_value=59,
                        value=break_minutes,
                        step=1,
                    )

                status = st.selectbox(
                    "Status",
                    ("working", "on break", "finished working"),
                    index=("working", "on break", "finished working").index(
                        shift_to_edit.status
                    ),
                )

                if st.form_submit_button("Update Shift"):
                    start_datetime = (
                        datetime.combine(date, start_time) if start_time else None
                    )
                    end_datetime = (
                        datetime.combine(date, end_time) if end_time else None
                    )
                    total_break = timedelta(
                        hours=total_break_hours, minutes=total_break_minutes
                    )
                    shift_to_edit.start_time = start_datetime
                    shift_to_edit.end_time = end_datetime
                    shift_to_edit.total_break = total_break
                    shift_to_edit.status = status
                    session.commit()
                    st.success("Shift updated successfully!")

else:
    st.warning("Only an administrator can view this page")


# print_session_state()
