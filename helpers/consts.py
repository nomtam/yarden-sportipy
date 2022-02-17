class CollectionNames:
    SONGS_KEY = "songs"
    ALBUMS_KEY = "albums"
    USERS_KEY = "users"
    ARTISTS_KEY = "artists"


class AccountTypes:
    FREE = "free"
    PREMIUM = "premium"
    ARTIST = "artist"


class DocumentKeys:
    ID = "id"
    NAME = "name"
    ALBUM = "album"
    TRACK = "track"
    ARTISTS = "artists"
    POPULARITY = "popularity"

# CR: FreeLimits, and then you don't have to use the word FREE 3 times
# CR: [MD] I'd expect to have these values configurable.
class Limits:
    FREE_PLAYLISTS_NUM = 5
    FREE_PLAYLIST_SONGS_NUM = 20
    FREE_RESULTS_NUM = 5
    MAX_POPULAR_SONGS_NUM = 10
