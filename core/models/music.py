class Song:
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
        if song not in self.songs:
            self.songs.append(song)


class Artist:
    def __init__(self, id, name, albums=None, ft_songs=None):
        self.id = id
        self.name = name
        if not albums:
            albums = list()
        self.albums = albums
        if not ft_songs:
            ft_songs = list()
        self.ft_songs = ft_songs

    def add_album(self, album):
        if album not in self.albums:
            self.albums.append(album)

    def add_ft_songs(self, song):
        self.ft_songs.append(song)
