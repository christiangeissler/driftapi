import streamlit as st
import requests
import pandas as pd 
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import time

def fetch(session, url, body):
    try:
        result = session.put(url, json=body)
        return result.json()
    except Exception:
        return {}



def main():
  """Dr!ft Racing Server
  """
  st.set_page_config(page_title="Drift Racing Display", page_icon="🤖")
  session = requests.Session()


  st.title("Drift Racing Display")
  html_temp = """
  <div style="background-color:blue;padding:10px">
  <h2 style="color:grey;text-align:center;">Streamlit App </h2>
  </div>

  """
  with st.form("my_form"):

      game_id = st.text_input("Game ID", value="Race1", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)
      submitted = st.form_submit_button("Show Scoreboard")

      if submitted:

        #agrid = AgGrid(df)
        future = st.empty()

        while True:
            body = {}
            result = fetch(session, f"http://localhost:8001/{game_id}", body)
            if result:
                with future.container():
                    toBeDisplayedData = pd.DataFrame( [{"username":r["user_name"], "best lap":r["best_lap"], "laps":r["laps_completed"]} for r in result if ("user_name" in r.keys())] )
                    st.dataframe(toBeDisplayedData)
            else:
                st.error("Error")
            time.sleep(1)

if __name__ == '__main__':
    main()