"""
query_interface.py
"""
from typing import Dict
from flask import Blueprint, Response, request, g

interface = Blueprint("query", __name__)

@interface.route("/", methods=["POST"])
def get_documents() -> Response:
    for document in request.form:
    	pass
    return 
  
