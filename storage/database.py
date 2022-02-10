import glob
import os
from collections import defaultdict
from typing import Dict


class CollectionMetaData:
    def __init__(self, name, root_path, filename_template):
        self.name: str = name
        self.root_path = root_path
        self.filename_template = filename_template


class DocumentDataBase:
    def __init__(self, collections_metadata: Dict[str, CollectionMetaData], reader: staticmethod, writer: staticmethod,
                 doc_extension):
        self.collections_metadata = collections_metadata
        self.collections = defaultdict(lambda: dict())
        self.doc_extension = doc_extension
        self.reader = reader
        self.writer = writer

    # receives collection name and returns a list of json docs
    def load_collection(self, collection_name):
        metadata = self.collections_metadata[collection_name]
        json_docs = []
        for filename in glob.glob(os.path.join(metadata.root_path, "*" + self.doc_extension)):
            json_docs.append(self.reader(filename))
        return json_docs

    def save_doc(self, json_doc, collection_name):
        metadata = self.collections_metadata[collection_name]
        filename = metadata.filename_template % json_doc["id"]
        self.writer(filename, json_doc)

