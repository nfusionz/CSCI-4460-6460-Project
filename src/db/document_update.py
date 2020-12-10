#!/usr/local/bin/python
# -*- coding: utf-8 -*-


from typing import Set, Optional

from common.document import Document
from db.inverse_index_cache import InverseIndexCache


class DocumentUpdateOperation:

    def __init__(self, *,
                 url: str,
                 add_keywords: Set[str],
                 remove_keywords: Set[str]):
        self._url = url
        self._add_keywords = add_keywords
        self._remove_keywords = remove_keywords

    def visit(self, index: InverseIndexCache):
        for keyword in self._remove_keywords:
            index.remove_url(keyword=keyword, url=self._url)

        for keyword in self._add_keywords:
            index.add_url(keyword=keyword, url=self._url)


def derive_document_update(*, new: Document, old: Optional[Document] = None) -> DocumentUpdateOperation:
    """
    Construct a update operation for one document. If there was
    no previous document, constructs an operation that adds the
    document.

    :param new: The document that replaces the old document.
    :param old: Defaults to None.
    :raise ValueError: If old exists, and the new url doesn't match.
    :return: The respective document update operation.
    """
    if old is not None and old.url != new.url:
        raise ValueError

    old_keys = set([key for key in old]) if old is not None else set()
    new_keys = set([key for key in new])

    add = new_keys.difference(old_keys)
    remove = old_keys.difference(new_keys)

    return DocumentUpdateOperation(url=new.url,
                                   add_keywords=add,
                                   remove_keywords=remove)
