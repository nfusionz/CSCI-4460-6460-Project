"""
index_db.py
"""
from typing import Dict, Set

class KeywordCache:

    def __init__(self):
        self._index: Dict[str, DocumentPositions] = {}

    def add_document(self, *, keyword: str, pos: Set[int]):
        pass


class DocumentPositions:

    def __init__(self):
        self._documents: Dict[str, Set[int]] = {}

    def add_document(self, *, doc: str, pos: Set[int]):
        pass

    def remove_document(self, doc: str):
        pass
