#!/usr/local/bin/python
# -*- coding: utf-8 -*-


"""
UI.py
"""
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="templates")

@router.get("")
@router.post("")
def hello(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def getthefilter():
    dbreader = open("filter.txt", "r")
    theset = set()
    while True:
        word = dbreader.readline()
        if word == '':
            break
        word = word.split("\n")[0]
        theset.add(word)
    dbreader.close()
    return theset


def writetofilter(theset):
    dbwriter = open("filter.txt", "w")
    for word in theset:
        dbwriter.write(word + "\n")
    dbwriter.close()
    return


@router.post("/lastupdate")
def lastupdate(request: Request):
    print("get updates")
    #  Todo:get the global document_update_history
    document_update_history = [
        "{\"www.hi.com\":{word:[\"magic\",\"Arknights\"] ,index:[[1,2,3],[7]], position[[\"title\",\"body\"],[\"body\"]]}}"]

    hist = document_update_history
    tmp = ""
    if len(hist) > 0:
        tmp = hist[-1]
    else:
        tmp = ""
    return templates.TemplateResponse("lastupdate.html", {"request": request, "theupdate": tmp})

@router.post("/showfilter")
def showfilter(request: Request):
    print("show filter")
    #  Todo:get the global wordfilter
    wordfilter = getthefilter()
    words = ""
    count = 1
    for filthyword in wordfilter:
        if count > 21:
            break
        words += str(count) + ". " + filthyword + " "
        count += 1
    return templates.TemplateResponse("showfilter.html", {"request": request, "theupdate": words})

@router.post("/rmfilter")
def removefilter(request: Request, word: str = Form(...)):
    print("remove filter")
    #  Todo:get the global wordfilter
    wordfilter = getthefilter()
    if word in wordfilter:
        wordfilter.remove(word)
        words = word + " is not in filter anymore."
    else:
        words = word + " is never in the filter"
    writetofilter(wordfilter)
    return templates.TemplateResponse("showfilter.html", {"request": request, "theupdate": words})


@router.post("/addfilter")
def addfilter(request: Request, word: str = Form(...)):
    print("add filter")
    ##Todo:get the global wordfilter
    wordfilter = getthefilter()
    wordfilter.add(word)
    words = word + " is in the filter now."
    writetofilter(wordfilter)
    return templates.TemplateResponse("showfilter.html", {"request": request, "theupdate": words})
