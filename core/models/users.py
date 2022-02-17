from typing import Dict, List

from helpers.consts import Limits, AccountTypes
from helpers.exceptions import ReachedFreePlaylistsLimit, ReachedFreePlaylistSongsLimit, PlaylistNameAlreadyExists

# CR: [MD] Filename `user.py``
class User:
    # CR: id shadows a built in name. It means you might have conflicts
    def __init__(self, id, password, playlists, account_type=AccountTypes.FREE):
        self.id: str = id
        self.password = password
        self.account_type: str = account_type
        # CR: [MD] Many times it's more coherent to name K/V (key/value) data types using X_by_Y naming. I.E. `playlist_by_name`
        # You might get rid of the comment as well if you do so
        self.playlists: Dict[str, List[str]] = playlists  # name and list of songs ids

    def add_playlist(self, name: str, songs: List[str]):
        if self.account_type == AccountTypes.FREE:
            if len(self.playlists) >= Limits.FREE_PLAYLISTS_NUM:
                raise ReachedFreePlaylistsLimit
            if len(songs) > Limits.FREE_PLAYLIST_SONGS_NUM:
                raise ReachedFreePlaylistSongsLimit
        if name in self.playlists:
            raise PlaylistNameAlreadyExists
        else:
            self.playlists[name] = songs
