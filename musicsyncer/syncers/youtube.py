from musicsyncer.syncers.base_syncer import Syncer
from ytmusicapi import YTMusic
from musicsyncer.syncers.utils import TrackInfo

class YouTubeSyncer(Syncer):
    name = 'YouTube'

    def __init__(self,APIGetter = YTMusic, auth:str='oauth.json') -> None:
        self.APIGetter = APIGetter(auth)

    def get_song_list(self) -> list[TrackInfo]:
        track_items = self.APIGetter.get_liked_songs(limit=999999)['tracks']
        track_names = [x['title'] for x in track_items]
        artist_names = [x['artists'][0]['name'] for x in track_items]
        return [TrackInfo(artist_name=x,track_name=y) for x,y in zip(artist_names,track_names)]

    def like_song(self,video_id:str):
        return self.APIGetter.rate_song(videoId=video_id,rating='LIKE')