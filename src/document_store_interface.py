"""
document_store_interface.py
"""
from typing import Dict
from flask import Blueprint, request,g

interface = Blueprint("document", __name__)

@interface.route("/", methods=["POST"])
def update_document() -> None:
    for document in request.form:
    	pass
    return 
  
@interface.route("/<name>")
def get_document(name: str) -> Dict[str, str]:
    result = "ayyy" + name
    return { "result": result }
