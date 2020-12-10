from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Dict, List

from common.document import DocumentBuilder
from database import get_db

router = APIRouter(prefix="/document")


class DocumentData(BaseModel):
    word: List[str]
    index: List[List[int]]
    position: List[List[str]]


class Update(BaseModel):
    documents: Dict[str, DocumentData]


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def update_document(update: Update):
    documents = []
    for url in update.documents:
        document_data = update.documents[url]
        document_builder = DocumentBuilder(url=url, title=[""])
        for word in document_data.word:
            document_builder.add(word)
        documents.append(document_builder.document)

    # Schedule update to db
    db = get_db()
    await db.update(documents)  # non-blocking

