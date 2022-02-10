import glob
import os
from storage.reading import Reading
from storage.writing import Writing
from core.models.music import Song, Album, Artist
from helpers.config import *

# read songs original files:
songs_jsons = []
for filename in glob.glob(os.path.join(ORIGINAL_SONGS_ROOT_PATH, "*" + ORIGINAL_SONGS_EXTENSION)):
    songs_jsons.append(Reading.read_json(filename)["track"])
print(len(songs_jsons))

# create dicts of collections:
album_objects = {}
song_objects = {}
artist_objects = {}

# split song json into parts:
for song in songs_jsons:
    album_id = song["album"]["id"]
    print(album_id)
    album_name = song["album"]["name"]
    artists = song["artists"]  # list of dicts
    owner_artist_id = artists[0]["id"]
    song_id = song["id"]
    song_name = song["name"]
    song_popularity = song["popularity"]

    # add to the dicts:
    # songs dict
    song_objects[song_id] = Song(song_id, song_name, album_id, song_popularity, [artist["id"] for artist in artists])
    # albums dict
    if album_id not in album_objects:
        album_objects[album_id] = Album(album_id, album_name, owner_artist_id)
    album_objects[album_id].add_song(song_id)
    # artists dict
    for artist in artists:
        artist_id = artist["id"]
        artist_name = artist["name"]
        if artist_id not in artist_objects:
            artist_objects[artist_id] = Artist(artist_id, artist_name)
        if artist_id == owner_artist_id:
            artist_objects[artist_id].add_album(album_id)
        else:
            artist_objects[artist_id].add_ft_songs(song_id)

# write new files:
# songs files
for song_id, song_obj in song_objects.items():
    # print(type(song_obj))
    Writing.write_json(SONGS_FILENAME_TEMPLATE % song_id, song_obj.__dict__)
    # print(Song(**Reading.read_json(SONGS_FILENAME_TEMPLATE % song_id)))
# albums files
for album_id, album_obj in album_objects.items():
    # print(type(album_obj))
    # print(album_obj.songs)
    Writing.write_json(ALBUMS_FILENAME_TEMPLATE % album_id, album_obj.__dict__)
    # print(Album(**Reading.read_json(ALBUMS_FILENAME_TEMPLATE % album_id)))
# artists files
for artist_id, artist_obj in artist_objects.items():
    Writing.write_json(ARTISTS_FILENAME_TEMPLATE % artist_id, artist_obj.__dict__)
    print(Artist(**Reading.read_json(ARTISTS_FILENAME_TEMPLATE % artist_id)))

# TODO: create and load users
