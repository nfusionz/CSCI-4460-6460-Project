from typing import NamedTuple
from datetime import datetime
from dataclasses import dataclass

from common.document import Document


@dataclass
class TimestampedDocument:
    """
    A dataclass containing the timestamp a which a document was received.
    Used to crudely handle receiving multiple updates to the same document within
    a short amount of time.
    """
    time: datetime
    document: Document
