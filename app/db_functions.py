from datetime import datetime, timedelta
from werkzeug.security import check_password_hash

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
def authenticate(session, table, email: str, password: str) -> bool:
    try:
        user_in_db = session.query(table).filter_by(email=email).one()
        if check_password_hash(user_in_db.password, password):
            return True
    except NoResultFound:
        pass
    return False


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
    Updates the shift with the provided shift_id for the user by setting the status to 'on break'
    and updating total_worked with the time worked since the last status change.
    """
    try:
        # Retrieve the shift with the provided shift_id
        current_shift = session.query(Shift).filter(Shift.shift_id == shift_id).one()

        # Check if the shift is currently working
        if current_shift.status == "working":
            # Calculate the time worked since the last status change
            worked_time = datetime.utcnow() - current_shift.start_time

            # Update total_worked with the time worked
            if current_shift.total_worked:
                current_shift.total_worked += worked_time
            else:
                current_shift.total_worked = worked_time

            # Set the status to 'on break'
            current_shift.status = "on break"

            # Commit the changes to the database
            session.commit()
        else:
            print("The shift is not currently in 'working' status.")
    except NoResultFound:
        # Handle the case where no shift is found with the given shift_id
        print(f"No shift found with shift_id {shift_id}")


def end_break(int, shift_id: int, session: Session):
    """
    Updates the shift with the provided shift_id for the user by setting the status to 'working'
    and updating total_break with the time spent on break since the last status change.
    """
    try:
        # Retrieve the shift with the provided shift_id
        current_shift = session.query(Shift).filter(Shift.shift_id == shift_id).one()

        # Check if the shift is currently on break
        if current_shift.status == "on break":
            # Calculate the break time
            break_time = datetime.utcnow() - (
                current_shift.start_time + current_shift.total_worked
            )

            # Update total_break with the break time
            if current_shift.total_break:
                current_shift.total_break += break_time
            else:
                current_shift.total_break = break_time

            # Set the status to 'working'
            current_shift.status = "working"

            # Commit the changes to the database
            session.commit()
        else:
            print("The shift is not currently in 'on break' status.")
    except NoResultFound:
        # Handle the case where no shift is found with the given shift_id
        print(f"No shift found with shift_id {shift_id}")


def end_shift(shift_id: int, session: Session):
    """
    Updates the current shift for the user by setting the status to 'not working', the end time to the current time,
    and updates total_worked with the time worked since the last status change if the user is coming off a break.
    """

    current_shift = session.query(Shift).filter(Shift.shift_id == shift_id).one()

    if current_shift:
        current_shift.end_time = datetime.utcnow()
        # If the user was on a break, we don't add to total_worked
        if current_shift.status == "working":
            worked_time = current_shift.end_time - (
                current_shift.start_time + current_shift.total_worked
            )
            if current_shift.total_worked:
                current_shift.total_worked += worked_time
            else:
                current_shift.total_worked = worked_time
        current_shift.status = "not working"
        session.commit()

    else:
        print(f"No shift found with shift_id {shift_id}")


def resume_shift(shift_id: int, session: Session):
    """
    Allows a worker to resume a shift if it was ended prematurely by using the shift_id.
    """
    try:
        # Retrieve the shift with the provided shift_id
        current_shift = session.query(Shift).filter(Shift.shift_id == shift_id).one()

        # Check if the shift is marked as 'not working' and the end time is today
        if (
            current_shift.status == "not working"
            and current_shift.end_time
            and current_shift.end_time.date() == datetime.utcnow().date()
        ):
            # Reset end_time to None and change status back to 'working'
            current_shift.end_time = None
            current_shift.status = "working"
            session.commit()
            return True
        else:
            # If the shift is not marked as 'not working' or the end time is not today, it cannot be resumed
            print(f"The shift with shift_id {shift_id} cannot be resumed.")
    except NoResultFound:
        # Handle the case where no shift is found with the given shift_id
        print(f"No shift found with shift_id {shift_id}")

    return False
