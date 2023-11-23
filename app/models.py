import os
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    Interval,
    CheckConstraint,
)

from sqlalchemy import func, case
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String(length=320), nullable=False, index=True)
    password = Column(String, nullable=False)

    # Relationship to the shifts table
    shifts = relationship("Shift", back_populates="user")


class Shift(Base):
    __tablename__ = "shifts"
    shift_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    date = Column(Date)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    current_break_start = Column(DateTime)
    total_break = Column(Interval)
    status = Column(String, default="not working")

    # Add a constraint to limit the values
    __table_args__ = (
        CheckConstraint(
            status.in_(("working", "on break", "not working", "finished working")),
            name="check_valid_status",
        ),
    )

    @hybrid_property
    def total_time_worked(self):
        if self.status in ["working", "on break"]:
            current_time = datetime.utcnow()
            return current_time - self.start_time
        elif self.status == "not working":
            return (
                self.end_time - self.start_time
                if self.start_time and self.end_time
                else None
            )
        return None

    @total_time_worked.expression
    def total_time_worked(cls):
        current_time_utc = func.timezone("UTC", func.current_timestamp())
        return case(
            [
                (
                    cls.status.in_(["working", "on break"]),
                    current_time_utc - cls.start_time,
                ),
                (cls.status == "not working", cls.end_time - cls.start_time),
            ],
            else_=None,
        )

    @hybrid_property
    def current_break_duration(self):
        if self.status == "on break" and self.current_break_start is not None:
            current_time = datetime.utcnow()
            return current_time - self.current_break_start
        return None

    @hybrid_property
    def payable_hours(self):
        if self.total_time_worked is None:
            return None
        else:
            # If total_break_duration is None, it will default to a timedelta of 0
            total_break_duration = (
                self.total_break if self.total_break is not None else timedelta(0)
            )
            return self.total_time_worked - total_break_duration

    # Relationship to the users table
    user = relationship("User", back_populates="shifts")


if os.environ.get("SSLMODE") == "True":
    SQLALCHEMY_DATABASE_URL = f'postgresql://{os.getenv("DATABASE_USERNAME")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOSTNAME")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}?sslmode=require'
else:
    SQLALCHEMY_DATABASE_URL = f'postgresql://{os.getenv("DATABASE_USERNAME")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOSTNAME")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}'

# debugging
# print(f"Database URL: {SQLALCHEMY_DATABASE_URL}")

# Setup the database connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

with SessionLocal() as session:
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
