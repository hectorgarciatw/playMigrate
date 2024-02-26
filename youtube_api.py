import os,pickle,json,time
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from spotify_api import SpotifyAPI

class YoutubeAPI:
    # Define los alcances de la API de YouTube v3
    SCOPES = ['https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/youtube']

    def __init__(self):
        # Almacena una referencia a las credenciales autorizadas
        self.yt_credentials = None

    def load_credentials(self):
        # Intenta cargar las credenciales desde un archivo de caché
        if os.path.exists('yt_credentials.pickle'):
            with open('yt_credentials.pickle', 'rb') as token:
                self.yt_credentials =  pickle.load(token)
        return None

    def save_credentials(self, yt_credentials):
        # Guarda las credenciales en un archivo de caché
        with open('yt_credentials.pickle', 'wb') as token:
            pickle.dump(yt_credentials, token)

    # Actualiza las credenciales del usuario
    def update_credentials(self):
        # Solicita al usuario que se autorice y actualiza las credenciales almacenadas
        self.yt_credentials = self.authorize()
        self.save_credentials(self.yt_credentials)

    def authorize(self):
        # Inicia el flujo de autorización de OAuth2
        flow = InstalledAppFlow.from_client_secrets_file('./client_secret_249986949363-k8ro9gijcpevkmpap9va4gq7neojcegq.apps.googleusercontent.com.json', self.SCOPES)
        yt_credentials = flow.run_local_server(port=0)

        # Guarda las credenciales para futuros usos
        self.save_credentials(yt_credentials)
        return yt_credentials

    def build_service(self):
        # Si no hay credenciales almacenadas, solicita al usuario que se autorice
        if not self.yt_credentials or not self.yt_credentials.valid:
            self.yt_credentials = self.authorize()

        # Construye el servicio de la API de YouTube v3 con las credenciales autorizadas
        return build('youtube', 'v3', credentials=self.yt_credentials)

    # Chequea si ya contamos con las credenciales correspondientes o no
    def get_youtube_service(self):
        # En caso de no contar con credenciales dumpeadas las creo
        if not self.load_credentials():
            # Construye el servicio de la API de YouTube v3
            return self.build_service()
        else:
            # Carga las credenciales almacenadas
            self.yt_credentials = self.load_credentials()
            # Construye y devuelve el servicio de la API de YouTube v3 con las credenciales cargadas
            return build('youtube', 'v3', yt_credentials=self.yt_credentials)

    # Listar las playlists del usuario en YoutubeMusic
    def list_playlists(self):
        # Obtén el servicio de la API de YouTube
        youtube = self.get_youtube_service()

        # Realiza la solicitud para obtener las listas de reproducción del usuario
        request = youtube.playlists().list(
            part='snippet,contentDetails',
            mine=True,
            maxResults=100  # Ajusta el número de resultados por página
        )
        response = request.execute()

        # Imprime las listas de reproducción del usuario
        for playlist in response['items']:
            print('Título de la lista de reproducción:', playlist['snippet']['title'])
            print('ID de la lista de reproducción:', playlist['id'])
            print()

    def get_playlist_id_by_name(self, playlist_name):
        # Obtén el servicio de la API de YouTube
        youtube = self.get_youtube_service()

        # Realiza la solicitud para obtener las listas de reproducción del usuario
        request = youtube.playlists().list(
            part='id,snippet',
            mine=True,
            maxResults=50  # Ajusta el número de resultados por página según tu necesidad
        )
        response = request.execute()

        # Busca la lista de reproducción por su nombre en la respuesta
        for playlist in response['items']:
            if playlist['snippet']['title'] == playlist_name:
                return playlist['id']

        # Si no se encuentra la lista de reproducción, devuelve None
        return None

    # Lista los tracks de una playlist en particular de Youtube Music
    def search_playlist_tracks(self, playlist_name):
        # Obtén el servicio de la API de YouTube
        youtube = self.get_youtube_service()
        # Obtén el ID de la lista de reproducción
        playlist_id = self.get_playlist_id_by_name(playlist_name)

        if not playlist_id:
            print("La lista de reproducción '{}' no fue encontrada.".format(playlist_name))
            return
        
        # Realiza la solicitud para obtener los detalles de la playlist
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=1000
        ).execute()

        # Itera sobre las páginas de resultados
        while playlist_response:
            # Itera sobre los elementos de la playlist e imprime los títulos de los videos
            for item in playlist_response['items']:
                audio_title = item['snippet']['title']
                print(audio_title)

            # Verifica si hay más páginas de resultados
            if 'nextPageToken' in playlist_response:
                next_page_token = playlist_response['nextPageToken']
                # Realiza una nueva solicitud utilizando el token de página siguiente
                playlist_response = youtube.playlistItems().list(
                    part='snippet',
                    playlistId=playlist_id,
                    maxResults=1000,
                    pageToken=next_page_token
                ).execute()
            else:
                # Si no hay más páginas, sal del bucle
                break
        print()
        print(f'Playlist Id: \"{playlist_id}\"')
        
    # Retorna información del usuario de Youtube Music
    def user_info(self):
        # Obtén el servicio de la API de YouTube
        youtube = self.get_youtube_service()

        # Obtiene la información del usuario
        user_info_response = youtube.channels().list(part='snippet', mine=True).execute()
        user_info = user_info_response['items'][0]['snippet']

        print("Información del usuario:")
        print("Nombre de usuario:", user_info['title'])
        print("Descripción:", user_info['description'])
        print("País:", user_info['country'])

        # Obtiene las 10 canciones más reproducidas
        playlist_items_response = youtube.playlistItems().list(
            part='contentDetails',
            playlistId='PL4fGSI1pDJn6XWshnH9CTP9NWNtquAYTh',  # ID de la playlist "Top 100 Most Popular Songs"
            maxResults=10
        ).execute()

        print("\nLas 10 canciones más reproducidas:")
        for item in playlist_items_response['items']:
            video_id = item['contentDetails']['videoId']
            video_response = youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()
            video_info = video_response['items'][0]['snippet']
            print("Título:", video_info['title'])
            print("ID del video:", video_id)
            print()

    # Creando una playlist de Youtube Music desde cero
    def create_playlist(self, playlist_name):
        # Get the YouTube service
        youtube = self.get_youtube_service()

        # Create the playlist
        request = youtube.playlists().insert(
            part="snippet",
            body={
                "snippet": {
                    "title": playlist_name
                }
            }
        )
        response = request.execute()
        print("Playlist '{}' created successfully with ID: {}".format(playlist_name, response["id"]))

    def migrate_playlist_from_sp(self,playlist_name):
        # Get the YouTube service
        youtube = self.get_youtube_service()

        spotify_api = SpotifyAPI()

        sp_playlist_data = spotify_api.get_playlist_data(playlist_name)

        # Creamos una playlist vacia
        request = youtube.playlists().insert(
            part="snippet",
            body={
                "snippet": {
                    "title": sp_playlist_data['playlist_name']
                }
            }
        )
        response = request.execute()
        playlist_id = response["id"]

        # Agregar pistas de Spotify a la playlist de YouTube Music
        for track in sp_playlist_data['tracks']:
            cont = 0
            # Obtener información de la pista
            artist_name = track['artist']
            track_name = track['track_name']

            # Inicializar variables para paginación
            page_token = None
            video_id = None
            
            # Realizar búsqueda con paginación hasta encontrar un video válido
            while not video_id:
                if cont%5==0:
                    time.sleep(2)
                # Buscar el vídeo en YouTube que coincida con la pista de Spotify
                search_response = youtube.search().list(
                    q=f"{artist_name} {track_name}",
                    part="id",
                    type="video",
                    videoCategoryId="10",  # Categoría de música
                    maxResults=1,
                    pageToken=page_token
                ).execute()

                # Obtener el ID del video de música encontrado
                video_id = search_response['items'][0]['id']['videoId'] if 'items' in search_response else None

                # Actualizar el token de página para la próxima iteración si hay más resultados
                page_token = search_response.get('nextPageToken')

                # Si no hay más resultados, salir del bucle
                if not page_token:
                    break

            if video_id:
                # Agregar el vídeo a la playlist
                request = youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id
                            }
                        }
                    }
                )
                response = request.execute()
                print(f"Track '{track_name}' agregado exitosamente a la playlist.")
                cont+=1
            else:
                print(f"No se encontró un video para la pista '{track_name}'.")