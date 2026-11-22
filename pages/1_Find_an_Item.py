import streamlit as st

from backend.service import LostFoundService
from backend.ui import apply_styles, render_item_cards


apply_styles()

st.title("🔍 Find an Item")
st.write("Search lost and found reports by item name, description, or location.")
query = st.text_input("Search items", placeholder="Try: blue backpack, library, keys")
left, middle, right = st.columns([1, 1, 1])
with left:
    kind = st.selectbox("Report type", ["All", "Lost", "Found"])
with middle:
    status = st.selectbox("Status", ["Open", "Resolved", "All"])
with right:
    st.write("")
    st.write("")
    st.caption("Choose filters to narrow your results")

matches = LostFoundService().list_items(kind=kind, status=status, query=query)
st.subheader(f"{len(matches)} matching item{'s' if len(matches) != 1 else ''}")
render_item_cards(matches)
