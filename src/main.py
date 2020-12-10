""" 
main.py - run using the following command:

`uvicorn main:app --reload`
"""

from fastapi import FastAPI
from routers import document, query
# from UI import interface as ui_interface

app = FastAPI()
app.include_router(document.router)
app.include_router(query.router)

@app.route("/")
async def root() -> str:
    return "Hello World!"
