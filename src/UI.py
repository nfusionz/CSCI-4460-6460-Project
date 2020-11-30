""" 
UI.py
"""
from flask import Flask,g,render_template, request,Blueprint

interface = Blueprint("admin", __name__)
@interface.route("/",methods=["POST","GET"])
def hello():
    
    wordfilter=set()    
    wordfilter.add("fuck you")    
    return render_template('index.html')

@interface.route("/lastupdate",methods=["POST"])
def lastupdate():
    print("get updates")
    ##Todo:get the global document_update_history
    document_update_history=[]
    '''
    document_update_history.append({"a":"mmm","b":["mmm","mmm"]})
    '''
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
    wordfilter=set()
    """
    wordfilter.add("Fuck")
    wordfilter.add("Fuck You")
    """
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
    wordfilter=set()
    theworld=request.form["word"]
    if theworld in wordfilter:
        wordfilter.remove(theworld)
        words=theworld+" is not in filter anymore."
    else:
        words=theworld+" is never in the filter"
    return render_template('showfilter.html',theupdate=words)

@interface.route("/addfilter",methods=["POST"])
def addfilter():
    print("add filter")
    ##Todo:get the global wordfilter
    wordfilter=set()
    theworld=request.form["word"]
    wordfilter.add(theworld)
    words=theworld+" is in the filter now."    
    return render_template('showfilter.html',theupdate=words)


