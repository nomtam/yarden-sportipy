from typing import Dict, List


class User:
    def __init__(self, id, password, playlists, account_type="free"):
        self.id: str = id
        self.password = password
        self.account_type: str = account_type
        self.playlists: Dict[str, List[str]] = playlists  # name and list of songs ids

    def add_playlist(self, name: str, songs: List[str]):
        self.playlists[name] = songs
