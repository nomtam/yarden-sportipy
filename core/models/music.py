class Song:
    def __init__(self, id, name, album, popularity, artists):
        self.id = id
        self.name = name
        self.album = album
        self.popularity = popularity
        self.artists = artists


class Album:
    def __init__(self, id, name, artist, songs=[]):
        self.id = id
        self.name = name
        self.artist = artist
        self.songs = songs

    def add_song(self, song):
        if song not in self.songs:
            self.songs.append(song)


class Artist:
    def __init__(self, id, name, albums=[], ft_songs=[]):
        self.id = id
        self.name = name
        self.albums = []
        self.ft_songs = []

    def add_album(self, album):
        if album not in self.albums:
            self.albums.append(album)

    def add_ft_songs(self, song):
        self.ft_songs.append(song)
