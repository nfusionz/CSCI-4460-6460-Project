#!/usr/local/bin/python
# -*- coding: utf-8 -*-


"""
inverse_index.py - A module that provides an inverse index,
"""
from typing import Dict, Set


class InverseIndexCache:
    """
    Stores keyword-document url associations in memory.
    """

    def __init__(self):
        # TODO: Work on file interfacing for long-term storage
        self._index: Dict[str, Set[str]] = {}

    def add_url(self, *, keyword: str, url: str) -> None:
        """
        Adds a keyword-document association.

        :param keyword: The keyword to associate the document by.
        :param url: The url of the document.
        """
        if keyword in self._index:
            self._index[keyword].add(url)
        else:
            # Construct a new set with the keyword
            self._index[keyword] = {url}

    def remove_url(self, *, keyword: str, url: str) -> bool:
        """
        Removes the keyword-document association.

        :param keyword: The keyword of the association.
        :param url: The url of the document.
        :returns: If the operation was successful or not.
        """
        if keyword in self._index:
            urls = self._index[keyword]
            if url in urls:
                urls.remove(url)
                return True

        # No document with this association
        return False

    def get_documents(self, keyword: str) -> Set:
        """
        Gets all documents associated with a keyword.

        :param keyword: The keyword associated with the document.
        :return: A new Set containing all document urls associated with the keyword.
                 If there is no such keyword, return an empty set.
        """
        return self._index.get(keyword, set())
