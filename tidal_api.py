import os,pickle,pprint,sys,csv,json
import spotipy
import tidalapi
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from youtube_api import YoutubeAPI
from openpyxl import Workbook

# Funciones auxiliares
from common_functions import create_download_folder

class TidalAPI:
    def __init__(self):
        # Carga de las variables de entorno desde el archivo .env
        load_dotenv()
        self.session_file = "tidal_credentials.pickle"
        # Credenciales de las variables de entorno para utiliar API de Spotify
        self.TIDAL_CLIENT_ID = os.getenv('TIDAL_CLIENT_ID')
        self.TIDAL_CLIENT_SECRET = os.getenv('TIDAL_CLIENT_SECRET')
        self.TIDAL_REDIRECT_URI = os.getenv('TIDAL_REDIRECT_URI')

    def service_login(self):
        try:
            if os.path.exists(self.session_file):
                # Si el archivo de sesión existe, cargar la sesión desde el archivo
                with open(self.session_file, 'rb') as f:
                    session = pickle.load(f)
            else:
                # Si el archivo de sesión no existe, iniciar una nueva sesión y guardarla en el archivo
                session = tidalapi.Session()
                session.login_oauth_simple()
                with open(self.session_file, 'wb') as f:
                    pickle.dump(session, f)
        except Exception as e:
            print(f"Error loading or saving the session: {e}")
            session = None
        return session

    # Listar las playlists del usuario en Tidal
    def list_playlists(self):
        counter = 0
        tracks = 0
        session = self.service_login()

        playlists = session.user.playlists()
        print(f"PLAYLISTS:{playlists}")

        print()
        print(f'My Tidal playlists:\n')
        for playlist in playlists:
            counter+=1
            tracks += playlist.num_tracks
            print(f'* {playlist.name} (id: {playlist.id})')
        
        print()
        print(f'Playlists found: {counter}')
        print(f'Total tracks found:{tracks}')

    # Lista los tracks con su información de una playlist en particular de Tidal
    def get_playlist_data(self, playlist_name):
        session = self.service_login()
        playlists = session.user.playlists()
        playlist_data = []
        for playlist in playlists:
            if playlist.name == playlist_name:
                for track in playlist.tracks():
                    playlist_data.append({
                    'track_name': track.name,
                    'artist': track.artist.name,
                    'album_name': track.album.name,
                    'album_release_date': track.album.year,
                    'playlist':playlist_name,
                    'service':'Tidal'
                })
        return playlist_data


    # Exporta la información de una playlist de Tidal en formáto CSV
    def get_playlist_csv(self,playlist_name):
        data_csv = [['track_title','artist','album','year','playlist','service']]
        session = self.service_login()
        playlist_data = self.get_playlist_data(playlist_name)
        for track in playlist_data:
            track_title = track['track_name']
            artist = track['artist']
            album = track['album_name']
            year = track['album_release_date']
            data_csv.append([track_title,artist,album,year,playlist_name,'Tidal'])

        file_path = os.path.join(create_download_folder(self,'csv'), playlist_name + "_tidal.csv")

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file_csv:
                escritor_csv = csv.writer(file_csv)
                for row in data_csv:
                    escritor_csv.writerow(row)

            print(f"CSV file '{file_path}' successfully created")
        except Exception as e:
            print(f"Error creating the CSV file: {e}")
    
    # Exporta la información de una playlist de Tidal en formáto JSON
    def get_playlist_json(self,playlist_name):
        data_json = []
        session = self.service_login()
        playlist_data = self.get_playlist_data(playlist_name)
        for track in playlist_data:
            track_title = track['track_name']
            artist = track['artist']
            album = track['album_name']
            year = track['album_release_date']
            data_json.append({'track_title':track_title,'artist':artist,'album':album,'year':year,'playlist':playlist_name,'service':'Tidal'})

        file_path = os.path.join(create_download_folder(self,'json'), playlist_name + "_tidal.json")
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data_json, file, indent=4, ensure_ascii=False)
                print(f"JSON file '{file_path}' successfully created")
        except Exception as e:
            print(f"Error creating the JSON file: {e}")
        
    # Exporta la información de una playlist de Tidal en formáto XLSX
    def get_playlist_xlsx(self,playlist_name):
        data_xlsx = []
        session = self.service_login()
        playlist_data = self.get_playlist_data(playlist_name)
        for track in playlist_data:
            track_title = track['track_name']
            artist = track['artist']
            album = track['album_name']
            year = track['album_release_date']
            data_xlsx.append({'track_title':track_title,'artist':artist,'album':album,'year':year,'playlist':playlist_name,'service':'Tidal'})
        # Crear un nuevo libro de trabajo de Excel
        try:
            wb = Workbook()
            sheet = wb.active
            sheet.title = playlist_name + ' tidal playlist info'

            # Escribir encabezados
            sheet.append(["Track title", "Artist", "Album", "Year","Playlist","Service"])

            # Escribir datos de la playlist
            for track in data_xlsx:
                sheet.append([track["track_title"], track["artist"], track["album"],track["year"],track["playlist"],track["service"]])

            # Guardar el libro de trabajo en un archivo Excel
            file = os.path.join(create_download_folder(self,'xlsx'), playlist_name + "_tidal.xlsx")
            wb.save(file)
            print(f"XLSX file successfully created")
        except Exception as e:
            print(f"Error creating the Excel file: {e}")