import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
import requests

CSS = ''' [data-testid="collapsedControl"] { display: none } '''

st.set_page_config(initial_sidebar_state="collapsed")
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

show_pages([
    Page("app_ui/app.py","Search"),
    Page("app_ui/player_suggestion.py","Player_Suggestion")
])

base_url_api = 'http://127.0.0.1:8000'

st.markdown(""" # Player Suggestion """)

player = st.session_state.get('choosen_player')
st.write(player['name'])

if st.button('Calculate Suggestions'):
    params = {'player_index': player['index']}
    response = requests.get(base_url_api + '/players-suggestion', params=params)
    players_suggestion = response.json()

    st.markdown(""" ### Suggestions """)
    cols = st.columns(5)
    col_num = 0
    for index, name in players_suggestion['players'].items():
        with cols[col_num]:
            container = st.container(border=True)
            container.write(name)
        col_num += 1

if st.button('Home'):
    switch_page('Search')
