import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import chaves

#Configurações de autenticação da API do Spotify
client_id = chaves.client_id
client_secret = chaves.client_secret
playlist_id = chaves.playlist_id

#Autenticar-se na API do Spotify
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

#Obter informações da playlist
playlist = sp.playlist(playlist_id)
playlist_name = playlist['name']

#Inicializar lista para armazenar todas as faixas da playlist
all_tracks= []

#Criar listas vazias para armazenar os dados das músicas
data = {
    'Track Name': [],
    'Artist Name': [],
    'Album Name': [],
    'Release Date': [],
    'Popularity': [],
    'Duration (ms)': [],
    'Danceability': [],
    'Energy': [],
    'Key': [],
    'Loudness': [],
    'Mode': [],
    'Speechiness': [],
    'Acousticness': [],
    'Instrumentalness': [],
    'Liveness': [],
    'Valence': [],
    'Tempo': []
}

#Obter todas as faixas da playlist usando paginação
def scrape():
    print('Fetching playlist track info')
    offset = 0
    while True:
        print(f'    | Tracks #{offset} to #{offset+100}')
        sleepSec = .5
        try:
            tracks = sp.playlist_tracks(playlist_id, offset=offset, limit=100)
            all_tracks.extend(tracks['items'])
            #if (len(tracks['items']) < 100):
            if (len(tracks['items']) == 0):
                break  # Sai do loop se não houver mais faixas
            offset += 100
        except spotipy.exceptions.SpotifyException as se:
            sleepSec = se.headers.get('Retry-after')
            print(f'    x Too many requests, waiting {sleepSec} seconds before next attempt...')

        #Adicionar uma pausa de 1 segundo entre as chamadas para evitar o erro 429
        time.sleep(sleepSec)
    print(f'    └ Success')

    #Extrair dados das músicas
    trackIndex = 0
    while trackIndex < len(all_tracks):
        sleepSec = .5
        track_info = all_tracks[trackIndex]['track']
        name = track_info['name']
        print(f'\n #{trackIndex} - {name}')

        #Obter features de áudio
        success = False
        while not success:
            print('    | Attempting to extract audio data...')
            try:
                features = sp.audio_features(track_info['id'])[0]
                
                data['Track Name'].append(track_info['name'])
                data['Artist Name'].append(track_info['artists'][0]['name'])
                data['Album Name'].append(track_info['album']['name'])
                data['Release Date'].append(track_info['album']['release_date'])
                data['Popularity'].append(track_info['popularity'])

                data['Duration (ms)'].append(features['duration_ms'])
                data['Danceability'].append(features['danceability'])
                data['Energy'].append(features['energy'])
                data['Key'].append(features['key'])
                data['Loudness'].append(features['loudness'])
                data['Mode'].append(features['mode'])
                data['Speechiness'].append(features['speechiness'])
                data['Acousticness'].append(features['acousticness'])
                data['Instrumentalness'].append(features['instrumentalness'])
                data['Liveness'].append(features['liveness'])
                data['Valence'].append(features['valence'])
                data['Tempo'].append(features['tempo'])
                print(f'    └ Success')
                trackIndex +=1
                success = True
            except spotipy.exceptions.SpotifyException as se:
                print(f'    x Too many requests, aborting...')
                return

        time.sleep(sleepSec)

scrape()

# Criar um DataFrame pandas com os dados coletados
df = pd.DataFrame(data)

# Salvar o DataFrame em um arquivo CSV
csv_filename = f'{playlist_name}_all_tracks.csv'
df.to_csv(csv_filename, index=False)

print(f'\n Exported to CSV file: {csv_filename}')
