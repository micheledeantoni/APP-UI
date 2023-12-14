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

# Display an image from a local file
image = Image.open('MATCHMASTER.jpg')

st.image(image, use_column_width=False, width = 210)

st.markdown(""" # Precise Player Profiling """)





st.markdown(""" ### Search Player """)

player_search = st.text_input('Enter player last name:', '')
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


st.markdown("""----------------------------------------------------""")
st.markdown("""----------------------------------------------------""")
st.markdown("""----------------------------------------------------""")

st.markdown("""



            ## MatchMaster: Your Ultimate Player Matchmaking App 🌟

Welcome to MatchMaster, the brainchild of a talented team of creators from the LeWagon Data Science bootcamp: **Luiz Felipe dos Santos, Michele Deantoni, Ayanda Ntombela, and Hieu Nguyen**. 👨‍💻🚀

### About Us

We are passionate students exploring the exciting world of data science, and MatchMaster is our innovative project that combines our love for sports and analytics. 📊⚽

### What is MatchMaster?

MatchMaster is not just an app; it's your go-to tool for finding the perfect match in the world of football. Thanks to this app, selecting the ideal player is no longer a daunting task. Whether you're a seasoned manager or a casual fan, MatchMaster has you covered. 📱🔍

### How It Works

Simply choose a player, and MatchMaster will work its magic, displaying the best match possible based on the natural characteristics of the selected player. Our algorithm takes into account various attributes to ensure a comprehensive and accurate match. ✨🔄

#### Filters for Precision

Want a player with a similar wage or age? No problem! MatchMaster allows you to fine-tune your search by applying filters, ensuring that the results align perfectly with your specific needs and preferences. ⚙️🎯

### Acknowledgments

We extend our sincere thanks to **EA Sports** for providing the data foundation for MatchMaster. The app relies on data from FIFA and FC games, creating a robust and realistic database to enhance your player selection experience. 🎮📈

Give MatchMaster a try today, and elevate your football management game to a whole new level! ⚽🚀 """)
