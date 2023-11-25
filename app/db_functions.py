from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
import streamlit as st

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func

from models import (
    Shift,
    User,
)  # Assuming you have a models.py file with your User and Shift classes
from sqlalchemy import and_

# Initialize your database session
# session = Session()


# Authenticating user with database
def handle_login(email, password, session):
    try:
        user_in_db = session.query(User).filter_by(email=email).one()
        if check_password_hash(user_in_db.password, password):
            # Authentication successful, handle user role and session state
            current_user_role = user_in_db.role

            st.session_state.is_admin = (
                True if current_user_role == "Administrator" else False
            )
            st.session_state.user_id = user_in_db.user_id
            st.session_state.user_name = user_in_db.name
            st.rerun()
        else:
            # Authentication failed
            st.sidebar.error("The login details are incorrect")
    except NoResultFound:
        # User not found
        st.sidebar.error("The login details are incorrect")


def find_shift_for_user_today(user_id: int, session: Session):
    # Get the current date, with the time set to midnight
    today = datetime.utcnow().date()

    # Query for existing shifts for the user that start today
    existing_shift = (
        session.query(Shift)
        .filter(
            Shift.user_id == user_id,
            func.date(Shift.date)
            == today,  # Extracting and comparing only the date part of the datetime
        )
        .first()
    )  # Using first() will return the first match or None if there is no match

    return existing_shift


def start_shift(user_id: int, session: Session):
    """
    Creates a new shift entry for the user with the current time as the start time and sets the status to 'working'.
    """
    if find_shift_for_user_today(user_id=user_id, session=session):
        raise ValueError(
            f"Cannot create shift: shift already exists for user: {user_id} on {datetime.utcnow().date()} "
        )

    new_shift = Shift(
        user_id=user_id,
        date=datetime.utcnow().date(),
        start_time=datetime.utcnow(),
        status="working",
    )
    session.add(new_shift)
    session.commit()


def start_break(shift_id: int, session: Session):
    """
    Sets the break to start at the current time, and updates the status to 'on break'
    """
    try:
        # Retrieve the shift with the provided shift_id
        current_shift = session.query(Shift).filter(Shift.shift_id == shift_id).one()

        if current_shift.status != "working":
            raise ValueError("Shift must be in 'working' state to start a break.")

        # Record the break start time and update the status
        current_shift.current_break_start = datetime.now()
        current_shift.status = "on break"
        session.commit()

    except NoResultFound:
        raise ValueError(f"No shift found with shift_id {shift_id}")
    except ValueError as ve:
        print(str(ve))


def end_break(shift_id: int, session: Session):
    """
    Ends the break for the shift with the provided shift_id by calculating the break duration,
    updating the total break duration, and setting the status back to 'working'.
    """
    try:
        # Retrieve the shift with the provided shift_id
        shift = session.query(Shift).filter(Shift.shift_id == shift_id).one()

        if shift.status != "on break":
            raise ValueError("Shift is not currently on break.")

        # Calculate the break duration
        break_duration = datetime.now() - shift.current_break_start
        # If total_break is None, initialize it as 0 timedelta
        if shift.total_break is None:
            shift.total_break = timedelta(0)
        # Add the break duration to the total
        shift.total_break += break_duration
        # Reset the current break start time and update the status
        shift.current_break_start = None
        shift.status = "working"
        session.commit()

    except NoResultFound:
        raise ValueError(f"No shift found with shift_id {shift_id}")
    except ValueError as ve:
        print(str(ve))


def end_shift(session, shift_id):
    try:
        # Attempt to retrieve the shift instance by its ID
        shift = session.query(Shift).filter_by(shift_id=shift_id).one()

        # Check if the shift is currently "working"
        if shift.status != "working":
            raise Exception(f"Shift with ID {shift_id} is not in a 'working' status.")

        # Get the current time
        current_time = datetime.now()

        # Update the shift instance
        shift.end_time = current_time
        shift.status = "finished working"

        # Commit the changes to the database
        session.commit()

    except NoResultFound:
        print(f"No shift found with ID {shift_id}.")


def create_default_user(session):
    # Check if the user with ID 1 exists
    user_with_id_1 = session.query(User).filter_by(user_id=1).first()

    if user_with_id_1 is None:
        # If default user doesn't exist, insert it
        new_user = User(
            user_id=1,
            name="Jake",
            email="jake@alkalimedia.co.uk",
            password="pbkdf2:sha256:600000$HfEqpWbeavZrTMNl$9d7177999ac36590ea40c868699a8a972315806961c68610950a4fa9ab540028",
        )
        # Add the new user to the session
        session.add(new_user)
        # Commit the changes to the database
        session.commit()
