import os,pickle,pprint,sys,csv,json
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