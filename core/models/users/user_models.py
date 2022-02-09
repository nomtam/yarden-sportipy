from typing import Dict
from abc import ABC

from core.models.music.music_models import Playlist
from helpers.exceptions import PlaylistNameAlreadyExists, ReachedFreePlaylistsLimit


class User(ABC):
    def __init__(self, unique_id, username, password, playlists, user_type="free"):
        self.id: str = unique_id
        self.username: str = username
        self.password = password
        self.type: str = user_type
        self.playlists: Dict[str, Playlist] = playlists

    def add_playlist(self, playlist: Playlist):
        if playlist.name not in self.playlists:
            self.playlists[playlist.name] = playlist
        else:
            raise PlaylistNameAlreadyExists


class FreeUser(User):
    def __init__(self, unique_id, username, password, playlists):
        super().__init__(unique_id=unique_id, username=username, password=password, playlists=playlists)

    def limit_playlists(self, add_playlist):
        from helpers.consts import FreeUserLimits

        def limit(playlist_name, songs):
            if len(self.playlists) < FreeUserLimits.MAX_PLAYLISTS_NUM:
                add_playlist(playlist_name, songs)
            else:
                raise ReachedFreePlaylistsLimit

        return limit

    @limit_playlists
    def add_playlist(self, playlist: Playlist):
        super().add_playlist(playlist)


class PremiumUser(User):
    def __init__(self, unique_id, username, password, playlists):
        super().__init__(unique_id=unique_id, username=username, password=password, playlists=playlists,
                         user_type="premium")


class Artist(PremiumUser):
    def __init__(self, unique_id, username, password, playlists, albums):
        super().__init__(unique_id=unique_id, username=username, password=password, playlists=playlists)
        self.albums: Dict[str, str] = albums
