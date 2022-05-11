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

    st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {95}%;
        padding-top: {1}rem;
        padding-right: {1}rem;
        padding-left: {1}rem;
        padding-bottom: {1}rem;
    }}
</style>
""",
        unsafe_allow_html=True,
    )

    if st.button("Back to Main Menue"):
        st.session_state.nextpage = "main_page"
        st.experimental_rerun()

    game_id = ""

    game_id = st.session_state.game_id
    future = st.empty()
    joker_lap_code = None

    with st.expander("Game Settings", expanded = False):
        result = fetch_get(f"{settings.driftapi_path}/manage_game/get/{game_id}/")
        if result:
            if "joker_lap_code" in result:
                joker_lap_code = result["joker_lap_code"]
            st.write(result)
    
    with st.expander("Connection info", expanded=False):
        submitUri:str = "http://"+settings.hostname+":8001/game"
        st.image(getqrcode(submitUri), clamp=True)
        st.write("URL: "+submitUri)
        st.write("GAME ID: "+game_id)

    result = fetch_get(f"{settings.driftapi_path}/game/{game_id}/ping")
    
    if result:
        result = fetch_get(f"{settings.driftapi_path}/game/{game_id}/playerstatus")
        if result:
            while True:
                with future.container():

                    # CSS to inject contained in a string
                    hide_dataframe_row_index = """
                                <style>
                                .row_heading.level0 {display:none}
                                .blank {display:none}
                                </style>
                    """
                    # Inject CSS with Markdown
                    st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

                    def constructEntry(r:dict):
                        d = {
                            "Spieler":r["user_name"] if "user_name" in r else "",
                            "Beste Runde[s]":r["best_lap"] if "best_lap" in r else None,
                            "Letzte Runde[s]":r["last_lap"] if "last_lap" in r else None,
                            "Runden":r["laps_completed"] if "laps_completed" in r else 0,
                            "Punkte":r["total_score"] if "total_score" in r else 0,
                            "Gesamtzeit":r["total_time"] if "total_time" in r else "",
                        }

                        if joker_lap_code:
                            d["Joker Laps"] = str(r["target_code_counter"][str(joker_lap_code)]) if "target_code_counter" in r else "0"

                        return d

                    result = [constructEntry(r) for r in result if (type(r) is dict)]
                    #if there is no entry, just add an empty one by calling the construct Entry with an empty dict
                    while len(result)<20:
                        result.append(constructEntry({}))
                    df = pd.DataFrame( result )
                    st.dataframe(df, width=1600, height = 20*len(result))
                    #AgGrid(toBeDisplayedData)
                    time.sleep(2)
        else:
            with future.container():
                st.write("uuups... unexpected result from server")
                #st.error("Error")
    else:
        with future.container():
            st.error("No Game with that id exists, going back to main menue...")
            time.sleep(1)
            st.session_state.nextpage = "main_page"
            st.experimental_rerun()
