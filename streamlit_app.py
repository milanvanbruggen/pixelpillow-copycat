import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os
import json

# Lees settings uit settings.json
with open("settings.json", "r") as read_file:
    settings = json.load(read_file)

# Maak Spotify object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=settings['client_id'],
                                               client_secret=settings['client_secret'],
                                               redirect_uri=settings['redirect_uri'],
                                               scope=settings['scope']))

# Haal code parameter uit URL
params = st.experimental_get_query_params()
code = params.get('code')

if code:
    # Gebruik de eerste code om een toegangstoken te krijgen
    token_info = sp.auth_manager.get_access_token(code[0])
    token = token_info['access_token']

    # Sla het token op voor later gebruik
    os.environ['SPOTIPY_TOKEN'] = token

    # Gebruik het token om toegang te krijgen tot Spotify API
    sp.set_access_token(token)
    
    # Haal de podcasts op die de gebruiker heeft opgeslagen
    shows = sp.current_user_saved_shows()

    # Maak een leeg dataframe om de show-gegevens in op te slaan
    df = pd.DataFrame()

    # Loop door de shows en voeg de gegevens toe aan het dataframe
    for show in shows['items']:
        show_data = show['show']
        df = df.append({
            'name': show_data['name'],
            'publisher': show_data['publisher'],
            'description': show_data['description'],
            'link': show_data['external_urls']['spotify'],
            'total_episodes': show_data['total_episodes'],
        }, ignore_index=True)

    # Toon het dataframe in de Streamlit-app
    st.write(df)

else:
    # Als er geen code is, vraag dan om in te loggen.
    auth_url = sp.auth_manager.get_authorize_url()
    st.write(f'Please log in [here]({auth_url}).')
