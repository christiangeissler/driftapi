import streamlit as st
import pandas as pd 
from  .session import fetch_post, fetch_put
from .singletons import settings


def app():
    
    #st.markdown("## Main Page")
    if 'game_id' in st.session_state:
        del st.session_state.game_id

    if st.button("Create New Game"):
        st.session_state.nextpage = "create_game"
        st.experimental_rerun()

    if st.button("Show Game"):
        st.session_state.nextpage = "racedisplay"
        st.experimental_rerun()

    st.write("Available games:")
    result = fetch_post(f"{settings.driftapi_path}/manage_game/find/", {})
    if result:
        result = pd.DataFrame( [{"game_id":r["game_id"]} for r in result if ("game_id" in r.keys())] )
        st.write(result)