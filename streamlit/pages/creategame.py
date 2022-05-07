import streamlit as st
import time
from datetime import datetime, timezone
import json
from  .session import fetch_post, fetch_put
from .singletons import settings



def app():
    
    with st.form("my_form"):
        game_id = st.text_input("Game ID", value="Race1", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)

        with st.expander("Optional settings", expanded=False):
            #password = st.text_input("password", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)
            track_id = st.text_input("Track name", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)

            with st.container():
                columnLeft, columnRight = st.columns(2)

                with columnLeft:
                    start_time_enabled = st.checkbox("Enable start time", value=False, key=None, help=None, on_change=None)
                with columnRight:
                    start_time = st.time_input('Start time (Local)', value=datetime.now(), key=None, help=None, on_change=None, disabled = False)
                start_time = datetime.combine(datetime.today(), start_time)
                start_time = start_time.astimezone(timezone.utc)

            with st.container():
                columnLeft, columnRight = st.columns(2)
                with columnLeft:
                    time_limit_enabled = st.checkbox("Enable time limit", value=False, key=None, help=None, on_change=None)
                with columnRight:
                    time_limit = st.number_input("time [m]", min_value=0, max_value=10000, value=10, step=1, format=None, key=None, help="time limit in minutes", on_change=None, disabled = False)
            
            with st.container():
                columnLeft, columnRight = st.columns(2)
                with columnLeft:
                    lap_limit_enabled = st.checkbox("Enable lap limit", value=False, key=None, help=None, on_change=None)
                with columnRight:
                    lap_count = st.number_input("laps", min_value=0, max_value=100, value=20, step=1, format=None, key=None, help="number of laps", on_change=None, disabled = False)

        submitted = st.form_submit_button("Create")

        if submitted:
                body = {
                    "game_id" : game_id,
                    
                    "track_id" : track_id,
                }

                if start_time_enabled:
                    body['start_time'] = str(start_time)

                if time_limit_enabled:
                    body['time_limit'] = str(time_limit)

                if lap_limit_enabled:
                    body['lap_count'] = str(lap_count)

                #body = {}
                result = fetch_post(f"{settings.driftapi_path}/manage_game/create", body)
                

                if result:
                    st.success("Race has been created")
                    #st.write(result)


                time.sleep(1)
                st.session_state.nextpage = "racedisplay"
                st.session_state.game_id = game_id
                st.experimental_rerun()



    if st.button("Back to Main Menue"):
        st.session_state.nextpage = "main_page"
        st.experimental_rerun()