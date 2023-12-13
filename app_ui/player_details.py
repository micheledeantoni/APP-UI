import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests

def plot_statistics():
    # Visualization
    colors = ['#1f77b4', '#7f7f7f', '#aec7e8', '#c7c7c7']  # Shades of blue and grey
    fig, axes = plt.subplots(nrows=1, ncols=len(metrics), figsize=(20, 5))

    # Plot each metric
    for i, metric in enumerate(metrics):
        aggregated_data[metric].plot(kind='bar', color=colors[i % len(colors)], ax=axes[i])
        add_trendline(axes[i], aggregated_data[metric], color='black')
        axes[i].set_title(f'{metric.replace("_", " ").capitalize()} per season')
        axes[i].set_ylabel(metric.replace("_", " ").capitalize())

    return fig

def add_trendline(ax, data, color):
    # Define the range of seasons for the trend line
    seasons_range = ['18/19', '19/20', '20/21', '21/22', '22/23']

    # Filter data to include only the defined range
    filtered_data = data.loc[data.index.intersection(seasons_range)]

    # Calculate and plot the trend line if there is any data
    if not filtered_data.empty:
        z = np.polyfit(np.arange(len(filtered_data)), filtered_data, 1)
        p = np.poly1d(z)
        ax.plot(filtered_data.index, p(np.arange(len(filtered_data))), color=color, linestyle='--')
        slope = round(z[0], 2)
        ax.text(0.05, 0.95, f'Trend: {slope}', transform=ax.transAxes, fontsize=12, verticalalignment='top', color=color)

def plot_radar():
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=grouped_df.iloc[player_chosen['idx']].values,
        theta=categories,
        fill='toself',
        name=player_chosen['short_name']
    ))
    fig.add_trace(go.Scatterpolar(
        r=grouped_df.iloc[player_suggested['idx']].values,
        theta=categories,
        fill='toself',
        name=player_suggested['short_name']
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 100]
        )),
    showlegend=True
    )
    return fig

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
    cols = st.columns(2)
    with cols[0]:
        st.markdown(""" ### Chosen Player """)
        player_chosen = st.session_state.get('chosen_player')
        container = st.container(border=True)
        container.write(player_chosen['short_name'])
        container.image(player_chosen['player_face_url'], width=100)
        container.write(player_chosen['league_name'])
        container.write(player_chosen['club_name'])

        st.markdown(""" ### Suggested Player """)
        player_suggested = st.session_state.get('suggested_player')
        container = st.container(border=True)
        container.write(player_suggested['short_name'])
        container.image(player_suggested['player_face_url'], width=100)
        container.write(player_suggested['league_name'])
        container.write(player_suggested['club_name'])

    with cols[1]:
        # Show statistics plot
        st.markdown(""" ### Statistics """)
        player_index = player_chosen['idx']
        params = {'player_index': player_index}
        response = requests.get(base_url_api + '/statistics', params=params)
        statistics = response.json()['statistics']
        metrics = statistics['metrics']
        aggregated_data = pd.DataFrame(statistics['aggregated_data'])

        st.pyplot(plot_statistics())

        player_index = player_suggested['idx']
        params = {'player_index': player_index}
        response = requests.get(base_url_api + '/statistics', params=params)
        statistics = response.json()['statistics']
        metrics = statistics['metrics']
        aggregated_data = pd.DataFrame(statistics['aggregated_data'])

        st.pyplot(plot_statistics())

#Show radar plot
params = {'player1_index': player_chosen['idx'],
          'player2_index': player_suggested['idx']}
response = requests.get(base_url_api + '/data_radar_plot', params=params)
radar = response.json()['radar_data']
grouped_df = pd.DataFrame(radar['grouped_df'])
categories = grouped_df.columns
st.plotly_chart(plot_radar())

if st.button('See Another Player', use_container_width=True):
    switch_page('player_suggestion')

if st.button('Home 🏠', use_container_width=True):
    switch_page('app')
