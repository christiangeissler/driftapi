import streamlit as st

from  .session import fetch_post, fetch_put, fetch_get
from .singletons import settings, logger

def app():

    game_id = None

    with st.form("my_form"):
        result = fetch_post(f"{settings.driftapi_path}/manage_game/find/", {})
        if result:
            result = [r["game_id"] for r in result if ("game_id" in r.keys())]
            game_id = st.selectbox(label="Choose Game for deletion", options=result)
            if st.form_submit_button("Delete"):
                result = fetch_get(f"{settings.driftapi_path}/manage_game/delete/{game_id}")
                st.session_state.game_id = None
                st.session_state.nextpage = "main_page"
                st.experimental_rerun()

    if st.button("Back to Main Menue"):
        st.session_state.nextpage = "main_page"
        st.experimental_rerun()
