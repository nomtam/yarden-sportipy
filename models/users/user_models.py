from typing import Dict
from abc import ABC
from models.music.music_models import Playlist


class User(ABC):
    def __init__(self, unique_id: str, username: str, playlists: Dict[str, Playlist], user_type="free"):
        self.id = unique_id
        self.username = username
        self.type = user_type
        self.playlists = playlists


class FreeUser(User):
    def __init__(self, unique_id: str, username: str, playlists: Dict[str, Playlist]):
        super().__init__(unique_id=unique_id, username=username, playlists=playlists)


class PremiumUser(User):
    def __init__(self, unique_id: str, username: str, playlists: Dict[str, Playlist]):
        super().__init__(unique_id=unique_id, username=username, playlists=playlists, user_type="premium")
