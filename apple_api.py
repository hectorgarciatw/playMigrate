import os,pickle,pprint,sys,csv,json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from youtube_api import YoutubeAPI
from openpyxl import Workbook

class AppleAPI:
    def __init__(self):
        # Carga de las variables de entorno desde el archivo .env
        load_dotenv()