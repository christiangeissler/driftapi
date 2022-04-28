import streamlit as st
import time
import pandas as pd 
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

from  .session import fetch_post, fetch_put
from .singletons import settings



def app():

    if st.button("Back to Main Menue"):
        st.session_state.nextpage = "main_page"
        st.experimental_rerun()

    game_id = ""


    if 'game_id' not in st.session_state:
        with st.form("my_form"):
            result = fetch_post(f"{settings.driftapi_rootpath}/manage_game/find/", {})
            if result:
                result = [r["game_id"] for r in result if ("game_id" in r.keys())]
                game_id = st.selectbox(label="Choose Game", options=result)
                submitted = st.form_submit_button("Show")

                if submitted:
                    st.session_state.game_id = game_id
                    st.experimental_rerun()
    else:
        game_id = st.session_state.game_id

        future = st.empty()

        result = fetch_post(f"{settings.driftapi_rootpath}/game/{game_id}/ping", {})
        
        if result:
            while True:
                result = fetch_put(f"{settings.driftapi_rootpath}/game/{game_id}/", {})
                if result:
                    with future.container():
                        toBeDisplayedData = pd.DataFrame( [{"username":r["user_name"], "best lap":r["best_lap"], "laps":r["laps_completed"]} for r in result if ("user_name" in r.keys())] )
                        st.dataframe(toBeDisplayedData)
                else:
                    with future.container():
                        st.write("Waiting for players to join...")
                        #st.error("Error")
                time.sleep(5)
        else:
            with future.container():
                st.error("No Game with that id exists, going back to main menue...")
                time.sleep(1)
                st.session_state.nextpage = "main_page"
                st.experimental_rerun()



