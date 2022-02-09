from core.models.music.music_models import Playlist
from helpers.consts import CollectionNames
from storage.files_database import AppDataBase


# optional: change app db to interface
class BasicApp:  # stateless (HTTP)
    def __init__(self, db: AppDataBase):
        self.db = db

    def search(self, user_id):
        pass


class AdvancedApp(BasicApp):  # state (CLI)
    def __init__(self, db):
        super().__init__(db)
        self.user = None

    def add_playlist(self, playlist_name, songs: [str]):
        new_playlist = Playlist(name=playlist_name, songs=songs)
        self.user.add_playlist(new_playlist)
        self.db.update_entity(CollectionNames.USERS_KEY, new_playlist)
