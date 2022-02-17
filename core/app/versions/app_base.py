# CR: [MD] Why is it inside a `versions` module?
import logging
from typing import Dict, List

from core.models.music import Song, Album, Artist
from core.models.users import User
from helpers.consts import Limits, CollectionNames, DocumentKeys, AccountTypes
from helpers.exceptions import *
from storage.database import DocumentDataBase

# CR: this class might not be named GodClass but it's a god class.
#  it loads data, searches on it and lets you save data
# CR: [MD] The wording 'Base' is usually reserved used in a class name when it's an abstract one. 'App' is great here
class AppBase:
    def __init__(self, db: DocumentDataBase):
        self.db = db
        self.songs: Dict[str, Song] = self.load_entities(CollectionNames.SONGS_KEY, Song)
        self.albums: Dict[str, Album] = self.load_entities(CollectionNames.ALBUMS_KEY, Album)
        self.artists: Dict[str, Artist] = self.load_entities(CollectionNames.ARTISTS_KEY, Artist)
        self.users: Dict[str, User] = self.load_entities(CollectionNames.USERS_KEY, User)
        logging.info("Finished loading all app entities")

    # CR: why not in helper?
    def load_entities(self, collection_name, cls: type):
        entities_docs = self.db.load_collection(collection_name)
        entities_objects = {}
        for entity_doc in entities_docs:
            entity_id = entity_doc[DocumentKeys.ID]
            if entity_id not in entities_objects:
                entities_objects[entity_id] = cls(**entity_doc)
        return entities_objects

    # CR: why is this here? SRP for the class. Why not make a user class?
    def add_playlist(self, user_id: str, playlist_name: str, songs: List[str]):
        user = self.users[user_id]
        try:
            user.add_playlist(playlist_name, songs)
        except PlaylistNameAlreadyExists:
            logging.info(f"{user_id} tried to add a playlist with a name he already has")
        except ReachedFreePlaylistsLimit:
            logging.info(f"{user_id} failed to add a playlist because he reached the free playlists num limit")
        except ReachedFreePlaylistSongsLimit:
            logging.info(f"{user_id} failed to add a playlist because he reached the free playlist songs num limit")
        else:
            # CR: [MD] Useless comment
            self.db.save_doc(user.__dict__, CollectionNames.USERS_KEY)  # save new user state to the db

    def limit_results(self, user_id, results):
        # CR: [MD] Something to think about -
        # We'd want to be able to tell the DAL (in this case the database module) what the limits are with each access.
        # For in the real world we'd save both network bandwidth (when querying results from a REST service or a DB) and processing time.

        # CR: What if id doesn't exist? [MD] A KeyError exception of course
        user_account_type = self.users[user_id].account_type
        if user_account_type == AccountTypes.FREE:
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

    # CR: why is this here? Why not make a search module? combining all here is an SRP breach
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
