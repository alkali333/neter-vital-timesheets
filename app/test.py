import streamlit as st
from your_authentication_module import authenticate, SessionLocal, User
import os

# Initialize the session state variables if they are not already set
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
    st.session_state["user_name"] = None

# Sidebar login form
email = st.sidebar.text_input("Email", value="jake@alkalimedia.co.uk")
password = st.sidebar.text_input(
    "Password", type="password", value=os.getenv("DEBUGGING_PASSWORD")
)


# Function to handle login logic
def handle_login():
    with SessionLocal() as session:
        # Authenticate the user
        authenticated = authenticate(session, User, email, password)

        if authenticated:
            user_in_db = session.query(User).filter_by(email=email).first()
            # Update session state
            st.session_state["user_id"] = user_in_db.user_id
            st.session_state["user_name"] = user_in_db.name
            # Display a welcome message
            st.sidebar.success(f"Welcome {user_in_db.name}")
        else:
            st.sidebar.error("The login details are incorrect")


# Button to trigger login
if st.sidebar.button("Login"):
    handle_login()

# Display the appropriate view based on login status
if st.session_state["user_id"] is not None:
    st.write(f"Welcome {st.session_state['user_name']}")
else:
    st.sidebar.write("Please login to continue")


import streamlit as st
import pandas as pd
from models import User, Shift, SessionLocal

# ... [The rest of your code remains the same until the Streamlit interface part] ...

# Streamlit interface
st.title("Working Hours Management")

# Retrieve data
with SessionLocal() as session:
    users, shifts = get_data(session)

users_df, shifts_df = convert_to_dataframe(users, shifts)

# Display the data
st.write("Users")
st.dataframe(users_df)

# Dropdown for selecting a user
user_names = users_df["name"].tolist()
selected_user_name = st.selectbox("Select User", user_names)

# Filter the shifts DataFrame based on the selected user
selected_user_id = users_df.loc[users_df["name"] == selected_user_name, "user_id"].iloc[
    0
]
selected_user_shifts_df = shifts_df[shifts_df["user_id"] == selected_user_id]

st.write(f"Shifts for {selected_user_name}")
st.dataframe(selected_user_shifts_df)

# Dropdown to select shift to edit
shift_id_to_edit = st.selectbox(
    "Select Shift ID to Edit", selected_user_shifts_df["shift_id"]
)

# ... [The rest of your shift editing code remains the same] ...
