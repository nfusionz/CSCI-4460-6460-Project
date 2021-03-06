#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
document_cache.py - A module that defines classes to store documents.
"""
from typing import Dict, Optional

from common.document import Document

# TODO: Figure out if some synchronization on this is necessary
from common.timestamped_document import TimestampedDocument


class DocumentCache:
    """
    Stores documents by their url in memory.
    """

    def __init__(self):
        # TODO: Work on file interfacing for long-term storage
        self._index: Dict[str, Document] = {}

    def add_document(self, document: Document) -> None:
        """
        Stores the document by it's url.

        :param document: The document to store.
        """
        self._index[document.url] = document

    def get_document(self, url: str) -> Optional[Document]:
        """
        Gets the associated document.

        :param url: The url of the document.
        :return: The document if it exists, otherwise, return None.
        """
        return self._index.get(url, None)
