import os,pickle
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class YoutubeAPI:
    # Define los alcances de la API de YouTube v3
    SCOPES = ['https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/youtube']

    def __init__(self):
        # Almacena una referencia a las credenciales autorizadas
        self.credentials = None

    def load_credentials(self):
        # Intenta cargar las credenciales desde un archivo de caché
        if os.path.exists('credentials.pickle'):
            with open('credentials.pickle', 'rb') as token:
                self.credentials =  pickle.load(token)
        return None

    def save_credentials(self, credentials):
        # Guarda las credenciales en un archivo de caché
        with open('credentials.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    def authorize(self):
        # Inicia el flujo de autorización de OAuth2
        flow = InstalledAppFlow.from_client_secrets_file('./client_secret_249986949363-k8ro9gijcpevkmpap9va4gq7neojcegq.apps.googleusercontent.com.json', self.SCOPES)
        credentials = flow.run_local_server(port=0)

        # Guarda las credenciales para futuros usos
        self.save_credentials(credentials)
        return credentials

    def build_service(self):
        # Si no hay credenciales almacenadas, solicita al usuario que se autorice
        if not self.credentials or not self.credentials.valid:
            self.credentials = self.authorize()

        # Construye el servicio de la API de YouTube v3 con las credenciales autorizadas
        return build('youtube', 'v3', credentials=self.credentials)

    # Chequea si ya contamos con las credenciales correspondientes o no
    def get_youtube_service(self):
        # En caso de no contar con credenciales dumpeadas las creo
        if not self.load_credentials():
            # Construye el servicio de la API de YouTube v3
            return self.build_service()
        else:
            # Carga las credenciales almacenadas
            self.credentials = self.load_credentials()
            # Construye y devuelve el servicio de la API de YouTube v3 con las credenciales cargadas
            return build('youtube', 'v3', credentials=self.credentials)

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

    # Lista los tracks de una playlist en particular de Youtube Music
    def search_playlist_tracks(self, id):
        # Obtén el servicio de la API de YouTube
        youtube = self.get_youtube_service()

        # Realiza la solicitud para obtener los detalles de la playlist
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=id,
            maxResults=50  # Puedes ajustar el número de resultados si es necesario
        ).execute()

        # Itera sobre los elementos de la playlist e imprime los títulos de los videos
        for item in playlist_response['items']:
            video_title = item['snippet']['title']
            print(video_title)
        
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