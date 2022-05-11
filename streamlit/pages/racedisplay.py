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


def getGameInfo(game_id):
    return fetch_get(f"{settings.driftapi_path}/manage_game/get/{game_id}/")

def getScoreBoard(game_id):
    return fetch_get(f"{settings.driftapi_path}/game/{game_id}/playerstatus")

def app():

    game_id = st.session_state.game_id

    if st.button("Back to Main Menue"):
        st.session_state.nextpage = "main_page"
        st.experimental_rerun()

    game = getGameInfo(game_id)

    if not game:
        st.error("No Game with that id exists, going back to main menue...")
        time.sleep(1)
        st.session_state.nextpage = "main_page"
        st.experimental_rerun()

    joker_lap_code = None
    if game:
        if "joker_lap_code" in game:
            joker_lap_code = game["joker_lap_code"]

    scoreboard = st.empty()

    with st.expander("Game Settings", expanded = False):
        st.write(game)

    with st.expander("Connection info", expanded=False):
        submitUri:str = "http://"+settings.hostname+":8001/game"
        st.image(getqrcode(submitUri), clamp=True)
        st.write("URL: "+submitUri)
        st.write("GAME ID: "+game_id)

    while True:
        with scoreboard.container():
            scoreboard_data = getScoreBoard(game_id)
            # CSS to inject contained in a string
            hide_dataframe_row_index = """
                        <style>
                        .row_heading.level0 {display:none}
                        .blank {display:none}
                        </style>
            """
            # Inject CSS with Markdown
            st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

            def showTime(s):
                return round(float(s),2) if not((s is None) or s== '') else 0.0

            def constructEntry(r:dict):
                d = {
                    "Spieler":r["user_name"] if "user_name" in r else "",
                    "Beste Runde[s]":showTime(r["best_lap"]) if "best_lap" in r else None,
                    "Letzte Runde[s]":showTime(r["last_lap"]) if "last_lap" in r else None,
                    "Runden":r["laps_completed"] if "laps_completed" in r else 0,
                    "Punkte":r["total_score"] if "total_score" in r else 0,
                    "Gesamtzeit":showTime(r["total_time"]) if "total_time" in r else None,
                }

                if joker_lap_code:
                    d["Joker Laps"] = str(r["target_code_counter"][str(joker_lap_code)]) if "target_code_counter" in r else "0"

                return d

            scoreboard_data = [constructEntry(r) for r in scoreboard_data if (type(r) is dict)]
            #if there is no entry, just add an empty one by calling the construct Entry with an empty dict
            while len(scoreboard_data)<3:
                scoreboard_data.append(constructEntry({}))
            df = pd.DataFrame( scoreboard_data )
            st.dataframe(df)
            #st.dataframe(df, width=1600, height = 20*len(scoreboard_data))
            #AgGrid(df)

            time.sleep(3)





