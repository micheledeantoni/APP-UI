import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
from PIL import Image
from io import BytesIO
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

base_url_api = 'https://app-rpisvpygla-ew.a.run.app'

with st.container():
    r = requests.get('https://tanzolymp.com/images/default-non-user-no-photo-1.jpg')
    default_img = Image.open(BytesIO(r.content))

    cols = st.columns(2)
    with cols[0]:
        st.markdown(""" ### Chosen Player """)
        player = st.session_state.get('chosen_player')
        container = st.container(border=True)
        container.write(player['short_name'])

        r = requests.get(player['player_face_url'])
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))
        else:
            img = default_img
        container.image(img, width=100)

        #container.write(player['league_name'])
        #container.write(player['club_name'])

    with cols[1]:
        st.markdown(""" ### Filters """)
        cols_filters = st.columns(3)
        with cols_filters[0]:
            continent = st.selectbox('Continent', ['Any', 'Europe', 'Americas', 'Africa', 'Asia', 'Oceania'])
        with cols_filters[1]:
            experience = st.selectbox('Experience', ['Any', 'Prospect', 'Emerging Talent',
                                                    'Established Player', 'Peak Performance', 'Experienced Campaigner'])
        with cols_filters[2]:
            league_level = st.selectbox('League Level', ['Any', '1st', '2nd'])
        with cols_filters[0]:
            value_range = st.selectbox('Value Range', ['Any', 'Good deal', 'Affordable', 'Expensive',
                                                    'Really expensive', 'Crazily expensive'])
        with cols_filters[1]:
            wage_range = st.selectbox('Wage Range', ['Any', 'Low salary', 'Medium-low salary', 'Medium-high salary', 'High salary'])

find_suggestions_btn = st.button('Find Suggested Players', use_container_width=True)

if st.session_state.get('find_suggestions_btn') != True:
    st.session_state['find_suggestions_btn'] = find_suggestions_btn

if st.session_state['find_suggestions_btn'] == True:
    params = {'player_index': player['idx']}
    if continent != 'Any':
        params['continent'] = continent
    if experience != 'Any':
        params['experience'] = experience
    if league_level != 'Any':
        params['league_level'] = league_level
    if value_range != 'Any':
        params['value_range'] = value_range
    if wage_range != 'Any':
        params['wage_range'] = wage_range

    response = requests.get(base_url_api + '/players-suggestion', params=params)
    players_suggestion = response.json()
    if len(players_suggestion['players']) == 0:
        st.markdown(''' No Players Found! ''')
    else:
        ##st.markdown(""" ### Suggestions """)
        cols = st.columns(5)
        col_num = 0
        for player in players_suggestion['players']:
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
                        st.session_state['find_suggestions_btn'] = False
                        st.session_state['suggested_player'] = player
                        switch_page('player_details')
            col_num += 1

if st.button('Home 🏠', use_container_width=True):
    st.session_state['find_suggestions_btn'] = False
    switch_page('app')
