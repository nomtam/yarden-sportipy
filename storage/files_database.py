from storage.reading import Reading
from storage.writing import Writing


class CollectionMetaData:
    def __init__(self, name, path_template):
        self.name: str = name
        self.path_template = path_template


class CollectionDataBase:
    def __init__(self, meta_data: CollectionMetaData, reader: staticmethod, writer: staticmethod):
        self.meta_data = meta_data
        self.reader = reader
        self.writer = writer
        self.entities = {}

    def get_entity(self, entity_id: str):
        full_path = self.meta_data.path_template % entity_id
        return self.reader(full_path)


# this db is capable of loading collections of objects from various file types.
class AppDataBase:
    def __init__(self, **collections):
        self.collections = collections

    def print_collections(self):
        print("collections: ", list(self.collections.keys()))


songs_meta = CollectionMetaData("songs", r"../resources/songs/song_%s.json")
songs_c = CollectionDataBase(meta_data=songs_meta, reader=Reading.read_json, writer=Writing.write_json)
print(songs_c.get_entity(r"0oHTvb0EVeYTUc0zscZphb"))
a = AppDataBase(songs=songs_c)
a.print_collections()
