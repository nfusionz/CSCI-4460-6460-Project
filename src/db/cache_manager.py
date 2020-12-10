#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
cache_manager.py - A module that defines a class to control access to the inverse index.
"""
import asyncio
import threading  # For lock object
from concurrent.futures import Executor
from typing import Set, List, Optional
from queue import Queue, Empty

from db.document_cache import DocumentCache
from db.inverse_index_cache import InverseIndexCache
from db.document_update import derive_document_update, DocumentUpdateOperation
from common.document import Document


class ManagedLockCounter:
    """
    An Asynchronous Context Manager for a semaphore that manages a lock
    when the semaphore is below it's initial value, and releases it when 
    the semaphore returns to it's initial value.

    Note that this class is not thread-safe, as it uses asyncio primitives
    and should only be executed from asyncio based code.

    Example:
        async with ManagedLockCounter(lock):
            # Do operations
    """

    def __init__(self, managed: threading.Lock, value=1):
        self._managed = managed
        self._counter_lock = asyncio.Lock()
        self._counter = 0
        self._sem = asyncio.BoundedSemaphore(value)

    async def __aenter__(self) -> None:
        """
        Note that this doesn't release resources properly if it crashes
        in this section.
        """
        async with self._counter_lock:
            if self._counter == 0:
                self._managed.acquire()
            self._counter += 1
            await self._sem.acquire()

    async def __aexit__(self, exc_type, exc, tb) -> None:
        async with self._counter_lock:
            self._sem.release()
            self._counter -= 1
            if self._counter == 0:
                self._managed.release()


class CacheManager:
    """
    Controls access to the inverse index and document cache.
    Operations on the manager may cause reads / writes from / to disk.

    :param executor: The executor to schedule tasks on. If left
                     empty, it uses a new default executor.

    :param concurrent_limit: The number of concurrent reads allowed on
                             the executor.
    """

    def __init__(self,
                 executor: Optional[Executor] = None,
                 concurrent_limit: int = 5):
        # Blocks writes from happening.
        # Also prevents reads from happening when writing
        #
        # Since this gets called in non-asyncio operations, this needs to be
        # from threading.
        self._swap_lock = threading.Lock()
        self._read_manager = ManagedLockCounter(self._swap_lock, concurrent_limit)
        self._executor = executor

        # Enable processing of documents separately from updating the index
        self._update_lock = asyncio.Lock()
        self._update_queue = Queue()

        self._documents = DocumentCache()
        self._index = InverseIndexCache()

    async def query(self, query: List[str]) -> Set[str]:
        """
        Gets a set of document urls that are relevant to the search.

        :param query: A list of keywords / n-grams.
        :return: A new set containing the relevant document urls.
        """
        async with self._read_manager:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(self._executor, self._query, query)

    def _query(self, query: List[str]) -> Set[str]:
        """
        A non-public function to actually run the query operation.

        :param query: A list of keywords / n-grams.
        :return: A new set containing the relevant document urls.
        """
        # Avoid potentially expensive union operation from running in event loop
        return set().union(*[self._index.get_documents(key) for key in query])

    async def update(self, documents: List[Document]) -> None:
        """
        Queues a list of documents for updates. Should not block.

        :param documents: The list of documents to update.
        """
        for document in documents:
            self._update_queue.put(document)

        if not self._update_lock.locked():
            await self._update_lock.acquire()
            loop = asyncio.get_running_loop()
            loop.run_in_executor(self._executor, self._update)

    def _update(self) -> None:
        """
        A non-public function that actually goes through the process of updating
        the documents. Blocking.
        """
        try:
            update_operations: List[DocumentUpdateOperation] = []
            while not self._update_queue.empty():
                new = self._update_queue.get_nowait()
                old = self._documents.get_document(new.url)
                update_operations.append(derive_document_update(old=old, new=new))

                # Replaces the document in the document cache so that if it
                # is update in the queue before this finishes, it will update
                # properly
                self._documents.add_document(new)
        finally:
            self._update_lock.release()

        # Actually try to lock the write operation now.
        with self._swap_lock:
            for op in update_operations:
                op.visit(self._index)
