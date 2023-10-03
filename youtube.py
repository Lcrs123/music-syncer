from ytmusicapi import YTMusic

yt = YTMusic('oauth.json')
liked_songs = yt.get_liked_songs(999)