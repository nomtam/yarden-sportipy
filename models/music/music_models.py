from typing import Dict


class Song:
    def __init__(self, unique_id, name, album, artists, popularity):
        self.id: str = unique_id
        self.name: str = name
        self.album: Dict[str, str] = album
        self.artists: Dict[str, str] = artists
        self.popularity: int = popularity


class Playlist:
    def __init__(self, name, songs):
        self.name: str = name
        self.songs: Dict[str, str] = songs
