import os,pickle,pprint,sys,csv,json,requests,webbrowser
import spotipy
import tidal_api
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from youtube_api import YoutubeAPI
from openpyxl import Workbook

class TidalAPI:
    def __init__(self):
        # Carga de las variables de entorno desde el archivo .env
        load_dotenv()

        # Credenciales de las variables de entorno para utiliar API de Spotify
        self.TIDAL_CLIENT_ID = os.getenv('SP_CLIENT_ID')
        self.TIDAL_CLIENT_SECRET = os.getenv('SP_CLIENT_SECRET')
        self.TIDAL_REDIRECT_URI = os.getenv('SP_REDIRECT_URI')

        # URL de autorización
        authorization_url = 'https://auth.tidal.com/v1/oauth2/authorize'

        # Genera la URL de autorización
        authorization_params = {
            'client_id': self.TIDAL_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': self.TIDAL_REDIRECT_URI
        }
        authorization_response = requests.get(authorization_url, params=authorization_params)

        # Imprime la URL de autorización y solicita al usuario que autorice la aplicación
        print("Por favor, visita la siguiente URL para autorizar la aplicación:")
        print(authorization_response.url)
        authorization_code = input('Por favor, introduce el código de autorización: ')

        # Intercambio de código de autorización por token de acceso
        token_url = 'https://auth.tidal.com/v1/oauth2/token'
        payload = {
            'client_id': self.TIDAL_CLIENT_ID,
            'client_secret': self.TIDAL_CLIENT_SECRET,
            'redirect_uri': self.TIDAL_REDIRECT_URI,
            'code': authorization_code,
            'grant_type': 'authorization_code'
        }

        # Realiza la solicitud POST para obtener el token de acceso
        response = requests.post(token_url, data=payload)

        # Verifica si la solicitud fue exitosa
        if response.status_code == 200:
            access_token = response.json()['access_token']
            print("Token de acceso:", access_token)
        else:
            print("Error al obtener el token de acceso:", response.text)