from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Set

from database import get_db

router = APIRouter(prefix="/query")


class Query(BaseModel):
    flag: List[str]
    word: List[str]


@router.post("/", response_model=Set[str])
async def query(query: Query):
    db = get_db()
    return await db.query(query.word)
