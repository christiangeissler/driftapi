import streamlit as st
from  .session import fetch


def app():
    
    st.markdown("## Main Page")


    if st.button("Create New Game"):
        st.session_state.nextpage = "create_game"
        st.experimental_rerun()

    if st.button("Show Game"):
        st.session_state.nextpage = "racedisplay"
        del st.session_state.game_id
        st.experimental_rerun()