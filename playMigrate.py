import sys
from spotify_api import SpotifyAPI

def main():
    spotify_api = SpotifyAPI()
    if len(sys.argv) > 1:
        # Listar todas las playlists del usuario
        if len(sys.argv) == 3 and sys.argv[1]=='spotify' and sys.argv[2]=='-l':
            spotify_api.list_playlists()
        # Listas los tracks de una playlist específica
        elif len(sys.argv) == 4 and sys.argv[1]=='spotify'and sys.argv[3]=='-l':
            spotify_api.search_playlist_tracks(sys.argv[2])
    else:
        print('Error con los argumentos')

if __name__ == "__main__":
    main()
