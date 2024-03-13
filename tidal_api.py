import os,pickle,pprint,sys,csv,json
import spotipy
import tidalapi
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from youtube_api import YoutubeAPI
from openpyxl import Workbook

class TidalAPI:
    def __init__(self):
        # Carga de las variables de entorno desde el archivo .env
        load_dotenv()

        # Credenciales de las variables de entorno para utiliar API de Spotify
        self.TIDAL_CLIENT_ID = os.getenv('TIDAL_CLIENT_ID')
        self.TIDAL_CLIENT_SECRET = os.getenv('TIDAL_CLIENT_SECRET')
        self.TIDAL_REDIRECT_URI = os.getenv('TIDAL_REDIRECT_URI')

    # Listar las playlists del usuario en Tidal
    def list_playlists(self):
        counter = 0
        tracks = 0
        session = tidalapi.Session()
        # Muestra en consola la URL para realizar el login correspondiente
        session.login_oauth_simple()

        playlists = session.user.playlists()
        print(f"PLAYLISTS:{playlists}")

        print()
        print(f'My Tidal playlists:\n')
        for playlist in playlists:
            counter+=1
            tracks += playlist.num_tracks
            print(f'* {playlist.name} (id: {playlist.id})')
        
        print()
        print(f'Playlists found: {counter}')
        print(f'Total tracks found:{tracks}')
