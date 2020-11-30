""" 
main.py
"""
from flask import Flask,g
from UI import interface as ui_interface
'''
from document_store_interface import interface as dds_interface
from index_db import *
'''
app = Flask(__name__)
'''
app.register_blueprint(dds_interface, url_prefix="/document")
'''
app.register_blueprint(ui_interface, url_prefix="/admin")
@app.route("/")
def hello() -> str:
    return "Hello World!"

if __name__ == "__main__":
   
    app.run()
