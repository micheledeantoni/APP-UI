import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
from PIL import Image
from io import BytesIO
import requests

CSS = '''
.st-emotion-cache-1y4p8pa {
    padding: 0rem 0rem 0rem;
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
    Page("app_ui/player_suggestion.py","player_suggestion"),
    Page("app_ui/player_details.py","player_details")
])

hide_pages(['player_suggestion', 'player_details'])

base_url_api = 'https://app-rpisvpygla-ew.a.run.app'

st.markdown(""" # APP - Advanced Player Profiling """)

st.markdown(""" ### Search Player """)

player_search = st.text_input('Player Name', '')
search_btn = st.button('Search', use_container_width=True)

if st.session_state.get('search_btn') != True:
    st.session_state['search_btn'] = search_btn

if st.session_state['search_btn'] == True:
    if player_search == '':
        st.warning('Search Player by Name')
    else:
        params = {'player_name': player_search}
        response = requests.get(base_url_api + '/find_player_by_name', params=params)
        try:
            players_search = response.json()
        except:
            players_search = {'players': []}

        if len(players_search['players']) == 0:
            st.warning(''' No Players Found! ''')
        else:
            #st.markdown(""" ### Choose Player """)
            r = requests.get('https://tanzolymp.com/images/default-non-user-no-photo-1.jpg')
            default_img = Image.open(BytesIO(r.content))

            cols = st.columns(5)
            col_num = 0
            for player in players_search['players']:
                with cols[col_num]:
                    container = st.container(border=True)
                    container.write(player['short_name'])

                    r = requests.get(player['player_face_url'])
                    if r.status_code == 200:
                        img = Image.open(BytesIO(r.content))
                    else:
                        img = default_img
                    container.image(img, width=150)

                    container.write(player['league_name'])
                    container.write(player['club_name'])
                    if container.button('Select', key=player['idx'], use_container_width=True):
                        st.session_state['search_btn'] = False
                        st.session_state['chosen_player'] = player
                        switch_page('player_suggestion')

                col_num = 0 if col_num == 4 else col_num + 1
