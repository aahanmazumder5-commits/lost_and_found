from html import escape

import streamlit as st

from backend.service import LostFoundService


def apply_styles():
    st.markdown("""
    <style>
    .stApp, [data-testid="stAppViewContainer"] { background: #090d1a; color: #f8fafc; }
    .block-container { max-width: 1280px; padding: 1.5rem 2rem 3rem; }
    [data-testid="stHeader"] { background: #090d1a; }
    [data-testid="stSidebar"] { background: #101729; border-right: 1px solid #27334a; }
    [data-testid="stSidebar"] * { color: #f8fafc; }
    [data-testid="stSidebarNav"] { padding: .3rem .25rem; }
    [data-testid="stSidebarNav"]::before { content: "Campus Lost And Found"; display: block; color: #ddd6fe; font-size: 1.15rem; font-weight: 800; line-height: 1.3; padding: .55rem .25rem 1rem; }
    [data-testid="stSidebarNavLink"] { background: #dcd2ff !important; border: 1px solid #c4b5fd !important; border-radius: 12px !important; margin: 0 0 .65rem !important; padding: .72rem .85rem !important; transition: background .15s ease, transform .15s ease; }
    [data-testid="stSidebarNavLink"] * { color: #241744 !important; font-weight: 700 !important; }
    [data-testid="stSidebarNavLink"]:hover { background: #c4b5fd !important; transform: translateX(2px); }
    [data-testid="stSidebarNavLink"][aria-current="page"] { background: #c4b5fd !important; border-color: #a78bfa !important; box-shadow: 0 4px 14px #0003; }
    h1, h2, h3, h4, p, label, span, div, li, [data-testid="stMarkdownContainer"] { color: #f1f5f9; }
    .brand { background: linear-gradient(90deg,#a78bfa,#818cf8); -webkit-background-clip: text; color: transparent; font-weight: 900; font-size: clamp(2rem,5vw,3.2rem); line-height: 1.15; text-align: center; }
    .brand-sub { color: #cbd5e1; font-size: 1.05rem; text-align: center; margin: .7rem 0 1.2rem; }
    .home-hero { background: radial-gradient(ellipse at 50% 0%,#20224c 0%,#11182b 58%,#0d1322 100%); border: 1px solid #2f3d59; border-radius: 24px; padding: 2.4rem 1.5rem 2rem; text-align: center; margin: .5rem 0 1.5rem; box-shadow: 0 20px 65px #0006; }
    .hero-mark { color: #a78bfa; font-size: 2.3rem; }
    .item-title { font-size: 1.2rem; font-weight: 750; color: #fff; margin: .5rem 0; }
    .item-description { color: #dbe2ef; min-height: 48px; }
    .item-meta { color: #cbd5e1; font-size: .9rem; line-height: 1.8; margin-top: .6rem; }
    .tag-lost, .tag-found { color: #fff; font-weight: 750; }
    [data-testid="stVerticalBlockBorderWrapper"] { background: #151d30; border: 1px solid #29364c; border-radius: 16px; box-shadow: 0 10px 25px #0004; }
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stSelectbox"] div[data-baseweb="select"] > div { background: #202a3d; color: #fff; border-color: #475569; }
    [data-baseweb], [data-baseweb] * { color: #fff; }
    input::placeholder, textarea::placeholder { color: #cbd5e1 !important; opacity: 1; }
    [data-baseweb="popover"], [data-baseweb="popover"] > div, [data-baseweb="menu"], [role="listbox"] { background-color: #202a3d !important; color: #fff !important; }
    [data-baseweb="menu"] ul, [data-baseweb="menu"] li, [role="listbox"] [role="option"], [data-testid="stSelectboxVirtualDropdown"] { background-color: #202a3d !important; color: #fff !important; }
    [role="option"] { color: #fff !important; }
    [role="option"]:hover, [role="option"][aria-selected="true"], [role="option"][aria-selected="true"] * { background-color: #514078 !important; color: #fff !important; }
    [data-testid="stAlert"] { background: #17243a; border: 1px solid #334155; }
    [data-testid="stCaptionContainer"] { color: #cbd5e1; }
    div.stButton > button, [data-testid="stFormSubmitButton"] button { border-radius: 10px; min-height: 2.8rem; background: #202a3d; color: #fff; border: 1px solid #475569; }
    div.stButton > button:hover, [data-testid="stFormSubmitButton"] button:hover { border-color: #a78bfa; color: #fff; }
    button[kind="primary"], [data-testid="stFormSubmitButton"] button[kind="primary"] { background: linear-gradient(100deg,#7c3aed,#4f46e5); border: 0; color: white; }
    [data-testid="stExpander"] { background: #111a2c; border: 1px solid #334155; border-radius: 12px; }
    @media (max-width: 700px) { .block-container { padding: 1rem .8rem 2rem; } .home-hero { padding: 1.5rem .8rem; } }
    </style>
    """, unsafe_allow_html=True)


def render_item_cards(items):
    if not items:
        st.info("No items match your search.")
        return
    cards = st.columns(3)
    for index, item in enumerate(items):
        with cards[index % 3]:
            with st.container(border=True):
                status_class = "tag-found" if item["kind"] == "Found" else "tag-lost"
                status_icon = "🟢" if item["kind"] == "Found" else "🟣"
                st.markdown(f'<span class="{status_class}">{status_icon} {item["kind"].upper()}</span>　 ·　 Item #{item["id"]}', unsafe_allow_html=True)
                st.markdown(f'<div class="item-title">{escape(item["title"])}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="item-description">{escape(item["description"])}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="item-meta">📍 {escape(item["location"])}<br>🗓️ {escape(item["created_at"][:10])}<br>Status: {escape(item["status"])}</div>', unsafe_allow_html=True)
                with st.expander("View details / claim"):
                    st.write(f"**Reported by:** {item['reporter']}")
                    st.write(f"**Contact:** {item['contact']}")
                    if item["status"] == "Open":
                        st.caption("Contact the reporter if this is your item, then mark it resolved after it is returned.")
                        with st.form(f"claim_{item['id']}"):
                            claimant = st.text_input("Your name", key=f"claimant_{item['id']}")
                            if st.form_submit_button("Claim / mark returned"):
                                try:
                                    if not claimant.strip():
                                        raise ValueError("Enter your name to claim this item.")
                                    LostFoundService().close_item(item["id"])
                                    st.success("Item marked as resolved.")
                                    st.rerun()
                                except Exception as error:
                                    st.error(str(error))
