import streamlit as st
import requests

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

      race_id = st.text_input("Race ID", value="Race1", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, disabled=False)
      submitted = st.form_submit_button("Show Scoreboard")

      if submitted:
          st.write("Result")
          body = {}
          result = fetch(session, f"http://localhost:8000/{race_id}/events", body)
          if result:
              toBeDisplayedData = [{"username":r["username"]} for r in result if ("username" in r.keys())]
              st.dataframe(data=toBeDisplayedData, width=None, height=None)
          else:
              st.error("Error")

if __name__ == '__main__':
    main()