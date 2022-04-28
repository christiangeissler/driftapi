import streamlit as st
import time
from datetime import datetime
import json
from  .session import fetch_post, fetch_put
from .singletons import settings



def app():
    
    with st.form("my_form"):
        game_id = st.text_input("Game ID", value="Race1", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)
        password = st.text_input("password", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)
        track_id = st.text_input("racetrack", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)


        start_time = st.time_input('Start time', value=datetime.now(), key=None, help=None, on_change=None)
        start_time = datetime.combine(datetime.today(), start_time)

        time_limit = st.number_input("time limit[m]", min_value=0, max_value=10000, value=10, step=1, format=None, key=None, help="time limit in minutes", on_change=None)
        lap_count = st.number_input("laps", min_value=0, max_value=100, value=20, step=1, format=None, key=None, help="number of laps", on_change=None)

        submitted = st.form_submit_button("Create")

        if submitted:
                body = {
                    "game_id" : game_id,
                    "password_sh3" : password,
                    "start_time": str(start_time),
                    "track_id" : track_id,
                    "time_limit": str(time_limit),
                    "lap_count": str(lap_count)
                }
                body = {
                    "game_id" : game_id,
                }
                #body = {}
                result = fetch_post(f"{settings.driftapi_rootpath}/manage_game/create", body)
                st.write(result)

                result = fetch_post(f"{settings.driftapi_rootpath}/game/{game_id}/ping",{})
                st.write(result)

                time.sleep(5)
                st.session_state.nextpage = "racedisplay"
                st.session_state.game_id = game_id
                st.experimental_rerun()



    if st.button("Back to Main Menue"):
        st.session_state.nextpage = "main_page"
        st.experimental_rerun()