# CR: same comment about name shadowing with id
class Song:
    # CR: [MD] Typing please. Is it a bird? Is it a plane?
    def __init__(self, id, name, album, popularity, artists):
        self.id = id
        self.name = name
        self.album = album
        self.popularity = popularity
        self.artists = artists


class Album:
    def __init__(self, id, name, artist, songs=None):
        self.id = id
        self.name = name
        self.artist = artist
        if not songs:
            songs = list()
        self.songs = songs

    def add_song(self, song):
        # CR: [MD] Have you considered using a `set` type (with derived changes to `Song` class)?
        if song not in self.songs:
            self.songs.append(song)


class Artist:
    def __init__(self, id, name, albums=None, ft_songs=None):  # CR: [MD] Why didn't you use a default value of `[]` here? (>>> trick question <<< remove this lol)
        self.id = id
        self.name = name
        # CR: [MD] Using the `or` statement would look cleaner
        # self.albums = albums or []
        # self.ft_songs = ft_songs or []
        if not albums:
            albums = list()  # CR: [MD] Using list() instead of [] isn't very pythonic, on top of being twice as slower (not that we count).
        self.albums = albums
        if not ft_songs:
            ft_songs = list()
        self.ft_songs = ft_songs

    # CR: [MD] If you want to "enforce" using these add methods, it's good practice to set the `albums` and `songs` properties to privates.
    def add_album(self, album):
        if album not in self.albums:  # CR: [MD] Have you considered using `set` instead of a `list` for your
            self.albums.append(album)

    def add_ft_songs(self, song):
        self.ft_songs.append(song)
