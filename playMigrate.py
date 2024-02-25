import sys,argparse
from spotify_api import SpotifyAPI
from youtube_api import YoutubeAPI

def main():
    spotify_api = SpotifyAPI()
    youtube_api = YoutubeAPI() 
    
    # Crear el parser
    parser = argparse.ArgumentParser(description='Gestión de playlists en Spotify y YouTube Music')

    # Agregar los argumentos
    parser.add_argument('platform', choices=['spotify', 'youtube'], help='Plataforma a interactuar (spotify o youtube)')
    parser.add_argument('destination', nargs='?', choices=['spotify', 'youtube'], default=None, help='Servicio de destino de la playlist (opcional)')
    parser.add_argument('-l', action='store_true', help='Listar todas las playlists')
    parser.add_argument('-i', action='store_true', help='Mostrar información del usuario')
    parser.add_argument('-u', action='store_true', help='Actualizar credenciales')
    parser.add_argument('-c', metavar='PLAYLIST_NAME', help='Crear una playlist (especificar el nombre)')
    parser.add_argument('-t', metavar='PLAYLIST_NAME', help='Listar tracks de una playlist específica')
    parser.add_argument('-m', metavar='PLAYLIST_NAME', help='Migrar playlist de Spotify a YouTube Music')

    # Parsear los argumentos
    args = parser.parse_args()

    if args.platform == 'spotify' and args.destination == 'youtube':
        if args.m:
            youtube_api.migrate_playlist_from_sp(args.m)
        else:
            print('Error: Falta el nombre de la playlist a migrar')

    # Realizar la acción correspondiente
    if args.platform == 'spotify':
        if args.l:
            spotify_api.list_playlists()
        elif args.i:
            spotify_api.user_info()
        elif args.t:
            spotify_api.search_playlist_tracks(args.t)
        else:
            print('Error con los argumentos')
    elif args.platform == 'youtube':
        if args.l:
            youtube_api.list_playlists()
        elif args.i:
            youtube_api.user_info()
        elif args.u:
            youtube_api.update_credentials()
        elif args.c:
            youtube_api.create_playlist(args.c)
        else:
            print('Error con los argumentos')
    else:
        print('Error con los argumentos')

# script principal, invoca el main
if __name__ == "__main__":
    main()
