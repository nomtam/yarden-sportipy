from typing import Dict
from abc import ABC
from models.music.music_models import Playlist


class User(ABC):
    def __init__(self, unique_id: str, username: str, playlists: Dict[str, Playlist]):
        self.id = unique_id
        self.username = username
        self.playlists = playlists
