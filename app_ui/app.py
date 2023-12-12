import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
import requests

CSS = '''[class="st-emotion-cache-r421ms e1f1d6gn0"] {
    border: 2px groove red;
}
[data-testid="collapsedControl"] { display: none }'''

st.set_page_config(initial_sidebar_state="collapsed")
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

show_pages([
    Page("app_ui/app.py","app"),
    Page("app_ui/player_suggestion.py","player_suggestion")
])

hide_pages(['player_suggestion'])

base_url_api = 'http://127.0.0.1:8000'

st.markdown(""" # Search Player """)

player_search = st.text_input('Player Name', '')
search_btn = st.button('Search')

if st.session_state.get('search_btn') != True:
    st.session_state['search_btn'] = search_btn

if st.session_state['search_btn'] == True:
    if player_search == '':
        st.warning('Search Player by Name')
    else:
        params = {'player_name': player_search}
        response = requests.get(base_url_api + '/find_player_by_name', params=params)
        players_search = response.json()

        if len(players_search['players']) == 0:
            st.markdown(''' No Players Found! ''')
        else:
            st.markdown(""" ### Choose Player """)
            cols = st.columns(5)
            col_num = 0
            for player in players_search['players']:
                with cols[col_num]:
                    container = st.container(border=True)
                    container.write(player['short_name'])
                    if container.button('Select', key=player['idx']):
                        st.session_state['search_btn'] = False
                        st.session_state['choosen_player'] = player
                        switch_page('player_suggestion')

                col_num = 0 if col_num == 4 else col_num + 1
