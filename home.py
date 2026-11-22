import streamlit as st

from backend.models import User
from backend.service import LostFoundService
from backend.ui import apply_styles


apply_styles()
service = LostFoundService()

st.markdown("""
<section class="home-hero">
  <div class="hero-mark">🔎</div>
  <div class="brand">Campus Lost &amp; Found</div>
  <div class="brand-sub">A shared place to reunite people with their belongings</div>
</section>
""", unsafe_allow_html=True)

action_left, action_right = st.columns([1, 1])
with action_left:
    if st.button("＋ Report an Item", type="primary", use_container_width=True):
        st.session_state["show_report"] = not st.session_state.get("show_report", False)
with action_right:
    st.metric("Registered items", service.total_count())

if st.session_state.get("show_report"):
    with st.container(border=True):
        st.subheader("Create a report")
        with st.form("report_form", clear_on_submit=True):
            report_kind = st.radio("Report type", ["Lost", "Found"], horizontal=True)
            left, right = st.columns(2)
            with left:
                title = st.text_input("Item name")
                location = st.text_input("Last seen / found at")
                reporter_name = st.text_input("Your name")
            with right:
                description = st.text_area("Description", height=120)
                contact = st.text_input("College email or contact")
            submitted = st.form_submit_button("Submit report", type="primary")
            if submitted:
                try:
                    user = User(reporter_name, contact)
                    item_id = service.report_item(report_kind, title, description, location, contact, user.display_name())
                    st.success(f"Report submitted. Item ID: {item_id}")
                    st.session_state["show_report"] = False
                    st.rerun()
                except Exception as error:
                    st.error(str(error))

with st.container(border=True):
    st.subheader("Description")
    st.write("Welcome to the campus lost and found. Report a lost belonging, register an item you found, or use the sidebar to search and browse campus reports.")
