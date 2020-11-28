"""
document.py
"""
from typing import Dict

class Document:
	
    def __init__(self, url: str):
    	self._url: str = url
        self._keywords: Dict[str, Set[int]] = {}
        
    @property
    def url():
      	return self._url
  	
    def add_keyword(self, *, keyword: str, pos: int):
    	if keyword in self._keywords:
            self._keywords[str].add(pos)
      	else:
            self._keywords[str] = { pos }
            
    def diff(self, document: "Document") -> UpdateDocumentStrategy:
      	"""
        Returns an UpdateDocumentStrategy that contains the operations needed
        to go from the first document to the second.
        """
        removed_keywords = self._keywords.keys() - document._keywords.keys()
        new_keywords = document._keywords.keys() - self._keywords.keys()
		
