import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import mainpage, creategame, select_race, delete_race, racedisplay, download_race, remove_player_from_race # import your pages here

def _max_width_(prcnt_width:int = 75):
    max_width_str = f"max-width: {prcnt_width}%;"
    st.markdown(f""" 
                <style> 
                .reportview-container .main .block-container{{{max_width_str}}}
                </style>    
                """, 
                unsafe_allow_html=True,
    )

if __name__ == '__main__':
    # Create an instance of the app 
    #st.set_page_config(layout="wide")
    _max_width_(90)
    app = MultiPage()
    # Title of the main page
    st.title("Drift Racedisplay Prototype")

    # Add all your applications (pages) here
    app.add_page("main_page", mainpage.app)
    app.add_page("create_game", creategame.app)
    app.add_page("select_race", select_race.app)
    app.add_page("delete_race", delete_race.app)
    app.add_page("racedisplay", racedisplay.app)
    app.add_page("download_race", download_race.app)
    app.add_page("remove_player_from_race", remove_player_from_race.app)

    

    print(app.pages)

    # The main app
    app.run()


