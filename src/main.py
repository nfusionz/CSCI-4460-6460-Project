#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
main.py - run using the following command:

`uvicorn main:app --reload`
"""

from fastapi import FastAPI, Request
from routers import document, query, ui
# from UI import interface as ui_interface

app = FastAPI()
app.include_router(document.router)
app.include_router(query.router)
app.include_router(ui.router)