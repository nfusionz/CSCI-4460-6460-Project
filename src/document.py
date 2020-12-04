""" 
document.py - A module that provides structures and functions to represent a document.
"""

from typing import List


class Document:
    """ 
    A class that stores information relevant to a document: 
    - The URL
    - The title
    - The keywords

    This class is iterable over the keywords.
    """

    def __init__(self, *,
                 url: str,
                 title: List[str],
                 keywords: List[str]):
        self._url: str = url
        self._title: List[str] = title
        self._keywords: List[str] = keywords

    @property
    def url(self) -> str:
        """
        :returns: The URL for this document.
        """
        return self._url


class DocumentBuilder:
    """
    A class to build a Document by the keyword.
    """

    def __init__(self, *,
                 url: str,
                 title: List[str]):
        self._url: str = url
        self._title: List[str] = title
        self._keywords: List[str] = []

    def add(self, keyword: str) -> None:
        """
        :param keyword: A keyword to add to the builder internal state.
        """
        self._keywords += keyword

    @property
    def document(self) -> Document:
        """
        :returns: A new Document from the internal state.
        """
        return Document(url=self._url,
                        title=self._title,
                        keywords=self._keywords)
