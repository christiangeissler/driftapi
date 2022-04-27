import streamlit as st


# Custom imports 
from multipage import MultiPage
from pages import mainpage, creategame, racedisplay # import your pages here

if __name__ == '__main__':
    # Create an instance of the app 
    app = MultiPage()

    # Title of the main page
    st.title("Drift Racedisplay Prototype")

    # Add all your applications (pages) here
    app.add_page("main_page", mainpage.app)
    app.add_page("create_game", creategame.app)
    app.add_page("racedisplay", racedisplay.app)

    print(app.pages)

    # The main app
    app.run()


