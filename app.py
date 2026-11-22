import streamlit as st

from backend.ui import apply_styles


st.set_page_config(page_title="Campus Lost & Found", page_icon="🔎", layout="wide")
apply_styles()

pages = [
    st.Page("home.py", title="Home", icon="🏠", default=True),
    st.Page("pages/1_Find_an_Item.py", title="Find an Item", icon="🔍"),
    st.Page("pages/2_View_All_Items.py", title="View All Items", icon="📋"),
]
navigation = st.navigation(pages)
navigation.run()
