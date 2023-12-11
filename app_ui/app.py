import streamlit as st

st.markdown(""" # Search Player """)

player_search = st.text_input('Player Name', '')
if st.button('Search'):
    st.markdown(""" ## Suggestions """)
