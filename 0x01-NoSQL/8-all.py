#!/usr/bin/env python3
""" MongoDB Operations with Python spesifc pymongo """


def list_all(mongo_collection):
    """ List all documents in Python """
    documents = mongo_collection.find()

    if documents.count() == 0:
        return []

    return documents
