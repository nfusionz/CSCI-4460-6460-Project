from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_item():
    response = client.post(
        "/document",
        json= {"www.hi.com":{"word":["magic"] ,"index":[[1,2,3]], "position":[["title","body"]]}}
    )
    print( "Can create document: ",response.status_code == 202)
def test_simple_query():
    response = client.post(
        "/query",
        json= {"flag":[], "word":["magic"]}
    )
    print( "Can do simple query: ",response.status_code == 200)    
    print("The response should be \"www.hi.com\": ", response.json())

def test_different_case_query():
    response = client.post(
        "/query",
        json= {"flag":[], "word":["Magic"]}
    )
    print( "Can do different case query: ",response.status_code == 200)    
    print("The response should be \"www.hi.com\": ", response.json())
def test_update_index():
    response = client.post(
        "/document",
        json= {"www.hi.com":{"word":["magic","arknights"] ,"index":[[1,2,3],[4,5]], "position":[["title","body"],["title","body"]]}}
    )
    print( "Can update document: ",response.status_code == 202)
    response = client.post(
        "/query",
        json= {"flag":[], "word":["arknights"]}
    )
    print( "Can do query after update: ",response.status_code == 200)    
    print("The response should be \"www.hi.com\": ", response.json())    
    
def test_update_chinese():
    response = client.post(
        "/document",
        json= {"www.hi.com":{"word":["magic","明日方舟"] ,"index":[[1,2,3],[4,5]], "position":[["title","body"],["title","body"]]}}
    )
    print( "Can update document with chinese characters: ",response.status_code == 202)
    response = client.post(
        "/query",
        json= {"flag":[], "word":["明日方舟"]}
    )
    print( "Can do query after update: ",response.status_code == 200)    
    print("The response should be \"www.hi.com\": ", response.json())
def test_remove_realation():
    response = client.post(
        "/query",
        json= {"flag":[], "word":["arknights"]}
    )
    print( "Can do query after removed realtions: ",response.status_code == 200)    
    print("The response should be nothing: ", response.json())

def test_update_multiple():
    response = client.post(
        "/document",
        json= {"www.hi.com":{"word":["magic","arknights"] ,"index":[[1,2,3],[4,5]], "position":[["title","body"],["title","body"]]},
               "www.hi1.com":{"word":["magic","arknights"] ,"index":[[1,2,3],[4,5]], "position":[["title","body"],["title","body"]]},
               "www.hi2.com":{"word":["arknights","明日方舟"] ,"index":[[1,2,3],[4,5]], "position":[["title","body"],["title","body"]]}}
    )
    print( "Can update multiple urls at a time: ",response.status_code== 202)
    
def test_multiple_word_query():
    response = client.post(
        "/query",
        json= {"flag":[], "word":["magic","arknights"]}
    )
    print( "Can do query after removed realtions: ",response.status_code == 200)    
    print("The response should be {\"www.hi.com\"，\"www.hi1.com\"，\"www.hi2.com\"}: ", response.json())    