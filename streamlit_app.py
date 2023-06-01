# Eerst installeren we de nodige pakketten
# !pip install streamlit spotipy pandas

import os
import spotipy
import pandas as pd
import streamlit as st
import spotipy.util as util
import json

# Controleer of het instellingenbestand bestaat
if os.path.exists('settings.json'):
    # Als het instellingenbestand bestaat, laad dan de instellingen
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        client_id = settings['client_id']
        client_secret = settings['client_secret']
        redirect_uri = settings['redirect_uri']
        username = settings['username']
        scope = settings['scope']
        podcast_id = settings['podcast_id']
else:
    # Als het instellingenbestand niet bestaat, vraag dan de instellingen aan de gebruiker
    client_id = st.text_input('Voer je Spotify Client ID in')
    client_secret = st.text_input('Voer je Spotify Client Secret in', type='password')
    redirect_uri = st.text_input('Voer je Redirect URI in')
    username = st.text_input('Voer je Spotify gebruikersnaam in')
    scope = st.text_input('Voer de scopes in die je wilt aanvragen', value='user-top-read')
    podcast_id = st.text_input('Voer het ID van de podcast in die je wilt volgen')

    if st.button('Sla instellingen op'):
        # Sla de instellingen op in het instellingenbestand
        settings = {
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'username': username,
            'scope': scope,
            'podcast_id': podcast_id
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

# Verkrijg een toegangstoken
token = util.prompt_for_user_token(
    username, 
    scope, 
    client_id=client_id, 
    client_secret=client_secret, 
    redirect_uri=redirect_uri
)

# Maak een nieuwe Spotify client met het toegangstoken
spotify = spotipy.Spotify(auth=token)

# Functie om de podcast data te krijgen
def get_podcast_data(podcast_id):
    podcast = spotify.show(podcast_id)
    return {
        'date': pd.Timestamp.now(),
        'followers': podcast['followers']['total'],
        'popularity': podcast['popularity']
    }

# Update het CSV bestand met de nieuwe data
def update_csv(data, filename='podcast_data.csv'):
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = df.append(data, ignore_index=True)
    else:
        df = pd.DataFrame([data])
    df.to_csv(filename, index=False)

# Krijg de nieuwe podcast data en update het CSV bestand
new_data = get_podcast_data(podcast_id)
update_csv(new_data)

# Nu dat we de data hebben, kunnen we het in Streamlit weergeven
df = pd.read_csv('podcast_data.csv')

# Functie om de podcast data te krijgen
def get_podcast_data(podcast_id):
    podcast = spotify.show(podcast_id)
    return {
        'date': pd.Timestamp.now(),
        'followers': podcast['followers']['total'],
        'popularity': podcast['popularity']
    }

# Update het CSV bestand met de nieuwe data
def update_csv(data, filename='podcast_data.csv'):
    df = pd.read_csv(filename)
    df = df.append(data, ignore_index=True)
    df.to_csv(filename, index=False)

# Krijg de nieuwe podcast data en update het CSV bestand
new_data = get_podcast_data(podcast_id)
update_csv(new_data)

# Nu dat we de data hebben, kunnen we het in Streamlit weergeven
df = pd.read_csv('podcast_data.csv')

# Nu dat we de data hebben, kunnen we het in Streamlit weergeven
df = pd.read_csv('podcast_data.csv')

st.title('Podcast Statistieken')

# Visualiseer de gegevens over tijd met behulp van lineaire grafieken
st.subheader('Aantal volgers over tijd')
st.line_chart(df['followers'])

st.subheader('Populariteit over tijd')
st.line_chart(df['popularity'])
