import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class YoutubeAPI:

    # Define los alcances de la API de YouTube v3
    SCOPES = ['https://www.googleapis.com/auth/youtube.readonly','https://www.googleapis.com/auth/youtube']

    #Listar las playlists del usuario en YoutubeMusic
    def list_playlists(self):
        # Inicia el flujo de autorización de OAuth2
        flow = InstalledAppFlow.from_client_secrets_file('./client_secret_249986949363-k8ro9gijcpevkmpap9va4gq7neojcegq.apps.googleusercontent.com.json', self.SCOPES)
        credentials = flow.run_local_server(port=0)

        # Construye el servicio de la API de YouTube v3
        youtube = build('youtube', 'v3', credentials=credentials)

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
        exit() #Revisar el problema de reabrir login de usuario

    def __init__(self):
        self.list_playlists()