"""
database.py - A module that instantiates a single CacheManager to be 
accessed by the application.
"""
from concurrent.futures.thread import ThreadPoolExecutor

from db.cache_manager import CacheManager
from db.document_cache import DocumentCache
from db.inverse_index_cache import InverseIndexCache

DB_WORKER_COUNT = 5

_executor = ThreadPoolExecutor(DB_WORKER_COUNT)
_base = CacheManager(_executor, DB_WORKER_COUNT)


def get_db() -> CacheManager:
    """
    Retrieves the current instance of the database.
    Use this instead of retrieving the database directly
    from this module.

    :return: The global CacheManager.
    """
    return _base
