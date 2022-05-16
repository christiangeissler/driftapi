import streamlit as st
import time
from datetime import timedelta
import pandas as pd 
import numpy as np
from PIL import Image

from  .session import fetch_post, fetch_put, fetch_get
from .singletons import settings, logger



def getGameInfo(game_id):
    return fetch_get(f"{settings.driftapi_path}/manage_game/get/{game_id}/")

def getScoreBoard(game_id):
    return fetch_get(f"{settings.driftapi_path}/game/{game_id}/playerstatus")

def app():

    game_id = st.session_state.game_id

    if st.button("Back to Race"):
        st.session_state.nextpage = "racedisplay"
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


            scoreboard_data = getScoreBoard(game_id)

            def showTime(s):
                return round(float(s),2) if not((s is None) or s== '') else 0.0

            def constructEntry(r:dict):
                d = {
                    "Spieler":r["user_name"] if "user_name" in r else "",
                    "Beste[s]":showTime(r["best_lap"]) if "best_lap" in r else None,
                    "Letzte[s]":showTime(r["last_lap"]) if "last_lap" in r else None,
                    "Runden":r["laps_completed"] if "laps_completed" in r else 0,
                    "Punkte":r["total_score"] if "total_score" in r else 0,
                    "Zeit[s]":showTime(r["total_time"]) if "total_time" in r else None,
                }

                if joker_lap_code != None:
                    #d["Joker Laps"] = str(r["target_code_counter"][str(joker_lap_code)]) if "target_code_counter" in r else "0"
                    d["Joker"] = int(r["joker_laps_counter"]) if "joker_laps_counter" in r else 0
                    

                return d

            scoreboard_data = [constructEntry(r) for r in scoreboard_data if (type(r) is dict)]

            while len(scoreboard_data)<1:
                scoreboard_data.append(constructEntry({}))

            df = pd.DataFrame( scoreboard_data )

            st.download_button(
                "Press to Download as csv",
                df.to_csv(index = False),
                game_id+".csv",
                "text/csv",
                key='download-csv'
            )
            '''
            st.download_button(
                "Press to Download as html",
                df.to_html(),
                game_id+".html",
                "text/html",
                key='download-html'
            )
            '''

            st.download_button(
                "Press to Download as json",
                df.to_json(orient='records'),
                game_id+".json",
                "text/json",
                key='download-json'
            )




