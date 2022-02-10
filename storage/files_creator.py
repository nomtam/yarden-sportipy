"""This file was created for preparing the app db file. Files were already created (single-use code)."""
import glob
import os
from storage.reading import Reading
from storage.writing import Writing
from core.models.music import Song, Album, Artist
from helpers.config import *
from helpers.consts import DocumentKeys
import logging

logging.basicConfig(level=logging.INFO)

# create dicts of collections:
album_objects = {}
song_objects = {}
artist_objects = {}


def get_original_songs_jsons():
    # read songs original files:
    songs_jsons = []
    for filename in glob.glob(os.path.join(ORIGINAL_SONGS_ROOT_PATH, "*" + ORIGINAL_SONGS_EXTENSION)):
        songs_jsons.append(Reading.read_json(filename)[DocumentKeys.TRACK])
    return songs_jsons


def write_new_obj_files(path_template, objects):
    for obj_id, obj in objects.items():
        Writing.write_json(path_template % obj_id, obj.__dict__)


def create_song_obj(song_id, song_name, album_id, song_popularity, artists):
    song_objects[song_id] = Song(song_id, song_name, album_id, song_popularity,
                                 [artist[DocumentKeys.ID] for artist in artists])


def create_artist_obj(artist, owner_artist_id, album_id, song_id):
    artist_id = artist[DocumentKeys.ID]
    artist_name = artist[DocumentKeys.NAME]
    if artist_id not in artist_objects:
        artist_objects[artist_id] = Artist(artist_id, artist_name)
    if artist_id == owner_artist_id:
        artist_objects[artist_id].add_album(album_id)
    else:
        artist_objects[artist_id].add_ft_songs(song_id)


def create_album_obj(album_id, album_name, owner_artist_id, song_id):
    if album_id not in album_objects:
        album_objects[album_id] = Album(album_id, album_name, owner_artist_id)
    album_objects[album_id].add_song(song_id)


def build_objects_from_song(song):
    album_id = song[DocumentKeys.ALBUM][DocumentKeys.ID]
    album_name = song[DocumentKeys.ALBUM][DocumentKeys.NAME]
    artists = song[DocumentKeys.ARTISTS]  # list of dicts
    owner_artist_id = artists[0][DocumentKeys.ID]
    song_id = song[DocumentKeys.ID]
    song_name = song[DocumentKeys.NAME]
    song_popularity = song[DocumentKeys.POPULARITY]

    create_song_obj(song_id, song_name, album_id, song_popularity, artists)
    create_album_obj(album_id, album_name, owner_artist_id, song_id)
    for artist in artists:
        create_artist_obj(artist, owner_artist_id, album_id, song_id)


def main():
    # read songs original files:
    songs_jsons = get_original_songs_jsons()
    logging.info("Finished loading all original songs files")

    # create new objects for the app
    for song in songs_jsons:
        build_objects_from_song(song)
    logging.info("Finished loading all new objects files")

    # save the objects to documents
    write_new_obj_files(SONGS_FILENAME_TEMPLATE, song_objects)
    write_new_obj_files(ALBUMS_FILENAME_TEMPLATE, album_objects)
    write_new_obj_files(ARTISTS_FILENAME_TEMPLATE, artist_objects)
    logging.info("Finished writing the new objects to documents")


if __name__ == '__main__':
    main()
