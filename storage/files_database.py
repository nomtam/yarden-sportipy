from typing import Dict

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

    def dump_entity(self, entity):
        full_path = self.meta_data.path_template % entity.id
        self.writer(full_path, entity)

    def load_entity(self, entity_id: str):
        full_path = self.meta_data.path_template % entity_id
        self.entities[entity_id] = self.reader(full_path)

    def set_entity(self, entity):
        self.entities[entity.id] = entity  # updates the entities dict
        self.dump_entity(entity)  # updates the entity file

    # TODO: check if valid id (raise exception if not)
    def get_entity(self, entity_id: str):
        if entity_id not in self.entities:  # load entity only if hasn't been loaded yet
            self.load_entity(entity_id)
        return self.entities[entity_id]


# this db is capable of loading collections of objects from various file types.
class AppDataBase:
    def __init__(self, **collections):
        self.collections: Dict[str, CollectionDataBase] = collections

    def update_entity(self, collection_key: str, entity):
        self.collections[collection_key].set_entity(entity)

    # TODO: delete
    def print_collections(self):
        print("collections: ", list(self.collections.keys()))


songs_meta = CollectionMetaData("songs", r"../resources/songs/song_%s.json")
songs_c = CollectionDataBase(meta_data=songs_meta, reader=Reading.read_json, writer=Writing.write_json)
print(songs_c.get_entity(r"0oHTvb0EVeYTUc0zscZphb"))
a = AppDataBase(songs=songs_c)
a.print_collections()
