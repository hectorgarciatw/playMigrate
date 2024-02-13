# Lic. García Héctor
#! python3
# playMigrate.py - Aplicación para migrar playlist entre diversos servicios de streaming de audio (Spotify, Tidal, Youtube Music ...) 

import spotipy,sys,os
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import MemoryCacheHandler
from dotenv import load_dotenv

# TO DO - Comandos esenciales para implementar
#playMigrate spotify -l (lista todas las playlists)
#playMigrate spotify playlist -l (listas todos los tracks de una playlist)
#playMigrate migrate spotify tidal -a (migra todas las playlists de un servicio a otro)
#playMigrate migrate spotify tidal playlist (migra la playlist ingresada de un servicio a otro)

# Carga de las variables de entorno desde el archivo .env
load_dotenv()

def serviceLogin(service):
    if service=='spotify':
        # Credenciales de las variables de entorno para utiliar API de Spotify
        CLIENT_ID = os.getenv('CLIENT_ID')
        CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        REDIRECT_URI = os.getenv('REDIRECT_URI')

        # Inicializa el objeto SpotifyOAuth
        sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope='playlist-read-private')
        # Obtiene el token de acceso (se conecta vía browser para obtener permisos)
        token_info = sp_oauth.get_access_token(as_dict=False)
        # Inicializa el objeto Spotify
        sp = spotipy.Spotify(auth_manager=sp_oauth)
        return sp
    else:
        return

if len(sys.argv) > 1:
    # Listar todas las playlists del usuario de Spotify
    if len(sys.argv) == 3 and sys.argv[1]=='spotify' and sys.argv[2]=='-l':
        service = sys.argv[1]
        if  service == 'spotify':
            sp = serviceLogin(service)
            # Obtiene las listas de reproducción del usuario
            playlists = sp.current_user_playlists()
            #Imprime las listas de reproducción
            counter = len(playlists['items'])
            tracks = 0

            print(f'My {service} playlists:')
            for playlist in playlists['items']:
                print('* ' + playlist['name'])
                tracks += playlist["tracks"]["total"]
            print(f'Playlists found: {counter}')
            print(f'Total tracks found:{tracks}')
    elif len(sys.argv) == 4 and sys.argv[1]=='spotify'and sys.argv[3]=='-l':
        service = sys.argv[1]
        playlist_name = sys.argv[2]
        sp = serviceLogin(service)
        # Busca la playlist por su nombre
        res = sp.search(q=playlist_name, type='playlist')
        playlist_info = res['playlists']['items']
        if playlist_info:
            playlist_id = playlist_info[0]["id"]
            counter = playlist_info[0]['tracks']['total']
        else:
            print("No se encontró ninguna playlist con ese nombre.")
        # Obtiene los tracks de la playlist especificada
        playlist_tracks = sp.playlist_tracks(playlist_id)
        if len(playlist_tracks['items']) >0:
            print(f'Playlist \"{playlist_name}\" with {counter} tracks found: \n')
            for track in playlist_tracks['items']:
                track_name = track["track"]["name"]
                artist_name = track["track"]["artists"][0]["name"]  # Suponiendo un solo artista por simplicidad
                print(f'{track_name} By {artist_name}')
        else:
            print('La playlist ingresada no existe o no tiene pistas agregadas')
else:
    print('Error con los argumentos')

