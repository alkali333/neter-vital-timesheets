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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from dotenv import load_dotenv, find_dotenv

load_dotenv()

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String(length=320), nullable=False)
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
    total_worked = Column(
        Interval
    )  # This can be calculated from start_time and end_time
    total_break = Column(Interval)
    status = Column(String, default="not working")

    # Add a constraint to limit the values
    __table_args__ = (
        CheckConstraint(
            status.in_(("working", "on break", "not working")),
            name="check_valid_status",
        ),
    )

    # Relationship to the users table
    user = relationship("User", back_populates="shifts")


if os.environ.get("SSLMODE") == "True":
    SQLALCHEMY_DATABASE_URL = f'postgresql://{os.getenv("DATABASE_USERNAME")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOSTNAME")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}?sslmode=require'
else:
    SQLALCHEMY_DATABASE_URL = f'postgresql://{os.getenv("DATABASE_USERNAME")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOSTNAME")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}'

# debugging
print(f"Database URL: {SQLALCHEMY_DATABASE_URL}")

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
