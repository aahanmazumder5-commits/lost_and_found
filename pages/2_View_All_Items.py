import streamlit as st

from backend.service import LostFoundService
from backend.ui import apply_styles, render_item_cards


apply_styles()

st.title("📋 View All Items")
st.write("Browse all campus reports and filter them by type or status.")
left, right = st.columns(2)
with left:
    kind = st.selectbox("Report type", ["All", "Lost", "Found"])
with right:
    status = st.selectbox("Status", ["All", "Open", "Resolved"])

items = LostFoundService().list_items(kind=kind, status=status)
st.subheader(f"{len(items)} registered item{'s' if len(items) != 1 else ''}")
render_item_cards(items)
