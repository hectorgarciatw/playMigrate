import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

class SpotifyAPI:
    def __init__(self):
        # Carga de las variables de entorno desde el archivo .env
        load_dotenv()

        # Credenciales de las variables de entorno para utiliar API de Spotify
        self.SP_CLIENT_ID = os.getenv('SP_CLIENT_ID')
        self.SP_CLIENT_SECRET = os.getenv('SP_CLIENT_SECRET')
        self.SP_REDIRECT_URI = os.getenv('SP_REDIRECT_URI')

        # Inicializa el objeto SpotifyOAuth
        self.sp_oauth = SpotifyOAuth(client_id=self.SP_CLIENT_ID, client_secret=self.SP_CLIENT_SECRET, redirect_uri=self.SP_REDIRECT_URI, scope='playlist-read-private')

        # Inicializa el objeto Spotify
        self.sp = spotipy.Spotify(auth_manager=self.sp_oauth)

    def service_login(self):
        # Obtiene el token de acceso (se conecta vía browser para obtener permisos)
        token_info = self.sp_oauth.get_access_token(as_dict=False)
        # Inicializa el objeto Spotify
        self.sp = spotipy.Spotify(auth_manager=self.sp_oauth)

    def list_playlists(self):
        # Obtiene las listas de reproducción del usuario
        playlists = self.sp.current_user_playlists()
        #Imprime las listas de reproducción
        counter = len(playlists['items'])
        tracks = 0

        print(f'My Spotify playlists:')
        for playlist in playlists['items']:
            print('* ' + playlist['name'])
            tracks += playlist["tracks"]["total"]
        print(f'Playlists found: {counter}')
        print(f'Total tracks found:{tracks}')

    def search_playlist_tracks(self, playlist_name):
        # Busca la playlist por su nombre
        res = self.sp.search(q=playlist_name, type='playlist')
        playlist_info = res['playlists']['items']
        if playlist_info:
            playlist_id = playlist_info[0]["id"]
            counter = playlist_info[0]['tracks']['total']
        else:
            print("No se encontró ninguna playlist con ese nombre.")
            return

        # Obtiene los tracks de la playlist especificada
        playlist_tracks = self.sp.playlist_tracks(playlist_id)
        if len(playlist_tracks['items']) >0:
            print(f'Playlist \"{playlist_name}\" with {counter} tracks found: \n')
            for track in playlist_tracks['items']:
                track_name = track["track"]["name"]
                artist_name = track["track"]["artists"][0]["name"]  # Suponiendo un solo artista por simplicidad
                print(f'{track_name} By {artist_name}')
        else:
            print('La playlist ingresada no existe o no tiene pistas agregadas')
