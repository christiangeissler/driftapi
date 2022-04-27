import streamlit as st
from  .session import fetch
import time
import pandas as pd 
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


def app():

    if st.button("Back to Main Menue"):
        st.session_state.nextpage = "main_page"
        st.experimental_rerun()

    game_id = ""

    if 'game_id' in st.session_state:
        game_id = st.session_state.game_id
    else:
        with st.form("my_form"):
            game_id = st.text_input("Game ID", value="Race1", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)
            submitted = st.form_submit_button("Show Scoreboard")

            if submitted:
                st.session_state.game_id = game_id


    future = st.empty()

    while True:
        body = {}
        result = fetch(f"http://localhost:8001/game/{game_id}", body)
        if result:
            with future.container():
                toBeDisplayedData = pd.DataFrame( [{"username":r["user_name"], "best lap":r["best_lap"], "laps":r["laps_completed"]} for r in result if ("user_name" in r.keys())] )
                st.dataframe(toBeDisplayedData)
        else:
            st.error("Error")
        time.sleep(5)



