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
    UniqueConstraint,
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
    role = Column(String, default="User")

    # Add a constraint to limit the values
    __table_args__ = (
        CheckConstraint("role IN ('User', 'Administrator')", name="check_valid_role"),
    )

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

    __table_args__ = (
        CheckConstraint(
            "status IN ('working', 'on break', 'not working', 'finished working')",
            name="check_valid_status",
        ),
        UniqueConstraint("user_id", "date", name="_user_date_uc"),
    )

    @hybrid_property
    def total_time_worked(self):
        if self.status in ["working", "on break"]:
            current_time = datetime.utcnow()
            # Ensure start_time is not None before calculating the difference
            if self.start_time is not None:
                return current_time - self.start_time
        elif self.status == "finished working":
            # Check both start_time and end_time are not None before subtraction
            if self.start_time is not None and self.end_time is not None:
                return self.end_time - self.start_time
        # If any of the times are None or if the status does not match, return None
        return None

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
    user = relationship("User", back_populates="shifts", cascade="all, delete")


SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")


pool_size = 10  # Maximum number of connections
pool_timeout = 10  # Maximum time to wait for a connection
pool_recycle = 3600  # Maximum age of connections in seconds

# Fix on Heroku which automatically generates the connection string but
# with the wrong format
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgres://", "postgresql://", 1
    )


# Setup the database connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
