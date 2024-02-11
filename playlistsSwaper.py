# Lic. García Héctor
#! python3
# playlistsSwaper.py - Aplicación para migrar playlist entre diversos servicios de streaming de audio (Spotify, Tidal, Youtube Music ...) 

import spotipy,sys,os
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import MemoryCacheHandler
from dotenv import load_dotenv

# Carga de las variables de entorno desde el archivo .env
load_dotenv()

# Credenciales de las variables de entorno
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

# Inicializa el objeto SpotifyOAuth
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope='playlist-read-private')

# Obtiene el token de acceso (se conecta vía browser para obtener permisos)
token_info = sp_oauth.get_access_token(as_dict=False)

# Inicializa el objeto Spotify
sp = spotipy.Spotify(auth_manager=sp_oauth)

# Obtiene las listas de reproducción del usuario
playlists = sp.current_user_playlists()

#Imprime las listas de reproducción
for playlist in playlists['items']:
    print(playlist['name'])
