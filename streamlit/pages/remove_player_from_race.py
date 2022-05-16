import streamlit as st
import time
import base64
from datetime import timedelta
import pandas as pd 
import numpy as np
from PIL import Image

from  .session import fetch_post, fetch_put, fetch_get
from .singletons import settings, logger

def app():
    game_id = st.session_state.game_id

    with st.form("my_form"):
        result = fetch_get(f"{settings.driftapi_path}/game/{game_id}/playerstatus")
        result = [r["user_name"] for r in result if (type(r) is dict) and ("user_name" in r.keys())]
        player_id = st.selectbox(label="Choose Player", options=result)

        if st.form_submit_button("Delete Selected"):
            result = fetch_get(f"{settings.driftapi_path}/manage_game/reset_player/{game_id}/{player_id}")
            st.session_state.nextpage = "racedisplay"
            st.experimental_rerun()


    if st.button("Back to Race"):
        st.session_state.nextpage = "racedisplay"
        st.experimental_rerun()
