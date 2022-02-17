import glob
import os
from collections import defaultdict
from typing import Dict
from helpers.consts import DocumentKeys


class CollectionMetaData:
    def __init__(self, name, root_path, filename_template):
        self.name: str = name
        self.root_path = root_path
        self.filename_template = filename_template


class DocumentDataBase:
    # CR: [MD] You can't REALLY enforce DI in python, but if you do try, use a better typehint.
    # I.E. A reader class instead of a function.
    # Even if you do choose to accept a function, `staticmethod` isn't for hinting. Use `typing.Callable` with expected arguments and a return type
    def __init__(self, collections_metadata: Dict[str, CollectionMetaData], reader: staticmethod, writer: staticmethod,
                 doc_extension):
        self.collections_metadata = collections_metadata
        self.collections = defaultdict(lambda: dict())  # CR: [MD] Redundant `lambda``, using `dict` is sufficient
        self.doc_extension = doc_extension
        self.reader = reader
        self.writer = writer

    # CR: [MD] Function docstring should be placed between triple quotes, not a mere comment
    # receives collection name and returns a list of docs
    def load_collection(self, collection_name):
        metadata = self.collections_metadata[collection_name]
        json_docs = []
        # CR: same as in files_creator. from glob import glob
        # CR: why *? comment explanation when leaving a magic string
        for filename in glob.glob(os.path.join(metadata.root_path, "*" + self.doc_extension)):
            json_docs.append(self.reader(filename))
        return json_docs

    def save_doc(self, doc, collection_name):
        # CR: [MD] This class seems to be your DAL for the app.
        # It'd be a good place to keep the mapping between the object you with to save and it's respective collection.
        # There's no reason for the main app to know where (or 'how' for that matter) the User is saved, or that it is saved in a collection.
        # Also, would I ever want to save a User object to the songs collection? Why allow such unwated behavior in the first place?
        metadata = self.collections_metadata[collection_name]
        # CR: same as using magic strings. When using special math you have to explain why (the %)
        # CR: [MD] I disagree. Again, a commonly known instance of an operator.
        # It DOES look funny because we're not c developers + there are no hints so it's unclear that this is a string templating operation.
        # Use `.format` instead.
        filename = metadata.filename_template % doc[DocumentKeys.ID]
        self.writer(filename, doc)
