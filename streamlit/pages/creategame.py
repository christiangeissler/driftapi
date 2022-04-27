import streamlit as st
from  .session import fetch


def app():
    
    with st.form("my_form"):
        game_id = st.text_input("Game ID", value="Race1", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)
        password = st.text_input("password", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)
        track_id = st.text_input("racetrack", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)

        submitted = st.form_submit_button("Create")

        if submitted:
                body = {
                    "game_id" : game_id,
                    "password_sh3" : password,
                    "track_id" : track_id
                }
                result = fetch(f"http://localhost:8001//manage_game/create", body)
                st.session_state.nextpage = "racedisplay"
                st.session_state.game_id = game_id
                st.experimental_rerun()



    if st.button("Back to Main Menue"):
        st.session_state.nextpage = "main_page"
        st.experimental_rerun()