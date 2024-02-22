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
                return pickle.load(token)
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

    # Listar las playlists del usuario en YoutubeMusic
    def list_playlists(self):
        # Construye el servicio de la API de YouTube v3
        youtube = self.build_service()

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