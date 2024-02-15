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
        if len(sys.argv) == 3 and sys.argv[1]=='youtube' and sys.argv[2]=='-l':
            youtube_api.list_playlists()
    else:
        print('Error con los argumentos')

if __name__ == "__main__":
    main()
