import sys,argparse,subprocess

def main():
    # Módulos que se necesitan instalar
    modules = ['spotipy', 'tidalapi', 'openpyxl',  'python-dotenv', 'google_auth_oauthlib', 'google-api-python-client']

    # Instalar los modulos que no estén instalados en el sistema
    for module in modules:
        try:
            # Detecta si el módulo está instalado en el sistema
            __import__(module)
        except ImportError:
            print(f"Installing   {module}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install",  "--quiet", module])
    
    from spotify_api import SpotifyAPI
    from youtube_api import YoutubeAPI
    from tidal_api import TidalAPI

    spotify_api = SpotifyAPI()
    youtube_api = YoutubeAPI() 
    tidal_api = TidalAPI() 

    # Crear el parser
    parser = argparse.ArgumentParser(description='Gestión de playlists en Spotify y YouTube Music')

    # Agregar los argumentos
    parser.add_argument('platform', choices=['spotify', 'youtube','tidal'], help='Plataforma a interactuar (spotify o youtube)')
    parser.add_argument('destination', nargs='?', default=None, help='Servicio de destino de la playlist (opcional)')
    parser.add_argument('-l', action='store_true', help='Listar todas las playlists')
    parser.add_argument('-i', action='store_true', help='Mostrar información del usuario')
    parser.add_argument('-u', action='store_true', help='Actualizar credenciales')
    parser.add_argument('-c', metavar='PLAYLIST_NAME', help='Crear una playlist (especificar el nombre)')
    parser.add_argument('-t', metavar='PLAYLIST_NAME', help='Listar tracks de una playlist específica')
    parser.add_argument('-m', metavar='PLAYLIST_NAME', help='Migrar playlist de Spotify a YouTube Music')
    parser.add_argument('-csv', metavar='PLAYLIST_NAME', help='Descargar data de la playlist en un archivo CSV')
    parser.add_argument('-json', metavar='PLAYLIST_NAME', help='Descargar data de la playlist en un archivo JSON')
    parser.add_argument('-xlsx', metavar='PLAYLIST_NAME', help='Descargar data de la playlist en un archivo Excel')
    parser.add_argument('-ujson', metavar='PLAYLIST_NAME', help='Crea y carga una playlist con sus pistas desde un archivo JSON')
    parser.add_argument('-ucsv', metavar='PLAYLIST_NAME', help='Crea y carga una playlist con sus pistas desde un archivo CSV')
    parser.add_argument('-uxlsx', metavar='PLAYLIST_NAME', help='Crea y carga una playlist con sus pistas desde un archivo XLSX')

    # Parsear los argumentos
    args = parser.parse_args()

    if args.platform == 'spotify' and args.destination == 'youtube':
        if args.m:
            youtube_api.migrate_playlist_from_sp(args.m)
        else:
            print('Error: Falta el nombre de la playlist a migrar')
            
    if args.platform == 'youtube' and args.destination == 'spotify':
        if args.m:
            spotify_api.migrate_playlist_from_yt(args.m)
        else:
            print('Error: Falta el nombre de la playlist a migrar')

    # Realizar la acción correspondiente
    if args.platform == 'spotify' and args.destination is None:
        if args.l:
            spotify_api.list_playlists()
        elif args.i:
            spotify_api.user_info()
        elif args.t:
            spotify_api.search_playlist_tracks(args.t)
        elif args.c:
            spotify_api.create_playlist(args.c)
        elif args.csv:
            spotify_api.get_playlist_csv(args.csv)
        elif args.json:
            spotify_api.get_playlist_json(args.json)
        elif args.xlsx:
            spotify_api.get_playlist_xlsx(args.xlsx)
        elif args.ujson:
            spotify_api.upload_playlist_from_json(args.ujson)
        elif args.ucsv:
            spotify_api.upload_playlist_from_csv(args.ucsv)
        elif args.uxlsx:
            spotify_api.upload_playlist_from_xlsx(args.uxlsx)
        else:
            print('Error con los argumentos')
    elif args.platform == 'youtube' and args.destination is None:
        if args.l:
            youtube_api.list_playlists()
        elif args.i:
            youtube_api.user_info()
        elif args.u:
            youtube_api.update_credentials()
        elif args.t:
            youtube_api.search_playlist_tracks(args.t)
        elif args.c:
            youtube_api.create_playlist(args.c)
        elif args.csv:
            youtube_api.get_playlist_csv(args.csv)
        else:
            print('Error con los argumentos')
    elif args.platform == 'tidal' and args.destination is None:
        if args.l:
            tidal_api.list_playlists()
        elif args.csv:
            tidal_api.get_playlist_csv(args.csv)
        elif args.json:
            tidal_api.get_playlist_json(args.json)
        elif args.xlsx:
            tidal_api.get_playlist_xlsx(args.xlsx)
        elif args.ujson:
            tidal_api.upload_playlist_from_json(args.ujson)
        elif args.ucsv:
            tidal_api.upload_playlist_from_csv(args.ucsv)
        elif args.uxlsx:
            tidal_api.upload_playlist_from_xlsx(args.uxlsx)
        elif args.i:
            tidal_api.user_info()
        elif args.c:
            tidal_api.create_playlist(args.c)
        elif args.t:
            tidal_api.search_playlist_tracks(args.t)
    else:
        exit()

# script principal, invoca el main
if __name__ == "__main__":
    main()
