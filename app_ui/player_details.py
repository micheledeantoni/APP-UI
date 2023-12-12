import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
import requests

CSS = '''
.st-emotion-cache-1y4p8pa {
    padding: 1rem 0rem 0rem;
    max-width: 70rem
}

[class="st-emotion-cache-r421ms e1f1d6gn0"] {
    border: 2px groove;
    width: 200px;
}
[data-testid="collapsedControl"] { display: none }'''

st.set_page_config(initial_sidebar_state="collapsed")
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

show_pages([
    Page("app_ui/app.py","app"),
    Page("app_ui/player_suggestion.py","Player_Suggestion"),
    Page("app_ui/player_details.py","player_details")
])

base_url_api = 'http://127.0.0.1:8000'

with st.container():
    cols = st.columns(2)
    with cols[0]:
        st.markdown(""" ### Choosen Player """)
        player = st.session_state.get('choosen_player')
        container = st.container(border=True)
        container.write(player['short_name'])
        container.image(player['player_face_url'], width=100)
        container.write(player['league_name'])
        container.write(player['club_name'])

    with cols[1]:
        st.markdown(""" ### Suggested Player """)
        player = st.session_state.get('suggested_player')
        container = st.container(border=True)
        container.write(player['short_name'])
        container.image(player['player_face_url'], width=100)
        container.write(player['league_name'])
        container.write(player['club_name'])

if st.button('See Another Player', use_container_width=True):
    switch_page('player_suggestion')

if st.button('Home 🏠', use_container_width=True):
    switch_page('app')
