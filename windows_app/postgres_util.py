from typing import Dict
import json
import requests

#Exampleof tree to add
#new_tree = {'position': '5-5','tag':'P1','tree_type':'Pommier','comments':'No comments','pictures':'http://test.com'}

def login_and_get_token(username:str, password:str)->str:
    URL1='http://farmcedric.herokuapp.com/accounts/login/'
    client = requests.session()
    # Retrieve the CSRF token first
    client.get(URL1)  # sets the cookie
    # login to app and get updated CSRF token
    login_data = dict(username=username, password=password, csrfmiddlewaretoken=client.cookies['csrftoken'])
    client.post(URL1, data=login_data)
    return client

with open("config.json",'r') as f:
    data = json.load(f)
    username = data[0]['auth']['username']
    password = data[0]['auth']['password']

client = login_and_get_token(username,password)
csrftoken = client.cookies['csrftoken']

def get_all_trees()->json:
    response = client.get('http://farmcedric.herokuapp.com/treeapi/trees/', headers={"X-CSRFToken":csrftoken})
    #response = client.get('http://127.0.0.1:8000/treeapi/trees/', headers={"X-CSRFToken":csrftoken})
    return response.json()

def get_tree_from_tag(tag:str)->json:
    data={'tag':tag}
    response = client.get('http://farmcedric.herokuapp.com/treeapi/trees/', params=data, headers={"X-CSRFToken":csrftoken})
    return response.json()

def update_tree(tag:str,new_values:Dict):
    id = get_tree_from_tag(tag)[0]['id']
    data_patch = new_values
    response = client.patch(f'http://farmcedric.herokuapp.com/treeapi/trees/{str(id)}/', data=data_patch, headers={"X-CSRFToken":csrftoken})

def create_tree(values:Dict):
    response = client.post('http://farmcedric.herokuapp.com//treeapi/trees/', values, headers={"X-CSRFToken":csrftoken})
