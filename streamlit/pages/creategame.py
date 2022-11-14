import streamlit as st
from zoneinfo import ZoneInfo #to set the timezone to german time
from enum import Enum
from datetime import datetime, timezone, timedelta
import random
from  .session import fetch_post, fetch_put
from .singletons import settings, logger
from .model import track_condition, track_bundle, wheels, setup_mode, target_code


def createGameOptionContainer(label:str, options:Enum):
    with st.container():
        columnLeft, columnRight = st.columns(2)
        with columnLeft:
            enabled = st.checkbox("Enable "+label, value=False, key=None, help=None, on_change=None)
        with columnRight:
            selected = st.selectbox(label=label, options=[e.value for e in options])
        if enabled:
            return {label:selected}
        else:
            return {}
        

def app():
    
    with st.form("my_form", clear_on_submit=True):
        gameOptions = {}
        game_id = st.text_input("Game ID", value="Race1", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)

        with st.expander("Optional settings", expanded=False):
            #password = st.text_input("password", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)
            track_id = st.text_input("Track name", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)

            with st.container():
                columnLeft, columnRight = st.columns(2)

                with columnLeft:
                    start_time_enabled = st.checkbox("Enable start time", value=False, key=None, help=None, on_change=None)
                with columnRight:
     
                    time1 = datetime.now(tz=ZoneInfo("Europe/Berlin"))
                    timedelta_1 = time1.utcoffset()
                    start_time = st.time_input('Start time (Local)', value=datetime.now(tz=ZoneInfo("Europe/Berlin")), key=None, help=None, on_change=None, disabled = False)
                    start_time = datetime.combine(datetime.today(), start_time)-timedelta_1
                    start_time = start_time.astimezone(timezone.utc)

            with st.container():
                columnLeft, columnRight = st.columns(2)
                with columnLeft:
                    enable_start_delay = st.checkbox("Enable random start delay", value=False, key=None, help="Enable a random delay of 1-3 seconds between the yellow and green light", on_change=None)

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

            with st.container():
                columnLeft, columnRight = st.columns(2)
                with columnLeft:
                   track_condition_enabled = st.checkbox("Enable track condition", value=False, key=None, help=None, on_change=None)
                with columnRight:
                   track_condition_selected = st.selectbox(label="track condition", options=[e.value for e in track_condition])

            with st.container():
                columnLeft, columnRight = st.columns(2)
                with columnLeft:
                    track_bundle_enabled = st.checkbox("Enable track bundle", value=False, key=None, help=None, on_change=None)
                with columnRight:
                    track_bundle_selected = st.selectbox(label="track bundle", options=[e.value for e in track_bundle])

            with st.container():
                columnLeft, columnRight = st.columns(2)
                with columnLeft:
                    wheels_enabled = st.checkbox("Enable wheels", value=False, key=None, help=None, on_change=None)
                with columnRight:
                    wheels_selected = st.selectbox(label="wheels", options=[e.value for e in wheels])

            with st.container():
                columnLeft, columnRight = st.columns(2)
                with columnLeft:
                    setup_mode_enabled = st.checkbox("Enable setup mode", value=False, key=None, help=None, on_change=None)
                with columnRight:
                    setup_mode_selected = st.selectbox(label="setup mode", options=[e.value for e in setup_mode])

            with st.container():
                columnLeft, columnRight = st.columns(2)
                with columnLeft:
                    joker_lap_enabled = st.checkbox("Enable Joker Lap Counter", value=False, key=None, help=None, on_change=None)
                    joker_lap_precondition_enabled = st.checkbox("Enable precondition", value=False, key=None, help="when a precondition code is set, the actual joker lap code is only counted when the racer deceted the precondition code right before the joker lap code.", on_change=None)
                with columnRight:
                    options = {"start/finish":target_code.start_finish, "angle drift":target_code.angle_drift, "360":target_code.threesixty, "180 speed":target_code.oneeighty, "speed drift":target_code.speed_drift}
                    joker_lap_code = str(options[st.selectbox(label="Code to be used for joker lap", options=[*options])].value)
                    joker_lap_precondition_code = str(options[st.selectbox(label="Additional code that need to be detected before the actual joker lap code", options=[*options], index=1)].value)


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

                if enable_start_delay:
                    body['start_delay'] = random.uniform(0,2)

                if lap_limit_enabled:
                    body['lap_count'] = str(lap_count)

                if track_condition_enabled:
                    body['track_condition'] = str(track_condition_selected)

                if track_bundle_enabled:
                    body['track_bundle'] = str(track_bundle_selected)

                if wheels_enabled:
                    body['wheels'] = str(wheels_selected)

                if setup_mode_enabled:
                    body['setup_mode'] = str(setup_mode_selected)


                if joker_lap_enabled:
                    body['joker_lap_code'] = str(joker_lap_code)

                    if joker_lap_precondition_enabled:
                        body['joker_lap_precondition_code'] = str(joker_lap_precondition_code)

                result = fetch_post(f"{settings.driftapi_path}/manage_game/create", body)

                #if result:
                    #st.success("Race has been created")
                    #st.write(result)


                st.session_state.nextpage = "racedisplay"
                st.session_state.game_id = game_id
                st.experimental_rerun()



    if st.button("Back to Main Menue"):
        st.session_state.nextpage = "main_page"
        st.experimental_rerun()