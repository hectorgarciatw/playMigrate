import os,pickle,pprint,sys,csv,json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from youtube_api import YoutubeAPI
from openpyxl import Workbook

# Funciones auxiliares
from common_functions import create_download_folder

class SpotifyAPI:
    def __init__(self):
        # Carga de las variables de entorno desde el archivo .env
        load_dotenv()

        # Credenciales de las variables de entorno para utiliar API de Spotify
        self.SP_CLIENT_ID = os.getenv('SP_CLIENT_ID')
        self.SP_CLIENT_SECRET = os.getenv('SP_CLIENT_SECRET')
        self.SP_REDIRECT_URI = os.getenv('SP_REDIRECT_URI')

        # Inicializa el objeto SpotifyOAuth
        self.sp_oauth = SpotifyOAuth(client_id=self.SP_CLIENT_ID, client_secret=self.SP_CLIENT_SECRET, redirect_uri=self.SP_REDIRECT_URI, scope='user-library-modify user-read-playback-position user-read-currently-playing user-read-recently-played user-top-read playlist-modify-public')

        # Inicializa el objeto Spotify
        self.sp = spotipy.Spotify(auth_manager=self.sp_oauth)
        self.username = self.sp.me()['id']

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

        print()
        print(f'My Spotify playlists:\n')
        for playlist in playlists['items']:
            print(f'* {playlist["name"]} (id: {playlist["id"]})')
            tracks += playlist["tracks"]["total"]

        print()
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

    # Retorna la información de una playlist en particular de Spotify para su migración a otro servicio de streaming
    def get_playlist_data(self, playlist_name):
        # En caso de no contar con credenciales dumpeadas las creo
        if not self.load_credentials():
            # Realiza el login
            self.service_login()

        playlist_data = {'tracks':[]}
        playlist_data['playlist_name'] = playlist_name
        # Busca la playlist por su nombre
        res = self.sp.search(q=playlist_name, type='playlist')
        playlist_info = res['playlists']['items']
        if playlist_info:
            playlist_id = playlist_info[0]['id']
            playlist_data['playlist_id'] = playlist_id
            counter = playlist_info[0]['tracks']['total']
            playlist_data['tracks_counter'] = counter
        else:
            print("No playlist found with that name")
            return

        # Obtiene los tracks de la playlist especificada
        playlist_tracks = self.sp.playlist_tracks(playlist_id)
        if len(playlist_tracks['items']) >0:
            for track in playlist_tracks['items']:
                track_name = track['track']['name']
                track_id = track['track']["id"]
                artist_name = track['track']['artists'][0]['name']  # Suponiendo un solo artista por simplicidad
                album_info = track['track']['album']
                album_name = album_info["name"]
                album_release_date = album_info['release_date']
                # Obtener géneros musicales de cada artista de la pista
                artist_id = track['track']['artists'][0]['id']
                artist_info = self.sp.artist(artist_id)
                genres = artist_info['genres']
                playlist_data['tracks'].append({'track_id':track_id,'artist':artist_name,'track_name':track_name, 'album_name':album_name, 'album_release_date':album_release_date,'genres': genres})
            return playlist_data
        else:
            print('La playlist ingresada no existe o no tiene pistas agregadas')

    # Lista los tracks de una playlist en particular de Spotify
    def search_playlist_tracks(self, playlist_name):
        cont = 0
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
            print("No playlist found with that name")
            return
        
        # Inicializa variables para paginación
        offset = 0
        limit = 100  # Número máximo de resultados por página

        # Itera mientras haya más tracks por recuperar
        print()
        while True:
            # Obtiene los tracks de la playlist especificada con paginación
            playlist_tracks = self.sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
            if len(playlist_tracks['items']) > 0:
                print(f'Playlist \"{playlist_name}\" with {counter} tracks found: \n')
                for track in playlist_tracks['items']:
                    cont += 1
                    track_name = track["track"]["name"]
                    artist_name = track["track"]["artists"][0]["name"]  # Suponiendo un solo artista por simplicidad
                    album_id = track["track"]["album"]["id"]
        
                    # Obtener información del álbum
                    album_info = self.sp.album(album_id)
                    album_name = album_info["name"]
                    release_date = album_info["release_date"]
                    print(f'* {track_name} by {artist_name} from the album  {album_name} released on {release_date}')

                # Actualiza el desplazamiento para obtener la próxima página de resultados
                offset += limit
            else:
                # Si no hay más tracks, sal del bucle
                break
        if cont == 0:
            print('The entered playlist has no tracks added')

    # Busca el artista y el nombre de la canción de a partir de una canción en particular
    def search_song_info(self,song_title):
        # Busca la canción en Spotify
        results = self.sp.search(q=song_title, limit=1)

        # Verifica si se encontraron resultados
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            artist_name = track['artists'][0]['name']
            return {'artist_name':artist_name,'track_name':track}
        else:
            return "No se encontraron resultados para la canción."
        
    # Define una función para obtener el nombre del artista a partir del track_id
    def get_artist_name(self,track_id):
        # Realiza la solicitud a la API de Spotify para obtener la información de la pista
        track_info = self.sp.track(track_id)
    
        # Verifica si la solicitud fue exitosa y si se encontró la pista
        if track_info:
            # Obtiene el nombre del primer artista de la lista de artistas
            if 'artists' in track_info and track_info['artists']:
                return track_info['artists'][0]['name']
        return None

    # Obtención del track_id a partir del nombre de la pista
    def get_track_id(self,track_name):
        results = self.sp.search(q=track_name, type='track', limit=1)
        if results['tracks']['items']:
            track_id = results['tracks']['items'][0]['id']
            return track_id
        else:
            print("No se encontró la canción")
            return None
        
    # Creando una playlist de Spotify desde cero
    def create_playlist(self, playlist_name):
        try:
            # Crear una nueva lista de reproducción en Spotify con el mismo nombre
            playlist = self.sp.user_playlist_create(user=self.username, name=playlist_name, public=True)
            playlist_id = playlist['id']
            print(f'Playlist created successfully with ID: {playlist_id}')
        except spotipy.SpotifyException as e:
            print("Error creating the playlist:", e)

    # Migración de una playlist de Youtube Music a Spotify
    def migrate_playlist_from_yt(self, playlist_name):
        print('Starting the playlist migration process...')
        youtube_api = YoutubeAPI()
        tracks_to_migrate = []
        # Avisamos al usuario que la playlist que se quiere migrar no existe en Youtube Music
        if youtube_api.get_playlist_id_by_name(playlist_name) is None:
            print(f'The entered playlist "{playlist_name}" does not exist')
            sys.exit()

        # Obtener la info de las pistas de la lista de reproducción de YouTube Music
        tracks_info = youtube_api.get_playlist_tracks(playlist_name)
        #pprint.pprint(tracks_info)
        
        for track in tracks_info:
            artist = self.get_artist_name(self.get_track_id(track['track_name']))
            if artist is not None:
                tracks_to_migrate.append({'track_name':track['track_name'],'artist':artist})
            else:
                print('An artist for a track in the playlist could not be found')

        # Obtiene la información del perfil del usuario
        profile_info = self.sp.me()

        # Extrae el nombre de usuario (ID de usuario) de la cuenta de Spotify
        username = profile_info['id']

        try:
            # Crear una nueva lista de reproducción en Spotify con el mismo nombre
            playlist = self.sp.user_playlist_create(user=username, name=playlist_name, public=True)
            playlist_id = playlist['id']
        except spotipy.SpotifyException as e:
            print("Error al crear la playlist:", e)

        # Lista para almacenar los URIs de las pistas
        track_uris = []

        # Agregar las pistas de la lista de reproducción de YouTube Music a la lista de reproducción de Spotify
        for track in tracks_to_migrate:
            # Realizar la búsqueda de la pista
            result = self.sp.search(q=f"track:{track['track_name']} artist:{track['artist']}", limit=1)
    
            # Obtener el URI de la primera pista encontrada (si existe)
            if result['tracks']['items']:
                track_uri = result['tracks']['items'][0]['uri']
                track_uris.append(track_uri)
            else:
                print(f"The track could not be found '{track['track_name']}' of '{track['artist']}' in Spotify.")

        # Añadir las pistas a la lista de reproducción
        self.sp.playlist_add_items(playlist_id, track_uris)
        print("Pistas añadidas a la lista de reproducción con éxito.")

    # Exporta la información de una playlist de Spotify en formáto CSV
    def get_playlist_csv(self,playlist_name):
        data_csv = [['track_title','artist','album','year','playlist','service']]
        # Obtengo la informacion de la playlist de Spotify
        playlist_data = self.get_playlist_data(playlist_name)
        for cancion in playlist_data['tracks']:
            track_title = cancion['track_name']
            artist = cancion['artist']
            album = cancion['album_name']
            year = cancion['album_release_date'][:4]  # Extrae sólo los primeros cuatro caracteres (el año)
            data_csv.append([track_title,artist,album,year,playlist_name,'Spotify'])

        file_path = os.path.join(create_download_folder(self,'csv'), playlist_name + "_spotify.csv")

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file_csv:
                escritor_csv = csv.writer(file_csv)
                for row in data_csv:
                    escritor_csv.writerow(row)

            print(f"CSV file '{file_path}' successfully created")
        except Exception as e:
            print(f"Error creating the CSV file: {e}")

    # Exporta la información de una playlist de Spotify en formáto JSON
    def get_playlist_json(self,playlist_name):
        data_json = []
        playlist_data = self.get_playlist_data(playlist_name)
        for cancion in playlist_data['tracks']:
            track_title = cancion['track_name']
            artist = cancion['artist']
            album = cancion['album_name']
            year = cancion['album_release_date'][:4]  # Extrae sólo los primeros cuatro caracteres (el año)
            data_json.append({'track_title':track_title,'artist':artist,'album':album,'year':year,'playlist':playlist_name,'service':'Spotify'})
        file_path = os.path.join(self.create_download_folder('json'), playlist_name + "_spotify.json")
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data_json, file, indent=4, ensure_ascii=False)
                print(f"JSON file '{file_path}' successfully created")
        except Exception as e:
            print(f"Error creating the JSON file: {e}")

    # Exporta la información de una playlist de Spotify en formáto XLSX
    def get_playlist_xlsx(self,playlist_name):
        data_xlsx = []
        playlist_data = self.get_playlist_data(playlist_name)
        for track in playlist_data['tracks']:
            track_title = track['track_name']
            artist = track['artist']
            album = track['album_name']
            year = track['album_release_date'][:4]  # Extrae sólo los primeros cuatro caracteres (el año)
            data_xlsx.append({'track_title':track_title,'artist':artist,'album':album,'year':year,'playlist':playlist_name,'service':'Spotify'})
        
        # Crear un nuevo libro de trabajo de Excel
        try:
            wb = Workbook()
            sheet = wb.active
            sheet.title = playlist_name + ' spotify playlist info'

            # Escribir encabezados
            sheet.append(["Track title", "Artist", "Album", "Year","Playlist","Service"])

            # Escribir datos de la playlist
            for track in data_xlsx:
                sheet.append([track["track_title"], track["artist"], track["album"],track["year"],track["playlist"],track["service"]])

            # Guardar el libro de trabajo en un archivo Excel
            file = os.path.join(self.create_download_folder('xlsx'), playlist_name + "_spotify.xlsx")
            wb.save(file)
            print(f"XLSX file successfully created")
        except Exception as e:
            print(f"Error creating the Excel file: {e}")

    # Importa la información de una playlist de Spotify desde un archivo local en formáto JSON
    def upload_playlist_from_json(self,playlist_name):
        local_path = os.path.dirname(__file__)
        sub_directories = ['downloads', 'json']  # Lista de subdirectorios
        folder_path = os.path.join(local_path, *sub_directories)
        json_file = os.path.join(folder_path,playlist_name + '_spotify.json')
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                # Carga el contenido del archivo JSON en un diccionario
                playlist_data = json.load(file)

                # En caso de no contar con credenciales dumpeadas las creo
                if not self.load_credentials():
                    # Realiza el login
                    self.service_login()

                playlist_description = "A playlist with songs uploaded with playMigrate"
                user_id = self.sp.current_user()["id"]
                playlist = self.sp.user_playlist_create(user_id, playlist_name, public=True, description=playlist_description)

                # Agrega las canciones a la playlist
                track_uris = []
                for track_info in playlist_data:
                    results = self.sp.search(q=f"{track_info['track_title']} {track_info['artist']}", type="track")
                    if results['tracks']['items']:
                        track_uri = results['tracks']['items'][0]['uri']
                        track_name = results['tracks']['items'][0]['name']
                        artist_name = results['tracks']['items'][0]['artists'][0]['name']
                        print(f"* Adding track: '{track_name}' of '{artist_name}'")
                        track_uris.append(track_uri)

                self.sp.playlist_add_items(playlist['id'], track_uris)
                print('Spotify playlist created successfully!')
        
        except FileNotFoundError:
            print("The file was not found")
        except json.decoder.JSONDecodeError:
            print("The file does not have a valid JSON format")
        except Exception as e:
            print("An error occurred while trying to read the JSON file:", e)