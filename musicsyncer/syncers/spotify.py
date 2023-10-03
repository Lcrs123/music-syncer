from spotipy import Spotify
from spotipy.oauth2 import SpotifyPKCE
from musicsyncer.syncers.base_syncer import Syncer
from musicsyncer.syncers.utils import TrackInfo

class SpotifySyncer(Syncer):
    name = 'Spotify'
    SPOTIFY_CLIENT_ID = '05b80e45a962450b9db98ea87b8aa70f'
    SCOPE = 'user-library-read,user-library-modify'
    REDIRECT_URI = 'http://localhost:8888/callback'

    def __init__(self,API_getter:type[Spotify]=Spotify,auth_manager:type[SpotifyPKCE]=SpotifyPKCE) -> None:
        self.auth_manager = auth_manager(
            client_id=self.SPOTIFY_CLIENT_ID,
            redirect_uri=self.REDIRECT_URI,
            scope=self.SCOPE
        )
        self.API_getter = API_getter(auth_manager=self.auth_manager)


    def get_song_list(self,limit:int=50,offset=0) -> list[TrackInfo]:
        track_items = []
        current_tracks = self.API_getter.current_user_saved_tracks(limit=limit,offset=offset)['items']
        while len(current_tracks) == limit:
            track_items.extend(current_tracks)
            offset += limit
            current_tracks = self.API_getter.current_user_saved_tracks(limit=limit,offset=offset)['items']
        track_items.extend(current_tracks)
        track_names = [x['track']['name'] for x in track_items]
        artist_names = [x['track']['artists'][0]['name'] for x in track_items]
        return [TrackInfo(artist_name=x,track_name=y) for x,y in zip(artist_names,track_names)]

    def like_song(self,id:str):
        return