import youtube_dl,os
from dotenv import load_dotenv

class YoutubeAPI:
    def __init__(self):
        self.YT_USER_ID = os.getenv('YT_USER_ID')

    def list_playlists(self):
        return