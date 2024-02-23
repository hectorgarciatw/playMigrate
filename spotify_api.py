import os,pickle
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
        self.sp_oauth = SpotifyOAuth(client_id=self.SP_CLIENT_ID, client_secret=self.SP_CLIENT_SECRET, redirect_uri=self.SP_REDIRECT_URI, scope='user-library-modify user-read-playback-position user-read-currently-playing user-read-recently-played user-top-read')

        # Inicializa el objeto Spotify
        self.sp = spotipy.Spotify(auth_manager=self.sp_oauth)

    def service_login(self):
        # Obtiene el token de acceso (se conecta vía browser para obtener permisos)
        token_info = self.sp_oauth.get_access_token(as_dict=False)
        # Serializa las credenciales de Spotipy
        with open('sp_credentials.pickle', 'wb') as f:
            pickle.dump(token_info, f)
        # Inicializa el objeto Spotify
        self.sp = spotipy.Spotify(auth_manager=self.sp_oauth)

    def load_credentials(self):
        # Intenta cargar las credenciales desde un archivo de caché
        if os.path.exists('sp_credentials.pickle'):
            with open('sp_credentials.pickle', 'rb') as token:
                return pickle.load(token)
        return None

    # Listar las playlists del usuario en Spotify
    def list_playlists(self):
        # En caso de no contar con credenciales dumpeadas las creo
        if not self.load_credentials():
            # Realiza el login
            self.service_login()

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

    # Retorna información del usuario de Spotify
    def user_info(self):
        # En caso de no contar con credenciales dumpeadas las creo
        if not self.load_credentials():
            # Realiza el login
            self.service_login()

        # Obtiene la información del perfil del usuario
        user_info = self.sp.current_user()

        # Obtiene las canciones más reproducidas
        top_tracks = self.sp.current_user_top_tracks(limit=10, time_range='short_term')

        # Obtiene los artistas más escuchados
        top_artists = self.sp.current_user_top_artists(limit=10, time_range='short_term')

        # Obtiene el tiempo total de reproducción
        playback = self.sp.currently_playing()

        if playback is not None:
            total_playback_time_ms = playback['progress_ms']
            total_playback_time_min = total_playback_time_ms / 60000

        # Imprime las estadísticas obtenidas del usuario
        print((' ' + user_info['display_name'] + ' Spotify account information: ').center(100,'*'))
        print('Total followers:' + str(user_info['followers']['total']))
        print("\nTop 10 most recently played songs:")
        for track in top_tracks['items']:
            print(track['name'], '-', track['artists'][0]['name'])
        print("\nTop 10 most recently listened to artists:")
        for artist in top_artists['items']:
            print(artist['name'])
        if playback is not None:
            print(f"\nTotal playback time: {total_playback_time_min:.2f} minutes")

    # Lista los tracks de una playlist en particular de Spotify
    def search_playlist_tracks(self, playlist_name):
        # En caso de no contar con credenciales dumpeadas las creo
        if not self.load_credentials():
            # Realiza el login
            self.service_login()
            
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
