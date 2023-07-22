import base64
import json
from dotenv import load_dotenv
import os
from requests import get, post
import mysql.connector

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes)
    auth_base64_string = auth_base64.decode("utf-8")

    token_url = "https://accounts.spotify.com/api/token"
    header = {
        "Authorization": "Basic " + auth_base64_string,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    result = post(token_url, headers=header, data=data)
    json_result = json.loads(result.content)

    token = json_result["access_token"]

    return token

def get_auth_header(token):
    return { "Authorization": "Bearer " + token}

def get_trackID(trackName):
    token = get_token()
    url = "https://api.spotify.com/v1/search?q="+ trackName +"&type=track&limit=1"
    header = get_auth_header(token=token)
    result = get(url, headers=header)
    print("here")
    json_result = json.loads(result.content)
    id = json_result["tracks"]["items"][0]["id"]

    return id
