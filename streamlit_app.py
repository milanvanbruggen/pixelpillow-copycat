import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import streamlit as st

# Laad de instellingen
with open('settings.json', 'r') as read_file:
    settings = json.load(read_file)

# Initialiseer de Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=settings['client_id'],
                                               client_secret=settings['client_secret'],
                                               redirect_uri="https://milanvanbruggen-pixelpillow-copycat-streamlit-app-rpi1ua.streamlit.app/",
                                               scope="user-read-playback-position,user-read-playback-state,user-modify-playback-state,playlist-modify-public,user-library-read"))

# Haal code parameter uit URL
params = st.experimental_get_query_params()
code = params.get('code')

if code:
    # Gebruik de eerste code om een toegangstoken te krijgen
    token_info = sp.auth_manager.get_access_token(code[0])
    token = token_info['access_token']

    # Sla het token op voor later gebruik
    os.environ['SPOTIPY_TOKEN'] = token

# Krijg de volgers van de podcast
podcast_id = settings['podcast_id']
followers = sp.podcast(podcast_id)['followers']['total']

# Lees de vorige podcast data
df = pd.read_csv('podcast_data.csv')

# Update de dataframe met de nieuwe volgers teller
df = df.append({'date': pd.Timestamp.now(), 'followers': followers}, ignore_index=True)

# Schrijf de dataframe terug naar het CSV bestand
df.to_csv('podcast_data.csv', index=False)

# Toon de dataframe in de Streamlit app
st.dataframe(df)
