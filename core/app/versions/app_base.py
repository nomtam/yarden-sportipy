from typing import Dict, List

from core.models.music import Song, Album, Artist
from core.models.users import User
from helpers.consts import Limits
from helpers.exceptions import *
from storage.database import DocumentDataBase


class AppBase:
    def __init__(self, db: DocumentDataBase):
        self.db = db
        self.songs: Dict[str, Song] = self.load_entities("songs", Song)
        self.albums: Dict[str, Album] = self.load_entities("albums", Album)
        self.artists: Dict[str, Artist] = self.load_entities("artists", Artist)
        self.users: Dict[str, User] = self.load_entities("users", User)

    def load_entities(self, collection_name, cls: type):
        entities_docs = self.db.load_collection(collection_name)
        entities_objects = {}
        for entity_doc in entities_docs:
            entity_id = entity_doc["id"]
            if entity_id not in entities_objects:
                entities_objects[entity_id] = cls(**entity_doc)
        return entities_objects

    def add_playlist(self, user_id: str, playlist_name: str, songs: List[str]):
        user = self.users[user_id]
        try:
            user.add_playlist(playlist_name, songs)
        except PlaylistNameAlreadyExists:
            print(f"{user_id} tried to add a playlist with a name he already has")
        except ReachedFreePlaylistsLimit:
            print(f"{user_id} failed to add a playlist because he reached the free playlists num limit")
        except ReachedFreePlaylistSongsLimit:
            print(f"{user_id} failed to add a playlist because he reached the free playlist songs num limit")
        else:
            self.db.save_doc(user.__dict__, "users")  # save new user state to the db

    def limit_results(self, user_id, results):
        user_account_type = self.users[user_id].account_type
        if user_account_type == "free":
            results = results[:Limits.FREE_RESULTS_NUM]
        return results

    def get_album_name(self, album_id):
        return self.albums[album_id].name

    def get_song_name(self, song_id):
        return self.songs[song_id].name

    def get_album_songs_ids(self, album_id):
        return self.albums[album_id].songs

    def get_artist_albums_ids(self, artist_id):
        return self.artists[artist_id].albums

    def get_artist_songs_ids(self, artist_id):
        songs_ids = []
        for album_id in self.get_artist_albums_ids(artist_id):
            songs_ids.append(self.get_album_songs_ids(album_id))
        songs_ids.extend(self.artists[artist_id].ft_songs)
        return songs_ids

    def search_all_artists_names(self, user_id):
        return self.limit_results(user_id, [artist.name for artist in self.artists.values()])

    def search_artist_albums_names(self, user_id, artist_id):
        albums_ids = self.get_artist_albums_ids(artist_id)
        return self.limit_results(user_id, [self.get_album_name(album_id) for album_id in albums_ids])

    def search_artist_popular_songs(self, user_id, artist_id):
        artist_songs_ids = self.get_artist_songs_ids(artist_id)
        artist_songs = [self.songs[song_id] for song_id in artist_songs_ids]
        sorted_artist_songs = sorted(artist_songs, key=lambda song: song.popularity)
        return self.limit_results(user_id, [song.name for song in sorted_artist_songs][Limits.MAX_POPULAR_SONGS_NUM])

    def search_album_songs_names(self, user_id, album_id):
        album_songs_ids = self.get_album_songs_ids(album_id)
        return self.limit_results(user_id, [self.get_song_name(song_id) for song_id in album_songs_ids])
