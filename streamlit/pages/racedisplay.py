import streamlit as st
import time
import base64
from datetime import timedelta
import pandas as pd 
import numpy as np
import qrcode
from PIL import Image
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

from  .session import fetch_post, fetch_put, fetch_get
from .singletons import settings, logger

@st.cache
def getqrcode(content):
    logger.info("create qr code")
    logger.info(content)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="white", back_color="#212529")
    #img = np.asarray(img)
    #logger.info(str(img.shape))
    logger.info(str(img))
    img.save('./qrcode_test.png')
    return Image.open('./qrcode_test.png')


def app():

    if st.button("Back to Main Menue"):
        st.session_state.nextpage = "main_page"
        st.experimental_rerun()

    game_id = ""


    if 'game_id' not in st.session_state:
        with st.form("my_form"):
            result = fetch_post(f"{settings.driftapi_path}/manage_game/find/", {})
            if result:
                result = [r["game_id"] for r in result if ("game_id" in r.keys())]
                game_id = st.selectbox(label="Choose Game", options=result)
                if st.form_submit_button("Show"):
                    st.session_state.game_id = game_id
                    st.experimental_rerun()
    else:
        game_id = st.session_state.game_id
        future = st.empty()

        with st.expander("Game Settings", expanded = False):
            result = fetch_get(f"{settings.driftapi_path}/manage_game/get/{game_id}/")
            st.write(result)
        
        with st.expander("Connection info", expanded=False):
            submitUri:str = settings.hostname+":8001/game"
            st.image(getqrcode(submitUri), clamp=True)
            st.write("URL: "+submitUri)
            st.write("GAME ID: "+game_id)

        result = fetch_get(f"{settings.driftapi_path}/game/{game_id}/ping")
        
        if result:
            while True:
                result = fetch_get(f"{settings.driftapi_path}/game/{game_id}/playerstatus")
                if result:
                    with future.container():
                        #"Targets":str(r["target_code_counter"])
                        toBeDisplayedData = pd.DataFrame( [{"Spieler":r["user_name"], "Beste Runde[s]":r["best_lap"], "Letzte Runde[s]":r["last_lap"], "Runden":r["laps_completed"], "Punkte":r["total_score"], "Gesamtzeit":r["total_time"]} for r in result if (type(r) is dict) and ("user_name" in r.keys())] )
                        st.dataframe(toBeDisplayedData)
                        #AgGrid(toBeDisplayedData)
                else:
                    with future.container():
                        st.write("Waiting for players to join...")
                        #st.error("Error")

                time.sleep(2)
        else:
            with future.container():
                st.error("No Game with that id exists, going back to main menue...")
                time.sleep(1)
                st.session_state.nextpage = "main_page"
                st.experimental_rerun()


