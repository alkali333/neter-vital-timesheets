import streamlit as st
from app.models import User, SessionLocal

with SessionLocal() as session:
    users = session.query(User).all()

name_dict = {user.user_id: user.name for user in users}

# name_dict = {1: "Jake", 2: "Jim", 3: "Bob"}

with st.form("Test Form"):
    selected_name = st.selectbox(
        "Choose a name",
        options=[None] + list(name_dict.keys()),
        format_func=lambda x: "Choose a name" if x is None else name_dict[x],
    )
    submitted = st.form_submit_button("Go")

    if submitted:
        st.write(f"Id:{selected_name} | Name: {name_dict[selected_name]}")
