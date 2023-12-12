import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
import requests

CSS = ''' [data-testid="collapsedControl"] { display: none } '''

st.set_page_config(initial_sidebar_state="collapsed")
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

show_pages([
    Page("app_ui/app.py","app"),
    Page("app_ui/player_suggestion.py","Player_Suggestion")
])

base_url_api = 'http://127.0.0.1:8000'

st.markdown(""" # Player Suggestion """)

player = st.session_state.get('choosen_player')
st.write(player['short_name'])

st.markdown(""" ## Filters """)
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

if st.button('Calculate Suggestions'):
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
        st.markdown(""" ### Suggestions """)
        cols = st.columns(5)
        col_num = 0
        for player in players_suggestion['players']:
            with cols[col_num]:
                container = st.container(border=True)
                container.write(player['short_name'])
            col_num += 1

if st.button('Home'):
    switch_page('app')
