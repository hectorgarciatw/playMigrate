import sys
from spotify_api import SpotifyAPI
from youtube_api import YoutubeAPI

def main():
    spotify_api = SpotifyAPI()
    youtube_api = YoutubeAPI() 
    if len(sys.argv) > 1:
        # Listar todas las playlists del usuario en Spotify
        if len(sys.argv) == 3 and sys.argv[1]=='spotify' and sys.argv[2]=='-l':
            spotify_api.list_playlists()
        # Información del usuario de Spotify
        elif len(sys.argv) == 3 and sys.argv[1]=='spotify' and sys.argv[2]=='-i':
            spotify_api.user_info()    
        # Listas los tracks de una playlist específica en Spotify
        elif len(sys.argv) == 4 and sys.argv[1]=='spotify'and sys.argv[3]=='-l':
            spotify_api.search_playlist_tracks(sys.argv[2])
        # Listar todas las playlists del usuario en Youtube
        elif len(sys.argv) == 3 and sys.argv[1]=='youtube' and sys.argv[2]=='-l':
            youtube_api.list_playlists()
        # Información del usuario de Spotify
        elif len(sys.argv) == 3 and sys.argv[1]=='youtube' and sys.argv[2]=='-i':
            youtube_api.user_info()    
        # Listas los tracks de una playlist específica en Youtube Music
        elif len(sys.argv) == 4 and sys.argv[1]=='youtube'and sys.argv[3]=='-l':
            youtube_api.search_playlist_tracks(sys.argv[2])
        # Actualizo las credenciales del usuario de Youtube Music
        elif len(sys.argv) == 3 and sys.argv[1]=='youtube'and sys.argv[2]=='-u':
            youtube_api.update_credentials()
        # Creamos una playlist de Youtube Music desde cero
        elif len(sys.argv) == 4 and sys.argv[1]=='youtube' and sys.argv[3]=='-c':
            youtube_api.create_playlist(sys.argv[2])
        # Migrando playlist de Spotify a Youtube Music
        elif len(sys.argv) == 5 and sys.argv[1]=='spotify' and sys.argv[2]=='youtube' and sys.argv[4]=='-m':
            youtube_api.migrate_playlist_from_sp(sys.argv[3])
    else:
        print('Error con los argumentos')

if __name__ == "__main__":
    main()
