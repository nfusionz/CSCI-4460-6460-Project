""" 
UI.py
"""
from flask import Flask,g,render_template, request,Blueprint

def getthefilter():
    dbreader=open("filter.txt","r")
    theset=set()
    while True:
        word=dbreader.readline()
        if word=='':
            break
        word=word.split("\n")[0]
        theset.add(word)
    dbreader.close()
    return theset
def writetofilter(theset):
    dbwriter=open("filter.txt","w")
    for word in theset:
        dbwriter.write(word+"\n")
    dbwriter.close()
    return
interface = Blueprint("admin", __name__)
@interface.route("/",methods=["POST","GET"])
def hello(): 
    return render_template('index.html')

@interface.route("/lastupdate",methods=["POST"])
def lastupdate():
    print("get updates")
    ##Todo:get the global document_update_history
    document_update_history=[]

    document_update_history.append("{\"www.hi.com\":{word:[\"magic\",\"Arknights\"] ,index:[[1,2,3],[7]], position[[\"title\",\"body\"],[\"body\"]]}}")
    
    hist=document_update_history
    tmp=""
    if(len(hist)>0):
        tmp=hist[-1]
    else:
        tmp=""
    return render_template('lastupdate.html',theupdate=tmp)

@interface.route("/showfilter",methods=["POST"])
def showfilter():
    print("show filter")
    ##Todo:get the global wordfilter
    wordfilter=getthefilter()
    words=""
    count=1
    for filthyword in wordfilter:
        if count>21:
            break
        words+=str(count)+". "+filthyword+" "
        count+=1
    return render_template('showfilter.html',theupdate=words)

@interface.route("/rmfilter",methods=["POST"])
def removefilter():
    print("remove filter")
    ##Todo:get the global wordfilter
    wordfilter=getthefilter()
    theworld=request.form["word"]
    if theworld in wordfilter:
        wordfilter.remove(theworld)
        words=theworld+" is not in filter anymore."
    else:
        words=theworld+" is never in the filter"
    writetofilter(wordfilter)
    return render_template('showfilter.html',theupdate=words)

@interface.route("/addfilter",methods=["POST"])
def addfilter():
    print("add filter")
    ##Todo:get the global wordfilter
    wordfilter=getthefilter()
    theworld=request.form["word"]
    wordfilter.add(theworld)
    words=theworld+" is in the filter now."
    writetofilter(wordfilter)
    return render_template('showfilter.html',theupdate=words)


