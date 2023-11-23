import streamlit as st
from utils import print_session_state

if "admin_type" not in st.session_state:
    st.session_state.admin_type = None


def go_back():
    st.session_state.admin_type = None


if st.session_state.is_admin == True:
    st.write("View Reports")
else:
    "Only the administrator can view this page"


print_session_state()
