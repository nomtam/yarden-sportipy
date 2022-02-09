from typing import Dict
from abc import ABC
from core.models.music import Playlist


class User(ABC):
    def __init__(self, unique_id, username, playlists, user_type="free"):
        self.id: str = unique_id
        self.username: str = username
        self.type: str = user_type
        self.playlists: Dict[str, Playlist] = playlists


class FreeUser(User):
    def __init__(self, unique_id, username, playlists):
        super().__init__(unique_id=unique_id, username=username, playlists=playlists)


class PremiumUser(User):
    def __init__(self, unique_id, username, playlists):
        super().__init__(unique_id=unique_id, username=username, playlists=playlists, user_type="premium")


class Artist(PremiumUser):
    def __init__(self, unique_id, username, playlists, albums):
        super().__init__(unique_id=unique_id, username=username, playlists=playlists)
        self.albums: Dict[str, str] = albums
