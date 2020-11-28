""" 
main.py
"""
from flask import Flask,g
from document_store_interface import interface as dds_interface
from index_db import *
app = Flask(__name__)
app.register_blueprint(dds_interface, url_prefix="/document")

@app.route("/")
def hello() -> str:
    return "Hello World!"

if __name__ == "__main__":
    g.indexes=KeywordCache()
    g.document_update_history=[]
    app.run()
