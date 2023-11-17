from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import (
    Shift,
    User,
)  # Assuming you have a models.py file with your User and Shift classes
from sqlalchemy import and_

# Initialize your database session
# session = Session()


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


def start_break(user_id: int, session: Session):
    """
    Updates the current shift for the user by setting the status to 'on break' and updating total_worked
    with the time worked since the last status change.
    """
    current_shift = (
        session.query(Shift)
        .filter(
            and_(
                Shift.user_id == user_id,
                Shift.end_time.is_(None),
                Shift.date == datetime.utcnow().date(),
            )
        )
        .one_or_none()
    )

    if current_shift and current_shift.status == "working":
        # Calculate the time worked since the last status change
        worked_time = datetime.utcnow() - current_shift.start_time
        if current_shift.total_worked:
            current_shift.total_worked += worked_time
        else:
            current_shift.total_worked = worked_time
        current_shift.status = "on break"
        session.commit()


def end_break(user_id: int, session: Session):
    """
    Updates the current shift for the user by setting the status to 'working' and updating total_break
    with the time spent on break since the last status change.
    """
    current_shift = (
        session.query(Shift)
        .filter(
            and_(
                Shift.user_id == user_id,
                Shift.end_time.is_(None),
                Shift.date == datetime.utcnow().date(),
            )
        )
        .one_or_none()
    )

    if current_shift and current_shift.status == "on break":
        # Calculate the break time
        break_time = datetime.utcnow() - (
            current_shift.start_time + current_shift.total_worked
        )
        if current_shift.total_break:
            current_shift.total_break += break_time
        else:
            current_shift.total_break = break_time
        current_shift.status = "working"
        session.commit()


def end_shift(user_id: int, session: Session):
    """
    Updates the current shift for the user by setting the status to 'not working', the end time to the current time,
    and updates total_worked with the time worked since the last status change if the user is coming off a break.
    """
    current_shift = (
        session.query(Shift)
        .filter(
            and_(
                Shift.user_id == user_id,
                Shift.end_time.is_(None),
                Shift.date == datetime.utcnow().date(),
            )
        )
        .one_or_none()
    )

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
