import os,pickle,json,time,csv
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Funciones auxiliares
from common_functions import create_download_folder

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

        total_playlists = len(response['items'])
        total_tracks = 0

        # Imprime las listas de reproducción del usuario
        print()
        print(f'My Youtube Music playlists:\n')
        for playlist in response['items']:
            print(f'* {playlist["snippet"]["title"]} (id: {playlist["id"]})')
            # Realiza una solicitud para obtener los detalles de la lista de reproducción
            playlist_id = playlist['id']
            playlist_details = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50  # Ajusta el número de resultados por página
            ).execute()
    
            # Suma la cantidad de pistas en esta lista de reproducción a la cantidad total de pistas
            total_tracks += len(playlist_details['items'])
            print()
        print(f'Playlists found: {total_playlists}')
        print(f'Total tracks found: {total_tracks}')


    def get_playlist_id_by_name(self, playlist_name):
        # Obtén el servicio de la API de YouTube
        youtube = self.get_youtube_service()

        # Realiza la solicitud para obtener las listas de reproducción del usuario
        request = youtube.playlists().list(
            part='id,snippet',
            mine=True,
            maxResults=100
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
        cont = 0
        # Obtén el servicio de la API de YouTube
        youtube = self.get_youtube_service()
        # Obtén el ID de la lista de reproducción
        playlist_id = self.get_playlist_id_by_name(playlist_name)

        if not playlist_id:
            print("The playlist '{}' was not found.".format(playlist_name))
            return
        
        # Realiza la solicitud para obtener los detalles de la playlist
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=1000
        ).execute()

        counter = playlist_response.get('pageInfo', {}).get('totalResults', 0)

        print()
        # Itera sobre las páginas de resultados
        while playlist_response:
            cont+=1
            print(f'Playlist \"{playlist_name}\" with {counter}  tracks found: \n')
            # Itera sobre los elementos de la playlist e imprime los títulos de los videos
            for item in playlist_response['items']:
                audio_title = item['snippet']['title']
                print(f'* {audio_title}')

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
                break
        print()
        print(f'Playlist Id: \"{playlist_id}\"')
        
    def get_playlist_tracks(self, playlist_name):
        # Obtén el servicio de la API de YouTube
        youtube = self.get_youtube_service()
        # Obtén el ID de la lista de reproducción
        playlist_id = self.get_playlist_id_by_name(playlist_name)

        if not playlist_id:
            print("The playlist '{}' was not found.".format(playlist_name))
            return None
    
        tracks_info = []  # Lista para almacenar la información de las pistas

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
                # Extrae la información relevante del elemento y agrégala al diccionario
                track_info = {
                    'track_id': item['snippet']['resourceId']['videoId'],
                    'track_name': item['snippet']['title'],
                }
                tracks_info.append(track_info)
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
                break
        return tracks_info

    # Retorna información del usuario de Youtube Music
    def user_info(self):
        # Obtén el servicio de la API de YouTube
        youtube = self.get_youtube_service()

        # Obtiene la información del usuario
        user_info_response = youtube.channels().list(part='snippet', mine=True).execute()
        user_info = user_info_response['items'][0]['snippet']

        print("User info:")
        print("Username:", user_info['title'])
        print("Descriprion:", user_info.get('description', 'Not available'))
        print("Country:", user_info.get('country', 'Not available'))

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


    def migrate_playlist_from_sp(self, spotify_api, playlist_name):
        # Get the YouTube service
        youtube = self.get_youtube_service()
        sp_playlist_data = spotify_api.get_playlist_data(playlist_name)

        try:
            # Creamos una playlist vacía
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
                    if cont % 5 == 0:
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
                    print(f"Track '{track_name}' successfully added to the playlist.")
                    cont += 1
                else:
                    print(f"No track found for the song '{track_name}'.")
        except HttpError as e:
            if e.resp.status == 403:
                print('😢 The program stops due to exceeding the quota provided by YouTube Music, please try again later.')
            else:
                # Captura cualquier otro error HTTP y muestra detalles
                print("An HTTP error occurred:", e)
        except Exception as ex:
            print("Sorry, an error occurred:", ex)

            # Get the YouTube service
            youtube = self.get_youtube_service()
            sp_playlist_data = spotify_api.get_playlist_data(playlist_name)

            try:
                # Creamos una playlist vacía
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
                        if cont % 5 == 0:
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
                        print(f"Track '{track_name}' successfully added to the playlist.")
                        cont += 1
                    else:
                        print(f"No track found for the song '{track_name}'.")
            except HttpError as e:
                if e.resp.status == 403:
                    print("😢 The program has stopped due to exceeding the quota provided by YouTube Music, please try again later.")
                else:
                    # Captura cualquier otro error HTTP y muestra detalles
                    print("An HTTP error occurred:", e)
            except Exception as ex:
                print("An error occurred:", ex)

            # Get the YouTube service
            youtube = self.get_youtube_service()
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
            batch_size = 50
            # Agrupar las pistas de Spotify en lotes más pequeños
            tracks_batches = [sp_playlist_data['tracks'][i:i + batch_size] for i in range(0, len(sp_playlist_data['tracks']), batch_size)]

        
            # Migrar cada lote de pistas
            for batch_index, batch in enumerate(tracks_batches):
                print(f"Processing batch {batch_index + 1}...")
                for track in batch:
                    # Obtener información de la pista
                    artist_name = track['artist']
                    track_name = track['track_name']

                    # Inicializar variables para paginación
                    page_token = None
                    video_id = None

                    # Realizar búsqueda con paginación hasta encontrar un video válido
                    while not video_id:
                        try:
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
                        except HttpError as e:
                            
                            # Verificar si la excepción es por exceso de cuota
                            if e.resp.status == 403 and 'quotaExceeded' in e.content:
                                print('😢 The program has stopped due to exceeding the quota provided by Youtube Music, please try again later')
                                return  # Salir de la función si la cuota está excedida
                            else:
                                raise  # Re-levantar la excepción si no es por cuota excedida

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
                        print(f"Track '{track_name}' successfully added to the playlist")
                    else:
                        print(f"No track found for the song '{track_name}'.")
        
                print(f"Batch {batch_index + 1} processed. Waiting 2 seconds before continuing with the next batch...")
                time.sleep(2)  # Esperar 2 segundos entre lotes

            print("Migration completed")
            
            
            
            
    # Obtiene información de una playlist de Youtube Music
    def get_playlist_info(self,playlist_id):
        # Obtén el servicio de la API de YouTube
        youtube = self.get_youtube_service()
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=100  # Esto limita a 50 resultados por solicitud, puedes ajustarlo según tus necesidades
        )
        response = request.execute()
        return response
        playlist_id = self.get_playlist_id_by_name(playlist_name)
        # Obtengo la informacion de la playlist de Youtube Music
        playlist_data = self.get_playlist_info(playlist_id)
        for item in playlist_data['items']:
            track_title = item['snippet']['title']
            artist = ""  # Inicializamos el artista como una cadena vacía
            album = item['snippet']['title']  # Podemos asignar el título de la pista al álbum por ahora
            year = ""  # No hay información del año en la lista de reproducción
            playlist = playlist_name
            service = 'YouTube Music'

            # Obtenemos información adicional sobre la pista para encontrar el artista
            video_id = item['snippet']['resourceId']['videoId']
            track_info = self.get_video_info(video_id)
            if 'artist' in track_info:
                artist = track_info['artist']

            data_csv.append([track_title, artist, album, year, playlist, service])

        file_path = os.path.join(create_download_folder(self,'csv'), playlist_name + "_youtube.csv")

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file_csv:
                csv_writer = csv.writer(file_csv)
                for row in data_csv:
                    csv_writer.writerow(row)

            print(f"CSV file '{file_path}' successfully created")
        except Exception as e:
            print(f"Error creating the CSV file: {e}")    